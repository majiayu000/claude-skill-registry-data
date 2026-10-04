---
name: passage-glossary
description: Use when producing a passage reader with a deduplicated lemma glossary. Use when user asks for a vocabulary list, glossary, lemmas in a passage, deduplicated glossary for a text, or a graded-reader study artifact. Combines passage text with an ordered, MCP-grounded glossary of every distinct headword. Always English output.
allowed-tools: Read, Write, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_morphology, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_lexicon, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__bible_lookup
version: 1.1.0
changed: "2026-09-30"
---

# Passage Glossary

## Model selection

Use Sonnet by default for delegated work. Explicit `model: opus` escalation is allowed
when the study warrants it; preserve an existing Opus selection. Never request Haiku,
inherit it, or use a built-in delegate that selects it. If this context is running on
Haiku, stop before study work and request a switch to Sonnet or Opus.

## Purpose

Produce a passage reader artifact: the passage text followed by a deduplicated, MCP-grounded glossary of every distinct headword occurring in it. Data-grounded. Never fabricate glosses. Output to file (default) or inline (`--output print`).

**Key constraint:** Every gloss must trace to MCP data (`query_lexicon` or morphology fallback). Unresolved headwords are shown explicitly — never invented.

---

## Headword Identity

> **headword identity = strongs ?? lemma**

A headword is identified by its **Strong's number** when the morphology data supplies one. When `strongs` is null, the exact `lemma` string serves as the key. This identity rule governs deduplication, lexicon calls, and glossary rendering throughout.

---

## Pipeline (Five Steps — Execute in Order)

### Step 1: Parse References

Accept one or more passage references. Supported forms:
- Single verse: `John 1:1`
- Intra-chapter range: `John 1:1-5`
- Cross-chapter range: `John 1:1-2:11`
- Multiple passages (comma- or `+`-separated): `John 1:1-5, Romans 8:1-4`

Translate each reference into the shared `{ book, range }` shape used by `query_morphology` and `bible_lookup`. `range` format: `"chapter:verse-chapter:verse"` (e.g., `"1:1-1:5"`).

**One book per call.** A cross-book span is split into per-book calls, each with its own `query_morphology` invocation.

**Book not found:** If `query_morphology` returns `BOOK_NOT_FOUND`, surface the error verbatim plus any `suggestions` it provides. Name the offending reference explicitly. Skip that passage but continue processing any remaining references — never silently drop a passage.

Do NOT call `list_books` — rely on the built-in error and suggestions from `query_morphology`.

---

### Step 2: Extract and Deduplicate Headwords

For each `{ book, range }`, call `query_morphology` with `fields: "lexical"`. This returns per-word records containing `lemma`, `strongs` (nullable), and `gloss` (nullable).

**Truncation check:** After each call, inspect `summary.truncated`. If `true`, the range exceeded the server's 25k-character cap and trailing words were silently dropped. Split the range into smaller sub-ranges (e.g., by chapter) and re-query until `summary.truncated` is `false` for every sub-range. Never build a glossary from a truncated word list.

**Deduplication:** Across all words in all passages, apply the headword identity rule:
- Key = `strongs` when non-null
- Key = `lemma` string when `strongs` is null

Preserve **first-occurrence order** across the combined span. When two words share the same key, keep the first-seen record; discard the duplicate.

Each headword record carries:
- `key`: the dedup key (Strong's number or lemma string)
- `lemma`: the display form (first-seen surface form)
- `strongs`: the Strong's number, or null
- `morphGloss`: the morphology `gloss` field value (may be null)
- `order`: first-occurrence index (1-based)

When one Strong's number maps to multiple surface lemma forms in the passage, display the first-seen surface form and show the Strong's number on the glossary row for disambiguation.

---

### Step 3: Resolve Glosses via Lexicon (Mandatory Batching ≤ 20)

Partition the distinct-headword list into two groups:
- **Strongs group**: headwords with a non-null `strongs`
- **Null-strongs group**: headwords whose key is the `lemma` string

**Batching rule:** Split each group into chunks of **at most 20** entries per chunk. Do not exceed 20 per `query_lexicon` call — the API enforces a hard cap of 20 (`strongs_ids` or `lemmas` array max = 20). A passage with many distinct headwords requires multiple calls.

Example arithmetic: 47 distinct Strong's IDs → 3 calls: 20 + 20 + 7.

**For the strongs group:** call `query_lexicon` with `mode: "strongs", strongs_ids: [<chunk of ≤20 Strong's numbers>]`.

**For the null-strongs group:** call `query_lexicon` with `mode: "lemmas", lemmas: [<chunk of ≤20 lemma strings>]`.

**Associating results:**
- Lexicon returns `entries` keyed by `strongs_id` and `not_found: string[]` listing unresolved inputs.
- For the strongs group: match each entry by its `strongs_id` back to the headword's `strongs` key.
- For the null-strongs group: any input lemma absent from `not_found` was resolved; use the returned entry's `gloss`.

**Gloss fallback chain (per headword, in order — never skip to a lower tier without exhausting the one above):**
1. `query_lexicon` `entry.gloss` — authoritative, multi-source scholarly definition (Tier 1).
2. Morphology `lexical` `gloss` **when it is non-null** — labeled `(morphology gloss)` in output. Single-scholar provenance; use only when lexicon does not resolve the headword (Tier 2).
3. `(unresolved — not in lexicon)` — explicit label; no gloss invented (Tier 3 / anti-fabrication floor).

**Transport failures vs. `not_found`:** Distinguish:
- `not_found`: the headword is not in the lexicon — follow the fallback chain above.
- Transport error / API error on the call itself: retry the chunk once. If still failing after one retry, mark every headword in that chunk `(gloss lookup failed)` and continue. A complete headword list with some unresolved glosses is better than aborting the artifact.

**Never fabricate a gloss.** If no tier resolves a headword, output `(unresolved — not in lexicon)`.

---

### Step 4: Render the Artifact

**Passage text:** Call `bible_lookup` with `{ book, range }` for each reference. Follow `page.next_cursor` until it is omitted, preserving the returned verse order. Surface any `versification_note` returned by the tool directly below the passage text.

**Glossary:** Project the resolved glosses back onto the **ordered distinct-headword list from Step 2** (the authoritative, order-preserving spine). Do not render from lexicon merge order — use Step 2 order.

**Per-row format (mandatory):**

```
lemma [STRONG'S | (no-strongs)] — gloss
```

- Always show the Strong's number when present: e.g., `θεός [G2316] — God`
- When the headword had no `strongs` and was lemma-keyed, show the literal token `(no-strongs)`: e.g., `עֲבוֹדָ֔ה (no-strongs) — service`
- Append transliteration when the lexicon returns it: e.g., `θεός [G2316] theos — God`
- Append `(morphology gloss)` label when using Tier 2 fallback.
- Append `(unresolved — not in lexicon)` or `(gloss lookup failed)` as applicable.

The per-row key token (`STRONG'S` number or `(no-strongs)`) MUST appear on every row — this is not optional decoration. It is the machine-readable dedup key that test assertions use to detect duplicate rows.

**Section header:** Use `## Glossary` as the section heading.

**Ordering:** Default = first-occurrence (reading order). Alphabetical available on explicit user request.

**Output modes:**

- **File mode** (default, or `--output file`): Save to `~/.claude/passage-glossary/{book}/{YYYY-MM-DD}-{range}.md`. Report the saved path.
- **Print mode** (`--output print`): Output the complete artifact inline. Do not save to file. Print ALL content — passage text plus full glossary — directly in the response.

**Never ignore `--output print`.** If the invocation includes `--output print`, print inline. Do not save to a file and return a summary.

**Empty passage / no words:** Emit the passage with an empty `## Glossary` section and an explicit note: `(No words found in this passage range.)`.

---

### Step 5: Theological Guardrails

Every gloss in this artifact traces to MCP data (`query_lexicon` or morphology). Unresolved headwords are shown with explicit labels — they are never invented. This is the anti-fabrication floor: the artifact is a data-grounded study tool, not a commentary.

Do not add interpretive notes, theological commentary, or application content to glossary rows. The glossary lists headwords and their lexical definitions. Exegetical analysis belongs in `/exegetical-notes`, not here.

---

## Common Failure Patterns (Red Flags)

| Failure | Prevention |
|---------|-----------|
| Glossary has duplicate headword rows | Apply dedup key = `strongs ?? lemma` before rendering; each key appears exactly once |
| Glossary omits words from the passage | Never render from a truncated morphology result; check `summary.truncated` and re-query |
| Wrong param name on morphology call | The param is `fields:` with value `"lexical"`. There is no `register` parameter — do not use it. |
| Sent >20 IDs in one `query_lexicon` call | Batch into chunks of **at most 20** — hard cap enforced by the API |
| Ignored `not_found` array | `not_found` is the unresolved signal; trigger the fallback chain on every entry in it |
| Fabricated a gloss when `not_found` | Follow the fallback chain; if Tier 2 (morphology gloss) is also null, output `(unresolved — not in lexicon)` |
| Rendered glossary in lexicon merge order | Render from the Step 2 ordered headword list, not from lexicon response iteration order |
| Per-row key token missing | Every row MUST show `[G####]` or `(no-strongs)` — it is the machine-readable dedup key |
| `--output print` but saved to file | If `--output print` is in the invocation, print ALL content inline |

---

## Invocation Format

```
/passage-glossary John 1:1-5
/passage-glossary John 1:1-5 --output print
/passage-glossary John 1:1-5, Romans 8:1-4
/passage-glossary Genesis 1:1-10
```

- `--output`: Optional. `file` (default) saves to disk. `print` outputs inline.
- Multiple passages: comma- or `+`-separated. Shared deduplication across all passages.
- Book names accept abbreviations (`John`, `Gen`, `Rom`, etc.) or full names.
