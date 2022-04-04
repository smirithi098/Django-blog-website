from dotenv import load_dotenv
import os
import requests
import random
from datetime import datetime, date


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

    response = requests.get(url=url, headers=headers, params=parameters)
    response.raise_for_status()

    data = response.json()
    img_url = data['photos'][random.randint(1, 5)]['src']['landscape']
    return img_url


def get_time_difference(obj_time):
    today_Date = date.today()
    otp_created_time = obj_time

    new_date = datetime.combine(today_Date, otp_created_time)

    current_date = datetime.now()

    time_diff = current_date - new_date

    minutes = divmod(time_diff.seconds, 60)

    return minutes[1]
