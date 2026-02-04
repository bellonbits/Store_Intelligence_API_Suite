from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

scaler = joblib.load('store_cluster_scaler.joblib')
kmeans = joblib.load('store_kmeans_model.joblib')
feature_names = joblib.load('cluster_features.joblib')
cluster_labels = joblib.load('cluster_lables.joblib')

app = FastAPI(title='Store Clustering API')

class StoreFeatures(BaseModel):
    Marketing_spend: float
    Store_Size: float
    Competitor_Price_Index: float

@app.get('/')
def root():
    return {"message":"Store Api is Up"}

@app.post('/cluster')
def assign_cluster(data: StoreFeatures):
    x = np.array([[getattr(data, f) for f in feature_names]])
    x_scaled = scaler.transform(x)
    cluster_id = int(kmeans.predict(x_scaled)[0])
    store_category = cluster_labels.get(cluster_id, 'Unknown')

    return {
        'cluster_id':cluster_id,
        'store_category':store_category
    }