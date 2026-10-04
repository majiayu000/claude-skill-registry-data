---
name: using-the-harness
description: Session-start orientation for this team harness. Load first, before any work. Explains the operating contract, when each skill triggers, and how installed companion plugins supply agent-craft capabilities while this harness supplies the team contract. Trigger at the start of every session and whenever unsure which skill applies.
---

# Using the Harness

This is a **team operating harness**: one shared contract for humans and AI agents
working in the same repository — same rules, same risk tiers, same evidence, same
definition of done. It exists to make a mixed human–AI team coherent, not to make one
agent faster.

A skill supplies a repeatable procedure. It never supplies permission or accountability.

## First actions, every session

1. **Ground in the contract.** If this project has adopted the operating model, read its
   project profile before anything else (`docs/operating-model/PROJECT-OPERATING-PROFILE.md`),
   then the manual it binds. Profile facts beat inference.
2. **Classify risk before acting.** Map the requested work to R0–R3. Round ambiguity
   upward. Confirm authority at that tier before any consequential, destructive,
   external, or credential-touching action.
3. **Route before doing.** Check the routing table below. If a skill applies to the
   work, use it. If you are unsure which applies, use `delivery-orchestrator`.

## Core invariants — not negotiable

- **Classify risk before confirming authority.** Approval is scoped to actual risk.
- **Infer intent; never infer permission.** Useful intent is not a grant of authority.
- **Receipts, not polish.** Produce an artefact or a pass/fail verdict, not a narrative.
- **Review binds to the exact candidate.** Any change after review invalidates it.
- **`seed` is not `active`.** A seed profile supports design and R0/R1 work only.
- **Never invent a project fact.** Unknowns get an owner and a resolving trigger.
- **Insufficient evidence is a stop, not a prompt to improvise.** Tag the roster role
  that owns the decision; silence never converts to permission.

## Skill routing

| Work in front of you | Skill |
|---|---|
| New repo, or operating model install/repair | `operating-model-bootstrap` |
| Multi-track epic, or "which skill applies?" | `delivery-orchestrator` |
| An agreed goal to drive to a working, merged outcome while the operator is away | `get-it-done` |
| The machine is slow, tests or browser skills left processes behind | `system-performance-guardrail` |
| Is everything live, any errors this week, the weekly SRE checkup of a GCP project | `cloud-checkup` |
| Is the page fast enough, Core Web Vitals, why is this route slow | `frontend-performance-audit` |
| Significant technical decision or ADR | `the-architect` |
| New feature, epic, or change — plan before code | `spec-first-delivery` |
| High-stakes decision, or before claiming done | `adversarial-gate` |
| Agent output feeding a decision, store, or another agent | `domain-validator` |
| Any PR or agent-generated code before commit | `pr-reviewer` |
| Anything about to ship to a real environment | `release-readiness` |
| CI triggers, Actions billing, issues, labels, branch protection, or release-tag workflow | `github-manager` |
| Release process governance: SemVer, ADR, changelog, release authority | `release-manager` |
| Enterprise policy, compliance, governance, or approved-vendor alignment | `governance-guardrail` |
| Status, standup, or situation report | `sitrep` |
| Plugin-directory, marketplace, or curated-list submission | `plugin-submission` |
| LLM/cloud cost estimate or architecture with LLM calls | `cost-guardrail` |
| Google ADK multi-agent design | `adk-expert` |
| Any cloud-vendor workload (GCP, AWS, Azure, Alibaba Cloud) | `cloud-expert` (`the-architect` routes) |
| Adding or reviewing an MCP server | `mcp-server-scaffold` |

## Companion plugins

Agent-craft capabilities may be provided by installed companion plugins instead of these
skills — see `INTEGRATIONS.md` for the evaluated map (simplicity discipline, TDD
methodology, frontend design review, and similar craft lanes).

- Route craft work to an installed companion when the project profile names one as the
  provider. Do not re-implement a capability an installed companion already provides.
- Companions supply capability, never authority. This harness's risk tiers, evidence,
  and review gates still apply to their output.
- No companion installed? The baseline skills above are the fallback. Record the
  equivalent and its owner in the project profile; do not silently skip the capability.

## Harness tool mapping

Skills name actions, not tools. The per-harness translation lives outside the
canonical skill bodies:

- **Antigravity (Gemini)** — read `references/antigravity-tools.md` (in this skill's
  directory) before acting; it maps subagent dispatch, task tracking, and file/search
  actions to Antigravity's native tools.
- **Kimi Code** — the plugin manifest's `skillInstructions` carry the mapping.
- **Claude Code / Codex** — the skills' action vocabulary resolves to the native
  tools of the same names.

## Anti-rationalization table

| Excuse the agent makes | Counter |
|---|---|
| "The skills are just docs — I can skip them" | The skills are the harness. Skipping them is running without the contract. |
| "This task is too small for a skill" | Gates are proportional to risk — R0/R1 is cheap. Skipped small gates are where big failures rehearse. |
| "The companion plugin handles quality" | Companions own craft. Authority, evidence, and completion semantics stay here. |
| "I'll edit the skill body to fit my tools" | Porting adds a thin adapter or tool mapping. Canonical skill bodies never change per harness. |
| "I remember the contract from earlier" | Sessions compact and clear. Re-ground in the tracked profile; memory is not the contract. |
| "The user seems in a hurry" | Speed is easy. Safe speed is engineered. Hurry raises risk tier, it does not lower it. |

## When unsure

Route through `delivery-orchestrator`. Record every unresolved fact with an owner and
the trigger that resolves it. Stop before any R2/R3 mutation or external action that
lacks explicit authority and runnable controls.
