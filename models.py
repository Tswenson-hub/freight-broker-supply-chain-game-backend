from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = MongoClient(os.getenv('MONGODB_URI'))
db = client.get_database()

class User:
    collection = db.Users

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save(self):
        return self.collection.insert_one(self.__dict__)

    @classmethod
    def find_one(cls, query):
        return cls.collection.find_one(query)