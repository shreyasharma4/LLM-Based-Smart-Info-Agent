import requests
from datetime import datetime, timedelta
from langchain.tools import tool


# ✅ WEATHER TOOL
@tool("get_weather")
def get_weather(city: str) -> str:
    """Fetches current weather for a given city using wttr.in API."""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        res = requests.get(url, timeout=10).json()
        temp = res["current_condition"][0]["temp_C"]
        desc = res["current_condition"][0]["weatherDesc"][0]["value"]
        return f"The temperature in {city} is {temp}°C with {desc.lower()}."
    except Exception as e:
        return f"Failed to fetch weather data for {city}: {e}"


# ✅ CRYPTO TOOL
@tool("get_crypto_price")
def get_crypto_price(symbol: str = "bitcoin") -> str:
    """Fetches live cryptocurrency prices from CoinGecko."""
    try:
        url = (
            f"https://api.coingecko.com/api/v3/simple/price"
            f"?ids={symbol.lower()}&vs_currencies=usd"
        )
        res = requests.get(url, timeout=10).json()
        price = res.get(symbol.lower(), {}).get("usd")
        if price:
            return f"The current price of {symbol.capitalize()} is ${price} USD."
        return f"Couldn't find price data for {symbol}."
    except Exception as e:
        return f"Failed to fetch crypto data: {e}"


# ✅ NEW: COMPARE CRYPTO TOOL
@tool("compare_crypto_prices")
def compare_crypto_prices(symbols: list) -> str:
    """Compares live prices of multiple cryptocurrencies using CoinGecko."""
    try:
        if not symbols or not isinstance(symbols, (list, tuple)):
            return "Please provide a list of cryptocurrency names to compare."

        results = []
        for sym in symbols:
            url = (
                f"https://api.coingecko.com/api/v3/simple/price"
                f"?ids={sym.lower()}&vs_currencies=usd"
            )
            res = requests.get(url, timeout=10).json()
            price = res.get(sym.lower(), {}).get("usd")
            if price:
                results.append(f"{sym.capitalize()}: ${price} USD")
            else:
                results.append(f"{sym.capitalize()}: data not found")

        return " | ".join(results)

    except Exception as e:
        return f"Failed to compare crypto prices: {e}"


# ✅ COMPARE WEATHER TOOL
@tool("compare_weather")
def compare_weather(cities: list) -> str:
    """Compares current weather across multiple cities."""
    results = []
    for city in cities:
        try:
            url = f"https://wttr.in/{city}?format=j1"
            res = requests.get(url, timeout=10).json()
            temp = res["current_condition"][0]["temp_C"]
            desc = res["current_condition"][0]["weatherDesc"][0]["value"]
            results.append(f"{city}: {temp}°C, {desc.lower()}")
        except Exception as e:
            results.append(f"{city}: error fetching data ({e})")
    return " | ".join(results)


# ✅ CRYPTO HISTORY TOOL
@tool("get_crypto_history")
def get_crypto_history(symbol: str = "bitcoin", period: str = "1month") -> str:
    """Fetches historical cryptocurrency data for given period (1week, 3months, 1year)."""
    try:
        symbol = symbol.lower()
        days = 30
        if "week" in period:
            days = 7
        elif "3" in period and "month" in period:
            days = 90
        elif "year" in period:
            days = 365

        url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart?vs_currency=usd&days={days}"
        res = requests.get(url, timeout=10).json()
        prices = res.get("prices", [])
        if not prices:
            return f"No historical data available for {symbol}."

        start_price = prices[0][1]
        end_price = prices[-1][1]
        change = ((end_price - start_price) / start_price) * 100
        trend = "increased" if change > 0 else "decreased"

        return (
            f"Over the last {period}, {symbol.capitalize()} has {trend} by "
            f"{abs(change):.2f}%, moving from ${start_price:.2f} to ${end_price:.2f}."
        )
    except Exception as e:
        return f"Failed to fetch historical data for {symbol}: {e}"


# ✅ RETURN ALL TOOLS
def get_agent_tools():
    return {
        "get_weather": get_weather,
        "get_crypto_price": get_crypto_price,
        "compare_crypto_prices": compare_crypto_prices,
        "compare_weather": compare_weather,
        "get_crypto_history": get_crypto_history,
    }
