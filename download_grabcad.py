import time

import requests
from selenium import webdriver
from selenium.webdriver.edge.options import Options


url = 'https://grabcad.com/library?page=1&per_page=100&time=all_time&sort=popular'

browser = webdriver.Chrome()

browser.get(url)
ls = browser.find_elements_by_class_name('login')

for tag in ls:
    if tag.text == 'Log in':
        tag.click()
        break
browser.find_element_by_name('member[email]').send_keys('18231169@buaa.edu.cn')
browser.find_element_by_name('member[password]').send_keys('20001003')
browser.find_element_by_id('signInButton').click()
time.sleep(3)

for page in range(2, 11):
    url = 'https://grabcad.com/library?page=1&per_page={}&time=all_time&sort=popular'.format(page)
    browser.get(url)
    counts_list = browser.find_elements_by_class_name('counts')

    for counts in counts_list:
        count = counts.find_elements_by_class_name('count')[1]
        try:
            count.click()
        except Exception:
            continue
        time.sleep(1)
