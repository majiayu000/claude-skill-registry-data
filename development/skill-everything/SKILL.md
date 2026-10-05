---
name: skill-everything
description: Git-versioned agent memory — agents that never make the same mistake twice.
version: 0.75.0
license: MIT
compatibility:
  opencode: ">=0.1"
  claude-code: ">=1.0"
metadata:
  source: https://github.com/sordi-ai/skill-everything
  type: router
  loads: nine sub-skills via trigger table
---

# skill-everything

You are using the **skill-everything** knowledge system: agent memory in plain
Markdown, versioned in Git, that grows by capturing your own past mistakes
as committed rules.

## Your responsibilities

1. **Before every implementation:** check the sub-skill directory below,
   load the matching skill via `skill_resource(...)`.
2. **After every mistake:** execute the self-extension workflow.
3. **When you learn something new:** add it to the appropriate category.

## Sub-skill directory

| Trigger | Sub-skill | Load via |
|---|---|---|
| writing code, refactoring, review | Code Quality | `skill_resource(skill_name="code-quality")` |
| python code, type hints, python packaging | Python | `skill_resource(skill_name="python")` |
| fastapi endpoint, pydantic model, async api | FastAPI | `skill_resource(skill_name="fastapi")` |
| langchain, lcel chain, agent framework | LangChain / Agent Framework Conventions | `skill_resource(skill_name="langchain")` |
| typescript code, strict types, async typescript | TypeScript | `skill_resource(skill_name="typescript")` |
| react component, react hooks, react performance | React | `skill_resource(skill_name="react")` |
| test-driven development, red green refactor, test first | Test-Driven Development | `skill_resource(skill_name="tdd")` |
| debugging, troubleshooting, root cause analysis, isolating bugs | Debugging | `skill_resource(skill_name="debugging")` |
| security review, vulnerability check, auth implementation | Security Review Depth | `skill_resource(skill_name="security-review")` |
| git commit, branch, pull request | Git Conventions | `skill_resource(skill_name="git-conventions")` |
| gh cli, github pr create, github issues | GitHub CLI (`gh`) Conventions | `skill_resource(skill_name="github-cli")` |
| finish branch, pre-merge checklist, branch cleanup | Closing Out a Feature Branch | `skill_resource(skill_name="branch-finishing")` |
| creating PR, deployment, review checklist | Review & Deployment | `skill_resource(skill_name="review-deployment")` |
| dockerfile, docker compose, container build | Docker / Container Conventions | `skill_resource(skill_name="docker")` |
| bash script, shell script, posix scripting | Bash / POSIX Scripting | `skill_resource(skill_name="shell-scripting")` |
| database schema, migration, table design | Database Schema Design | `skill_resource(skill_name="db-schema")` |
| svg edit, svg review, diagram, pixel review | SVG Check | `skill_resource(skill_name="svg-check")` |
| architecture diagram, mermaid diagram, drawio file | Diagrams (draw.io / Mermaid) | `skill_resource(skill_name="drawio")` |
| project-specific knowledge, business rules | Domain Knowledge (template) | `skill_resource(skill_name="domain-template")` |
| made or corrected a mistake, learn from this | Error Log | `skill_resource(skill_name="error-log")` |
| brainstorming, idea generation, divergent thinking | Brainstorming | `skill_resource(skill_name="brainstorming")` |
| implementation plan, planning before code, scope definition | Implementation Plan | `skill_resource(skill_name="implementation-plan")` |
| executing self-extension | Self-Extension Workflow | `skill_resource(skill_name="self-extension-workflow")` |

## Error capture triggers

Start the self-extension workflow when **any** of these is met:

- A test fails because of code you wrote.
- The user corrects you ("That was wrong", "Remember this").
- You realise during implementation that your first approach was wrong.
- A deployment problem occurs that your code caused.

Load the workflow:

```
skill_resource(skill_name="self-extension-workflow")
```

## Important

- **Search before write.** Before logging a new error, search the existing log for similar entries. Update instead of duplicate.
- **Action directives, not descriptions.** Always formulate rules as "Always X before Y" or "Never Z without W".
- **Stay compact.** Each sub-skill stays under 3,000 tokens. If exceeded, split.
- **PR-flow is mandatory.** Self-extension commits are opened as PRs labelled `needs-rule-review`. Never push to `main`.
- **Without `skill_resource`?** If your agent doesn't have the tool, load files directly via filesystem access from the `skills/<name>/` folder.

> This file is generated from `skills/_index.yml`. Edit the index, then run `python tools/render_loaders.py`.
