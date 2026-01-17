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
   git clone <your-repo-url>
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

2. **Query the data**:
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
