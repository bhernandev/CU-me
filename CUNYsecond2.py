import argparse
import mechanicalsoup
import credentials

#parser = argparse.ArgumentParser(description='Login to CUNYfirst.')
#parser.add_argument('username')
#parser.add_argument('password')
#arg = parser.parse_args()

browser = mechanicalsoup.Browser()

login_page = browser.get("https://home.cunyfirst.cuny.edu/access/dummy.cgi")

login_form = login_page.soup.select("#login-form")[0].select("form")[0]

login_form.select("#cf-login")[0]['value'] = credentials.cunyfirst_username
login_form.select("#password")[0]['value'] = credentials.cunyfirst_password

page2 = browser.submit(login_form, login_page.url)

messages = page2.soup.find('div', class_='ptnnw')
if messages:
    print(messages.text)
assert page2.soup.select(".ptnnw")

print(page2.soup.title.text)

page3 = browser.get("https://home.cunyfirst.cuny.edu/psp/cnyepprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?FolderPath=PORTAL_ROOT_OBJECT.HC_SSS_STUDENT_CENTER&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder")
assert page3.soup.select(".ptnnw")

print(page3.soup.title.text)

page4 = browser.get("https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL?Page=SSR_CLSRCH_ENTRY&Action=U&ExactKeys=Y&TargetFrameName=None")

print(page4.soup.title.text)

search_login_form = login_page.soup.select("form")[0]

search_login_form.select("#CLASS_SRCH_WRK2_INSTITUTION$31$")[0]['value'] = "HTR01"
search_login_form.select("#CLASS_SRCH_WRK2_STRM$35$")[0]['value'] = "1169"
search_login_form.select("#SSR_CLSRCH_WRK_SUBJECT_SRCH$0")[0]['value'] = "CSCI"

page5 = browser.submit(search_login_form, page4.url)

print(page5.soup.title.text)
