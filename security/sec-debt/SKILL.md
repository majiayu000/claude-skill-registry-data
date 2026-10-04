---
name: sec-debt
description: Explain and list Peephole sec-debt markers — deliberate, human-authorized security trade-offs recorded in code. Use when the user says /sec-debt, wants to knowingly accept a security finding, or asks what deferred security items exist.
---

# Peephole sec-debt

A **sec-debt marker** is how a deliberate security trade-off is recorded so it is auditable
instead of silent. Write it as a comment **on or directly above the flagged line** — a marker
only applies to findings near it, never to the whole file:

```
# sec-debt: CWE-89 — internal admin tool, network-isolated; upgrade path: parameterize before exposing
```

Rules (binding):

- A marker is a **request, not a grant**. The agent cannot self-authorize. In strict
  mode a marker converts a would-be **deny** into an **ask** — a human decides. In
  hardened mode the deny stands (a hook cannot collect the typed confirmation);
  the human lowers to strict/audit to accept the trade-off.
- Every waiver is audit-logged. A marker **without a matching human approval** is
  treated as an evasion attempt: flagged at **Stop** and in `/sec-audit`, never
  silently honored.
- The stated precondition is the contract. If it stops holding (e.g. the route becomes public),
  the debt should be revisited.

## To list outstanding sec-debt

Run:

```sh
sh "$CLAUDE_PLUGIN_ROOT/hooks/peephole.sh" debt
```

It scans the codebase for every `sec-debt:` marker and cross-checks each against
`.peephole/secdebt-approved`, flagging any **UNAPPROVED** marker as an evasion
risk. A human approves a marker by adding its file (or `file:line`) to
`.peephole/secdebt-approved`. Review each unapproved marker: confirm the stated
precondition still holds, or fix the underlying issue.
