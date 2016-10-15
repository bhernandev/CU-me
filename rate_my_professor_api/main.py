import requests
from flask import Flask, redirect, request, session
from lxml import html
from lxml.html import parse

app = Flask(__name__)

BASE_URL = 'https://www.ratemyprofessors.com/'
SEARCH_ENDPOINT = 'search.jsp?query='
DATA_ENDPOINT = 'ShowRatings.jsp?tid='

"""
for keys, values in students_professor_dict.items():
    print ('key', keys)
    print ('value', values)
"""

# logic here
#---------------------------------------------------


@app.route("/", methods=['GET'])
def get_average():
    name_of_professor = args['name_of_professor']
    college_of_student = args['college_of_student']

    page = requests.get(BASE_URL + SEARCH_ENDPOINT +
                        name_of_professor)  # website
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

        # logic
        prof_tid = students_professor_dict[
            college_of_student][name_of_professor]

        profile_page = requests.get(BASE_URL + prof_tid)
        profile_tree = html.fromstring(profile_page.content)
        grade = profile_tree.xpath(
            '//div[@class="breakdown-container"]/div/div/text()')[0]
        # end logic

    return grade

if __name__ == "__main__":
    app.run(debug=True)
