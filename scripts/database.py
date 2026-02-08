import sqlite3
import json
from typing import Optional, Dict, Any

DB_PATH = "film_recipes.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        -- Main Recipe Table
        -- We store standard fields as columns for fast SQL querying (analytics).
        -- 'full_settings' is a JSON dump to catch any new/weird fields Fuji adds in the future without migration.
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sensor TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            film_simulation TEXT,
            dynamic_range TEXT,
            grain_effect TEXT,
            white_balance TEXT,
            highlight TEXT,
            shadow TEXT,
            color TEXT,
            sharpness TEXT,
            noise_reduction TEXT,
            clarity TEXT,
            iso TEXT,
            exposure_compensation TEXT,
            wb_shift_red INTEGER,
            wb_shift_blue INTEGER,
            full_settings TEXT,  -- JSON string
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_recipe(data: Dict[str, Any]):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Serialize full_settings to JSON if present
    if "full_settings" in data and isinstance(data["full_settings"], dict):
        data["full_settings"] = json.dumps(data["full_settings"])

    fields = [
        "name", "sensor", "url", "film_simulation", "dynamic_range", 
        "grain_effect", "white_balance", "highlight", "shadow", "color", 
        "sharpness", "noise_reduction", "clarity", "iso", 
        "exposure_compensation", "wb_shift_red", "wb_shift_blue", "full_settings"
    ]
    
    # Filter data to only include known fields
    insert_data = {k: data.get(k) for k in fields}
    
    placeholders = ", ".join(["?"] * len(fields))
    columns = ", ".join(fields)
    
    sql = f"""
        INSERT INTO recipes ({columns}) 
        VALUES ({placeholders})
        ON CONFLICT(url) DO UPDATE SET
            name=excluded.name,
            sensor=excluded.sensor,
            film_simulation=excluded.film_simulation,
            dynamic_range=excluded.dynamic_range,
            grain_effect=excluded.grain_effect,
            white_balance=excluded.white_balance,
            highlight=excluded.highlight,
            shadow=excluded.shadow,
            color=excluded.color,
            sharpness=excluded.sharpness,
            noise_reduction=excluded.noise_reduction,
            clarity=excluded.clarity,
            iso=excluded.iso,
            exposure_compensation=excluded.exposure_compensation,
            wb_shift_red=excluded.wb_shift_red,
            wb_shift_blue=excluded.wb_shift_blue,
            full_settings=excluded.full_settings
    """
    
    values = [insert_data[f] for f in fields]
    
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
