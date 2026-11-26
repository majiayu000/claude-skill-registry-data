---
vendored_from: https://github.com/riverventures/coloring-book
name: coloring-book-generator
description: Generate printable coloring pages for kids on demand. Age-calibrated line art (0-2, 3-5, 6+), themed generators (animals, family, learning, stories, holidays), PDF output, optional direct-to-printer. Use when the user asks for a coloring page, coloring book, activity sheet, printable for kids, or line art for children to color.
triggers:
  - coloring-book-generator
  - coloring
  - book
  - generator

---

# coloring-book

Generate printable coloring pages for kids. Tell me the subject and the child's age — I handle the rest.

## Requirements

- Google API key with Generative Language API enabled (for Gemini image generation)
- Python 3.9+ with Pillow (`pip install Pillow`)
- Optional: network printer via CUPS/AirPrint for direct printing

## How It Works

1. User describes what they want ("a dinosaur playing soccer")
2. Skill generates age-appropriate line art via Gemini
3. Converts to printable A4/Letter PDF
4. Optionally sends to printer

## Age Calibration

Always ask for the child's age if not provided. Complexity scales:

### Under 2 years
- **Extra thick** bold outlines (4-6px stroke)
- Simple shapes only: one main subject, minimal background
- Large coloring areas (toddler crayon-friendly)
- No small details, no intricate patterns
- Max 3-4 distinct elements per page

### Ages 3-5
- **Thick** outlines (2-4px stroke)
- More detail: background elements, 2-3 characters
- Medium-sized coloring areas
- Simple patterns allowed (stripes, dots)
- Can include letters or numbers as part of the scene

### Ages 6+
- **Standard** outlines (1-2px stroke)
- Complex scenes with multiple elements
- Fine detail, small areas, patterns
- Can include hidden objects, mazes, or puzzles
- Intricate backgrounds

## Prompt Engineering

When generating via Gemini (model: `gemini-3.1-flash-image-preview`), use this structure:

```
Create a coloring book page for a [AGE] year old child.
Black and white line art only. No shading, no filled areas, no gray tones, no color.
Clean [THICKNESS] outlines suitable for a young child to color in.
The scene shows: [USER DESCRIPTION].
[AGE-SPECIFIC DETAILS].
Pure black lines on white background, coloring book style.
Portrait orientation, filling the full page.
```

### Thickness by age:
- Under 2: "extra thick bold"
- 3-5: "thick bold"
- 6+: "clean medium-weight"

### Background by age:
- Under 2: "Simple background with just ground line and sun. Maximum 3-4 elements total."
- 3-5: "Simple background with a few trees, flowers, or clouds. 5-8 elements total."
- 6+: "Detailed background with multiple elements. Can be complex."

## Themed Generators

### Animals
"[ANIMAL] in [LOCATION]" — generates the animal in a recognizable local setting.
Examples: "camel in the Dubai desert", "kangaroo at Sydney harbour", "bear in Swiss mountains"

### My Family
Ask for family member descriptions, then generate them in a fun scene together.
"A family with a dad, mom, baby girl, and a dog at the beach"

### Learning Pages
Letters, numbers, shapes with coloring areas and the word spelled out.
"The letter B with a butterfly, a ball, and a banana"

### Story Pages (Booklet Mode)
Generate sequential scenes. Each page advances the narrative.
"A 5-page story about a kitten who gets lost and finds her way home"
Generate each page separately, maintaining character consistency in the prompts.

### Holiday / Cultural
Ramadan, Eid, Diwali, Christmas, Lunar New Year, Easter — culturally appropriate scenes.
"Ramadan iftar table with family, lanterns, dates, and a crescent moon"

## Personalization

If the user provides a child's name, add it to the top of the page:
- Generate the coloring page image first
- Then use Pillow to add the name in outline bubble font at the top margin
- The name itself should be colorable (outline only, not filled)

## Output

### Single Page
Generate image → convert to A4 PDF → deliver to user.

```python
from PIL import Image

img = Image.open("coloring_page.jpg").convert("RGB")
a4_w, a4_h = int(8.5 * 150), int(11 * 150)
page = Image.new("RGB", (a4_w, a4_h), "white")
margin = 75
max_w, max_h = a4_w - 2*margin, a4_h - 2*margin
ratio = min(max_w/img.width, max_h/img.height)
new_w, new_h = int(img.width*ratio), int(img.height*ratio)
img_resized = img.resize((new_w, new_h), Image.LANCZOS)
page.paste(img_resized, ((a4_w-new_w)//2, (a4_h-new_h)//2))
page.save("coloring_page.pdf", "PDF", resolution=150)
```

### Booklet Mode (Multiple Pages)
Generate each page image → create individual PDFs → merge into single multi-page PDF.

```python
pages = []
for img_path in page_images:
    img = Image.open(img_path).convert("RGB")
    # ... same resize logic as above ...
    pages.append(page)

pages[0].save("coloring_book.pdf", "PDF", resolution=150, save_all=True, append_images=pages[1:])
```

### Direct Print (Optional)
If user says "print it" or "send to printer":

```bash
# Detect available printers
lpstat -p -d

# Print to default printer
lp -d [PRINTER_NAME] coloring_page.pdf

# Or AirPrint
lp coloring_page.pdf
```

## API Call

```bash
API_KEY="YOUR_GEMINI_API_KEY"

curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "PROMPT_HERE"}]}],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "thinkingConfig": {"thinkingBudget": 2048}
    }
  }'
```

Extract image: `jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' | base64 -d > page.jpg`

## Examples

**"Make a coloring page of a giraffe and his bird friend for my 19-month-old"**
→ Extra thick lines, baby giraffe with big eyes, small bird on head, simple grass and sun. Max 4 elements. A4 PDF output.

**"10-page ocean coloring book for a 4-year-old named Liam"**
→ 10 pages: whale, octopus, clownfish, seahorse, turtle, starfish, submarine, mermaid, pirate ship, treasure chest. Each page has "LIAM" in bubble letters at top. Compiled into single PDF.

**"Ramadan coloring page for a 6-year-old"**
→ Detailed scene: family at iftar table, lanterns hanging, crescent moon, dates and Vimto on table, mosque silhouette in background. Standard line weight with fine detail.
