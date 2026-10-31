import pandas as pd
from scipy.io import arff
from sklearn.preprocessing import LabelEncoder


# Load ARFF and decode byte strings
def load_and_preprocess_arff(filepath):
    data, meta = arff.loadarff(filepath)
    df = pd.DataFrame(data)
    df = df.map(lambda x: x.decode() if isinstance(x, bytes) else x)
    return df


# Encode categorical features and the label column
def encode_features(df, label_col='xAttack'):
    label_encoders = {}
    for col in df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    return df, label_encoders


# Save DataFrame to CSV
def save_to_csv(df, output_path):
    df.to_csv(output_path, index=False)
    print(f"Saved preprocessed data to {output_path}")


if __name__ == "__main__":
    input_path = "data/full-d/KDDTrain+Multi.arff"
    output_path = "data/KDDTrain+Multi.csv"
    df = load_and_preprocess_arff(input_path)
    df, encoders = encode_features(df)
    save_to_csv(df, output_path)
