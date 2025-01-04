from pymongo import MongoClient


def get_db_client():
    uri = "mongodb+srv://ModularBackend:Modular22Back22end@cluster0.qvfca76.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    conn = MongoClient(uri);
    return conn;


conn = get_db_client();
db = conn.get_database("modular_db");

