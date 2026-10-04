---
name: generatemangapage
description: "Generate production-ready manga pages, chapter pages, covers, and panel sequences with strict recurring-character consistency. Use this when the user asks for a manga page, manga scene, chapter page, comic page, storyboard page, or character-consistent page generation. Before generating any page, inspect `img-memory`, create missing character sprites/reference sheets, make those images visible to image generation, then generate the final manga page."
---

# Generate Manga Page

Use this skill to generate manga pages with consistent character identity across pages.

The skill has two responsibilities:

1. Maintain `img-memory` for every recurring character.
2. Generate polished manga pages using those visible references.

## Parameters

Infer these from the user request:

- `page_type`: `story_page` | `cover` | `splash_page` | `character_intro` | `battle_page` | `dialogue_page` | `transition_page`
- `reading_direction`: `right_to_left` | `left_to_right`
- `page_size`: `print_manga_b5` | `webtoon_slice` | `square_preview` | `custom`
- `tone`: `shonen` | `seinen` | `shojo` | `dark_fantasy` | `comedy` | `cinematic`
- `ink_style`: `clean_black_white` | `screentone` | `high_contrast` | `sketchy_ink` | `color_manga`
- `panel_count`: `auto` or explicit count
- `characters`: names and roles present on the page
- `location`: scene setting
- `script`: narration, action beats, and dialogue intent
- `text_policy`: `no_text` | `exact_user_text_only` | `lettering_placeholders`
- `asset_group`: `main-characters` | `side-characters` | `monsters` | `locations` | `props` | custom slug
- `character_version`: `base` or a specific variant/evolution slug
- `version_type`: `base` | `variant` | `evolution`
- `memory_root`: default `img-memory`
- `output_root`: default `outputs/manga-pages`

Read [references/modes.md](references/modes.md) when the request is ambiguous.

## Non-Negotiable Rules

- Do not generate a manga page with a recurring character until that character has usable `img-memory`.
- If a character version is missing from `img-memory`, generate the character sprites/reference sheets first.
- Store recurring assets under `img-memory/assets/<asset-group>/<asset-slug>/versions/<version-slug>/`.
- Use `main-characters` for protagonists, rivals, long-running antagonists, and other core cast members.
- Never overwrite `base` when a character evolves, transforms, changes costume, ages, is injured across pages, or gains a persistent visual change. Create a new version.
- Make every reference image visible in the conversation before page generation. A file path in a prompt is not a visual reference.
- Preserve character identity: face shape, eyes, hair silhouette, body proportions, costume, symbols, accessories, palette, and line language.
- Only change pose, facial expression, camera angle, lighting, damage state, or temporary scene effects when the page requires it.
- Do not invent dialogue text. Use no text unless the user provides exact wording or asks for placeholders.
- Keep panel flow readable. Use clear gutters, deliberate camera staging, and a controlled focal hierarchy.
- Generate one production page at a time unless the user asks for a batch. Batch pages still need per-page memory checks.

## Workflow

### 1. Parse the page request

Extract:

- page number or chapter context
- characters appearing on the page
- asset group and version for each character
- setting and time of day
- action beats and emotional beats
- dialogue or narration policy
- reading direction
- desired panel count and page format

When a character is implied by role rather than name, assign a stable name or slug before memory work.

### 2. Inspect and prepare `img-memory`

Use [references/img-memory-contract.md](references/img-memory-contract.md).

Run the helper when useful:

```bash
python3 skills/generatemangapage/scripts/manage_img_memory.py init --project "Dungeonia Manga"
python3 skills/generatemangapage/scripts/manage_img_memory.py missing --characters "Aiko,Ryu"
```

For each page character version, require:

- `portrait-front.png`
- `full-body-front.png`
- `turnaround-sheet.png`
- `expression-sheet.png`
- `pose-sheet.png`
- `manifest.json`

If any required image does not exist for the selected version, generate it before page generation.

Use version folders:

```text
img-memory/assets/main-characters/aiko/versions/base/
img-memory/assets/main-characters/aiko/versions/awakened-ink-form/
img-memory/assets/monsters/obsidian-wyrm/versions/juvenile/
```

### 3. Generate missing character memory sprites

Use built-in `image_gen`.

Create missing memory images as reference sheets, not finished pages:

- `portrait-front.png`: face and hair identity anchor.
- `full-body-front.png`: body proportions, costume, accessories.
- `turnaround-sheet.png`: front, side, back, three-quarter views.
- `expression-sheet.png`: neutral, angry, shocked, smiling, determined, injured.
- `pose-sheet.png`: standing, running, attacking, defending, falling, close-up hand/weapon pose.

After generating each memory image:

- save it under `img-memory/assets/<asset-group>/<character-slug>/versions/<version-slug>/`
- update both the character-level and version-level `manifest.json` files
- keep the image visible or call the image-viewing tool before the page generation step

For evolutions and variations:

- preserve lineage markers from the base version
- document the exact visual change in the version manifest
- keep every future page on the same named version until the story changes it again
- create a new version for each persistent transformation, costume, injury, age state, or monster evolution stage

### 4. Build the manga page plan

Before generating the final page, write a compact page plan:

- panel order and size hierarchy
- camera shot for each panel
- character placement and emotion per panel
- action continuity between panels
- background continuity
- text policy

Use [references/prompt-rules.md](references/prompt-rules.md).

### 5. Generate the page

Use built-in `image_gen` with all relevant character memory images visible.

The prompt must state:

- use the images just shown as the visual references for named characters
- name the selected asset group and version for each character
- preserve each character's exact identity markers
- page size, reading direction, and panel count
- manga ink style and tone
- panel-by-panel action
- no generated text unless exact text is provided

### 6. Quality check

Reject and regenerate if:

- a recurring character is visually redesigned
- the same character changes face, hair, costume, or body proportions across panels
- panel order is confusing
- page has unreadable clutter or broken anatomy
- fake text, nonsense lettering, UI, labels, or watermarks appear
- important action crosses panel borders unintentionally
- the page ignores the requested scene beat

### 7. Save outputs and update memory

Expected output structure:

```text
outputs/manga-pages/
  chapter-001/
    page-001.png
    page-001-prompt.md
    page-001-plan.md
    page-001-meta.json
```

Also record page usage in:

```text
img-memory/pages/page-001.json
```

## Resources

- `references/modes.md`: page types, layouts, and default production choices.
- `references/prompt-rules.md`: manga prompt rules and page quality standards.
- `references/img-memory-contract.md`: required character memory structure.
- `scripts/manage_img_memory.py`: helper for memory initialization, validation, and metadata registration.
