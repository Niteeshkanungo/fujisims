import matplotlib.pyplot as plt
import pandas as pd

# Data for the Nishti Recipe
data = {
    "Setting": [
        "Film Simulation", "Dynamic Range", "Highlights", "Shadows", 
        "Color", "Exposure Comp.", "Noise Reduction", "Sharpening", 
        "Clarity", "Grain Effect", "Color Chrome", "Chrome FX Blue", "White Balance"
    ],
    "Value": [
        "Classic Chrome", "DR400", "-2", "-2", 
        "+2", "+1.0", "-2", "+1", 
        "-2", "Weak, Small", "Strong", "Weak", "Auto, -1R -3B"
    ],
    "The Logic": [
        "The foundation", "Saves the sky", "Softens glare", "Moody lift",
        "Punchy color", "Bright & Airy", "Clean texture", "Crisp edges",
        "Dreamy bloom", "Analog grain", "Deep shades", "Royal skies", "Cinematic cool"
    ]
}

df = pd.DataFrame(data)

# Styling the table
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')
ax.axis('tight')

table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='left', loc='center')

# Modern styling
table.auto_set_font_size(False)
table.set_fontsize(13)
table.scale(1.2, 2.5)

# Header styling
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold', color='white')
        cell.set_facecolor('#2c3e50')
    else:
        cell.set_facecolor('#f8f9fa' if row % 2 == 0 else 'white')
    cell.set_edgecolor('#dddddd')

plt.title("THE NISHTI RECIPE: Community Consensus Configuration", 
          fontsize=18, fontweight='bold', pad=20, color='#2c3e50')

plt.savefig('images/nishti_recipe_table.png', dpi=300, bbox_inches='tight', transparent=False)
print("Generated images/nishti_recipe_table.png")
