import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator
import pickle
import os
import base64

def load_data():
    """
    Loads data from a CSV file, serializes it, and returns the serialized data.
    Returns:
        str: Base64-encoded serialized data (JSON-safe).
    """
    print("We are here")
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/file.csv"))
    serialized_data = pickle.dumps(df)                    # bytes
    return base64.b64encode(serialized_data).decode("ascii")  # JSON-safe string

def data_preprocessing(data_b64: str):
    """
    Deserializes base64-encoded pickled data, performs preprocessing,
    and returns base64-encoded pickled clustered data.
    """
    # decode -> bytes -> DataFrame
    data_bytes = base64.b64decode(data_b64)
    df = pickle.loads(data_bytes)

    df = df.dropna()
    clustering_data = df[["BALANCE", "PURCHASES", "CREDIT_LIMIT"]]
    clustering_data['PURCHASES_TO_LIMIT_RATIO'] = (
        clustering_data['PURCHASES'] / (clustering_data['CREDIT_LIMIT'] + 1)
    )
    clustering_data['BALANCE_TO_LIMIT_RATIO'] = (
        clustering_data['BALANCE'] / (clustering_data['CREDIT_LIMIT'] + 1)
    )

    Q1 = clustering_data.quantile(0.25)
    Q3 = clustering_data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    mask = ~((clustering_data < lower_bound) | (clustering_data > upper_bound)).any(axis=1)
    clustering_data = clustering_data[mask]
    
    # Use RobustScaler instead of MinMaxScaler (more resistant to outliers)
    robust_scaler = RobustScaler()
    clustering_data_scaled = robust_scaler.fit_transform(clustering_data)
    # Make sure it's a 2D array
    if clustering_data_scaled.ndim == 1:
        clustering_data_scaled = clustering_data_scaled.reshape(-1, 1)
    # Serialize as a tuple: (scaled_data, scaler, feature_names)
    result = (clustering_data_scaled, robust_scaler, clustering_data.columns.tolist())
    
    # bytes -> base64 string for XCom
    clustering_serialized_data = pickle.dumps(result)
    return base64.b64encode(clustering_serialized_data).decode("ascii")


def build_save_model(data_b64: str, filename: str):
    """
    Builds a DBSCAN model on the preprocessed data and saves it.
    Returns metrics for evaluation.
    """
    # decode -> bytes -> tuple
    data_bytes = base64.b64decode(data_b64)
    result = pickle.loads(data_bytes)
    
    # Unpack the tuple
    df = result[0]
    scaler = result[1]
    feature_names = result[2]
    
    # Try different epsilon values to find optimal clustering
    eps_range = np.linspace(0.3, 2.0, 20)
    silhouette_scores = []
    n_clusters_list = []
    
    best_score = -1
    best_model = None
    best_eps = None
    
    for eps in eps_range:
        dbscan = DBSCAN(eps=eps, min_samples=5, metric='euclidean')
        labels = dbscan.fit_predict(df)
        
        # Skip if all points are noise or only one cluster
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        if n_clusters > 1:
            score = silhouette_score(df, labels)
            silhouette_scores.append(score)
            n_clusters_list.append(n_clusters)
            
            if score > best_score:
                best_score = score
                best_model = dbscan
                best_eps = eps
        else:
            silhouette_scores.append(-1)
            n_clusters_list.append(n_clusters)
    
    # Save the best model
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    
    # Save as tuple
    model_data = (best_model, scaler, feature_names, best_eps)
    
    with open(output_path, "wb") as f:
        pickle.dump(model_data, f)
    
    return {
        'silhouette_scores': silhouette_scores,
        'n_clusters_list': n_clusters_list,
        'best_eps': float(best_eps),
        'best_score': float(best_score)
    }


def load_model_elbow(filename: str, metrics: dict):
    """
    Loads the saved DBSCAN model and makes predictions.
    Returns the first prediction for test.csv.
    """
    # load the saved model
    output_path = os.path.join(os.path.dirname(__file__), "../model", filename)
    with open(output_path, "rb") as f:
        model_data = pickle.load(f)
    
    # Unpack tuple (NOT dictionary access)
    loaded_model = model_data[0]
    scaler = model_data[1]
    feature_names = model_data[2]
    best_eps = model_data[3]
    
    print(f"Best epsilon: {best_eps}")
    print(f"Best silhouette score: {metrics['best_score']}")
    
    # Load and preprocess test data
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/test.csv"))
    df = df.dropna()
    
    # Apply same feature engineering
    test_data = df[["BALANCE", "PURCHASES", "CREDIT_LIMIT"]].copy()
    test_data['PURCHASES_TO_LIMIT_RATIO'] = (
        test_data['PURCHASES'] / (test_data['CREDIT_LIMIT'] + 1)
    )
    test_data['BALANCE_TO_LIMIT_RATIO'] = (
        test_data['BALANCE'] / (test_data['CREDIT_LIMIT'] + 1)
    )
    
    # Scale using saved scaler
    test_data_scaled = scaler.transform(test_data)
    
    # Predict
    pred = loaded_model.fit_predict(test_data_scaled)[0]
    
    return int(pred) if pred != -1 else -1  # -1 indicates noise point in DBSCAN