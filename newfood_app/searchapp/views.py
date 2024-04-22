from django.http import JsonResponse
from elasticsearch import Elasticsearch
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

es = Elasticsearch("http://localhost:9200")

@csrf_exempt  # Disable CSRF for this view, handle security appropriately
@require_http_methods(["POST"])
def search(request):
    data = json.loads(request.body.decode('utf-8'))
    print("Received data:", data)
    term = data['term']
    sort_by = data.get('sort_by', 'score')  # Default to score if no sort_by provided
    filter_state = data.get('state')  # State filter (optional)

    query = {
        "query": {
            "function_score": {
                "query": {"match": {"keyword": term}},
                "functions": [
                    {
                        "script_score": {
                            "script": {
                                "source": "50000 + doc['positive'].value - 200 * doc['negative'].value - 5 * doc['neutral'].value",
                                "lang": "painless"
                            }
                        }
                    }
                ],
                "boost_mode": "replace"
            }
        },
        "size": 30  # Increased to 30 to apply filters after
    }
    results = es.search(index="keywords", body=query)
    hits = results['hits']['hits']
    business_ids = [hit["_source"]["business_id"] for hit in hits]
    score_map = {hit["_source"]["business_id"]: hit['_score'] for hit in hits}

    # Construct the query for restaurant details, potentially filtered by state
    restaurant_query_body = {
        "query": {
            "terms": {
                "business_id": business_ids
            }
        }
    }
    if filter_state:  # If a state filter is provided, apply it
        restaurant_query_body["query"] = {
            "bool": {
                "must": [
                    {"terms": {"business_id": business_ids}},
                    {"match": {"state": filter_state}}
                ]
            }
        }

    restaurant_results = es.search(index="restaurants", body=restaurant_query_body)
    restaurant_hits = {hit["_source"]["business_id"]: hit["_source"] for hit in restaurant_results['hits']['hits']}

    # Sorting logic remains unchanged
    sorted_restaurants = sorted(
        restaurant_hits.values(),
        key=lambda x: float(x['stars']) if sort_by == 'stars' else int(x['review_count']) if sort_by == 'popularity' else score_map[x['business_id']],
        reverse=True
    )[:10]  # Limit to top 10 after sorting

    output = []
    for restaurant in sorted_restaurants:
        business_id = restaurant['business_id']
        review_query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"business_id": business_id}},
                        {"match_phrase": {"text": term}}
                    ]
                }
            },
            "size": 1
        }
        review_result = es.search(index="reviews", body=review_query)
        review_text = review_result['hits']['hits'][0]['_source']['text'] if review_result['hits']['hits'] else "No review found"

        output.append({
            "custom_score": score_map.get(business_id, 0),
            "business_id": business_id,
            "restaurant_name": restaurant['name'],
            "address": restaurant['address'],
            "review_text": review_text,
            "stars": restaurant['stars'],
            "review_count": restaurant['review_count']
        })

    return JsonResponse(output, safe=False)

# Remember to map this view in urls.py
