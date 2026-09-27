from flask import Flask, jsonify, request
from datetime import datetime
import requests

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

#==================HOMEPAGE=======================================
@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Google Cloud Run service running a Flask Python web server</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
        </head>
        <body>
            <h1>Cloud Run service running a Flask Python web server</h1>

            <p>
                &nbsp;&nbsp;This homepage page is served from the Python web server.<br/>
                &nbsp;&nbsp;It also has a path to see current status: "/status"<br/>
                &nbsp;&nbsp;It also has a path to get weather: "/weather"
            </p>

            <ul>
                <li>Github Repo:
                    <a href="https://github.com/wizzard262/python-server-rhys">
                        https://github.com/wizzard262/python-server-rhys
                    </a>
                </li>

                <li>Github Repo README (setup):
                    <a href="https://github.com/wizzard262/python-server-rhys/blob/main/README.md">
                        https://github.com/wizzard262/python-server-rhys/blob/main/README.md
                    </a>
                </li>

                <li>Console Service URL:
                    <a href="https://console.cloud.google.com/run/detail/europe-west1/python-server-rhys/observability/metrics?project=my-project-1491071384075">
                        https://console.cloud.google.com/run/detail/europe-west1/python-server-rhys/observability/metrics?project=my-project-1491071384075
                    </a>
                </li>
            </ul>

            <h3>PATHS:</h3>
            <ul>
                <li><a href="/">/</a> – (this HTML page)</li>
                <li><a href="/status">/status</a> – JSON status endpoint</li>
                <li>
                    <a href="/weather?lat=53.24&lon=2.09">
                        /weather?lat=53.24&lon=2.09
                    </a>
                    – JSON weather endpoint (Stockport, UK)<br/>
                    (calls Open Meteo API:
                    https://api.open-meteo.com/v1/forecast?current_weather=true&latitude=53.24&longitude=2.09)
                </li>
            </ul>
        </body>
    </html>
    """

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

    # Call the API
    response = requests.get(url)
    data = response.json()

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
