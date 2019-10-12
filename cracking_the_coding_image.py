from PIL import Image
import pytesseract

image_file = "ad.jpeg"

text = str(((pytesseract.image_to_string(Image.open(image_file)))))
text = text.replace('-\n', '')

print(text)