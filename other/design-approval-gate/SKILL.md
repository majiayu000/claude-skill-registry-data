---
name: design-approval-gate
version: "1.0.0"
user-invocable: false
description: "Hard gate before production implementation: do not write behavior/production code until the chosen solution/design is approved; named escapes for auto mode, Jira auto/force, and lean hotfix require short 留痕. Referenced by PDCA hosts before execution stages. Triggers — 「设计批准门禁」「方案批准后才能写码」「实现前批准」「design approval gate」 / design approval gate, pre-impl approval. Do NOT use as a name alias for brainstorming."
---

# Design Approval Gate

> Internal shared skill. Single source of truth for **pre-implementation approval**. Hosts declare it in `dependencies` and abort if missing — no silent fallback.
>
> **Name note:** intentionally **not** named `brainstorming` (external skills repo). Use this name only.

## Iron Law

**NO PRODUCTION / BEHAVIOR IMPLEMENTATION WITHOUT DESIGN OR SOLUTION APPROVAL.**

- **Manual mode:** wait for explicit user pass (or equivalent structured confirmation) on the chosen solution/design before stage-6-style code edits.
- **Allowed before approval:** OpenSpec / host analysis artifacts; `analysis-core` analysis-assist temporary edits (must still roll back per that skill).
- **Forbidden before approval:** shipping the fix in business/production code; calling implementation skills for the purpose of landing the change.

## Named escapes (require 留痕)

These MAY proceed without a human pass; each MUST record a one-line 留痕 (escape name + reason):

| Escape | When |
|--------|------|
| **auto mode** | Host entered via explicit auto trigger («自动…» / `--auto`) |
| **Jira auto/force** | `jira-fix` / `opsx-jira-fix` auto or force path |
| **lean hotfix** | Host selected lean path with high-certainty hot fix |

**Not an escape:** "this is too simple" / unspoken skip in manual mode.

## 留痕 template

`【设计批准门禁逃生】escape=<auto|jira-auto-force|lean-hotfix>；reason=<short>；time=<ISO>。`

## Forbidden

- Silent skip in manual mode without approval or named escape
- Renaming this skill to `brainstorming` inside this repository
- Treating OpenSpec artifact writes as a violation of this gate

## Integration guide

- Hosts: one-line pointer before the execution stage — load this skill; do not paste the escape table into hosts.
- Prefer `user-invocable: false`.
- Compose with `workflow-mode-lifecycle`: auto escape only when auto mode is actually active.
