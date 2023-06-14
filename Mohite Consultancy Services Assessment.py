from pymongo import MongoClient
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def fetchData():
    url = "https://www.insiderbiz.in/company-list/?page=1"
    path = "E:\Codes\Python\selenium\msedgedriver.exe"
    service = Service(executable_path=path)
    driver = webdriver.Edge(service=service)
    driver.get(url)
    driver.maximize_window()

    tbody = driver.find_element(By.XPATH, '//*[@id="WebGrid"]/tbody')

    data = []
    for _ in range(0, 10):

        for tr in tbody.find_elements(By.XPATH, '//tr'):
            data.append([item.text for item in tr.find_elements(By.XPATH, './/td')])
        data.remove([])
        data.remove(['1 2 3 4 5 >'])

        try:
            run_test = WebDriverWait(driver, 120).until( \
                EC.presence_of_element_located((By.XPATH, '//*[@id="description"]/div/div/div/div/ul/li[8]/a')))
            run_test.click()
            break
        except StaleElementReferenceException as e:
            raise e

    print(data)
    driver.quit()
    return data


def saveData(data):
    try:
        conn = MongoClient('localhost', 27017)
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    db = conn.MohiteConsultancyServiceAssessment
    collection = db.companies

    for d in data:

        mydict = {
            "CIN(Company Identification Number)": d[0],
            "COMPANY NAME": d[1],
            "ROC (Registrar of Companies)": d[2],
            "ADDRESS": d[3],
                  }

        collection.insert_one(mydict)

    print("Data inserted")


if __name__ == "__main__":
    data = fetchData()
    saveData(data)
