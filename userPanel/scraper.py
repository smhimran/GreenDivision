#!/usr/bin/env python3
from urllib.request import urlopen as uReq, Request

import pytz
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time
import datetime
from .models import Problem, Profile, Submission
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from django.utils.timezone import make_aware
from django.db.models import Q


# ----------------------------------------------------------------------------------------------------------
# ## imported libraries

# 1. urllib
# 2. BeaytifullSoup
# 3. xml
# 4. datetime
# 5. time (optionl)

# ## input

# during initialization uri_scraer class take
# 1. a list of green division problem in string type and they are unsolved by the user so far.
# 2. total page scraped last time
# 3. user id

# ## output

# get_list method of uri_scraper class will return a single list [LS]
# LS contain a list [A] and a string [B]

# 1. list [A] will contain the information of problems solved by user this information is a list [sol]
# 2. list [sol] contain: "problem id", "submission language", datetime_object
# 3. datetime_object is python buit in date type object, which is created for raw string and can be used simply for use.
# 4. [B] string this total page scraped so far
# --------------------------------------------------------------------------------------------------------------------


class uri_scraper(object):

    def __init__(self, unsolved_green_problem_list, total_scraped, user_id):
        self.__green_problems_list = set(unsolved_green_problem_list)
        self.__user_id = user_id
        self.__total_scraped = max(int(total_scraped), 1)
        self.__AC = set()
        self.__final_list = list()

    def __get_solved_problems(self, page_no):

        url = "https://www.urionlinejudge.com.br/judge/en/profile/" + \
            self.__user_id+"?page="+page_no+"&sort=Ranks.created&direction=asc"
        hdr = {'User-Agent': 'Mozilla/5.0'}

        try:
            req = Request(url, headers=hdr)
            html = uReq(req, timeout=5)
            html = html.read().decode()

            soup = BeautifulSoup(html, "lxml")

            tr_data = soup.find_all("tr")
        except:
            return

        for td in tr_data:
            td_data = td.find_all("td")
            # print(td_data)
            if len(td_data) == 7:
                try:
                    prob_no = ET.fromstring(str(td_data[0]))
                    sol_lang = ET.fromstring(str(td_data[4]))
                    sol_time = ET.fromstring(str(td_data[6]))

                    prob_no = prob_no.find('a').text.strip()
                    sol_lang = sol_lang.text.strip()
                    sol_time = sol_time.text.strip()
                    sol_time = datetime.datetime.strptime(
                        sol_time, '%m/%d/%y, %I:%M:%S %p')

                    sol_time = pytz.timezone("UTC").localize(sol_time)

                    problem_details = [prob_no, sol_lang, sol_time]
                    # print(problem_details)

                    if problem_details[0] in self.__green_problems_list:
                        # print('Prob_in_scrap: {}'.format(problem_details[0]))
                        if problem_details[0] not in self.__AC:
                            self.__final_list.append(problem_details)
                            self.__AC.add(problem_details[0])
                except:
                    continue
        return

    def __get_total_page_number(self):

        url = "https://www.urionlinejudge.com.br/judge/en/profile/"+self.__user_id
        hdr = {'User-Agent': 'Mozilla/5.0'}

        try:
            req = Request(url, headers=hdr)
            html = uReq(req)
            html = html.read().decode()

            soup = BeautifulSoup(html, 'html.parser')

            data = soup.find("div", attrs={"id": "table-info"})
            return int(data.contents[0].split()[2])
        except:
            return int(0)

    def get_list(self):
        total_page = self.__get_total_page_number()

        for page_no in range(self.__total_scraped, total_page+1):
            self.__get_solved_problems(str(page_no))

        return [self.__final_list, str(total_page)]
# ----------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------
# testing uri scraper


# total_scraped = "0"
# user_id = "258234" #input("user_id - ")


# calculate runtime
# start_time = time.time()

# starting scraper


def scrape_data():
    print('Scrapper Started')
    start_time = time.time()
    users = Profile.objects.filter(Q(status='Active') | Q(
        status='Requested') | Q(status='Eligible'))
    problems = Problem.objects.all()

    timezone.now()
    # print(users)
    fp = open("scrapper_log.txt", 'a')
    fp.write('Scrapper started at: {}\n'.format(datetime.datetime.now()))
    fp.close()
    for user in users:
        # print(user.name)
        user_id = user.uri_link[51:]
        solved_problems = []
        submissions = Submission.objects.filter(
            user=user)
        for submission in submissions:
            # print('problem id: {}'.format(submission.problem.problem_id))
            solved_problems.append(submission.problem.problem_id)

        # print(solved_problems)
        unsolved_green_problem_list = []
        for problem in problems:
            # print(problem.problem_id)
            if problem.problem_id not in solved_problems:
                # print('problem s id: {}'.format(problem.problem_id))
                unsolved_green_problem_list.append(str(problem.problem_id))

        # print(unsolved_green_problem_list)
        total_scraped = user.total_scrapped
        try:
            profile = uri_scraper(
                unsolved_green_problem_list, total_scraped, user_id)
            profile = profile.get_list()
        except Exception as e:
            fp = open("scrapper_log.txt", 'a')
            fp.write('Error for user {}\n'.format(user.varsity_id))
            fp.write(e)
            fp.close()

        user.total_scrapped = profile[1]
        # print(profile[0])

        if len(profile[0]):
            user.solve_count = user.solve_count + len(profile[0])
            if user.status == 'Requested':
                user.status = 'Active'
        else:
            if user.status == 'Requested':
                user.status = 'Inactive'

        if user.status == 'Request from Blue':
            user.status = 'Blue'

        user.save()

        min_date = datetime.datetime.now(pytz.timezone("Asia/Dhaka"))

        for submission in profile[0]:
            # print(submission[0])
            min_date = min(min_date, submission[2])
            problem = Problem.objects.get(problem_id=submission[0])
            solve = Submission.objects.create(user=user, problem=problem,
                                              language=submission[1], dateTime=submission[2])

        user.last_submission_time = min_date

        user.save()

        submissions = Submission.objects.filter(user=user).order_by('problem')
        # problems = Problem.objects.all()

        beginner = list(Problem.objects.filter(category="Input/Output"))
        beginner_count = len(beginner)

        condition = list(Problem.objects.filter(category="Condition"))
        condition_count = len(condition)

        geo = list(Problem.objects.filter(category="Geometry"))
        geo_count = len(geo)

        math = list(Problem.objects.filter(category="Simple Math"))
        math_count = len(math)

        loop = list(Problem.objects.filter(category="Loop"))
        loop_count = len(loop)

        array = list(Problem.objects.filter(category="Array/Simple DS"))
        array_count = len(array)

        string = list(Problem.objects.filter(category="String"))
        string_count = len(string)

        adhoc = list(Problem.objects.filter(category="Ad-hoc"))
        adhoc_count = len(adhoc)

        beginner_solved = 0
        condition_solved = 0
        math_solved = 0
        loop_solved = 0
        geo_solved = 0
        array_solved = 0
        string_solved = 0
        adhoc_solved = 0

        for problem in beginner:
            solve_time = submissions.filter(problem=problem)

            if solve_time.exists():
                beginner_solved += 1

        for problem in condition:
            solve_time = submissions.filter(problem=problem)

            if solve_time.exists():
                condition_solved += 1

        for problem in math:
            solve_time = submissions.filter(problem=problem)

            if solve_time.exists():
                math_solved += 1

        for problem in loop:
            solve_time = submissions.filter(problem=problem)

            if solve_time.exists():
                loop_solved += 1

        for problem in array:
            solve_time = submissions.filter(problem=problem)

            if solve_time.exists():
                array_solved += 1

        for problem in string:
            solve_time = submissions.filter(problem=problem)

            if solve_time.exists():
                string_solved += 1

        for problem in adhoc:
            solve_time = submissions.filter(problem=problem)

            if solve_time.exists():
                adhoc_solved += 1

        for problem in geo:
            solve_time = submissions.filter(problem=problem)

            if solve_time.exists():
                geo_solved += 1

        beginner_percentage = (beginner_solved / beginner_count) * 100
        math_percentage = (math_solved / math_count) * 100
        condition_percentage = (condition_solved / condition_count) * 100
        loop_percentage = (loop_solved / loop_count) * 100
        geo_percentage = (geo_solved / geo_count) * 100
        array_percentage = (array_solved / array_count) * 100
        string_percentage = (string_solved / string_count) * 100
        adhoc_percentage = (adhoc_solved / adhoc_count) * 100

        eligible = True

        if beginner_percentage < 60:
            eligible = False

        if math_percentage < 60:
            eligible = False

        if condition_percentage < 60:
            eligible = False

        if loop_percentage < 60:
            eligible = False

        if geo_percentage < 60:
            eligible = False

        if array_percentage < 60:
            eligible = False

        if string_percentage < 60:
            eligible = False

        if adhoc_percentage < 60:
            eligible = False

        if eligible == True:
            user.status = "Eligible"

        user.save()


    fp = open("scrapper_log.txt", 'a')
    fp.write("\n\n>>Scraper Runtime: %s seconds\n" %
             (time.time() - start_time))
    fp.write(
        "\n----------------------------------------------------------------------\n\n")
    fp.close()
    print('Scrapper ended')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_data, 'interval', minutes=25, max_instances=1)
    scheduler.start()


# ----------------------------------------------------------------------------------------------------------
