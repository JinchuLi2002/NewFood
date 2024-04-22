from elasticsearch import Elasticsearch, helpers
import json
from datetime import datetime
es = Elasticsearch("http://localhost:9200")


def create_index(index_name, mappings):
    es.options(ignore_status=400).indices.create(index=index_name, body=mappings)

def index_data(index_name, data):
    try:
        helpers.bulk(es, data, index=index_name)
    except helpers.BulkIndexError as e:
        print("Errors occurred while indexing data:", e.errors)


# Define mappings for the restaurant index
restaurant_mappings = {
    "mappings": {
        "properties": {
            "business_id": {"type": "keyword"},
            "name": {"type": "text"},
            "address": {"type": "text"},
            "city": {"type": "text"},
            "state": {"type": "text"},
            "postal_code": {"type": "text"},
            "latitude": {"type": "float"},
            "longitude": {"type": "float"},
            "stars": {"type": "float"}
        }
    }
}

# Define mappings for the review index
review_mappings = {
    "mappings": {
        "properties": {
            "review_id": {"type": "keyword"},
            "business_id": {"type": "keyword"},
            "date": {"type": "date", "format": "yyyy-MM-dd"},  # Ensure correct date format
            "text": {"type": "text"}
        }
    }
}


# Define mappings for the keywords index
keywords_mappings = {
    "mappings": {
        "properties": {
            "business_id": {"type": "keyword"},
            "keyword": {"type": "text"},
            "positive": {"type": "float"},
            "negative": {"type": "float"},
            "neutral": {"type": "float"}
        }
    }
}
def format_date(date_str):
    return datetime.strptime(date_str.split(' ')[0], '%Y-%m-%d').date().isoformat()
# Create indices
create_index("restaurants", restaurant_mappings)
create_index("keywords", keywords_mappings)
create_index("reviews", review_mappings)

# Index restaurant data
with open("../processed_data/yelp_academic_dataset_restaurants.json", 'r') as file:
    restaurant_data = [{"_id": item["business_id"], **item} for item in json.load(file)]
    index_data("restaurants", restaurant_data)

# Index keywords data
with open("../processed_data/restaurant_keywords copy.json", 'r') as file:
    keywords_content = json.load(file)
    keyword_data = [
        {"_id": f"{key}_{k}", "business_id": key, "keyword": k, "positive": v['positive'], "negative": v['negative'], "neutral": v['neutral']}
        for key, terms in keywords_content.items()
        for k, v in terms.items()
    ]
    index_data("keywords", keyword_data)

# Index review data
with open("../processed_data/yelp_academic_dataset_reviews_restaurants.json", 'r') as file:
    reviews = json.load(file)  # Load the entire JSON file as a list of dictionaries
    review_data = [
        {
            "_id": review["review_id"],
            "business_id": review["business_id"],
            "date": format_date(review["date"]),
            "text": review["text"]
        }
        for review in reviews
    ]
    index_data("reviews", review_data)

def search_restaurants(term):
    # Search for keywords that match the term, and aggregate the positive sentiment
    query = {
        "query": {
            "match": {"keyword": term}
        },
        "size": 5,  # Limit the number of results to the top 5
        "sort": [{"positive": {"order": "desc"}}]  # Sort by positive sentiment score
    }
    results = es.search(index="keywords", body=query)
    hits = results['hits']['hits']
    business_ids = [hit["_source"]["business_id"] for hit in hits]

    # Fetch restaurant details based on business IDs
    restaurant_query = {
        "query": {
            "terms": {
                "business_id": business_ids
            }
        }
    }
    restaurant_results = es.search(index="restaurants", body=restaurant_query)
    restaurant_hits = {hit["_source"]["business_id"]: hit["_source"] for hit in restaurant_results['hits']['hits']}

    # Print results
    for hit in hits:
        business_id = hit["_source"]["business_id"]
        print(f"Sentiment Score: {hit['_source']['positive']} related to {term}.")
        if business_id in restaurant_hits:
            restaurant = restaurant_hits[business_id]
            print(f"Recommendation: {restaurant['name']} located at {restaurant['address']}")


def main():
    while True:
        term = input("Enter a search term, or 'exit' to quit: ").strip()
        if term.lower() == 'exit':
            break
        if not term:
            print("Please enter a valid search term.")
            continue

        # Call the search function
        search_restaurants(term)

if __name__ == "__main__":
    main()
