# New Food: US Food Explorer

## Description
Restaurant finder web application that provides tailored recommendations based on user-provided keywords, using keyword extraction via spaCy and sentiment analysis via Transformers.

## Disclaimer
* Due to data limitations, the only available states for location filtering are NJ, PA, CA,FL,LA,MO,NV
* The review data is from the Yelp dataset and we are not responsible for the content of the reviews, this is a proof of concept project.

## Prerequisites
- Elasticsearch
- Django
- spaCy
- Transformers
- React

## Dataset
The dataset used for this project is the Yelp dataset, which can be found [here](https://www.yelp.com/dataset). We have included data cleaning and processing steps in `utils/`.

## Running Locally
1. Start Elastic Search: `docker run --rm -p 9200:9200 -p 9300:9300 -e "xpack.security.enabled=false" -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.7.0`
2. Populate Elastic Search: `python3 utils/search.py`
   * Note that this would require `yelp_academic_dataset_reviews_restaurants.json` and `yelp_academic_dataset_restaurants.json` to be also present in the `processed_data` directory. We could not upload it here due to size constraints. You can download them from the below links
     * https://drive.google.com/file/d/1wvbhwVSkQ47OwKq7YZd9yXdyEXM2iv9W/view?usp=sharing
     * https://drive.google.com/file/d/1CAUpp54ncB7NQhniKz0DxW5ntH5ORMMl/view?usp=sharing
* Start Django Backend: `python3 newfood_app/manage.py runserver 5001`
* Start React Frontend: `cd frontend && npm start`