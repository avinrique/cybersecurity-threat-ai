from flask import Flask, request, jsonify, render_template
import joblib
import os
import pandas as pd

from nsl_kdd import load_connections

app = Flask(__name__)

# Load the trained model
model = joblib.load("models/threat_detector.pkl")

# Get the exact feature order used during training
FEATURE_COLUMNS = list(model.feature_names_in_)

# The text values the model knows for protocol_type, service and flag
encoder = model[0].named_transformers_["ordinalencoder"]
TEXT_VALUES = {col: values.tolist() for col, values in zip(encoder.feature_names_in_, encoder.categories_)}

# Real connections from the NSL-KDD test set (never seen in training), used by the web page
SAMPLES = load_connections("data/KDDTest+.txt")


# Reject text the model has never seen, e.g. a misspelled service
def check_text(column, value):
    if value not in TEXT_VALUES[column]:
        raise ValueError(f"Unknown {column} '{value}'")
    return value


@app.route('/')
def home():
    return render_template("index.html", text_values=TEXT_VALUES, features=FEATURE_COLUMNS)


@app.route('/sample')
def sample():
    attack_type = request.args.get("type", "any")
    pool = SAMPLES if attack_type == "any" else SAMPLES[SAMPLES["attack_type"] == attack_type]
    row = pool.sample(1).to_dict(orient="records")[0]
    return jsonify({
        "connection": {col: row[col] for col in FEATURE_COLUMNS},
        "attack": row["attack"],
        "attack_type": row["attack_type"],
    })


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input JSON data from the POST request
        input_data = request.get_json()

        # Convert to DataFrame
        input_df = pd.DataFrame([input_data]) if isinstance(input_data, dict) else pd.DataFrame(input_data)

        # Reorder columns to match training data
        input_df = input_df[FEATURE_COLUMNS]
        input_df.columns.name = None  # Clear index name if it exists

        # protocol_type, service and flag are sent as text, e.g. "tcp", "http", "SF"
        for col in TEXT_VALUES:
            input_df[col] = input_df[col].map(lambda value: check_text(col, value))

        # Make prediction and get probabilities
        prediction = model.predict(input_df)
        probabilities = model.predict_proba(input_df)

        # Return prediction, confidence and the share of trees voting for each class
        return jsonify({
            "prediction": prediction.tolist(),
            "confidence": probabilities.max(axis=1).tolist(),
            "probabilities": [dict(zip(model.classes_.tolist(), p)) for p in probabilities.tolist()],
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run the Flask app (macOS uses port 5000 for AirPlay, so it can be changed with PORT)
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
