---
name: lessons-learn
description: Consolidate the accumulated lessons log for one of this plugin's skills and apply user-approved improvements to that skill's SKILL.md. User-invokable only (`/dev:lessons-learn <slug>`), typically periodically; the model never triggers it. Presents each surviving improvement via AskUserQuestion, edits the working-clone SKILL.md for approved ones, then snapshots the whole active log to <slug>.archive-<UTC stamp>.md under ~/.claude/dev-skills/lessons/, writing deferred entries back to a fresh active log. Takes the target skill's slug as its only argument. Never commits — edits stay in the working tree for review.
disable-model-invocation: true
---

# Lessons learn

This skill is the inverse of `lessons-capture`. Where `lessons-capture` writes one entry per run, `lessons-learn` reads the accumulated log for a target skill, synthesises the durable signal out of it, and applies user-approved improvements directly to that skill's `SKILL.md`. Processed entries are moved to an archive so the next run does not reconsider them.

The user invokes this deliberately — e.g. once a fortnight, or when they notice the log for a skill has grown. It is not chained from any other skill.

## Input

The calling user (or skill, if ever invoked programmatically) passes the target skill's slug as the only argument — e.g. `feature-design`, `feature-plan`, `feature-implement`.

If no argument is provided, list the slugs under `~/.claude/dev-skills/lessons/` that have at least one entry with a real recommendation (i.e. not just "No skill-improvement recommendations from this run."), and ask the user via `AskUserQuestion` which one to process. If the lessons directory does not exist or no log has a real entry, tell the user there is nothing to learn from and stop.

## Step 1 — Locate the target SKILL.md

The target skill lives in this plugin under `skills/<slug>/SKILL.md`. Locate the absolute path on disk. The plugin can be installed anywhere, so do not assume a fixed prefix; instead, search:

```bash
find ~ -path "*/dev-skills/skills/<slug>/SKILL.md" 2>/dev/null
```

- If exactly one match is found, use it.
- If multiple are found (e.g. one in `~/.claude/plugins/...` and one in a working clone), ask the user which one to edit. Do not guess.
- If none are found, tell the user the target skill could not be located and stop.

Read the target SKILL.md in full. All synthesis happens with the current skill content in context, so suggestions that are already addressed are dropped automatically.

## Step 2 — Read the lessons log

Read `~/.claude/dev-skills/lessons/<slug>.md` in full.

- Parse each `## <timestamp>` entry.
- Discard entries whose body is "No skill-improvement recommendations from this run."
- If nothing remains after filtering, tell the user the log has no actionable entries and stop.

## Step 3 — Group and synthesise

Cluster the surviving entries into a small number of distinct improvements (typically 1–5; rarely more). Two entries are in the same cluster if they target the same step / behaviour / failure mode, even when their wording differs.

For each cluster, draft **one** consolidated improvement, then run it through these filters in order. Drop any that fail:

1. **Already addressed?** — Read the current target SKILL.md again with the cluster in mind. If the improvement has already been incorporated since the lessons were captured, drop the cluster as obsolete. Note in the archive that it was dropped as already-implemented.
2. **One-off, not durable?** — If every entry in the cluster reflects a single project's quirk, a single user mistake, or a transient issue (flaky network, an LLM glitch), drop it. The bar is: "would this make the skill better on the *next ten* runs, not just the run that produced the lesson?"
3. **Language- or framework-specific?** — The feature-* skills are deliberately language-agnostic. If the cluster recommends a fix that names a specific language, framework, build tool, or test runner (e.g. "use `pytest -q`", "auto-detect Cargo.toml", "run `npm test`"), **rewrite it generically first** ("auto-detect the project's quiet test command from common manifests"). If you cannot reframe it generically without losing the substance, drop it — better no change than a change that pigeonholes the skill.
4. **Adds complexity for no clear win?** — If the proposed change makes the skill noticeably longer or more conditional, but the captured upside is mild, drop it. Skills decay under accumulated qualifiers.
5. **Reasoning is sound?** — Spot-check the captured *Expected benefit* against the current SKILL.md. If the benefit assumes a misreading of the skill, drop it.

What survives is the candidate list. **A typical run produces 0–3 surviving improvements**, even from a long log; that is healthy. If you find yourself with more than 5 survivors, you are probably under-filtering — re-apply filter 4 more strictly.

## Step 4 — Present each improvement to the user

For each surviving candidate, prepare a proposal with these fields:

- **What** — one-line summary of the improvement (generic phrasing).
- **Where** — the section / step in the target SKILL.md it touches.
- **Concrete edit** — the actual textual change you would apply (old text → new text, or "add the following after step N: ..."), so the user can judge it without opening the file.
- **Why** — one short clause, drawn from the cluster.

Present them via `AskUserQuestion`. Batch up to 4 proposals per `AskUserQuestion` call (the tool supports up to 4 questions). Each proposal becomes one question; use these options on every question:

- `Apply` (mark as Recommended only when the proposal is clearly an improvement; otherwise leave neutral).
- `Skip` — do not apply this, and archive the entries with status `skipped`.
- `Defer` — do not apply this and keep the entries in the active log so a future run reconsiders them.

The user can also pick `Other` to redirect (e.g. "apply but reword the heading"). If they redirect, ask one follow-up `AskUserQuestion` to confirm the revised wording before editing.

If after filtering there are **zero** surviving candidates, do not call `AskUserQuestion`. Tell the user nothing actionable came out of the log, archive the entries with status `dropped` (with the filter reason recorded), and stop.

## Step 5 — Apply approved edits

For each `Apply` decision, edit the target SKILL.md using the `Edit` tool with the exact `old_string` / `new_string` from the proposal. Apply edits one at a time so a failure on one does not roll back others.

If an `Edit` fails because the `old_string` is no longer unique or no longer present (the skill changed between proposal and apply), stop, surface the conflict to the user, and ask whether to retry with a refreshed proposal or skip. Do not try to "fix it up" silently.

**Never** auto-commit. The SKILL.md edits land in the working tree; the user reviews `git diff` and commits at their own pace.

## Step 6 — Archive the active log

Once Steps 4–5 are complete, archive the **entire active log file** as a dated snapshot, then rebuild a fresh active log containing only any `Defer` entries.

Concretely, via the `Bash` tool:

```bash
# 1. Snapshot the current active log under a UTC-stamped name.
#    If a snapshot already exists at this timestamp (multiple runs in the same
#    minute), append a -2, -3, ... suffix.
SRC=~/.claude/dev-skills/lessons/<slug>.md
STAMP=$(date -u +%Y-%m-%dT%H%MZ)
DEST=~/.claude/dev-skills/lessons/<slug>.archive-${STAMP}.md
N=2; while [ -e "$DEST" ]; do DEST=~/.claude/dev-skills/lessons/<slug>.archive-${STAMP}-${N}.md; N=$((N+1)); done
mv "$SRC" "$DEST"
```

The archived snapshot is the active log exactly as it was at the moment of processing — no per-entry status tags are written into it. The session summary in Step 7 records which entries were applied / skipped / deferred for this run; that is the audit trail.

If any entries were marked `Defer` in Step 4, write a new active log containing just those entries (in their original order, with original timestamps and bodies). Otherwise, do **not** recreate the active log — let the next `lessons-capture` run create it fresh.

The session summary should reference the snapshot path so the user can revisit it if needed.

## Step 7 — Present a summary

Output a short chat summary so the user sees what changed without having to diff:

```
Archived: ~/.claude/dev-skills/lessons/<slug>.archive-<stamp>.md
Target:   <absolute path to target SKILL.md>

**Entries reviewed:** <N>
**Improvements applied:** <count>
- <one-line description of each applied change>

**Skipped / dropped:** <count> (<one-line reason per item, if useful>)
**Deferred:** <count> (written back to ~/.claude/dev-skills/lessons/<slug>.md)

**Next step:** review `git diff` for the target SKILL.md and commit when satisfied. This skill does not commit or push.
```

Keep the summary under ~25 lines.

## Constraints (non-negotiable)

- **Never auto-commit.** SKILL.md edits stay uncommitted so the user retains full review.
- **Never push or run any git command other than `status`/`diff` for the user's information.**
- **Never edit any SKILL.md other than the target slug's.** Do not improve sibling skills as a side-effect, even if you spot something.
- **Language-agnostic survives, language-specific dies.** Generic reframing is allowed; pigeonholing is not. When in doubt, drop.
- **Filter aggressively.** A run that applies 0 changes is a valid outcome. A run that applies 5+ changes is suspicious.
- **Archive is read-only after the snapshot is written.** Once `<slug>.archive-<stamp>.md` exists, never modify it. If the user wants to reconsider a deferred-then-archived entry, they copy it back into the active log manually.
- **Never overwrite an existing archive file.** Each run gets its own UTC-stamped filename; collisions get a numeric suffix.
- **Do not invoke `lessons-capture` at the end.** This is a meta-maintenance skill; it does not feed its own reflections back into a log.
