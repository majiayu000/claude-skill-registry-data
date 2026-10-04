---
name: line-check
version: 0.1.0
license: MIT
description: Use when asked to audit a repository, assess project health, find the highest-value improvements a repo needs, check whether a project is ready for contributors or coding agents, or decide what to work on next in a codebase.
---

# line-check

A chef's line check before service: walk every station, score it, and leave with an ordered list of what to fix first. The output is not a wall of findings, it is a backlog sorted by leverage (impact relative to effort) that someone could start executing immediately.

**Read-only.** Never modify the repo during an audit. If the user wants fixes applied afterward, that is a separate step on a branch.

## Stations

Walk all seven. Score each 0-5 (5 = exemplary, 3 = functional with real gaps, 1 = broken or absent, 0 = actively harmful).

| # | Station | What to check |
|---|---------|---------------|
| 1 | Docs and onboarding | README answers what/why/how-fast; quickstart commands actually exist and match the code; examples are current |
| 2 | Agent-readiness | AGENTS.md or CLAUDE.md present and accurate; memory/handoff wiring if the project uses it (`.brigade/`, `.claude/memory-handoffs/`); build/test commands documented for agents |
| 3 | Tests and CI | Critical paths covered, not just happy paths; CI exists and is green; lint/format gates wired |
| 4 | Hygiene | .gitignore excludes agent dirs (`.claude/`, `.codex/`) and build artifacts; LICENSE present (critical if public); no secrets or credentials in the tree; stale branches |
| 5 | Structure | Oversized files and god modules; dead code; tangled responsibilities; dependency health (outdated, vulnerable, unused) |
| 6 | Release hygiene | CHANGELOG maintained; version in code matches latest tag; tags not far behind the default branch |
| 7 | TODO and issue mining | In-code TODO/FIXME/HACK markers and open issues, folded into the backlog rather than reported raw |

Station guidance:
- For station 2, if the brigade CLI is installed and the repo has brigade wiring, run `brigade handoff doctor` and `brigade memory care scan` and fold their output into findings.
- For station 5, do not chase abstract purity. Find the friction that makes the code hard to change, and ask: what gets easier if this module disappears? Can a newcomer predict where the next change belongs?
- Respect .gitignore; never audit `node_modules/`, `vendor/`, `dist/`, or other generated trees.

## Execution

If the harness supports parallel subagents, dispatch one per station with the station's row above plus the finding schema below, then merge. Otherwise walk the stations sequentially. Either way, the merge step deduplicates findings that share a location and re-sorts the backlog across all stations.

## Rules

- Verify every finding by looking at the actual file before reporting it. A finding you could not verify gets downgraded one severity and marked `(unverified)` in its title.
- One finding per discrete problem. No "and also" findings.
- Every fix is an action with commands or a sketch, never "consider improving X".
- A few high-leverage findings beat a laundry list. If a station produced fifteen lows, summarize them as one finding.
- Always include the "Not checked" section. Silent gaps read as clean bills of health.

## Report contract

Severity: **critical** (active harm or imminent loss) / **high** (bites soon or blocks adoption) / **medium** (real cost, not urgent) / **low** (friction or polish) / **info** (worth knowing). Effort: **S** (under 30 min) / **M** (under half a day) / **L** (multi-day).

```markdown
# line-check report: <repo> (<date>)

## Verdict
One paragraph: overall state, the single most important thing to do,
and whether the repo is healthy, needs work, or on fire.

## Scorecard
| Station | Score (0-5) | Summary |

## Findings
Grouped by severity, descending. Each:
### [SEVERITY] Short imperative title
- **Station:** which station produced this
- **Where:** file:line, directory, or "repo-wide" (must be checkable)
- **What:** one or two sentences, concrete
- **Why it matters:** the consequence if ignored
- **Fix:** the specific action
- **Effort:** S / M / L

## Backlog
Findings re-sorted by leverage (impact relative to effort), numbered,
one line each: `N. [SEVERITY/EFFORT] title (station)`.
Cheap high-impact items float to the top regardless of severity.

## Not checked
What the audit skipped and why.
```

## Common mistakes

- Reporting raw TODO dumps or lint output instead of folding them into prioritized findings.
- Scoring from vibes. Every score needs at least one concrete observation behind it.
- Flagging a missing convention the project deliberately rejected. Read CLAUDE.md/AGENTS.md/ADRs first; deliberate choices are info, not findings.
- Auditing generated or vendored code.
- Ending without the backlog. The backlog is the deliverable; the findings are its evidence.
