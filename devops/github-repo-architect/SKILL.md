---
name: github-repo-architect
description: Convert a repository idea into a complete GitHub repository architecture. Always trigger immediately when the user's message starts with "repo", "gra", or "architect repo". Also trigger on "build a repo structure", "design a GitHub repo", "scaffold this repository", "create repository architecture", "turn this idea into a repo", or any request to generate README, folder layout, prompts, GitHub Actions CI, issue templates, pull request templates, or starter project structure for a new repository.
---

# GitHub Repo Architect Skill

## Intent

Turn rough software ideas into practical GitHub repository structures with files, workflows, prompts, and setup direction.

## Workflow

1. Identify the exact task and available source material.
2. Apply the domain rules and output format in this skill.
3. State assumptions, uncertainty, and missing inputs clearly.
4. Return the requested artifact, recommendation, or review in a practical format.
5. Check the result against the validation checklist before finishing.

## Constraints

- Do not fabricate missing facts, measurements, dates, sources, or user context.
- Keep output aligned with Mick's direct, practical communication style unless the skill says otherwise.
- Preserve safety, legal, medical, financial, and operational boundaries stated in this file.
- Prefer concise, usable output over broad explanation.

Turn a rough project idea into a complete GitHub repository plan that can be implemented directly. Produce the repository structure, README, prompts, CI pipeline, and starter files that fit the project.

## Primary Triggers

**`repo`**, **`gra`**, or **`architect repo`** — Provide the idea after the trigger and generate the repository architecture immediately.

Other triggers: "build a repo structure", "design a GitHub repo", "scaffold this repository", "create repository architecture", "turn this idea into a repo"

```text
repo [project idea, target language, or rough requirements]
gra [GitHub repo concept]
architect repo [existing notes or spec]
```

## Do Not Use When

- The user wants to improve an **existing repo** that already has structure — use a code review or audit approach instead.
- The user only needs a **README written** for a known repo layout — use the `github-readme` skill instead.
- The user has **no project idea** and wants a generic starter template with no specifics — ask for a concrete idea before proceeding.
- The request is for **a private or sensitive system** (internal corporate infra, credential vaults, personal data stores) and no security context has been provided — gather security requirements first.

## Step 1 — Identify Project Type

Classify the idea before writing files. Choose the closest type and adapt the output.

| Type | Examples | Architecture Focus |
|---|---|---|
| Claude or Codex skill | Content writer, repo architect, automation helper | `skill.md`, README, packaging notes, examples |
| CLI tool | PowerShell module, Python utility, Node script | commands, config, tests, release workflow |
| API service | FastAPI, Express, Flask, webhook receiver | routes, auth, OpenAPI, tests, deploy path |
| Web app | React, Next.js, static dashboard | app structure, components, env vars, build workflow |
| MCP server | Home Assistant MCP, Pi-hole MCP | tool definitions, server entrypoint, config, tests |
| Automation repo | Playwright scraper, scheduled task, n8n helper | workflows, secrets, logs, retries, docs |
| Data project | ETL, analysis notebook, report generator | datasets, schemas, reproducibility, outputs |
| Infrastructure repo | Docker, Proxmox, Terraform, Ansible | inventory, variables, validation, rollback notes |

If the type is unclear, pick the safest minimal architecture and state the assumption in one line.

## Step 2 — Extract Requirements

Pull these details from the user's message:

- Repo name or working title
- Goal and target user
- Language or framework
- Runtime environment
- Inputs and outputs
- External services, APIs, secrets, or credentials
- Required commands
- Deployment target
- Test expectations
- License preference

If a key detail is missing, make a practical assumption. Ask a question only when the missing detail changes the whole architecture.

## Step 3 — Generate The Repository Blueprint

Return a complete blueprint in this order:

1. **Repository name**
2. **One sentence purpose**
3. **Assumptions**
4. **Folder layout**
5. **Generated files**
6. **README.md**
7. **Development prompts**
8. **GitHub Actions CI**
9. **Setup commands**
10. **Next implementation tasks**

For code or automation repos, include starter file contents when the user asks for a scaffold or when the idea is specific enough to generate useful files. For broad planning requests, provide filenames and concise descriptions instead of long boilerplate.

## Stack Scaffolding Presets

For Mick's common stacks, start from these opinionated presets instead of deriving the layout from scratch:

- **PowerShell-first automation repo**: `src/` module folder with one `.psm1` plus a `.psd1` manifest, `scripts/` for entry points, `Tests/` with Pester, `PSScriptAnalyzerSettings.psd1` at root, CI running ScriptAnalyzer then Pester on `pwsh`
- **Python CLI**: `pyproject.toml` with a console entry point, `src/<package>/` layout, `tests/` with pytest, `ruff` for lint, no setup.py
- **Hybrid PowerShell and Python repo**: split by language at the top level like the Trading repo, shared `docs/` and `Tests/`, CI with one job per stack so a failure points at the right half
- **Static site**: content separated from layout, local preview command documented, deploy workflow only when the host is known

## Repo Documentation Plan

Plan which planning docs are tracked versus local-only, following the pattern Mick's repos already use:

- tracked: `README.md`, `changelog.md`, completed-work logs, specs
- local-only (gitignored): future-upgrade backlogs, scratch assessments, personal notes
- name the gitignore entries explicitly in the blueprint so local planning files never land in commits

## Folder Layout Rules

Use an annotated tree. Keep the structure lean and useful.

```text
RepoName/
|-- README.md                  # Project overview and usage
|-- .github/
|   |-- workflows/
|   |   |-- ci.yml             # Test and lint workflow
|   |-- ISSUE_TEMPLATE/
|   |   |-- bug_report.md      # Bug report template
|   |   |-- feature_request.md # Feature request template
|   |-- pull_request_template.md
|-- src/                       # Main source code
|-- tests/                     # Automated tests
|-- docs/                      # Architecture and usage notes
```

Adapt folders to the project. Do not add empty complexity. Avoid including Docker, Terraform, or release automation unless the project calls for it.

## README Requirements

Generate a complete README tailored to the repo. Include only sections that fit.

Core sections:

- `# [Repo Name]`
- One sentence description
- `## Overview`
- `## What This Does`
- `## Repository Structure`
- `## Prerequisites`
- `## Setup`
- `## Usage`
- `## Testing`
- `## Configuration`
- `## Security Notes`
- `## License`

Use tables for structured configuration, commands, modules, or environment variables.

## Development Prompts

Include prompts that help the user continue building the repo with Claude or Codex.

Prompt set:

- **Implementation prompt** — build the first working version from the scaffold
- **Test prompt** — add or improve automated tests
- **Review prompt** — inspect for bugs, missing docs, and security issues
- **Release prompt** — prepare tags, changelog, and release notes when relevant

Prompts must be specific to the generated repository. Do not write generic prompts that could apply to any project.

## GitHub Actions CI

Generate `.github/workflows/ci.yml` for the chosen stack.

Minimum workflow:

- Runs on pull requests and pushes to the default branch
- Checks out the repo
- Sets up the language runtime
- Installs dependencies
- Runs linting when a lint command exists
- Runs tests

Use conservative defaults:

| Stack | CI Defaults |
|---|---|
| Python | `actions/setup-python`, install from `requirements.txt` or `pyproject.toml`, run `pytest` |
| Node | `actions/setup-node`, `npm ci`, `npm test`, `npm run lint` if present |
| PowerShell | `pwsh`, `Invoke-ScriptAnalyzer` if configured, Pester tests |
| .NET | `actions/setup-dotnet`, `dotnet restore`, `dotnet test` |
| Docker | `docker build` and optional compose validation |
| Claude skill | package validation, archive creation, markdown checks |

If no stack is clear, create a placeholder CI with markdown checks and TODO comments.

Be opinionated enough to implement directly: name the exact test framework, the lint tool and its config file, and the first three tests worth writing for this specific repo. "Add tests" is not a recommendation; "add Pester tests covering the auth module's token refresh, error path, and config fallback" is.

## Issue And PR Templates

Include templates when generating a full repo scaffold.

Bug report fields:

- Problem
- Steps to reproduce
- Expected result
- Actual result
- Environment

Feature request fields:

- Use case
- Proposed behavior
- Inputs
- Outputs
- Notes

Pull request template fields:

- Summary
- Changes
- Tests
- Risk
- Checklist

## Voice And Formatting Rules

Apply Mick's repository voice to human facing prose:

- No emojis
- No motivational sign offs
- No AI sounding language: "journey", "transformative", "game-changer", "leverage", "showcase", "utilize", "diving deep", "I'm excited to share", "The takeaway here is..."
- First person only when the repository is personal or intentionally written from Mick's perspective
- Direct, conversational, short sentences
- Lead with concrete details
- Use exact commands and file paths

Technical syntax is allowed to use hyphens, quotation marks, YAML punctuation, package names, flags, and filenames when required.

## Output Guardrails

- Do not produce a generic template when project details are available.
- Do not invent secrets, API keys, URLs, or package names.
- Mark uncertain commands as assumptions.
- Keep generated CI runnable for the selected stack.
- Include security notes for any repo that handles secrets, credentials, personal data, trading data, scraping, or automation against logged in services.
- Keep the initial architecture small enough for one person to build.

## Validation Checklist

Run these checks before delivering any generated blueprint:

- Generated folder tree matches the stated project type from the type table.
- README includes all required sections for the project — no placeholder headings with no content.
- CI workflow targets the correct runtime and includes a working test or lint step, not just a checkout.
- Development prompts reference actual files and folder names from the generated repo, not generic placeholders.
- Security notes are present whenever the project involves API keys, credentials, personal data, scraping, or automation against authenticated services.
- No invented package names, service URLs, or environment variable values appear in generated files.
- Setup commands are runnable as written for the stated language and OS.
- Architecture fits one person building from scratch — no unnecessary layers, services, or abstractions.
- If type was unclear and an assumption was made, that assumption is stated in the output.

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- The project idea, target stack, and any must-have repo components.

Example prompts:

- `Use github-repo-architect to turn this project idea into a complete repo layout with docs and workflows.`
- `Design the structure for a PowerShell and Python automation repo with clear module boundaries.`
- `Show me how to ask this skill for a repository architecture plan with folders and starter files.`

