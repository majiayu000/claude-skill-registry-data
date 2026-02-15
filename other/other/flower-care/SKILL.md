# flower-care

name: flower-care
description: Analyze flower images for identification, health diagnosis, and care recommendations (output in Polish)
argument-hint: [image-path] [--name flower-name] [--issue problem] [--indoor|outdoor] [--quick]
allowed-tools: Read, WebSearch, WebFetch, Write, Glob, Edit, Bash
user-invocable: true

---

## Overview

Multimodal plant analysis skill using Claude's vision capabilities. Identifies flowers from photos, diagnoses health issues, and generates comprehensive care guides in Polish.

**Input:** Image path + optional flags
**Output:** Polish care guide saved to Obsidian inbox + local archive

---

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `image-path` | ✅ | Path to flower image (JPG/PNG/HEIC supported, auto-converts iPhone photos) |
| `--name` | ❌ | Known flower name (helps narrow identification) |
| `--issue` | ❌ | Specific problem to diagnose (yellowing, wilting, spots, pests) |
| `--indoor` | ❌ | Indoor environment (default) |
| `--outdoor` | ❌ | Outdoor environment |
| `--quick` | ❌ | Skip deep research, basic care only |

---

## Workflow

### Phase 1: Parse Arguments

Extract from `$ARGUMENTS`:
- **image-path:** Required — validate file exists
- **--name:** Optional plant name hint
- **--issue:** Optional specific problem
- **--indoor/--outdoor:** Environment context (default: indoor)
- **--quick:** Reduced research depth

**Validation:**
- If image path doesn't exist → error: "Nie znaleziono pliku: [path]. Sprawdź ścieżkę do zdjęcia."
- Convert relative paths to absolute

### Phase 1.5: Image Preprocessing

**Always convert image to optimized JPG before analysis.**

iPhone photos often use HEIC format and can be very large. This phase ensures compatibility and performance.

**Steps:**
1. Check file format using `file` command
2. If HEIC/HEIF or >2MB, convert using `sips`:
   ```bash
   # Convert HEIC to JPG
   sips -s format jpeg "[input]" --out "/tmp/plant-analysis.jpg"

   # If still >2MB, resize to max 2000px width
   sips -Z 2000 "/tmp/plant-analysis.jpg"

   # Check final size
   ls -la "/tmp/plant-analysis.jpg"
   ```
3. Use converted file at `/tmp/plant-analysis.jpg` for Phase 2

**Conversion rules:**
- HEIC/HEIF → always convert to JPG
- PNG/JPG >2MB → resize to max 2000px width
- PNG/JPG ≤2MB → use original (no conversion needed)
- Other formats → convert to JPG

**Output path:** `/tmp/plant-analysis.jpg` (used for all subsequent analysis)

### Phase 2: Image Analysis (Multimodal)

Use **Read tool** on preprocessed image (`/tmp/plant-analysis.jpg` or original if no conversion needed).

**Identify and document:**
- Species identification: common name, botanical name, family
- Confidence level: High/Medium/Low
- Visual observations:
  - Overall health impression
  - Leaf condition (color, texture, spots, edges)
  - Stem/trunk condition
  - Soil visible? Moisture level?
  - Pot type/size if visible
  - Any pests visible?
  - Growth pattern (leggy, compact, drooping)

### Phase 3: Health Diagnosis

Load `diagnosis-guide.md` and match observations to conditions.

**Urgency levels:**
- 🔴 Critical/High — immediate action needed
- 🟡 Medium — address within days
- 🟢 Low — monitor and adjust

**Output:** List of detected issues with confidence + urgency.

### Phase 4: Research Care Requirements

**WebSearch queries (4-6 searches):**
1. "[flower-name] care guide watering light humidity"
2. "[flower-name] indoor/outdoor care tips"
3. "[flower-name] common problems treatment"
4. "[flower-name] seasonal care calendar"
5. If issues detected: "[flower-name] [specific-issue] treatment"
6. "[flower-name] propagation methods"

**Target sources (priority order):**
- **Tier 1:** RHS, Missouri Botanical Garden, UCANR
- **Tier 2:** Gardening Know How, The Spruce, Houseplant Central
- **Tier 3:** Reddit r/houseplants, forums (signal validation)

**Extract:**
- Watering frequency + method
- Light requirements (hours, intensity, direction)
- Humidity + temperature ranges
- Soil type + fertilizer schedule
- Seasonal adjustments
- Common problems + solutions

### Phase 5: Treatment Research (if issues detected)

For each diagnosed issue, **WebSearch:**
- "[issue] treatment [flower-name]"
- "[issue] organic remedy plants"
- "[issue] prevention indoor plants"

**Build treatment plan:**
- Immediate actions (today)
- Short-term (this week)
- Long-term prevention
- Products/tools needed

**Skip if:** No issues detected or `--quick` flag used.

### Phase 6: Synthesize Care Matrix

Combine research into care matrix:

| Aspekt | Wymagania | Uwagi |
|--------|-----------|-------|
| 💧 Podlewanie | frequency, method | seasonal adjustments |
| ☀️ Światło | hours, intensity | window direction |
| 💨 Wilgotność | % range | how to increase |
| 🌡️ Temperatura | min-max °C | danger zones |
| 🪴 Podłoże | type, drainage | repot frequency |
| 🧪 Nawożenie | NPK ratio, frequency | dormancy pause |

### Phase 7: Generate Seasonal Calendar

Create month-by-month care adjustments:
- **Wiosna (Spring):** Active growth, increase watering, start fertilizing
- **Lato (Summer):** Peak care, watch for pests, humidity
- **Jesień (Fall):** Reduce watering, stop fertilizing, dormancy prep
- **Zima (Winter):** Minimal water, no fertilizer, protect from drafts

**Skip calendar if:** `--quick` flag used.

### Phase 8: Verification Checklist

Before output, verify:
- [ ] Plant identification confident (≥Medium)?
- [ ] All care aspects covered (water/light/humidity/temp/soil/fertilizer)?
- [ ] Issues diagnosed with treatment plan?
- [ ] Seasonal variations included?
- [ ] All claims cite sources?
- [ ] No hallucinated care data?
- [ ] Polish translation accurate?

### Phase 9: Generate Output

Follow `output-template.md` format.

**Translation rules:**
- Section headers in Polish
- Care instructions in Polish
- Keep botanical names in Latin
- Keep source URLs as-is
- When uncertain: "przesuszenie (underwatering)"

### Phase 10: Save Output

**Save to both locations:**

1. **Local archive:** `findings/plants/[flower-slug].md`
2. **Obsidian inbox:** `/Users/marcin.skalski@konghq.com/Library/Mobile Documents/iCloud~md~obsidian/Documents/second-brain/0_Inbox/plant-[flower-slug].md`

**Update state:**
- Append to `findings/plants/.plant-history`: `[date] [flower-name] [image-path]`
- Keep under 200 lines (trim oldest if exceeded)

---

## Configuration

### Defaults
- Environment: indoor
- Output language: Polish
- Research depth: full (unless --quick)
- Save locations: both local + Obsidian

### Thresholds
- Identification confidence: report if <Medium
- Issue urgency: Critical/High → treatment first in output
- Source minimum: 3 sources before generating output

### Quick Mode
- Skip Phase 5 (treatment research)
- Skip Phase 7 (seasonal calendar)
- Reduce WebSearch to 2-3 queries
- Output: basic care matrix only

---

## Error Handling

### Image Not Found
```
Error: Nie znaleziono pliku: [path]. Sprawdź ścieżkę do zdjęcia.
```

### Image Conversion Failed
- If `sips` fails → try with `magick` (ImageMagick) as fallback
- If both fail → error: "Nie udało się przetworzyć zdjęcia. Spróbuj z plikiem JPG/PNG."
- Common issues: corrupted file, unsupported format, insufficient disk space

### Unidentifiable Plant
- If `--name` provided → use that name for research
- If no `--name` → error: "Nie udało się zidentyfikować rośliny. Użyj --name [nazwa]."

### WebSearch Fails
- Log failure, continue with other sources
- Minimum 2 sources required for output
- If <2 sources → warn: "Ograniczone źródła — zalecana weryfikacja."

### No Issues Detected
- Skip Phase 5
- Generate healthy plant care guide
- Include preventive tips instead of treatment

---

## Example Invocations

```bash
# Basic usage (iPhone HEIC supported)
/flower-care ~/photos/my-orchid.heic

# With hints
/flower-care ./monstera.jpg --name "monstera deliciosa"

# iPhone photo from AirDrop
/flower-care ~/Downloads/IMG_1234.HEIC --name "kalanchoe"

# Problem-focused
/flower-care ~/plants/sick-fern.png --issue "yellow leaves" --indoor

# Quick assessment
/flower-care garden-rose.jpg --outdoor --quick

# Full diagnosis
/flower-care ~/Desktop/plant.jpg --name "ficus elastica" --issue "dropping leaves"
```
