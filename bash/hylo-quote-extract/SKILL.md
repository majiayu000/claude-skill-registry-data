---
name: hylo-quote-extract
description: Extract high-value verbatim quotes from a Hylo note and save each as a short note with a backlink wikilink. Use this skill whenever the user wants to extract key quotes, highlight important passages, or "划重点" from a vault note. Trigger on phrases like "extract quotes", "highlight this note", "save important quotes from", "提取引文", "划重点", "摘录重点", or any request to pull out notable original text from a note and store it.
---

# Hylo Quote Extractor

Extract high-value verbatim passages from a Hylo note and save each one as a short note with a backlink to the source.

## What counts as a good quote

Think of it like a **pull quote in a magazine**: not just the punchline, but enough setup that the insight lands on its own. A single sentence that contains the conclusion but relies on prior paragraphs for meaning is not a good quote — include the setup.

A quote worth saving:
- Tells a **complete mini-story**: claim + reasoning, or observation + implication, or setup + payoff. If you need to re-read the source to understand why it matters, the quote is too short.
- Is **verbatim** — exact words from the source, never paraphrased or summarized. Splice adjacent sentences or paragraphs together if they form a coherent unit; trim only scaffolding words between them.
- Has **enough context** to be vivid and specific when encountered cold, weeks later.
- Is **dense with meaning** — surprising, counterintuitive, or crystallizing something the reader half-knew but couldn't articulate.

**Typical length**: 2–5 sentences, or one full paragraph. A single memorable sentence is fine only when it is fully self-explanatory. A quote can span multiple consecutive paragraphs if they build a single argument.

Skip generic transitions, introductions, obvious statements, and boilerplate. Quality over quantity — 3–8 quotes per note is typical.

## Step-by-step

### 1. Identify the source

The user will name the note as either a vault-absolute path (`/clips/article.md`) or a bare name (`article.md` or `article`). Use whichever form they provided.

### 2. Read the note

```bash
hylo raw_note read <path-or-name>
```

If this fails, surface the error directly — don't proceed.

### 3. Extract the stem and display text

The backlink needs a **stem** (the filename without `.md`) and a **display** label.

Derive the stem:
```bash
# e.g. /clips/网络效应.md → 网络效应
basename "<path>" .md
```

For the display label, use (in priority order):
1. The `title:` value from YAML frontmatter, if present
2. The first H1 heading (`# ...`), if present
3. The stem itself

### 4. Save each quote as a short note

For every extracted quote run:

```bash
hylo short_note create --content "QUOTE_TEXT

[[STEM|DISPLAY]]"
```

The wikilink goes on its own paragraph (blank line separator) after the quote text. This creates a backlink so the short note points back to the source.

**Example** — source `/clips/网络效应.md`, title "网络效应":

```bash
hylo short_note create --content "网络效应使得先发优势几乎不可逾越，后进者需要付出数倍的资源才能撬动用户迁移。

[[网络效应|网络效应]]"
```

Run each `hylo short_note create` call separately (one per quote), not batched into one.

### 5. Report

After all saves succeed, output:
- How many quotes were saved
- The file path(s) returned by each `hylo short_note create` call (the CLI prints `saved short note to "..."`)

## Edge cases

- **Note not found**: `hylo raw_note read` will error — surface it.
- **Very short note / few quotable passages**: save what exists (even 1–2 is fine) and note it.
- **Note is itself a list of bullets or quotes**: each bullet is a candidate; still apply the quality filter — don't blindly save every line.
- **Frontmatter title with quotes or special chars**: escape them properly in the shell argument, or use `$'...'` syntax.
