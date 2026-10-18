---
name: forge-scribe
description: "Owner-wish ledger: every ask kept verbatim until done+acked. Use for: onthoud dit, wat wilde ik ook alweer, ik heb nog een wijziging, note my change, scrap that, open wishes, did I ask that."
---

# Forge Scribe — never lose what the owner asked

**Self-improvement substrate:** before applying this skill, read `learnings.md` in this skill's own folder
and honor its corrections. After a run that produced a genuine correction, append it there with a date
and real evidence — never invent a lesson.

Every owner prompt is kept word-for-word (secrets scrubbed) and becomes a tracked item `R-n` that stays
visible until it is planned, done **with evidence** and acked **by the owner**. The only way to change
scribe state is `node .claude/forge-bin/forge-scribe.cjs`. Never edit the files under `.claude/forge-scribe/`
by hand.

## When to use
- The owner sends a new wish, change, cancel or preference mid-project ("onthoud dit", "ik heb nog een
  wijziging", "note my change", "scrap that", "voortaan…").
- The owner asks what they asked before ("wat wilde ik ook alweer", "open wensen", "did you miss
  anything I asked").
- End-of-run reconciliation (before finalize) and on resume of a long project.

Not for: storing a standing rule directly (that is `/forge remember`), writing a PRD (`forge-prd`), or
taking meeting minutes of a document.

## Context rule
Only `DIGEST.md` (<= 1200 chars) goes back into context. Never paste `inbox.jsonl` or `ledger.jsonl`.

## Wiring (hooks, rule, finalize)
The hook prints `[forge-scribe] Genoteerd: R-n …` per captured prompt (the digest only when it changed); act on it.
A Stop reminder blocks once per unplanned item; before completion log `owner_requests_reconciled` (the writer refuses
it unless `gate` is OK) — see `config/orchestration/HOOKS_OPT_IN.md` section 7.

## Lifecycle
`unclassified -> open -> planned -> in-progress -> done (evidence) -> acked (owner)`;
side states: `defer-proposed` (an agent's `defer`, with reason; NOT final until the owner acks it, then `deferred` = a recorded carry-over), `cancelled` (owner), `superseded`, `answered`.

| Step | Command (`node .claude/forge-bin/forge-scribe.cjs ...`) |
|---|---|
| capture (automatic: the UserPromptSubmit hook `forge-scribe-hook.cjs`; by hand only for a missed prompt) | `capture --text "<prompt>" --source cli --transcript <path>` |
| settle an unclassified item | `classify R-n change` (split a multi-ask: `--split "<exact quote>"` per ask) |
| mid-run change: which packages? | `impact R-n --run <run_id>` (read-only proposal) |
| plan it | `link R-n --wp wp-3,wp-5 --run <run_id>` |
| start / done | `transition R-n start` · `transition R-n done --evidence wp_completed:wp-3 --run <run_id>` |
| propose a carry-over (becomes `defer-proposed`; needs the owner's ack) | `transition R-n defer --reason "<why>"` |
| question answered | `transition R-n answer --reason "<where>"` |
| owner ack / cancel | `transition R-n ack --prompt P-n` (`--pid` is kept as an alias). P-n must be a hook-captured owner prompt with a clear yes for that exact R-id in the same sentence; no other wording counts as owner approval |
| status | `list --status open,planned --json` · `digest --write` |
| gate | `gate` (run) · `gate --final` (programme end: also done-but-unacked) — exit 3 = blocked |

Evidence types: `wp_completed:<wp_id>` (linked wp, real event in the run), `check_passed:<event_id>`,
`commit:<sha>`, `standing_rule:<rule id>` (preference items only).

## Preferences
A `preference` item ("voortaan…", "always…") is NOT stored as a rule by the scribe. Run
`forge-scribe.cjs route R-n`, ask the owner to confirm, then `forge-standing.cjs remember "<text>"`
(the existing `/forge remember` path) and close with `done --evidence standing_rule:<id>`.

## Mid-run change protocol
1. `impact R-n --run <id>` → proposed wp_ids. 2. Confirm with `link`. 3. Amend a not-started package, or
re-create a completed one as a new `agent_work_package_created` with `supersedes` and `req_ids:["R-n"]`.
4. Head Chef triages only that delta.

## Acks are batched
At the end of a run present ONE list of done-unacked items to the owner (batch-the-asks rule). Never
pause mid-run per item. Ack/cancel are refused unless the prompt is a real owner message in the session
transcript — a classifier, not a proof.

## When to dispatch the Scribe agent (sonnet/low, GOAT quick route)
The `scribe` specialist (`.claude/agents/scribe.md`, exec-reviewer class, no Write/Edit) is dispatched by
the Lead only for a prompt flagged `multi_ask` (3+ asks), end-of-run reconciliation, or a resume with
>= 20 open items. The normal path costs no LLM call: the Lead runs the CLI directly.

## Honesty
Never report an item as planned, done or acked unless `forge-scribe.cjs` output says so; quote the
literal `gate` exit code.
