---
name: screenshot-context-builder
description: >
  Rename batches of generic screenshots into descriptive names, and optionally turn a bug-report or feedback prompt into a polished HTML report that embeds the real screenshots beside each issue. Use when the user wants to: rename screenshots with generic names (e.g. "Screenshot 2026-04-08...", "SCR-...png"), improve a voice-dictated or AI-rewritten prompt that references images, build a readable bug/feedback report from screenshots, attach exact image references to a prompt, or do any combination of these. Triggers on: "rename my screenshots", "rename these images", "my prompt references screenshots", "I dictated this prompt", "turn these screenshots into a report", "prepare screenshots for Claude", "improve my prompt with the images".
---

# Screenshot Context Builder

This skill does two related jobs: give screenshots meaningful names, and turn a rough (often voice-dictated) bug/feedback prompt into an accurate, readable **HTML report** where each issue sits next to the real screenshots that prove it.

The single idea that makes the output trustworthy: **the images are the ground truth.** A dictated prompt is a lossy account of what the user saw — names are misheard, messages are paraphrased, the wrong screenshot gets associated with a bug. Your job is to reconcile the prompt against the pixels and let the images win every disagreement.

## When the user arrives

Read what they already gave you and ask only for what's missing:

1. **Folder path** — where are the images? (required)
2. **Domain/project context** — what is the app/project? A sentence helps naming and analysis. If they shared a prompt, mine it for context.
3. **Mode** — rename only, or rename + build the report?
4. **Image path format for the report** — by default the HTML is saved *in the images folder* so `src="filename.png"` resolves with no path. Only ask if they need a different root (e.g. the report will live elsewhere, or they want a relative `images/...` path for a repo).

---

## Mode A — Rename images

### 1. List the images
List every image in the folder (png, jpg, jpeg, gif, webp). Tell the user the count.

<!-- runtime-slot:first-pass -->
### 2. First-pass names with Haiku (in parallel)
Split into batches of ~7 and spawn a Haiku subagent per batch (all in the same turn). Give each: the file paths, the domain context, and this instruction:

> For each image, read it and propose a kebab-case filename, no accents/special chars, max 60 chars, capturing (1) the section/feature visible and (2) the main element/problem/state shown. Use grouping prefixes (e.g. `grille-`, `modal-`, `vide-`, `filtre-`, `footer-`). Return one line per image: `ORIGINAL.png -> new-name.png`. Also add an `OBSERVATIONS:` section with exact strings you can read (names, totals, labels, messages).

Treat these names as a **draft**. Haiku reads thumbnails and will sometimes mislabel — e.g. naming a file `grille-interne-*` when it actually shows external data, or `soumission-*` for a screen that's merely "open". Do not ship these blindly.
<!-- /runtime-slot:first-pass -->

### 3. Verify before committing (do this yourself, not via Haiku)
For any name you're unsure about — and at minimum a spot-check across the batch — open the image and confirm the name matches what's actually on screen. When small text decides the label (a status badge, a filter state, which employee is shown), use the zoom helper to read it (see "Reading small text"). Fix names that mislead; a filename that lies is worse than a generic one because it will later be cited as evidence for the wrong thing.

### 4. Apply renames
Rename with `mv` via Bash. Guard against collisions (append `-2`, `-3` for near-duplicates). Confirm the final count.

---

## Mode B — Rename + build the HTML report

Do Mode A first, then build the report. The report is the deliverable, so the accuracy work below is where most of the value is.

### Why the dictated prompt can't be trusted verbatim
- It was dictated and rewritten by another model, so **proper nouns are misspelled** (a name said aloud becomes "Giro" when the screen says "Gireaud").
- Messages and button labels are **paraphrased**, not quoted.
- The user often wrote it **before/while** taking screenshots, so a described screen may not be the one that got captured.
- The same bug is mentioned in several places without pointing at a specific image.

### 5. Read the images yourself and extract ground truth
Go through the screenshots (not via Haiku — you are writing the report, so you need to see them). For each, capture the exact, on-screen strings the report will rely on: employee/person names, company names, hour totals, error and empty-state messages, button labels, status badges, filter states, column headers, URLs/IDs.

**Reading small text.** Full-resolution screenshots render UI text illegibly when read whole. Crop the region and upscale it 2–3× first, using the bundled helper:

```
python scripts/zoom_crop.py --src shot.png --info                      # print size
python scripts/zoom_crop.py --src shot.png --box 620 320 1320 650 --scale 2 --out /tmp/crops/modal.png
python scripts/zoom_crop.py --src shot.png --frac 0 0.9 1 1 --scale 2 --out /tmp/crops/footer.png
```

Save crops to a scratch dir, then read them. Re-crop with adjusted coordinates if you guessed wrong (screenshots often have browser chrome at the top, so app content starts lower than you'd expect).

### 6. Reconcile prompt ↔ images
- **Names & messages:** wherever the dictation disagrees with a screen, use the spelling/wording from the image. Do this silently in the output, but it's worth flagging the notable corrections to the user (e.g. "the prompt said 'Ludovic Giro'; the screen shows 'Ludovic Gireaud' — I used the latter").
- **Image ↔ bug fit:** for every issue, confirm the screenshots you attach actually depict *that* problem in *that* state (right filter, right status, right data present/absent). Re-assign images that don't fit. This is the most common defect to catch.
- **Grouping:** when two, three, or four images together explain a problem better (e.g. the empty state on one filter vs. another, or a before/after), group them under that issue — this is good, not clutter.

### 7. Build the report from the template
Use `assets/report-template.html` as the skeleton — don't hand-roll new CSS. It's a dark-mode, accessible layout with a sticky table of contents, numbered sections, per-issue cards, a "repères/landmarks" block for the verified facts, and a click-to-zoom lightbox for the thumbnails. Fill it in:

- **Structure:** one `<section>` per functional area; one `.issue` card per distinct bug. Mark a critical area with `class="major"`.
- **Repères block:** populate it with the exact strings you transcribed (names, labels, statuses, totals). This is what tells the reader the report is grounded in the pixels.
- **Thumbnails:** at the end of each issue, embed the real screenshots as `<figure class="thumb">` with the bare filename in `src` (the HTML sits in the images folder) — or the path format the user requested. The caption is the filename.
- **Accuracy:** use exact on-screen values, never generic placeholders.
- **Missing context:** fold in anything the user said verbally but didn't write — scale, user role, technical stack, conventions (e.g. "Fluent UI only, no emojis").
- **Tone & intent:** factual and problem-focused. Describe the problem; don't prescribe the fix. Don't invent sections the user didn't ask for (no priority matrices or checklists unless requested). If you spotted something in an image the user didn't mention, add it as a brief note marked "(observé dans l'image)" / "(observed in image)".
- **Language:** write the report in the **same language as the original prompt**. Never switch languages.

Save the HTML in the images folder (so thumbnails resolve), then share the path. If the user explicitly wants Markdown instead, that's a fine fallback — but the default deliverable is HTML.

### 8. Final checks
- No original generic names (`Screenshot ...`, `SCR-...`) remain; no duplicate names.
- Every `src` in the HTML resolves to a file that exists in the folder (grep the filenames and check).
- Each issue's images genuinely depict that issue (filter/status/data state matches the text).
- Names, messages, and labels match the screens, not the dictation.
- Report language matches the original prompt.

---

## Naming conventions reference

| Pattern | Use for |
|---|---|
| `grille-` | Data grids / time-entry tables |
| `filtre-` | A specific filter/tab state |
| `footer-` | Footer / totals bars |
| `modal-` | Dialogs, pop-ups |
| `vide-` | Empty states |
| `erreur-` | Error states |
| `soumission-` / `verification-` | Submission / review flows |
| `resume-` / `dashboard-` | Summary / overview screens |
| `notes-` / `settings-` | Notes panels / configuration |

Adapt prefixes to the domain. Crucially, name from what the image **actually shows**, not from what a sibling screen or the prompt implies — verify (Mode A step 3) before trusting a prefix.

## Bundled resources
- `scripts/zoom_crop.py` — crop + upscale a screenshot region so its text is legible. Run with `--info` to get the size, then `--box`/`--frac` + `--scale`.
- `assets/report-template.html` — the report skeleton (dark mode, TOC, issue cards, landmarks block, lightbox). Read its top comment for placeholders.
