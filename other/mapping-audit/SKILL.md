---
name: mapping-audit
description: Use when checking kasane's catalog for bad arc mappings — after inserting or editing a series in Supabase, before cutting a release, when a user reports an episode pointing at the wrong chapter, or when asked to "audit the catalog", "check the mappings", or "find bad data".
---

# Mapping Audit

Arc mappings are hand-researched and written straight into Supabase. They pass through no code review, no CI, and no migration. A mistyped boundary ships to every client on next launch. This audit is the only gate between a typo and production.

## Run it

```bash
bun run scripts/audit-mappings.ts               # structural checks, triaged findings hidden
bun run scripts/audit-mappings.ts --errors-only # the actionable backlog
bun run scripts/audit-mappings.ts --series "One Piece"
bun run scripts/audit-mappings.ts --anilist     # + AniList count cross-check (slow, rate-limited)
bun run scripts/audit-mappings.ts --json        # for programmatic consumers
bun run scripts/audit-mappings.ts --no-ignore   # include findings already triaged as intentional
```

Exit code is 1 when any `error` survives, so it composes into a release gate.

## What each code means

| Code                                                                       | Severity                                    | Meaning                                                                                                                                                                                                         |
| -------------------------------------------------------------------------- | ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `chapter-overlap` / `episode-overlap`                                      | error if 2+ shared units, warn if exactly 1 | Consecutive arcs claim the same unit. Two arcs answer one lookup and `find` returns the earlier one. **One** shared unit is ambiguous: adaptations routinely split a chapter or episode across an arc boundary. |
| `position-sequence`                                                        | error                                       | Positions are not a dense 0-based run, so display order is undefined.                                                                                                                                           |
| `chapter-range-inverted`, `episode-range-inverted`, `non-positive-episode` | error                                       | Impossible range. Always a typo.                                                                                                                                                                                |
| `negative-chapter`                                                         | error                                       | Chapter below 0. Chapter **0 is legal**: publishers number prologue chapters `00`.                                                                                                                              |
| `catalog-behind-anime`                                                     | info                                        | Arcs stop short of the anime's episode count while manga chapters are still unmapped. Expected whenever the anime outruns its source; confirm the stop was deliberate rather than an unfinished mapping.        |
| `episode-null-sandwich`                                                    | warn                                        | An unadapted arc sits between two adapted ones. Real when the anime skipped that source and resumed after it; also what a misordered row looks like.                                                            |
| `chapter-gap` / `episode-gap`                                              | warn if the hole is 1-3 units, else info    | Small holes are off-by-one typos; long runs are anime filler or deliberately skipped stretches.                                                                                                                 |
| `season-partial`                                                           | warn                                        | Some adapted arcs carry `season`, some do not. Per-season coverage UI needs all or none.                                                                                                                        |
| `movie-*`                                                                  | warn                                        | A film's chapter range or `after_episode` falls outside the mapped arcs.                                                                                                                                        |
| `catalog-behind-manga`                                                     | warn                                        | The manga has published past the last mapped arc. Feed this to `mapping-correction`.                                                                                                                            |
| `anime-original-pinned`                                                    | info                                        | A zero-width arc pinned at the previous arc's last chapter. `chapter_start`/`chapter_end` are `NOT NULL`, so this is the schema's only way to say "adapts no further manga". Normal, not a defect.              |
| `shared-manga-id`                                                          | info                                        | Two series share a manga id. The lowest series id wins the lookup. Confirm the winner is the one users expect.                                                                                                  |

## Triage before fixing

**Not every finding is a bug.** These modelling choices produce findings legitimately:

- **Light-novel adaptations** store LN _volume_ numbers in the chapter columns, so ranges overlap and skip freely. Tell: arc names containing "Vol", "LN", or "Novel".
- **Anime-original arcs** woven mid-stream share a boundary chapter with the arc around them.
- **Non-linear adaptations** (a season that backfills chapters an earlier season skipped) genuinely overlap.
- **Episodic anthologies** reorder chapters freely. Tell: episode titles that concatenate the chapter titles they adapt.
- **Straddling boundaries** where one chapter or episode is split across two arcs. Tell: the show's wiki lists that unit under both arcs, often marked "(Partially)".
- **Mid-run skipped source** where the anime jumps a volume or arc and resumes after it, leaving an unadapted arc between two adapted ones.
- **Deliberately partial mappings** of very long shows leave large gaps on purpose.

The first full triage pass found that **only 2 of 16 reported errors were real data bugs**. Assume a finding is a modelling choice until a primary source says otherwise, and when a whole class of finding turns out legitimate, fix the check rather than filing another ignore entry.

Confirm the intent from the arc name, the `note`, or `source_notes` before touching data. When a finding is intentional, record it in `scripts/audit-ignore.json` with a reason:

```json
"Toilet-bound Hanako-kun": {
  "chapter-overlap": "S1 skipped chapters 23-29 and S2 backfilled them, so the season ranges genuinely overlap"
}
```

Suppression is per series + code, so a new bug of an already-triaged code in an already-triaged series stays hidden. **Re-run with `--no-ignore` whenever you edit a series that has an entry there.**

## Fixing what is real

Corrections are Supabase writes, not code changes. Use the `mapping-correction` skill. Never edit rows to silence the audit without confirming the underlying fact against the fandom wiki or Wikipedia first.

## Common mistakes

| Mistake                                         | Why it hurts                                                                                                                                                  |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Adding an ignore entry to make the output green | The audit exists to be believed. An unjustified entry makes every future run less trustworthy.                                                                |
| Treating every `chapter-gap` as a bug           | Most long gaps are anime filler. Fix the 1-3 unit ones first.                                                                                                 |
| Treating `catalog-behind-anime` as a defect     | It compares two different quantities: episodes that adapt manga vs every episode aired. An anime outrunning its source is the common case, so this is `info`. |
| Editing rows with the app's publishable key     | Catalog tables are read-only under RLS. Write via Supabase MCP, the dashboard, or a service-role script.                                                      |
