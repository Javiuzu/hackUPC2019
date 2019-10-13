from PIL import Image
import pytesseract

image_file = "./tmp/ads/ad5.png"

text = str(((pytesseract.image_to_string(Image.open(image_file)))))
text = text.replace('-\n', '')

if "Why this ad" in text:
	text = ""
print(text)