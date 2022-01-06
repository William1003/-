from selenium import webdriver
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains


options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
browser = webdriver.Chrome(options=options)
button = browser.find_element_by_id('downloader-trigger')
print(button.get_attribute('outerHTML'))
button.click()

