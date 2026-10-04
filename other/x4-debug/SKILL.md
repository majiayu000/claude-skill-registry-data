---
name: x4-debug
description: Read and summarize the active X4 profile's debug.txt, filtering known-benign noise and surfacing only real mod errors. Use after an in-game test, or when the user asks what went wrong or to check the debug output.
allowed-tools: Read, Bash
---

Read the active profile's debug log and report only REAL errors.

**Run the tool first, do not hand-roll the triage.** `uv run --python 3.13 x4debug triage [log]` resolves the log
the same way this skill does, states its mtime and whether the session was a NEW GAME or a save
load, and buckets **every** `[=ERROR=]` line by mod, by script, by engine subsystem, and by
unclassified residue. Its rows are required to sum to the lines read.

A hand-rolled `grep | sort | uniq -c` pass cannot tell you what it dropped. That is not a
hypothetical: the parser underneath this skill silently discarded 44% of a real log for two weeks,
and the most consequential defect in that log sat in the discarded part.

Then, for any mod the log names:

- `uv run --python 3.13 x4debug crosscheck <deployed-mod>` — a **per-item** diff of the ops the engine SKIPPED
  against the ops x4validate predicted would fail. Three buckets, never two totals: agreed,
  predicted-only (a stale prediction, or an op that never ran), and **observed-only**, which is a
  blind spot in the validator and should be reported as one.
- `uv run --python 3.13 x4debug baseline` — archive the log with a content fingerprint, so the NEXT launch can be
  diffed against this one instead of against a remembered number.

**Never compare two logs by their totals.** Compare per bucket and per item; a net-zero change is
the shape a real regression hides in.

**Locating the log.** Resolve it, never hard-code it: `$X4_DEBUGLOG`, else
`$X4_PROFILE/debug.txt`, else ask. If neither is configured the profile lives at
Windows `Documents\Egosoft\X4\<profile-id>\` and Linux `~/.config/EgoSoft/X4/<profile-id>/`. `x4validate --paths` prints what the toolkit resolves. A profile
folder is a numeric id; if several exist, confirm which is active rather than guessing — a stale
profile's log will look plausible and be months old, so **check the file's mtime before trusting
it**.

## How to classify a line

Work in this order. The goal is a short list of things that are actually broken, not a transcript.

**1. Benign by category — do not report:**
- `Failed to verify the file signature` (error 13/14) — normal for every unsigned mod.
- `LibraryLoadout()` / `ConstructionPlan()` errors naming an extension id that is **not installed** —
  the player's saved loadouts/blueprints referencing a mod they no longer have. Unrelated to the mod
  under test.
- Errors whose root cause is vanilla data rather than any mod. Prove it before dismissing: the
  claim "vanilla does this too" needs a `reference\` check, not an assumption.

**2. Known-benign specifics — consult, don't memorize.** The catalogue of *which* mods currently
produce known-harmless volume, and why, lives in **KNOWLEDGEBASE.md → "Debug triage"**. Read it at
triage time. It is dated and revisable; this skill is not the place for it, because a mod list
changes and a skill that names mods goes quietly stale and starts suppressing real findings.

**3. Expected-and-correct — do not report as a regression:**
- An upstream mod's failing `<replace>` still logs even when a load-last overlay supplies the value
  afterwards: the upstream op runs first and fails regardless. **Judge such fixes by the effective
  value (`x4effective who-sets`), not by the log line disappearing.**
- A mod's own ambiguous selector (`Multiple matching nodes ... Skipping`) when an overlay is
  deliberately supplying the content instead.

**4. Everything else is a finding.** Focus on `[=ERROR=]` and `[=WARNING=]`. Group by mod/source,
quote each with line numbers, and name the likely cause: XML parse error, missing/unresolved
reference, unknown event or property, or a missing required attribute. For version-shift symptoms,
cross-check the **Version Migration Map** in KNOWLEDGEBASE.md.

## Comparing two logs

Check whether each log is a NEW GAME or a save load (`grep -c "Universe generation begins"`). Raw
error **counts are not comparable across that boundary** — compare per-category presence/absence
instead.

## Reporting

Summarize: total real errors, grouped by source, highest-severity first. Say explicitly what you
filtered and why, so the user can challenge a filter.

**A mod that loads without crashing is NOT necessarily correct** — call out silent reference
failures, and remember the log only lists *failures*: an op that silently did nothing successfully
never appears. Pair the log with `x4validate` (which models what the engine sees) rather than
treating a quiet log as proof.

## Deferrals

If the user has explicitly deferred a known-noisy source, collapse it to a single counted line —
but record the deferral **with its reason and date in the KB or registry**, never as a standing
instruction here. A deferral written into a skill outlives the decision that justified it: one such
line survived the mod being uninstalled and kept telling every session to ignore errors that could
no longer occur.
