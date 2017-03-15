#!/home/mikmaks/.virtualenvs/cume/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datetime

import json

def fetch():
    searchForm = {}

    browser = webdriver.PhantomJS('/usr/local/share/phantomjs-1.9.8-linux-x86_64/bin/phantomjs')
    browser.maximize_window()

    browser.get('https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/GUEST/HRMxS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL')

    #COLLEGES
    collegesList = []

    collegeElements = browser.find_elements_by_xpath('//*[@id="CLASS_SRCH_WRK2_INSTITUTION$31$"]/option')
    collegeElements.pop(0)
    colleges = []
    for element in collegeElements:
        colleges.append({'name': element.text, 'code': element.get_attribute('value')})

    for college in colleges:
        newCollege = {'name': college['name'], 'code': college['code']}

        collegeSelect = Select(browser.find_element_by_name('CLASS_SRCH_WRK2_INSTITUTION$31$'))
        collegeSelect.select_by_value(college['code'])
        browser.find_element_by_name('CLASS_SRCH_WRK2_INSTITUTION$31$').submit()

        #CAREERS
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="SSR_CLSRCH_WRK_ACAD_CAREER$2"]/option[2]'))
            )
        except:
            browser.quit()
            return {"result": "Careers not found"}

        careersList = []
        careers = browser.find_elements_by_xpath('//*[@id="SSR_CLSRCH_WRK_ACAD_CAREER$2"]/option')
        careers.pop(0)

        for career in careers:
            newCareer = {'name': career.text, 'code': career.get_attribute('value')}
            careersList.append(newCareer)

        newCollege['careers'] = careersList

        #CAMPUSES
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="SSR_CLSRCH_WRK_CAMPUS$14"]/option[2]'))
            )
        except:
            browser.quit()
            return {"result": "Campuses not found"}

        campusList = []
        campuses = browser.find_elements_by_xpath('//*[@id="SSR_CLSRCH_WRK_CAMPUS$14"]/option')
        campuses.pop(0)

        for campus in campuses:
            newCampus = {'name': campus.text, 'code': campus.get_attribute('value')}
            campusList.append(newCampus)

        newCollege['campuses'] = campusList

        #LOCATIONS
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="SSR_CLSRCH_WRK_LOCATION$15"]/option[2]'))
            )
        except:
            browser.quit()
            return {"result": "Locations not found"}

        locationsList = []
        locations = browser.find_elements_by_xpath('//*[@id="SSR_CLSRCH_WRK_LOCATION$15"]/option')
        locations.pop(0)

        for location in locations:
            newLocation = {'name': location.text, 'code': location.get_attribute('value')}
            locationsList.append(newLocation)

        newCollege['locations'] = locationsList

        #TERMS
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="CLASS_SRCH_WRK2_STRM$35$"]/option[2]'))
            )
        except:
            browser.quit()
            return {"result": "Terms not found"}

        termsList = []
        termElements = browser.find_elements_by_xpath('//*[@id="CLASS_SRCH_WRK2_STRM$35$"]/option')
        termElements.pop(0)
        terms = []
        for element in termElements:
            terms.append({'name': element.text, 'code': element.get_attribute('value')})
        for term in terms:
            newTerm = {'name': term['name'], 'code': term['code']}
            subjectsList = []

            termSelect = Select(browser.find_element_by_name('CLASS_SRCH_WRK2_STRM$35$'))
            termSelect.select_by_value(term['code'])
            browser.find_element_by_name('CLASS_SRCH_WRK2_STRM$35$').submit()

            #SUBJECTS
            try:
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="SSR_CLSRCH_WRK_SUBJECT_SRCH$0"]/option[2]'))
                )
            except:
                resultG = 'subject not found'
            else:
                subjectElements = browser.find_elements_by_xpath('//*[@id="SSR_CLSRCH_WRK_SUBJECT_SRCH$0"]/option')
                subjectElements.pop(0)
                subjects = []
                for element in subjectElements:
                    subjects.append({'name': element.text, 'code': element.get_attribute('value')})
                for subject in subjects:
                    newSubject = {'name': subject['name'], 'code': subject['code']}
                    subjectsList.append(newSubject)

                newTerm['subjects'] = subjectsList

            termsList.append(newTerm)

        newCollege['terms'] = termsList

        collegesList.append(newCollege)

    searchForm['colleges'] = collegesList
    searchForm['updated'] = str(datetime.datetime.now())

    outputFile = open('/home/mikmaks/dev/CUNYsecond/cume/schedule/form.txt', 'w')
    outputFile.write(json.dumps(searchForm))
    outputFile.close()

    browser.quit()

def wait(seconds):
    startTime = time()
    currentTime = time()
    while (currentTime - startTime < seconds):
        currentTime = time()
        continue
    return

fetch()
