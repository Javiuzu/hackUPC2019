from selenium import webdriver
import requests
import adblockparser
from adblockparser import AdblockRules


url = 'https://www.youtube.com/watch?v=6ftCIfHwqtg'
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
num_adds_selenium = 0

elems = driver.find_elements_by_xpath("//a[href]")
for link in elems:
	print(link.get_attribute("href"))
print(elems.len())

driver.close()