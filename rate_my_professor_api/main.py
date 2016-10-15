import requests
from lxml import html
from lxml.html import parse

BASE_URL = 'https://www.ratemyprofessors.com/'
SEARCH_ENDPOINT = 'search.jsp?query='
DATA_ENDPOINT = 'ShowRatings.jsp?tid='

# HARD CODED
name_of_professor = 'david'
college_of_student = 'Queens College, Anthropology'
# HARD CODED


page = requests.get(BASE_URL + SEARCH_ENDPOINT + name_of_professor)  # website
tree = html.fromstring(page.content)


# create list of professors
professors = tree.xpath('//span[@class="main"]/text()')
colleges = tree.xpath('//span[@class="sub"]/text()')
tid = tree.xpath('//li[@class="listing PROFESSOR"]/a/@href')
print 'tid', tid
# print 'professors', professors
# print 'colleges', colleges


# dictionary keys are colleges values are dicts of {professor: search_tid}
students_professor_dict = {}
for i in range(len(professors)):
    students_professor_dict[colleges[i]] = professors[i]
# students_professor = dict(zip(colleges, zip(professors, tid)))

for keys, values in students_professor_dict.items():
    print ('key', keys)
    print ('value', values)

# logic here
#---------------------------------------------------
"""
profile_page = requests.get(
    BASE_URL + students_professor[])
"""
