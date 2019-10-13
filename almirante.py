from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import multiprocessing
from random import seed
from random import randint

def html_worker(x, options, webList):
  seed()
  print(x)
  driver = webdriver.Firefox(options = options)
  driver.get(webList[x])
  html = driver.page_source
  driver.close()


def camera_worker(x, options, webList):
  driver = webdriver.Firefox(options = options)
  driver.get(webList[x])
  driver.save_screenshot("ad"+str(randint(0,10000))+".png")
  driver.close()
    
def loadPages(webList, options):
    #open tabs

    i = len(webList)
    print(i)
    jobs = []
    worked = 0
    for x in range (0,i,4):
      print(x)
      p = multiprocessing.Process(target=html_worker, args=(x, options, webList[x:x+4]))
      jobs.append(p)
      p.start()
      worked = worked + 4
    if worked < i:
      p = multiprocessing.Process(target=html_worker, args=(x, options, webList[worked:i]))
      jobs.append(p)
      p.start()


def loadScreenshots(webList, options):
    #open tabs

    i = len(webList)
    jobs = []
    worked = 0
    for x in range (0,i,4):
      p = multiprocessing.Process(target=camera_worker, args=(x, options, webList[x:x+4]))
      jobs.append(p)
      p.start()
    if worked < i:
      p = multiprocessing.Process(target=camera_worker, args=(x, options, webList[x:x+4]))
      jobs.append(p)
      p.start()

#def main():
#    print("Fuck off")
#    options = Options()
#    options.headless = True
#    adMines=["https://collider.com", "https://clickondetroit.com", "https://nationalinterest.org"]
#    loadPages(adMines, options)
    

#main()
