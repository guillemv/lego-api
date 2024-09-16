import pymongo

class Client:
    
    def __init__(self, connection_string, database_name):
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[database_name]

    def insert_one(self, collection_name, document):
        collection = self.db[collection_name]
        return collection.insert_one(document)

    def find_one(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.find_one(query)

    def find_many(self, collection_name, query):
        collection = self.db[collection_name]
        return list(collection.find(query))

    def update_one(self, collection_name, query, update):
        collection = self.db[collection_name]
        return collection.update_one(query, update)

    def delete_one(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.delete_one(query)
