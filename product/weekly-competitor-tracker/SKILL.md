---
name: weekly-competitor-tracker
description: "Track weekly competitor changes and generate a delta-report from your markdown notes. Compares current files vs. last-week snapshot — no APIs, no code required. Use for Monday reviews, roadmap prep, or strategy meetings. Triggers: 'track competitor changes', 'weekly competitor report', 'что изменилось у конкурентов', 'отследи изменения конкурентов', 'дельта-отчёт по конкурентам'."
version: 1.0.0
---

# Weekly Competitor Tracker

This skill tracks weekly competitor changes by comparing your current markdown competitor notes against a saved snapshot from the previous week. It generates a structured delta-report showing what changed, what's new, and what was removed — with no APIs, no code, and no external services required.

**Input:**
- `competitors/` folder with one `.md` file per competitor (e.g., `competitors/acme.md`)
- Optional: `competitors/snapshot/` subfolder with previous-week versions of the same files

**Output:**
- `competitor-delta-YYYY-MM-DD.md` — structured delta-report saved to the `competitors/` folder

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

**Important:** All error messages, warnings, and instructions in subsequent steps must be output in the detected language.

---

## Instructions

### Step 1: Validate Input

1. Check that the user has provided a path to a `competitors/` folder.
   - If no folder provided:
     - EN: "No competitors folder provided. Create a `competitors/` folder with one .md file per competitor and try again."
     - RU: "Папка конкурентов не предоставлена. Создайте папку `competitors/` с одним файлом .md на каждого конкурента и повторите попытку."
   - If folder is empty (no .md files):
     - EN: "No competitor files found in the folder. Add at least one .md file and retry."
     - RU: "В папке не найдены файлы конкурентов. Добавьте хотя бы один файл .md и повторите попытку."

2. List all `.md` files in the `competitors/` folder (excluding the `snapshot/` subfolder).
   - These are the current-week competitor notes.
   - If only non-.md files are found:
     - EN: "Warning: only non-markdown files found. Proceed only if .md files exist."
     - RU: "Внимание: найдены только файлы не-Markdown. Продолжайте только если существуют файлы .md."

3. Check for `competitors/snapshot/` subfolder.
   - If it exists: load snapshot files for comparison (Step 3).
   - If it does not exist: this is a first run — proceed to baseline mode (Step 4).

### Step 2: Read Current Competitor Files

1. For each `.md` file in `competitors/`:
   - Extract the competitor name from the filename (e.g., `acme.md` → "Acme").
   - Read the file content.
   - Parse into sections by H2 headers (`## Section Name`).
   - If no H2 headers found: treat the entire file as one section called "General".
   - Extract key facts per section (bullet points, sentences with factual content).

2. Build a data structure: `{competitor_name: {section_name: [fact_list]}}` for all current files.

### Step 3: Compare Against Snapshot (if snapshot exists)

1. For each current competitor file, look for a matching file in `competitors/snapshot/`.
   - Match by filename (case-insensitive).
   - If current file has no snapshot counterpart: mark as "NEW — first appearance".
   - If snapshot has a file with no current counterpart: mark as "REMOVED from tracking".

2. For each matched competitor, compare section by section:
   - **Changed:** content differs between current and snapshot version.
   - **New:** section or fact present in current but not in snapshot.
   - **Removed:** section or fact present in snapshot but not in current.
   - **Unchanged:** content identical or semantically equivalent.

3. Assign significance rating to each change based on section type:
   - **High:** Pricing, Product, Features, Plans, Roadmap
   - **Medium:** Messaging, Homepage, UX, Positioning
   - **Low:** News, Blog, Social, About, Team

4. Determine overall status per competitor:
   - 🔴 Significant: at least one High-significance change found
   - 🟡 Minor: only Medium or Low changes found
   - 🟢 No changes: no differences detected

**Edge Cases:**
- If section names differ between current and snapshot: match by similarity (e.g., "Pricing" matches "Price"); note unmatched sections as "Structure changed".
- If snapshot file is empty or unreadable: treat as missing snapshot for that competitor; note in report.
- If competitor file has no sections (plain text only): perform paragraph-level diff; add note in detected language:
  - EN: "Diff quality limited — consider adding ## section headers."
  - RU: "Качество сравнения ограничено — рассмотрите добавление заголовков ## для секций."

### Step 4: Baseline Mode (no snapshot exists)

1. Generate a baseline summary (not a diff) for each competitor:
   - List all sections found.
   - Summarize key facts per section.
   - Do not attempt diff comparisons.

2. Add a prominent note at the top of the report (in detected language):
   - EN: > ⚠️ **First Run — No Snapshot Found**
   >    > This is your baseline report. To enable delta tracking next week, copy all files from `competitors/` to `competitors/snapshot/`.
   - RU: > ⚠️ **Первый запуск — снимок не найден**
   >    > Это базовый отчёт. Чтобы включить отслеживание изменений на следующей неделе, скопируйте все файлы из `competitors/` в `competitors/snapshot/`.

### Step 5: Generate Delta Report

1. Create the output file: `competitor-delta-YYYY-MM-DD.md` (use today's date).

2. Write report header:
   - Period: last snapshot date (from snapshot file metadata or "unknown") → today's date
   - Competitors tracked: count
   - Changes detected: total count of High + Medium changes

3. For each competitor, write a section following the Output Format below.

4. Write a Summary table at the end covering all competitors.

5. Add a reminder at the bottom (in detected language):
   - EN: > **Next step:** Copy current files from `competitors/` to `competitors/snapshot/` to update your baseline for next week.
   - RU: > **Следующий шаг:** Скопируйте текущие файлы из `competitors/` в `competitors/snapshot/` для обновления вашей базовой линии на следующую неделю.

6. Save file to `competitors/` folder.

### Negative Cases

- **No folder provided or folder empty:** Stop. Return error message with instructions (see Step 1, with language-appropriate messages).
- **User provides a single file path instead of a folder:** 
  - EN: "Expected a folder path, not a single file. Point to the `competitors/` folder."
  - RU: "Ожидается путь к папке, а не к одному файлу. Укажите путь к папке `competitors/`."
- **All competitor files are empty:** 
  - EN: "All competitor files appear to be empty. Add content to each file and retry."
  - RU: "Все файлы конкурентов пусты. Добавьте содержание в каждый файл и повторите попытку."

---

## Output Format

```markdown
# Competitor Delta Report — YYYY-MM-DD

**Period:** [last snapshot date or "First run (baseline)"] → [today's date]
**Competitors tracked:** N
**Changes detected:** N (High: N, Medium: N, Low: N)

---

## [Competitor Name]

**Overall:** 🔴 Significant changes / 🟡 Minor changes / 🟢 No changes

### What Changed
| Section | Change | Significance |
|---------|--------|-------------|
| Pricing | New Starter plan added at $49/mo | High |
| Messaging | Homepage headline updated | Medium |

### What's New
- [new fact not present in snapshot]

### What Was Removed
- [fact present in snapshot but gone now]

### Unchanged
- Product core features: no changes detected

---

## Summary

| Competitor | Status | Key Change |
|------------|--------|------------|
| Acme | 🔴 Significant | New pricing tier |
| Rival | 🟢 No changes | — |

---

> **Next step:** Copy current files from `competitors/` to `competitors/snapshot/` to update your baseline for next week.
```

**Field rules:**
- Significance: High (Pricing/Product/Features), Medium (Messaging/UX/Positioning), Low (News/Blog/Social)
- Emoji status: 🔴 = at least one High change; 🟡 = only Medium/Low changes; 🟢 = no changes
- "What Changed" table: only include actual changes, not stable items
- "Unchanged" section: brief summary only (not a full list of all stable facts)
- If first run (no snapshot): replace What Changed/New/Removed sections with "Baseline Summary" section listing current state
