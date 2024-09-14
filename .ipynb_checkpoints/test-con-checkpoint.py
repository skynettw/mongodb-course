from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# MongoDB connection URI
uri = "mongodb://admin:mymdb$1234@localhost:27017/"

try:
    # Create a MongoClient to the running mongod instance
    client = MongoClient(uri)
    
    # Attempt to get server info to check connection
    client.admin.command('ping')
    
    print("連線成功")
except ConnectionFailure as e:
    print(f"連線失敗: {e}")
