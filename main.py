import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, MinMaxScaler

df = pd.read_csv("./clustering/survey/FlourishingScale.csv")
df = df.drop(columns=["uid", "type"], axis=1)

for column in df.columns:
    df[column].fillna(df[column].mode()[0], inplace=True)

# Step 1: Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# Step 2: Apply PCA for dimensionality reduction (optional, helps with clustering)
pca = PCA(n_components=2)
pca_data = pca.fit_transform(scaled_data)

# Step 3: Perform K-Means Clustering (Assuming 3 burnout levels: Low, Medium, High)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(pca_data)
df['Burnout_Level'] = clusters

# Step 4: Apply Isolation Forest for anomaly detection
iso_forest = IsolationForest(contamination=0.1, random_state=42)
anomaly_scores = iso_forest.fit_predict(
    scaled_data)  # -1 for anomalies, 1 for normal

# Step 5: Assign Burnout Risk Score (1-10)
# Normalize cluster distances and anomaly scores to get a final risk score
cluster_distances = np.linalg.norm(
    pca_data - kmeans.cluster_centers_[clusters], axis=1)
risk_scores = MinMaxScaler(feature_range=(1, 10)).fit_transform(
    cluster_distances.reshape(-1, 1))

# Penalize anomalies (increase their burnout risk score)
df['Burnout_Risk_Score'] = risk_scores.flatten()
# Increase risk for outliers
df.loc[anomaly_scores == -1, 'Burnout_Risk_Score'] += 2

# Ensure scores stay within 1-10
df['Burnout_Risk_Score'] = df['Burnout_Risk_Score'].clip(1, 10)

# Rounding to 1 decimal
df['Burnout_Risk_Score'] = np.round(df['Burnout_Risk_Score'], 1)

# Step 6: Plot results
plt.scatter(pca_data[:, 0], pca_data[:, 1],
            c=df['Burnout_Risk_Score'], cmap='coolwarm')
plt.colorbar(label="Burnout Risk Score (1-10)")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.title("Burnout Risk Clustering with PCA")
plt.show()

# Show sample results
print(df[['Burnout_Level', 'Burnout_Risk_Score']].head(10))
