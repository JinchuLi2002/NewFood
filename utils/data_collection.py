
# import pandas as pd
# import requests
# api_key = 'r3G-1JzDYd38QJHbt_YNEDWBXNlwI7ikf5q_9TCoCQBdpbO5q4Ffht8UCE80-RNVYkOkzPIuHNLaE7eainkCKIhRoJ_CfABQkq8XX1XJA-QJInGqj91e_hoHkTckZnYx'


# def fetch_yelp_data(api_key, city, category="restaurants", sort_by="rating", limit=20):
#     """ Fetches business data from Yelp API based on specified parameters. """
#     headers = {'Authorization': f'Bearer {api_key}'}
#     url = "https://api.yelp.com/v3/businesses/search"
#     params = {
#         'location': city,
#         'categories': category,
#         'sort_by': sort_by,
#         'limit': limit
#     }
#     response = requests.get(url, headers=headers, params=params)
#     return response.json()


# def fetch_reviews(api_key, business_id, sort_by='default'):
#     """ Fetches reviews for a specific business using Yelp API with sorting. """
#     headers = {'Authorization': f'Bearer {api_key}'}
#     url = f"https://api.yelp.com/v3/businesses/{business_id}/reviews?limit=20&sort_by=yelp_sort"
#     print(business_id)
#     # Fetches only 3 reviews at a time
#     response = requests.get(url, headers=headers)
#     print(response.json())
#     return response.json()


# def save_to_csv(data, filename):
#     """ Saves the data to a CSV file. """
#     df = pd.DataFrame(data)
#     df.to_csv(filename, index=False)


# curl -X POST "https://api.zembra.io/reviews/subscription/yelp/?slug=tbo8sNRbN_upwKpEP-nZTQ&fields[]=id&fields[]=text&fields[]=timestamp&fields[]=rating&includeRawData=true&sortBy=timestamp&sortDirection=DESC&limit=3&autoRenew=false" \
# -H "Accept: application/json" \
# -H "Authorization: Bearer 3GIjnZDuLvJsdGYqSTrtWsaQo4T945DWcdkqLP37l57XfPkiUK2OAiKOi0e2W6rk6aJ5bOpx7yelL9Q7s7F3YqiKOZfb03KijJw2qGbnoakEF74NIyUWgBtre7f3l2b7"


# # Set up your API key and city list
# cities = ['New York', 'Los Angeles', 'Chicago', 'Houston']

# # Loop through each city
# for city in cities:
#     businesses = fetch_yelp_data(api_key, city)
#     all_reviews = []

#     # Fetch reviews for each business under different sorting methods
#     for business in businesses.get('businesses', []):
#         # Default sorted reviews
#         reviews_default = fetch_reviews(api_key, business['id'], 'default')
#         # Newest first sorted reviews
#         reviews_newest = fetch_reviews(api_key, business['id'], 'newest')

#         # Combine reviews from both sorts
#         for review in reviews_default.get('reviews', []) + reviews_newest.get('reviews', []):
#             all_reviews.append({
#                 'Business ID': business['id'],
#                 'Business Name': business['name'],
#                 'Review ID': review['id'],
#                 'Review': review['text'],
#                 'Rating': review['rating'],
#                 'Time Created': review['time_created'],
#                 'Sort By': 'Default' if review in reviews_default.get('reviews', []) else 'Newest'
#             })

#     # Save reviews data to a CSV file for each city
#     filename = f'{city}_reviews.csv'
#     save_to_csv(all_reviews, filename)
