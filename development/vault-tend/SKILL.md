---
name: vault-tend
description: Acts like a team of knowledge managers doing a thorough maintenance pass over the WHOLE vault — re-languaging notes to one language, normalizing frontmatter, repairing broken wikilinks, deduplicating people/projects, tidying formatting, proposing archives, or any vault-wide adjustment you ask for. Always previews and asks before changing anything. Use when the user says "tidy/clean up the vault", "translate the whole vault to French", "normalize", "fix the broken links", "deduplicate", "vault maintenance", "act like a knowledge manager", or requests a sweeping change across notes.
---

# Skill: Vault Tend

The standing **knowledge-manager team** for your vault. Where `knowledge-build` *creates*
knowledge and the monthly Vault Health Check *audits* (read-only), this skill **acts**: it
makes careful, sweeping changes across many notes — re-languaging, normalizing, repairing,
deduplicating, tidying, archiving, or any adjustment you ask for.

Because it edits at scale, it is **preview-first and confirmation-gated, always.**

## When to activate

- "tidy / clean up the vault", "vault maintenance", "act like a knowledge manager".
- "translate / put the whole vault in French" (re-language).
- "normalize the frontmatter", "fix the broken wikilinks", "deduplicate people/projects".
- "make this adjustment everywhere…" (a custom vault-wide edit).
- After a Vault Health Check, to *act on* what it flagged.

**Do NOT use vault-tend when:**
- It's a single-note edit → just edit that note.
- The user wants to *create* synthesis/knowledge → `knowledge-build`.
- The user wants to *find* something → `recall`.

## Non-negotiable safety model

This skill can touch hundreds of notes. Every run follows the same loop:

1. **Scope** — restate exactly what will change and where (which folders, which note types).
2. **Scan & preview** — report counts and show 2–3 representative before/after diffs. Change nothing yet.
3. **Confirm** — get explicit go-ahead. For large scopes, confirm per batch.
4. **Apply in batches** — small batches, **one Git commit per batch**, so any step is reversible.
5. **Report** — what changed, what was skipped, what needs a human decision.

Hard rules (from `_CLAUDE.md`):
- **Never delete a note** — propose moving to `07-archive/` instead.
- **Append-only zones** (`02-people/`, `05-decisions/`): never delete a dated timeline entry
  or an `(auto-logged)` / `(Backfilled)` marker. (The pre-commit hook enforces this.)
- **Preamble stays English** — the `## For future Claude` block is never translated.
- **Wikilinks are identities** — don't rewrite link *paths* during a language change; rename
  only via the dedup/rename operation, and update all backlinks when you do.
- **Fuzzy-match before merging** duplicates; never merge without confirmation.
- Prefer many small commits over one giant diff.

## Operations

Pick the one(s) the user asked for. Each still runs the preview→confirm→apply→report loop.

### 1. Re-language the vault
Translate note **bodies** into the target language (from `MY-PROFILE.md` Working language, or
the one the user names — e.g. "tout en français").
- Translate: prose, section content, editable sections (`Compiled truth`, `Open threads`,
  goals, decisions text, knowledge bodies, the bullet prose inside timeline entries).
- **Keep verbatim**: the `## For future Claude` preamble (English), frontmatter values
  (enums/dates/tags), wikilink paths, quoted verbatim sources, code, and — by default — the
  **dated timeline headers** (`### YYYY-MM-DD — …`) and protected markers.
- **Section headings**: you may localize standard headings (e.g. `## Links` → `## Liens`) only
  if the user wants it; default is to keep canonical English headings so skills still match them.
  Flag this trade-off in the preview.
- **Deep mode** (only if the user explicitly asks to also translate historical entry headers):
  this rewrites append-only history, so the pre-commit hook will flag it — that's the safety net.
  Do it as a clearly-labeled, separately-committed migration the user has acknowledged.

### 2. Normalize frontmatter
Ensure each note has the required fields for its `type` (per `_CLAUDE.md` schemas): add missing
`ai-first: true`, fix field casing, dedupe/trim tags, fill obvious gaps (`updated`), flag the rest.

### 3. Repair wikilinks
Find broken `[[...]]` (target missing), empty `[[ ]]`, or path drift. Offer to create stubs or
fix the path; update backlinks. Report orphans (no inbound link).

### 4. Deduplicate
Fuzzy-match within `02-people/` and `03-projects/` for near-duplicates (e.g. `Alex Rivera` vs
`Alex Rivera (PM)`). Propose merges (keep the richer note, append the other's timeline, update
all backlinks, archive the loser). **Confirm each merge.**

### 5. Tidy formatting & consistency
Align section names/order to the type schema, fix heading levels, remove accidental duplicate
sections — without changing meaning. Never touch append-only history content.

### 6. Archive sweep
Propose moving completed projects, leavers, and notes stale past the `MY-PROFILE.md` threshold
to `07-archive/` (add `status: archived`). Confirm the list; never auto-archive silently.

### 7. Custom adjustment
Any vault-wide change the user describes ("add a `priority` tag to all active projects",
"standardize date formats"). Same loop: scope → preview → confirm → batched apply → report.

### 8. Knowledge garden
A focused maintenance pass on `06-knowledge/`. Delegates to `knowledge-build curator` (Mode C)
under the standing preview→confirm→apply loop, with extra reporting:
- Run the **curator sweep** (Mode C.2): rebuild auto-maintained hub listings, refresh
  `_INDEX.md`, detect orphans, near-duplicates, stubs awaiting enrichment, stale wiki pages.
- Propose **structural moves**: any `type: doc` still sitting at the root of `06-knowledge/`
  (legacy from before the `_sources/` convention) → move into `_sources/` and rewrite the
  inbound wikilinks. Any vault-meta artifact (`kickstart-backfill-*`, `vault-health-*`) in
  `06-knowledge/` → propose archival.
- Propose **new hubs** for unhubbed domain clusters with ≥ 3 notes (Mode C.2 step 3).
- Propose **merges** for near-duplicate wiki/lesson pages.
- Update `## Knowledge domains` in `MY-PROFILE.md` if the user confirms newly proposed domains.
- Report: hubs rebuilt, notes moved, orphans flagged, merges proposed, stubs aging out.

This is the recurring "tidy 06-knowledge" pass. Run it monthly or when `_INDEX.md` health
counters cross thresholds (the brief surfaces them).

## Report

```
✓ vault-tend — operation: re-language → fr
  Scanned: 142 notes. In scope: 96 (excluded 46: already fr / archive / preamble-only).
  Applied in 5 batches (5 commits). Skipped 3 (flagged below).
  Preserved: 38 dated timeline headers, all (auto-logged)/(Backfilled) markers, all preambles (EN).
  ⚠️ Needs you: 2 person notes have conflicting duplicates — review proposed merges.
  ⚠️ Heads-up: canonical headings kept in English so skills keep matching; say the word to localize.
```

## Anti-patterns to avoid
❌ **Applying without a preview** — always show the diff and counts first.
❌ **One massive commit** — batch it so it's reversible.
❌ **Translating the preamble or frontmatter enums** — those stay as-is.
❌ **Rewriting append-only history** unless the user explicitly opts into deep mode.
❌ **Deleting notes** — archive instead.
❌ **Silent merges** — confirm every dedup.
❌ **Rewriting wikilink paths during a language pass** — paths are identities.

## Special cases

### Mixed-language vault (the common one)
"Put everything in French": detect each note's language, translate only the non-`fr` ones,
keep already-French notes untouched, and update `MY-PROFILE.md` Working language to `fr` so new
notes follow suit. Preview the count of EN→FR notes before starting.

### Very large vault
Work folder by folder, oldest-first, committing per folder. Offer to stop after each so the
user can sanity-check before continuing. In Claude Code, fan out parallel subagents for the
read-only scan/preview phase (one per folder) — modern models handle this well and it cuts
the sweep time; keep the apply phase sequential and batch-committed.

### Running from a health report
If a `06-knowledge/vault-health-*.md` exists, offer to action its findings (orphans, stubs,
stale people, duplicates) one category at a time.
