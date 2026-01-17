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
    plt.text(5, 5, 'Warm/Vintage', fontsize=12, color='red', ha='center')
    plt.text(-5, -5, 'Cool/Modern', fontsize=12, color='blue', ha='center')
    plt.tight_layout()
    plt.savefig('images/wb_trends.png')
    plt.close()

    # 4. Dynamic Range Usage - Pie Chart
    print("Generating images/dr_usage.png...")
    query_dr = "SELECT dynamic_range, COUNT(*) as count FROM recipes WHERE dynamic_range IS NOT NULL GROUP BY dynamic_range"
    df_dr = pd.read_sql_query(query_dr, conn)
    
    # Simple cleanup to grouping main DR types
    def clean_dr(val):
        if '400' in val: return 'DR400'
        if '200' in val: return 'DR200'
        return 'DR100/Standard'
    
    df_dr['dr_group'] = df_dr['dynamic_range'].apply(clean_dr)
    df_dr_grouped = df_dr.groupby('dr_group')['count'].sum().reset_index()
    
    plt.figure(figsize=(7, 7))
    plt.pie(df_dr_grouped['count'], labels=df_dr_grouped['dr_group'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'])
    plt.title('Dynamic Range Preference', fontsize=16)
    plt.tight_layout()
    plt.savefig('images/dr_usage.png')
    plt.close()

    # 5. Grain Effect - Bar Chart
    print("Generating images/grain_usage.png...")
    query_grain = "SELECT grain_effect, COUNT(*) as count FROM recipes WHERE grain_effect IS NOT NULL GROUP BY grain_effect"
    df_grain = pd.read_sql_query(query_grain, conn)
    
    # Clean up grain values (e.g. "Strong, Large" -> "Strong")
    def clean_grain(val):
        val = val.lower()
        if 'strong' in val: return 'Strong'
        if 'weak' in val: return 'Weak'
        if 'off' in val: return 'Off'
        return 'Other'

    df_grain['grain_group'] = df_grain['grain_effect'].apply(clean_grain)
    df_grain_grouped = df_grain.groupby('grain_group')['count'].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(8, 5))
    df_grain_grouped.plot(kind='bar', color='gray', edgecolor='black')
    plt.title('Grain Effect Intensity', fontsize=16)
    plt.xlabel('Intensity')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('images/grain_usage.png')
    plt.close()

    # 6. ISO Limit Analysis - Bar Chart
    print("Generating images/iso_limit.png...")
    query_iso = "SELECT iso FROM recipes WHERE iso LIKE '%up to%'"
    df_iso = pd.read_sql_query(query_iso, conn)
    
    def extract_iso(val):
        # Extract number after "ISO"
        import re
        match = re.search(r'ISO\s+(\d+)', val)
        return match.group(1) if match else None

    df_iso['iso_limit'] = df_iso['iso'].apply(extract_iso)
    iso_counts = df_iso['iso_limit'].value_counts().sort_index()
    
    plt.figure(figsize=(8, 5))
    iso_counts.plot(kind='bar', color='#e74c3c')
    plt.title('Preferred Auto-ISO Limits', fontsize=16)
    plt.xlabel('ISO Limit')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('images/iso_limit.png')
    plt.close()

    # 7. Recipes by Sensor Generation
    print("Generating images/sensor_distribution.png...")
    query_sensor = "SELECT sensor, COUNT(*) as count FROM recipes GROUP BY sensor"
    df_sensor = pd.read_sql_query(query_sensor, conn)
    
    plt.figure(figsize=(8, 5))
    plt.bar(df_sensor['sensor'], df_sensor['count'], color='#8e44ad')
    plt.title('Recipes Per Sensor Generation', fontsize=16)
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('images/sensor_distribution.png')
    plt.close()

    # 8. The "Average" User Preference (Radar Chart)
    print("Generating images/average_preferences.png...")
    # Extract numerical values from text settings (e.g. "+2" -> 2, "-1" -> -1)
    
    # Helper to safe convert string to float
    def parse_setting_val(val):
        if val is None: return None
        try:
            # Handle "+1" or "-1" or "0"
            clean = val.replace('+', '').strip()
            # If range "0 to +2", take average? For now take first number found
            import re
            match = re.search(r'([+-]?\d+(?:\.\d+)?)', clean)
            if match:
                return float(match.group(1))
            return 0.0
        except:
            return 0.0

    query_avg = "SELECT highlight, shadow, color, sharpness, noise_reduction, clarity FROM recipes"
    df_avg = pd.read_sql_query(query_avg, conn)
    
    metrics = ['highlight', 'shadow', 'color', 'sharpness', 'noise_reduction', 'clarity']
    averages = []
    
    for m in metrics:
        df_avg[m] = df_avg[m].apply(parse_setting_val)
        averages.append(df_avg[m].mean())
        
    # Plot Radar Chart
    import numpy as np
    
    # Close the loop
    values = averages + [averages[0]]
    angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
    angles += [angles[0]]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='teal', alpha=0.25)
    ax.plot(angles, values, color='teal', linewidth=2)
    
    ax.set_yticks([-2, -1, 0, 1, 2])
    ax.set_yticklabels(['-2', '-1', '0', '+1', '+2'])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([m.capitalize() for m in metrics])
    
    plt.title('The "Average" Recipe Settings\n(Community Standard)', size=20, color='teal', y=1.1)
    plt.savefig('images/average_preferences.png')
    plt.close()


if __name__ == "__main__":
    analyze_trends()
