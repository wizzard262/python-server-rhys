from flask import Flask, jsonify, request, render_template
from datetime import datetime
import requests
from iching import iching

#==================weather codes=======================================
app = Flask(__name__)
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

app.secret_key = "your_secret_key_here"  # Replace with a secure random key in production

app.register_blueprint(iching)

#==================HOMEPAGE=======================================
@app.route("/")
def home():
    # The page is templates/index.html; its stylesheet is static/site.css
    return render_template("index.html")

#==================STATUS ENDPOINT=======================================
@app.route("/status")
def status():
    return jsonify({
        "status": "ok",
        "time": datetime.utcnow().isoformat() + "Z"
    })
#======================== web ================================
@app.route("/weather")
def weather():
    # Read lat/lon from query parameters
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Missing lat or lon"}), 400

    # Build Open-Meteo API URL
    url = (
        "https://api.open-meteo.com/v1/forecast"
        + "?latitude=" + str(lat)
        + "&longitude=" + str(lon)
        + "&current_weather=true"
    )

    # Call the API (give up after 10 seconds rather than hang the request)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return jsonify({"error": "Weather service unavailable", "detail": str(e)}), 502

    # Extract only the current weather section
    current = data.get("current_weather")

    if not current:
        return jsonify({"error": "No current weather available"}), 404

    # Add human-readable weather description
    weather_code = current.get("weathercode")
    if weather_code is not None:
        current["weather_description"] = WEATHER_CODES.get(weather_code, "Unknown")

    return jsonify(current)

#======================== web ================================
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
