---
name: daftai-subtitle-translator
description: >
  Translate subtitle files (SRT/VTT) between languages. Auto-detect source language,
  batch translate with count validation, optional bilingual merge output.
  Use when user asks to "translate subtitles", "翻译字幕", "subtitle translation",
  or needs subtitles converted to another language.
---

# Subtitle Translator

Translate subtitle files between languages with accuracy validation.

> **Scripts**: All scripts are in `scripts/` relative to this SKILL.md.
> **CRITICAL**: When running any `bun scripts/...` command, you MUST set the working directory (`cwd`) to this skill's base directory. Do NOT run from the user's project directory.

## Workflow

```
- [ ] Step 1: Input validation (file exists, format supported)
- [ ] Step 2: Detect source language + confirm target language
- [ ] Step 3: Preprocess (VTT → SRT if needed)
- [ ] Step 4: Terminology scan (extract terms, build session glossary)
- [ ] Step 5: Translate subtitles (batch, with validation)
- [ ] Step 6: Review (optional, check consistency & quality)
- [ ] Step 7: Bilingual merge (optional)
- [ ] Step 8: Output report
```

### Flow

```
Input → [Step 1: Validate] → File exists, format check
        ↓
[Step 2: Language] → Auto-detect source + confirm target
        ↓
[Step 3: Preprocess] → VTT → SRT convert (if needed)
        ↓
[Step 4: Term Scan] → Extract terms, build session glossary
        ↓
[Step 5: Translate] → Batch translate (20 lines) + count validation
        ↓
[Step 6: Review] → Consistency & quality check (optional)
        ↓
[Step 7: Merge] → Bilingual SRT (if requested)
        ↓
[Step 8: Report] → Output paths + counts
```

---

### Step 1: Input Validation

**Goal**: Confirm subtitle file exists and format is supported

1. User provides subtitle file path
2. Supported formats: `.srt`, `.vtt`, `.ass`, `.ssa`
3. Verify file exists and is readable

---

### Step 2: Language Detection

**Goal**: Determine source and target languages

1. Auto-detect source language:
   ```bash
   bun scripts/detect_language.ts "<subtitle_path>"
   ```
   - From filename (e.g., `subtitles_en.srt` → `en`)
   - From content (Chinese characters → `zh`, Latin → `en`, etc.)

2. Confirm with user if detection is uncertain

3. Confirm target language:
   - If user already specified → use it
   - Otherwise → ask user

**Common language codes**: `en`, `zh`, `ja`, `ko`, `fr`, `de`, `es`

---

### Step 3: Preprocess

**Goal**: Ensure input is in SRT format for translation

If input is VTT format:
```bash
bun scripts/convert_vtt_to_srt.ts "<input.vtt>" "<output.srt>"
```

If input is already SRT → use directly.

---

### Step 4: Terminology Scan

**Goal**: Before translating, scan the entire subtitle file to extract terms and build a session glossary for consistency.

1. **Scan all subtitle text**: Read through all subtitle entries, identify:
   - Proper nouns (person names, product names, company names)
   - Technical terms and jargon
   - Recurring phrases or expressions
   - Terms with non-obvious translations

2. **Build session glossary**: For each identified term, decide the translation upfront:
   - Check against the built-in Term Mapping below
   - Check against user-provided custom term mappings (highest priority)
   - For terms not in any glossary, determine the industry-standard translation
   - Record all decisions as a working term table

3. **Use session glossary throughout**: All batches in Step 5 must follow this glossary. Same term = same translation, no exceptions.

> For short subtitle files (< 50 entries), this step can be done mentally while translating the first batch. For longer files, explicitly list the session glossary before starting translation.

#### Built-in Glossary

Load built-in glossary for the language pair: [references/glossary-en-zh.md](references/glossary-en-zh.md)

Merge priority (highest → lowest): user-provided custom mappings > session glossary (extracted in scan) > built-in glossary

---

### Step 5: Translate Subtitles

**Goal**: Translate all subtitle lines accurately

**Output path**: `<output_dir>/<filename>_<target_lang>.srt`
- Example: `output/video_zh.srt`
- Default output_dir: same directory as input file, under `output/` subfolder

#### Translation Principles

1. **Accuracy**: Preserve original meaning faithfully — facts, data, and logic must match the original exactly
2. **Meaning over words**: Translate what the speaker means, not just what the words say. When a literal translation sounds unnatural, restructure freely to express the same meaning in idiomatic target language
3. **Fluency**: Natural target language word order and expression
4. **Conciseness**: Conversational tone, no redundancy — subtitles must be brief
5. **Figurative language**: Interpret metaphors, idioms, and figurative expressions by their intended meaning rather than word-for-word. Replace with natural target-language equivalents that convey the same idea
6. **Emotional fidelity**: Preserve the emotional connotations of word choices. Words that carry feelings (e.g., "alarming", "fascinating") should evoke the same response in target-language viewers
7. **Consistency**: Follow the session glossary from Step 4 — same term = same translation throughout the entire file
8. **Punctuation**: No period (。) at end of subtitle lines for Chinese (`zh`)

#### Batch Translation

- Translate **20 subtitle entries per batch**
- Maintain SRT structure: preserve index numbers and timestamps exactly
- Only translate the text content lines

#### Count Validation (MUST execute)

After translation is complete, validate line counts:

```bash
grep -c "^[0-9]\+$" <original.srt>
grep -c "^[0-9]\+$" <translated.srt>
```

- Translated count **MUST** equal original count
- If mismatch → **fix it immediately**. NEVER say "only off by one, close enough"
- Re-run validation after fix

---

### Step 6: Review (Optional)

**Trigger**: Automatically for files with 100+ entries. For shorter files, skip unless user requests "review" / "审校" / "检查".

**Goal**: Post-translation quality check

1. **Terminology consistency**: Scan the translated file — verify every occurrence of a term from the session glossary uses the same translation. Flag and fix any inconsistencies.

2. **Missing translations**: Check for any untranslated source-language text left in the output (e.g., a line accidentally skipped or left in English).

3. **Subtitle length**: For Chinese (`zh`) target, flag any subtitle line exceeding ~18 characters — these may be too long to read comfortably on screen. Suggest shorter alternatives.

4. **Meaning spot-check**: Sample 5-10 entries spread across the file, compare with source — verify meaning is preserved and expression is natural.

If issues are found → fix in place and re-run count validation.

---

### Step 7: Bilingual Merge (Optional)

**Trigger**: User requests bilingual subtitles, or asks for both languages in one file.

**Output path**: `<output_dir>/<filename>_bilingual.srt`

```bash
bun scripts/merge_bilingual_subtitles.ts \
  "<top_subtitle.srt>" \
  "<bottom_subtitle.srt>" \
  "<output_dir>/<filename>_bilingual.srt"
```

Default order: Source language (original) on top, target language (translated) on bottom.
User can specify the order.

---

### Step 8: Output Report

**Goal**: Show results to user

1. Show:
   - Translated subtitle file path
   - Bilingual subtitle file path (if generated)
   - Total subtitle entry count
   - Source → Target language pair

2. Keep all generated files (translated SRT, bilingual SRT)

---

## Error Handling

| Issue | Solution |
|-------|----------|
| Unsupported format (.ass/.ssa) | Inform user, suggest converting to SRT first |
| Encoding error | Convert to UTF-8 before processing |
| Count mismatch after translation | Auto-fix and re-validate |
| Language detection fails | Ask user to specify source language |

---

## Examples

**Basic translation:**
```
User: 把这个英文字幕翻译成中文
→ Detect language (en) → Term scan → Translate → output/video_zh.srt
```

**With bilingual output:**
```
User: Translate to Chinese and make a bilingual version
→ Detect (en) → Term scan → Translate → Merge bilingual → output/video_zh.srt + output/video_bilingual.srt
```

**Specify languages:**
```
User: Translate this Japanese subtitle to English
→ Confirm (ja→en) → Term scan → Translate → output/video_en.srt
```

**VTT input:**
```
User: 翻译这个 VTT 字幕文件
→ Convert VTT→SRT → Detect language → Term scan → Translate → output/video_zh.srt
```
