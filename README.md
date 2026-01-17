# FujiSims: The Science of X100V & X100VI Aesthetics
> *"Don't just pick a recipe. Understand the DNA of the Fuji look."*

I analyzed **240+ film simulation recipes** to find the mathematical average of what the community considers "beautiful". This project scrapes the top recipe sites, stores the settings in a SQLite database, and visualizes the trends to uncover the "Golden Mean" of Fujifilm aesthetics for the **X100V and X100VI**.

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

## 📊 View the Full Analysis
**[Click here to view the Interactive Data Deep Dive](https://niteeshkanungo.github.io/fujisims/)**

> The `README` below contains the summary of our findings. for the complete breakdown of all 11 data points (including White Balance quadrants, Clarity analysis, and Sensor distribution), please visit the live website above.

---

### The "Nishti Recipe" (Highest Probability of Likeness)
Through statistical averaging of every X100V & X100VI recipe in our database, we typically find the "Golden Mean"—a set of settings that represents the collective consensus of the Fujifilm community. 

**Why this works:** The mathematical average converges on a look that balances modern sharpness with vintage character. It adopts the desaturated documentary feel of **Classic Chrome**, adds the highlight protection of **DR400**, and layers it with a "Golden Hour" warmth (Red+0, Blue-2) that is universally pleasing to the human eye. This isn't just an average; it is the "safe harbor" of aesthetics—the recipe most likely to yield a pleasing result in any condition.

| Setting | Value | Why? |
| :--- | :--- | :--- |
| **Film Simulation** | **Classic Chrome** | The gold standard for documentary photography. It creates a distinct, slightly desaturated look that feels "real" yet cinematic. |
| **Dynamic Range** | **DR400** | Preserves highlight roll-off. Essential for that "analog" inability to blow out skies. |
| **Highlights** | **+0.5** | A slight boost to keep images punchy without losing detail. |
| **Shadows** | **+1.0** | Adds contrast and depth, avoiding the flat "HDR" look of modern smartphones. |
| **Color** | **+1.0** | Compensates for Classic Chrome's natural desaturation. |
| **Noise Reduction** | **-4** | **Critical.** Turns off smearing to allow the lens's natural character and sensor noise to breathe. |
| **Sharpening** | **-1** | Removes digital halos. Makes the image look "optical" rather than "processed". |
| **Clarity** | **-2** | The "Mist Filter" effect. Softens micro-contrast for a dreamy look. *(Note: Adds ~1s delay)* |
| **Grain Effect** | **Strong, Small** | Adds texture to simulate High-ISO film stock, masking the "clean" digital sensor look. |
| **Color Chrome Effect** | **Strong** | Deepens colors (especially reds/greens) in shadows, acting like a polarizer. |
| **Color Chrome FX Blue** | **Weak** | Adds a subtle depth to blue skies without turning them neon. |
| **White Balance** | **Auto, R:0 B:-2** | The "Golden Warmth". Shifts the image slightly yellow/orange for a nostalgic afternoon feel. |
| **ISO** | **Auto (up to 6400)** | Embraces noise. ISO 6400 on X100V looks like structured grain, not ugly color noise. |

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
