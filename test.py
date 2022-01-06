import time

from selenium import webdriver
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import multiprocessing
from threading import Thread
import threadpool

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
browser = webdriver.Chrome(options=options)
urls = ['www.baidu.com', 'www.sougou.com', 'www.bilibili.com', 'www.163.com']


def visit(url):
    print(url)
    js = "window.open('" + url + "');"
    print(js)
    browser.execute_script(js)
    time.sleep(2)
    browser.close()


if __name__ == '__main__':
    pool = threadpool.ThreadPool(4)
    tasks = threadpool.makeRequests(visit, urls)
    [pool.putRequest(task) for task in tasks]
    pool.wait()