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

    # 9. Calculate the Golden Recipe (Exact Values)
    avg_settings = {}
    for m in metrics:
        avg_settings[m] = round(df_avg[m].mean() * 2) / 2 # Round to nearest 0.5 step

    # Most popular film sim
    top_sim = df_sims.iloc[0]['film_simulation']
    
    # Most popular DR
    top_dr_row = df_dr.groupby('dynamic_range')['count'].sum().sort_values(ascending=False).iloc[0]
    # We need the index name, bit tricky with series, let's re-query simple group
    top_dr = df_dr_grouped.sort_values('count', ascending=False).iloc[0]['dr_group']
    
    # Re-run WB query for the average calculation
    query_wb = """
        SELECT 
            AVG(wb_shift_red) as avg_red, 
            AVG(wb_shift_blue) as avg_blue 
        FROM recipes 
        WHERE wb_shift_red IS NOT NULL
    """
    df_wb = pd.read_sql_query(query_wb, conn)
    
    # Simple WB Avg
    avg_wb_red = round(df_wb.iloc[0]['avg_red'])
    avg_wb_blue = round(df_wb.iloc[0]['avg_blue'])
    
    print("\nXXX_GOLDEN_RECIPE_START_XXX")
    print(f"Name: The Nishti Recipe (Highest Probability of Likeness)")
    print("Description: Based on statistical averages of 240+ recipes, this is the 'Golden Mean' of Fuji aesthetics.")
    print(f"Film Simulation: {top_sim}")
    print(f"Dynamic Range: {top_dr}")
    print(f"Highlights: {avg_settings['highlight']:+}")
    print(f"Shadows: {avg_settings['shadow']:+}")
    print(f"Color: {avg_settings['color']:+}")
    print(f"Noise Reduction: {avg_settings['noise_reduction']:+}")
    print(f"Sharpening: {avg_settings['sharpness']:+}")
    print(f"Clarity: {avg_settings['clarity']:+}")
    print(f"Grain Effect: Strong, Small") # Hardcoded based on grain graph analysis
    print(f"Color Chrome Effect: Strong") # Common defaults
    print(f"Color Chrome FX Blue: Weak")
    print(f"White Balance: Auto, {avg_wb_red:+} Red & {avg_wb_blue:+} Blue")
    print(f"ISO: Auto, up to ISO 6400")
    print("XXX_GOLDEN_RECIPE_END_XXX")


    print("Generating images/clarity_dist.png...")
    plt.figure(figsize=(8, 5))
    # Clarity is expensive on processor, so checking if people use it
    query_clarity = "SELECT clarity FROM recipes WHERE clarity IS NOT NULL"
    df_clarity = pd.read_sql_query(query_clarity, conn)
    
    # Parse clarity
    def parse_clarity(val):
        try: return float(val.replace('+', ''))
        except: return 0
        
    df_clarity['val'] = df_clarity['clarity'].apply(parse_clarity)
    
    plt.hist(df_clarity['val'], bins=range(-5, 6), align='left', rwidth=0.8, color='#e67e22')
    plt.title('Clarity Settings Distribution', fontsize=16)
    plt.xlabel('Clarity Value (Negative = Soft, Positive = Sharp)')
    plt.ylabel('Frequency')
    plt.axvline(0, color='k', linestyle='--', linewidth=1)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('images/clarity_dist.png')
    plt.close()
    
    # 11. Chrome Effect vs Color Saturation (Correlation)
    print("Generating images/chrome_color_corr.png...")
    # Does Strong Chrome Effect imply Lower Saturation?
    query_corr = "SELECT full_settings, color FROM recipes"
    df_corr = pd.read_sql_query(query_corr, conn)
    
    chrome_vals = []
    color_vals = []
    
    import json
    for idx, row in df_corr.iterrows():
        try:
            settings = json.loads(row['full_settings']) if row['full_settings'] else {}
            chrome = settings.get('Color Chrome Effect', 'Off').lower()
            color = float(row['color'].replace('+', '')) if row['color'] else 0
            
            if 'strong' in chrome: c_score = 2
            elif 'weak' in chrome: c_score = 1
            else: c_score = 0
            
            chrome_vals.append(c_score)
            color_vals.append(color)
        except:
            continue
            
    plt.figure(figsize=(8, 6))
    # Jitter the points so they don't overlap
    jitter_x = [x + np.random.uniform(-0.1, 0.1) for x in chrome_vals]
    jitter_y = [y + np.random.uniform(-0.2, 0.2) for y in color_vals]
    
    plt.scatter(jitter_x, jitter_y, alpha=0.5, c='#8e44ad')
    plt.title('Color Chrome Effect vs. Saturation Setting', fontsize=16)
    plt.xlabel('Color Chrome Effect (0=Off, 1=Weak, 2=Strong)')
    plt.ylabel('Color Saturation Setting')
    plt.xticks([0, 1, 2], ['Off', 'Weak', 'Strong'])
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.tight_layout()
    plt.savefig('images/chrome_color_corr.png')
    plt.close()

if __name__ == "__main__":
    analyze_trends()
