import os
import mimetypes
import json


def create_index(base_dir, index_file):
    if not os.path.exists(base_dir):
        print("Base directory does not exist.")
        return
    index = {}
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'unknown'

            # Create an entry in the index for each file
            index_entry = {
                'name': file_name,
                'path': file_path,
                'size': file_size,
                'content_type': content_type
            }

            # Add the index entry to the index dictionary
            index[file_path] = index_entry

    # Write the index dictionary to the index file
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=4)


def search_index(index_file, query):
    with open(index_file, 'r') as f:
        index = json.load(f)

    results = []
    for file_path, entry in index.items():
        if query.lower() in entry['name'].lower():
            results.append(entry)

    return results


while True:
    print("\nFile Indexer")
    print("1. Index a Directory")
    print("2. Search Files")
    print("3. Exit")
    
    choice = input("\nEnter your choice: ")
    
    if choice == "1":
        print("\nIndexing a Directory")
        base_directory = input("Enter the base directory path Example 'test_data' : ")
        index_filename = input("Enter the index file name: ")
        create_index(base_directory, index_filename)
        print("Indexing complete.")
    
    elif choice == "2":
        print("\nSearching Files")
        index_filename = input("Enter the index file name: ")

        if not os.path.exists(index_filename):
            print("Index file name does not exist. Please enter a valid index file to search.")
        else:
            search_query = input("Enter the search query: ")
            search_results = search_index(index_filename, search_query)

            if len(search_results) > 0:
                print(f"\nFound {len(search_results)} matching file(s):")
                for result in search_results:
                    print(f"Name: {result['name']}")
                    print(f"Path: {result['path']}")
                    print(f"Size: {result['size']} bytes")
                    print(f"Content Type: {result['content_type']}")
                    print()
            else:
                print("No matching files found.")

    elif choice == "3":
        break
    
    else:
        print("Invalid choice. Please try again.")

print("\nExiting File Indexer")
