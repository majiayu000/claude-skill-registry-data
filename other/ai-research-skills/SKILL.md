---
name: ai-research-skills
description: "AI research: ideas, ML papers, plots, presentations, artifacts and scoped experiments; 10 cloud modules, 98 in full local source. TR: AI araştır, araştırma fikri, ML makalesi, deney planla."
license: MIT
---

# AI Research Skills Library

Upstream [orchestra-research/AI-research-SKILLs](https://github.com/orchestra-research/AI-research-SKILLs) (MIT, 773a529 2026-06-15) — chat subset (ideation, paper writing, research artifacts, autoresearch); the full 98-skill library is installed locally in Codex, Claude Code and OpenCode. Upstream technical resources are retained; controlling instructions in autoresearch and research-manager have documented authorization/privacy adaptations; paths inside a module are relative to that module's folder.

## Execution protocol

Read [research execution and data boundaries](yigit/execution-protocol.md) before any module. Existing host permissions and task-specific authorization apply to every technical example.

## How to use

- Starting or steering an AI/ML research project end to end → `autoresearch` module; it routes to the domain modules below.
- Open one of the ten bundled modules for its supported deliverable. Framework training, serving and RAG modules belong to the full local library; report that boundary and use available official documentation without claiming those files are bundled.
- Research or thesis ideas in any field → `brainstorming-research-ideas`, then `creative-thinking-for-research`; translate CS/ML examples to the user's field.
- Install the Python packages a module lists only when the task needs them; ask before installing GPU, cloud or paid tooling.

## Modules by category

### 0-autoresearch-skill

- [`autoresearch`](modules/autoresearch/MODULE.md) — Orchestrates end-to-end autonomous AI research projects using a two-loop architecture.

### 20-ml-paper-writing

- [`academic-plotting`](modules/academic-plotting/MODULE.md) — Generates publication-quality figures for ML papers from research context.
- [`ml-paper-writing`](modules/ml-paper-writing/MODULE.md) — Write publication-ready ML/AI papers for NeurIPS, ICML, ICLR, ACL, AAAI, COLM.
- [`presenting-conference-talks`](modules/presenting-conference-talks/MODULE.md) — Generates conference presentation slides (Beamer LaTeX PDF and editable PPTX) from a compiled paper with speaker notes and talk script.
- [`systems-paper-writing`](modules/systems-paper-writing/MODULE.md) — Comprehensive guide for writing systems papers targeting OSDI, SOSP, ASPLOS, NSDI, and EuroSys.

### 21-research-ideation

- [`brainstorming-research-ideas`](modules/brainstorming-research-ideas/MODULE.md) — Guides researchers through structured ideation frameworks to discover high-impact research directions.
- [`creative-thinking-for-research`](modules/creative-thinking-for-research/MODULE.md) — Applies cognitive science frameworks for creative thinking to CS and AI research ideation.

### 22-agent-native-research-artifact

- [`compiler`](modules/compiler/MODULE.md) — Compiles any research input — PDF papers, GitHub repositories, experiment logs, code directories, or raw notes — into a complete Agent-Nati…
- [`research-manager`](modules/research-manager/MODULE.md) — Records research provenance as a post-task epilogue, scanning conversation history at the end of a coding or research session to extract de…
- [`rigor-reviewer`](modules/rigor-reviewer/MODULE.md) — Performs ARA Seal Level 2 semantic epistemic review on Agent-Native Research Artifacts, scoring six dimensions (evidence relevance, falsifi…
