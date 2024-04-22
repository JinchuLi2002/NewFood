import spacy
import json
from transformers import pipeline
# 1
# rest = []
# count = 0
# with open('yelp_dataset/yelp_academic_dataset_business.json', 'r') as f:
#     for line in f:
#         business = json.loads(line)
#         if business.get('categories') and 'Restaurants' in business['categories']:
#             rest.append(business)
#             count += 1

# # Save the filtered data to a new JSON file
# with open('processed_data/yelp_academic_dataset_restaurants.json', 'w') as j:
#     json.dump(rest, j)
#     print(f'{count} restaurants saved to yelp_academic_dataset_restaurants.json')

# 2
# with open('processed_data/yelp_academic_dataset_restaurants.json', 'r') as f:
#     restaurants = json.load(f)
#     restaurant_ids = [restaurant['business_id'] for restaurant in restaurants]
# with open('yelp_dataset/yelp_academic_dataset_review.json', 'r') as f:
#     count = 0
#     reviews_usable = []
#     for line in f:
#         review = json.loads(line)
#         if review['business_id'] in restaurant_ids:
#             count += 1
#             reviews_usable.append(review)
#             print(count)
# with open('processed_data/yelp_academic_dataset_reviews_restaurants.json', 'w') as j:
#     json.dump(reviews_usable, j)
#     print(f'{count} reviews saved to yelp_academic_dataset_reviews_restaurants.json')


# 3
import json
import spacy
from transformers import pipeline
from collections import defaultdict

# Load spaCy model for English
nlp = spacy.load("en_core_web_sm")
# Load sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")


def extract_keywords(doc):
    """ Extracts keywords using noun chunks and filtering with POS tagging. """
    keywords = []
    for chunk in doc.noun_chunks:
        chunk_text = ' '.join(
            token.text for token in chunk if token.pos_ in ['NOUN', 'ADJ'])
        if chunk_text:
            keywords.append(chunk_text)
    return keywords


def get_sentiment(text):
    """ Get sentiment score by evaluating each sentence separately. """
    doc = nlp(text)
    sentiments = []
    for sentence in doc.sents:
        result = sentiment_pipeline(sentence.text)[0]
        sentiments.append((sentence.text, result['label'], result['score']))
    return sentiments


def save_to_disk(data, filename="processed_data/restaurant_keywords.json"):
    """ Append data to a JSON file. """
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


# Load spaCy model for English
nlp = spacy.load("en_core_web_sm")
# Load sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")


def extract_keywords(doc):
    """ Extracts keywords using noun chunks and filtering with POS tagging. """
    keywords = []
    for chunk in doc.noun_chunks:
        chunk_text = ' '.join(
            token.text for token in chunk if token.pos_ in ['NOUN', 'ADJ'])
        if chunk_text:
            keywords.append(chunk_text)
    return keywords


def get_sentiment(text):
    """ Get sentiment score by evaluating each sentence separately. """
    doc = nlp(text)
    sentiments = []
    for sentence in doc.sents:
        result = sentiment_pipeline(sentence.text)[0]
        sentiments.append((sentence.text, result['label'], result['score']))
    return sentiments


def save_to_disk(data, filename="processed_data/restaurant_keywords.json"):
    """ Append data to a JSON file. """
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


# Load business to city mapping
business_to_city = {}
businesses = json.load(
    open('processed_data/yelp_academic_dataset_restaurants.json', 'r'))
count = 0
for business in businesses:
    business_to_city[business['business_id']] = business['city']
    count += 1
    print(f'{count} / {len(businesses)}')

# Load the restaurant reviews
with open('processed_data/yelp_academic_dataset_reviews_restaurants.json', 'r') as file:
    reviews = json.load(file)

# Dictionary to hold the aggregate scores for each restaurant
restaurant_keywords = {}

# Organizing reviews by city and restaurant
city_restaurants = defaultdict(lambda: defaultdict(list))
count = 0
for review in reviews:
    city_restaurants[business_to_city[review['business_id']]
                     ][review['business_id']].append(review)
    count += 1
    print(f'{count} / {len(reviews)}')

# Process reviews in rounds
round_size = 30
all_cities = list(city_restaurants.keys())
max_loops = max(len(restaurants)
                for restaurants in city_restaurants.values()) // round_size + 1

for round_index in range(max_loops):
    for city in all_cities:
        restaurants = city_restaurants[city]
        start_idx = round_index * round_size
        end_idx = start_idx + round_size
        restaurant_ids = list(restaurants.keys())[start_idx:end_idx]

        for restaurant_id in restaurant_ids:
            # Process up to 10 reviews per restaurant
            reviews_list = restaurants[restaurant_id][:10]
            for review in reviews_list:
                review_text = review['text']
                doc = nlp(review_text)

                # Extract keywords
                keywords = extract_keywords(doc)

                # Determine sentiment of the review
                sentiments = get_sentiment(review_text)

                # Initialize restaurant in dictionary if not present
                if restaurant_id not in restaurant_keywords:
                    restaurant_keywords[restaurant_id] = {}

                # Aggregate keyword scores based on sentiment proximity
                for sentence, sentiment, score in sentiments:
                    for keyword in keywords:
                        if keyword in sentence:
                            if keyword not in restaurant_keywords[restaurant_id]:
                                restaurant_keywords[restaurant_id][keyword] = {
                                    'positive': 0, 'negative': 0, 'neutral': 0}
                            if sentiment == 'POSITIVE':
                                restaurant_keywords[restaurant_id][keyword]['positive'] += score
                            elif sentiment == 'NEGATIVE':
                                restaurant_keywords[restaurant_id][keyword]['negative'] += score
                            else:
                                restaurant_keywords[restaurant_id][keyword]['neutral'] += score

                # Save after each review
                save_to_disk(restaurant_keywords)

                # Detailed logging
                print(
                    f"Round {round_index + 1}, City {city}: Processed restaurant {restaurant_id}")

# Final save and completion notice
save_to_disk(restaurant_keywords)
print("Keyword sentiment analysis completed and saved.")
