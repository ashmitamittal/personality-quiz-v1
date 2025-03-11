from flask import Flask, request, jsonify, session
import numpy as np
import pandas as pd
import joblib
import json
import traceback
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Needed for session storage
CORS(app)  # Enable CORS for frontend interaction

# Load trained ML model once
try:
    model = joblib.load("personality_model.pkl")
except FileNotFoundError:
    model = None
    print("⚠️ Warning: ML Model not found!")

# Load questions from JSON file
def load_questions():
    with open("questions.json", "r", encoding="utf-8") as file:
        return json.load(file)

questions = load_questions()

# Define archetypes list
archetypes = [
    "Trailblazer 🔥", "Precision Architect 🏗️", "Fearless Gambler 🎲",
    "Strategic Guardian 🛡️", "Diplomatic Orchestrator 🎭",
    "Instinctive Maverick ⚡", "Perfectionist Engineer 🛠️",
    "Pragmatic Solver 🔍", "Rebel Thinker 🧩", "Ethical Compass ⚖️"
]

# Define expected feature columns
feature_columns = [
    "Openness", "Conscientiousness", "Extraversion", "Agreeableness", 
    "Neuroticism", "MBTI_Introvert", "MBTI_Thinking", "DISC_Dominance",
    "DISC_Influence", "DISC_Steadiness", "Hogan_Ambition", 
    "Bias_Overconfidence", "Bias_Confirmation"
]

@app.route("/get_question/<int:index>", methods=["GET"])
def get_question(index):
    """Returns the next question from the JSON file."""
    if index < len(questions):
        return jsonify(questions[index])
    return jsonify({"message": "Quiz complete!"})

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    """Processes user answer, updates scores, and predicts personality."""
    try:
        data = request.json

        # ✅ Ensure request has required keys
        if "question_index" not in data or "chosen_option" not in data:
            return jsonify({"error": "Missing 'question_index' or 'chosen_option'"}), 400

        q_index = data["question_index"]
        choice = data["chosen_option"]

        # ✅ Validate question index
        if q_index >= len(questions):
            return jsonify({"error": "Invalid question index"}), 400

        # ✅ Validate choice
        if choice not in questions[q_index]["options"]:
            return jsonify({"error": "Invalid answer choice"}), 400

        # ✅ Initialize user session scores if not already present
        if "user_scores" not in session:
            session["user_scores"] = {trait: 0 for trait in feature_columns}

        user_scores = session["user_scores"]

        # ✅ Update user scores
        for trait, value in questions[q_index]["options"][choice]["traits"].items():
            if trait in user_scores:
                user_scores[trait] += value

        # ✅ Save updated user scores to session
        session["user_scores"] = user_scores

        # ✅ Ensure ML model is available
        if model is None:
            return jsonify({"error": "ML Model not available"}), 500

        # ✅ Prepare input vector
        input_vector = np.array([[user_scores.get(trait, 0) for trait in feature_columns]])

        # ✅ Validate input shape
        if input_vector.shape[1] != len(feature_columns):
            return jsonify({"error": f"Model input shape mismatch: expected {len(feature_columns)}, got {input_vector.shape[1]}"}), 500

        # ✅ Get model probabilities
        probs = model.predict_proba(input_vector)[0]

        # ✅ Get top 3 personality archetypes
        top_indices = np.argsort(probs)[-3:]  
        top_archetypes = {archetypes[i]: round(probs[i] * 100, 2) for i in reversed(top_indices)}

        return jsonify({"top_archetypes": top_archetypes, "updated_scores": user_scores})

    except Exception as e:
        print("\n🔥 ERROR TRACEBACK 🔥\n")
        traceback.print_exc()
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
