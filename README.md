# Film Simulation Recipe Scraper

A Python tool to collect and organize film simulation recipes for Fujifilm cameras from public sources into a local SQLite database.

## Data Analysis & Trends
This project analyzes over 240 film simulation recipes. Below are the key findings on how photographers are styling their Fuji cameras.

### 1. Most Popular Film Simulations
**Classic Chrome** and **Classic Negative** are the clear favorites, accounting for the majority of recipes.
![Top Simulations](images/top_simulations.png)

### 2. Color Behavior (White Balance Shift)
There is a massive preference for **Warm/Vintage** tones. The scatter plot below shows that most recipes shift Red positively (Green -> Magenta) and Blue negatively (Blue -> Yellow).
![WB Trends](images/wb_trends.png)

### 3. Dynamic Range Preferences
**DR400** is the dominant setting, used to preserve highlight detail in high-contrast "film" looks.
![Dynamic Range](images/dr_usage.png)

### 4. Grain Effect
Most recipes enable Grain to simulate film texture, with **Strong** grain being the most popular choice.
![Grain Usage](images/grain_usage.png)

### 5. ISO Limits
The community generally accepts high ISOs to simulate film grain naturally, with **ISO 6400** being the most common auto-limit.
![ISO Limit](images/iso_limit.png)

### 6. Sensor Distribution
The current dataset has a rich collection for both X-Trans IV and X-Trans V generations.
![Sensor Distribution](images/sensor_distribution.png)

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
