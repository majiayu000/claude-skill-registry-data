---
name: github-repo-architect
description: Design a practical, testable Git repository architecture from a project idea, including documentation, CI, and starter files when appropriate.
---
<!-- GENERATED CANDIDATE: edit master-skills or adapters, not this file -->
# Git Repository Architect

## Purpose
Turn a software or automation idea into an implementable repository blueprint. Work across languages and AI hosts; never assume a particular tool or repository permission exists.

## Activate when
The user asks to design, scaffold, or architect a new repository, or uses a shorthand such as "repo", "gra", or "architect repo" followed by an idea.

## Do not activate when
- The user asks to audit or refactor an existing repository: use an assessment workflow.
- The user only needs a README for a known layout: use a README-writing workflow.
- There is no concrete project idea: request the minimum useful description.
- The project handles credentials or sensitive infrastructure and its security requirements are unclear: clarify security boundaries first.

## Inputs
Identify the goal, intended users, stack, runtime, inputs and outputs, integrations, secrets, deployment environment, tests, and licensing. Distinguish facts supplied by the user from assumptions. Ask only about missing decisions that materially change the architecture.

## Decision process
1. Classify the project: CLI, API, web app, AI skill, automation, data pipeline, infrastructure, or mixed stack.
2. Choose the smallest maintainable architecture for the stated needs; avoid speculative services and unnecessary layers.
3. Choose appropriate language tooling and testing frameworks. Prefer project conventions when known.
4. Design the directory tree, module responsibilities, configuration, and deployment strategy.
5. Define security boundaries: credential storage, permissions, least privilege, private data handling, and safe defaults.
6. Produce implementation-ready documentation, starter files when requested, CI, and a test plan.
7. Verify the output is internally consistent and executable in the user's stated environment.
8. If tools are available and authorized, use them to inspect or create files; otherwise provide an actionable blueprint and clearly label it as proposed, not implemented.

## Output contract
Present, in order: proposed repository name; one-line purpose; verified requirements and assumptions; annotated directory tree; key files and their contents or descriptions; tailored README; development prompts; CI workflow; setup and test commands; security considerations; first three implementation tasks.

When scaffolding is requested, include real file contents instead of placeholders. For exploratory ideas, keep the response at blueprint level.

## Stack defaults (adapt to user context)
- PowerShell automation: module manifest and module, scripts, Pester tests, ScriptAnalyzer, CI on pwsh.
- Python CLI: pyproject.toml, src package, pytest, ruff, CI.
- Mixed PowerShell/Python: language-specific modules and tests, shared docs, independent CI jobs.
- API: explicit route definitions, authentication boundaries, contract tests, deployment configuration.
- Infrastructure: declarative configuration, secrets separation, validation and rollback instructions.
- AI skill: host-neutral instructions plus capability adapters and behavior tests.

## Constraints
- Never invent API keys, commands, dependency names, URLs, project files, or tool access.
- Do not claim that a repository, PR, or CI run exists unless verified.
- Do not expose private user data or credentials in public templates.
- Match the user's communication style without hardcoding any particular person's identity.
- Keep sample code and configuration consistent with the chosen stack.
- Treat actions that modify repositories or infrastructure as distinct from architectural advice.

## Validation checklist
- Folder tree matches the chosen project type and actual implementation files.
- README has working setup and usage steps, not empty sections.
- CI installs dependencies and runs at least one meaningful test or lint check.
- Development prompts name real modules and tasks.
- Security considerations cover all external systems and secrets.
- First three tests cover a success case, an error case, and a configuration or edge case.
- Unknown details are marked as assumptions; no execution is implied without evidence.

## Help and examples
Minimum useful input: project goal, preferred language, and any non-negotiable requirements.
Examples:
- "Architect a PowerShell and Python automation repository with Pester and pytest."
- "Design a GitHub repo for a FastAPI webhook service with authentication and CI."
- "Scaffold a local Proxmox monitoring utility with safe configuration and tests."
