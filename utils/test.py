# from elasticsearch import Elasticsearch
# from elasticsearch.exceptions import ConnectionError

# def test_elasticsearch_connection():
#     try:
#         # Connect to Elasticsearch
#         es = Elasticsearch('http://localhost:9200')

#         # Check if cluster is healthy
#         if es.cluster.health()['status'] == 'green':
#             print("Elasticsearch cluster is healthy!")
#         else:
#             print("Elasticsearch cluster is not healthy.")

#         # Test index creation
#         index_name = "test_index"
#         if not es.indices.exists(index=index_name):
#             es.indices.create(index=index_name)
#             print(f"Index '{index_name}' created successfully.")
#         else:
#             print(f"Index '{index_name}' already exists.")

#         # Test document indexing
#         doc_body = {"title": "Test Document", "content": "This is a test document for Elasticsearch."}
#         res = es.index(index=index_name, body=doc_body)
#         if res['result'] == 'created':
#             print("Document indexed successfully.")
#         else:
#             print("Failed to index document.")

#         # Test document retrieval
#         doc_id = res['_id']
#         retrieved_doc = es.get(index=index_name, id=doc_id)
#         if retrieved_doc['found']:
#             print("Document retrieved successfully.")
#             print(retrieved_doc['_source'])
#         else:
#             print("Failed to retrieve document.")

#         # Delete the index after testing
#         es.indices.delete(index=index_name)
#         print(f"Index '{index_name}' deleted successfully.")
        
#     except ConnectionError:
#         print("Failed to connect to Elasticsearch. Make sure Elasticsearch is running.")

# if __name__ == "__main__":
#     test_elasticsearch_connection()
# import json
# with open("processed_data/json-fixer.json", 'r') as file:
#     d = json.load(file)
#     print(len(d.items()))

import json

# Load the data from a JSON file
with open('processed_data/yelp_academic_dataset_restaurants.json', 'r') as file:
    data = json.load(file)

# Collect unique states
unique_states = set()
for restaurant in data:
    unique_states.add(restaurant['state'])

# Print all unique states
print(unique_states)
