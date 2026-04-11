# Wine Quality Prediction with MLflow

A machine learning project that predicts red wine quality using a **Random Forest Regressor**, with experiment tracking powered by **MLflow**.

Dataset: [UCI Wine Quality Dataset](http://archive.ics.uci.edu/ml/datasets/Wine+Quality)

---

## Project Structure

```
├── random_forest.py   # Main training script (Random Forest model)
├── serving.py             # MLflow pip requirements demo with XGBoost
├── requirements.txt       # Python dependencies
├── mlflow.db              # SQLite backend store for MLflow
└── mlruns/                # Artifact storage (created on first run)
```

---

## Setup

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Start the MLflow tracking server**
```bash
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 \
  --port 5001
```

**3. Set the tracking URI** (in a new terminal)
```bash
export MLFLOW_TRACKING_URI=http://localhost:5001
```

---

## Training

**Run with default hyperparameters** (`n_estimators=100, max_depth=None, min_samples_split=2`)
```bash
python linear_regression.py
```

**Run with custom hyperparameters**
```bash
python linear_regression.py <n_estimators> <max_depth> <min_samples_split>

```

| Argument | Description | Default |
|---|---|---|
| `n_estimators` | Number of trees in the forest | `100` |
| `max_depth` | Maximum depth of each tree (`None` = unlimited) | `None` |
| `min_samples_split` | Minimum samples required to split a node | `2` |

---

## What Gets Logged to MLflow

Each training run logs the following:

- **Parameters:** `n_estimators`, `max_depth`, `min_samples_split`
- **Metrics:** RMSE, MAE, R²
- **Artifacts:** `feature_importance.png` — bar chart of feature importances
- **Model:** Registered under `RandomForestWineModel` in the MLflow Model Registry

---

## Viewing Results

Open the MLflow UI in your browser:
```
http://localhost:5001
```

From there you can:
- Compare runs side by side
- View the feature importance plot under the **Artifacts** tab
- Manage registered models under the **Models** tab

---

## Serving the Model

Once a run completes, serve the registered model as a REST API:
```bash
mlflow models serve -m "models:/RandomForestWineModel/1" --port 1234
```

Then send a prediction request:
```bash
curl -X POST http://localhost:1234/invocations \
  -H "Content-Type: application/json" \
  -d '{
    "dataframe_split": {
      "columns": ["fixed acidity","volatile acidity","citric acid","residual sugar","chlorides","free sulfur dioxide","total sulfur dioxide","density","pH","sulphates","alcohol"],
      "data": [[7.4, 0.7, 0.0, 1.9, 0.076, 11.0, 34.0, 0.9978, 3.51, 0.56, 9.4]]
    }
  }'
```

---

## Expected Performance

| Model | R² | RMSE |
|---|---|---|
| Random Forest | ~0.45–0.55 | ~0.55–0.62 |

---