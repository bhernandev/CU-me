import requests
from lxml import html
from lxml.html import parse

BASE_URL = 'https://www.ratemyprofessors.com/'
SEARCH_ENDPOINT = 'search.jsp?query='
DATA_ENDPOINT = 'ShowRatings.jsp?tid='

# HARD CODED
name_of_professor = 'Daniel, David B.'
college_of_student = 'James Madison University, Psychology'
# HARD CODED


page = requests.get(BASE_URL + SEARCH_ENDPOINT + name_of_professor)  # website
tree = html.fromstring(page.content)


# create list of professors
professors = tree.xpath('//span[@class="main"]/text()')
colleges = tree.xpath('//span[@class="sub"]/text()')
tid = tree.xpath('//li[@class="listing PROFESSOR"]/a/@href')
# print 'professors', professors
# print 'colleges', colleges


# dictionary keys are colleges values are dicts of {professor: search_tid}
students_professor_dict = {}

for i in range(len(professors)):
    students_professor_dict[colleges[i]] = dict([(professors[i], tid[i])])

# students_professor = dict(zip(colleges, zip(professors, tid)))
"""
for keys, values in students_professor_dict.items():
    print ('key', keys)
    print ('value', values)
"""

# logic here
#---------------------------------------------------
prof_tid = students_professor_dict[
    college_of_student][name_of_professor]

profile_page = requests.get(
    BASE_URL + prof_tid)


profile_tree = html.fromstring(profile_page.content)
grade = profile_tree.xpath(
    '//div[@class="breakdown-container"]/div/div/text()')[0]

print grade
