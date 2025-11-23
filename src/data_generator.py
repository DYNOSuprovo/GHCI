import pandas as pd
import random
import yaml
import os

def load_config(config_path="config/categories.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def generate_synthetic_data(num_samples=50000, output_path="data/transactions.csv"):
    config = load_config()
    categories = config["categories"]
    
    data = []
    
    for _ in range(num_samples):
        category = random.choice(categories)
        keyword = random.choice(category["keywords"])
        
        # Simulate noise
        noise_types = [
            lambda k: k.upper(),
            lambda k: k.lower(),
            lambda k: f"POS {k} 1234",
            lambda k: f"PAYPAL *{k}",
            lambda k: f"{k} STORE NY",
            lambda k: f"{k} #12345",
            lambda k: f"TST* {k}",
            lambda k: f"SQ *{k}",
            lambda k: f"AMZN Mktp {k}",
            lambda k: f"{k} .COM",
            lambda k: f"CHECKCARD {k}",
            lambda k: f"{k}",
        ]
        
        description = random.choice(noise_types)(keyword)
        amount = round(random.uniform(5.0, 500.0), 2)
        
        data.append({
            "description": description,
            "amount": amount,
            "category": category["name"],
            "category_id": category["id"]
        })
        
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {num_samples} transactions at {output_path}")

if __name__ == "__main__":
    generate_synthetic_data()
