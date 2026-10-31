from sklearn.compose import make_column_transformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OrdinalEncoder
import joblib

from nsl_kdd import FEATURES, TEXT_FEATURES, load_connections

# Load the raw NSL-KDD training and test connections
train = load_connections("data/KDDTrain+.txt")
test = load_connections("data/KDDTest+.txt")

# Turn protocol_type, service and flag text into category ids (unknown text -> missing)
encoder = make_column_transformer(
    (OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), TEXT_FEATURES),
    remainder="passthrough",
    verbose_feature_names_out=False,
).set_output(transform="pandas")

# Gradient boosting with shallow trees: generalizes better to attack types not seen in
# training, and balanced class weights stop the rare r2l/u2r attacks being ignored
classifier = HistGradientBoostingClassifier(
    max_depth=3,
    l2_regularization=1.0,
    class_weight="balanced",
    categorical_features=TEXT_FEATURES,
    random_state=42,
)

# Train on all training connections
model = make_pipeline(encoder, classifier)
model.fit(train[FEATURES], train["attack_type"])
print(f"Accuracy on KDDTest+ (connections never seen in training): {model.score(test[FEATURES], test['attack_type']):.2%}")

# Save model
joblib.dump(model, "models/threat_detector.pkl")
print("Model saved to models/threat_detector.pkl")
