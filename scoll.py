from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import time
import json

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
driver = webdriver.Chrome(options=options)

current_height = 0
retry = 0
while True:
    list_item = driver.find_element_by_class_name('project-list')
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    with open('data/temp.html', 'wb') as f:
        source_code = list_item.get_attribute("outerHTML")
        f.write(source_code.encode('utf-8'))
        f.close()
