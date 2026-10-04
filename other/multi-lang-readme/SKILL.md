---
name: multi-lang-readme
description: Use when creating bilingual or multilingual README files from an existing README while preserving Markdown structure.
---

# Multi-Lang README

## Overview

Create multilingual README files by translating an existing README while preserving Markdown structure, links, code blocks, and language-switch navigation. The workflow supports bilingual and multilingual README sets without rewriting unrelated project documentation.

## When to Use

Use this skill when the user asks for:
- Bilingual README creation (for example English + Chinese)
- Multilingual README generation
- Translating an existing README into one or more target languages
- Standardized language-switch links across README files

## Do not use

Do not use this skill for:
- Translating arbitrary non-README documents
- Rewriting product requirements or legal documents
- Content generation tasks unrelated to README translation

## Instructions

1. Locate the source README file to translate (ask user if ambiguous).
2. Confirm target language(s) and desired canonical README language.
3. Translate content while preserving markdown, links, and code blocks.
4. Write translated files using language suffix conventions.
5. Add or update language-switch links at the top of each README.
6. Verify filenames, link paths, and formatting before final output.

## Supported Languages

| Code  | Language |
|-------|----------|
| en    | English  |
| de    | German   |
| ja    | Japanese |
| ko    | Korean   |
| zh-CN | Chinese  |

## Workflow

### Step 1: Detect README

Find the source README:
- Check root directory for `README.md`
- If multiple README files exist, ask which file should be translated

### Step 2: Read README Content

Read full markdown content, including:
- Title
- Badges
- All sections (Features, Installation, Usage, Contributing, License, etc.)
- Code blocks
- Links

### Step 3: Confirm Target Language

Ask user which language(s) to translate to. Default assumptions:
- **README.md should always be in English** as the canonical version
- If current README is in Chinese (or any non-English), translate it to English first
- After English version is established, add other language versions as requested

If user says "create bilingual README" without specifying:
- Translate existing README to English first (replace or create README.md)
- Then add Chinese version (README.zh-CN.md)

### Step 4: Translate with AI

Translate with these rules:
- Preserve markdown formatting
- Keep code blocks unchanged
- Translate section titles to target language
- Keep internal links (relative paths) as-is
- For external links, use target language anchor text if appropriate

### Step 5: Create Translated README

**Important**: keep `README.md` as canonical English unless the user explicitly asks for another convention.

- English: README.md (create or replace with English version)
- German: README.de.md
- Japanese: README.ja.md
- Korean: README.ko.md
- Chinese: README.zh-CN.md

If the original README is non-English and user agrees, replace it with English `README.md`.

### Step 6: Add Language Switcher

Update original README to include language switcher at the top:

```markdown
**English** | [中文](README.zh-CN.md) | [Deutsch](README.de.md) | [日本語](README.ja.md) | [한국어](README.ko.md)
```

Add below the title or badges, before the main content.

### Step 7: Update Translated README

Add reciprocal link in the translated README:

```markdown
**[Original](README.md)** | [中文](README.zh-CN.md)
```

## Language Code Reference

```
en    → no suffix (README.md)
de    → README.de.md
ja    → README.ja.md
ko    → README.ko.md
zh-CN → README.zh-CN.md
```

## Common Triggers

- "create bilingual README"
- "create English and Chinese README"
- "translate README to Japanese"
- "add German version of README"
- "add README.zh-CN.md"
