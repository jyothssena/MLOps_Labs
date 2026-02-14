Lab No.2 - Airflow Lab 1 

Step 1. Setup Airflow and Docker 

Step 2: Altered the model pipeline 
Functions
- `load_data()`: Loads and serializes CSV data
- `data_preprocessing()`: Performs feature engineering, outlier removal, and scaling
  Feature engineering with ratio calculations, outlier removal using IQR method, and RobustScaler normalization
- `build_save_model()`: Trains DBSCAN model with parameter optimization
  Density-based clustering that automatically identifies optimal clusters and detects noise points
- `load_model_elbow()`: Loads saved model and makes predictions on test data
  Uses silhouette score to select the best epsilon parameter across multiple iterations

Step 3 : Created a DAG file - airflow.py 

Step 4: Trigger the DAG
Triggered the DAG pipeline and fixed errors.

Step 6: Pipeline Outputs
Once the DAG completes its execution, check the outputs from the functions.
