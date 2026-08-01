import requests
from config import NEWS_API_KEY

BASE_URL = "https://newsapi.org/v2/top-headlines"


def get_news(country="in", category=None, limit=5):
    """
    Fetch top news headlines.

    Parameters:
        country : Country code (default: India)
        category : business, sports, technology, health, science, entertainment
        limit : Number of headlines

    Returns:
        List of news headlines
    """

    if not NEWS_API_KEY:
        return []

    params = {
        "country": country,
        "apiKey": NEWS_API_KEY
    }

    if category:
        params["category"] = category

    try:

        response = requests.get(BASE_URL, params=params, timeout=10)

        response.raise_for_status()

        data = response.json()

        articles = data.get("articles", [])

        headlines = []

        for article in articles[:limit]:

            title = article.get("title")

            source = article.get("source", {}).get("name", "Unknown")

            headlines.append(f"{title} (Source: {source})")

        return headlines

    except requests.exceptions.ConnectionError:

        return []

    except requests.exceptions.Timeout:

        return []

    except Exception:

        return []


if __name__ == "__main__":

    news = get_news()

    if len(news) == 0:

        print("No news available.")

    else:

        print("\nToday's Headlines\n")

        for i, headline in enumerate(news, start=1):

            print(f"{i}. {headline}")