# ============================================================
#  CLI Weather App
#  Created by   : VISHNU S
#  Project       : Oasis Infobyte Python Internship
#  Description   : A command-line weather application that
#                  fetches real-time weather data using the
#                  OpenWeatherMap API.
# ============================================================

import requests
import sys
from datetime import datetime


# ----------------------------------------------------------
#  CONFIGURATION
#  Get your free API key at https://openweathermap.org/api
#  Sign up -> go to API keys -> copy your key below
# ----------------------------------------------------------
API_KEY = "f04f01059831da7a2544d4697d73a271"   # <-- Replace with your actual key

BASE_URL  = "https://api.openweathermap.org/data/2.5/weather"


# ── Helpers ──────────────────────────────────────────────

def celsius_to_fahrenheit(c):
    return round((c * 9 / 5) + 32, 1)


def fahrenheit_to_celsius(f):
    return round((f - 32) * 5 / 9, 1)


def get_wind_direction(degrees):
    """Turn a degree value into a compass label like NE or SSW."""
    compass = [
        "N", "NNE", "NE", "ENE",
        "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW",
        "W", "WNW", "NW", "NNW"
    ]
    idx = round(degrees / 22.5) % 16
    return compass[idx]


def weather_emoji(condition):
    """Return a small emoji that matches the weather condition string."""
    cond = condition.lower()
    if "clear" in cond or "sunny" in cond:
        return "☀️ "
    elif "cloud" in cond:
        return "☁️ "
    elif "drizzle" in cond:
        return "🌦️ "
    elif "rain" in cond:
        return "🌧️ "
    elif "thunder" in cond or "storm" in cond:
        return "⛈️ "
    elif "snow" in cond or "sleet" in cond:
        return "❄️ "
    elif "mist" in cond or "fog" in cond or "haze" in cond:
        return "🌫️ "
    else:
        return "🌤️ "


# ── API calls ────────────────────────────────────────────

def fetch_by_city(city, unit):
    """Call the API using a city name string."""
    params = {
        "q":      city,
        "appid":  API_KEY,
        "units":  unit,
    }
    return _call_api(params, label=f"city '{city}'")


def fetch_by_zip(zip_code, country_code, unit):
    """Call the API using a ZIP / PIN code + country code."""
    params = {
        "zip":   f"{zip_code},{country_code}",
        "appid": API_KEY,
        "units": unit,
    }
    return _call_api(params, label=f"ZIP '{zip_code}'")


def _call_api(params, label):
    """Shared request logic with error handling."""
    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    except requests.exceptions.ConnectionError:
        print("\n  [ERROR] No internet connection. Please check your network.\n")
    except requests.exceptions.Timeout:
        print("\n  [ERROR] Request timed out. Please try again.\n")
    except requests.exceptions.HTTPError:
        code = resp.status_code
        if code == 401:
            print("\n  [ERROR] Invalid API key. Double-check the API_KEY variable.\n")
        elif code == 404:
            print(f"\n  [ERROR] Location not found for {label}. Check the spelling / code.\n")
        else:
            print(f"\n  [ERROR] HTTP {code} received for {label}.\n")
    except Exception as e:
        print(f"\n  [ERROR] Something unexpected happened: {e}\n")

    return None


# ── Display ───────────────────────────────────────────────

def display_weather(data, unit):
    """Pretty-print the weather data returned by the API."""

    if data is None:
        return

    # Pull out the values we need
    city        = data["name"]
    country     = data["sys"]["country"]
    condition   = data["weather"][0]["main"]
    description = data["weather"][0]["description"].title()
    temp        = data["main"]["temp"]
    feels_like  = data["main"]["feels_like"]
    temp_min    = data["main"]["temp_min"]
    temp_max    = data["main"]["temp_max"]
    humidity    = data["main"]["humidity"]
    pressure    = data["main"]["pressure"]
    clouds      = data["clouds"]["all"]
    wind_speed  = data["wind"]["speed"]
    wind_deg    = data["wind"].get("deg", 0)
    visibility  = data.get("visibility", None)
    sunrise     = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p")
    sunset      = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p")
    now         = datetime.now().strftime("%A, %d %B %Y  |  %I:%M %p")

    # Labels that depend on the chosen unit system
    if unit == "metric":
        t_unit     = "°C"
        s_unit     = "m/s"
        alt_temp   = celsius_to_fahrenheit(temp)
        alt_unit   = "°F"
    else:
        t_unit     = "°F"
        s_unit     = "mph"
        alt_temp   = fahrenheit_to_celsius(temp)
        alt_unit   = "°C"

    wind_dir = get_wind_direction(wind_deg)
    icon     = weather_emoji(condition)

    vis_str = (
        f"{round(visibility / 1000, 1)} km"
        if visibility is not None
        else "N/A"
    )

    # Output block
    print()
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║            🌍  CLI WEATHER FORECAST APP              ║")
    print("  ║                   Created by VISHNU S                ║")
    print("  ╚══════════════════════════════════════════════════════╝")
    print()
    print(f"  📍  Location     :  {city}, {country}")
    print(f"  🕐  Fetched at   :  {now}")
    print()
    print("  ┌──────────────────────────────────────────────────────┐")
    print("  │                    CURRENT CONDITIONS                │")
    print("  ├──────────────────────────────────────────────────────┤")
    print(f"  │  {icon} Condition   :  {description:<36}│")
    print(f"  │  🌡️  Temperature  :  {temp}{t_unit}  ({alt_temp} {alt_unit}){'':<21}│")
    print(f"  │  🤔  Feels Like   :  {feels_like}{t_unit}{'':<33}│")
    print(f"  │  🔼  Max Temp     :  {temp_max}{t_unit}{'':<33}│")
    print(f"  │  🔽  Min Temp     :  {temp_min}{t_unit}{'':<33}│")
    print("  ├──────────────────────────────────────────────────────┤")
    print("  │                  ATMOSPHERE & WIND                   │")
    print("  ├──────────────────────────────────────────────────────┤")
    print(f"  │  💧  Humidity     :  {humidity}%{'':<34}│")
    print(f"  │  📊  Pressure     :  {pressure} hPa{'':<31}│")
    print(f"  │  👁️   Visibility   :  {vis_str:<35}│")
    print(f"  │  ☁️   Cloud Cover  :  {clouds}%{'':<34}│")
    print(f"  │  💨  Wind         :  {wind_speed} {s_unit}  Direction: {wind_dir:<13}│")
    print("  ├──────────────────────────────────────────────────────┤")
    print("  │                    SUN TIMINGS                       │")
    print("  ├──────────────────────────────────────────────────────┤")
    print(f"  │  🌅  Sunrise      :  {sunrise:<35}│")
    print(f"  │  🌇  Sunset       :  {sunset:<35}│")
    print("  └──────────────────────────────────────────────────────┘")
    print()


# ── Input helpers ─────────────────────────────────────────

def ask_unit():
    """Let the user pick Celsius or Fahrenheit."""
    while True:
        print()
        print("  Select temperature unit:")
        print("  [1] Celsius  (metric)   — default")
        print("  [2] Fahrenheit (imperial)")
        choice = input("\n  Your choice (press Enter for Celsius): ").strip()

        if choice in ("", "1"):
            return "metric"
        elif choice == "2":
            return "imperial"
        else:
            print("  [!] Please type 1 or 2.")


def is_zip_code(text):
    """Return True if the input looks like a numeric ZIP / PIN code."""
    return text.isdigit() and 4 <= len(text) <= 6


# ── Main loop ─────────────────────────────────────────────

def main():
    print()
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║         🌦️   CLI WEATHER APP  —  VISHNU S   🌦️       ║")
    print("  ║              Oasis Infobyte Python Internship         ║")
    print("  ╚══════════════════════════════════════════════════════╝")

    # Warn early if the user forgot to set the key
    if API_KEY == "your_api_key_here":
        print()
        print("  ⚠️  WARNING: API key not set!")
        print("  ➜  Sign up free at https://openweathermap.org/api")
        print("  ➜  Paste your key into the API_KEY variable at the top of this file.")

    while True:
        print()
        print("  ┌────────────────────────────────────┐")
        print("  │  MAIN MENU                        │")
        print("  │  [1] Search by City Name          │")
        print("  │  [2] Search by ZIP / PIN Code     │")
        print("  │  [3] Exit                         │")
        print("  └────────────────────────────────────┘")

        option = input("\n  Enter option (1 / 2 / 3): ").strip()

        if option == "1":
            city = input("\n  Enter city name (e.g. Chennai, London): ").strip()
            if not city:
                print("  [!] City name cannot be empty.")
                continue

            unit = ask_unit()
            print(f"\n  ⏳ Fetching weather for '{city}' ...")
            data = fetch_by_city(city, unit)
            display_weather(data, unit)

        elif option == "2":
            zip_code = input("\n  Enter ZIP / PIN code: ").strip()
            if not is_zip_code(zip_code):
                print("  [!] That doesn't look like a valid ZIP/PIN code (digits only, 4–6 chars).")
                continue

            country = input("  Country code (e.g. IN, US, GB) [default: IN]: ").strip().upper()
            if not country:
                country = "IN"

            unit = ask_unit()
            print(f"\n  ⏳ Fetching weather for ZIP '{zip_code}', {country} ...")
            data = fetch_by_zip(zip_code, country, unit)
            display_weather(data, unit)

        elif option == "3":
            print()
            print("  ════════════════════════════════════")
            print("   Thank you for using the Weather App!")
            print("   Created by  :  VISHNU S")
            print("   Internship  :  Oasis Infobyte")
            print("   Goodbye! 👋")
            print("  ════════════════════════════════════")
            print()
            sys.exit(0)

        else:
            print("  [!] Invalid option. Please enter 1, 2, or 3.")
            continue

        # Ask if the user wants to check another location
        again = input("  🔁 Check another location? (yes / no): ").strip().lower()
        if again not in ("yes", "y"):
            print()
            print("  Thank you for using CLI Weather App!")
            print("  Created by VISHNU S  |  Oasis Infobyte Internship")
            print("  Goodbye! 👋")
            print()
            break


if __name__ == "__main__":
    main()