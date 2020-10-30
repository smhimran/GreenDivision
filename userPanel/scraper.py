#!/usr/bin/env python3
from urllib.request import urlopen as uReq, Request
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time
import datetime
from .models import Problem, Profile, Submission
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
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

        for submission in profile[0]:
            # print(submission[0])
            problem = Problem.objects.get(problem_id=submission[0])
            solve = Submission.objects.create(user=user, problem=problem,
                                              language=submission[1], dateTime=submission[2])

    fp = open("scrapper_log.txt", 'a')
    fp.write("\n\n>>Scraper Runtime: %s seconds\n" %
             (time.time() - start_time))
    fp.write(
        "\n----------------------------------------------------------------------\n\n")
    fp.close()
    print('Scrapper ended')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_data, 'interval', minutes=1)
    scheduler.start()


# ----------------------------------------------------------------------------------------------------------
