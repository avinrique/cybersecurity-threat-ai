import joblib

from nsl_kdd import FEATURES, load_connections

# Load model
model = joblib.load("models/threat_detector.pkl")

# Load test data (or any new data)
df = load_connections("data/KDDTest+.txt")

# Separate features
X = df[FEATURES]

# Make prediction
predictions = model.predict(X)
confidences = model.predict_proba(X).max(axis=1)

# Preview predictions
for i in range(5):
    print(f"Prediction: {predictions[i]}, Confidence: {confidences[i]:.2f}, Actual: {df['attack_type'][i]}")
print(f"Accuracy on all {len(df):,} connections: {(predictions == df['attack_type']).mean():.2%}")
