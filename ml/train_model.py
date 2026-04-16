import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load data
df = pd.read_csv('invoice_data.csv')

def check_gstin_format(gstin):
    # Standard Indian GSTIN format: 2 digits + 10 alphanumeric + 1 digit + 'Z' + 1 alphanumeric
    pattern = r'^[0-3][0-9][A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$'
    # Simplified check for our mock: starts with 2 digits (state code)
    return 1 if re.match(r'^[0-9]{2}[A-Z0-9]{13}$', str(gstin)) else 0

def preprocess_features(data):
    features = pd.DataFrame()
    
    # 1. GSTIN Format Validity
    features['gstin_valid'] = data['seller_gst'].apply(check_gstin_format)
    
    # 2. Calculation Integrity
    features['calc_diff'] = np.abs((data['subtotal'] + data['taxes']) - data['total_amount'])
    features['is_calc_correct'] = (features['calc_diff'] < 0.1).astype(int)
    
    # 3. Tax Rate Integrity
    features['tax_calc_diff'] = np.abs((data['subtotal'] * data['gst_percentage'] / 100) - data['taxes'])
    features['is_tax_correct'] = (features['tax_calc_diff'] < 0.1).astype(int)
    
    # 4. Product Category Mapping (Simple encoding)
    categories = {'Electronics': 1, 'Books': 2, 'Luxury Goods': 3, 'Grocery': 4, 'Services': 5, 'Essential Medicine': 6}
    features['category_id'] = data['product_category'].map(categories)
    
    # 5. Raw values that might signal anomalies
    features['subtotal'] = data['subtotal']
    features['total_amount'] = data['total_amount']
    features['gst_percentage'] = data['gst_percentage']
    
    return features

# Prepare dataset
X = preprocess_features(df)
y = df['is_fraud']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
print("Training Random Forest Classifier...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save model and feature list
joblib.dump(model, 'invoice_fraud_model.pkl')
print("Model saved to invoice_fraud_model.pkl")

# Save a small sample for node.js inference test
sample_data = X_test.head(1).to_dict(orient='records')[0]
print(f"Sample features for testing: {sample_data}")
