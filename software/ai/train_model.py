"""
AI Model Training for Gas Leak Detection
Uses Isolation Forest for anomaly detection
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_prepare_data():
    """Load and prepare training data"""
    print("Loading training data...")
    data = pd.read_csv('training_data.csv')
    
    # Feature engineering
    data['mq2_moving_avg'] = data['mq2_value'].rolling(window=5).mean()
    data['mq7_moving_avg'] = data['mq7_value'].rolling(window=5).mean()
    data['sensor_ratio'] = data['mq2_value'] / data['mq7_value']
    
    # Fill NaN values from rolling average
    data = data.fillna(method='bfill')
    
    # Select features for training
    features = ['mq2_value', 'mq7_value', 'temperature', 'humidity', 
                'mq2_moving_avg', 'mq7_moving_avg', 'sensor_ratio']
    
    X = data[features]
    y = data['label']
    
    return X, y, features

def train_isolation_forest(X, y):
    """Train Isolation Forest model"""
    print("Training Isolation Forest model...")
    
    # Split data (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train model - adjust contamination based on expected anomaly rate
    model = IsolationForest(
        n_estimators=100,
        max_samples='auto',
        contamination=0.1,  # Expected 10% anomalies
        random_state=42,
        verbose=1
    )
    
    # Fit the model
    model.fit(X_train)
    
    # Predict on test set
    y_pred = model.predict(X_test)
    
    # Convert predictions (Isolation Forest: 1=normal, -1=anomaly)
    y_pred_binary = [1 if x == -1 else 0 for x in y_pred]
    
    return model, X_test, y_test, y_pred_binary

def evaluate_model(y_true, y_pred):
    """Evaluate model performance"""
    print("Evaluating model performance...")
    
    # Classification report
    print("\n📊 Classification Report:")
    print(classification_report(y_true, y_pred))
    
    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Normal', 'Leak'],
                yticklabels=['Normal', 'Leak'])
    plt.title('Confusion Matrix - Gas Leak Detection')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.savefig('confusion_matrix.png')
    plt.show()
    
    # Calculate accuracy
    accuracy = (y_true == y_pred).mean()
    print(f"✅ Model Accuracy: {accuracy:.2%}")
    
    return accuracy

def save_model(model, features):
    """Save the trained model"""
    model_filename = 'gas_leak_model.pkl'
    joblib.dump(model, model_filename)
    
    # Save feature list
    feature_info = {
        'features': features,
        'feature_count': len(features),
        'model_type': 'IsolationForest'
    }
    
    import json
    with open('model_features.json', 'w') as f:
        json.dump(feature_info, f, indent=2)
    
    print(f"✅ Model saved as: {model_filename}")
    print(f"✅ Feature info saved as: model_features.json")
    
    return model_filename

def main():
    """Main training pipeline"""
    print("=== AI Model Training Pipeline ===")
    
    try:
        # Step 1: Load and prepare data
        X, y, features = load_and_prepare_data()
        print(f"📊 Dataset shape: {X.shape}")
        print(f"🎯 Features: {features}")
        
        # Step 2: Train model
        model, X_test, y_test, y_pred = train_isolation_forest(X, y)
        
        # Step 3: Evaluate model
        accuracy = evaluate_model(y_test, y_pred)
        
        # Step 4: Save model
        if accuracy > 0.85:  # Only save if accuracy > 85%
            model_path = save_model(model, features)
            print(f"🎉 Model training completed successfully!")
            print(f"📈 Final Accuracy: {accuracy:.2%}")
        else:
            print("❌ Model accuracy too low. Retraining needed.")
            
    except Exception as e:
        print(f"❌ Error during training: {e}")

if __name__ == "__main__":
    main()
