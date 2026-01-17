# Fujifilm X100V & X100VI Recipe Analysis

A data-driven deep dive into the most popular film simulation recipes used by the **Fujifilm X100V** and **X100VI** community.

## Data Analysis & Trends
This project analyzes over 240 film simulation recipes. Below are the key findings on how photographers are styling their Fuji cameras.

### 1. Most Popular Film Simulations
**Classic Chrome** and **Classic Negative** are the clear favorites, accounting for the majority of recipes.

![Top Simulations](images/top_simulations.png)

---

### 2. Color Behavior (White Balance Shift)
There is a massive preference for **Warm/Vintage** tones. The scatter plot below shows that most recipes shift Red positively (Green -> Magenta) and Blue negatively (Blue -> Yellow).

![WB Trends](images/wb_trends.png)

---

### 3. Dynamic Range Preferences
**DR400** is the dominant setting, used to preserve highlight detail in high-contrast "film" looks.

![Dynamic Range](images/dr_usage.png)

---

### 4. Grain Effect
Most recipes enable Grain to simulate film texture, with **Strong** grain being the most popular choice.

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
Clarity adds a "digital" local contrast but slows down saving times. The distribution shows a skew towards **Negative** Clarity (softness), proving users prioritize an organic look despite the performance cost.

![Clarity Distribution](images/clarity_dist.png)

---

### 9. Color Chrome vs. Saturation correlation
Do users who use "Strong" Chrome Effect compensate with higher color saturation? The scatter plot below reveals the relationship.

![Chrome vs Color](images/chrome_color_corr.png)

---

### 10. The "Golden Recipe"
Based on the exact averages of all X100V/VI-compatible recipes, here is the mathematically perfect "Fuji Look":

| Setting | Value |
| :--- | :--- |
| **Film Simulation** | **Classic Chrome** |
| **Dynamic Range** | DR400 |
| **Highlights** | +0.5 |
| **Shadows** | +1.0 |
| **Color** | +1.0 |
| **Noise Reduction** | -4 |
| **Sharpening** | -1 |
| **Clarity** | -2 |
| **Grain Effect** | Strong, Small |
| **Color Chrome Effect** | Strong |
| **Color Chrome FX Blue** | Weak |
| **White Balance** | Auto, 0 Red & -2 Blue |

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
