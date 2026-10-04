---
name: skill-synthesis
description: Compose multiple installed skills into one coordinated execution stack with ordered packets, minimal context load, and deterministic handoff artifacts. Use when tasks span multiple domains (for example HYDRA + browser + training + deploy) and you need a single combined workflow instead of invoking skills one-by-one.
---

# Skill Synthesis

## Overview
Use this skill to fuse multiple installed skills into one execution loop with clear ordering, packet boundaries, and artifacts.

This skill is also the preferred bridge when work spans:
- repo code and canonical docs
- Notion exports and live Notion pages
- Obsidian vault notes
- local research/foundation texts

It should treat those sources as layered evidence, not one flat corpus.

## Quick Start

1. Build a stack from a task prompt.
```powershell
python C:\Users\issda\.codex\skills\skill-synthesis\scripts\compose_skill_stack.py --task "Build gamma funnels and deploy" --top 8
```

2. Run the resulting packets in order from highest leverage to lowest risk.

## Workflow

### 1) Select Minimal Stack
- Pick one **primary** skill (owns outcome).
- Pick up to five **support** skills (execution lanes).
- Do not load the whole skill catalog unless explicitly requested.
- If the task spans repo + Notion + Obsidian + local notes, prefer a foundation map pass before implementation.

### 2) Build Ordered Packets
- Packet A: foundation-source scan
- Packet B: canonicality split (`canonical`, `operational`, `exploratory`, `evidence`, `historical`)
- Packet C: implementation/modeling
- Packet D: validation/smoke
- Packet E: publish/deploy
- Packet F: evidence + vault notes

### 3) Turing / Local-Rule Conversion Rule
When a task sounds infinite, metaphor-heavy, or underdefined, convert it into a finite engineering packet instead of debating abstractions.

Required conversion fields:
- state space
- initial state
- local update rule
- monitored quantity
- validation harness
- lane tag: `facts`, `tested-results`, or `theories-untested`

Use this for theory-to-runtime bridges such as ternary governance, phi-lifts, Turing-tape style local rules, or manifold overlays.

### 4) Execute with Context Discipline
- Keep live context to only the active packet.
- Move long notes to artifacts or vault docs.
- Keep source links and proofs in packet output.
- When foundation texts disagree, code-first canonical surfaces win unless the task is explicitly archival or patent-history oriented.

### 5) Output Contract
- stack plan JSON
- ordered packet list
- execution report (what ran, what passed, what is blocked)
- evidence paths for each packet

## Built-in Stack Profiles

### `hydra-library-wing`
- `hydra-clawbot-synthesis`
- `aetherbrowser-arxiv-nav`
- `aetherbrowser-github-nav`
- `hugging-face-model-trainer`
- `notion`

Use for deep research + dataset handoff + multi-agent synthesis.

### `revenue-gamma-funnel`
- `living-codex-browser-builder`
- `article-posting-ops`
- `scbe-shopify-money-flow`
- `aetherbrowser-shopify-nav`
- `vercel-deploy`

Use for landing pages, conversion flow, and web deployment.

### `platform-release`
- `development-flow-loop`
- `playwright`
- `scbe-connector-health-check`
- `vercel-deploy`

Use for implementation -> smoke -> deploy.

### `foundation-magma-map`
- `scbe-codebase-orienter`
- `obsidian-vault-ops`
- `notion-research-documentation`
- `scbe-system-engine`
- `agent-handoff-packager`

Use for turning repo docs, Notion exports, Obsidian, and local research texts into one authority map.

### `ternary-turing-bridge`
- `scbe-experimental-research-safe-integration`
- `development-flow-loop`
- `scbe-context-full-test-suite`
- `obsidian-vault-ops`
- `notion-research-documentation`

Use for converting ternary / Turing / manifold theory into finite local-rule experiments, docs, and bounded validation lanes.

### `docs-funnel-evidence`
- `scbe-github-pages-funnel-builder`
- `development-flow-loop`
- `playwright`
- `obsidian-vault-ops`

Use for taking a validated system surface and turning it into a linked GitHub Pages funnel with evidence trails.

### `security-corpus-prism`
- `notion-research-documentation`
- `scbe-experimental-research-safe-integration`
- `hugging-face-datasets`
- `development-flow-loop`
- `obsidian-vault-ops`

Use for turning primary security/framework sources into structured `UM` and `DR` training packets such as framework summaries, control crosswalks, diagram packets, working-vs-broken examples, attack-to-control maps, and debate/conclusion packets.

### `github-gitlab-pond-meridian-flush`

- `scbe-gitlab-pond-integration`
- `gh-fix-ci`
- `gh-address-comments`
- `scbe-github-sweep-sorter`
- `scbe-github-systems`
- `aetherbrowser-github-nav`

Use for keeping cross-pond flows unblocked: quick pond flush, then PR/CI triage, then comment handling, then sweep routing.
## Rules
- Favor official docs and primary sources for unstable facts.
- Keep stack size small unless user explicitly asks for full-spectrum mode.
- Prefer deterministic scripts and repeatable packets over ad-hoc chat instructions.
- Record evidence paths for every packet.
- Treat foundation mapping as a first-class packet, not a side note, when system ontology is in question.

## Resources

### scripts/
- `compose_skill_stack.py`: Generate ranked skill stacks and packet plans from a task description.

### references/
- `stack-profiles.md`: Reusable profile templates and packet recipes.

