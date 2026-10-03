---
name: whats-next
description: Use when asked "what should I work on next?", "what's the backlog?", or when planning a session, prioritizing a project's open work, or checking that nothing pending has been missed. Assumes the docs-architecture conventions (a CLAUDE.md router + charter'd reference set).
---

# What's next (backlog triage)

Answer "what's next?" by **sweeping every backlog source**, separating **live-actionable** work
from **accepted constraints**, and returning a **categorized, prioritized backlog plus a
coverage manifest**. Prioritization is innate to a capable agent; the rules below force the two
things unguided runs omit — the manifest ("did I see everything?") and the accepted-constraints
list ("considered; by design; skip") — plus sweep completeness. This is the planning layer on
top of the docs-architecture family (it consumes audit flags and maintain's residue as backlog
inputs; doc hygiene itself belongs to the siblings). **After** an audit when doc currency is in
doubt: stale docs → stale backlog, so currency-check first.

## Sweep — every row; manifest whatever you can't reach
| Source | Yields |
|---|---|
| working tree + `git status` / `log` | uncommitted WIP to finish; recent direction |
| ROADMAP "Future directions" / "Next" / known-limitations | planned features + accepted limits |
| `CLAUDE.md` + docs gotchas | hazards — most are *accepted constraints*, not work (W1–W2) |
| journal `docs/` + `NOTEBOOK.md` "pending / open items" | un-promoted decisions, open questions |
| code `TODO` / `FIXME` (note **whose** — first-party vs vendored/upstream) | actionable only if first-party |
| planning/change-tool state (e.g. `openspec/` changes, issue tracker) | in-flight work |
| **audit findings** (`docs-architecture-audit` output) | doc-drift fixes |
| cross-repo blockers / consumers | dependencies + sequencing |
| tests / build status | red = urgent |

## Rules
- **W1.** Live-actionable requires a **live marker**: a first-party `TODO`/`FIXME`, an audit
  `flag-code-bug`, a ROADMAP "Next" item, or an explicit pending/open marker. Everything else —
  by-design, "do not re-litigate", deferred-by-decision, vendored/upstream — → the
  accepted-constraints list (shown, not actioned).
- **W2.** **Default to accepted when unsure.** *(A false "todo" on every gotcha trains the user
  to ignore the output.)*
- **W3.** Bucket each actionable: **urgent** (red tests / broken) · **deferred-fix** ·
  **future-feature** · **doc-debt**.
- **W4.** Rank by value × (1 / effort) × **exposure-if-deferred** — the cost of *not* doing it
  (what it blocks or de-risks); implementation riskiness alone never raises rank. Tag effort
  (XS/S/M/L) + risk.
- **W5.** Deliver a **top-N with a recommended sequence** (what unblocks / de-risks what) —
  never a flat list. Priority is a *proposal*; the user owns the call.
- **W6.** **REQUIRED:** reuse the fan-out from **docs-architecture-audit** — independent passes,
  merge, **loop-until-dry**. *(Passes agree on the core; the margins are a coin-flip.)*

## Two REQUIRED outputs
- **W7.** **Coverage manifest** — a table over every sweep row: **swept** (with what it yielded)
  or **not reached** (and why — no run logs, vendored, sibling repo). *(Without it the backlog
  reads complete when it isn't — the #1 unguided omission.)*
- **W8.** **Accepted constraints — "considered, not work"** — each with the one-line reason to
  skip. *(Shows the work; prevents re-litigation.)*

Full rationale + RED/GREEN provenance:
https://github.com/Apoplectic1/YetAnotherSkillsRepo/blob/main/docs/docs-architecture-design.md
