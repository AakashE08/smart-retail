import sys
import json
import joblib
import pandas as pd
import re
import numpy as np
import os

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'invoice_fraud_model.pkl')
model = joblib.load(model_path)

def check_gstin_format(gstin):
    return 1 if re.match(r'^[0-9]{2}[A-Z0-9]{13}$', str(gstin)) else 0

def preprocess_single(data):
    # Mapping categories to same IDs used in training
    categories = {'Electronics': 1, 'Books': 2, 'Luxury Goods': 3, 'Grocery': 4, 'Services': 5, 'Essential Medicine': 6}
    
    cat_id = categories.get(data.get('product_category'), 0)
    
    features = {
        'gstin_valid': check_gstin_format(data.get('seller_gst', '')),
        'calc_diff': np.abs((data.get('subtotal', 0) + data.get('taxes', 0)) - data.get('total_amount', 0)),
        'is_calc_correct': 1 if np.abs((data.get('subtotal', 0) + data.get('taxes', 0)) - data.get('total_amount', 0)) < 0.1 else 0,
        'tax_calc_diff': np.abs((data.get('subtotal', 0) * data.get('gst_percentage', 0) / 100) - data.get('taxes', 0)),
        'is_tax_correct': 1 if np.abs((data.get('subtotal', 0) * data.get('gst_percentage', 0) / 100) - data.get('taxes', 0)) < 0.1 else 0,
        'category_id': cat_id,
        'subtotal': data.get('subtotal', 0),
        'total_amount': data.get('total_amount', 0),
        'gst_percentage': data.get('gst_percentage', 0)
    }
    return pd.DataFrame([features])

if __name__ == "__main__":
    try:
        arg = sys.argv[1]
        if os.path.exists(arg):
            with open(arg, 'r') as f:
                input_data = json.load(f)
        else:
            input_data = json.loads(arg)
            
        X = preprocess_single(input_data)
        prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0].tolist()
        
        result = {
            "is_fraud": int(prediction),
            "confidence": float(max(probability)),
            "analysis": {
                "gstin_valid": bool(X['gstin_valid'][0]),
                "is_calc_correct": bool(X['is_calc_correct'][0]),
                "is_tax_correct": bool(X['is_tax_correct'][0])
            }
        }
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

