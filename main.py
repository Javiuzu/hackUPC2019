import ad_scraper
import process_module
import os


ads_dir = str(os.getcwd())+"/tmp/ads"

if __name__ == "__main__":
	 #os.makedirs(ads_dir, exist_ok=True)
	 #urls = ['https://www.wikihow.com/Be-a-Communist']
	 #for url in urls:
	# 	ad_scraper.getAds(url, ads_dir)
	 ad_text = {}
	 process_module.getAdText(ads_dir, ad_text)
	 print(ad_text)
