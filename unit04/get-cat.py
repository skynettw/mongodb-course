from woocommerce import API

# 設定 WooCommerce API 連接
wcapi = API(
    url="http://localhost:8081",  # 本地 WooCommerce 網站 URL
    consumer_key="ck_53c93a2b250a345d0d56ef348c0c16d811546096",  
    consumer_secret="cs_41803c47be4fae4e8735d89dc5adbad3560d86eb",  
    version="wc/v3", 
    timeout=20
)

# 取得所有商品分類
categories = wcapi.get("products/categories").json()

# 列出所有分類名稱
for category in categories:
    print(f"ID: {category['id']}, Name: {category['name']}")
