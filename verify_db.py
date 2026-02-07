import sqlite3
import json

DB_PATH = "film_recipes.db"

def verify():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Count
    cursor.execute("SELECT count(*) FROM recipes")
    count = cursor.fetchone()[0]
    print(f"Total recipes: {count}")
    
    # Sample
    print("\nSample Recipe:")
    cursor.execute("SELECT name, film_simulation, dynamic_range, full_settings FROM recipes ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    if row:
        print(f"Name: {row[0]}")
        print(f"Sim: {row[1]}")
        print(f"DR: {row[2]}")
        print(f"Full Settings: {row[3]}")
        
    conn.close()

if __name__ == "__main__":
    verify()
