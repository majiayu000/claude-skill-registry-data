---
name: buildr-operator
description: |
  Produces a complete, agent-executable project workspace from a human
  project description. Combines Forge (onboarding + scaffold), Vault
  (agnostic skills/constraints), Imperfektum (fabricated agent memory),
  and Orchestration (wave-based execution) into a single folder that
  any LLM agent can autonomously build from.

  USE THIS SKILL when: the user wants to build something — a website, app,
  tool, SaaS, booking system, e-commerce site, or any software project.
  Triggers on: "bygg", "skapa", "jag vill ha", "projekt", "sajt", "app",
  "verktyg", "system", "webbplats", "landing page", "build", "create",
  "I want", "make me", or any description of something to be realized.

  Also triggers when the user provides a project description and expects
  a structured output that an agent can execute autonomously.

  This skill does NOT execute the build itself. It produces the workspace
  that another agent session (or the same agent) then executes via RUN.md.
---

# Buildr Operator

## What This Skill Does

Takes a human idea → produces a folder → any agent builds it autonomously.

The folder contains everything: constraints, design system, module specs,
quality gates, fabricated memories, relevant tools, a builder role, an
evaluator role, and a step-by-step runbook. No conversation history needed.
No re-explanation needed.

## The Pipeline

```
User says "I want X"
    ↓
Phase 1: ONBOARDING (extract what, who, how, feel)
    ↓
Phase 2: DERIVE (technical decisions — never asked, always inferred)
    ↓
Phase 3: SELECT (pick Vault items relevant to this project)
    ↓
Phase 4: GENERATE (produce the complete workspace folder)
    ↓
Phase 5: VERIFY (confirm workspace is self-contained and executable)
```

## Two entry paths (legacy vs advanced / v2)

| Path | When | Workspace generation |
|------|------|----------------------|
| **Legacy / basic** | User invokes this skill directly with no prior preflight | Run Phases 1–5 from scratch as below. |
| **Advanced (v2)** | User runs **Buildr Advanced Operator** (`v2/prompts/buildr-advanced-operator.md`) | **Mandatory:** preflight must complete first via `buildr-workspace-architect`. Do **not** redefine approved purpose, CRI, acceptance, or architecture decisions. Ingest staging under `v2/.buildr/preflight/<project-slug>/` per **`references/preflight-ingest.md`**. |

**Before generating** in the advanced path, binary gate (when artifacts exist): run  
`python -m engines.preflight_validate <staging-dir>` — exit code `0` required.  
Overview: **`docs/v2-overview.md`**. Vault routine: **`vault/routines/preflight-gate-check.md`**.

## Phase 1: Onboarding

Ask human questions. Never technical questions. Maximum 8 questions total.
Adapt based on how much the initial description already reveals.

### Required Information (gather through conversation, not a form)

| Dimension | What to learn | Example answer |
|-----------|--------------|----------------|
| **What** | Project type, core function | "A booking site for fishing trips" |
| **Who** | Target users, their context | "Tourists visiting Zanzibar" |
| **Feel** | Emotional quality | "Professional but inviting" |
| **Color** | Visual direction | "Blue-ish, ocean vibes" |
| **Scope** | Must-haves vs nice-to-haves | "Booking calendar, payment, WhatsApp" |
| **Context** | Location, language, device | "Zanzibar, English + Swahili, mobile" |

### Derivation Rules (NEVER ask, ALWAYS derive)

| Signal | Derivation |
|--------|-----------|
| "booking", "boka", "reservation" | category=booking, needs calendar, needs confirmation flow |
| "sälj", "shop", "products" | category=e-commerce, needs cart, needs checkout |
| "login", "dashboard", "konto" | category=web-app, needs auth, needs user state |
| Location in Africa/Middle East | Add WhatsApp module, mobile-first, light assets |
| Location in Sweden | Consider Swish payment, Swedish default language |
| "betala", "pay", "online" | Add payment module, derive payment provider from location |
| Multiple languages mentioned | Add i18n module |
| Any category with public pages | Add SEO module |

### Category Classification

Classify into exactly one:
`website` | `booking` | `e-commerce` | `web-app` | `saas` | `tool` | `api`

If ambiguous, ask ONE clarifying question. Not two.

## Phase 2: Derive Technical Decisions

Using the onboarding answers, derive (do not ask):

1. **Tech stack** — booking/e-commerce/web-app/saas → Next.js. Simple website → static HTML or Astro. Tool → Python.
2. **Modules** — See `references/category-modules.md` for the complete mapping.
3. **Design system** — Feeling → palette, typography, component style. See `references/design-derivation.md`.
4. **Integrations** — Payment provider, WhatsApp, email, calendar — derived from scope + location.
5. **Device strategy** — Tourist audience or African location → mobile-first. B2B SaaS → desktop-first.

## Phase 3: Select Vault Items

For each module in the project, select relevant items from The Vault.

### Selection Logic

```
For each wave/module:
  1. Read the module's intent (what it builds)
  2. Select skills from vault/skills/ that match the intent
  3. Select constraints from vault/constraints/ that apply to this tier
  4. Select routines from vault/routines/ for QA
  5. Select memory templates from vault/memories/ for Imperfektum
```

### Tier-Based Selection

| Tier | Skills | Constraints | Routines |
|------|--------|-------------|----------|
| A (architecture) | api-design, data-modeling, component-arch | All constraints | retrospective |
| B (planning) | decomposition, contract-first | code-hygiene, file-discipline | module-qa |
| C (mechanical) | Specific to task (form-validation, responsive, etc.) | code-hygiene | code-complete |

## Phase 4: Generate Workspace

Produce the complete folder. Use `forge_engine.py` + `imperfektum_engine.py` + `bridge.py` if available. If not available, generate the files directly following this structure:

### Workspace File Inventory

```
project-workspace/
├── WORKSPACE.md              ← Master overview (read first)
├── PROJECT.md                ← What to build, hard constraints
├── SYSTEM.md                 ← Design system, code standards
├── MEMORY.md                 ← Imperfektum: fabricated agent memories
├── TOOLS.md                  ← Available tools from The Index
├── AGENT.md                  ← Builder behavior protocol
├── EVALUATOR.md              ← Evaluator behavior protocol
├── RUN.md                    ← Execution entrypoint for builder + evaluator
│
├── state/
│   └── orchestration.yaml    ← Source of truth: phase, budget, decisions
│
├── waves/
│   └── 001-foundation.md     ← First wave (others generated organically)
│
├── contracts/                ← Interface contracts (created during Tier A waves)
│
├── modules/                  ← Per-module specifications
│   ├── 01-foundation.md
│   ├── 02-design-system.md
│   └── ...
│
├── qa/
│   ├── checklist.md          ← Binary QA checks per module
│   ├── acceptance.md         ← Definition of "done"
│   └── evaluations/          ← Evaluator feedback artifacts
│
├── vault-selection/          ← Vault items selected for THIS project
│   ├── skills/               ← Copied/referenced relevant skills
│   ├── constraints/          ← Copied/referenced relevant constraints
│   └── routines/             ← Copied/referenced relevant routines
│
└── spec.json                 ← Machine-readable project specification
```

### AGENT.md Reading Order

```markdown
| # | File | When |
|---|------|------|
| 0 | WORKSPACE.md | First — understand the project |
| 1 | PROJECT.md | Before starting — hard constraints |
| 2 | SYSTEM.md | Before starting — design + code standards |
| 3 | MEMORY.md | Before starting — your experience from last time |
| 4 | TOOLS.md | Reference — available tools |
| 5 | EVALUATOR.md | Understand evaluation criteria and review loop |
| 6 | RUN.md | Execute — start the orchestration loop |
```

### RUN.md Content

Use the canonical content from `templates/RUN.md`. If that template is not
available, the generated `RUN.md` must preserve the same builder/evaluator loop:

```markdown
# Run

1. Read AGENT.md for builder role, reading order, and execution gates.
2. Read EVALUATOR.md for evaluator review criteria and output expectations.
3. Read WORKSPACE.md for the file contract and project summary.
4. Read MEMORY.md for your experience with this project.
5. Read state/orchestration.yaml for current progress.
6. If onboarding_complete is false → run onboarding/prompt.md (if present).
7. Find the first wave in waves/ with status != complete.
8. Load vault items declared in that wave.
9. Builder executes the wave's steps.
10. Evaluator reviews the result and writes advisory feedback.
11. Builder addresses evaluator feedback or records why no change is needed.
12. Run QA (qa/checklist.md for this module).
13. Update state.
14. Repeat until all waves complete.
```

### Orchestration State (initial)

```yaml
version: 1
contract_version: 1
onboarding_complete: false
phase: "build"
loc_budget: 10000
loc_consumed: 0
file_touch_budget: null
project_name: "example-project"
category: "web-app"
stack: "nextjs"
last_evaluation_summary: ""
waves:
  001-foundation:
    status: "pending"
    module_order: 1
    module_id: "foundation"
    module_file: "01-foundation.md"
evaluation_mode: "advisory"
decisions: []
derivations: []
vault_selections: {}
backlog: []
```

## Phase 5: Verify

Before delivering the workspace, verify:

- [ ] CLAUDE.md exists (orchestration protocol with roles, gates, rescue detection)
- [ ] WORKSPACE.md exists and is readable by a human in 2 minutes
- [ ] PROJECT.md has hard constraints listed
- [ ] SYSTEM.md has complete design system (colors, fonts, spacing)
- [ ] MEMORY.md has vision + scars + insights + completion criteria
- [ ] EVALUATOR.md exists and describes the reviewer role clearly
- [ ] RUN.md includes quality gates and reviewer steps in the execution loop
- [ ] agents/ directory exists with agent-manifest.json and per-agent .md files
- [ ] qa/gates.md exists with 3-phase quality gates (concept → implementation → delivery)
- [ ] state/orchestration.yaml has current_wave and next_wave fields
- [ ] At least Wave 001 is defined
- [ ] QA checklist covers all modules
- [ ] A fresh agent with no prior context can start from CLAUDE.md alone

## Phase 6: Register

After workspace is verified, register it in the project registry:

```bash
bash memory-system/tools/project-registry.sh \
  --register \
  --name "[project-name]" \
  --path "[workspace-path]" \
  --category "[category]" \
  --origin "new"
```

This enables cross-session tracking, pause/resume, and multi-project management.

## Key Principles

1. **The user never sees technical decisions.** They describe what they want. The system translates.

2. **Organic over upfront.** Only Wave 1 is fully planned at generation time. Later waves are planned as the project progresses.

3. **Everything the agent needs is in files.** Zero dependence on conversation history. Full restart capability from state + files alone.

4. **Imperfektum memories are generated per-wave, not once.** Each wave gets fresh, specific memories relevant to what it's building.

5. **The Vault provides 95%. The project provides 5%.** Skills and constraints are agnostic. Only the project description, design system, and domain model are project-specific.
