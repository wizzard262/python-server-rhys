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
    return """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Python Flask on Cloud Run</title>
        <link rel="stylesheet"
              href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
        <style>
            body {
                background: #f8f9fa;
            }
            .hero {
                padding: 3rem 1rem;
                background: #0d6efd;
                color: white;
                border-radius: .5rem;
                margin-bottom: 2rem;
            }
            .card {
                margin-bottom: 1.5rem;
            }
        </style>
    </head>

    <body class="container py-4">

        <div class="hero text-center">
            <h1 class="display-5 fw-bold">Flask Web Server on Google Cloud Run</h1>
            <p class="lead">
                This service is deployed using Cloud Run and built automatically from GitHub.
            </p>
        </div>

        <div class="row">
            <div class="col-md-6">
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">Useful Links</h5>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item">
                                <a href="https://github.com/wizzard262/python-server-rhys" target="_blank">
                                    GitHub Repository
                                </a>
                            </li>
                            <li class="list-group-item">
                                <a href="https://github.com/wizzard262/python-server-rhys/blob/main/README.md"
                                   target="_blank">
                                    GitHub README (Setup)
                                </a>
                            </li>
                            <li class="list-group-item">
                                <a href="https://console.cloud.google.com/run/detail/europe-west1/python-server-rhys-git/revisions?project=my-project-1491071384075"
                                   target="_blank">
                                    Cloud Run Console (Service)
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>

                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">API Endpoints</h5>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item">
                                <a href="/">/</a> — Homepage
                            </li>
                            <li class="list-group-item">
                                <a href="/status">/status</a> — JSON status
                            </li>
                            <li class="list-group-item">
                                <a href="/weather?lat=53.24&lon=2.09">
                                    /weather?lat=53.24&lon=2.09
                                </a>
                                — Weather (Stockport, UK)
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="col-md-6">
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">About This Service</h5>
                        <p>
                            This Flask application exposes a simple homepage, a status endpoint,
                            and a weather endpoint powered by the Open‑Meteo API.
                        </p>
                        <p>
                            The service is built using Google Cloud Build and deployed automatically
                            to Cloud Run on every push to the <strong>main</strong> branch.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
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
