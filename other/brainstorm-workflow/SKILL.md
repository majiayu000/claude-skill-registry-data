---
name: brainstorm-workflow
version: "1.0.0"
user-invocable: true
description: "Design-to-plan host: thin wrap of Superpowers brainstorming, then hard handoff to solve-workflow Make a Plan. Use for new features and fuzzy design before coding. Triggers — 「头脑风暴」「设计头脑风暴」「brainstorm」「brainstorm workflow」「先设计再计划」「头脑风暴工作流」. Do NOT use for bug root-cause PDCA (solve-workflow / opsx-solve-workflow) or when you only need a one-line edit."
dependencies:
  - brainstorming
  - solve-workflow
---

# Brainstorm Workflow

> Thin **design-to-plan** host. Design dialogue is owned by external Superpowers `brainstorming`; implementation planning is owned by in-repo `solve-workflow`「制定计划」. This host owns prerequisite checks, path prompt, terminal override (no `writing-plans`), and hard handoff.
>
> **Not** a stricter `solve-workflow`. Bug root-cause / evidence-driven diagnosis → use `solve-workflow` or `opsx-solve-workflow`.
>
> **Output templates**: [reference.md](reference.md).

## Positioning

| This host | Prefer instead |
|-----------|----------------|
| New feature, fuzzy requirements, architecture/design before code | — |
| Collaborative design → approved spec → executable plan | — |
| Bug / regression / “why is it broken?” | `solve-workflow` / `opsx-solve-workflow` |
| Already have an approved plan, need execute/verify only | `solve-workflow` from「执行计划」 |
| Long unattended run toward a verifiable goal | `goal-driven-workflow` |

## Prerequisite skill check

At startup, verify every frontmatter `dependencies` entry. If any is missing, abort with the install table in [reference.md](reference.md) — **no silent degradation**.

| Missing skill | Install |
|---------------|---------|
| `brainstorming` | Install Superpowers (provides `brainstorming`), e.g. platform plugin from `https://github.com/obra/superpowers`, or `npx skills add https://github.com/obra/superpowers.git --skill brainstorming` when the skills CLI supports it. Directory / `name` MUST be `brainstorming`. |
| `solve-workflow` | `npx skills add FuDesign2008/open-skills -g --skill solve-workflow --yes` |

**Must not vendor:** do not add `skills/brainstorming/` to this repository.

## Triggers and modes

| Phrasing | Mode | Note |
|----------|------|------|
| 「头脑风暴」「设计头脑风暴」「先设计再计划」「brainstorm workflow」 | 👤 Manual | Default; pause at host exits below |
| 「自动头脑风暴」「自动模式」+ brainstorm intent | 🤖 Auto | After written-spec approval, hard-handoff without extra host pause |

**Mode detection:** trigger contains「自动」→ auto; else manual. Mid-run: 「切换自动模式」/「切换手动模式」.

## Flow (host orchestration only)

```text
0 Prerequisite check (brainstorming + solve-workflow)
1 Intent gate — if bug root-cause primary → redirect to solve / opsx-solve; abort this host
2 Load brainstorming — follow it for context → clarify → approaches → sectional design → write spec → self-review → user reviews written spec
   Host overrides (MUST win over brainstorming defaults):
   - Before write: ask save path; recommend docs/design/YYYY-MM-DD-<topic>-design.md
   - After written-spec approval: do NOT invoke writing-plans
3 Hard handoff — load solve-workflow at「制定计划」(Make a Plan); skip solve stages 1–4; pass design path + summary
4 Stop at solve stage-5 exit (plan confirmation) — further execute/verify is solve-workflow, not this host
```

### Host exits

| Point | 👤 Manual | 🤖 Auto |
|-------|-----------|---------|
| After intent gate (if redirect) | Stop; tell user to use solve | Same |
| Path prompt before writing design | Wait for path / accept default | May accept recommended default if user already said auto and topic is clear; still announce the path used |
| After user approves written spec | Confirm handoff once | Proceed to hard handoff |
| Inside solve Make a Plan | Follow solve-workflow stage-5 rules | Follow solve-workflow auto rules |

## Stage details

### 0–1. Gate

1. Run prerequisite check.
2. If the user’s primary goal is locating/fixing a defect in existing behavior (root cause), **redirect** to `solve-workflow` / `opsx-solve-workflow` and **abort** this host (do not start brainstorming as a substitute for `analysis-core`).

### 2. Delegate design to `brainstorming`

Load `brainstorming` and follow its checklist (explore context, one question per turn, 2–3 approaches, sectional design approval, write design doc, spec self-review, user review of the written spec).

**Overrides (host wins):**

1. **Save path** — Before writing the design file, ask where to save. Recommend: `docs/design/YYYY-MM-DD-<topic>-design.md`. User preference overrides. Do not silently use `docs/superpowers/specs/` unless the user chooses that path.
2. **Terminal** — After the user approves the written spec, **do not** invoke `writing-plans`. Go to hard handoff (§3).

Visual Companion and other brainstorming optional tools remain as defined by that skill (intent-only; no platform-tool hardcoding in this host).

### 3. Hard handoff to `solve-workflow` Make a Plan

1. Load `solve-workflow`.
2. Enter **Stage 5 — Make a Plan** only (skip stages 1–4 for this work item).
3. Supply handoff inputs ([reference.md](reference.md) § Handoff payload): approved design path, short summary (goal, chosen approach, constraints, non-goals).
4. Produce the plan per `solve-workflow` Stage 5. This host MUST NOT write business/production code.

After the plan is confirmed, the user continues inside `solve-workflow` (「执行计划」…) if they want implementation — that is outside this host’s success criteria.

## Red flags

- Starting design dialogue when the ask is bug root-cause analysis
- Invoking `writing-plans` after design approval
- Writing the design doc without a path question (unless auto accepted the announced default)
- Re-running solve stages 1–4 after a successful handoff for the same design
- Silent degrade when `brainstorming` or `solve-workflow` is missing
- Vendoring `brainstorming` into this repo
