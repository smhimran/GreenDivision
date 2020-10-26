#!/usr/bin/env python3
from urllib.request import urlopen as uReq, Request
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time
import datetime




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
		
		url = "https://www.urionlinejudge.com.br/judge/en/profile/"+self.__user_id+"?page="+page_no+"&sort=Ranks.created&direction=asc"
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
			td_data = td.find_all("td");
			
			if len(td_data) == 7:
				try:
					prob_no = ET.fromstring(str(td_data[0]))
					sol_lang = ET.fromstring(str(td_data[4]))
					sol_time = ET.fromstring(str(td_data[6]))
					
					prob_no = prob_no.find('a').text.strip()
					sol_lang = sol_lang.text.strip()
					sol_time = sol_time.text.strip()
					sol_time = datetime.datetime.strptime(sol_time, '%m/%d/%y, %I:%M:%S %p')

					problem_details = [prob_no, sol_lang, sol_time]
					# print(problem_details)

					if problem_details[0] in self.__green_problems_list:
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

			data = soup.find("div",attrs={"id":"table-info"})
			return int(data.contents[0].split()[2])
		except:
			return int(0)

	def get_list(self):
		total_page = self.__get_total_page_number()

		for page_no in range(self.__total_scraped, total_page+1):
			print("scraping page :", page_no)
			self.__get_solved_problems(str(page_no))

		return [self.__final_list, str(total_page)]
#----------------------------------------------------------------------------------------------------------





#----------------------------------------------------------------------------------------------------------
# testing uri scraper

fp = open("in.txt")
unsolved_green_problem_list = fp.read().split()
fp.close()

total_scraped = "0"
user_id = "258234" #input("user_id - ")


# calculate runtime
# start_time = time.time()

# starting scraper
profile = uri_scraper(unsolved_green_problem_list, total_scraped, user_id)
profile = profile.get_list()

# total time and page
# print(">>Scraper Runtime: %s seconds" % (time.time() - start_time))
# print("Total page scraped :", profile[1], "\n")

# print("Total problem solved -", len(profile[0]))
# print("Top 10 submission :")
# print("-----------------------------------------------")
# for i in range(10):
# 	print(profile[0][i][0],'|', profile[0][i][1],'|', profile[0][i][2].strftime("%a %d-%b-%Y, %I:%M:%S %p"))


# info of a problem solved by user
# for i in profile[0]:
# 	if "1150" == i[0]:
# 		print(i[0],'|', i[1],'|', i[2].strftime("%a %d-%b-%Y, %I:%M:%S %p"))


#----------------------------------------------------------------------------------------------------------
