from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import multiprocessing
import os

def worker(x, options, webList, html_dir):
  driver = webdriver.Firefox(options = options)
  driver.get(webList[x-1])
  html = driver.page_source
  html_file = html_dir+"/"+driver.title+".html"
  driver.close()

    
def loadPages(webList, options, html_dir):
    #open tabs

    i = len(webList)
    jobs = []
    for x in range (i):
      p = multiprocessing.Process(target=worker, args=(x, options, webList, html_dir))
      jobs.append(p)
      p.start()