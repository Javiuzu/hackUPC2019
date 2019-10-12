from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import multiprocessing

def worker(x, options, webList):
  print(x)
  driver = webdriver.Firefox(options = options, executable_path="/sbin/geckodriver")
  driver.get(webList[x-1])
  print(driver.page_source)
  driver.close()
  print("closed")

    
def loadPages(webList, options):
    #open tabs

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
    adMines=["https://collider.com", "https://clickondetroit.com", "https://nationalinterest.org"]
    loadPages(adMines, options)
    

main()
