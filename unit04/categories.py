from woocommerce import API

# 設置 WooCommerce API 的連接
wcapi = API(
    url="http://localhost:8081",  # WooCommerce 網站的 URL
    consumer_key="ck_b30416d781c7cb878e9c432d8e78c86a95a14e8f",  # 從 WooCommerce 獲取的 Consumer Key
    consumer_secret="cs_3bf8a4b269c915a0288de0ce18b7f312eab4df6c",  # 從 WooCommerce 獲取的 Consumer Secret
    version="wc/v3",  # WooCommerce API 版本
    timeout=120
)

# 發送請求以獲取所有商品類別
response = wcapi.get("products/categories")

# 檢查請求是否成功
if response.status_code == 200:
    categories = response.json()  # 解析 JSON 數據
    for category in categories:
        print(f"ID: {category['id']}, Name: {category['name']}, Slug: {category['slug']}")
else:
    print(f"無法獲取商品類別，狀態碼: {response.status_code}")
