import requests
from config import WEATHER_API_KEY


BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    """
    Fetch current weather for the given city.
    """

    if not WEATHER_API_KEY:
        return "Weather API key is missing."

    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(BASE_URL, params=params, timeout=10)

        response.raise_for_status()

        data = response.json()

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].title()
        wind_speed = data["wind"]["speed"]

        message = (
            f"Current weather in {city.title()}.\n"
            f"Temperature: {temperature}°C\n"
            f"Feels Like: {feels_like}°C\n"
            f"Condition: {description}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} meter per second."
        )

        return message

    except requests.exceptions.HTTPError:

        return "City not found."

    except requests.exceptions.ConnectionError:

        return "Unable to connect to the weather service."

    except requests.exceptions.Timeout:

        return "Weather request timed out."

    except Exception:

        return "Unable to fetch weather information."


if __name__ == "__main__":

    city = input("Enter City: ")

    print(get_weather(city))