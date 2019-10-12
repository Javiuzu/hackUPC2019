from selenium import webdriver
import requests
import adblockparser
import time
from adblockparser import AdblockRules


url = 'https://stackoverflow.com/questions/51284071/how-to-get-all-the-link-in-page-using-selenium-python	'
rules_file = open("adblock_rules.txt", "r")


raw_rule = rules_file.readline()
raw_rules = []
while raw_rule:
	raw_rules.append(raw_rule)
	raw_rule = rules_file.readline()


rules = AdblockRules(raw_rules)


driver = webdriver.Firefox()
driver.get(url)
body = driver.page_source
adds = []
time.sleep(5)
elems = driver.find_elements_by_xpath("//*[@href]")
for link in elems:
	if rules.should_block(link.get_attribute("href")): 
		adds.append(link.get_attribute("href"))

elems = driver.find_elements_by_xpath("//*[@src]")
for link in elems:
	if rules.should_block(link.get_attribute("src")): 
		adds.append(link.get_attribute("src"))


print(adds)

driver.close()