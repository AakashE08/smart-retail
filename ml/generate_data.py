import csv
import random
import uuid

# Configuration
NUM_SAMPLES = 5000
OUTPUT_FILE = 'invoice_data.csv'

# Constants
PRODUCT_CATEGORIES = {
    'Electronics': 0.18,
    'Books': 0.05,
    'Luxury Goods': 0.28,
    'Grocery': 0.05,
    'Services': 0.18,
    'Essential Medicine': 0.12
}

VALID_STATE_CODES = [str(i).zfill(2) for i in range(1, 38)]

def generate_gstin(valid=True):
    if valid:
        state = random.choice(VALID_STATE_CODES)
        pan = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=5)) + \
              ''.join(random.choices('0123456789', k=4)) + \
              random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        fixed = '1Z5' # Mocking entity/checksum
        return f"{state}{pan}{fixed}"
    else:
        # Generate something that looks like GST but is clearly wrong or random
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=15))

def generate_invoice():
    category = random.choice(list(PRODUCT_CATEGORIES.keys()))
    standard_rate = PRODUCT_CATEGORIES[category]
    
    subtotal = round(random.uniform(100, 50000), 2)
    
    # Decide if this will be a fraud sample (roughly 30% chance)
    is_fraud = 0
    fraud_type = "None"
    
    rand_val = random.random()
    if rand_val < 0.3:
        is_fraud = 1
        fraud_scenario = random.randint(1, 4)
        
        if fraud_scenario == 1: # WRONG_CALCULATION
            fraud_type = "Calculation Error"
            taxes = round(subtotal * standard_rate, 2)
            total = subtotal + taxes + random.choice([-50, 50, 100])
        elif fraud_scenario == 2: # WRONG_RATE for category
            fraud_type = "Rate Mismatch"
            wrong_rate = random.choice([0.05, 0.12, 0.18, 0.28])
            if wrong_rate == standard_rate: wrong_rate = 0.05 if standard_rate != 0.05 else 0.18
            taxes = round(subtotal * wrong_rate, 2)
            total = subtotal + taxes
            actual_rate = wrong_rate
        elif fraud_scenario == 3: # INVALID_GSTIN
            fraud_type = "Invalid GSTIN"
            taxes = round(subtotal * standard_rate, 2)
            total = subtotal + taxes
            return {
                'seller_gst': generate_gstin(valid=False),
                'product_category': category,
                'subtotal': subtotal,
                'taxes': taxes,
                'total_amount': total,
                'gst_percentage': standard_rate * 100,
                'is_fraud': 1,
                'fraud_type': fraud_type
            }
        else: # MISC DATA ANOMALY (e.g., negative total)
             fraud_type = "Anomalous Value"
             taxes = 0
             total = -100
    else:
        taxes = round(subtotal * standard_rate, 2)
        total = subtotal + taxes

    return {
        'seller_gst': generate_gstin(valid=True),
        'product_category': category,
        'subtotal': subtotal,
        'taxes': taxes,
        'total_amount': total,
        'gst_percentage': standard_rate * 100,
        'is_fraud': is_fraud,
        'fraud_type': fraud_type
    }

print(f"Generating {NUM_SAMPLES} samples...")
with open(OUTPUT_FILE, 'w', newline='') as f:
    fieldnames = ['seller_gst', 'product_category', 'subtotal', 'taxes', 'total_amount', 'gst_percentage', 'is_fraud', 'fraud_type']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for _ in range(NUM_SAMPLES):
        writer.writerow(generate_invoice())

print(f"Data saved to {OUTPUT_FILE}")
