# The Science of Nostalgia: I Analyzed 256 Fujifilm Recipes and Found Four Patterns

*Oct 2026 update: rescraped from scratch and fixed the parser — bare sim names on legacy pages, sim-name normalization, High ISO NR recovery, nav-junk filtering. Counts below are the corrected 256-recipe numbers.*

![Fuji Header Composite](https://raw.githubusercontent.com/Niteeshkanungo/fujisims/main/images/fuji_header_composite.png)

Why do we choose a Fujifilm camera over an iPhone? 

An iPhone is a computer that *documents* reality. It solves for dynamic range, sharpness, and color balance before you even click the shutter. The result is technically perfect, but emotionally flat.

A Fujifilm camera is a poet. It *interprets* reality. It embraces shadows, allows highlights to bloom, and adds texture. It creates a memory, not a forensic scan.

But with thousands of "Film Simulation Recipes" out there, how do you choose the right one? I decided to stop guessing and start measuring. I built **FujiSims**, a Python-based analysis engine that scraped and analyzed 256 popular recipes to find the "Hidden Consensus" of the Fuji community.

## The Goal: Finding the "Likeability Index"

Instead of just averaging numbers, I looked for "Peak Preferences." I wanted to know where the "Hive Mind" of Fujifilm photographers lives. What are the settings most likely to be loved out of the box?

[View the Interactive Analysis Here](https://niteeshkanungo.github.io/fujisims/) | [GitHub Repository](https://github.com/niteeshkanungo/fujisims)

---

## 1. The Canvas: Classic Chrome is King
Every recipe starts with a base Film Simulation. **Classic Chrome** leads in a duel with **Classic Negative** (59 vs 56 of 256) — the two longtime favorites are now nearly tied, with Eterna a distant third. Chrome's muted tones and deep contrast provide the perfect "analog" foundation.

![Top Simulations](https://raw.githubusercontent.com/Niteeshkanungo/fujisims/main/images/top_simulations.png)

---

## 2. The Color of Memory: White Balance Shifts
White Balance isn't just about accuracy; it's about emotion. The data shows a massive cluster in the **Golden/Vintage** quadrant. Users are intentionally shifting toward warmth to capture that nostalgic, faded-film look.

![WB Trends](https://raw.githubusercontent.com/Niteeshkanungo/fujisims/main/images/wb_trends.png)

---

## 3. Protecting the Highlights: The DR400 Paradox
In the digital world, blown-out highlights are "death." **DR400** is a hardware trick that saves your skies and whites from digital "clipping." Nearly 60% of recipes utilize this to make digital sensors behave like film.

![DR Usage](https://raw.githubusercontent.com/Niteeshkanungo/fujisims/main/images/dr_usage.png)

---

## 4. Tone Curve: A Three-Way Tie
How does the community handle contrast? The **Contrast Map** is nearly tied three ways — **Soft/Cinematic 29%, High Contrast 28%, Moody 27%** (Ethereal 16%). There is no consensus here: as many recipes push hard contrast as soft. Pick your mood.

![Contrast Map](https://raw.githubusercontent.com/Niteeshkanungo/fujisims/main/images/contrast_map.png)

---

## 5. The "Organic Index": Sharpness vs. Noise Reduction
Modern sensors are "too clean." To combat this, the community lives in the **Organic/Analog** zone: **Negative Sharpness** (to soften digital edges) and **Negative Noise Reduction** (to allow natural grain to show through).

![Organic Index](https://raw.githubusercontent.com/Niteeshkanungo/fujisims/main/images/sharpness_nr_corr.png)

---

## 6. Structure & Texture: Sharpness vs. Clarity
**Clarity** is a powerful but "expensive" setting (it adds processing delay). Most recipes use a slightly negative clarity to create a "bloom" or "mist" effect, creating a dreamier, less clinical structure.

![Structure Index](https://raw.githubusercontent.com/Niteeshkanungo/fujisims/main/images/structure_index.png)

---

## 7. B&W Contrast: Shadow Hardness
Interestingly, when the community builds Black & White recipes, they push shadows significantly harder than in color recipes. B&W isn't just "desaturated color"; it's a completely different approach to lighting.

![BW Contrast](https://raw.githubusercontent.com/Niteeshkanungo/fujisims/main/images/bw_contrast.png)

---

## 8. The Finding: Four Patterns, Not One Recipe
No single recipe wins. Shadows are a 3-way tie, grain is 62/57/53, WB is flat — averaging them into one "consensus" hides the real splits. K-means (k=4, n=256) finds four stable looks. Shared constants: DR400, NR -4, ISO Auto 6400.

*   **Warm Cinematic — 35% (90):** Classic Chrome, H -2 / S -1, Color +4, Sh -2, Clarity -2, Grain Strong Small, WB +1/-5, Chrome Strong/Weak (tie), Exp +2/3. The default. Start here.
*   **Cool Contrast — 26% (66):** Mixed sims (Eterna/Chrome/Acros 10/10/9), H +4 / S +2, Color +4, Sh -2, Clarity -3, Grain Weak Small, WB -2/+1, Chrome Strong/Strong, Exp 0. Punchy + B&W-friendly. Signature is crushed highlights + cool WB; grain is a 3-way tie.
*   **Vintage Fade — 21% (53):** Classic Negative, H -1 / S -2, Color -4, Sh -2, Clarity -4, Grain Strong Large, WB +1/-3, Chrome Strong/Strong, Exp +1/3. Muted film look.
*   **Vivid Crisp — 18% (47):** Classic Chrome, H +1 / S +1, Color +4, Sh 0, Clarity +3, Grain Weak Small, WB +1/-3, Chrome Strong/Weak (tie), Exp +2/3. Crisp, no mist delay.

![Four Patterns](https://raw.githubusercontent.com/Niteeshkanungo/fujisims/main/images/pattern_map.png)

---

## 9. See the Difference: Real World Examples
Theory is nice, but what does the **Warm Cinematic** pattern actually look like? Here are straight-from-camera JPEGs (Classic Chrome, H -2 / S -1, Color +4, Clarity -2).

### "Cinema Bloom"
![Cat on shelf](https://raw.githubusercontent.com/Niteeshkanungo/fujisims/main/images/example_cat_shelf.jpg)
Look at the light catching the fur. The negative clarity and soft highlights create a "blooming" effect that looks like printed film, not a digital file.

### Dynamic Range Protection
![Puzzle table](https://raw.githubusercontent.com/Niteeshkanungo/fujisims/main/images/example_puzzle_table.jpg)
This is **DR400** doing the heavy lifting. The sunlight hitting the white table is extremely harsh, but the recipe protects those highlights, allowing you to see the texture of the table clearly.

### Organic Texture
![Cat in bed](https://raw.githubusercontent.com/Niteeshkanungo/fujisims/main/images/example_cat_bed.jpg)
Negative Sharpness and Noise Reduction work together to remove the "digital edge," making fur and fabric look soft and natural.

### Backlight Contrast
![Plants by window](https://raw.githubusercontent.com/Niteeshkanungo/fujisims/main/images/example_plants_window.jpg)
Even in difficult lighting, the **Shadows -2** setting maintains rich, deep blacks, while the specific White Balance shift keeps the light neutral and clean.

---

## Conclusion: Meaning > Megapixels
Data science usually focuses on efficiency. But in photography, it helps us understand **aesthetics**. By analyzing the "Hive Mind," we can identify the settings that trigger emotion.

**Full Project on GitHub:** [https://github.com/niteeshkanungo/fujisims](https://github.com/niteeshkanungo/fujisims)
