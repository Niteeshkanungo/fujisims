# Film Simulation Recipe Scraper

A Python tool to collect and organize film simulation recipes for Fujifilm cameras from public sources into a local SQLite database.

## Features
- Scrapes recipe details (Simulation, Dynamic Range, White Balance, etc.)
- Parses advanced settings including White Balance shifts (Red/Blue).
- Stores data in a local SQLite database for easy querying.
- Deduplicates entries based on URL.

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

## Data Analysis
Based on the scraped data, here are the key technical trends:

### 1. Most Popular Film Simulation Bases
Users heavily favor **Classic Chrome** and **Classic Negative** across all generations.
- **Classic Chrome**: The go-to for many recipes (14 recipes).
- **Classic Negative**: A close second (13 recipes).
- **Nostalgic Neg.**: Dominated X-Trans V usage.

### 2. Evolution: X-Trans IV vs V
- **X-Trans IV**: A balanced mix of Classic Chrome, Eterna, and Classic Negative.
- **X-Trans V**: Shows a massive shift towards **Nostalgic Neg.** and **Reala Ace** (new simulations).

### 3. Color Grading Trends
There is a clear preference for **warm, nostalgic tones**:
- Average Red Shift: **+0.46**
- Average Blue Shift: **-2.15**
- *Interpretation*: Recipes are frequently pushing Red up and Blue down to achieve a golden/vintage look.

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
