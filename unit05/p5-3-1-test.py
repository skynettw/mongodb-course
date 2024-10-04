from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 開啟指定的網頁
url = "https://www.lexuscpo.com.tw/Home/Search"
driver.get(url)

# 等待網頁完全加載
time.sleep(5)

all_cars = []

while True:
    # 提取車款、公里數、出廠年、價格等資料
    cars = driver.find_elements(By.CLASS_NAME, 'cars-item')

    for car in cars:
        # 車款名稱
        model = car.find_element(By.CLASS_NAME, 'info-name').text
        
        # 公里數
        km = car.find_element(By.CLASS_NAME, 'info-mileage').text
        
        # 出廠年
        year = car.find_element(By.CLASS_NAME, 'info-y').text
        
        # 價格
        price = car.find_element(By.CLASS_NAME, 'info-price').text
        
        car_info = {
            "車款": model,
            "公里數": km,
            "出廠年": year,
            "價格": price
        }
        all_cars.append(car_info)
        print(f"車款: {model}, 公里數: {km}, 出廠年: {year}, 價格: {price}")

    # 檢查是否有下一頁
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.next'))
        )
        next_button.click()
        time.sleep(5)  # 等待新頁面加載
    except:
        print("已經是最後一頁")
        break

# 將結果儲存為 JSON 檔案
with open('cpocars.json', 'w', encoding='utf-8') as f:
    json.dump(all_cars, f, ensure_ascii=False, indent=4)

print("資料已儲存至 cpocars.json")

# 關閉瀏覽器
driver.quit()