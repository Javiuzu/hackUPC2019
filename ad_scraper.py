from selenium import webdriver
import requests
import adblockparser
import time
from adblockparser import AdblockRules

url = 'https://www.wikihow.com/Be-a-Communist'
rules_file = open("adblock_rules.txt", "r")
ads = []

def search_href(driver):
	elems = driver.find_elements_by_xpath("//*[@href]")
	for link in elems:
		if rules.should_block(link.get_attribute("href")) or 'img_ad' in link.get_attribute("class"):
			ads.append(link.get_attribute("href"))

def search_src(driver):
	elems = driver.find_elements_by_xpath("//*[@src]")
	for link in elems:
		if rules.should_block(link.get_attribute("src")) or'image' in link.get_attribute("class") or 'img_ad' in link.get_attribute("class"):
			ads.append(link.get_attribute("src"))



def find_all_iframes(driver):
    iframes = driver.find_elements_by_xpath("//iframe")
    for index, iframe in enumerate(iframes):
        # Your sweet business logic applied to iframe goes here.
        driver.switch_to.frame(index)
        find_all_iframes(driver)
        search_href(driver)	
        search_src(driver)

        driver.switch_to.parent_frame()



raw_rule = rules_file.readline()
raw_rules = []
while raw_rule:
	raw_rules.append(raw_rule)
	raw_rule = rules_file.readline()


rules = AdblockRules(raw_rules)


driver = webdriver.Firefox()
driver.get(url)
body = driver.page_source
time.sleep(5)

search_href(driver)
search_src(driver)


find_all_iframes(driver)

driver.close()

valid_ads = [elem for elem in ads if not elem.endswith(".js") and rules.should_block(elem)] 

i = 0
for ad in valid_ads:
	ad_driver = webdriver.Firefox()
	ad_driver.get(ad)
	ad_driver.save_screenshot("ad"+str(i)+".png")
	i = i + 1
	print(i)



