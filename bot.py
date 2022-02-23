import wget
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


#url = "https://mobileapps.saude.gov.br/esus-vepi/files/unAFkcaNDeXajurGB7LChj8SgQYS2ptm/eb7d242583455d1def07101098cca54e_HIST_PAINEL_COVIDBR_22fev2022.7z"

#file_name = wget.download(url)
#print(file_name)

xpath = "/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-content/div[1]/div[2]/ion-button"

s=Service("./chromedriver.exe")
driver = webdriver.Chrome(service=s)
driver.maximize_window()

driver.get("https://covid.saude.gov.br")

csv_button = driver.find_element(By.XPATH,xpath)
csv_button.click()

link = driver.execute_script("return requestAnimationFrame.name")
print(link)

time.sleep(5)

driver.close()
