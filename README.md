# FujiSims: The Science of X100V & X100VI Aesthetics
> *"Don't just pick a recipe. Understand the DNA of the Fuji look."*

I analyzed **256 film simulation recipes** (fresh rescrape, Oct 2026) and found **four patterns**, not one winner. K-means clustering (k=4) on highlights, shadows, color, sharpness, clarity, and white balance. This tool scrapes recipe sites, stores them in SQLite, and visualizes trends.

*Oct 2026 rerun: rescraped from scratch (185 X-Trans IV + 71 X-Trans V source links, 12 cross-listed on both). Sim names normalized (Nostalgic Neg. → Nostalgic Negative, filter variants grouped), High ISO NR promoted into Noise Reduction, nav junk filtered from settings.*

---

---

## 🚀 [CLICK HERE TO VIEW THE INTERACTIVE ANALYSIS](https://niteeshkanungo.github.io/fujisims/)
## 📝 [READ THE FULL STORY ON MEDIUM](https://medium.com/@niteeshkanungo/the-science-of-nostalgia-i-analyzed-240-fujifilm-recipes-to-find-the-community-consensus-0bc073adf72a)
**👆 The full data deep dive and the story behind it.**

> This README contains the summary of my findings. For the complete breakdown of all 11 data points (including White Balance quadrants, Clarity analysis, and Sensor distribution), please visit the link above.

---

---

### The Four Patterns (not one recipe)
No single setting wins — shadows are a 3-way tie, grain is 62/57/53, WB is flat. K-means (k=4, n=256) finds four stable looks. Shared constants: **DR400, NR -4, ISO Auto 6400**. Full table: `meta/patterns.json`.

| Pattern | Share | Settings |
| :--- | :--- | :--- |
| **Warm Cinematic** (start here) | 35% (90) | Classic Chrome · H -2 / S -1 · Color +4 · Sh -2 · Clarity -2 · Grain Strong Small · WB +1/-5 |
| **Cool Contrast** | 26% (66) | Mixed sims (Eterna/Chrome/Acros) · H +4 / S +2 · Color +4 · Sh -2 · Clarity -3 · Grain Weak Small · WB -2/+1 |
| **Vintage Fade** | 21% (53) | Classic Negative · H -1 / S -2 · Color -4 · Sh -2 · Clarity -4 · Grain Strong Large · WB +1/-3 |
| **Vivid Crisp** | 18% (47) | Classic Chrome · H +1 / S +1 · Color +4 · Sh 0 · Clarity +3 · Grain Weak Small · WB +1/-3 |

Close calls labeled on the site (e.g. Cool Contrast sims 10/10/9, Faded shadows 3-way tie). Signatures are solid: Warm = warm + mist, Cool = crushed + cool, Vintage = desat + heavy mist, Vivid = only positive clarity.

*Retired: the single "Nishti Recipe" — it averaged away real splits (raw modes: Color +4, Sharpness -2, NR -4, Highlights -1). Pick a pattern instead.*

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
