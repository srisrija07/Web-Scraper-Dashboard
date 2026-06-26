
Web Scraper Dashboard (Python Script Version)
Fixed version – works in terminal (NO Jupyter widgets)
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import Counter


# Scraping Functions
-------------------------

def scrape_weather():
    cities = ["London", "New York", "Tokyo", "Delhi", "Sydney"]
    data = []

    for city in cities:
        url = f"https://wttr.in/{city}?format=%t"
        try:
            response = requests.get(url, timeout=5)
            temp = response.text.strip()
            data.append({"City": city, "Temperature": temp})
        except Exception:
            data.append({"City": city, "Temperature": "N/A"})

    return pd.DataFrame(data)


def scrape_news(topic="General"):
    urls = {
        "General": "https://www.bbc.com/news",
        "Sports": "https://www.bbc.com/sport",
        "Environment": "https://www.bbc.com/news/science_and_environment",
        "Social Trends": "https://www.bbc.com/news/world",
    }

    url = urls.get(topic, urls["General"])
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    headlines = [
        h.get_text().strip()
        for h in soup.select("h3")
        if len(h.get_text().strip()) > 10
    ]

    return pd.DataFrame(headlines[:15], columns=["Headline"])


def scrape_crypto():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 5,
        "page": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    return pd.DataFrame(
        [{"Name": c["name"], "Price (USD)": c["current_price"]} for c in data]
    )

# -------------------------
# Visualization Functions
# -------------------------

def plot_weather(df):
    df["Temperature"] = (
        df["Temperature"]
        .str.replace("+", "", regex=False)
        .str.replace("°C", "", regex=False)
        .str.replace("°F", "", regex=False)
    )
    df["Temperature"] = pd.to_numeric(df["Temperature"], errors="coerce")

    df.plot(x="City", y="Temperature", kind="bar", legend=False)
    plt.title("City Temperatures")
    plt.ylabel("Temperature")
    plt.show()


def plot_news(df):
    words = " ".join(df["Headline"]).split()
    common = Counter(words).most_common(10)

    if not common:
        print("No data to plot")
        return

    freq_df = pd.DataFrame(common, columns=["Word", "Frequency"])
    freq_df.plot(x="Word", y="Frequency", kind="bar", legend=False)
    plt.title("Top Words in News Headlines")
    plt.ylabel("Count")
    plt.show()


def plot_crypto(df):
    df.plot(x="Name", y="Price (USD)", kind="bar", legend=False)
    plt.title("Top 5 Cryptocurrencies")
    plt.ylabel("Price (USD)")
    plt.show()

# -------------------------
# Main Menu (REPLACEMENT FOR WIDGETS)
# -------------------------

def main():
    print("\nWEB SCRAPER DASHBOARD")
    print("1. Weather Data")
    print("2. News Headlines")
    print("3. Cryptocurrency Prices")
    print("4. Exit")

    choice = input("\nEnter your choice (1-4): ")

    if choice == "1":
        df = scrape_weather()
        df.to_csv("weather.csv", index=False)
        print(df)
        plot_weather(df)

    elif choice == "2":
        print("\nTopics: General | Sports | Environment | Social Trends")
        topic = input("Enter topic: ").strip()
        df = scrape_news(topic)
        df.to_csv("news.csv", index=False)
        print(df)
        plot_news(df)

    elif choice == "3":
        df = scrape_crypto()
        df.to_csv("crypto.csv", index=False)
        print(df)
        plot_crypto(df)

    elif choice == "4":
        print("Exiting program.")

    else:
        print("Invalid choice!")

# -------------------------
# Run Program
# -------------------------

if __name__ == "__main__":
    main()

