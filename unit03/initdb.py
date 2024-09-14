from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# 連線字串
conn = "mongodb://admin:mymdb$1234@localhost:27017"

try:
    # 建立連線
    client = MongoClient(conn)
    
    # 檢查連線
    client.admin.command('ismaster')
    
    # 選擇或建立資料庫
    db = client['unit03db']
    
    # 建立集合
    user_collection = db['user']
    transaction_collection = db['transaction']
    
    # 新增使用者
    new_user = {"username": "minhuang", "password": "1234"}
    user_collection.insert_one(new_user)
    
    print("成功連接到資料庫並完成操作")

except ConnectionFailure:
    print("無法連接到MongoDB伺服器")
except OperationFailure:
    print("資料庫操作失敗")
finally:
    client.close()
