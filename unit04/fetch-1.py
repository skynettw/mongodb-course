from woocommerce import API
import json

# 初始化 WooCommerce API
wcapi = API(
    url="http://localhost:8081",  # 替換成你的 WooCommerce 網址
    consumer_key="ck_53c93a2b250a345d0d56ef348c0c16d811546096",  # 替換成你的 Consumer Key
    consumer_secret="cs_41803c47be4fae4e8735d89dc5adbad3560d86eb",  # 替換成你的 Consumer Secret
    version="wc/v3",  # 使用 WooCommerce API 的 v3 版本
    timeout=30
)

# 取得商品資訊
response = wcapi.get("products")

# 檢查回應狀態並處理回傳結果
if response.status_code == 200:
    products = response.json()
else:
    print(f"無法取得商品資訊，狀態碼: {response.status_code}")
for item in products:
    print(item['name'], item['price'], item['categories'][0]['name'])
