---
name: agent-directory
description: Discover and invoke specialist agent personas from the shared agent library. Use before delegating any specialised task to check if a domain expert persona exists.
when_to_use: Before delegating specialised work, check if a domain expert exists in the agent library
user-invocable: true
argument-hint: "[search-term]"
---

# Agent Directory

You have access to a library of 69+ specialist agent personas at `~/.config/opencode/agent/` (shared with OpenCode). Each `.md` file defines a domain expert with specific skills, identity, and methodology.

## How to Discover Available Agents

List all available specialists:

```bash
ls ~/.config/opencode/agent/
```

To find an agent's name and capabilities, read the first 10 lines (frontmatter has name + description):

```bash
head -10 ~/.config/opencode/agent/<filename>.md
```

## How to Use a Specialist Persona

Once you find a relevant specialist, read their full `.md` file and adopt their expertise, methodology, and critical rules for the current task. Use the Agent tool to delegate work with the specialist's instructions as context:

```
Agent(
  description="<brief task>",
  prompt="You are adopting the following specialist persona:\n\n<contents of agent .md file>\n\nTask: <specific work to do>"
)
```

For simpler tasks, just load the specialist's rules and methodology into your own approach.

## When to Use a Specialist vs Generic Approach

| Situation | Use |
|---|---|
| A specialist's description closely matches your task | Load that specialist's persona |
| No specialist fits | Proceed with general-purpose approach |
| Multiple specialists relevant | Load the primary one, reference others |

**Rule**: Always scan the agent directory before defaulting to a generic approach. A specialist has domain-specific rules and methodology that improve output quality.

## Key Specialists

- `Senior Developer` — Full-stack implementation, Laravel/Livewire/FluxUI
- `Backend Architect` — Scalable system design, database, APIs, cloud
- `Frontend Developer` — Frontend components, UX, modern CSS
- `DevOps Automator` — CI/CD, infrastructure automation, cloud deployments
- `Security Engineer` — Security reviews, vulnerability analysis, compliance
- `Data Engineer` — Data pipelines, ETL, analytics infrastructure
- `Technical Writer` — Documentation, API docs, technical prose
- `Code Reviewer` — Multi-language PR reviews, GitHub integration
- `Infrastructure Maintainer` — Cloud infra, Kubernetes, IaC
- `Performance Benchmarker` — Performance profiling and optimisation
- `UI Designer` / `UX Architect` / `UX Researcher` — Design and UX work

For the full list of 69 agents, run `ls ~/.config/opencode/agent/`.

## Arguments

If `$ARGUMENTS` is provided, search for matching agents:

```bash
ls ~/.config/opencode/agent/ | grep -i "$ARGUMENTS"
```

Then read matching agent files and present their capabilities.
