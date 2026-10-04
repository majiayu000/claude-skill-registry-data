---
name: academic-paper-translation
version: 1.0.0
description: Use when reading foreign academic papers or primary sources to translate text into configured native language with bilingual parallel paragraphs and terminology glossaries
---

# Academic Paper Translation Skill

## Purpose
Translate foreign academic papers into the user's configured native language (set in [`config/user_preferences.json`](../../../config/user_preferences.json)), creating bilingual parallel paragraphs and building a structured terminology inventory. This skill preserves scholarly objectivity, domain-specific terminology, and traceability to the original text.

## Trigger Conditions
- When beginning close reading of a foreign-language paper
- When incorporating a non-native-language source into the literature review

## Configuration
Manage native language settings via the included script [`scripts/manage_user_config.py`](../../../scripts/manage_user_config.py) or directly edit [`config/user_preferences.json`](../../../config/user_preferences.json):

```bash
# Display current language settings (Submodule: python3 .scholarly-agent-skills/scripts/manage_user_config.py --show)
python3 scripts/manage_user_config.py --show

# Set native language to English
python3 scripts/manage_user_config.py --set-language "English" --set-code "en"

# Set native language to German
python3 scripts/manage_user_config.py --set-language "German" --set-code "de"
```

> [!NOTE]
> When running inside a submodule deployment, prefix script paths with `.scholarly-agent-skills/` (e.g. `python3 .scholarly-agent-skills/scripts/manage_user_config.py`).

## Four Translation Disciplines

1. **Maintain Academic Register**:
   Use formal academic register in the target language. For English: active voice with hedging verbs (`suggests`, `demonstrates`, `implies`). For Japanese: 常体 (である調).
2. **Preserve Original Terms (Bilingual Annotation)**:
   For polysemic or language-dependent keywords (e.g., *Hermeneutik*, *Dasein*, *Epistemic Injustice*), annotate with the original term on first occurrence: "Translation (*Original Term*)".
3. **Bilingual Parallel Output**:
   For critical paragraphs and direct quotations, produce side-by-side Original / Translation pairs for source criticism and citation verification:
   ```markdown
   > **Original**: Large Language Models risk institutionalizing epistemic injustice when deployed as conversational tutors.
   > **Translation**: 大規模言語モデル（LLM）は、対話型チューターとして運用される際、認識的不当性（epistemic injustice）を制度化するリスクを負っている。
   ```
4. **Bilingual Glossary**:
   Accumulate domain terms encountered during translation into `docs/bilingual-glossary.md` to prevent terminological drift:
   ```markdown
   | Original Term | Native Translation | Context in This Paper |
   |---|---|---|
   | Epistemic Injustice | 認識的不当性 | Fricker (2007) concept: testimonial credibility systematically undervalued |
   | Hermeneutics | 解釈学 | Theory of contextual interpretation of texts and historical discourse |
   ```

## Workflow

### Step 1: Load Source Text
Use Markdown output from `pdf-paper-ingestion` or the raw manuscript file.

### Step 2: Generate Paragraph-Level Parallel Translation
The AI applies the native language setting and produces bilingual parallel output for each paragraph.

### Step 3: Append to Bilingual Glossary
New domain terms are recorded in `docs/bilingual-glossary.md`.

## Outputs
- `docs/translated_[paper_name].md` (Bilingual Parallel Translation)
- `docs/bilingual-glossary.md` (Academic Term Bilingual Inventory)

