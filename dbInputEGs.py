import pymongo
from dateutil.parser import parse
import locale
from datetime import datetime
import pymysql


def convert_date_string_to_datetime(date_string):
    # Set the Portuguese locale to parse month names correctly
    locale.setlocale(locale.LC_TIME, 'pt_PT.UTF-8')
    
    # Specify the input format of the date string
    date_format = "%d de %B de %Y"
    
    # Parse the date string using the specified format
    parsed_date = parse(date_string, fuzzy_with_tokens=True)
    
    # Extract the parsed date
    parsed_date = parsed_date[0]
    
    return parsed_date

def insert_to_mongodb(collection_name, dbClient,data_to_insert, mongodb_uri="mongodb://localhost:27017/"):
    # Connect to MongoDB
    client = pymongo.MongoClient(mongodb_uri)
    db = client[dbClient]  # Replace with your database name
    collection = db[collection_name]

    # Insert the data into the collection
    result = collection.insert_one(data_to_insert)
    return result


def insert_to_mysql(mySQLhost, mySQLuser, mySQLpassword, mySQLdatabase, custom_schema):
    db_connection = pymysql.connect(
    host=mySQLhost,
    user=mySQLuser,
    password=mySQLpassword,
    database=mySQLdatabase
    )
    
    try:
        cursor = db_connection.cursor()

        # Extract data from the custom_schema dictionary
        item = custom_schema["item"]
        name = item["name"]
        price = item["price"]
        location = item["location"]
        updated_at = convert_date_string_to_datetime(custom_schema["updated_at"])
        timestamp = custom_schema["timestamp"]

        # Insert data into the price_data table
        insert_price_query = "INSERT INTO price_data (name, price, timestamp) VALUES (%s, %s, %s)"
        price_data = (name, price, timestamp)
        cursor.execute(insert_price_query, price_data)

        # Insert data into the item_data table
        insert_item_query = "INSERT INTO item_data (location, updated_at) VALUES (%s, %s)"
        item_data = (location, updated_at)
        cursor.execute(insert_item_query, item_data)

        db_connection.commit()

    except Exception as e:
        print("Error: ", e)
