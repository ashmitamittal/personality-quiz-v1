import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Define 10 archetypes
archetypes = [
    "Trailblazer 🔥", "Precision Architect 🏗️", "Fearless Gambler 🎲", 
    "Strategic Guardian 🛡️", "Diplomatic Orchestrator 🎭", "Instinctive Maverick ⚡",
    "Perfectionist Engineer 🛠️", "Pragmatic Solver 🔍", "Rebel Thinker 🧩", "Ethical Compass ⚖️"
]

# Create a dataset (each row is a simulated user)
data = {
    "Openness": [9, 3, 8, 2, 6, 9, 4, 5, 8, 7],  # Big Five Openness Score
    "Conscientiousness": [4, 10, 3, 9, 6, 4, 10, 6, 5, 7],  # Big Five Conscientiousness
    "Extraversion": [10, 2, 9, 3, 8, 9, 4, 5, 8, 6],  # Big Five Extraversion
    "Agreeableness": [5, 4, 6, 8, 10, 7, 3, 6, 9, 10],  # Big Five Agreeableness
    "Neuroticism": [3, 8, 2, 7, 5, 6, 2, 4, 7, 3],  # Big Five Neuroticism
    "MBTI_Introvert": [0, 1, 0, 1, 0, 0, 1, 0, 0, 1],  # MBTI (1 = Introvert, 0 = Extrovert)
    "MBTI_Thinking": [1, 1, 0, 1, 0, 0, 1, 1, 0, 1],  # MBTI (1 = Thinking, 0 = Feeling)
    "DISC_Dominance": [9, 3, 8, 4, 6, 9, 4, 5, 8, 6],  # DISC Dominance
    "DISC_Influence": [8, 2, 10, 3, 9, 7, 3, 6, 9, 8],  # DISC Influence
    "DISC_Steadiness": [3, 7, 2, 9, 6, 4, 10, 6, 5, 7],  # DISC Steadiness
    "Hogan_Ambition": [10, 6, 9, 4, 8, 9, 3, 5, 7, 6],  # Hogan Ambition
    "Bias_Overconfidence": [8, 2, 9, 3, 5, 9, 4, 5, 8, 7],  # Bias Overconfidence
    "Bias_Confirmation": [4, 9, 3, 8, 6, 5, 10, 6, 5, 7],  # Bias Confirmation Bias
    "Archetype": archetypes  # Personality labels
}

# Convert dataset to DataFrame
df = pd.DataFrame(data)

# Convert archetypes into numbers for training
archetype_map = {archetype: i for i, archetype in enumerate(archetypes)}
df["Archetype"] = df["Archetype"].map(archetype_map)

# Split data into features (X) and labels (y)
X = df.drop(columns=["Archetype"])
y = df["Archetype"]

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save trained model
joblib.dump(model, "personality_model.pkl")

print("✅ Model training complete & saved as 'personality_model.pkl'")

# # Simulated new user response (Alex)
# new_user = np.array([[8, 6, 7, 9, 3, 10]])  # Alex's responses

# probs = model.predict_proba(new_user)[0]

# # Get top 2 archetypes with highest probabilities
# top_indices = np.argsort(probs)[-2:]  # Get indices of top 2
# top_archetypes = [archetypes[i] for i in reversed(top_indices)]  # Convert indices back to archetypes

# print(f"Predicted Personality Archetypes: {top_archetypes[0]} + {top_archetypes[1]}")
