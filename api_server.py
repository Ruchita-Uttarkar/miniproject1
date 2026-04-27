"""
Flask REST API for the Ayurvedic Formulation Recommender.
Exposes a single endpoint: POST /recommend
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from ayurveda_recommender import load_and_preprocess, AyurvedaRecommender
from dosha import load_dosha_model

app = Flask(__name__)
CORS(app)   # Allow cross-origin requests from the React UI

CSV_PATH = os.environ.get("CSV_PATH", "herbal_formulation.csv")

# Warm up the model at startup
print("Warming up the recommender …")
_df  = load_and_preprocess(CSV_PATH)
_rec = AyurvedaRecommender(_df)
print("Recommender ready ✓")


@app.route("/recommend", methods=["POST"])
def recommend():
    """
    POST /recommend
    Body: { "query": "bloating nausea stomach pain", "top_n": 5 }
    Returns: { "results": [ { ...formulation fields... } ] }
    """
    body  = request.get_json(silent=True) or {}
    query = body.get("query", "").strip()
    top_n = int(body.get("top_n", 5))

    if not query:
        return jsonify({"error": "query field is required"}), 400

    results = _rec.recommend_formulations(query, top_n=top_n)
    return jsonify({"results": results})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "total_formulations": len(_df)})

@app.route("/dashboard", methods=["GET"])
def dashboard():
    return jsonify({
        "modules": [
            {
                "name": "Ayurveda Recommendation",
                "description": "Get formulations based on symptoms",
                "endpoint": "/recommend",
                "method": "POST"
            },
            {
                "name": "Dosha Detector",
                "description": "Find your body type (Vata, Pitta, Kapha)",
                "endpoint": "/dosha",
                "method": "POST"
            },
            {
                "name": "Diet Planner",
                "description": "Personalized diet based on dosha",
                "endpoint": "/diet",
                "method": "POST"
            }
        ]
    })
    

dosha_model, reverse_mapping = load_dosha_model()

@app.route("/dosha", methods=["POST"])
def dosha():
    data = request.json

    try:
        body_map = {"Thin": 0, "Medium": 1, "Heavy": 2}
        skin_map = {"Dry": 0, "Normal": 1, "Oily": 2}
        digestion_map = {"Irregular": 0, "Strong": 1, "Slow": 2}
        sleep_map = {"Light": 0, "Moderate": 1, "Heavy": 2}

        user_input = [
            body_map[data["body"]],
            skin_map[data["skin"]],
            digestion_map[data["digestion"]],
            sleep_map[data["sleep"]]
        ]

        prediction = dosha_model.predict([user_input])[0]
        result = reverse_mapping[prediction]

        return jsonify({"dominant_dosha": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 400
        
@app.route("/diet", methods=["POST"])
def diet():
    return jsonify({
        "eat": ["warm food", "ghee", "rice"],
        "avoid": ["cold food", "dry snacks"]
    })


if __name__ == "__main__":
    app.run(port=5050, debug=False)
