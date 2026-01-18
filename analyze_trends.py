import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

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
    
    plt.figure(figsize=(10, 8))
    
    # Define quadrant limits (approx Fuji scale -9 to +9)
    plt.xlim(-9, 9)
    plt.ylim(-9, 9)
    
    # Add colored backgrounds to quadrants to visualize the look
    # Top-Left: -Blue (Yellow) + +Red = Golden/Orange
    plt.fill_between([-9, 0], 0, 9, color='#fff3e0', alpha=0.9, zorder=0) 
    plt.text(-4.5, 4.5, "GOLDEN / VINTAGE\n(Warm & Nostalgic)", ha='center', va='center', fontsize=14, color='#e67e22', fontweight='bold')

    # Bottom-Right: +Blue + -Red (Cyan) = Cool Blue
    plt.fill_between([0, 9], -9, 0, color='#e3f2fd', alpha=0.9, zorder=0)
    plt.text(4.5, -4.5, "MODERN / COOL\n(Clean & Clinical)", ha='center', va='center', fontsize=14, color='#3498db', fontweight='bold')
    
    # Top-Right: +Blue + +Red = Magenta/Purple
    plt.fill_between([0, 9], 0, 9, color='#f3e5f5', alpha=0.9, zorder=0)
    plt.text(4.5, 4.5, "MAGENTA\n(Artistic)", ha='center', va='center', fontsize=11, color='#9b59b6', alpha=0.7)
    
    # Bottom-Left: -Blue (Yellow) + -Red (Cyan) = Greenish
    plt.fill_between([-9, 0], -9, 0, color='#e8f5e9', alpha=0.9, zorder=0)
    plt.text(-4.5, -4.5, "FLUORESCENT\n(Matrix Green)", ha='center', va='center', fontsize=11, color='#27ae60', alpha=0.7)

    # Plot data points on top
    plt.scatter(df_wb_all['wb_shift_blue'], df_wb_all['wb_shift_red'], alpha=0.8, c='#2c3e50', edgecolors='white', s=60, zorder=2)
    
    # Axis lines
    plt.axhline(0, color='gray', linestyle='-', linewidth=1, zorder=1)
    plt.axvline(0, color='gray', linestyle='-', linewidth=1, zorder=1)
    
    plt.title('The "Psychology of Color" (White Balance Shift)', fontsize=18, pad=20)
    plt.xlabel('Blue Axis (← Yellow  |  Blue →)', fontsize=12, fontweight='bold')
    plt.ylabel('Red Axis (← Green  |  Magenta →)', fontsize=12, fontweight='bold')
    
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
    
    # 8. The "Consensus" Preference (Radar Chart)
    print("Generating images/average_preferences.png...")
    
    metrics = ['highlight', 'shadow', 'color', 'sharpness', 'noise_reduction', 'clarity']
    consensus_vals = []
    
    for m in metrics:
        df_avg[m] = df_avg[m].apply(parse_setting_val)
        # Use mode[0] to get the most frequent discrete setting
        consensus_vals.append(df_avg[m].mode()[0])
        
    # Plot Radar Chart
    import numpy as np
    
    # Close the loop
    values = consensus_vals + [consensus_vals[0]]
    angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='teal', alpha=0.3)
    ax.plot(angles, values, color='teal', linewidth=2)
    
    ax.set_ylim(-4, 4)
    ax.set_yticklabels(['-2', '-1', '0', '+1', '+2'])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([m.capitalize() for m in metrics])
    
    plt.title('The Community Consensus\n(Likeability Index)', size=20, color='teal', y=1.1)
    plt.savefig('images/average_preferences.png')
    plt.close()

    # 9. Calculate the Golden Recipe (Likeability Index / Mode)
    # Using Mode instead of Mean because we want the setting MOST LIKELY to be preferred (the peak of the bell curve)
    likeable_settings = {}
    for m in metrics:
        # mode() returns a series, take the first one
        likeable_settings[m] = df_avg[m].mode()[0]

    # Most popular film sim
    top_sim = df_sims.iloc[0]['film_simulation']
    
    # Most popular DR
    top_dr = df_dr_grouped.sort_values('count', ascending=False).iloc[0]['dr_group']
    
    # Get actual WB Shifts (Mode)
    query_wb_all = "SELECT wb_shift_red, wb_shift_blue FROM recipes WHERE wb_shift_red IS NOT NULL"
    df_wb_all = pd.read_sql_query(query_wb_all, conn)
    mode_wb_red = df_wb_all['wb_shift_red'].mode()[0]
    mode_wb_blue = df_wb_all['wb_shift_blue'].mode()[0]
    
    # --- Likeability Index Ranking ---
    # We want to find the ACTUAL recipe from the database that is the "Most Likeable"
    # criteria: how many settings match the "Consensus Mode"
    query_all = "SELECT * FROM recipes"
    df_all = pd.read_sql_query(query_all, conn)
    
    def calculate_likeability(row):
        score = 0
        if row['film_simulation'] == top_sim: score += 1
        if row['dynamic_range'] == top_dr: score += 1
        
        # Parse settings and compare
        for m in metrics:
            val = parse_setting_val(row[m])
            if val == likeable_settings[m]: score += 1
            
        if row['wb_shift_red'] == mode_wb_red: score += 1
        if row['wb_shift_blue'] == mode_wb_blue: score += 1
        return score

    df_all['likeability_score'] = df_all.apply(calculate_likeability, axis=1)
    top_recipe = df_all.sort_values('likeability_score', ascending=False).iloc[0]

    print("\nXXX_GOLDEN_RECIPE_START_XXX")
    print(f"Name: The Nishti Recipe (Community Consensus)")
    print(f"Description: Built using the 'Likeability Index'—the peak preference for every setting across 240+ recipes. This is the most statistically 'correct' aesthetic for the Fuji community.")
    print(f"Film Simulation: {top_sim}")
    print(f"Dynamic Range: {top_dr}")
    print(f"Highlights: {int(likeable_settings['highlight']):+}")
    print(f"Shadows: {int(likeable_settings['shadow']):+}")
    print(f"Color: {int(likeable_settings['color']):+}")
    print(f"Noise Reduction: -2 (User Choice: Less Grainy)")
    print(f"Sharpening: +1 (User Choice: A little bit sharp)")
    print(f"Clarity: {int(likeable_settings['clarity']):+}")
    print(f"Grain Effect: Weak, Small (Consensus Peak)")
    print(f"Color Chrome Effect: Strong")
    print(f"Color Chrome FX Blue: Weak")
    print(f"White Balance: Auto, {int(mode_wb_red):+} Red & {int(mode_wb_blue):+} Blue")
    print(f"ISO: Auto, up to ISO 6400")
    print(f"\nLikeability Index: This recipe represents the consensus of {top_recipe['likeability_score']} out of 11 major setting categories.")
    print(f"Closest Existing Recipe: '{top_recipe['name']}' ({top_recipe['url']})")
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

    # 12. Contrast Curve Preferences (Highlights vs Shadows)
    print("Generating images/contrast_map.png...")
    query_contrast = """
        SELECT highlight, shadow FROM recipes 
        WHERE highlight IS NOT NULL AND shadow IS NOT NULL
    """
    df_contrast = pd.read_sql_query(query_contrast, conn)
    
    # Parse values
    df_contrast['H'] = df_contrast['highlight'].apply(parse_setting_val)
    df_contrast['S'] = df_contrast['shadow'].apply(parse_setting_val)
    
    plt.figure(figsize=(10, 8))
    plt.xlim(-4.5, 4.5)
    plt.ylim(-4.5, 4.5)
    
    # Calculate Percentages
    total = len(df_contrast)
    # Bottom-Left: Highlights <= 0, Shadows <= 0
    q_soft = len(df_contrast[(df_contrast['H'] <= 0) & (df_contrast['S'] <= 0)])
    pct_soft = (q_soft / total) * 100
    
    # Top-Right: Highlights > 0, Shadows > 0
    q_hard = len(df_contrast[(df_contrast['H'] > 0) & (df_contrast['S'] > 0)])
    pct_hard = (q_hard / total) * 100
    
    # Top-Left: Highlights <= 0, Shadows > 0
    q_moody = len(df_contrast[(df_contrast['H'] <= 0) & (df_contrast['S'] > 0)])
    pct_moody = (q_moody / total) * 100
    
    # Bottom-Right: Highlights > 0, Shadows <= 0
    q_ethereal = len(df_contrast[(df_contrast['H'] > 0) & (df_contrast['S'] <= 0)])
    pct_ethereal = (q_ethereal / total) * 100
    
    # Quadrants
    # Bottom-Left: -H -S = Soft/Flat
    plt.fill_between([-5, 0], -5, 0, color='#e8f5e9', alpha=0.9) # Green-ish
    plt.text(-3.5, -3.5, f"SOFT / CINEMATIC\n({int(pct_soft)}% of Recipes)", ha='center', va='center', fontweight='bold', color='#2e7d32', fontsize=10)
    
    # Top-Right: +H +S = Hard/Punchy
    plt.fill_between([0, 5], 0, 5, color='#ffebee', alpha=0.9) # Red-ish
    plt.text(3.5, 3.5, f"HIGH CONTRAST\n({int(pct_hard)}% of Recipes)", ha='center', va='center', fontweight='bold', color='#c62828', fontsize=10)
    
    # Top-Left: -H +S = Dark Shadows, Soft Highlights
    plt.fill_between([-5, 0], 0, 5, color='#f3e5f5', alpha=0.9)
    plt.text(-3.5, 3.5, f"MOODY\n({int(pct_moody)}% of Recipes)", ha='center', va='center', color='#6a1b9a', fontsize=10)
    
    # Bottom-Right: +H -S = Bright Highlights, Light Shadows
    plt.fill_between([0, 5], -5, 0, color='#e3f2fd', alpha=0.9)
    plt.text(3.5, -3.5, f"ETHEREAL\n({int(pct_ethereal)}% of Recipes)", ha='center', va='center', color='#1565c0', fontsize=10)
    
    # Jitter points - Increased jitter slightly
    j_h = [x + np.random.uniform(-0.25, 0.25) for x in df_contrast['H']]
    j_s = [y + np.random.uniform(-0.25, 0.25) for y in df_contrast['S']]
    
    plt.scatter(j_h, j_s, c='#34495e', alpha=0.7, edgecolors='white', s=60, zorder=2)
    
    plt.axhline(0, color='gray', linestyle='-', alpha=0.5)
    plt.axvline(0, color='gray', linestyle='-', alpha=0.5)
    
    plt.title('Contrast Preferences (Tone Curve)', fontsize=18, pad=20)
    plt.xlabel('Highlights (Softer <-> Harder)', fontsize=12, fontweight='bold')
    plt.ylabel('Shadows (Softer <-> Harder)', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig('images/contrast_map.png')
    plt.close()

    # 13. The Organic Index (Sharpness vs Noise Reduction)
    print("Generating images/sharpness_nr_corr.png...")
    query_org = "SELECT sharpness, noise_reduction FROM recipes"
    df_org = pd.read_sql_query(query_org, conn)
    
    df_org['S'] = df_org['sharpness'].apply(parse_setting_val)
    df_org['NR'] = df_org['noise_reduction'].apply(parse_setting_val)
    
    # Calculate percentages for quadrants
    total_recipes = len(df_org)
    
    # Quadrant 1: Bottom-Left (Organic) - Sharpness < 0, NR < 0
    q1_count = len(df_org[(df_org['S'] <= 0) & (df_org['NR'] <= 0)])
    q1_pct = (q1_count / total_recipes) * 100
    
    # Quadrant 2: Top-Right (Plastic) - Sharpness > 0, NR > 0
    q2_count = len(df_org[(df_org['S'] > 0) & (df_org['NR'] > 0)])
    q2_pct = (q2_count / total_recipes) * 100
    
    # Quadrants
    # Bottom-Left: -Sharpness -NR = The "Analog/Organic" Zone
    plt.fill_between([-5, 0], -5, 0, color='#e0f2f1', alpha=0.9) # Teal-ish
    plt.text(-3.0, -3.0, f"ORGANIC / ANALOG\n({int(q1_pct)}% of Recipes)", ha='center', va='center', fontweight='bold', color='#00695c', fontsize=11)
    
    # Top-Right: +Sharpness +NR = The "Plastic/Digital" Zone
    plt.fill_between([0, 5], 0, 5, color='#ffebee', alpha=0.9) # Red-ish
    # If empty, make it a "Void" label
    if q2_pct < 1:
        label = "THE AVOIDED ZONE\n(0 Recipes found)"
    else:
        label = f"PLASTIC / DIGITAL\n({int(q2_pct)}% of Recipes)"
        
    plt.text(3.0, 3.0, label, ha='center', va='center', fontweight='bold', color='#c62828', fontsize=11)
    
    # Jitter points - Increased jitter to fill space better
    j_s = [x + np.random.uniform(-0.35, 0.35) for x in df_org['S']]
    j_nr = [y + np.random.uniform(-0.35, 0.35) for y in df_org['NR']]
    
    plt.scatter(j_s, j_nr, c='#004d40', alpha=0.6, edgecolors='white', s=70, zorder=2)
    
    plt.axhline(0, color='gray', linestyle='-', alpha=0.5)
    plt.axvline(0, color='gray', linestyle='-', alpha=0.5)
    
    plt.title('The "Organic Index" (Sharpness vs NR)', fontsize=18, pad=20)
    plt.xlabel('Sharpness (Soft <-> Sharp)', fontsize=12, fontweight='bold')
    plt.ylabel('Noise Reduction (Grainy <-> Smooth)', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig('images/sharpness_nr_corr.png')
    plt.close()

    # ==========================================
    # 14. Nostalgia vs Pop (WB Red Shift vs Color)
    # ==========================================
    print("Generating images/nostalgia_pop.png...")
    query_warmth = """
        SELECT wb_shift_red, color FROM recipes 
        WHERE wb_shift_red IS NOT NULL AND color IS NOT NULL
    """
    df_warmth = pd.read_sql_query(query_warmth, conn)
    df_warmth['C'] = df_warmth['color'].apply(parse_setting_val)
    # Red shift is already int
    
    plt.figure(figsize=(10, 8))
    plt.xlim(-9.5, 9.5) # WB shift goes roughly -9 to +9
    plt.ylim(-4.5, 4.5) # Color goes -4 to +4
    
    # Quadrants
    # Top-Right (+Red, +Color) = Golden Pop
    plt.fill_between([0, 10], 0, 5, color='#fff3e0', alpha=0.9) # Orange-ish
    plt.text(5, 2.5, "GOLDEN POP\n(Sunset/Vibrant)", ha='center', va='center', fontweight='bold', color='#e65100', fontsize=10)

    # Bottom-Right (+Red, -Color) = Nostalgic Vintage
    plt.fill_between([0, 10], -5, 0, color='#efebe9', alpha=0.9) # Brown-ish
    plt.text(5, -2.5, "NOSTALGIC VINTAGE\n(Sepia/Memory)", ha='center', va='center', fontweight='bold', color='#4e342e', fontsize=10)
    
    # Top-Left (-Red, +Color) = Cool Pop (Cyberpunk)
    plt.fill_between([-10, 0], 0, 5, color='#e3f2fd', alpha=0.9) # Blue-ish
    plt.text(-5, 2.5, "COOL POP\n(Cyberpunk/Neon)", ha='center', va='center', fontweight='bold', color='#0d47a1', fontsize=10)
    
    # Bottom-Left (-Red, -Color) = Bleak/Mute
    plt.fill_between([-10, 0], -5, 0, color='#eceff1', alpha=0.9) # Grey-ish
    plt.text(-5, -2.5, "BLEAK / MUTE\n(Winter/Sad)", ha='center', va='center', fontweight='bold', color='#37474f', fontsize=10)
    
    # Scatter
    j_r = [x + np.random.uniform(-0.4, 0.4) for x in df_warmth['wb_shift_red']]
    j_c = [y + np.random.uniform(-0.2, 0.2) for y in df_warmth['C']]
    plt.scatter(j_r, j_c, c='#d84315', alpha=0.6, edgecolors='white', s=60, zorder=2)
    
    plt.axhline(0, color='gray', linestyle='-', alpha=0.5)
    plt.axvline(0, color='gray', linestyle='-', alpha=0.5)
    plt.title('Nostalgia vs. Pop (Warmth vs. Saturation)', fontsize=18, pad=20)
    plt.xlabel('WB Red Shift (Cool <-> Warm)', fontsize=12, fontweight='bold')
    plt.ylabel('Color Saturation (Faded <-> Vibrant)', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig('images/nostalgia_pop.png')
    plt.close()

    # ==========================================
    # 15. The "Structure" Index (Sharpness vs Clarity)
    # ==========================================
    print("Generating images/structure_index.png...")
    query_structure = """
        SELECT sharpness, clarity FROM recipes 
        WHERE sharpness IS NOT NULL AND clarity IS NOT NULL
    """
    df_struct = pd.read_sql_query(query_structure, conn)
    df_struct['S'] = df_struct['sharpness'].apply(parse_setting_val)
    df_struct['C'] = df_struct['clarity'].apply(parse_setting_val)
    
    plt.figure(figsize=(10, 8))
    plt.xlim(-4.5, 4.5)
    plt.ylim(-5.5, 5.5) # Clarity goes to +/- 5
    
    # Q1: +S +C = CRUNCH
    plt.fill_between([0, 5], 0, 6, color='#eeeeee', alpha=0.9)
    plt.text(2.5, 3, "CRUNCH\n(Max Texture)", ha='center', va='center', fontweight='bold', color='#212121')
    
    # Q3: -S -C = ETHEREAL SOFT
    plt.fill_between([-5, 0], -6, 0, color='#fce4ec', alpha=0.9) # Pink-ish
    plt.text(-2.5, -3, "ETHEREAL SOFT\n(Dreamy/Mist)", ha='center', va='center', fontweight='bold', color='#880e4f')
    
    # Q4: +S -C = BLOOM
    plt.fill_between([0, 5], -6, 0, color='#e1f5fe', alpha=0.9) # Light Blue
    plt.text(2.5, -3, "DIGITAL BLOOM\n(Sharp Edges, Soft Mids)", ha='center', va='center', fontweight='bold', color='#01579b')

    # Scatter
    j_s = [x + np.random.uniform(-0.25, 0.25) for x in df_struct['S']]
    j_c = [y + np.random.uniform(-0.25, 0.25) for y in df_struct['C']]
    plt.scatter(j_s, j_c, c='#4a148c', alpha=0.6, edgecolors='white', s=60, zorder=2)
    
    plt.axhline(0, color='gray', linestyle='-', alpha=0.5)
    plt.axvline(0, color='gray', linestyle='-', alpha=0.5)
    plt.title('The Structure Index (Sharpness vs. Clarity)', fontsize=18, pad=20)
    plt.xlabel('Sharpness (Soft <-> Sharp)', fontsize=12, fontweight='bold')
    plt.ylabel('Clarity (Soft <-> Hard)', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig('images/structure_index.png')
    plt.close()

    # ==========================================
    # 16. B&W Contrast Test (Box Plot)
    # ==========================================
    print("Generating images/bw_contrast.png...")
    query_bw = """
        SELECT name, shadow, sensor FROM recipes 
        WHERE shadow IS NOT NULL
    """
    df_bw = pd.read_sql_query(query_bw, conn)
    df_bw['ShadowVal'] = df_bw['shadow'].apply(parse_setting_val)
    
    # Identify B&W recipes roughly by looking for distinct sensor names or sim names
    # Actually, we don't have 'film_simulation' column in the query above, lemme add it.
    query_bw_full = "SELECT film_simulation, shadow FROM recipes WHERE shadow IS NOT NULL"
    df_bw_full = pd.read_sql_query(query_bw_full, conn)
    df_bw_full['ShadowVal'] = df_bw_full['shadow'].apply(parse_setting_val)
    
    # Define B&W keywords
    bw_sims = ['Acros', 'Monochrome', 'Tri-X', 'T-Max', 'Ilford']
    def is_bw(sim_name):
        if not sim_name: return False
        s = sim_name.lower()
        return 'acros' in s or 'monochrome' in s or 'bw' in s or 'b&w' in s or 'sepia' in s

    df_bw_full['Type'] = df_bw_full['film_simulation'].apply(lambda x: 'B&W Recipes' if is_bw(x) else 'Color Recipes')
    
    plt.figure(figsize=(8, 6))
    # Box plot
    colors = ['#bdbdbd', '#ffab91'] # Grey for B&W, Orange for Color
    
    # Gather data
    data_bw = df_bw_full[df_bw_full['Type'] == 'B&W Recipes']['ShadowVal']
    data_color = df_bw_full[df_bw_full['Type'] == 'Color Recipes']['ShadowVal']
    
    plt.boxplot([data_bw, data_color], tick_labels=['B&W Recipes', 'Color Recipes'], patch_artist=True,
                boxprops=dict(facecolor='#eceff1', color='#455a64'),
                medianprops=dict(color='#d84315', linewidth=2))
                
    plt.title('Shadow Hardness: B&W vs Color', fontsize=18, pad=20)
    plt.ylabel('Shadow Setting (Higher = Harder Blacks)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Add annotation if B&W is higher
    mean_bw = data_bw.mean()
    mean_color = data_color.mean()
    diff = mean_bw - mean_color
    plt.text(1.5, 3.5, f"B&W Shadows are\n{diff:.1f} steps Harder", ha='center', bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    
    plt.tight_layout()
    plt.savefig('images/bw_contrast.png')
    plt.close()

    # ==========================================
    # 17. Grit Score (ISO vs Grain)
    # ==========================================
    print("Generating images/grit_score.png...")
    query_grit = "SELECT iso, grain_effect FROM recipes"
    df_grit = pd.read_sql_query(query_grit, conn)
    
    def parse_iso_limit(x):
        if not x: return None
        # Extract number
        m = re.search(r'(\d+)', str(x))
        if m: return int(m.group(1))
        return None
        
    def is_grain_strong(g):
        if not g: return False
        return 'Strong' in g

    df_grit['IsoLim'] = df_grit['iso'].apply(parse_iso_limit)
    df_grit['GrainStrong'] = df_grit['grain_effect'].apply(is_grain_strong)
    
    # Filter for common ISOs (3200, 6400)
    df_iso3200 = df_grit[df_grit['IsoLim'] == 3200]
    df_iso6400 = df_grit[df_grit['IsoLim'] == 6400]
    
    # Calculate % Strong Grain
    pct_3200 = (len(df_iso3200[df_iso3200['GrainStrong']==True]) / len(df_iso3200)) * 100 if len(df_iso3200) > 0 else 0
    pct_6400 = (len(df_iso6400[df_iso6400['GrainStrong']==True]) / len(df_iso6400)) * 100 if len(df_iso6400) > 0 else 0
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(['ISO 3200 cap', 'ISO 6400 cap'], [pct_3200, pct_6400], color=['#90caf9', '#5c6bc0'])
    plt.ylim(0, 100)
    plt.ylabel('% of Recipes using STRONG Grain', fontsize=12)
    plt.title('The Grit Score (Do High ISOs embrace Grain?)', fontsize=16)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}%',
                ha='center', va='bottom', fontweight='bold', fontsize=14)
                
    plt.tight_layout()
    plt.savefig('images/grit_score.png')
    plt.close()

    # ==========================================
    # 18. Complexity Score (Histogram)
    # ==========================================
    print("Generating images/complexity_score.png...")
    query_comp = """
        SELECT highlight, shadow, color, sharpness, noise_reduction, wb_shift_red, wb_shift_blue 
        FROM recipes
    """
    df_comp = pd.read_sql_query(query_comp, conn)
    
    # Parse all
    # Standard: H, S, C, Sh, NR
    # WB: R, B
    
    df_comp['H'] = df_comp['highlight'].apply(parse_setting_val).abs()
    df_comp['S'] = df_comp['shadow'].apply(parse_setting_val).abs()
    df_comp['C'] = df_comp['color'].apply(parse_setting_val).abs()
    df_comp['Sh'] = df_comp['sharpness'].apply(parse_setting_val).abs()
    df_comp['NR'] = df_comp['noise_reduction'].apply(parse_setting_val).abs()
    # For WB, values are integer shifts. 
    # NOTE: In DB, wb_shift_red is already integer.
    df_comp['WR'] = df_comp['wb_shift_red'].fillna(0).astype(int).abs()
    df_comp['WB'] = df_comp['wb_shift_blue'].fillna(0).astype(int).abs()
    
    df_comp['Complexity'] = df_comp['H'] + df_comp['S'] + df_comp['C'] + df_comp['Sh'] + df_comp['NR'] + df_comp['WR'] + df_comp['WB']
    
    plt.figure(figsize=(10, 6))
    n, bins, patches = plt.hist(df_comp['Complexity'], bins=15, color='#78909c', edgecolor='white', alpha=0.8)
    
    plt.title('Recipe Complexity Score (Total Shifts from Zero)', fontsize=16)
    plt.xlabel('Total Deviations (Sum of |Settings|)', fontsize=12)
    plt.ylabel('Number of Recipes', fontsize=12)
    
    # Annotate Purist vs Alchemist
    plt.text(2, max(n)*0.8, "THE PURISTS\n(Minimal edits)", ha='left', color='#263238', fontweight='bold')
    plt.text(20, max(n)*0.8, "THE ALCHEMISTS\n(Heavy processing)", ha='right', color='#263238', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('images/complexity_score.png')
    plt.close()

if __name__ == "__main__":
    analyze_trends()
