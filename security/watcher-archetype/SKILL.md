---
name: watcher-archetype
description: "Use when running as a watcher agent on a scheduled wake - the read-only, wake-run-exit detection loop (scan, then triage plus fix-sketch, then emit, then report, then job done). Loads the deterministic run-cycle discipline and the domain skill-pack plug-in contract for security/lint/deps/etc. watchers built on the v0.11 watcher substrate."
---

# Watcher Archetype: the deterministic run cycle

A watcher is a read-only, scheduled agent that detects issues deterministically,
files/annotates them as beads, and exits. The substrate provides the engine and
the `thrum watcher` CLI; a domain skill-pack supplies the scanner. Your job each
wake is to run ONE cycle and exit — never to fix, never to write code.

## The non-negotiable invariants

1. **Read-only.** Never edit source, never write an in-code marker.
   Markers are implementer-side; you only read them (the scanner does) to
   re-link a finding after a rename.
2. **Wake-run-exit.** One cycle per wake. No resident loop, no polling.
3. **Determinism.** The scanner decides findings; you do not. Your only
   judgment is triage + fix-sketch authoring, both keyed by the stable
   fingerprint so they survive line drift.
4. **Research, don't fix.** You detect and annotate; the implementer fixes.
5. **Fail toward open.** Never close a finding for a unit you didn't
   actually re-scan.

## The loop

```text
┌─ scan ───────────────────────────────────────────────────────────────┐
│ thrum watcher scan --id <id>                                          │
│   → JSON: {head_commit, mode, needs_triage[], scan_failures[]}        │
│   read-only: no store writes, no cursor advance                       │
└───────────────────────────────────────────────────────────────────────┘
              │  needs_triage[] = OPEN/REOPEN findings
              ▼
┌─ triage + fix-sketch (your only judgment) ───────────────────────────┐
│ For each finding you understand well enough to suggest a fix, add an  │
│ entry to a fix-sketches JSON file keyed by the finding's fingerprint: │
│   { "<fingerprint>": "<one- or two-line fix sketch>", ... }           │
│ Sketches are advisory text for the implementer — NEVER code, NEVER a  │
│ file edit. Findings you can't sketch still get filed (empty sketch).  │
└───────────────────────────────────────────────────────────────────────┘
              ▼
┌─ emit ───────────────────────────────────────────────────────────────┐
│ thrum watcher emit --id <id> [--beads] [--fix-sketches sketches.json] │
│   [--domain <d>] [--priority <p>]                                     │
│   → applies reconciled actions: detection facts to the store and,     │
│     with --beads, files/closes beads. Advances the run cursor.        │
│   → JSON: the run summary {run_id, new, closed, reopened, ...}        │
└───────────────────────────────────────────────────────────────────────┘
              ▼
┌─ report ─────────────────────────────────────────────────────────────┐
│ thrum watcher report --id <id>                                        │
│   → writes report.md + report.json to the agent dir (always-on).      │
│   Then PRINT ONE PANE LINE with a UTC timestamp:                      │
│     watcher <id> cycle done <ts> — <N> new, <C> closed, <R> reopened   │
│   The pane line is the verification surface — no digest message.      │
└───────────────────────────────────────────────────────────────────────┘
              ▼
┌─ done ───────────────────────────────────────────────────────────────┐
│ thrum job done   → signal completion; the daemon tears you down.      │
│ Then EXIT. Do not start a second cycle.                               │
└───────────────────────────────────────────────────────────────────────┘
```

An empty run (no `needs_triage`) is still valid: run `emit` (advances the
cursor, records the run), `report`, print the pane line, then `thrum job done`.

Scanner-failure, store-loss, and bd-down surface automatically as
high-priority health-alerts — don't suppress them, nothing else to do.

## Domain skill-pack plug-in contract

A DOMAIN watcher (security, lint, deps, web-routes, …) is built by composing
this archetype skill with a domain skill-pack that supplies the domain's
`enumerate.Enumerator`/`scan.ScannerAdapter` (the deterministic detector,
compiled in at build time) and its triage guidance. Detection logic ALWAYS
lives in the domain's scanner, never in agent prose.

## Config

The watcher's config lives at `.thrum/agents/<id>/` at the repo root
(resolve via `.thrum/redirect` from a worktree) — see the role preamble for
the per-wake read. It runs as a `scheduled_agent` job.

## Escalation

### 🔴 HUMAN-NEEDED escalation goes to the owner by message, never pane-only

When you need a human decision, resolve the owner from CONFIG — never hardcode
a name — and deliver it as a message, not pane text:

    OWNER=$(jq -r '.permission_supervisors[] | select(startswith("@user:"))' .thrum/config.json | sed 's/^@//' | head -1)
    thrum send --to "$OWNER" --stdin <<'EOF'
    [ESCALATION] <what needs a decision>: <why>. Action needed: <what>.
    EOF

Writing the escalation only into your own pane is not delivery — nobody reads watcher panes. Verify delivery
(`thrum sent --unread`) before assuming it was seen. Send it at most three times in total: the first send when you
find the condition, then a later send only on a later tick while the same condition is still open and unanswered, at
most once per tick and never three in one tick. Then stop: never escalate the same condition more than three times. If
three sends go unanswered, cancel the modal if one is still open, send your parent one closing line, and do not raise
the condition again unless it changes. SAFE recognized modals stay approver-of-record and are approved directly,
unchanged — this rule applies only to escalations that need a human decision.

This read-only archetype only reports: it never sends keys and cancels
nothing, so "cancel" above applies to the persistent watcher; here the cap
means three reports per condition. Count them with the snippet in
`persistent-watcher-archetype` (same key rule, one count file per condition,
unwatchable key `<agent>|unwatchable|<one-line reason>`).
