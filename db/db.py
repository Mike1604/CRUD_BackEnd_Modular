from pymongo import MongoClient


def get_db_client():
    #Uncomment the db you want to use 
    uri = "mongodb://localhost:27017/"
    #uri = "mongodb+srv://Modular:FlashCardsModular@cluster0.mresw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    conn = MongoClient(uri);
    return conn;


conn = get_db_client();
db = conn.get_database("modular_db");

