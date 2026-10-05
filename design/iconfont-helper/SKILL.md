---
name: iconfont-helper
description: Search iconfont.cn for public SVG icon candidates, save multiple results, and choose the best-looking asset for articles, slides, videos, demos, or HTML compositions. Use when the user needs Iconfont SVGs, visual symbols, lightweight illustration assets, or design-led icon selection.
---

# Iconfont Helper

## Core Goal

Find useful SVG candidates from Iconfont without turning icon selection into a
random first-result pick. Start from the scene or design need, search broadly,
save several candidates, preview them, and choose the icon that looks best in the
final layout.

This skill is for public SVG asset discovery only. It does not manage Iconfont
projects, upload icons, sync account assets, or preserve any login state.

## Workflow

1. Translate the visual need into 2-4 search keywords. Use concrete nouns,
   actions, objects, or metaphors instead of only the article title.
2. Search Iconfont with the bundled helper and save multiple SVG candidates.
3. Review the saved SVG files and `search-response.json`.
4. Choose by clarity, beauty, line weight, fill style, recognizability, and
   whether it matches the surrounding design.
5. Keep icon style consistent inside one deliverable. Avoid mixing thin line
   icons, heavy filled icons, flat cute icons, and complex illustrations unless
   the contrast is intentional.
6. If Iconfont search fails or the candidates look poor, use another open icon
   source, draw a simple SVG, or build the shape in HTML/CSS instead of forcing a
   bad icon into the work.

## Helper Command

```powershell
python "skills/iconfont-helper/scripts/search_iconfont_svg.py" "keyword" --out "<PROJECT_FOLDER>/assets/iconfont" --limit 12 --all
```

Optional style filters:

```powershell
python "skills/iconfont-helper/scripts/search_iconfont_svg.py" "keyword" --type line --out "<PROJECT_FOLDER>/assets/iconfont" --all
python "skills/iconfont-helper/scripts/search_iconfont_svg.py" "keyword" --type fill --out "<PROJECT_FOLDER>/assets/iconfont" --all
```

The helper calls:

```text
https://www.iconfont.cn/api/icon/search.json
```

It reads each result's `show_svg` field and writes the SVG candidates locally.
By default it saves up to three SVGs; pass `--all` to save every returned SVG
candidate within the requested limit.

## Login And Token Boundary

Some Iconfont requests may work without a token; some environments may require
a local `ctoken`. If needed, provide it only at runtime:

```powershell
$env:ICONFONT_CTOKEN = "<LOCAL_TOKEN>"
python "skills/iconfont-helper/scripts/search_iconfont_svg.py" "keyword" --out "<PROJECT_FOLDER>/assets/iconfont" --all
```

Never commit `ctoken`, cookies, browser profiles, cache files, logs, sessions,
private project folders, or account-specific Iconfont data.

## Validation Checklist

- Multiple SVG candidates were saved when the design needs selection.
- `search-response.json` exists for traceability.
- The selected SVG looks good in the actual layout, not just in isolation.
- No token, cookie, account data, local private path, cache, log, or session file
  was committed.
- If the icon will be published, the usage fits the target project's licensing
  and attribution requirements.
