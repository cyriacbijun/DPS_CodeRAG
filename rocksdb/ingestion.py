import argparse
import csv
import json
from rocksdbpy import rocksdbpy, Option

def preprocess_text(text):
    """Preprocess text by stripping whitespace and normalizing line endings."""
    text = text.strip()
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    return text

def insert_data_from_csv(db_path, csv_file_path):
    opts = Option()
    opts.create_if_missing(True)

    # Open or create a RocksDB database at the specified path
    db = rocksdbpy.open(db_path, opts)

    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        i = 0
        for row in csv_reader:
            if len(row) < 2:
                print(f"Skipping malformed row: {row}")
                continue

            # Preprocess the code snippet and description
            code_snippet = preprocess_text(row[0])
            description = preprocess_text(row[1])

            # Create a dictionary to hold the data
            data_dict = {
                "code": code_snippet,
                "description": description
            }

            # Serialize the dictionary to a JSON string
            value = json.dumps(data_dict).encode('utf-8')

            # Use the index as the key
            key = i.to_bytes(2, 'big')

            # Store in RocksDB
            db.set(key, value)
            i += 1

def main():
    parser = argparse.ArgumentParser(description='Insert data from a CSV file into a RocksDB database.')
    parser.add_argument('db_path', type=str, help='Path to the RocksDB database')
    parser.add_argument('csv_file_path', type=str, help='Path to the CSV file containing data')

    args = parser.parse_args()

    insert_data_from_csv(args.db_path, args.csv_file_path)

if __name__ == '__main__':
    main()