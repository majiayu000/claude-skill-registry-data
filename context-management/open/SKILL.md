---
name: open
description: Boot the session, load context from the vault, and surface what matters
trigger: /open
status: DEPRECATED by the two-verb lifecycle — see skills/resume/SKILL.md. /resume absorbs /open; the post-clear boot runs it automatically via daemons/resume-verb.mjs. Kept for manual invocation during the transition; not deleted.
---

# Session Open

> **Deprecated.** This skill is superseded by [[skills/resume/SKILL.md|/resume]] (docs/two-verb-lifecycle.md). New installs should reach for `/resume`; this file stays for anyone still invoking `/open` by habit during the transition.

Run this at the start of every normal working session.

## Nightly alert surface

Before normal orientation, run the local watchdog with the same configured time
zone and cutoff used by the pass:

```text
node daemons/nightly-watchdog.mjs --root <aigent-root>
```

Surface every active named alert from
`vault/memory/runtime/NIGHTLY_ALERTS.jsonl`. The append-only ledger and stderr
are the default delivery channels; no external coordination service is
required. If the ledger is unreadable, report `ALERT_LEDGER_INVALID` and
continue the resume path. An alert-read failure must never suppress session
orientation or make the hook indistinguishable from "not installed."

## First-run detection

Before the normal protocol, read `.aigent/state.json`.

- If `status` is not `ready`, run `/start` instead of the normal open protocol.
- If the JSON state is missing but `.aigent/first-run-done` exists, treat the installation as ready and create the JSON state as a compatibility migration.
- Do not inspect natural-language placeholders in `system/00_identity.md`. Product state belongs in machine-readable state, not in whether a sentence happens to survive an edit.

## Protocol

**Unbanked-session recovery:** Compare `.aigent/last-close`, if present, with the newest Session Captures in `vault/daily/`. If newer captures exist, recover a short summary into `vault/memory/SESSION_LOG.md`, mark it `(auto-recovered)`, and continue. State the recovery in one neutral line.

1. **Load the heat index** from `vault/memory/HEAT_INDEX.json` when present. Use `hot_top_20` as the prioritized reading list. If missing, use steps 2 through 6 normally.
2. **Read the latest daily note** in `vault/daily/`.
3. **Read the session log** at `vault/memory/SESSION_LOG.md` and extract the newest next action and open threads.
4. **Read active priorities** at `vault/memory/ACTIVE_PRIORITIES.md`.
5. **Follow the graph** from the latest daily note and open threads into the three to five most relevant project, concept, person, or agent notes.
6. **Check delegation** at `vault/memory/DELEGATION_TRACKER.md` for blocked, stale, or review-ready work.
7. **Decision aging**: compare `vault/memory/DECISION_LOG.md` and `vault/memory/DECISION_OUTCOMES.md`. Surface at most three unresolved decisions around 30, 60, or 90 days old.
8. **Attention reconciliation**: compare the last seven days in `vault/daily/` with intended focus in `vault/memory/ACTIVE_PRIORITIES.md`. Surface material drift only.
9. **Skill gap scan**: once per week, inspect `memory/SKILL_GAPS.md`. If an open gap is older than seven days, run `/skill-hunt` on the oldest one and update the ledger if resolved.
10. **Compute runtime state**:

```bash
python3 "$AIGENT_ROOT/daemons/runtime/update-active-state.py"
```

11. **Read runtime state** at `vault/memory/runtime/ACTIVE_STATE.json`. Use `next_valid_action`, `blocked_items`, active reflexes, and mode to orient the session.
12. **Reconcile weekly**: on Monday or after seven days without a reconciliation, run `/reconcile` and surface contradictions only.

## Output

Give a brief greeting, then surface only:

- Due decision-aging prompts.
- Material attention drift.
- Stale or blocked items.
- Work dropped from the previous next action.
- Open threads requiring attention now.

If nothing needs flagging, greet the operator and let them drive. Do not dump a full priority report merely because the files exist.
