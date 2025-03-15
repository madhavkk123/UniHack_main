import json
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

def insert_json_to_mongodb(json_file_path, db_name, collection_name, mongo_uri='mongodb://localhost:27017/'):
    """
    Inserts data from a JSON file into a specified MongoDB collection.

    Parameters:
    - json_file_path: Path to the JSON file containing the data.
    - db_name: Name of the MongoDB database.
    - collection_name: Name of the collection within the database.
    - mongo_uri: URI for connecting to MongoDB (default is 'mongodb://localhost:27017/').

    Returns:
    - A message indicating the number of documents inserted or an error encountered.
    """
    try:
        # Establish a connection to MongoDB
        client = MongoClient(mongo_uri)
        print("Connected to MongoDB successfully.")

        # Access the specified database and collection
        db = client[db_name]
        collection = db[collection_name]

        # Load and parse the JSON file
        with open(json_file_path, 'r') as file:
            file_data = json.load(file)
            print(f"Loaded data from {json_file_path}.")

        # Insert data into MongoDB
        if isinstance(file_data, list):
            result = collection.insert_many(file_data)
            print(f"Inserted {len(result.inserted_ids)} documents into the collection '{collection_name}'.")
        else:
            result = collection.insert_one(file_data)
            print(f"Inserted document with id {result.inserted_id} into the collection '{collection_name}'.")

    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from the file '{json_file_path}'.")
    except ConnectionFailure:
        print("Error: Failed to connect to MongoDB. Please ensure that the MongoDB server is running.")
    except OperationFailure as e:
        print(f"Error: An operation error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Close the MongoDB connection
        client.close()
        print("MongoDB connection closed.")

# Example usage
if __name__ == "__main__":
    json_file_path = 'studocu_data.json'  # Replace with your JSON file path
    db_name = 'Database_unihack'                 # Replace with your database name
    collection_name = 'query_responses'       # Replace with your collection name

    insert_json_to_mongodb(json_file_path, db_name, collection_name)
