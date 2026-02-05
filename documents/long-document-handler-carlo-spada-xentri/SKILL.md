---
name: long-document-handler
description: Triggers when reading or writing documents exceeding 20,000 tokens (~80,000 characters or ~15,000 words). Use when encountering large files, lengthy documentation, big markdown documents, massive PRDs, architecture docs, or any content that risks context window overflow. Activates on phrases like "this document is long", "large file", "too many tokens", or when Claude detects document size approaching limits.
---

# Long Document Handler

## Purpose

This skill INTERRUPTS work when encountering or creating documents that exceed 20,000 tokens. Large documents consume excessive context window, reduce response quality, and risk truncation.

## Detection Thresholds

| Metric             | Threshold | Action                |
| ------------------ | --------- | --------------------- |
| Characters         | > 80,000  | STOP and consult user |
| Words              | > 15,000  | STOP and consult user |
| Lines              | > 2,000   | STOP and consult user |
| Tokens (estimated) | > 20,000  | STOP and consult user |

**Token estimation:** ~4 characters per token for English text.

## MANDATORY BEHAVIOR

When detecting a document at or approaching these thresholds:

### 1. STOP IMMEDIATELY

Do not continue reading or writing. Do not attempt to process the full document.

### 2. INFORM THE USER

State clearly:

- The document's approximate size
- That it exceeds the recommended threshold
- That continuing may degrade quality or cause issues

### 3. PRESENT OPTIONS

Ask the user how to proceed with these choices:

---

## Options for READING Large Documents

### Option A: Targeted Extraction

"I'll read only the specific sections relevant to your request. Tell me what you're looking for."

### Option B: Summary Mode

"I'll read the document in chunks and provide a summary of its structure and key content."

### Option C: Shard the Document

"I can split this into smaller, focused files using the `/bmad:core:tools:shard-doc` command (splits on level-2 headings by default)."

### Option D: Proceed Anyway

"I'll read the full document, but be aware this may consume significant context and affect response quality."

---

## Options for WRITING Large Documents

### Option A: Phased Writing

"I'll write the document in phases, checking in with you after each major section."

### Option B: Outline First

"I'll create a detailed outline for your approval before writing any content."

### Option C: Split by Design

"I'll create multiple smaller documents organized by topic/section instead of one large file."

### Option D: Template + Placeholders

"I'll write the structure with placeholders, then we fill in sections incrementally."

---

## Example Dialogue

**Claude detects large document:**

> **STOP** — This document is approximately 25,000 tokens (~100,000 characters).
>
> This exceeds the 20,000 token threshold. Processing the full document may:
>
> - Consume excessive context window
> - Reduce response quality for follow-up questions
> - Risk truncation or incomplete processing
>
> **How would you like to proceed?**
>
> 1. **Targeted extraction** — Tell me what specific information you need
> 2. **Summary mode** — I'll provide a structural overview
> 3. **Shard it** — Split into smaller files by section
> 4. **Proceed anyway** — Read the full document (not recommended)

---

## Integration with BMAD

For BMAD documents specifically:

- Use `/bmad:core:tools:shard-doc` to split large docs by H2 sections
- PRDs, Architecture docs, and Epics are common candidates for sharding
- Consider the entity hierarchy when splitting (maintain traceability)

---

## When NOT to Interrupt

- Code files (even large ones) — these are handled differently
- Log files being searched with grep (partial reads are fine)
- When user explicitly says "read the whole thing" or "I know it's large"
- Binary files or images (not applicable)
