import ad_scraper
import process_module
import os
import shutil
import json
import subprocess
import interface

ads_dir = str(os.getcwd())+"/tmp/ads/"
word_dir = str(os.getcwd())+"/tmp/words/"

if __name__ == "__main__":
	 os.makedirs(ads_dir, exist_ok=True)
	 os.makedirs(word_dir, exist_ok=True)
	 #urls = ['https://www.wikihow.com/Be-a-Communist']
	 #for url in urls:
	 #	ad_scraper.getAds(url, ads_dir)
	 ads = {}
	 process_module.getAdText(ads_dir, ads)
	 word_cloud = []
	 ad_text = ads.items()
	 for key, ad in ad_text:
	 	print(ad)
	 	ad_file = open(word_dir+"ad.txt", 'w+')
	 	ad_file.write(ad)
	 	script = ["python2.7", "webClassifier.py"]
	 	process = subprocess.Popen(" ".join(script),
	 										shell=True,
	 										env={"PYTHONPATH": "."})    
	 	class_file = open(word_dir+"/class_words.txt", 'r')
	 	print(class_file.read())
	 	#word_cloud.append(class_file.read())
	 	#print(word_cloud)
	 
	 """with open(word_dir+"/cloud.txt", 'w+') as cloud_file:
	 	for word in word_cloud:
	 		cloud_file.write(str(word))	
	 interface.generateWordCloud(word_dir)"""


	 #shutil.rmtree("./tmp/", ignore_errors=False, onerror=None)
