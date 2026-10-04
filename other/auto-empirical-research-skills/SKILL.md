---
name: auto-empirical-research-skills
description: Route empirical-research requests through the Auto-Empirical Research Skills catalog when this whole repository is installed as one skill in Codex, CodeBuddy, Claude Code, or another IDE. Use to choose and load the right vendored AERS skill for causal inference, econometrics, replication, manuscript writing, citation checking, de-AIGC editing, or full empirical-paper workflows without reading the entire repository at once.
---

# Auto-Empirical Research Skills Router

Use this root skill when the full AERS repository has been installed as a single skill folder. Treat it as a router and catalog, not as a request to load every vendored `SKILL.md`.

## Workflow

1. Classify the user's empirical-research task by stage:
   - Full pipeline or orchestration: start with `skills/69-Paper-WorkFlow/` or the `skills/00.*` flagship analysis skills.
   - Causal inference and econometrics: search `catalog/skills.json` or `docs/TAXONOMY.md` for DID, IV, RD, SCM, DML, panel FE, matching, survival, Bayesian, or Stata/R/Python terms.
   - AER or top economics journal work: start with `skills/50-brycewang-aer-skills/`.
   - Replication, citation, or peer review: use `docs/SKILL_CATALOG.md` and `docs/GOLDEN_WORKFLOWS.md` to choose a focused skill.
   - Chinese academic de-AIGC or academic rewriting: start with `skills/48-copaper-ai-chinese-de-aigc/` or nearby writing skills in the catalog.
2. Read only the selected child skill's `SKILL.md`, then follow its progressive-disclosure instructions for `references/`, `scripts/`, `assets/`, or templates.
3. If no child skill clearly matches, inspect `catalog/skills.json` first, then `docs/SKILL_CATALOG.md`. Avoid broad recursive reads of `skills/`.
4. For installation help, use `docs/INSTALL.md` for Codex-style copy installs and `INSTALL.md` for Claude Code marketplace/plugin installs.
5. If editing this repository, keep parent and nested repos separate. In particular, inspect `git status` inside `skills/69-Paper-WorkFlow/` before touching it.

## Install Notes

- Whole-repo imports are supported by this root `SKILL.md` as a lightweight compatibility entry point.
- Individual skill installs are still preferred when a runtime expects one folder per skill. Copy the folder that directly contains the target `SKILL.md`.
- Do not copy the repository root into a runtime and expect every child skill to become individually registered unless that runtime explicitly supports recursive skill discovery.

## Key Files

- `catalog/skills.json`: machine-readable list of vendored skills.
- `docs/SKILL_CATALOG.md`: human-readable skill index.
- `docs/TAXONOMY.md`: task and method taxonomy.
- `docs/GOLDEN_WORKFLOWS.md`: ready-to-use empirical-research prompts.
- `docs/INSTALL.md`: runtime installation guidance for single-skill and whole-repo use.
