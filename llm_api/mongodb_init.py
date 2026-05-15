import os
from config import ENABLE_MONOGODB

# 从环境变量获取 MongoDB URI，如果没有则使用默认值
mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')

if ENABLE_MONOGODB:
    try:
        from pymongo import MongoClient
    except ImportError as exc:
        raise RuntimeError("已启用 MongoDB，但未安装 pymongo。请安装 backend/requirements.txt。") from exc

    mongo_client = MongoClient(mongo_uri)
else:
    mongo_client = None
