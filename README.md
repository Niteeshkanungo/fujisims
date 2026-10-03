# FujiSims: The Science of X100V & X100VI Aesthetics
> *"Don't just pick a recipe. Understand the DNA of the Fuji look."*

I analyzed **256 film simulation recipes** to uncover the **Likeability Index**—identifying the exact settings the community collectively prefers. Instead of just averaging numbers, this project identifies the "Peak Preferences" of the Fuji world. This tool scrapes recipe sites, stores them in SQLite, and visualizes trends to reveal the true **Community Consensus** for the **X100V and X100VI**.

*Oct 2026 rerun: rescraped from scratch (185 X-Trans IV + 71 X-Trans V source links, 12 cross-listed on both). Sim names normalized (Nostalgic Neg. → Nostalgic Negative, filter variants grouped), High ISO NR promoted into Noise Reduction, nav junk filtered from settings.*

---

---

## 🚀 [CLICK HERE TO VIEW THE INTERACTIVE ANALYSIS](https://niteeshkanungo.github.io/fujisims/)
## 📝 [READ THE FULL STORY ON MEDIUM](https://medium.com/@niteeshkanungo/the-science-of-nostalgia-i-analyzed-240-fujifilm-recipes-to-find-the-community-consensus-0bc073adf72a)
**👆 The full data deep dive and the story behind it.**

> This README contains the summary of my findings. For the complete breakdown of all 11 data points (including White Balance quadrants, Clarity analysis, and Sensor distribution), please visit the link above.

---

---

### The "Nishti Recipe" (Community Consensus)
By applying the **Likeability Index**—identifying the "Peak Preference" for every setting—I have built the definitive Fuji aesthetic. This isn't just an average; it is the most statistically liked configuration in the Fuji world.

**Why this works:** It reflects the community's true "Hive Mind." It favors **Color +2** (refined from +4) and **Soft Shadows (-2)**, reflecting the modern shift toward punchy, cinematic colors and a gentle, filmic highlight roll-off. This is the "Safe Harbor" of Fuji aesthetics—the configuration most likely to be loved out of the box.

*Transparency: the raw community modes are punchier/softer than the curated picks — Color **+4** (67 recipes), Sharpness **-2** (89), Noise Reduction **-4** (155 of 256). The Nishti Recipe deliberately restrains Color to +2 for skin tones, lifts Sharpness to +1 for micro-detail, and polishes NR to -2. Contrast is a three-way tie (Soft 29% / High 28% / Moody 27%), so -2 shadows is a choice, not a landslide.*

| Setting | Value | Why? |
| :--- | :--- | :--- |
| **Film Simulation** | **Classic Chrome** | Top of the Likeability Index in a duel with Classic Negative (59 vs 56 of 256). |
| **Dynamic Range** | **DR400** | The unanimous choice for protecting highlights. |
| **Highlights** | **-2** | Softens the glare on the white desk from the sun. |
| **Shadows** | **-2** | A strong preference for **Softer Shadows** (Cinematic Look). |
| **Color** | **+2** | **The Refined Consensus.** Retains punch without ruining skin tones. |
| **Exposure Compensation** | **+1.0** | Physically turn the dial on top of your camera to make the whole image brighter. |
| **Noise Reduction** | **-2** | **Polished Preference.** Reduces digital grit. |
| **Sharpening** | **+1** | **Professional Choice.** Enhanced micro-detail and edge definition. |
| **Clarity** | **-2** | The "Mist Filter" effect. *(Note: Adds ~1s delay)* |
| **Grain Effect** | **Weak, Small** | **Peak Consensus.** Texture without the grit. |
| **Color Chrome Effect** | **Strong** | Deepens colors in shadows, acting like a polarizer. |
| **Color Chrome FX Blue** | **Weak** | Adds a subtle depth to blue skies. |
| **White Balance** | **Auto, R:-1 B:-3** | A cleaner "Modern/Cinematic Cool" shift (less aggressive than -5). |
| **ISO** | **Auto (up to 6400)** | Embraces noise as structured grain. |

---

### 🧠 The Philosophy: Meaning > Megapixels
**Why choose a Fuji over an iPhone?**

*   **iPhone = "The Computer":** It solves every problem before you click. It lifts all shadows (HDR), perfectly sharpens faces, and balances every highlight. The result is technically perfect but emotionally flat. It *documents* reality.
*   **Fuji = "The Poet":** It interprets reality. It embraces shadows, allows highlights to bloom, and adds texture. It creates a *memory*, not a forensic scan.

---

## ⚡ Performance Warning: The "Clarity Tax"
**Setting Clarity to anything other than 0 causes a ~1 second "Storing" delay after every shot.**
*   **For Portraits/Travel:** Keep Clarity at `-2` (The Nishti Recipe default). The aesthetic gain is worth the wait.
*   **For Street/Moments:** Set Clarity to `0`. You lose the "mist filter" softness, but gaining instant shot-to-shot speed is critical for capturing fleeting moments.

> **Pro Tip:** Use a **PolarPro Mist Filter** (e.g., Shortstache Everyday Filter) to get the "Clarity" look optically with zero software delay.

---




## Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/niteeshkanungo/fujisims.git
   cd fujisims
   ```

2. **Setup environment**:
   ```bash
   # Using uv (recommended)
   uv venv
   source .venv/bin/activate
   uv pip install -e .
   
   # Or using standard pip
   python3 -m venv venv
   source venv/bin/activate
   pip install .
   ```

## Usage
1. **Run the scraper**:
   ```bash
   python scripts/scrape.py
   ```
   This will populate `film_recipes.db`.


## Querying the Data
   Use the provided example script:
   ```bash
   python scripts/query_examples.py
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

## 📬 Contact & Feedback
If you used the **Nishti Recipe** or analyze tool and want to share your results, feedback, or suggestions, please reach out!

*   **Email**: [email@niteeshkanungo.com](mailto:email@niteeshkanungo.com)
*   **Alternate**: [niteeshkanungo@gmail.com](mailto:niteeshkanungo@gmail.com)

## License
MIT
