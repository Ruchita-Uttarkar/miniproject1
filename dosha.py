import pandas as pd
from sklearn.tree import DecisionTreeClassifier

def load_dosha_model():
    # Load dataset
    dosha_df = pd.read_csv("C:/Users/user/Desktop/Python Mini Project/backend/dosha_dataset.csv")

    # Encoding
    dosha_df["Body_Type"] = dosha_df["Body_Type"].map({
        "Thin": 0, "Medium": 1, "Heavy": 2
    })

    dosha_df["Skin"] = dosha_df["Skin"].map({
        "Dry": 0, "Normal": 1, "Oily": 2
    })

    dosha_df["Digestion"] = dosha_df["Digestion"].map({
        "Irregular": 0, "Strong": 1, "Slow": 2
    })

    dosha_df["Sleep"] = dosha_df["Sleep"].map({
        "Light": 0, "Moderate": 1, "Heavy": 2
    })

    dosha_df["Dosha"] = dosha_df["Dosha"].map({
        "Vata": 0, "Pitta": 1, "Kapha": 2
    })

    # Clean data
    dosha_df = dosha_df.dropna()

    X = dosha_df[["Body_Type", "Skin", "Digestion", "Sleep"]].astype(int)
    y = dosha_df["Dosha"].astype(int)

    # Train model
    model = DecisionTreeClassifier()
    model.fit(X, y)

    reverse_mapping = {0: "Vata", 1: "Pitta", 2: "Kapha"}

    return model, reverse_mapping