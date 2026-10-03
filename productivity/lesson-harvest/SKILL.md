---
name: lesson-harvest
description: Process chat sessions into durable lessons — walk unprocessed transcripts (Claude first; other lanes as enumerators land), extract every defect/workaround/correction/insight, route each to its EXISTING durable owner (censor precedent, his-hand lever, memory file, board task), and stamp the session processed in censor/lesson-harvest.jsonl. Use when asked to "process chats/sessions into lessons", "harvest lessons", "drain the session backlog", or when the lesson-harvest-backlog sensor reports unprocessed sessions. The mechanical half (queue, cursor, backlog predicate) is scripts/lesson-harvest.py; this skill is its model-in-the-loop complement, the sibling of vendor-insights, experience-judge, and decorum-voice-judge.
---

# lesson-harvest

The operator's law (memory `feedback-codify-every-session-lesson`): every discussion carries
lessons, and a discussion not processed into a durable owner was wasted. `scripts/
lesson-harvest.py` owns everything deterministic (queue, cursor, backlog); this skill owns
only judgment — reading a session and deciding what it taught, where that lesson binds, and
whether it is already codified.

**Iron rules:**
- Route ONLY to existing termini. Never invent a new ledger, doc, or registry for a lesson
  (`PREC-2026-07-30-plan-decisions-dont-bind`: a lesson binds only when it names a registry
  path, predicate script, lever id, or precedent id).
- PII firewall: owner refs and one-line summaries only. No verbatim personal content, no
  third-party names, no secrets, no `/Users/...` paths in anything tracked. Person-scoped
  material (people reviews, relationship content) is NOT a lesson-harvest output — it
  belongs to the `_people-private` review lane (ARCA-sealed), and in a background session
  its writes are classifier-gated; cite `existing` and move on.
- Bounded reads only: `vendor-insights.py cat-session` excerpts, never whole-file loads.
- Tier the fan-out: session reading is scan-class work — use cheap-tier subagents for the
  first pass; reserve the session model for judgment on candidate lessons.

## Steps

1. **Queue.** `python3 scripts/lesson-harvest.py --queue [--vendor claude] [--limit N]`
   → TSV: vendor, session id, project label, day, bytes. Newest first. Note the excluded
   vendors it prints — carry them into your report verbatim (backlog unknown ≠ zero).
2. **Read.** For each session:
   `python3 scripts/vendor-insights.py cat-session --vendor claude --session <sid>`
   (raise `--max-chars` only when the excerpt truncates mid-incident). Look for: a
   correction from the operator; a workaround that was narrated but not codified; a wrong
   confident claim and what refuted it; a gate/tool/method fought twice; a decision that
   binds future sessions. Skip pleasantries and routine execution — a lesson is something
   the NEXT session would otherwise get wrong.
3. **Dedupe against the owners first.** Before writing anything, check whether the lesson
   already lives somewhere: `grep` censor/precedents.jsonl, `his-hand-levers.json`, the
   memory index (`.agent-runtime/claude/projects/<project>/memory/MEMORY.md`), and CLAUDE.md.
   Already owned → record `{"owner_kind":"existing","owner_ref":"<the id/path>"}` and write
   nothing new.
4. **Route each genuinely new lesson** by the cascade:
   - Repeatable correction with a binding site → **precedent**: append one JSON line to
     `censor/precedents.jsonl` matching the live schema (`id: PREC-YYYY-MM-DD-<slug>`, `ts`,
     `type`, `subject`, `outcome`, `reversible`, `action` naming WHERE it binds, `authorised_by` (the file's uniform
     spelling — all 36 records), `review`). Any script it cites must exist (`check-runner-coverage.py` E).
   - Irreducible human atom → **lever** in `his-hand-levers.json` (id `L-…`, label with the
     concrete ~minutes action, owner, cost, unlocks, source_task, issue).
   - Behavioral/project knowledge for future sessions → **memory file** (frontmatter
     `name/description/metadata.type`) + one pointer line in `MEMORY.md`
     (`evocator.py`-verifiable).
   - Buildable work → **board task** through the conduct broker (`limen conduct …` /
     TABVLARIVS) — never by editing `tasks.yaml`.
5. **Mark.** `python3 scripts/lesson-harvest.py --mark <sid> --vendor claude --lessons
   '[{"owner_kind":"precedent","owner_ref":"PREC-…"}, …]'` — or `--none-found` when a
   session genuinely taught nothing (processed is a state, not a success claim). Marking is
   idempotent; re-marking is a no-op.
6. **Report.** End with `python3 scripts/lesson-harvest.py --check` output: per-vendor
   remaining/processed, exclusions, TOTAL. The backlog number is the deliverable — never
   summarize a tranche as if it drained the corpus.

## Tranche discipline

Default tranche: 10 sessions, newest first (recency = highest un-codified density; the
oldest sessions' lessons mostly got codified since). The daily `lesson-harvest-backlog`
sensor keeps the remaining count on the beat, so stopping mid-backlog is safe — the state
is in the cursor, not in anyone's memory.
