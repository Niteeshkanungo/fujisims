import requests
from bs4 import BeautifulSoup
import re
import time
from database import save_recipe

# Headers to mimic a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
}
# NOTE: FujiXWeekly and other sites often block non-browser user agents (403 Forbidden).
# The User-Agent above mimics a standard Chrome browser on macOS.

TARGET_URLS = {
    "X-Trans V": "https://fujixweekly.com/fujifilm-x-trans-v-recipes/",
    "X-Trans IV": "https://fujixweekly.com/fujifilm-x-trans-iv-recipes/",
    # Add others as needed
}

def clean_text(text):
    return text.replace('\xa0', ' ').strip()

def normalize_sim(raw):
    """Canonicalize film-sim names so votes aren't split.
    Groups filter variants (Acros+G -> Acros) and punctuation
    variants (Nostalgic Neg. -> Nostalgic Negative). Returns None
    for uncountable placeholders like 'Any'."""
    if not isinstance(raw, str):
        return None
    s = raw.strip().strip('.')
    low = s.lower()
    if low in ('any', 'n/a', 'various'):
        return None
    # Strip Fuji filter suffixes: "Monochrome (+Y, +R, +G)" -> "Monochrome",
    # "Acros+G" -> "Acros", "Provia/STD" -> "Provia", "Acros (" (truncated) -> "Acros"
    s = re.split(r'\s*[\(\[/\+]', s, maxsplit=1)[0].strip().strip('.')
    low = s.lower()
    aliases = {
        'nostalgic neg': 'Nostalgic Negative',
        'nostalgic negative': 'Nostalgic Negative',
        'classic negative': 'Classic Negative',
        'classic chrome': 'Classic Chrome',
        'eterna bleach bypass': 'Eterna Bleach Bypass',
        'eterna': 'Eterna',
        'reala ace': 'Reala Ace',
        'provia': 'Provia',
        'velvia': 'Velvia',
        'astia': 'Astia',
        'acros': 'Acros',
        'monochrome': 'Monochrome',
        'sepia': 'Sepia',
        'pro neg hi': 'Pro Neg Hi',
        'pro neg. hi': 'Pro Neg Hi',
        'pro neg std': 'Pro Neg Std',
        'pro neg. std': 'Pro Neg Std',
        'pro neg': 'Pro Neg Std',
    }
    # Normalize internal whitespace/punctuation for lookup
    key = re.sub(r'\s+', ' ', low).strip()
    return aliases.get(key, s)

# Keys that are site nav/commerce noise, never real settings
JUNK_KEYS = {
    '', 'See also', 'See Also', 'in black', 'in silver', 'in charcoal',
    'Comparison', 'Update', 'cameras',
}

def _is_junk_key(key, value=None):
    if not key or not key.strip():
        return True
    k = key.strip()
    if k in JUNK_KEYS:
        return True
    if k.startswith('Fujifilm '):
        return True
    if len(k) > 30:  # real setting names are short
        return True
    if ',' in k or '.' in k:  # sentence fragments, not settings
        return True
    lk = k.lower()
    if ' vs ' in lk or '?' in k:  # comparison headers / questions, not settings
        return True
    return False

def parse_recipe_page(url, sensor):
    print(f"Scraping {url}...")
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Try to find the title
    title_tag = soup.find('h1', class_='entry-title')
    title = clean_text(title_tag.text) if title_tag else "Unknown Recipe"

    # Main content area
    content = soup.find('div', class_='entry-content')
    if not content:
        print("No content found")
        return None

    # Extraction Logic
    # We look for lines like "Film Simulation: ..."
    # This is tricky because formatting varies. We'll scan all text nodes or p tags.
    
    data = {
        "name": title,
        "sensor": sensor,
        "url": url,
        "full_settings": {}
    }
    
    # Mappings from text keys to DB fields
    key_map = {
        "Film Simulation": "film_simulation",
        "Film Sim": "film_simulation",
        "Simulation": "film_simulation",
        "Dynamic Range": "dynamic_range",
        "Grain Effect": "grain_effect",
        "Grain": "grain_effect",
        "White Balance": "white_balance",
        "Highlight": "highlight",
        "Shadow": "shadow",
        "Color": "color",
        "Sharpness": "sharpness",
        "Sharpening": "sharpness",
        "Sharpeness": "sharpness",  # source typo seen in the wild
        "Noise Reduction": "noise_reduction",
        "Clarity": "clarity",
        "ISO": "iso",
        "Exposure Compensation": "exposure_compensation",
        # Aliases or partial matches could be added here
        "Color Chrome Effect": "full_settings", # saving to JSON for now if not in main schema
        "Color Chrome FX Blue": "full_settings",
        "Color Chrome Effect Blue": "full_settings",
        "High ISO NR": "full_settings",
        "Toning": "full_settings",
    }
    # Merge duplicate Chrome-blue spellings into one canonical key
    CHROME_BLUE_KEYS = {"Color Chrome FX Blue", "Color Chrome Effect Blue"}

    # Bare film-sim names used by older X-Trans IV/III pages with no "Film Simulation:" prefix
    # e.g. "Classic Chrome|Dynamic Range: DR400|..." or "Monochrome (+Y, +R, +G)"
    KNOWN_SIMS = [
        "Classic Chrome", "Classic Negative", "Nostalgic Neg", "Nostalgic Negative",
        "Eterna Bleach Bypass", "Eterna", "Provia", "Velvia", "Astia",
        "Acros", "Monochrome", "Reala Ace", "Pro Neg", "Pro Neg Hi", "Pro Neg Std",
        "Sepia",
    ]

    def _detect_bare_sim(line):
        low = line.lower()
        for sim in KNOWN_SIMS:
            if low == sim.lower() or low.startswith(sim.lower() + " ") or low.startswith(sim.lower() + "("):
                return normalize_sim(sim)
        # Handle "Monochrome (+Y, +R, +G)" style -> normalize to base
        if low.startswith("monochrome"):
            return normalize_sim(line)
        return None

    # Iterate through paragraphs to find settings
    # Use separator='\n' to handle <br> tags or implicit newlines
    for p in content.find_all(['p', 'li']):
        # Split block content into lines
        lines = p.get_text(separator='\n').split('\n')
        
        for line in lines:
            line = clean_text(line)
            if ':' not in line:
                # Old format: bare sim name on its own line
                if "film_simulation" not in data:
                    bare = _detect_bare_sim(line)
                    if bare:
                        data["film_simulation"] = bare
                continue
                
            parts = line.split(':', 1)
            key = parts[0].strip()
            value = parts[1].strip()
            
            # Check if this key matches one of our expected fields
            matched_field = None
            for k, field in key_map.items():
                if k.lower() == key.lower():
                    matched_field = field
                    break
            
            if matched_field:
                if matched_field == "full_settings":
                    if key in CHROME_BLUE_KEYS:
                        key = "Color Chrome FX Blue"  # canonical spelling
                    if _is_junk_key(key):
                        continue
                    data["full_settings"][key] = value
                elif matched_field == "film_simulation":
                    normed = normalize_sim(value)
                    if normed:
                        data[matched_field] = normed
                    # 'Any'/multi-recipe placeholders -> leave unset (counted as NULL)
                else:
                    data[matched_field] = value
            else:
                 # Store unrecognized keys in full_settings just in case
                 if not _is_junk_key(key):
                    data["full_settings"][key] = value

    # Promote High ISO NR into noise_reduction when the dedicated field is missing
    # (older pages only list High ISO NR; same NR axis for analysis).
    # Kept in full_settings too for provenance.
    hi_nr = data["full_settings"].get("High ISO NR")
    if hi_nr and not data.get("noise_reduction"):
        data["noise_reduction"] = hi_nr

    # Parse White Balance Shift
    if "white_balance" in data:
        wb_text = data["white_balance"]
        # Look for Red shift
        r_match = re.search(r'([+-]?\d+)\s*R(?:ed)?', wb_text, re.IGNORECASE)
        if r_match:
            data["wb_shift_red"] = int(r_match.group(1))
            
        # Look for Blue shift
        b_match = re.search(r'([+-]?\d+)\s*B(?:lue)?', wb_text, re.IGNORECASE)
        if b_match:
            data["wb_shift_blue"] = int(b_match.group(1))

    return data

def scrape_sensor_index(sensor, index_url):
    print(f"Fetching index for {sensor}...")
    response = requests.get(index_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    links = set()
    content = soup.find('div', class_='entry-content')
    
    # Find all links in the content
    for a in content.find_all('a', href=True):
        href = a['href']
        # Filter for recipe pages (heuristics: contains fujixweekly.com, has date or slug)
        if "fujixweekly.com" in href and _is_likely_recipe(href, index_url):
            links.add(href)
            
    print(f"Found {len(links)} potential recipes.")
    return list(links)

def _is_likely_recipe(href, index_url):
    """
    Heuristic Filter:
    We don't want to scrape "About" pages or "Categories".
    True recipe pages on this site usually have a date structure in the URL (e.g. /2023/05/12/).
    """
    # Basic filter: exclude tag archives, internal nav, etc.
    if href == index_url: return False
    if "/tag/" in href: return False
    if "/category/" in href: return False
    if "/author/" in href: return False
    # Recipes usually have a date YYYY/MM/DD in URL
    if re.search(r'/\d{4}/\d{2}/\d{2}/', href):
        return True
    return False

def main():
    for sensor, url in TARGET_URLS.items():
        recipe_links = scrape_sensor_index(sensor, url)
        
        count = 0
        for link in recipe_links:
            # Removed limit for production run, but let's keep a small limit per sensor for this verification step if user wants FULL scrape.
            # User asked to "scrape all", so we should process all.
            # However, for this agent step, I'll limit to 5 per sensor to verify the fix first, then user can clear the DB and run fully if desired.
            # Actually, the user asked to "store up it", implying full execution.
            # I will remove the limit.
    
            recipe_data = parse_recipe_page(link, sensor)
            if recipe_data:
                print(f"Title: {recipe_data['name']}")
                print(f"Sim: {recipe_data.get('film_simulation')}")
                save_recipe(recipe_data)
                time.sleep(1) # Be polite
        


if __name__ == "__main__":
    main()
