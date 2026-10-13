from flask import Blueprint, jsonify, request, redirect, url_for, session, render_template
import random

#================== I CHING BLUEPRINT ==================================
# All I Ching pages live here, registered onto the app in main.py
#   /pyching       — original version (Copilot)
#   /claude-iching — interactive version (Claude)
iching = Blueprint("iching", __name__)

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

#================== COIN TOTAL → LINE NAME ============================
LINE_NAMES = {6: "old-yin", 7: "young-yang", 8: "young-yin", 9: "old-yang"}

#================== TRIGRAMS ==========================================
# Key = trigram lines read bottom → top (1 = yang/solid, 0 = yin/broken)
TRIGRAMS = {
    "111": {"name": "Qian", "symbol": "☰", "image": "Heaven"},
    "110": {"name": "Dui", "symbol": "☱", "image": "Lake"},
    "101": {"name": "Li", "symbol": "☲", "image": "Fire"},
    "100": {"name": "Zhen", "symbol": "☳", "image": "Thunder"},
    "011": {"name": "Xun", "symbol": "☴", "image": "Wind"},
    "010": {"name": "Kan", "symbol": "☵", "image": "Water"},
    "001": {"name": "Gen", "symbol": "☶", "image": "Mountain"},
    "000": {"name": "Kun", "symbol": "☷", "image": "Earth"},
}

# (upper, lower) trigram for each hexagram, in King Wen order 1–64
KING_WEN_TRIGRAMS = [
    ("Qian", "Qian"), ("Kun", "Kun"), ("Kan", "Zhen"), ("Gen", "Kan"),
    ("Kan", "Qian"), ("Qian", "Kan"), ("Kun", "Kan"), ("Kan", "Kun"),
    ("Xun", "Qian"), ("Qian", "Dui"), ("Kun", "Qian"), ("Qian", "Kun"),
    ("Qian", "Li"), ("Li", "Qian"), ("Kun", "Gen"), ("Zhen", "Kun"),
    ("Dui", "Zhen"), ("Gen", "Xun"), ("Kun", "Dui"), ("Xun", "Kun"),
    ("Li", "Zhen"), ("Gen", "Li"), ("Gen", "Kun"), ("Kun", "Zhen"),
    ("Qian", "Zhen"), ("Gen", "Qian"), ("Gen", "Zhen"), ("Dui", "Xun"),
    ("Kan", "Kan"), ("Li", "Li"), ("Dui", "Gen"), ("Zhen", "Xun"),
    ("Qian", "Gen"), ("Zhen", "Qian"), ("Li", "Kun"), ("Kun", "Li"),
    ("Xun", "Li"), ("Li", "Dui"), ("Kan", "Gen"), ("Zhen", "Kan"),
    ("Gen", "Dui"), ("Xun", "Zhen"), ("Dui", "Qian"), ("Qian", "Xun"),
    ("Dui", "Kun"), ("Kun", "Xun"), ("Dui", "Kan"), ("Kan", "Xun"),
    ("Dui", "Li"), ("Li", "Xun"), ("Zhen", "Zhen"), ("Gen", "Gen"),
    ("Xun", "Gen"), ("Zhen", "Dui"), ("Zhen", "Li"), ("Li", "Gen"),
    ("Xun", "Xun"), ("Dui", "Dui"), ("Xun", "Kan"), ("Kan", "Dui"),
    ("Xun", "Dui"), ("Zhen", "Gen"), ("Kan", "Li"), ("Li", "Kan"),
]
HEXAGRAM_BY_TRIGRAMS = {pair: number for number, pair in enumerate(KING_WEN_TRIGRAMS, start=1)}

#================== 3 COIN RANDOM TOSS ================================
def toss_coin_faces():
    return [random.choice(["H", "T"]) for _ in range(3)]

def coins_total(faces):
    # Heads = 3, Tails = 2
    return sum(3 if face == "H" else 2 for face in faces)

def toss_three_coins():
    return coins_total(toss_coin_faces())

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

#================== CHANGING LINE (OLD → OPPOSITE) ====================
def changed_line(line):
    return {"old-yin": "young-yang", "old-yang": "young-yin"}.get(line, line)

#================== BINARY (BOTTOM → TOP) → HEXAGRAM ==================
def lookup_hexagram(bits):
    lower = TRIGRAMS["".join(str(b) for b in bits[:3])]
    upper = TRIGRAMS["".join(str(b) for b in bits[3:])]
    number = HEXAGRAM_BY_TRIGRAMS[(upper["name"], lower["name"])]
    hexagram = ICHING_HEXAGRAMS[number - 1]
    return {
        "number": number,
        "name": hexagram["name"],
        "desc": hexagram["desc"],
        "symbol": chr(0x4DC0 + number - 1),  # Unicode hexagram block ䷀..䷿
        "binary": bits,
        "upper": upper,
        "lower": lower,
    }

#================== TRANSFORM LINES → HEXAGRAM (COPILOT) ==============
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

    new_line = LINE_NAMES[toss_three_coins()]

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

#================== ICHING (COPILOT) ===================================
@iching.route("/pyching")
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
@iching.route("/pyching_reset")
def pyching_reset():
    session["lines"] = []
    return redirect(url_for("iching.pyching"))

#================== ICHING (CLAUDE) PAGE ===============================
@iching.route("/claude-iching")
def claude_iching():
    return render_template("claude_iching.html")

#================== ICHING (CLAUDE) THROW ONE LINE (JSON) ==============
@iching.route("/claude-iching/throw")
def claude_iching_throw():
    faces = toss_coin_faces()
    total = coins_total(faces)
    return jsonify({
        "coins": faces,
        "total": total,
        "line": LINE_NAMES[total],
        "label": line_type(total)
    })

#================== ICHING (CLAUDE) READING FOR 6 LINES (JSON) =========
# e.g. /claude-iching/reading?line1=young-yang&line2=old-yin&...&line6=young-yin
# line1 is the bottom line (first throw), line6 the top
@iching.route("/claude-iching/reading")
def claude_iching_reading():
    lines = [request.args.get(f"line{i}") for i in range(1, 7)]
    if not all(l in LINE_NAMES.values() for l in lines):
        return jsonify({"error": "Need line1..line6, each one of: " + ", ".join(LINE_NAMES.values())}), 400

    changing = [i for i, l in enumerate(lines, start=1) if l.startswith("old-")]
    primary = lookup_hexagram([encode_line(l) for l in lines])
    relating = lookup_hexagram([encode_line(changed_line(l)) for l in lines]) if changing else None

    return jsonify({
        "lines": lines,
        "changing_lines": changing,
        "primary": primary,
        "relating": relating
    })
