from pymongo import MongoClient


def get_db_client():
    uri = "mongodb://localhost:27017/"
    conn = MongoClient(uri);
    return conn;


conn = get_db_client();
db = conn.get_database("modular_db");

