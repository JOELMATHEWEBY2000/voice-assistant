import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# API Keys
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")


def validate_keys():
    """
    Check whether required API keys are available.
    """
    missing = []

    if not WEATHER_API_KEY:
        missing.append("WEATHER_API_KEY")

    if not GNEWS_API_KEY:
        missing.append("GNEWS_API_KEY")

    if missing:
        print("\n========== WARNING ==========")
        print("Missing API Keys:")

        for key in missing:
            print(f"- {key}")

        print("\nCreate a .env file in the project root.")
        print("=============================\n")
    else:
        print("All API keys loaded successfully.")


if __name__ == "__main__":
    validate_keys()