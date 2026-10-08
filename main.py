from flask import Flask, jsonify, request, redirect, url_for, session
from datetime import datetime
import requests
import random

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

# 64 hexagrams (very short descriptions — you can expand them)
ICHING_HEXAGRAMS = [
    {"id": 1, "name": "The Creative", "desc": "Pure strong force, initiative, powerful beginnings."},
    {"id": 2, "name": "The Receptive", "desc": "Yielding, support, patience, nurturing energy."},
    {"id": 3, "name": "Difficulty at the Beginning", "desc": "Chaos before order; perseverance brings clarity."},
    {"id": 4, "name": "Youthful Folly", "desc": "Learning, guidance, humility, correcting mistakes."},
    {"id": 5, "name": "Waiting", "desc": "Patience, preparation, trusting the process."},
    {"id": 6, "name": "Conflict", "desc": "Disputes, tension; seek resolution or withdraw."},
    {"id": 7, "name": "The Army", "desc": "Discipline, leadership, coordinated effort."},
    {"id": 8, "name": "Holding Together", "desc": "Unity, cooperation, shared purpose."},
    {"id": 9, "name": "Small Taming", "desc": "Gentle restraint, small gains, steady progress."},
    {"id": 10, "name": "Treading", "desc": "Caution, respect, careful movement forward."},
    {"id": 11, "name": "Peace", "desc": "Harmony, balance, prosperity, smooth progress."},
    {"id": 12, "name": "Stagnation", "desc": "Blockage, inactivity, pause before change."},
    {"id": 13, "name": "Fellowship", "desc": "Community, shared goals, collaboration."},
    {"id": 14, "name": "Great Possession", "desc": "Abundance, capability, responsible power."},
    {"id": 15, "name": "Modesty", "desc": "Humility, balance, grounded behaviour."},
    {"id": 16, "name": "Enthusiasm", "desc": "Motivation, inspiration, collective energy."},
    {"id": 17, "name": "Following", "desc": "Adaptation, alignment, moving with the flow."},
    {"id": 18, "name": "Work on the Decayed", "desc": "Repair, correction, confronting issues."},
    {"id": 19, "name": "Approach", "desc": "Opportunity, growth, positive movement."},
    {"id": 20, "name": "Contemplation", "desc": "Observation, reflection, gaining insight."},
    {"id": 21, "name": "Biting Through", "desc": "Resolving obstacles, decisive action."},
    {"id": 22, "name": "Grace", "desc": "Beauty, refinement, presentation matters."},
    {"id": 23, "name": "Splitting Apart", "desc": "Decline, breakdown, letting go."},
    {"id": 24, "name": "Return", "desc": "Cycles, renewal, coming back to centre."},
    {"id": 25, "name": "Innocence", "desc": "Naturalness, honesty, simple action."},
    {"id": 26, "name": "Great Taming", "desc": "Restraint, preparation, storing strength."},
    {"id": 27, "name": "Nourishment", "desc": "Self‑care, values, what sustains you."},
    {"id": 28, "name": "Great Exceeding", "desc": "Pressure, overload, pivotal moment."},
    {"id": 29, "name": "The Abyss", "desc": "Danger, repeated challenges, staying centred."},
    {"id": 30, "name": "The Clinging", "desc": "Clarity, illumination, dependence on something."},
    {"id": 31, "name": "Influence", "desc": "Gentle attraction, persuasion, emotional impact."},
    {"id": 32, "name": "Duration", "desc": "Consistency, endurance, long‑term stability."},
    {"id": 33, "name": "Retreat", "desc": "Strategic withdrawal, conserving strength."},
    {"id": 34, "name": "Great Power", "desc": "Force, confidence, responsible strength."},
    {"id": 35, "name": "Progress", "desc": "Advancement, recognition, rising influence."},
    {"id": 36, "name": "Darkening of the Light", "desc": "Adversity, concealment, protecting yourself."},
    {"id": 37, "name": "The Family", "desc": "Roles, structure, harmony in relationships."},
    {"id": 38, "name": "Opposition", "desc": "Differences, contrast, complementary forces."},
    {"id": 39, "name": "Obstruction", "desc": "Hardship, detours, seeking help."},
    {"id": 40, "name": "Deliverance", "desc": "Release, relief, solving problems."},
    {"id": 41, "name": "Decrease", "desc": "Simplification, sacrifice, focusing essentials."},
    {"id": 42, "name": "Increase", "desc": "Growth, generosity, expanding resources."},
    {"id": 43, "name": "Breakthrough", "desc": "Decisive clarity, confronting issues."},
    {"id": 44, "name": "Coming to Meet", "desc": "Sudden influence, temptation, caution."},
    {"id": 45, "name": "Gathering Together", "desc": "Assembly, unity, shared purpose."},
    {"id": 46, "name": "Pushing Upward", "desc": "Steady rise, effort rewarded."},
    {"id": 47, "name": "Oppression", "desc": "Exhaustion, limitation, inner strength needed."},
    {"id": 48, "name": "The Well", "desc": "Resources, renewal, tapping deeper support."},
    {"id": 49, "name": "Revolution", "desc": "Transformation, major change, new identity."},
    {"id": 50, "name": "The Cauldron", "desc": "Culture, nourishment, refining potential."},
    {"id": 51, "name": "The Arousing", "desc": "Shock, awakening, sudden events."},
    {"id": 52, "name": "Keeping Still", "desc": "Stillness, meditation, grounding."},
    {"id": 53, "name": "Gradual Progress", "desc": "Slow development, maturity, patience."},
    {"id": 54, "name": "The Marrying Maiden", "desc": "Compromise, secondary roles, adapting."},
    {"id": 55, "name": "Abundance", "desc": "Fullness, peak energy, clarity."},
    {"id": 56, "name": "The Wanderer", "desc": "Travel, transition, adapting to new places."},
    {"id": 57, "name": "The Gentle", "desc": "Subtle influence, penetration, steady shaping."},
    {"id": 58, "name": "The Joyous", "desc": "Pleasure, openness, communication."},
    {"id": 59, "name": "Dispersion", "desc": "Dissolving obstacles, unity through openness."},
    {"id": 60, "name": "Limitation", "desc": "Boundaries, discipline, clarity through restriction."},
    {"id": 61, "name": "Inner Truth", "desc": "Sincerity, intuition, authentic connection."},
    {"id": 62, "name": "Small Exceeding", "desc": "Attention to detail, caution, small steps."},
    {"id": 63, "name": "After Completion", "desc": "Order, finishing well, maintaining balance."},
    {"id": 64, "name": "Before Completion", "desc": "Transition, near‑completion, careful final steps."}
]

import random

#================== 3 COIN RANDOM TOSS ================================
def toss_three_coins():
    # Heads = 3, Tails = 2
    return sum(random.choice([2, 3]) for _ in range(3))

#================== ICHING LINE TYPE (DISPLAY TEXT) ===================
def line_type(total):
    if total == 6:
        return "⚋ (old yin)"
    elif total == 7:
        return "⚊ (young yang)"
    elif total == 8:
        return "⚋ (young yin)"
    elif total == 9:
        return "⚊ (old yang)"

#================== ENCODE LINE (QUERYSTRING → BINARY) ================
def encode_line(line):
    if line in ("old-yin", "young-yin"):
        return 0
    if line in ("young-yang", "old-yang"):
        return 1

#================== TRANSFORM LINES → HEXAGRAM ========================
def transform_lines_to_hexagram(request):
    lines = []
    for i in range(1, 7):
        val = request.args.get(f"line{i}")
        if val:
            lines.append(val)

    if len(lines) < 6:
        return {"complete": False, "lines": lines}

    bits = [encode_line(l) for l in lines]
    index = int("".join(str(b) for b in bits), 2) % 64
    hexagram = ICHING_HEXAGRAMS[index]

    return {
        "complete": True,
        "lines": lines,
        "binary": bits,
        "hexagram_number": hexagram["id"],
        "hexagram_name": hexagram["name"],
        "hexagram_desc": hexagram["desc"]
    }

#================== TOSS → QUERYSTRING LINE ===========================
def toss_to_querystring(request):
    lines = []
    for i in range(1, 7):
        val = request.args.get(f"line{i}")
        if val:
            lines.append(val)

    if len(lines) >= 6:
        return None

    toss = toss_three_coins()
    if toss == 6:
        new_line = "old-yin"
    elif toss == 7:
        new_line = "young-yang"
    elif toss == 8:
        new_line = "young-yin"
    elif toss == 9:
        new_line = "old-yang"

    qs = "&".join([f"line{i+1}={lines[i]}" for i in range(len(lines))])
    qs += f"&line{len(lines)+1}={new_line}"
    return qs

#================== HTML LINE RENDERER (FIXED WIDTH BARS + LABELS TO RIGHT + NUMBERS LEFT) ===================
def render_html_lines(display_lines):
    html = ""
    # enumerate gives us the throw order (1–6)
    for idx, l in enumerate(display_lines, start=1):
        if "yin" in l:
            # Broken line (two halves with a gap)
            html += f"""
            <div style="display:flex; align-items:center; margin:8px auto; width:360px;">
                <!-- Throw number -->
                <div style="width:30px; text-align:right; margin-right:8px; font-size:0.9rem; color:#333;">{idx}</div>
                <!-- Line bar -->
                <div style="display:flex; justify-content:space-between; width:200px;">
                    <div style="width:90px; height:20px; background:#000;"></div>
                    <div style="width:20px;"></div>
                    <div style="width:90px; height:20px; background:#000;"></div>
                </div>
                <!-- Label -->
                <div style="margin-left:12px; font-size:0.9rem; color:#333;">{l}</div>
            </div>
            """
        else:
            # Solid line
            html += f"""
            <div style="display:flex; align-items:center; margin:8px auto; width:360px;">
                <!-- Throw number -->
                <div style="width:30px; text-align:right; margin-right:8px; font-size:0.9rem; color:#333;">{idx}</div>
                <!-- Line bar -->
                <div style="width:200px; height:20px; background:#000;"></div>
                <!-- Label -->
                <div style="margin-left:12px; font-size:0.9rem; color:#333;">{l}</div>
            </div>
            """
    return html

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

            <div class="card shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">I Ching Hexagram Generator</h5>
                    <p>
                        Use the traditional three‑coin method to generate a six‑line hexagram.
                        Each throw builds the pattern, and the final result is matched to one of the
                        64 classical I Ching interpretations.
                    </p>

                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">
                            <a href="/pyching">/pyching</a> — Interactive coin‑toss generator
                        </li>
                        <li class="list-group-item">
                            Generates 3‑coin throws × 6 lines
                        </li>
                        <li class="list-group-item">
                            Displays the resulting hexagram and its meaning
                        </li>
                        <li class="list-group-item">
                            Includes a reset button to start again
                        </li>
                    </ul>
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

#==================STATUS ICHING =======================================
@app.route("/pyching")
def pyching():
    lines = []
    for i in range(1, 7):
        val = request.args.get(f"line{i}")
        if val:
            lines.append(val)

    if request.args.get("throw") == "1" and len(lines) < 6:
        qs = toss_to_querystring(request)
        if qs:
            return redirect(f"/pyching?{qs}")

    display_lines = list(reversed(lines))
    html_lines = render_html_lines(display_lines)

    result = transform_lines_to_hexagram(request)

    hex_html = ""
    if result["complete"]:
        hex_html = f"""
        <div class="card shadow-sm mb-4">
            <div class="card-body">
                <h5 class="card-title">
                    Hexagram: {result['hexagram_number']}. {result['hexagram_name']}
                </h5>
                <p>{result['hexagram_desc']}</p>
            </div>
        </div>
        """

    throw_button = ""
    if not result["complete"]:
        qs = "&".join([f"line{i+1}={lines[i]}" for i in range(len(lines))])
        throw_button = f"""
        <a class='btn btn-primary btn-lg'
           href='/pyching?throw=1&{qs}'>
           Throw Coins
        </a>
        """

    return f"""
    <html>
    <head>
        <link rel="stylesheet"
              href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
    </head>
    <body class="container py-4">
        <h1 class="mb-4">I Ching – Three Coin Method</h1>
        {html_lines}
        {hex_html}
        {throw_button}
        <a class="btn btn-secondary mt-3" href="/pyching_reset">Reset</a>
    </body>
    </html>
    """

#======================== pyching reset ================================
@app.route("/pyching_reset")
def pyching_reset():
    session["lines"] = []
    return redirect(url_for("pyching"))

#======================== web ================================
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
