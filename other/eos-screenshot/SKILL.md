---
name: eos-screenshot
description: Capture screenshots of EmptyOS UI for blog posts and the marketing site, with privacy + branding redaction baked in. Works against any URL — localhost, demo.binbian.net, an exported bundle. Pre-blurs selectors you specify, then scans visible text against `.eos-personal` and `.eos-branding` patterns and refuses to write the file when a leak is detected (unless `--force`). Outputs to `{vault}/30_Resources/Published/media/<slug>.png` with a sidecar `<slug>.alt.txt` and a manifest entry in `media/.shots.toml`. Use when the user says "screenshot this", "grab a shot of /journal", "shoot the capability inspector", or wants article images for a Published post. NOT for editing an image you already have (use eos-image-edit) and NOT for authoring a diagram (use eos-article-diagrams).
---

# EmptyOS Screenshot Skill

Article and site screenshots get reused across LinkedIn posts, the EmptyOS site, and docs. Three risks repeat every time:

1. **Personal data leak** — real journal entries, contact names, expense rows, paths, coords. Code is gated by `scripts/check-personal.py`; pixels weren't.
2. **Branding leak** — UI text mentioning Obsidian / Suno / Kindle / etc. (Rule 14). Same posture: code-gated, pixels weren't.
3. **Reproducibility** — the next post wants the same shot at the same dimensions; ad-hoc capture drifts.

This skill closes those gaps with the smallest possible workflow: navigate, blur what you say to blur, scan visible text against the same regex sets the code checks use, fail loudly on a hit, write to the published-media folder.

## When to use

- User says "screenshot the X page", "shoot Y for the article", "grab a hero image"
- After drafting a post in `30_Resources/Published/` that references `media/...png` files that don't exist yet
- When refreshing stale screenshots on the live site

Skip if: the asset is a chart/SVG (those come from data, not screenshots — use `eos-article-diagrams`), a non-UI photo (cover images, etc.), or an **already-captured image with no live DOM** — a phone screenshot the user AirDropped, an exported photo. This skill blurs *CSS selectors on a live page*; to blur pixel regions + crop chrome on an existing image file, use `eos-image-edit` (`scripts/redact_screenshot.py`).

## Prerequisites

- Playwright installed: `pip install playwright pytest-playwright && playwright install chromium`
- Pillow installed: `pip install pillow` (for selector-region cropping)
- A reachable target URL — typically `http://localhost:9000` (default) or `https://demo.binbian.net/?token=...`
- Vault connected (`.claude/vault-connection.json`) so output paths resolve

## Arguments

| Arg | Default | Meaning |
|---|---|---|
| `--url URL` | `http://localhost:9000/` | Page to capture. May include path + query. |
| `--selector SEL` | (none) | Crop to a single element instead of full page (`bounding_box`). |
| `--blur "sel1,sel2"` | (none) | CSS selectors to blur *before* capture. Use for known-personal regions (e.g. `.user-name`, `[data-personal]`). |
| `--out NAME` | derived | Output filename stem under `media/`. Required if `--scenario` not set. |
| `--scenario NAME` | (none) | Named recipe from `scenarios.toml` — sets url/selector/blur/out together. |
| `--alt "TEXT"` | (none) | Alt text written to sidecar `<stem>.alt.txt` and manifest. |
| `--viewport WxH` | `1440x900` | Browser viewport. Use `390x844` for mobile shots. |
| `--wait MS` | 1000 | Extra wait after `domcontentloaded` for dashboards / lazy panels. |
| `--prep "JS"` | (none) | JS to run after navigation, before capture. Use to flip toggles, dismiss modals. |
| `--force` | false | Skip the redaction-pass abort. **Use only after eyeballing the failing match.** |

## Workflow

### 1. Read vault + site source

```python
import json
with open(".claude/vault-connection.json") as f:
    vault = json.load(f)["vault_path"]
media_dir = f"{vault}/30_Resources/Published/media"
```

### 2. Resolve scenario (if any)

If `--scenario` set, look up the recipe in `scenarios.toml` (in this skill folder). Recipes pin url/selector/blur/out so re-shooting an article asset is one command. Example:

```toml
[capability-inspector]
url = "http://localhost:9000/system"
selector = "#capability-inspector"
out = "ai-relationship-capability-inspector"
alt = "Capability Inspector showing the Simulate Capability Offline toggle"

[ai-offline-banner]
url = "http://localhost:9000/journal/"
prep = "await fetch('/api/system/simulate-offline?on=1', {method:'POST'})"
out = "ai-relationship-offline-banner"
alt = "Journal page with the AI offline banner shown after simulating capability offline"
```

CLI args override scenario fields when both supplied.

### 3. Capture

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

w, h = map(int, viewport.split("x"))
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": w, "height": h})
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_timeout(wait_ms)
    if prep_js:
        page.evaluate(prep_js)
        page.wait_for_timeout(wait_ms)
    if blur_selectors:
        page.add_style_tag(content=f"{blur_selectors} {{ filter: blur(10px) !important; }}")
    visible_text = page.locator("body").inner_text()
    if selector:
        page.locator(selector).screenshot(path=str(tmp_png))
    else:
        page.screenshot(path=str(tmp_png), full_page=True)
    browser.close()
```

### 4. Redaction pass (the gate)

Load patterns from project root:

```python
import re
def load_patterns(path):
    out = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.append(re.compile(line))
    return out

patterns = load_patterns(".eos-personal") + load_patterns(".eos-branding")
hits = [(p.pattern, m.group(0)) for p in patterns for m in p.finditer(visible_text)]
if hits and not force:
    print("REDACTION FAIL — visible text matched protected patterns:")
    for pat, snippet in hits:
        print(f"  {pat!r}: {snippet!r}")
    print("Either add the offending element to --blur, navigate to a clean state, or pass --force after review.")
    tmp_png.unlink(missing_ok=True)
    raise SystemExit(2)
```

The redaction pass scans **visible text** (DOM `inner_text`), not pixels — much more reliable than OCR for short UI strings, and instant. It misses text rendered as images (charts, screenshots-of-screenshots), so for those, eyeball the result. The `--blur` arg covers the regions you already know are sensitive; the pattern scan covers the ones you forgot about.

### 5. Write outputs + manifest

```python
final_png = Path(media_dir) / f"{out_stem}.png"
final_png.parent.mkdir(parents=True, exist_ok=True)
tmp_png.replace(final_png)
if alt_text:
    (final_png.with_suffix(".alt.txt")).write_text(alt_text, encoding="utf-8")

# Append to media/.shots.toml
manifest = Path(media_dir) / ".shots.toml"
entry = f'\n[{out_stem}]\nurl = "{url}"\nviewport = "{viewport}"\ncaptured_at = "{datetime.utcnow().isoformat()}Z"\nalt = {alt_text!r}\n'
with manifest.open("a", encoding="utf-8") as f:
    f.write(entry)
```

### 6. Print result

```
✓ Captured: 30_Resources/Published/media/ai-relationship-offline-banner.png  (1440×900, 312KB)
  Alt: Journal page with the AI offline banner...
  Manifest: media/.shots.toml updated
```

## Rules

- **Never `--force` blindly.** A redaction hit is the skill working. Read the match, decide whether to blur the region, navigate to a clean state, or accept the leak (rare, e.g. a generic word matched too broadly — then patch the pattern).
- **No silent overwrites.** If the target file exists, abort unless `--force`. Re-shooting from the same scenario is fine; surprise overwrites aren't.
- **Don't commit the .shots.toml manifest if vault is gitignored** — it lives in the published-media folder which goes to the live site, so OK.
- **Don't `--force` to publish a personal-vault shot** — instead, navigate the daemon to a sanitized state (sample journal entry, generic project), then re-capture. The redaction pass is downstream defense; clean source is upstream.

## Recipe registry (scenarios.toml)

Add entries for shots reused across multiple posts. Keep one-off shots out of the registry — those are CLI-arg invocations.

When this article ("A Healthy Relationship with AI") gets shot, the recipes are:

- `capability-inspector` — `/system` cropped to the inspector card
- `ai-offline-banner` — `/journal/` after the simulate-offline toggle is flipped
- `ai-on-off-compare` — pair shot, two captures stitched (do this manually or extend the skill later)

## Graduation paths

- **Selector-based blur library** — once we accumulate a list of `[data-personal]` selectors that always need blurring, bake them into a default `--blur` set. Also: add `data-personal` attributes to the personal-leak surfaces in the codebase, so the skill defaults to blurring them.
- **OCR fallback for chart shots** — when a screenshot of a chart bakes in axis labels with personal numbers, DOM-text scanning misses it. Add Tesseract pass behind a `--ocr` flag.
- **Stitching** — side-by-side / before-after composites. Extend after the third article that needs it.
- **CI hook** — pre-commit / pre-deploy check that every `media/*.png` referenced in a `publish: true` post has a manifest entry, to catch hand-dropped images that bypassed the gate.
