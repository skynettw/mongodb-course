from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, CollectionInvalid

# 連線到MongoDB
conn = "mongodb://admin:mymdb$1234@localhost:27017"
client = MongoClient(conn)

try:
    # 檢查連線
    client.admin.command('ismaster')
    
    # 建立或獲取資料庫
    db = client['unit03db']
    
    # 建立collections
    try:
        db.create_collection('user')
    except CollectionInvalid:
        print("user collection 已存在")
    
    try:
        db.create_collection('transaction')
    except CollectionInvalid:
        print("transaction collection 已存在")
    
    # 新增使用者
    user_collection = db['user']
    new_user = {"username": "minhuang", "password": "1234"}
    user_collection.insert_one(new_user)
    
    print("資料庫和collections已成功建立，並新增了使用者")

except ConnectionFailure:
    print("無法連接到MongoDB")

finally:
    client.close()
