# 建立一個新的Scrapy專案
import os
import subprocess

# 設定專案名稱
project_name = 'udnnews'

# 使用Scrapy命令行工具創建新專案
subprocess.run(['scrapy', 'startproject', project_name])

# 切換到專案目錄
os.chdir(project_name)

# 創建一個新的Spider
spider_name = 'udn_spider'
target_url = 'https://udn.com/news/breaknews/1'

subprocess.run(['scrapy', 'genspider', spider_name, target_url])

print(f'已成功創建Scrapy專案 "{project_name}" 並生成Spider "{spider_name}"')
print(f'目標網址: {target_url}')
print('請檢查並編輯生成的檔案以完成爬蟲邏輯')
