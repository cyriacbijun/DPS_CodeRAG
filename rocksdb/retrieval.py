from rocksdbpy import rocksdbpy
import json

def retrieve_data(db_path, key_index):
    """Retrieve data from RocksDB given a database path and key index."""
    # Open the RocksDB database at the specified path
    db = rocksdbpy.open_default(db_path)

    # Convert key index to bytes
    key = key_index.to_bytes(2, 'big')
    value = db.get(key)
    if value:
        # Deserialize JSON string back to dictionary
        data_dict = json.loads(value.decode('utf-8'))
        return data_dict
    else:
        print("Key not found")
        return None

# Example usage
db_path = "myrocksdb"
key_to_check = 10
data_dict = retrieve_data(db_path, key_to_check)
if data_dict:
    print("Code Snippet:")
    print(data_dict["code"])
    print("\nDescription:")
    print(data_dict["description"])