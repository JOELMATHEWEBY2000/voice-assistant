import requests
from config import NEWS_API_KEY

BASE_URL = "https://newsapi.org/v2/top-headlines"


def get_news(country="in", limit=5):

    if not NEWS_API_KEY:
        return ["NEWS_API_KEY is missing."]

    params = {
        "country": country,
        "apiKey": NEWS_API_KEY
    }

    try:

        response = requests.get(BASE_URL, params=params, timeout=10)

        data = response.json()

        print(data)      # View this in the Render logs

        if response.status_code != 200:

            return [
                data.get("message", "Unable to fetch news.")
            ]

        articles = data.get("articles", [])

        if not articles:
            return ["No news articles found."]

        headlines = []

        for article in articles[:limit]:

            headlines.append(article.get("title"))

        return headlines

    except Exception as e:

        return [str(e)]