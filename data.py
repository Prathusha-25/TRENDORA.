import pandas as pd
import numpy as np
from datetime import datetime
import random

random.seed(42)
np.random.seed(42)

TRENDS = [
    {"id": 1, "name": "Baggy Cargo Pants", "category": "Bottoms", "heat": 94, "direction": "Viral", "city": "Hyderabad", "change": "+38%", "tags": ["streetwear", "Gen-Z", "unisex"], "urgency": "HIGH", "description": "Cargo silhouettes dominating local markets.", "peak_weeks": 6},
    {"id": 2, "name": "Pastel Oversized Shirts", "category": "Tops", "heat": 87, "direction": "Rising", "city": "Hyderabad", "change": "+24%", "tags": ["summer", "unisex", "casual"], "urgency": "HIGH", "description": "Pastel oversized shirts trending across Instagram reels.", "peak_weeks": 8},
    {"id": 3, "name": "Co-ord Sets", "category": "Sets", "heat": 82, "direction": "Rising", "city": "Hyderabad", "change": "+19%", "tags": ["fusion", "women", "festive"], "urgency": "MEDIUM", "description": "Ethnic-modern fusion co-ords gaining traction.", "peak_weeks": 10},
    {"id": 4, "name": "Relaxed Linen Trousers", "category": "Bottoms", "heat": 71, "direction": "Rising", "city": "Hyderabad", "change": "+15%", "tags": ["summer", "workwear"], "urgency": "MEDIUM", "description": "Comfort-work hybrid trend.", "peak_weeks": 12},
    {"id": 5, "name": "Logo Crop Hoodies", "category": "Tops", "heat": 65, "direction": "Stable", "city": "Hyderabad", "change": "+4%", "tags": ["streetwear", "women"], "urgency": "LOW", "description": "Holding steady as a consistent seller.", "peak_weeks": 16},
    {"id": 6, "name": "Formal Straight Blazers", "category": "Outerwear", "heat": 38, "direction": "Declining", "city": "Hyderabad", "change": "-12%", "tags": ["formal", "office"], "urgency": "DEAD_STOCK", "description": "Formal wear slowing down.", "peak_weeks": 0},
]

INVENTORY = [
    {"sku": "BGC-001", "name": "Baggy Cargo Pants - Olive", "qty": 12, "reorder_point": 30, "cost": 480, "selling_price": 1299, "status": "REORDER NOW", "category": "Bottoms", "trend_alignment": 94, "image_path": ""},
    {"sku": "PST-002", "name": "Pastel Oversized Shirt - Blue", "qty": 8, "reorder_point": 25, "cost": 320, "selling_price": 899, "status": "REORDER NOW", "category": "Tops", "trend_alignment": 87, "image_path": ""},
    {"sku": "CRD-003", "name": "Ethnic Co-ord Set - Beige", "qty": 34, "reorder_point": 20, "cost": 650, "selling_price": 1799, "status": "HEALTHY", "category": "Sets", "trend_alignment": 82, "image_path": ""},
    {"sku": "BLZ-005", "name": "Straight Blazer - Black", "qty": 78, "reorder_point": 10, "cost": 890, "selling_price": 1499, "status": "DEAD STOCK", "category": "Outerwear", "trend_alignment": 38, "image_path": ""},
]

PRICING = [
    {"product": "Baggy Cargo Pants", "your_price": 1299, "market_avg": 1350, "suggested": 1399, "opportunity": "Price UP"},
    {"product": "Pastel Oversized Shirt", "your_price": 899, "market_avg": 849, "suggested": 949, "opportunity": "Price UP"},
    {"product": "Logo Crop Hoodie", "your_price": 999, "market_avg": 849, "suggested": 849, "opportunity": "Reduce Price"},
    {"product": "Straight Blazer", "your_price": 1499, "market_avg": 1099, "suggested": 999, "opportunity": "Clearance Sale"},
]

WHOLESALERS = [
    {"name": "Rajesh Textiles & Exports", "city": "Surat", "rating": 4.8, "speciality": "Bottoms & Denims", "products": ["Baggy Cargo Pants", "Relaxed Linen Trousers"]},
    {"name": "Femina Fashion House", "city": "Jaipur", "rating": 4.6, "speciality": "Women's Fashion", "products": ["Pastel Oversized Shirts", "Printed Maxi Dresses"]},
    {"name": "StyleSync Wholesale Hub", "city": "Mumbai", "rating": 4.4, "speciality": "Fusion & Streetwear", "products": ["Ethnic Co-ord Sets", "Logo Crop Hoodies"]},
]

CATEGORIES = ["All", "Tops", "Bottoms", "Dresses", "Sets", "Outerwear"]

def get_forecast_data():
    return {
        "weeks": [f"W{i}" for i in range(1, 13)],
        "Baggy Cargo Pants": [18, 24, 32, 41, 55, 68, 74, 70, 62, 50, 38, 28],
        "Pastel Oversized Shirts": [22, 28, 35, 44, 52, 61, 65, 60, 52, 42, 30, 22],
        "Formal Blazers": [20, 18, 15, 12, 10, 8, 7, 6, 6, 5, 5, 4],
    }

def get_sales_history():
    dates = pd.date_range(end=datetime.today(), periods=30, freq="D")
    return pd.DataFrame({
        "date": dates,
        "revenue": np.random.randint(8000, 28000, 30),
        "units_sold": np.random.randint(15, 65, 30),
    })