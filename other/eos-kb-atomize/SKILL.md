---
name: eos-kb-atomize
description: Turn a KB `kind:reference` standard (IEC/IEEE/Transgrid PDF archive) into atomic `kind:clause` notes — audit which references are undigested, reformat PyMuPDF-split or bilingual archives so they're section-addressable, then atomize with a throttled write that won't storm the vault watcher. Use when the user says "atomize this standard", "digest the KB references", "this full text needs proper md / sections", or asks to make a stored standard's clauses individually indexable. Case-by-case per document; this is the decision tree + the safe write procedure. NOT for digesting a fresh PDF into the KB (use vault-source-digest) and NOT for checking KB consistency afterwards (use eos-kb-audit).
---

# EmptyOS KB Atomize

Turn a stored standard (a `kind: reference` note pointing at a verbatim PDF
archive) into **atomic, connectable `kind: clause` notes** — one per level-2
§X.Y section — so each clause is individually indexable, searchable, and
citable, while the reference note composes them into the readable document.

Every standard's PDF extraction is different, so this is **case-by-case** —
but the method, the failure modes, and the safe write procedure are fixed.
This skill is that fixed spine.

## Prerequisites (read first)

- **The daemon must be running** at `http://127.0.0.1:9000` — Step 3 throttles
  writes against the live vault watcher and probes `GET /api/health` between
  batches (`127.0.0.1`, never `localhost`). The three tools themselves are
  pure/no-kernel-boot, but the throttle + spot-check need the daemon up.

## The pipeline (3 tools, all pure / no kernel boot)

| Stage | Tool | What |
|---|---|---|
| **Discover** | `emptyos.sdk.doc_slice.parse_contents` | Finds sections **only** from dot-leader TOC rows (`4.1 Title …… 13`), filtered to `level==2`. |
| **Slice** | `emptyos.sdk.doc_slice.slice_clause_text` | Spans a clause: its body heading (`4.1 Title`, number+title **one line**) → next heading of `depth ≤`. Sub-clauses promoted to `## §X.Y.Z` anchors by `_format_section_body`. |
| **Plan/write** | `scripts/atomize_standard.py <slug> [--write] [--throttle=SEC]` | One `clause` note per level-2 section; **skips** clauses that already have a (curated) note of the same `standard_id` **and** `edition`. |
| **Repair** | `scripts/reformat_split_headings.py <slug> [--write] [--drop-french]` | Fixes archives the discover/slice stages can't read (see below). |

## Step 1 — Audit (always dry-run first)

For each `kind: reference` note with a `local_text:`/`source_file:` pointer:

```
python scripts/atomize_standard.py <slug>          # dry-run, prints planned NEW count (M)
```

Classify by M and existing curated count (N):

| Verdict | Meaning | Action |
|---|---|---|
| **DIGESTED** | M=0, N large | done |
| **UNDIGESTED** | M>0, N=0 | atomize (Step 3) — highest value |
| **PARTIAL** | M>0, N>0 | atomize; skip-check protects curated notes |
| **NO_SECTIONS** | M=0, archive has no readable TOC | **reformat first** (Step 2) |
| **ERROR** | empty/self-referential pointer | fix the reference note's frontmatter |

Write the audit as a table sorted by M descending. **Never `--write` in this pass.**

## Step 2 — Reformat NO_SECTIONS archives (case-by-case)

A NO_SECTIONS verdict almost always means one of these PDF-extraction shapes.
Diagnose by reading the archive's TOC region (`grep -nE "CONTENTS|\.{4,}"`):

| Shape | Tell | Fix |
|---|---|---|
| **Split number→title** | Clause number on its own line, title on the next (`4.1\nThermal resistance …… 10`) — defeats both TOC + body matching | `reformat_split_headings.py <slug> --write` (rejoins them; also rejoins **wrapped TOC rows** where a long title spills onto the dot-leader line — body headings that wrap are fine, `_is_heading_for` matches by number prefix) |
| **Bilingual (IEC FR/EN)** | French clause appears before English; `parse_contents` dedup keeps the **French** title | add `--drop-french` (drops pages whose running header is `CEI:YYYY` and not `IEC:YYYY`) |
| **Spaced dot-leaders / OCR noise** | TOC uses `. . . .` (spaced) not `....`; OCR errors (`Aspectsgénéraux`); no language header token | **usually not worth it** — leave NO_SECTIONS, especially for a superseded edition. Extract its formulae as a hand-curated `formula` note instead. |

`reformat_split_headings.py --write` emits `<archive>.repaired.md` (original kept
as backup) and repoints the reference note's pointer. Re-run Step 1 on the
repaired archive to confirm M>0 before atomizing.

**The yield test:** if a NO_SECTIONS doc only yields ~3 level-2 sections and is
bilingual/superseded, the verbatim clause notes are low-value — a single
`formula` note capturing its equations beats 3 fragile auto-slices. Reformat the
*valuable, high-yield, clean* archives (the cable-rating standards you actually
use); leave the messy stragglers as referenced blobs.

## Step 3 — Atomize with a throttled write (mandatory)

A bulk write of 100+ notes fires 100+ `vault:changed` events; the EventBus runs
handlers serially, so a burst can wedge `:9000` (the realtime-broadcast /
reactor storm pattern). **Always throttle** — there is no watcher-pause API:

```
python scripts/atomize_standard.py <slug> --write --throttle=0.25
```

`--throttle=0.25` ≈ 4 writes/s — the bus drains each well under 250 ms, so events
trickle instead of bursting. Never touch the daemon process / `restart.bat` /
`data/*.db` (`.claude/rules/daemon-handling.md`). After each batch:

```
curl -s -m5 http://127.0.0.1:9000/api/health -o /dev/null -w "HTTP %{http_code} %{time_total}s\n"
```

A sub-10 ms 200 confirms no wedge.

## Step 4 — Dedup check (edition-string trap)

The skip-check matches `clause` + `standard_id` + a **normalized** `edition`
(`_norm_edition`: parenthetical qualifiers stripped, lowercased — so `2015 (2.1)`
≡ `2015`, while `Rev 0.2` ≠ `Rev 1.0`). Cosmetic spelling differences dedup
automatically; genuine revisions still each get their own notes. If a residual
dup slips through (an edition spelled differently in a way the normalizer can't
collapse), list the standard's clause notes and remove any auto note (its
`source_file:` points at the `.repaired.md`) colliding with a curated one —
**curated wins**:

```
grep -lE "^standard_id: <ID>" *.md   # then per file: clause + is-auto (source_file ~ repaired)
```

Delete the colliding auto `.md` directly (one file → one event, no storm).

## Step 5 — Spot-check + record

- Open one written note: correct frontmatter (`parent`, `related`, `clause`,
  `standard_id`), verbatim body, `## §X.Y.Z` sub-anchors present.
- Verify total written matches the dry-run plan minus any dedup deletions.
- Commit **only your files** (`git status --short` first — parallel sessions;
  never `git add -A`). Devlog the run if it touched many references.

## When NOT to atomize

- Academic papers / textbooks (Anders 1997) — chapters aren't `§X.Y` clauses;
  hand-curate `lesson`/`formula` notes instead.
- Pure table dumps (IEEE 835 — 7 MB of ampacity tables) — atomizing yields
  noise, not knowledge.
- A reference whose value is a handful of equations — one `formula` note > N
  verbatim clause notes.

## Cross-references

- `scripts/atomize_standard.py`, `scripts/reformat_split_headings.py` — the tools.
- `emptyos/sdk/standard_atomize.py` (`plan_atomization`), `emptyos/sdk/doc_slice.py`
  (`parse_contents`/`slice_clause_text`) — the pure engine.
- `.claude/rules/daemon-handling.md` — never restart/kill `:9000`; throttle instead.
- CLAUDE.md § KB note kinds — `reference` (landing page) vs `clause` (atomic),
  `formula` (implementable spec) as the fallback for low-yield standards.
