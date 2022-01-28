#!/usr/bin/env python
# coding: utf-8

# In[60]:

#install selenium
#install chrome driver for selenium

#change these variables here
driver_path="C:\\Users\\Conor\\Downloads\\chromedriver_win32\\chromedriver.exe"
username="username"
password="passowrd"

#gym time slot in this form
t="14:30"

#order preference for gyms- keep strings exact as below
first,second="Poolside Gym","Performance gym"

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
from datetime import datetime


driver=webdriver.Chrome(executable_path=driver_path)
driver.get("https://hub.ucd.ie/usis/W_WEB_WELCOME_PAGE")
driver.implicitly_wait(2)
acc_cookies_btn=driver.find_element_by_id("onetrust-accept-btn-handler")
acc_cookies_btn.click()
driver.find_element_by_link_text('Log in via SSO').click()
user_input=driver.find_element_by_id("username")
user_input.send_keys(username)
user_pass=driver.find_element_by_id("password")
user_pass.send_keys(password)
driver.find_element_by_link_text("LOGIN").click()
driver.execute_script("window.open('https://hub.ucd.ie/usis/W_HU_MENU.P_PUBLISH?p_tag=GYMBOOK');")
driver.switch_to.window(driver.window_handles[1])

#needed so both pages in sync with login details - 10 refreshes is enough
n_times_refr=10
for _ in range(n_times_refr):
    driver.find_element_by_link_text("Refresh").click()

bookbutton=False
i=-1
preference=first
while not bookbutton:
    i=i+1
    table_id='SW300-1|'+str(i)
    try:
        avail_time=driver.find_element_by_xpath("//tr[@id='"+table_id+"']//td[contains(text(), t)]").text
    except:
        print("Can't find time/gym combination in table")
        sys.exit()
    if avail_time!=t:
        continue
    
    gym_loc=driver.find_element_by_xpath("//tr[@id='"+table_id+"']//td[2]").text
    if gym_loc==preference:
        slot_button=driver.find_element_by_xpath("//tr[@id='"+table_id+"']//td[6]")
    else:
        continue
        
    if  slot_button.text=="Book":
        slot_button.click()
        bookbutton=True
    elif slot_button.text=='Full':
        if preference==first:
            print(first+' is Full at:')
            print(datetime.now())
            preference=second
            i=-1
        else:
            print(second+' is Full at:')
            print(datetime.now())
            sys.exit()
    else:
        driver.find_element_by_link_text("Refresh").click()
        i=-1
        print('Slot not open yet. Currently refreshing to see if slot will become available. Terminate program manually if necessary')

driver.find_element_by_link_text('Confirm Booking').click()
print('Success: Gym booked at:')
print(datetime.now())
sys.exit()


