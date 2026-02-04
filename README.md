# Store Intelligence API Suite
**FastAPI + Machine Learning | Clustering + Regression**

This project deploys a complete store intelligence system with two ML models working together:
1. **Clustering API** - Groups stores into business categories (K-Means)
2. **Sales Prediction API** - Forecasts sales based on store characteristics (Random Forest)

Both models are accessible through REST APIs, allowing integration with any system (Power BI, Excel, web apps, mobile apps).

---

## What This Project Does

### Clustering Model (Unsupervised Learning)
Groups stores into **4 business-friendly categories** based on:
- Marketing Spend
- Store Size  
- Competitor Price Index

**Output Categories:**
- Low Value
- Emerging
- Core
- High Value

### Sales Prediction Model (Supervised Learning)
Predicts **Monthly Sales** using:
- Marketing Spend
- Store Size
- Number of Products
- Competitor Price Index

---

## Project Structure

```text
.
├── sales.csv                          # Training dataset
├── clustering_training.py             # Train K-Means clustering model
├── regression_training.py             # Train Random Forest regression model
├── main_cluster_api.py                # FastAPI clustering endpoint
├── main_regression_api.py             # FastAPI sales prediction endpoint
├── store_cluster_scaler.joblib        # Scaler for clustering
├── store_kmeans_model.joblib          # Trained K-Means model
├── cluster_features.joblib            # Feature names for clustering
├── cluster_labels.joblib              # Cluster category mapping
├── sales_scaler.joblib                # Scaler for regression
├── sales_model.joblib                 # Trained Random Forest model
├── model_features.joblib              # Feature names for regression
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

---

## Dataset (`sales.csv`)

Required columns:

| Column | Description | Used In |
|--------|-------------|---------|
| `Marketing_Spend` | Monthly marketing budget | Both models |
| `Store_Size` | Store size in sqm | Both models |
| `Competitor_Price_Index` | Competitor pricing pressure | Both models |
| `Number_of_Products` | Product count | Regression only |
| `Sales` | Monthly sales (target) | Regression training & cluster ranking |

---

## Machine Learning Approach

### Clustering Model
- **Type:** Unsupervised Learning
- **Algorithm:** K-Means
- **Preprocessing:** StandardScaler
- **Number of Clusters:** 4 (chosen via Elbow Method)
- **Cluster Ranking:** Based on average Sales per cluster

**Cluster Label Mapping:**
1. Lowest avg sales → **Low Value**
2. Second lowest → **Emerging**
3. Second highest → **Core**
4. Highest avg sales → **High Value**

### Regression Model
- **Type:** Supervised Learning
- **Algorithm:** Random Forest Regressor
- **Preprocessing:** StandardScaler
- **Hyperparameters:** 100 trees, max_depth=10, random_state=42
- **Evaluation Metrics:** MAE, MSE, RMSE, R²

---

## Installation

### 1. Create & Activate Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux / macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Or install manually:**

```bash
pip install fastapi uvicorn scikit-learn pandas numpy joblib matplotlib
```

---

## Training the Models (One-Time Setup)

### Train Clustering Model

```bash
python clustering_training.py
```

**Generates:**
- `store_cluster_scaler.joblib`
- `store_kmeans_model.joblib`
- `cluster_features.joblib`
- `cluster_labels.joblib`

### Train Regression Model

```bash
python regression_training.py
```

**Generates:**
- `sales_scaler.joblib`
- `sales_model.joblib`
- `model_features.joblib`

---

## Running the APIs

### Option 1: Run Both APIs Separately

**Terminal 1 - Clustering API:**
```bash
uvicorn main_cluster_api:app --reload --host 0.0.0.0 --port 8001
```
Docs: http://127.0.0.1:8001/docs

**Terminal 2 - Regression API:**
```bash
uvicorn main_regression_api:app --reload --host 0.0.0.0 --port 8000
```
Docs: http://127.0.0.1:8000/docs

### Option 2: Combined API (Recommended)

Create `main.py` to combine both:

```python
from fastapi import FastAPI
from main_cluster_api import app as cluster_app
from main_regression_api import app as regression_app

app = FastAPI(title="Store Intelligence API Suite")

# Mount sub-applications
app.mount("/clustering", cluster_app)
app.mount("/prediction", regression_app)

@app.get("/")
def root():
    return {
        "message": "Store Intelligence API Suite",
        "endpoints": {
            "clustering": "/clustering/docs",
            "prediction": "/prediction/docs"
        }
    }
```

Run combined API:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

---

## Testing the APIs

### Clustering API

**Health Check:**
```bash
curl http://127.0.0.1:8001/
```

**Assign Store Cluster:**
```bash
curl -X POST http://127.0.0.1:8001/cluster \
-H "Content-Type: application/json" \
-d '{"Marketing_Spend":25000,"Store_Size":220,"Competitor_Price_Index":0.95}'
```

**Example Response:**
```json
{
  "cluster_id": 3,
  "store_category": "High Value"
}
```

---

### Regression API

**Health Check:**
```bash
curl http://127.0.0.1:8000/
```

**Predict Sales:**
```bash
curl -X POST http://127.0.0.1:8000/predict \
-H "Content-Type: application/json" \
-d '{"Marketing_Spend":25000,"Store_Size":220,"Number_of_Products":85,"Competitor_Price_Index":0.95}'
```

**Example Response:**
```json
{
  "predicted_sales": 67832.45
}
```

---

## API Endpoints Reference

### Clustering API (`/cluster`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/cluster` | Assign store to cluster |

**Request Body (`/cluster`):**
```json
{
  "Marketing_Spend": 25000,
  "Store_Size": 220,
  "Competitor_Price_Index": 0.95
}
```

**Response:**
```json
{
  "cluster_id": 2,
  "store_category": "Core"
}
```

---

### Regression API (`/predict`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/predict` | Predict monthly sales |

**Request Body (`/predict`):**
```json
{
  "Marketing_Spend": 25000,
  "Store_Size": 220,
  "Number_of_Products": 85,
  "Competitor_Price_Index": 0.95
}
```

**Response:**
```json
{
  "predicted_sales": 67832.45
}
```

---

## Use Cases

### Business Intelligence
- Segment stores for targeted marketing campaigns
- Forecast revenue for budget planning
- Identify underperforming stores

### Integration Examples
- **Power BI:** Import predictions via REST API connector
- **Excel:** Use Power Query to fetch predictions
- **Web Dashboard:** Build React/Vue frontend
- **Mobile App:** Integrate via HTTP requests
- **ETL Pipelines:** Automate predictions in data workflows

---

## Learning Outcomes

This project teaches:

**Machine Learning:**
- Unsupervised learning (K-Means clustering)
- Supervised learning (Random Forest regression)
- Feature scaling with StandardScaler
- Model evaluation (R², MAE, RMSE)
- Hyperparameter tuning
- Model persistence with joblib

**API Development:**
- Building REST APIs with FastAPI
- Request validation with Pydantic
- API documentation (Swagger/OpenAPI)
- Testing APIs with curl
- Deploying ML models in production

**Software Engineering:**
- Project structure & organization
- Virtual environments
- Dependency management
- Version control readiness

---

## Key Concepts

### Why Two Models?
1. **Clustering** → Discovers hidden patterns (no target variable)
2. **Regression** → Predicts specific outcomes (has target variable)

### Why This Architecture?
- **Separation of Concerns:** Each model has its own API
- **Scalability:** Models can be updated independently
- **Flexibility:** Clients can use one or both APIs

### Real-World Value
**Before ML:** Manual store categorization, guesswork on sales  
**After ML:** Data-driven decisions, accurate forecasts, scalable intelligence

---

## Next Steps & Extensions

### Beginner Level
- [ ] Add input validation error messages
- [ ] Create a simple HTML frontend
- [ ] Add logging to track API usage

### Intermediate Level
- [ ] Combine predictions: `/intelligent-forecast` (cluster + sales)
- [ ] Add PostgreSQL database for logging predictions
- [ ] Implement API authentication (JWT tokens)
- [ ] Add rate limiting

### Advanced Level
- [ ] Deploy to AWS/GCP/Azure with Docker
- [ ] Set up CI/CD pipeline (GitHub Actions)
- [ ] Add model monitoring & retraining pipeline
- [ ] Build admin dashboard for model performance

---

## Requirements File

**`requirements.txt`:**
```text
fastapi==0.104.1
uvicorn[standard]==0.24.0
scikit-learn==1.3.2
pandas==2.1.3
numpy==1.26.2
joblib==1.3.2
matplotlib==3.8.2
pydantic==2.5.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution:** Ensure virtual environment is activated and dependencies are installed

### Issue: Port already in use
**Solution:** Change port number:
```bash
uvicorn main:app --port 8002
```

### Issue: Model files not found
**Solution:** Run training scripts first:
```bash
python clustering_training.py
python regression_training.py
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is open source and available under the MIT License.

---

## Author

Built as a learning project to demonstrate ML model deployment with FastAPI.

---

## Summary

| Feature | Clustering API | Regression API |
|---------|----------------|----------------|
| **Type** | Unsupervised | Supervised |
| **Algorithm** | K-Means | Random Forest |
| **Input Features** | 3 | 4 |
| **Output** | Category Label | Numeric Prediction |
| **Business Value** | Store Segmentation | Revenue Forecasting |

**Together, these APIs provide complete store intelligence:** Know which category a store belongs to AND predict its sales potential.

---

**Ready to deploy intelligent ML systems? Start here!**
