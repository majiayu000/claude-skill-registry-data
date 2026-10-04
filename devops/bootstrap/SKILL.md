---
name: bootstrap
description: "Analyzes a new or existing codebase to generate project-specific rules, skills, workflows, and documentation. Triggers when onboarding to a project, scanning a codebase, setting up a new project, or when the user says 'onboard' or 'analyze this project'."
---

# Bootstrap Skill

## Goal

Transform any project — new or existing — into a fully configured Ground Zero workspace by scanning, analyzing, and generating project-specific configuration.

## Instructions

### Determine Project Type

First, check if the project has existing code:
- If the workspace contains only `.agent/`, `GEMINI.md`, `docs/`, and `README.md` → this is a **NEW project**
- If the workspace contains other source files, config files, or directories → this is an **EXISTING project**

### For NEW Projects

1. **Ask the orchestrator** what they want to build. Ask about:
   - What is the project? (one sentence description)
   - What platform? (web app, mobile app, API, CLI tool, etc.)
   - Any technology preferences? (or should you recommend?)
   - Any constraints? (budget, timeline, must-use services)

2. **Recommend a tech stack** based on the answers. Explain each choice in plain English. Create an ADR for the tech stack decision.

3. **Generate project-specific files**:
   - A rule file in `.agent/rules/` for the chosen code style
   - A rule file for the chosen architecture conventions
   - Skills for: build, test, run/serve, lint (based on the tech stack)
   - Update `.agent/knowledge/tech-stack.md`
   - Update `.agent/knowledge/project-map.md` with the planned structure
   - Add framework-specific terms to `.agent/knowledge/glossary.md`
   - Log all generated items to `.agent/knowledge/evolution-log.md`

4. **Report to orchestrator**: Plain-English summary of everything generated and why.

### For EXISTING Projects

1. **Scan the directory tree** — list all directories and file types present

2. **Detect the tech stack** — read the checklist in `resources/scan-checklist.md` and the signatures in `resources/tech-stack-signatures.md`. Look for:
   - Package manager files (package.json, requirements.txt, Cargo.toml, go.mod, etc.)
   - Framework config files (next.config.js, vite.config.ts, django settings, etc.)
   - CI/CD files (.github/workflows/, Dockerfile, etc.)
   - Test configuration (jest.config, pytest.ini, etc.)

3. **Sample code files** — read 10-15 representative source files to detect:
   - Coding style (tabs/spaces, naming conventions, semicolons, quotes)
   - Architecture patterns (MVC, component-based, microservices, etc.)
   - Common patterns (error handling style, logging, validation approach)
   - Test patterns (test file naming, assertion style)

4. **Read existing documentation** — README, CONTRIBUTING, any docs/ folder

5. **Generate project-specific files**:
   - Rules matching the detected code style
   - Rules matching the detected architecture conventions
   - Skills for detected build/test/lint/deploy commands
   - Update `.agent/knowledge/tech-stack.md` with detected technologies
   - Update `.agent/knowledge/project-map.md` with directory descriptions
   - Add project-specific terms to `.agent/knowledge/glossary.md`
   - Log all generated items to `.agent/knowledge/evolution-log.md`

6. **Report to orchestrator**: Plain-English summary of what was found and what was generated.

## Constraints

- Never modify existing source code during bootstrap — only create `.agent/` configuration files
- Always ask the orchestrator for approval before generating rules or skills
- If the codebase is very large (>500 files), do a representative sample rather than reading everything
- State your confidence level in detected patterns ("I am 90% sure this uses React because...")
