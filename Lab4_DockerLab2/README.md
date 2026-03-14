## Project Structure

```
Lab4_DockerLab2/
├── docker-compose.yml
├── requirements.txt
└── src/
    ├── model_training.py   # Trains and saves the model
    ├── main.py             # Flask web server
    ├── templates/
    │   └── predict.html    # Frontend UI
    └── statics/
        ├── setosa.jpeg
        ├── versicolor.jpeg
        └── virginica.jpeg
```

---

## How It Works

### 1. Model Training
`model_training.py` loads the Iris dataset, standardizes the features using `StandardScaler`, and trains a neural network with the following architecture:
- Dense layers: 64 → 128 → 64 → 32 neurons
- Batch Normalization and Dropout at each layer to prevent overfitting
- Early stopping to automatically stop training when the model stops improving
- Saves the trained model as `my_model.keras`

I made the architecture a bit more complex than the sample

### 2. Model Serving
`main.py` is a Flask app that:
- Loads the trained model on startup
- Serves the prediction UI at `GET /predict`
- Accepts flower measurements via `POST /predict` and returns the predicted species and class probabilities as JSON

### 3. Docker Setup
Two services are defined in `docker-compose.yml`:
- **model-training** — runs training and copies the model to a shared Docker volume
- **serving** — waits for training to complete, copies the model from the shared volume, and starts the Flask server

The `serving` service only starts after `model-training` completes successfully (`condition: service_completed_successfully`).

---

## Running the App

**Prerequisites:** Docker Desktop installed and running.

```bash
docker compose up
```

This will:
1. Train the model
2. Start the Flask server once training is done
3. Serve the app at **http://localhost:4000**

To stop:
```bash
docker compose down
```

---

## Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Health check |
| GET | `/predict` | Prediction UI |
| POST | `/predict` | Run prediction, returns JSON |

### POST `/predict` — Example Response
```json
{
  "predicted_class": "Setosa",
  "probabilities": {
    "Setosa": 0.97,
    "Versicolor": 0.02,
    "Virginica": 0.01
  }
}
```

---

## Input Features

| Feature | Description | Example |
|---------|-------------|---------|
| `sepal_length` | Sepal length in cm | 5.1 |
| `sepal_width` | Sepal width in cm | 3.5 |
| `petal_length` | Petal length in cm | 1.4 |
| `petal_width` | Petal width in cm | 0.2 |


In the html, i added a highlight around the pictures and a bar to show teh confidence levels. 