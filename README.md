# Fujifilm X100V & X100VI Recipe Analysis

A data-driven deep dive into the most popular film simulation recipes used by the **Fujifilm X100V** and **X100VI** community.

## Data Analysis & Trends
This project analyzes over 240 film simulation recipes. Below are the key findings on how photographers are styling their Fuji cameras.

---

| **Dynamic Range** | **DR400** | Preserves highlight roll-off. Essential for that "analog" inability to blow out skies. |
| **Highlights** | **+0.5** | A slight boost to keep images punchy without losing detail. |
| **Shadows** | **+1.0** | Adds contrast and depth, avoiding the flat "HDR" look of modern smartphones. |
| **Color** | **+1.0** | Compensates for Classic Chrome's natural desaturation, bringing life back to skin tones. |
| **Noise Reduction** | **-4** | **CRITICAL**. Fuji's default NR smears detail. -4 ensures organic, grain-like noise structure. |
| **Sharpening** | **-1** | Digital sharpening looks artificial. -1 allows the lens character to shine. |
| **Clarity** | **-2** | Acts as a "Mist Filter". It softens local micro-contrast for a dreamy, less clinical vibe. **⚠️ Note: Causes ~1 sec storage delay.** |
| **Grain Effect** | **Strong, Small** | Textural grounding. It breaks up digital gradient banding and adds tactile "bite". |
| **Color Chrome Effect** | **Strong** | Deepens luminance in highly saturated colors (like flowers or skies) for richer tonality. |
| **Color Chrome FX Blue** | **Weak** | Adds a subtle depth to blue skies without making them look radioactive. |
| **White Balance** | **Auto, 0 R & -2 B** | The "Golden Warmth". Shifting away from Blue creates a permanent "afternoon light" feel. |

> [!CAUTION]
> **Performance Warning:** This recipe uses **Clarity -2**, which forces the camera to pause for ~1 second after every shot to process the image.
>
> **For Street/Action Photography:** Change **Clarity to 0**. You lose the "dreamy" softness, but the camera becomes instant again.
>
> 💡 **Pro Tip (Hardware Fix):**
> To get the dreamy look *without* the lag, use a **PolarPro Mist Filter** (e.g., Shortstache Everyday Filter). This optical glass adds the "bloom" and mist effect instantly, while also cutting UV haze, letting you shoot at **fps speeds**.

---

### 1. Most Popular Film Simulations
**Classic Chrome** (14 recipes) and **Classic Negative** (13 recipes) are the undisputed kings, accounting for the vast majority of usage.

**Technical Analysis**: Why these two?
- **Classic Chrome**: Mimics Kodachrome. It feels "journalistic" because it separates color intensity from luminance, giving a mature, understated look.
- **Classic Negative**: Mimics Superia 200/400. It introduces cyan shifts in shadows and hard contrast, offering a "street photography" grit that standard profiles lack.
- **Trend**: We see a shift away from standard "Provia/Standard" because users buy Fuji specifically *not* to look accurate, but to look *interpretive*.

![Top Simulations](images/top_simulations.png)

---

### 2. Color Behavior (White Balance Shift)
The data shows a massive preference for **Warm/Vintage** tones.

**How to read this chart:**
*   **The Orange Zone (Top-Left):** This is the "Golden Hour" zone. Most recipes fall here because shifting AWAY from Blue (towards Yellow) and TOWARDS Red creates a nostalgic, afternoon-sun look.
*   **The Blue Zone (Bottom-Right):** This is the "Modern/Clean" zone. Very few recipes aim for this cold, clinical look.
*   **The Center:** This is neutral/accurate color. Notice how few dots are actually in the center? Nobody buys a Fuji for accuracy; they buy it for *character*.

![WB Trends](images/wb_trends.png)

---

### 3. Dynamic Range Preferences
**DR400** is the dominant setting.

**Technical Analysis**:
- **Highlight Roll-off**: DR400 forces the camera to underexpose the RAW file by 2 stops and push the shadows digitally. This preserves 2 extra stops of highlight data.
- **Why it matters**: Film handles overexposure gracefully; Digital sensors clip to pure white instantly. DR400 is the most effective tool to mimic film's graceful highlight handling, preventing the dreaded "digital white clipped sky".
![Dynamic Range](images/dr_usage.png)

---

### 4. Grain Effect
**Strong** grain is the overwhelming favorite.

**Technical Analysis**:
- **Texture vs. Noise**: In the film days, grain was an unavoidable defect. Today, it is a creative choice. "Strong" grain masks the clinical perfection of modern high-resolution sensors (26MP/40MP).
- **Perceived Sharpness**: Paradoxically, grain can make an image feel "sharper" or more detailed because the random noise pattern adds high-frequency texture that our brains interpret as detail.
![Grain Usage](images/grain_usage.png)

---

### 5. ISO Limits
The community generally accepts high ISOs to simulate film grain naturally, with **ISO 6400** being the most common auto-limit.

![ISO Limit](images/iso_limit.png)

---

### 6. Sensor Distribution
![Sensor Distribution](images/sensor_distribution.png)

---

### 7. The "Community Standard" Recipe
By averaging all settings (Highlights, Shadows, Color, etc.), we can visualize the "default" preference of the community.
- **Highlights/Shadows**: Generally negative (softer contrast).
- **Color**: Slightly positive (vibrant).
- **Sharpness/NR**: Negative (softer, organic look).
![Average Preferences](images/average_preferences.png)

---

### 8. Clarity Settings
The distribution skews heavily towards **Negative Clarity**.

**Technical Analysis**:
- **The "Mist Filter" Effect**: Clarity affects mid-tone contrast using a large radius unsharp mask. Negative clarity bleeds highlights into shadows, creating a "bloom" effect similar to a ProMist diffusion filter.
- **The Trade-off**: High positive clarity looks like "HDR" (gritty, harsh). Negative clarity looks like "Cinema" (soft, dreamy). Users clearly prefer the cinematic look, accepting the 1-second processing delay required to save clarity files.
![Clarity Distribution](images/clarity_dist.png)

---

### 9. Color Chrome vs. Saturation correlation
Do users who use "Strong" Chrome Effect compensate with higher color saturation? The scatter plot below reveals the relationship.

![Chrome vs Color](images/chrome_color_corr.png)

---


## Overview
A Python tool to collect and organize film simulation recipes for Fujifilm cameras from public sources into a local SQLite database.

## Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/niteeshkanungo/fujisims.git
   cd fujisims
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. **Run the scraper**:
   ```bash
   python scrape.py
   ```
   This will populate `film_recipes.db`.


## Querying the Data
   Use the provided example script:
   ```bash
   python query_examples.py
   ```
   Or use any SQLite client:
   ```bash
   sqlite3 film_recipes.db "SELECT * FROM recipes LIMIT 1;"
   ```

## Database Schema
- `name`: Recipe Title
- `sensor`: Sensor Generation (e.g., X-Trans V)
- `film_simulation`: Base Film Simulation
- `wb_shift_red` / `wb_shift_blue`: White Balance adjustments
- ... and more.

## License
MIT
