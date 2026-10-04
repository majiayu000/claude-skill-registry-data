---
name: codebase-cost-estimator
description: "Estimate the full development cost of an existing codebase from lines of code, architectural complexity, and team-composition overhead. Use for 'how much would this cost to build', 'what did this codebase cost', development-cost or build-cost estimates, calendar-time estimates, and Claude/AI ROI on a delivered codebase. Estimates by measured LOC and complexity, not by ticket volume."
when_to_use: |
  Use when you have an existing codebase and need a defensible build-cost estimate: catalog
  lines of code by language, convert to developer-hours with productivity rates and overhead
  multipliers, research current market hourly rates, convert raw hours to calendar time with
  organizational-overhead factors, layer in full-team cost (PM, design, QA, DevOps), and
  optionally compute AI/Claude ROI for a codebase built with AI assistance. Triggers on
  "how much would this cost to build", "what did this cost to build", "development cost
  estimate", "build cost", "engineering cost", "rebuild cost", "calendar time to build", or
  "Claude ROI"/"AI ROI" for a delivered codebase.

  Not when: the task is pricing a *future*
  project from a spec rather than measuring an existing codebase (there is no code to count
  yet) — scope the spec first, then return here once code exists.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Codebase Cost Estimator

Estimate what it cost (or would cost) to build an existing codebase. The estimate is driven by
**measured lines of code and complexity** — not by ticket count, story points, or feature lists.
Always present a range with explicit assumptions; never a single number.

## Inputs

- A checked-out codebase (local path or repo) you can run `git`, `cloc`/`tokei`, and file counts against.
- Optional: project README/status for version and scope context.
- Optional: git history, for the AI-ROI step (commit timestamps).

## Process

1. **Measure the codebase.** Count LOC by language and separate production code, tests, and docs.
   Prefer a real counter over guessing:
   ```bash
   # whichever is installed; both break LOC down by language
   tokei .        # or: cloc --vcs=git .
   ```
   Record per-language LOC, test LOC, doc LOC, and total. Note complexity drivers: advanced
   frameworks, system-level/GPU/native code, and third-party integrations. These map directly to
   the productivity bands in `references/rates.md`.

2. **Convert LOC to raw developer-hours.** For each code category, divide its LOC by the
   lines-per-hour band in `references/rates.md` (e.g. simple CRUD/UI 30–50 LOC/hr; GPU/shader
   10–20 LOC/hr; comprehensive tests 25–40 LOC/hr). Sum to a raw coding-hours subtotal. Keep the
   per-category breakdown — it is the audit trail for the estimate.

3. **Apply overhead multipliers.** Raw coding time is not total engineering time. Add the
   multipliers from `references/rates.md` for architecture & design, debugging, review &
   refactoring, documentation, integration & testing, and learning curve. Total overhead is
   typically 1.9x–2.25x raw coding hours. This yields **total estimated engineering hours**.

4. **Research current market rates.** Web-search hourly rates for the relevant tech stack and
   seniority **for the current year** — do not use stale figures. Build a low / median / high
   rate table and state the rationale for the recommended rate (stack, specialization, region).

5. **Convert to calendar time.** Raw hours ≠ wall-clock delivery. Apply the
   organizational-overhead efficiency factors in `references/org-overhead.md`
   (`Calendar Weeks = Raw Dev Hours ÷ (40 × Efficiency Factor)`) and show calendar time across
   company types (lean startup → enterprise), since a solo founder and a bureaucracy ship the
   same code on very different timelines.

6. **Layer in full-team cost.** Engineering is not the whole bill. Apply the supporting-role
   ratios and team multipliers in `references/team-cost.md` (PM, UX/UI, eng management, QA,
   program management, tech writing, DevOps) to produce a role-by-role breakdown across company
   stages, plus a full-team total.

7. **Assemble the estimate.** Use the structure in `assets/output-template.md`: codebase
   metrics, dev hours, calendar time, market rates, engineering cost (low/median/high), full-team
   cost, grand-total summary, confidence level, and assumptions.

8. **AI / Claude ROI (optional).** If the codebase was built with AI assistance, follow
   `references/claude-roi.md` to estimate Claude's actual active hours (git-commit clustering
   preferred; file timestamps or `LOC ÷ 350` as fallbacks) and compute value per Claude hour,
   speed multiplier vs. a human developer, and cost ROI.

## Key principles

- **Estimate from measured LOC and complexity — never from ticket volume or story points.**
- Always show ranges (low / median / high). A single number is a lie about precision.
- State confidence level and every load-bearing assumption.
- Use current-year market rates; flag the search date.
- Present professionally — the output should stand up in front of a client or stakeholder.

## References

- `references/rates.md` — lines-per-hour productivity bands and overhead multipliers
- `references/org-overhead.md` — efficiency factors and the calendar-time formula
- `references/team-cost.md` — supporting-role ratios and full-team multipliers
- `assets/output-template.md` — the stakeholder-ready estimate template
- `references/claude-roi.md` — AI/Claude ROI calculation method
