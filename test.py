import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest


def assign_burnout_risk(new_student_data, scaler, pca, kmeans, iso_forest, min_max_scaler, min_score=1, max_score=10):
    """
    Assigns a burnout risk score to a new student based on the trained clustering model.

    Parameters:
    - new_student_data: 1D array-like, raw input features of the new student
    - scaler: Trained StandardScaler instance
    - pca: Trained PCA instance
    - kmeans: Trained KMeans model
    - iso_forest: Trained Isolation Forest model
    - min_score, max_score: Range for risk score scaling

    Returns:
    - risk_score: Normalized risk score (1-10)
    """
    # Scale the new student's data using the trained scaler
    new_scaled = scaler.transform([new_student_data])

    # Apply PCA transformation
    new_pca = pca.transform(new_scaled)

    # Predict the cluster the student belongs to
    cluster = kmeans.predict(new_pca)[0]

    # Compute the distance from the new point to the cluster centroid
    centroid = kmeans.cluster_centers_[cluster]
    distance = np.linalg.norm(new_pca - centroid)

    # Normalize the distance to a 1-10 scale
    risk_score = min_max_scaler.transform(
        [[distance]])[0][0]  # Ensure proper transformation

    # Check for anomalies using Isolation Forest
    anomaly_score = iso_forest.decision_function(new_scaled)
    if anomaly_score < 0:
        risk_score += 2  # Slightly increase risk for anomalies

    # Ensure it's within bounds
    risk_score = np.clip(risk_score, min_score, max_score)

    return round(risk_score, 1)


# Load the saved models
# scaler = joblib.load('./clustering/trained_models/scaler.pkl')
# pca = joblib.load('./clustering/trained_models/pca.pkl')
# min_max_scaler = joblib.load('./clustering/trained_models/min_max_scaler.pkl')
# kmeans = joblib.load('./clustering/trained_models/kmeans.pkl')
# iso_forest = joblib.load('./clustering/trained_models/iso_forest.pkl')


# # Replace with actual student questionnaire responses
# new_student_data = np.array([6, 7, 5, 6, 5, 6, 4, 7])  # 8 features

# risk_score = assign_burnout_risk(
#     new_student_data, scaler, pca, kmeans, iso_forest, min_max_scaler)
# print(f"Burnout Risk Score: {risk_score}")
