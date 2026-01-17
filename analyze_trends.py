import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "film_recipes.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def analyze_trends():
    conn = get_connection()
    
    # 1. Top Film Simulation Bases - Bar Chart
    print("Generating images/top_simulations.png...")
    query_sims = """
        SELECT film_simulation, COUNT(*) as count 
        FROM recipes 
        WHERE film_simulation IS NOT NULL AND film_simulation != ''
        GROUP BY film_simulation 
        ORDER BY count DESC 
        LIMIT 7
    """
    df_sims = pd.read_sql_query(query_sims, conn)
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(df_sims['film_simulation'], df_sims['count'], color='#4a90e2')
    plt.title('Top Film Simulation Recipes', fontsize=16)
    plt.xlabel('Simulation Base', fontsize=12)
    plt.ylabel('Number of Recipes', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('images/top_simulations.png')
    plt.close()

    # 3. White Balance Trends - Scatter Plot
    print("Generating images/wb_trends.png...")
    query_wb_all = """
        SELECT wb_shift_red, wb_shift_blue 
        FROM recipes 
        WHERE wb_shift_red IS NOT NULL AND wb_shift_blue IS NOT NULL
    """
    df_wb_all = pd.read_sql_query(query_wb_all, conn)
    
    plt.figure(figsize=(8, 8))
    plt.scatter(df_wb_all['wb_shift_blue'], df_wb_all['wb_shift_red'], alpha=0.6, c='orange', edgecolors='k')
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    plt.axvline(0, color='gray', linestyle='--', linewidth=0.8)
    plt.title('Color Grading Preferences (WB Shift)', fontsize=16)
    plt.xlabel('Blue Shift (Cool <-> Warm)', fontsize=12)
    plt.ylabel('Red Shift (Green <-> Magenta)', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # Annotate quadrants
    plt.text(5, 5, 'Warm/Vintage', fontsize=12, color='red', ha='center')
    plt.text(-5, -5, 'Cool/Modern', fontsize=12, color='blue', ha='center')
    
    plt.tight_layout()
    plt.savefig('images/wb_trends.png')
    plt.close()

    conn.close()

if __name__ == "__main__":
    analyze_trends()
