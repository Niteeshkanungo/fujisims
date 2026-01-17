# FujiSims: The Science of X100V & X100VI Aesthetics
> *"Don't just pick a recipe. Understand the DNA of the Fuji look."*

I analyzed **240+ film simulation recipes** to uncover the **Likeability Index**—identifying the exact settings the community collectively prefers. Instead of just averaging numbers, this project identifies the "Peak Preferences" of the Fuji world. This tool scrapes recipe sites, stores them in SQLite, and visualizes trends to reveal the true **Community Consensus** for the **X100V and X100VI**.

---

---

## 🚀 [CLICK HERE TO VIEW THE INTERACTIVE ANALYSIS](https://niteeshkanungo.github.io/fujisims/)
**👆 The full data deep dive is hosted on our live website.**

> This README contains the summary of our findings. For the complete breakdown of all 11 data points (including White Balance quadrants, Clarity analysis, and Sensor distribution), please visit the link above.

---

---

### The "Nishti Recipe" (Community Consensus)
By applying the **Likeability Index**—identifying the "Peak Preference" for every setting—we have built the definitive Fuji aesthetic. This isn't just an average; it is the most statistically liked configuration in the Fuji world.

**Why this works:** It reflects the community's true "Hive Mind." It favors **Color +4** and **Soft Shadows (-2)**, reflecting the modern shift toward punchy, cinematic colors and a gentle, filmic highlight roll-off. This is the "Safe Harbor" of Fuji aesthetics—the configuration most likely to be loved out of the box.

| Setting | Value | Why? |
| :--- | :--- | :--- |
| **Film Simulation** | **Classic Chrome** | The undisputed king of the Likeability Index. |
| **Dynamic Range** | **DR400** | The unanimous choice for protecting highlights. |
| **Highlights** | **-1** | Subtractive highlights ensure the sky never looks "digital." |
| **Shadows** | **-2** | A strong preference for **Softer Shadows** (Cinematic Look). |
| **Color** | **+4** | **The Surprise Consensus.** Intense, deep crimson and blues. |
| **Noise Reduction** | **-4** | The "Anti-Digital" standard. |
| **Sharpening** | **+1** | **Professional Choice.** Enhanced micro-detail and edge definition. |
| **Clarity** | **-2** | The "Mist Filter" effect. *(Note: Adds ~1s delay)* |
| **Grain Effect** | **Strong, Small** | Adds texture to simulate High-ISO film stock. |
| **Color Chrome Effect** | **Strong** | Deepens colors in shadows, acting like a polarizer. |
| **Color Chrome FX Blue** | **Weak** | Adds a subtle depth to blue skies. |
| **White Balance** | **Auto, R:-1 B:-5** | A "Modern/Cinematic Cool" shift found in high-end editorial work. |
| **ISO** | **Auto (up to 6400)** | Embraces noise as structured grain. |

---

## ⚡ Performance Warning: The "Clarity Tax"
**Setting Clarity to anything other than 0 causes a ~1 second "Storing" delay after every shot.**
*   **For Portraits/Travel:** Keep Clarity at `-2` (The Nishti Recipe default). The aesthetic gain is worth the wait.
*   **For Street/Moments:** Set Clarity to `0`. You lose the "mist filter" softness, but gaining instant shot-to-shot speed is critical for capturing fleeting moments.

> **Pro Tip:** Use a **PolarPro Mist Filter** (e.g., Shortstache Everyday Filter) to get the "Clarity" look optically with zero software delay.

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
