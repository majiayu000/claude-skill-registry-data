---
name: school-problems
description: "Help solve academic STEM problems (physics, math, chemistry) from school PDFs/assignments — extract data, apply formulas, show step-by-step calculations, save to Obsidian vault."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [school, physics, math, homework, problems, step-by-step]
    related_skills: [ocr-and-documents, youtube-content, obsidian-markdown]
---

# School Problems — Step-by-Step Help

## When to Use

Use when the user asks for help solving **academic problems from school assignments**:
- Physics problems (dilatação, calorimetria, cinemática, etc.)
- Math problems (equations, geometry, functions)
- Chemistry problems (stoichiometry, thermochemistry)
- Any problem with formulas and calculations

## User Preferences (keila)

This user has specific preferences. If you notice similar patterns with other users, adapt accordingly:

- **Language**: Portuguese (Brazilian) with "você" — always
- **Verbosity**: Show ALL calculation steps. Never skip intermediate algebra. Every unit conversion must be visible.
- **Algebra detail**: When the user asks "pq" (why) about a step (e.g., sign change, equation isolation), break it down into separate sub-steps showing exactly what moves where. Never just say "because algebra" — show each sign flip.
- **Confirmation**: The user double-checks understanding with statements like "fica negativo né". Confirm when they're right and explain why clearly.
- **Terminal trust**: If the user has experienced forced-exit / crash errors from terminal commands, always present the execution plan in plain language first — list each step, wait for confirmation before running anything.
- **Organization**: Save solved problems to Obsidian vault (escola/<subject>/<problem-slug>.md) and commit with git.

## Workflow

### Step 1: Present the Plan First

If the user has had terminal issues before (forced exits, crashes), **show the plan in plain language** before running any commands:

```
O que vou fazer:
1. Extrair texto do PDF com PyMuPDF
2. Procurar a questão específica
3. Resolver passo-a-passo
```

Wait for user confirmation ("vai", "pode ir", "ok") before executing.

Otherwise, proceed directly to finding the problem.

If the problem is in a PDF, use **`ocr-and-documents`** skill to extract text:

```python
import fitz
doc = fitz.open("T1 de Física - Dilatação_compressed.pdf")
for page in doc:
    print(page.get_text())
```

**Pitfall — tables as images**: Many school PDFs have coefficient tables, formula sheets, or graphs as **embedded images**, not text. PyMuPDF's `get_text()` won't capture them. Detect this:

```python
# Check for images on the page
page = doc[0]
images = page.get_images()
print(f"Images found: {len(images)}")
for i, img in enumerate(images):
    xref = img[0]
    base = doc.extract_image(xref)
    with open(f"/tmp/table_{i}.{base['ext']}", "wb") as f:
        f.write(base["image"])
```

Then OCR the extracted image:
```bash
sudo apt-get install -y tesseract-ocr tesseract-ocr-por  # Portuguese language pack
```
```python
import pytesseract
from PIL import Image
text = pytesseract.image_to_string(Image.open("/tmp/table_0.png"), lang="por")
# Interpret carefully — OCR may misread exponents (e.g., "105" = 10⁻⁵, "x108" = ×10⁻⁵)
```

**Alternative**: If the user provides the problem text directly (no PDF), skip to Step 2.

### Step 2: Extract the Data

Identify and list all given values with their units:

| Variable | Value | Unit | Notes |
|----------|-------|------|-------|
| L₀ | 61.80 | m | Initial length |
| T₀ | 17 | °C | Initial temperature |
| ΔL | 233 | mm | → convert to m (0.233 m) |
| α | 2.4×10⁻⁵ | °C⁻¹ | From table (aluminum) |

**Critical — unit conversion**: Always check if units are consistent. Common traps:
- mm → m (divide by 1000)
- cm → m (divide by 100)
- g → kg (divide by 1000)
- °C stays °C for ΔT calculations

### Step 3: Identify the Formula

Match the problem type to the correct formula:

| Topic | Formula | Variables |
|-------|---------|-----------|
| Dilatação linear | ΔL = L₀·α·ΔT | α = coefficient, ΔT = temp change |
| Dilatação superficial | ΔA = A₀·β·ΔT | β = 2α |
| Dilatação volumétrica | ΔV = V₀·γ·ΔT | γ = 3α |
| Calorimetria | Q = m·c·ΔT | c = specific heat |
| Calor latente | Q = m·L | L = latent heat |

**Relation between coefficients**: For the same material:
- β = 2α (surface = 2 × linear)
- γ = 3α (volume = 3 × linear)

### Step 4: Solve Step by Step

Present the solution as numbered steps, showing **every substitution**:

```
1️⃣ ΔL = L₀ · α · ΔT
   0.233 = 61.80 × 2.4×10⁻⁵ × ΔT

2️⃣ ΔT = 0.233 / (61.80 × 2.4×10⁻⁵)
   ΔT = 0.233 / 0.0014832
   ΔT = 157.09 °C

3️⃣ T_final = T₀ + ΔT
   T_final = 17 + 157.09
   T_final = 174.09 °C ✅
```

**Key rules (from the user's assignment instructions):**
- Show ALL calculations — incomplete answers are disqualified
- Include units in every step
- 30% of the exercise value is deducted for unit/scale errors
- Present the final answer clearly boxed/highlighted

### Step 5: Handle Signs in Detail

**Heating vs. Cooling**:
- **Heating** (temp increases) → ΔT positive → ΔL/ΔA/ΔV positive (expansion)
- **Cooling** (temp decreases) → ΔT negative → ΔL/ΔA/ΔV negative (contraction)

When the problem says "resfriada" (cooled) or the final area is smaller than initial:
```python
ΔA = A − A₀  →  if A < A₀, ΔA is NEGATIVE
```

**Algebra sign trick — WALK THROUGH EVERY FLIP (common confusion)**:

Students often get stuck at this step. Show it like this:

```
−T_i = −637

# Both sides are negative. Multiply both sides by −1:
(−1) · (−T_i) = (−1) · (−637)

# Negative × negative = positive:
T_i = 637 °C ✅
```

Or equivalently: "O −T_i significa que T_i está com sinal trocado. Pra achar T_i, multiplica os dois lados por −1."

**When showing sign flips, use this format**:

```
12 − T_i = −625
     ↓ (12 passa pra direita subtraindo)
−T_i = −625 − 12
     ↓ (−625 − 12 = −637)
−T_i = −637
     ↓ (× −1 nos dois lados)
T_i = 637
```

Every arrow must explain the operation. Never skip a line.

### Step 6: Save to Obsidian Vault

After solving, save the solution to the vault for future reference:

```
Path: escola/<subject>/<problem-slug>.md
```

With frontmatter:
```yaml
---
tags: [subject, topic, assignment]
title: "Question N — Short Description"
---
```

Include in the note:
- Full problem statement (or reference to it)
- All given data
- Step-by-step solution
- Final answer highlighted

Always commit vault changes:
```bash
cd /mnt/c/Users/keila/Mateus/vault
git add "escola/<subject>/<file>.md"
git commit -m "update vault: resolucao questao N - <topic>"
```

### Step 7: Offer to Save as Reference

After solving a non-trivial problem, ask if the user wants the solution saved to the vault. They appreciate having permanent notes they can review later.

## Pitfalls

- **OCR misreads**: Tesseract OCR on physics tables frequently reads "×10⁻⁵" as "x105" or "x108". The comma separator also gets lost — "2,4" becomes "24". Always interpret OCR output critically and cross-reference with known values.
- **Table image overwrites**: When extracting multiple images from a PDF page with `extract_image()`, subsequent saves overwrite previous ones. Use unique filenames (`table_0.jpeg`, `table_1.jpeg`).
- **Delta vs absolute**: NEVER confuse Δ (variation/change) with the absolute value. ΔL = L_final − L_initial, not just L_final.
- **β and γ from α**: Students often plug α directly into surface/volume formulas. Always calculate β = 2α or γ = 3α first.
- **Sign in cooling problems**: When ΔA or ΔL is negative, the algebra with negative signs confuses students. Walk through each sign flip explicitly (see Step 5).
- **No vision model**: The current provider (DeepSeek/open-code-zen) does NOT support vision/image inputs. Never try `vision_analyze` on PDF table images or graphs.
- **Extracting graph data without vision**: When you need to read data from a small, low-quality graph image but vision is unavailable, use this approach:

  1. Extract the image from PDF with `doc.extract_image(xref)` → save as JPEG/PNG
  2. Install tesseract + Portuguese language pack: `sudo apt-get install tesseract-ocr tesseract-ocr-por`
  3. Enlarge the image (6x) with PIL and OCR with `--psm 6` or `--psm 4`
  4. For axis labels and values, crop specific regions (y-axis area, x-axis area) and OCR each separately
  5. For the graph line itself, use binary pixel analysis:
     ```python
     gray = np.mean(np.array(img), axis=2)
     # Find dark pixels (the line)
     dark_mask = gray < threshold
     # Group by y to find where the line crosses each row
     for y in range(y_min, y_max):
         row_dark = np.where(dark_mask[y])[0]
         if len(row_dark) in [5, 10]:  # line, not text block
             x_avg = row_dark.mean()
     ```
  6. Map pixel coordinates to data values:
     ```python
     # Find axis boundaries from OCR and pixel analysis
     T_per_px = 60 / (x_60_label - x_origin)   # °C per pixel
     A_per_px = 100 / (y_origin - y_100_label)  # A-units per pixel
     T = (x_line - x_origin) * T_per_px
     A = (y_origin - y_line) * A_per_px
     ```
  7. **Limitation**: Pixel-level estimation has ~5-15% error. Best used when the answer key is available for cross-checking (work backwards from the answer to determine exact graph slope).

## Reference Files

- `references/coeficientes-dilatacao.md` — Tabela de coeficientes de dilatação linear (α) dos materiais comuns + fórmulas de dilatação linear, superficial e volumétrica + conversões de unidades. Use esta tabela para resolver problemas de física do T1.
