import requests
from config import GNEWS_API_KEY

BASE_URL = "https://gnews.io/api/v4/top-headlines"


def get_news(country="in", category="general", limit=5):

    if not GNEWS_API_KEY:
        return ["GNews API key is missing."]

    params = {
        "country": country,
        "category": category,
        "lang": "en",
        "max": limit,
        "apikey": GNEWS_API_KEY
    }

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )

        data = response.json()

        print(data)

        if response.status_code != 200:

            return [
                data.get("errors", ["Unable to fetch news"])[0]
            ]

        articles = data.get("articles", [])

        if not articles:
            return ["No news available."]

        headlines = []

        for article in articles:

            title = article.get("title", "No Title")

            source = article.get("source", {}).get("name", "")

            headlines.append(
                f"{title} ({source})"
            )

        return headlines

    except requests.exceptions.Timeout:

        return ["Request timed out."]

    except requests.exceptions.ConnectionError:

        return ["Unable to connect to GNews API."]

    except Exception as e:

        return [str(e)]


if __name__ == "__main__":

    news = get_news()

    print("\nToday's News\n")

    for i, headline in enumerate(news, 1):

        print(i, headline)