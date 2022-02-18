from dotenv import load_dotenv
import os
import requests
import random

load_dotenv(".env")
pexels_api = os.environ.get("API_KEY")


def get_image_url(tag):
    url = "https://api.pexels.com/v1/search"

    headers = {"Authorization": pexels_api}
    parameters = {
        "query": tag,
        "orientation": "landscape",
        "per_page": 5
    }

    try:
        response = requests.get(url=url, headers=headers, params=parameters)
    except requests.HTTPError as error:
        print(error)
    else:
        data = response.json()
        img_url = data['photos'][random.randint(1, 5)]['src']['landscape']
        return img_url

