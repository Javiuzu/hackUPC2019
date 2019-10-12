from selenium import webdriver

driver = webdriver.Firefox()
driver.get("https://www.youtube.com/watch?v=PgvEe6UhahA")
body = driver.page_source
body_file = open("body_selenium.txt", "w+")
body_file.write(body)
body_file.close()
driver.close()

