from selenium import webdriver

driver = webdriver.Firefox()
driver.get("https://www.youtube.com/watch?v=PgvEe6UhahA")
body = driver.page_source


body_file = open("body_selenium.txt", "w+")
body_file.write(body)
body_file.close()



import requests

url = 'https://www.youtube.com/watch?v=PgvEe6UhahA'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'}

response = requests.get(url, headers)

body_file = open("body_request.txt", "w+")
body_file.write(response.text)
body_file.close()




driver.close()

