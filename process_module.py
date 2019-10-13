from PIL import Image
import pytesseract
import os



def getAdText(ads_dir, ad_text):
	for image_file in os.listdir(ads_dir):
		text = str(((pytesseract.image_to_string(Image.open(ads_dir+"/"+image_file)))))
		text = text.replace('\n', ' ')
		#text = text.split('\n')
		if "Why this ad" in text:
			text = ""
		ad_text[image_file] = text
