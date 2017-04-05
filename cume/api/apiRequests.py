from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

#selenium waiting for elements
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#for converting xml to html
from time import time
import lxml.etree as ET
from io import StringIO

import requests  #for RateMyProfessors requests
from bs4 import BeautifulSoup

import re
from operator import itemgetter

#searches for classes through CUNYFirst based on arguments
#college             the college to search for classes at
#term                the term (semester) to search for
#dept                the department, e.g. GTECH, STAT
#number              the course number, e.g. 150, 127
#selector            is the course number given EXACTLY the full course number or does it CONTAIN it
#session             the session, e.g. Winter
#classNbr            the class number i.e. 10452
#courseCareer        e.g. undergraduate, graduate
#reqdes              the requirement designation, e.g. Scientific World
#instructorName      the instructor to search for
#instructorSelector  same as selector except for instructors
#RETURNS JSON with the found classes matching the query
def classSearch(college, term, dept, number, selector, session, classNbr, courseCareer, reqdes, instructorName, instructorSelector):
    browser = webdriver.PhantomJS()  #create a new Selenium browser
    browser.maximize_window()

    #go to CUNYFirst guest search
    browser.get('https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/GUEST/HRMxS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL')
    deptName = ""
    collegeName = ""

    #college select
    try:
        collegeSelect = Select(browser.find_element_by_name('CLASS_SRCH_WRK2_INSTITUTION$31$'))
        collegeSelect.select_by_value(college)
        collegeName = collegeSelect.first_selected_option.text  #store the college name to search for professors for this college in RateMyProfessors
    except:
        browser.quit()
        return {"error": "Invalid college query"}
    browser.find_element_by_name('CLASS_SRCH_WRK2_INSTITUTION$31$').submit()
    #term select
    try:
        #wait until the term select is populated with options
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="CLASS_SRCH_WRK2_STRM$35$"]/option[2]'))
        )
    except:
        browser.quit()
        return {"error": "Not found term options"}
    try:
        termSelect = Select(browser.find_element_by_name('CLASS_SRCH_WRK2_STRM$35$'))
        termSelect.select_by_value(term)
    except:
        browser.quit()
        return {"error": "Invalid term query"}
    wait(1)
    #dept select
    try:
        #wait until department select is populated with options
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="SSR_CLSRCH_WRK_SUBJECT_SRCH$0"]/option[4]'))
        )
    except:
        browser.quit()
        return {"error": "Not found subject options"}
    try:
        deptSelect = Select(browser.find_element_by_name('SSR_CLSRCH_WRK_SUBJECT_SRCH$0'))
        deptSelect.select_by_value(dept)
        deptName = deptSelect.first_selected_option.text
    except:
        browser.quit()
        return {"error": "Invalid department query"}
    #course number selector select
    try:
        selectorSelect = Select(browser.find_element_by_name('SSR_CLSRCH_WRK_SSR_EXACT_MATCH1$1'))
        selectorSelect.select_by_value(selector)
    except:
        browser.quit()
        return {"error": "Invalid contains/exact match selector query"}
    #course number input
    try:
        numberInput = browser.find_element_by_name('SSR_CLSRCH_WRK_CATALOG_NBR$1')
        numberInput.send_keys(number)
    except:
        browser.quit()
        return {"error": "Invalid class number query"}
    #session select
    try:
        sessionSelect = Select(browser.find_element_by_name('SSR_CLSRCH_WRK_SESSION_CODE$6'))
        sessionSelect.select_by_value(session)
    except:
        browser.quit()
        return {"error": "Invalid session query"}
    #class number input
    try:
        classNumberInput = browser.find_element_by_name('SSR_CLSRCH_WRK_CLASS_NBR$10')
        classNumberInput.send_keys(classNbr)
    except:
        browser.quit()
        return {"error": "Invalid class number query"}
    #course career select
    try:
        courseCareerSelect = Select(browser.find_element_by_name('SSR_CLSRCH_WRK_ACAD_CAREER$2'))
        courseCareerSelect.select_by_value(courseCareer)
    except:
        browser.quit()
        return {"error": "Invalid course career query"}
    #req designation select
    try:
        reqDesignationSelect = Select(browser.find_element_by_name('SSR_CLSRCH_WRK_CU_RQMNT_DESIGNTN$4'))
        reqDesignationSelect.select_by_value(reqdes)
    except:
        browser.quit()
        return {"error": "Invalid requirement designation query"}
    #instructor last name input
    try:
        instructorNameInput = browser.find_element_by_name('SSR_CLSRCH_WRK_LAST_NAME$16')
        instructorNameInput.send_keys(instructorName)
    except:
        browser.quit()
        return {"error": "Invalid instructor last name query"}
    #instructor name selector select
    try:
        instructorNameSelect = Select(browser.find_element_by_name('SSR_CLSRCH_WRK_SSR_EXACT_MATCH2$16'))
        instructorNameSelect.select_by_value(instructorSelector)
    except:
        browser.quit()
        return {"error": "Invalid contains/exact match selector for instructor last name query"}

    #submit the search form (this runs the JS function that runs when the search button is clicked on the form)
    browser.execute_script("return submitAction_win0(document.win0,'CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH');")

    courses = []
    #try to wait for the Search Results title of the page. If it doesn't appear after 10 seconds, return no results found.
    try:
        element = WebDriverWait(browser, 10).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "PAPAGETITLE"), 'Search Results')
        )
    except:
        browser.quit()
        return {"error": "Not found"}

    courseList = browser.find_elements_by_xpath('//*[@id="ACE_$ICField$4$$0"]/tbody/tr')
    courseList.pop(0)  #the first course is empty

    sectionCounter = 0
    for course in courseList:
        courseName = course.find_element_by_id('win0divSSR_CLSRSLT_WRK_GROUPBOX2GP$' + str(courseList.index(course))).text
        sectionList = course.find_elements_by_xpath('//*[@id="ACE_$ICField48$' + str(courseList.index(course)) + '"]/tbody/tr')
        sections = []
        for section in sectionList:
            if sectionList.index(section) % 2 == 1:
                #if the section is 'Open' (shows the green status circle)
                if (section.find_element_by_class_name('SSSIMAGECENTER').get_attribute('alt') == 'Open'):
                    #get all of the section info
                    sectionTimes = section.find_element_by_id('MTG_DAYTIME$' + str(sectionCounter)).text
                    sectionRoom = section.find_element_by_id('MTG_ROOM$' + str(sectionCounter)).text
                    sectionInstructor = section.find_element_by_id('MTG_INSTR$' + str(sectionCounter)).text
                    sectionMeetingDates = section.find_element_by_id('MTG_TOPIC$' + str(sectionCounter)).text

                    searchProfName = sectionInstructor.split(',')[0]  #get only the last name of the professor
                    instructorGrades = {}
                    if (searchProfName != "Staff"):  #do not search RMP if professor "name" is Staff
                        instructorGrades = professorRating(searchProfName, collegeName, deptName.split('-')[1].strip().split(' '))

                    #compile the dict of all of the section info for the course
                    sectionDict = {'times': sectionTimes, 'room': sectionRoom, 'instructor': sectionInstructor, 'instructorGrades': instructorGrades, 'meetingDates': sectionMeetingDates}
                    sections.append(sectionDict)
                sectionCounter += 1

        sortedSections = sorted(sections, key=getGrade , reverse=True)  #sort the sections by professor ratings
        courseDict = {'courseName': courseName, 'sections': sortedSections}  #add the sections to the course info 
        if courseDict['sections']:  #if a course has sections (is not empty)
            courses.append(courseDict)  #add the course to the list of courses

    browser.quit()
    return {"departmentName": deptName, "courses": courses}  #return the list of courses found!


#gets the RateMyProfessors rating for a professor
#name    last name of the professor
#school  school at which the professor teaches
#dept    in the case of multiple professors with the same last name at the same school, the department helps choose the right one
#RETURNS JSON with professor ratings
def professorRating(name, school, dept):
    query = {'query': name}
    searchResult = requests.get('http://www.ratemyprofessors.com/search.jsp', params=query)
    soup = BeautifulSoup(searchResult.text, 'html.parser')
    listings = soup.find_all('li', class_="listing PROFESSOR")
    #if the search result isn't empty
    if listings:
        #find the right professor
        for listing in listings:
            span = listing.find('span', class_="sub")
            searchList = span.string.split(',')
            searchSchool = searchList[0]
            searchDept = searchList[1].strip()
            if (searchSchool == school and any(depWord in searchDept for depWord in dept)):
                #if everything matches, try to get the professor's info using another request to the details
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

#Gets the professor's rating in a section dict
#item  the dict, in which to find the rating
#RETURNS the grade of the professor
def getGrade(item):
    key = '0'
    try:
        key = itemgetter('overall')(item['instructorGrades'])  #this goes through the section dict to find the rating
    except:
        key = '0'
    return key

#Gets a student's required classes from DegreeWorks
#userName  the student's CUNYPortal username
#passWord  the student't CUNYPortal password
#RETURNS JSON of the classes the student still needs to take
def degreeClasses(userName, passWord):
    browser = webdriver.PhantomJS()
    browser.maximize_window()

    browser.get('https://cunyportal.cuny.edu/cpr/authenticate/portal_login.jsp')  #go to CUNYPortal

    #enter student login info into the login form
    userid = browser.find_element_by_id("userid")
    password = browser.find_element_by_id("password")
    userid.send_keys(userName)
    password.send_keys(passWord)
    browser.find_element_by_name("image").click()  #submit the login form

    #try to go to DegreeWorks (the name/pass combo is wrong or sometimes Degreeworks is down)
    try:
        browser.get("https://degreeworks.cuny.edu/cuny_redirector.cgi")
    except Exception as e:
        browser.quit()
        return {'error': 'Username or password is incorrect, or DegreeWorks is down'}
    #this rarely happens, but is a precaution
    try:
        browser.switch_to_frame('frBody')
    except:
        browser.quit()
        return {'error': 'Could not get course info'}
    startTime = time()  #either wait 30 seconds for the Degree content to load or return that it couldn't load
    waiting = 0
    frameContent = ""
    while (waiting < 30 or frameContent[1] != '?'):  #if successfully loaded, the content will be xml, so the second character will be '?' because of the opening '<?'
        timeNow = time()
        waiting = timeNow - startTime
        frameContent = browser.page_source
    if (frameContent[1] != '?'):
        browser.quit()
        return {'error': 'School info empty'}

    #Degree content loads as XML and is not converted to HTML, so convert it
    xml = ET.parse(StringIO(frameContent))
    xslt = ET.parse("/home/mikmaks/dev/CUNYsecond/cume/api/DGW_Report.xsl")  #these is a stylesheet that transform the xml to html. I downloaded it from CUNY
    transform = ET.XSLT(xslt)
    html = transform(xml)
    soup = BeautifulSoup(ET.tostring(html), 'html.parser')

    schoolName = soup.find('span', class_="SchoolName").text  #get the school name of the student to do class searches later
    needed = soup.find_all('tr', class_="bgLight0")  #get all the unfulfilled reqs (red background)
    allReqs = []
    previousReq = None
    for req in needed:
        dataBlocks = req.find_all('td', class_="RuleAdviceData")  #this is where the requirements contain the actual data (like what classes to take to fulfill it)
        for dataBlock in dataBlocks:
            #if it's a real requirement with the word 'Credits' or 'Class' in it, parse it
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
                        try:
                            name = previousReq.find('td', class_="RuleLabelTitleNeeded").text
                        except:
                            name = ""
                data = dataBlock.text
                data = " ".join(data.split())
                numOfCredits = int(re.search(r'\d+', data).group())
                classesThatFulfillReq = []
                allMatches = re.findall(r'([A-Z]{3,5}((?![A-Z]).)*)', data)  #use a regex search to get the courses that fulfill the req
                #the regex search actually splits the requirement by the courses, so if it's a list like GTECH 201, 301, 361 or CSCI 360, 340
                #the matches will be GTECH 201, 301, 361 and CSCI 360 340. Two matches separated.
                allMatchesList = []
                for match in allMatches:
                    allMatchesList.append(match[0])
                for match in allMatchesList:
                    classCode = match.split()[0]  #class code is GEOG or CSCI
                    numberList = [int(s) for s in match.split() if s.isdigit()]  #find all full 5 digit course codes
                    notFullNumberList = re.findall(r'\d{1,3}@', match)  #some courses aren't complete, like CSCI499@. Find these separately
                    #add all courses that fulfill the req
                    for number in numberList:
                        newClass = {'code': classCode, 'number': number}
                        classesThatFulfillReq.append(newClass)
                    for number in notFullNumberList:
                        newClass = {'code': classCode, 'number': number}
                        classesThatFulfillReq.append(newClass)

                #add the courses to a requirement dict
                newReq = {'name': name, 'credits': numOfCredits, 'classes': classesThatFulfillReq, 'reqWord': reqWord}
                allReqs.append(newReq)  #add the new dict to a list of requirements
        previousReq = req
    reqsResponse = {'schoolName': schoolName, 'allRequirements': allReqs}
    browser.quit()
    return reqsResponse

#pauses script execution for seconds time. I need this to prevent PhantomJS from racing before it refreshes.
#seconds  the number of seconds to pause for
def wait(seconds):
    startTime = time()
    currentTime = time()
    while (currentTime - startTime < seconds):
        currentTime = time()
        continue
    return
