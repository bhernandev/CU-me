from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
from bs4 import BeautifulSoup

import re
from operator import itemgetter

def classSearch(college, term, dept, number, selector, session):
    display = Display(visible=0, size=(800, 600))
    display.start()
    browser = webdriver.Chrome()

    browser.get('https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/GUEST/HRMxS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL')
    deptName = ""
    collegeName = ""
    try:
        collegeSelect = Select(browser.find_element_by_name('CLASS_SRCH_WRK2_INSTITUTION$31$'))
        collegeSelect.select_by_value(college)
        collegeName = collegeSelect.first_selected_option.text
    except:
        browser.quit()
        return {"error": "Invalid college query"}
    browser.find_element_by_name('CLASS_SRCH_WRK2_INSTITUTION$31$').submit()
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="CLASS_SRCH_WRK2_STRM$35$"]/option[2]'))
        )
    except:
        browser.quit()
        return {"result": "Not found"}
    try:
        termSelect = Select(browser.find_element_by_name('CLASS_SRCH_WRK2_STRM$35$'))
        termSelect.select_by_value(term)
    except:
        browser.quit()
        return {"error": "Invalid term query"}
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="SSR_CLSRCH_WRK_SUBJECT_SRCH$0"]/option[4]'))
        )
    except:
        browser.quit()
        return {"result": "Not found"}
    try:
        deptSelect = Select(browser.find_element_by_name('SSR_CLSRCH_WRK_SUBJECT_SRCH$0'))
        deptSelect.select_by_value(dept)
        deptName = deptSelect.first_selected_option.text
    except:
        browser.quit()
        return {"error": "Invalid department query"}
    try:
        selectorSelect = Select(browser.find_element_by_name('SSR_CLSRCH_WRK_SSR_EXACT_MATCH1$1'))
        selectorSelect.select_by_value(selector)
    except:
        browser.quit()
        return {"error": "Invalid contains/exact match selector query"}
    try:
        numberInput = browser.find_element_by_name('SSR_CLSRCH_WRK_CATALOG_NBR$1')
        numberInput.send_keys(number)
    except:
        browser.quit()
        return {"error": "Invalid class number query"}
    try:
        sessionSelect = Select(browser.find_element_by_name('SSR_CLSRCH_WRK_SESSION_CODE$6'))
        sessionSelect.select_by_value(session)
    except:
        browser.quit()
        return {"error": "Invalid session query"}

    browser.find_element_by_name('CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH').click()

    courses = []
    try:
        element = WebDriverWait(browser, 10).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "PAPAGETITLE"), 'Search Results')
        )
    except:
        browser.quit()
        return {"error": "Not found"}

    courseList = browser.find_elements_by_xpath('//*[@id="ACE_$ICField$4$$0"]/tbody/tr')
    courseList.pop(0)

    sectionCounter = 0
    for course in courseList:
        courseName = course.find_element_by_id('win0divSSR_CLSRSLT_WRK_GROUPBOX2GP$' + str(courseList.index(course))).text
        sectionList = course.find_elements_by_xpath('//*[@id="ACE_$ICField48$' + str(courseList.index(course)) + '"]/tbody/tr')
        sections = []
        for section in sectionList:
            if sectionList.index(section) % 2 == 1:
                if (section.find_element_by_class_name('SSSIMAGECENTER').get_attribute('alt') == 'Open'):
                    sectionTimes = section.find_element_by_id('MTG_DAYTIME$' + str(sectionCounter)).text
                    sectionRoom = section.find_element_by_id('MTG_ROOM$' + str(sectionCounter)).text
                    sectionInstructor = section.find_element_by_id('MTG_INSTR$' + str(sectionCounter)).text
                    sectionMeetingDates = section.find_element_by_id('MTG_TOPIC$' + str(sectionCounter)).text

                    searchProfName = sectionInstructor.split(',')[0]
                    instructorGrades = {}
                    if (searchProfName != "Staff"):
                        instructorGrades = professorRating(searchProfName, collegeName, deptName.split('-')[1].strip().split(' '))

                    sectionDict = {'times': sectionTimes, 'room': sectionRoom, 'instructor': sectionInstructor, 'instructorGrades': instructorGrades, 'meetingDates': sectionMeetingDates}
                    sections.append(sectionDict)
                sectionCounter += 1

        sortedSections = sorted(sections, key=getGrade , reverse=True)
        courseDict = {'courseName': courseName, 'sections': sortedSections}
        if courseDict['sections']:
            courses.append(courseDict)

    browser.quit()
    return {"departmentName": deptName, "courses": courses}


def professorRating(name, school, dept):
    print(name)
    query = {'query': name}
    searchResult = requests.get('http://www.ratemyprofessors.com/search.jsp', params=query)
    soup = BeautifulSoup(searchResult.text, 'html.parser')
    listings = soup.find_all('li', class_="listing PROFESSOR")
    if listings:
        for listing in listings:
            span = listing.find('span', class_="sub")
            searchList = span.string.split(',')
            searchSchool = searchList[0]
            searchDept = searchList[1].strip()
            if (searchSchool == school and any(depWord in searchDept for depWord in dept)):
                try:
                    detailsLink = 'http://www.ratemyprofessors.com' + listing.find('a').get('href')
                    detailsResult = requests.get(detailsLink)
                    soup = BeautifulSoup(detailsResult.text, 'html.parser')
                    allGrades = soup.find_all('div', class_='grade')
                    grades = {'overall': allGrades[0].text, 'difficulty': allGrades[2].text.strip()}
                    return grades
                except:
                    return {}
        return {}
    else:
        return {}

def getGrade(item):
    key = '0'
    try:
        key = itemgetter('overall')(item['instructorGrades'])
    except:
        key = '0'
    return key

def degreeClasses(userName, passWord):
    display = Display(visible=0, size=(800, 600))
    display.start()
    browser = webdriver.Chrome()

    browser.get('https://cunyportal.cuny.edu/cpr/authenticate/portal_login.jsp')

    userid = browser.find_element_by_id("userid")
    password = browser.find_element_by_id("password")
    userid.send_keys(userName)
    password.send_keys(passWord)
    browser.find_element_by_name("image").click()

    try:
        browser.get("https://degreeworks.cuny.edu/cuny_redirector.cgi")
    except:
        browser.quit()
        return {'error': 'Could not load Degreeworks'}
    try:
        browser.switch_to_frame('frBody')
    except:
        browser.quit()
        return {'error': 'Could not switch to course info frame'}
    try:
        element = WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'SchoolName'))
        )
    except:
        browser.quit()
        return {'error': 'Could not find school'}

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    schoolName = soup.find('span', class_="SchoolName").text
    needed = soup.find_all('tr', class_="bgLight0")
    allReqs = []
    previousReq = None
    for req in needed:
        dataBlocks = req.find_all('td', class_="RuleAdviceData")
        for dataBlock in dataBlocks:
            if (dataBlock is not None and ("Credits" in dataBlock.text or "Class" in dataBlock.text)):
                reqWord = ""
                if ("Credits" in dataBlock.text):
                    reqWord = "credits"
                else:
                    reqWord = "class"
                name = ""
                try:
                    name = req.find('td', class_="RuleLabelTitleNeeded").text
                except:
                    if previousReq is not None:
                        name = previousReq.find('td', class_="RuleLabelTitleNeeded").text
                data = dataBlock.text
                data = " ".join(data.split())
                numOfCredits = int(re.search(r'\d+', data).group())
                classesThatFulfillReq = []
                allMatches = re.findall(r'([A-Z]{3,5}((?![A-Z]).)*)', data)
                allMatchesList = []
                for match in allMatches:
                    allMatchesList.append(match[0])
                for match in allMatchesList:
                    classCode = match.split()[0]
                    numberList = [int(s) for s in match.split() if s.isdigit()]
                    notFullNumberList = re.findall(r'\d{1,3}@', match)
                    for number in numberList:
                        newClass = {'code': classCode, 'number': number}
                        classesThatFulfillReq.append(newClass)
                    for number in notFullNumberList:
                        newClass = {'code': classCode, 'number': number}
                        classesThatFulfillReq.append(newClass)

                newReq = {'name': name, 'credits': numOfCredits, 'classes': classesThatFulfillReq, 'reqWord': reqWord}
                allReqs.append(newReq)
        previousReq = req
    reqsResponse = {'schoolName': schoolName, 'allRequirements': allReqs}
    browser.quit()
    return reqsResponse
