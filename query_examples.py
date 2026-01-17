import sqlite3
import pandas as pd

DB_PATH = "film_recipes.db"

def run_query(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    try:
        # Use pandas for pretty printing if available, else standard cursor
        df = pd.read_sql_query(query, conn, params=params)
        if not df.empty:
            print(df.to_markdown(index=False))
        else:
            print("No results found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def main():
    print("--- 1. All Unique Film Simulations Used ---")
    run_query("SELECT DISTINCT film_simulation FROM recipes ORDER BY film_simulation")

    print("\n--- 2. Recipes using 'Reala Ace' ---")
    run_query("SELECT name, sensor, iso FROM recipes WHERE film_simulation LIKE ?", ('%Reala Ace%',))

    print("\n--- 3. Count of Recipes per Sensor ---")
    run_query("SELECT sensor, COUNT(*) as count FROM recipes GROUP BY sensor")

    print("\n--- 4. Recipes with High ISO Noise Reduction (-4) ---")
    # Note: Values are currently text, so exact string match or casting might be needed depending on precision
    run_query("SELECT name, noise_reduction FROM recipes WHERE noise_reduction = '-4' LIMIT 5")

    print("\n--- 5. Recipes with Positive Red Shift (> 2) ---")
    run_query("SELECT name, white_balance, wb_shift_red FROM recipes WHERE wb_shift_red > 2 LIMIT 5")

if __name__ == "__main__":
    # Ensure pandas is installed for this script, or fall back to printing rows
    try:
        import pandas
        import tabulate # required for to_markdown
    except ImportError:
        print("Installing pandas and tabulate for pretty output...")
        import os
        import sys
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "tabulate"])
    
    main()
