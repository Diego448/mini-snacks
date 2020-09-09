from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)
db = client['mini-snacks']
collection = db.snacks

def get_all_snacks():
    cursor = collection.find()
    return list(cursor)

def get_snack(id):
    result = collection.find_one({'_id': ObjectId(id)})
    return result

def add_snack(data):
    id = collection.insert_one(data)
    return id

def edit_snack(id, data):
    result = collection.update_one({'_id': ObjectId(id)}, 
        {'$set': data})
    return str(result.modified_count)