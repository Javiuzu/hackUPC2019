

from selenium import webdriver

from selenium.webdriver.firefox.options import Options

import multiprocessing

​

def worker(x, options, webList):

  print(x)

  driver = webdriver.Firefox(options = options, executable_path="/sbin/geckodriver")

  driver.get(webList[x-1])

  html = driver.page_source

  driver.close()

​

    

def loadPages(webList, options):

    #open tabs

​

    i = len(webList)

    jobs = []

    for x in range (i):

      p = multiprocessing.Process(target=worker, args=(x, options, webList))

      jobs.append(p)

      p.start()

      

      

def main():

    print("Fuck off")

    options = Options()

    options.headless = True

    adMines=["https://www.digitaltrends.com/cool-tech/nasa-esa-images-water-mars/"]

    loadPages(adMines, options)

    

​

main()

