from selenium import webdriver
import adblockparser
import time
from adblockparser import AdblockRules
from selenium.webdriver.firefox.options import Options


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
		if rules.should_block(link.get_attribute("src")) or 'img_ad' in link.get_attribute("class"):
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


#driver = webdriver.Firefox()
#driver.get(url)
#body = driver.page_source
#time.sleep(5)
def getAds(url, ads_dir):
	options = Options()
	options.headless = True
	driver = webdriver.Firefox(options=options)
	driver.get(url)
	body = driver.page_source
	search_href(driver)
	search_src(driver)

	find_all_iframes(driver)

	

	valid_ads = [elem for elem in ads if not elem.endswith(".js") and rules.should_block(elem)] 
	valid_ads = list(dict.fromkeys(valid_ads)) #erases duplicate elements in the list
	print(len(valid_ads))	
	options = Options()
	i = 0
	options.headless = True
	for ad in valid_ads:
		adDriver = webdriver.Firefox(options = options)
		adDriver.get(ad)
		adDriver.save_screenshot(ads_dir+"/ad"+str(i)+".png")
		i = i + 1
		adDriver.close()
