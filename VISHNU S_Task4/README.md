# 🌦️ Weather Forecast App

A Python application that fetches and displays real-time weather details for any location worldwide using the **OpenWeatherMap API**.

Created by **[Vishnu S](https://github.com/vishnusadasivan2006)** as part of the **Oasis Infobyte Internship Project (OIBSIP)**.

---

## 🌟 Key Features

- 🌍 **Global Coverage**: Fetch weather parameters for any city or ZIP / PIN code globally.
- 📊 **Detailed Weather Metrics**:
  - Weather Condition & Descriptions (with dynamically matching emojis).
  - Current Temperature, Feels Like, Minimum, and Maximum temperature values.
  - Atmospheric Humidity and Pressure.
  - Visibility range and Cloud Cover percentage.
  - Wind speed and Compass direction (N, NNE, NE, E, etc.).
  - Sunrise and Sunset timings converted to local time format.
- 🔄 **Dual Unit System**: Toggle between Metric (Celsius, m/s) and Imperial (Fahrenheit, mph) scales.
- 🛡️ **Network & API Guarding**: Handles lost connections, timeouts, incorrect API keys, and nonexistent locations.

---

## 📋 Prerequisites & Installation

### 1. Install Dependencies
This application requires the `requests` library to fetch API data. Install it via:
```bash
pip install -r requirements.txt
```

### 2. Configure OpenWeatherMap API Key
1. Go to [OpenWeatherMap](https://openweathermap.org/api) and register for a free account.
2. Generate a free API Key from your profile dashboard.
3. Open `VISHNU S_4.py` and set your key in the `API_KEY` configuration block:
   ```python
   API_KEY = "your_api_key_here"
   ```

---

## 🚀 Running the App

Run the application using:
```bash
python "VISHNU S_4.py"
```

---

## 💬 Sample Output

```text
  ╔══════════════════════════════════════════════════════╗
  ║         🌦️   WEATHER APP  —  VISHNU S   🌦️           ║
  ║              Oasis Infobyte Python Internship         ║
  ╚══════════════════════════════════════════════════════╝

  ┌────────────────────────────────────┐
  │  MAIN MENU                        │
  │  [1] Search by City Name          │
  │  [2] Search by ZIP / PIN Code     │
  │  [3] Exit                         │
  └────────────────────────────────────┘

  Enter option (1 / 2 / 3): 1

  Enter city name (e.g. Chennai, London): Chennai

  Select temperature unit:
  [1] Celsius  (metric)   — default
  [2] Fahrenheit (imperial)

  Your choice (press Enter for Celsius): 1

  ⏳ Fetching weather for 'Chennai' ...

  ╔══════════════════════════════════════════════════════╗
  ║            🌍  WEATHER FORECAST APP                  ║
  ║                   Created by VISHNU S                ║
  ╚══════════════════════════════════════════════════════╝

  📍  Location     :  Chennai, IN
  🕐  Fetched at   :  Sunday, 12 July 2026  |  10:04 AM

  ┌──────────────────────────────────────────────────────┐
  │                    CURRENT CONDITIONS                │
  ├──────────────────────────────────────────────────────┤
  │  ☁️  Condition   :  Clouds                               │
  │  🌡️  Temperature  :  31.2°C  (88.2°F)                     │
  │  🤔  Feels Like   :  34.5°C                               │
  │  🔼  Max Temp     :  31.2°C                               │
  │  🔽  Min Temp     :  31.2°C                               │
  ├──────────────────────────────────────────────────────┤
  │                  ATMOSPHERE & WIND                   │
  ├──────────────────────────────────────────────────────┤
  │  💧  Humidity     :  62%                                 │
  │  📊  Pressure     :  1008 hPa                             │
  │  👁️   Visibility   :  6.0 km                              │
  │  ☁️   Cloud Cover  :  75%                                 │
  │  💨  Wind         :  4.1 m/s  Direction: WSW              │
  ├──────────────────────────────────────────────────────┤
  │                    SUN TIMINGS                       │
  ├──────────────────────────────────────────────────────┤
  │  🌅  Sunrise      :  05:49 AM                            │
  │  🌇  Sunset       :  06:38 PM                            │
  └──────────────────────────────────────────────────────┘

  🔁 Check another location? (yes / no): no
```

---

## 📂 Folder Structure

```text
├── VISHNU S_Task4/
│   ├── VISHNU S_4.py       # Main Weather forecast application
│   ├── requirements.txt    # HTTP Request module (requests)
│   └── README.md           # Project documentation (this file)
```
