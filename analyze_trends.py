import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "film_recipes.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def analyze_trends():
    conn = get_connection()
    
    # 1. Top Film Simulation Bases
    print("## Top Film Simulation Bases")
    query_sims = """
        SELECT film_simulation, COUNT(*) as count 
        FROM recipes 
        WHERE film_simulation IS NOT NULL AND film_simulation != ''
        GROUP BY film_simulation 
        ORDER BY count DESC 
        LIMIT 5
    """
    df_sims = pd.read_sql_query(query_sims, conn)
    print(df_sims.to_markdown(index=False))
    
    # 2. Shift in Preferences: X-Trans IV vs X-Trans V
    print("\n## Evolution of Preferences (X-Trans IV vs V)")
    query_sensors = """
        SELECT sensor, film_simulation, COUNT(*) as count
        FROM recipes
        WHERE sensor IN ('X-Trans IV', 'X-Trans V')
        AND film_simulation IS NOT NULL AND film_simulation != ''
        GROUP BY sensor, film_simulation
    """
    df_sensors = pd.read_sql_query(query_sensors, conn)
    
    # Get top sim for each sensor
    for sensor in ['X-Trans IV', 'X-Trans V']:
        print(f"\n### Top 3 for {sensor}")
        top = df_sensors[df_sensors['sensor'] == sensor].sort_values('count', ascending=False).head(3)
        print(top[['film_simulation', 'count']].to_markdown(index=False))

    # 3. White Balance Trends (Are we getting warmer?)
    print("\n## Color Grading Trends")
    query_wb = """
        SELECT 
            AVG(wb_shift_red) as avg_red, 
            AVG(wb_shift_blue) as avg_blue 
        FROM recipes 
        WHERE wb_shift_red IS NOT NULL
    """
    df_wb = pd.read_sql_query(query_wb, conn)
    print(f"Average WB Shift: Red {df_wb.iloc[0]['avg_red']:.2f}, Blue {df_wb.iloc[0]['avg_blue']:.2f}")
    if df_wb.iloc[0]['avg_red'] > 0 and df_wb.iloc[0]['avg_blue'] < 0:
        print("Analysis: There is a strong trend towards 'Warmer' tones (positive Red, negative Blue).")

    conn.close()

if __name__ == "__main__":
    analyze_trends()
