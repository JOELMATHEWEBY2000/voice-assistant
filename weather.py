import requests
from config import WEATHER_API_KEY

def get_weather(city):

    # Step 1: Get coordinates
    geo_url = "https://api.openweathermap.org/geo/1.0/direct"

    geo_params = {
        "q": city,
        "limit": 1,
        "appid": WEATHER_API_KEY
    }

    geo_response = requests.get(geo_url, params=geo_params)
    geo_data = geo_response.json()

    if not geo_data:
        return "City not found."

    lat = geo_data[0]["lat"]
    lon = geo_data[0]["lon"]

    # Step 2: Get weather using coordinates
    weather_url = "https://api.openweathermap.org/data/2.5/weather"

    weather_params = {
        "lat": lat,
        "lon": lon,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    weather_response = requests.get(weather_url, params=weather_params)
    data = weather_response.json()

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    condition = data["weather"][0]["description"]

    return f"""
Weather in {data['name']}

Temperature : {temp} °C

Humidity : {humidity} %

Condition : {condition.title()}
"""