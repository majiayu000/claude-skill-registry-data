---
name: ops-change-review
description: Assess the deploy risk of one production change — what it touches and its blast radius, the error budget status of the affected SLOs, the rollback and how long it takes, whether a flag or staged rollout is possible, and what to watch, ending in go, go with conditions or wait. Use when a team is about to ship a risky change to production. Not for reviewing the code itself; see /development-review.
metadata:
  argument-hint: "[project] <change>"
  stack-aware: true
---

# Change review

Decide whether the change in "$ARGUMENTS" should ship now, and how.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Stack.** Before you build, test, lint, run or generate code, read the `Stack` section of the project's `AGENTS.md`, or of `CLAUDE.md` when `AGENTS.md` has none. Use its commands exactly as written, its `layout` for where files go and its `rules` as requirements. If it names a `profile`, also read the file `<profile>.md` in the `stacks` folder of this skill's bundled references for the full commands, layout and rules; the project's own keys win where both speak. If there is no `Stack` section, run the `singular-detect` skill, state what you inferred in one line, and offer to write the section with `singular-init`. Never assume a package manager, test runner or formatter the project did not declare.

The change: a description, a pull request summary or a deploy plan. When `$ARGUMENTS` or the request names a project, use that name as `<project>` whether or not its folder exists yet in `.singularskills/ops/`. With no project named: with exactly one folder there, use it; with several, ask which; with no folder at all, read none and continue. Read `.singularskills/ops/<project>/01-inventory.md` (services, dependencies and **Tooling**), `02-slos.md` and the newest `06-review.md` when they exist.

## Process

1. **What it touches:** the services, data, schemas and dependencies, and the **blast radius**: which journeys and how many users would be hurt if it went wrong.

2. **The budget:** the error budget status of the affected SLOs from `06-review.md` or `02-slos.md`, and what the error budget policy allows now (a freeze means only P0 and security fixes ship).

3. **The way back:** how to roll back, how long it takes, and whether a rollback is possible at all (a data migration may not be reversible). Write the rollback steps for the tooling under **Tooling**, marking steps that **change production**; with the tooling unknown, mark them **command to fill in**.

4. **Reduce the risk:** a feature flag, a staged rollout (one region or a small share of users first), a deploy outside peak hours, someone watching.

5. **What to watch** during and after: the SLIs and alerts, and for how long.

6. **The call:** **go**, **go with conditions** (name them), or **wait** (and until what).

7. **Never touch live systems.** Do not run any command against a live system, and never say a command, alert or runbook was tested or verified; you write them for people to apply.

## References

- `references/stacks/bun-react-ts.md` and `references/stacks/rust-gpui.md`: the shipped stack profiles

## Output

In chat: the call first, then the blast radius, the rollback and what to watch. This skill writes no file.
