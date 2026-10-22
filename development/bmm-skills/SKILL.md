---
name: bmm-skills
description: >-
  Routes requests to the BMad Method (v6.12.4) agile framework: persona agents, planning skills (brief,
  PRFAQ, PRD, UX, spec, architecture, epics, sprint planning), shipping skills (build, code review,
  walkthrough, QA tests, retrospective), and core helpers (brainstorming, research, review, party mode).
  Use when the user mentions BMad or BMM, names a BMad agent such as Mary, John, Sally, Winston, or
  Amelia, or wants a structured flow from idea through PRD and architecture to built, reviewed code.
version: "6.12.4"
license: MIT
source: "https://github.com/bmad-code-org/BMAD-METHOD"
attribution: "bmad-code-org/BMAD-METHOD by BMad Code, LLC"
---

> **Attribution:** The skills in this folder are sourced from [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) v6.12.4 by [BMad Code, LLC](https://github.com/bmad-code-org), licensed MIT. BMad and BMad Method are trademarks of BMad Code, LLC; this collection is not affiliated with or endorsed by it. This router was written for this collection.

# BMad Method router

This file holds no workflow logic. It routes a request to the one sub-skill that handles it. The folder
mirrors upstream's layout:

```
agents/   persona agents (Mary, John, Sally, Winston, Amelia)
plan/     brief, PRFAQ, PRD, UX, spec, architecture, epics and stories, sprint planning, project context
ship/     build, unattended build loop, code review, walkthrough, QA tests, correct course, retrospective
core/     brainstorming, idea forging, research, review lenses, elicitation, party mode, help, customize
```

`module.yaml` (method) and `core/module.yaml` hold the shared settings and the agent roster.
`module-help.csv` and `core/module-help.csv` list every skill with its menu code, phase, and what
usually comes before and after it.

## Before first use

The sub-skills call helper scripts that the BMad installer puts in the project:
`{project-root}/_bmad/scripts/` (`render_skill.py`, `resolve_customization.py`, `resolve_config.py`,
`memlog.py`), run with [`uv`](https://docs.astral.sh/uv/) and Python 3.11 or later. Set a project up once with:

```bash
npx bmad-method install
```

Most skills fall back to their own `customize.toml` defaults when a script is missing. `bmad-build` and
`bmad-build-auto` do not: they stop and report the error. If `_bmad/` is absent and the user wants Build,
tell them to run the installer first.

## Routing

1. **The user names an agent?** Load that persona skill and let it take over.
2. **The user names an artifact or action?** Match it in the tables below.
3. **Unsure where to start, or asks what to do next?** Load `core/bmad-help/SKILL.md`; it reads the
   project state and recommends the next skill.
4. **Just a code change?** `ship/bmad-build/SKILL.md` is the standard implementation flow at any size.

Read only the sub-skill that matches. Each one resolves its own customization when it starts.

### Agents

| Agent | Role | Skill |
|---|---|---|
| Mary 📊 | Business analyst: market research, competitive analysis, requirements | `agents/bmad-agent-analyst/SKILL.md` |
| John 📋 | Product manager: PRDs and requirements discovery | `agents/bmad-agent-pm/SKILL.md` |
| Sally 🎨 | UX designer and UI specialist | `agents/bmad-agent-ux-designer/SKILL.md` |
| Winston 🏗️ | System architect: technical design | `agents/bmad-agent-architect/SKILL.md` |
| Amelia 💻 | Senior engineer: implements stories and code changes | `agents/bmad-agent-dev/SKILL.md` |

### Plan

| Request | Skill |
|---|---|
| Capture a product idea in a brief | `plan/bmad-product-brief/SKILL.md` |
| Stress-test a concept with Working Backwards (press release plus FAQ) | `plan/bmad-prfaq/SKILL.md` |
| Create, update, or validate a PRD | `plan/bmad-prd/SKILL.md` |
| Condense any input into a short SPEC.md, or split a spec into stories | `plan/bmad-spec/SKILL.md` |
| UX design: DESIGN.md and EXPERIENCE.md | `plan/bmad-ux/SKILL.md` |
| Architecture decisions document | `plan/bmad-architecture/SKILL.md` |
| Break requirements into epics and stories | `plan/bmad-create-epics-and-stories/SKILL.md` |
| Readiness check and sprint status file; sprint progress summary | `plan/bmad-sprint-planning/SKILL.md` |
| Set up or refresh the repo's AGENTS.md block for agents | `plan/bmad-project-context/SKILL.md` |

### Ship

| Request | Skill |
|---|---|
| Implement a feature, story, bug fix, or change | `ship/bmad-build/SKILL.md` |
| One iteration of an unattended build loop (only when invoked by name) | `ship/bmad-build-auto/SKILL.md` |
| Review code changes with parallel reviewers | `ship/bmad-code-review/SKILL.md` |
| Walk a human reviewer through a change | `ship/bmad-walkthrough/SKILL.md` |
| Generate API and end-to-end tests for built features | `ship/bmad-qa-generate-e2e-tests/SKILL.md` |
| Assess a significant mid-sprint change | `ship/bmad-correct-course/SKILL.md` |
| Retrospective on a finished epic | `ship/bmad-retrospective/SKILL.md` |

### Core

| Request | Skill |
|---|---|
| Brainstorm or ideate | `core/bmad-brainstorming/SKILL.md` |
| Test a half-formed idea through probing personas | `core/bmad-forge-idea/SKILL.md` |
| Research to support a decision (market, domain, technical) | `core/bmad-deep-recon/SKILL.md` |
| Review a diff, PR, or document with review lenses | `core/bmad-review/SKILL.md` |
| Push a draft further (pre-mortem, first principles, red team) | `core/bmad-advanced-elicitation/SKILL.md` |
| Several agents discuss a topic together | `core/bmad-party-mode/SKILL.md` |
| What to do next, or questions about BMad | `core/bmad-help/SKILL.md` |
| Change how an installed BMad skill behaves | `core/bmad-customize/SKILL.md` |

## Usual chain

brief or PRFAQ → PRD (plus UX when there is a UI) → architecture → epics and stories → sprint planning
→ build → code review → retrospective. A spec can stand in for the brief and PRD on small work. Run
correct course when a change mid-sprint invalidates the plan.

## Names from earlier v6 releases

Older BMad guides use names that upstream has since merged or retired. Route them like this:

| Old name | Now |
|---|---|
| `bmad-quick-dev`, `bmad-create-story`, `bmad-dev-story` | `ship/bmad-build` |
| `bmad-dev-auto` | `ship/bmad-build-auto` |
| `bmad-create-prd`, `bmad-edit-prd`, `bmad-validate-prd` | `plan/bmad-prd` |
| `bmad-create-architecture` | `plan/bmad-architecture` |
| `bmad-create-ux-design` | `plan/bmad-ux` |
| `bmad-check-implementation-readiness`, `bmad-sprint-status` | `plan/bmad-sprint-planning` |
| `bmad-checkpoint-preview` | `ship/bmad-walkthrough` |
| `bmad-domain-research`, `bmad-market-research`, `bmad-technical-research` | `core/bmad-deep-recon` |
| `bmad-document-project`, `bmad-generate-project-context` | `plan/bmad-project-context` |
| `bmad-agent-tech-writer` (Paige) | retired upstream with no replacement yet; `core/bmad-review` covers editorial review |
