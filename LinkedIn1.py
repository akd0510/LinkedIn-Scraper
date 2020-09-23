from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import csv
import time
import re
import sys

full_name = []
first_name = []
last_name = []
profile_page = []
working = []
position= []
years_of_experience = []
years_of_experience_at_that_pos = []
institute = []
qualification = []
time_of_qualification = []
list_ = []

def linkedin():
    counter = 0
    driver = webdriver.Chrome("https://drive.google.com/file/d/1HMK0csW_fbmyYrr3JQsSkTe9YiwLrO4O/view?usp=sharing")
    login = driver.get("https://www.linkedin.com/uas/login?fromSignIn=true&trk=cold_join_sign_in")
    time.sleep(1)
    user_id = driver.find_element_by_id("username").send_keys("akshayd.wematter@gmail.com")
    time.sleep(1)
    password = driver.find_element_by_id("password").send_keys("Akshay@1234")
    time.sleep(3)
    driver.find_element_by_class_name('btn__primary--large').click()   
    if driver.title == "Security Verification | LinkedIn":
        otp = int(input("Enter OTP: "))
        driver.find_element_by_name("pin").send_keys(otp)
        time.sleep(3)
        driver.find_element_by_id("email-pin-submit-button").click()
    time.sleep(3)
    google = driver.get("https://www.google.com/")
    filters = 'site:Linkedin.com "AZB & Partners" AND "India" AND "People"'
    driver.find_element_by_name('q').send_keys(filters)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[3]/center/input[1]').click()
    time.sleep(4)
    page_no = int(input("Enter page_number: "))
    for page in range(page_no):
        if counter == 1:
            break
        url = driver.current_url
        search_mail = driver.find_elements_by_class_name('st')
        google_page = driver.page_source
        source_page = BeautifulSoup(google_page,'lxml')
        google_links = source_page.find_all('div',{'class':'r'})
        for links_to_iterate in google_links:
            p_l = links_to_iterate.find('a', href=True)
            p_l = str(p_l)
            p_l = p_l.split()
            list_.append(p_l[1].strip('href=').strip('""'))
        for i in search_mail:
            mail = emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", i.text)
            print(mail)
        for x_path in list_:
            try:
                driver.get(x_path)
                time.sleep(2)
                driver.execute_script("window.scrollTo(0,800)","")
                time.sleep(7)
            except:
                    try:
                        sheet = pd.DataFrame([full_name,first_name,last_name,working,profile_page,position,years_of_experience,years_of_experience_at_that_pos,institute,qualification,time_of_qualification])
                        sheet.to_csv('FINAL Sheet.csv')
                        quit()
                    except:
                        print("File is open please close the file")
                        input("Done? ")
                        sheet = pd.DataFrame([full_name,first_name,last_name,working,profile_page,position,years_of_experience,years_of_experience_at_that_pos,institute,qualification,time_of_qualification])
                        sheet.to_csv('FINAL Sheet.csv')
                        quit()
            try:
                src = driver.page_source
                html_page = BeautifulSoup(src, "lxml")
                profile_link = driver.current_url
                profile_link = str(profile_link)
                profile_page.append(profile_link)
            except:
                profile_page.append("No link provided")
            try:
                name_div = html_page.find('div', {'class':'flex-1 mr5'})
                name_loc = name_div.find_all('ul')
                name = name_loc[0].find('li').get_text().strip()
                full_name.append(name)
                name = name.split()
                first = name[0]
                last = name[-1]

                first_name.append(first)
                last_name.append(last)
            except:
                full_name.append("No name found")
                first_name.append("No name found")
                last_name.append("No name found")
            try:    
                profile_title = name_div.find('h2', {'class':'mt1 t-18 t-black t-normal break-words'}).get_text().strip()
                position.append(profile_title)
            except:
                position.append('No profile title found')
            try:    
                experience = html_page.find('h4',{'class':'t-14 t-black t-normal'})
                years_of_experience.append(experience.get_text().strip('Total Duration\n'))
            except:
                years_of_experience.append("No experience provided")
            try:
                time_dur = driver.find_element_by_class_name('pv-entity__bullet-item-v2').text
                years_of_experience_at_that_pos.append(time_dur)
            except:
                years_of_experience_at_that_pos.append("Not provded")
            try:
                edu = driver.find_element_by_class_name('pv-entity__school-name').text
                institute.append(edu)
            except:
                institute.append("Not provided")
            try:
                spec = driver.find_elements_by_class_name('pv-entity__comma-item')
                qualification.append(spec[0].text + " " + spec[1].text)
            except:
                qualification.append("Not provided")
            try:
                time_of_edu = driver.find_elements_by_tag_name('time')
                time_of_qualification.append(time_of_edu[0].text + "-" + time_of_edu[1].text)
            except:
                time_of_qualification.append("Not provided")
            try:
                work = driver.find_element_by_class_name('pv-top-card--experience-list-item').text
                working.append(work)
            except:
                working.append("Not provided")
            if x_path == list_[len(list_) -1]:
                try:
                    driver.get(url)
                    time.sleep(5)
                    driver.find_element_by_link_text('Next').click()
                    list_.clear()
                except:
                    try:
                        counter = counter + 1
                        sheet = pd.DataFrame([full_name,first_name,last_name,working,profile_page,position,years_of_experience,years_of_experience_at_that_pos,institute,qualification,time_of_qualification])
                        sheet.to_csv('FINAL Sheet1.csv')
                        print("Excel sheet is ready... 1")
                    except:
                        counter = counter + 1
                        print("File is open please close the file 2")
                        input("Done? ")
                        sheet = pd.DataFrame([full_name,first_name,last_name,working,profile_page,position,years_of_experience,years_of_experience_at_that_pos,institute,qualification,time_of_qualification])
                        sheet.to_csv('FINAL Sheet1.csv')
                        print("Excel sheet is ready... 2")
    try:
        if counter == 0:
            sheet = pd.DataFrame([full_name,first_name,last_name,working,profile_page,position,years_of_experience,years_of_experience_at_that_pos,institute,qualification,time_of_qualification])
            sheet.to_csv('FINAL Sheet1.csv')
            print("Excel sheet is ready...")
    except:
        if counter == 0:
            print("File is open please close the file")
            input("Done? ")
            sheet = pd.DataFrame([full_name,first_name,last_name,working,profile_page,position,years_of_experience,years_of_experience_at_that_pos,institute,qualification,time_of_qualification])
            sheet.to_csv('FINAL Sheet1.csv')
            print("Excel sheet is ready...")
linkedin()