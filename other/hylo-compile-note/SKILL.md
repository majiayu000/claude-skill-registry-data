---
name: hylo-compile-note
description: "Compiles a single raw Hylo note into knowledge units using a two-phase AI process (triage → compile). Use this skill whenever the user wants to compile a note into knowledge, extract knowledge from a note, update the knowledge base from a note, merge note content into knowledge units, or run knowledge compilation. Triggers on phrases like 'compile this note', 'compile note into knowledge', 'extract knowledge from note', 'update knowledge base', 'run compile on', or any request to turn a raw note into structured knowledge units."
---

# Hylo Compile Note

Compiles a single raw note into **knowledge units** — wiki-style pages that capture the author's accumulating understanding of the entities and concepts that matter to them.

**Run all five steps to completion without stopping.** Do not present intermediate results, ask for confirmation, or pause between steps. Pre-compile (Step 3) is internal — never output it to the user. Only speak at the end (Step 5 summary).

---

## Inputs

1. **Note path** — the raw note to compile (vault-absolute or filesystem path)
2. **Knowledge directory** — where knowledge units live (default: `_knowledge/` relative to cwd, which is always the vault root)

---

## Step 1 — Read the note

Read the full content of the target note. Note its path and **original publication date** — check in order: YAML front matter (`date` / `published`), filename date prefix, article/podcast header, or any explicit timestamp in the body. Record this as `source_date`. If none is found, mark `source_date` as unknown.

---

## Step 2 — Load relevant knowledge index

List available domain indexes:

```bash
hylo knowledge list-indexes
```

This returns a JSON array of `{"domain": "...", "path": "..."}` objects. Based on the note's content, select the 1–2 domains most relevant to what the note covers. Read only those index files to obtain the unit table for this compilation.

If the output is empty (no indexes exist), fall back to cold start: scan `<knowledge-dir>` directly and build a compact table (title | entity_type | tags | first paragraph ≤80 chars).

---

## Step 3 — Pre-compile (internal, not shown to user)

Scan the note and produce a **unit manifest** — a list of knowledge units to create or update. Do not generate any content yet.

### What qualifies as a knowledge unit

A knowledge unit is a wiki page for any **core or key entity** in the note that has depth worth accumulating. There are no fixed types — an entity can be a person, company, book, concept, technique, place, event, story, product, methodology, or anything the note treats with substance.

### Three qualifying questions

Before adding a unit to the manifest, answer all three:

1. **Does it have a stable name?** A recognized term or proper noun — not a sentence ("the argument that..."). Unnamed ideas belong inside another unit.
2. **Does it have depth to accumulate?** If the content would just restate a definition, there's nothing to compile. A unit needs room to grow — mechanisms, tensions, implications, meaning.
3. **Will it recur?** Would this entity appear across notes from different contexts and dates? If yes, it belongs here. One-off references don't.

If any answer is no, fold the content into an existing unit instead.

### Granularity calibration

**Too broad** — the title is a domain, not an entity ("AI Trends"). Fix: find the specific entity the note actually advances.

**Too narrow** — a sub-point or isolated fact with no room to grow. Fix: fold into the relevant unit.

**Right size** — something you'd naturally treat as its own subject. One clear defining sentence, and more to say beyond it.

### Split vs. sub-point

Create two units when they have **different cores** and would grow independently. Keep as a sub-point when one is an example or implication of the other — separating them would leave both thin.

### Don't add to the manifest

- Data points and metrics
- Sub-arguments that don't stand alone
- Passing references with no analysis

### Output: unit manifest

| unit name      | entity_type  | operation |
| -------------- | ------------ | --------- |
| \<unit title\> | \<freeform\> | create    |
| \<unit title\> | \<freeform\> | update    |

`entity_type` is a short descriptive label for what this entity is (e.g. `person`, `company`, `book`, `concept`, `event`, `technique`). It is freeform metadata — there are no type restrictions and no templates tied to it.

The manifest may be empty if the note has no content worth compiling. Immediately continue to Step 4.

For every unit marked `update` in the manifest: read its existing file at `<knowledge-dir>/<unit-name>.md` now, before Step 4 begins. Do not proceed to Step 4 until all existing files are loaded.

---

## Step 4 — Compile

For each unit in the manifest, check its `operation` and read the corresponding file:

- **`create`** → read `references/create.md` and follow it completely.
- **`update`** → read `references/update.md` and follow it completely.

`references/extract.md` documents partial-read commands (`hylo extract outline / section / segment / …`). Use them at any step when reading the full note is not necessary.

Complete one unit fully before moving to the next. After all units are done, confirm in prose: which were created, which updated, and what changed in each.

---

## Language

Match the language of existing units in the knowledge directory. If no units exist, use the language of the source note. Dates in opinion sections always use `YYYY-MM-DD`. When the vault language is not English, translate all section names accordingly.

## Time attribution

Knowledge units must anchor time to the **original publication date of the source material**, not the compilation date.

- If `source_date` is known: use it when writing any time-sensitive content in the unit (e.g. "as of YYYY-MM-DD", "at the time of publication").
- If `source_date` is unknown: omit the time reference or mark it as "date unknown". Never substitute today's date.
