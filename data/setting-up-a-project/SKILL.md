---
name: setting-up-a-project
description: You MUST use this skill when the user asks you to setup a claude code project. You should also suggest it if there is no CLAUDE.md or when starting work on an empty codebase.
---

# Setting up a Project

## Overview

Help Claude author a CLAUDE.md file that defines a project's purpose, development practices, and tech stack before writing code.

**Core principle:** A well-configured project prevents rework and ensures consistency. Establishing guardrails upfront helps Claude Code work reliably, produce high-quality code, and avoid doom loops where code is written, broken, and rewritten repeatedly.

## The Process

### Define the Project Purpose

Ask questions to determine:

1. **What should this project be called?** Get a name and brief description.
2. **What problem does this solve?** Understand the pain point, who experiences it, and why existing solutions are inadequate.
3. **How will it work?** Get a high-level explanation of the approach or mechanism.

Then update CLAUDE.md. Document the answers in CLAUDE.md under a `## Project Overview` section.
Here's a template:

```markdown
## Project Overview

**Setting Up a Project Skill**: Helps Claude author a CLAUDE.md file that defines a project's purpose, development practices, and tech stack before writing code.


### Problem

Claude Code often writes unreliable, inconsistent or low quality code.
It can make errors like adding two different unit testing frameworks to a project.
It can also get stuck in doom loops where code is written, broken, and rewritten repeatedly.

### Approach

A well-configured project prevents rework and ensures consistency. Establishing guardrails upfront helps Claude Code work reliably, produce high-quality code, and avoid doom loops where code is written, broken, and rewritten repeatedly.
```

## Define the Tech Stack

Ask the user about each of these areas. Suggest sensible defaults based on the language/runtime.

### Questions to Ask

1. **Language and runtime** - What programming language? What version/runtime?
2. **Deployment target** - Where will this run? (CLI, web server, serverless, container, browser, etc.)
3. **Package manager** - How will dependencies be managed?
4. **Testing framework** - What will be used for TDD?
5. **Build tools** - How will the project be built/compiled?
6. **Linting and formatting** - What tools enforce code style?
7. **Key libraries** - Any specific libraries or frameworks required?
8. **Unique concerns** - Any other technical requirements specific to this project? (e.g., database, auth, external APIs)

### Suggested Defaults

When suggesting defaults, base them on the language:

| Language | Package Manager | Testing | Linting | Build |
|----------|-----------------|---------|---------|-------|
| TypeScript/Node.js | pnpm | Vitest | ESLint + Prettier | esbuild or tsc |
| Python | uv | pytest | Ruff | - |
| Go | go modules | go test | golangci-lint | go build |
| Rust | cargo | cargo test | clippy | cargo build |

Adjust suggestions based on deployment target and project needs.

Document the output in CLAUDE.md under a `## Tech Stack` section.
Here's a template:

```markdown
## Tech Stack

- **Language**: [Language and version]
- **Runtime**: [Runtime environment]
- **Package Manager**: [Package manager]
- **Testing**: [Testing framework]
- **Linting**: [Linter and formatter]
- **Build**: [Build tool]
- **Key Libraries**: [List of essential libraries]
```

After defining the tech stack:
- confirm with the user
- write the choices to `CLAUDE.md`
- commit the file to git

## Establish Development Practices

### TDD Rules (Mandatory)

TDD is non-negotiable for all projects set up with this skill.
Read the contents of `https://raw.githubusercontent.com/britt/claude-code-skills/refs/heads/main/rules/TDD.rules.md` 
and copy it verbatim into `CLAUDE.md`. 

### Git Practices

Ask the user about their preferred git workflow, then document it in CLAUDE.md:

1. **Branching strategy** - Feature branches, trunk-based, or git worktrees?
2. **Branch naming** - Convention for naming branches (e.g., `feature/`, `fix/`, `chore/`)
3. **Worktrees** - If using worktrees, establish conventions for worktree location and naming

### Commit Early, Commit Often (CRITICAL)

**This rule is non-negotiable.** Add the following to CLAUDE.md verbatim:

```markdown
## Git Commit Rules

**COMMIT EARLY, COMMIT OFTEN** - This is mandatory.

- Commit after every successful TDD cycle (RED-GREEN-REFACTOR)
- Commit after completing any discrete unit of work
- Commit before switching context or taking breaks
- Never have more than 30 minutes of uncommitted work
- Each commit should be atomic: one logical change per commit

Why this matters:
- Small commits are easier to review and revert
- Frequent commits prevent loss of work
- Atomic commits make git history useful for debugging
- Regular commits force you to think in small, testable increments
```

### Verification Plan

Use the `britt/writing-verification-plans` skill to create a verification plan. 
This produces a VERIFICATION_PLAN.md file that should be linked in CLAUDE.md as shown below:

```markdown
## Verification

See @VERIFICATION_PLAN.md for acceptance testing procedures.
```

## After Setting Up

* Write the `CLAUDE.md` file
* Use elements-of-style:writing-clearly-and-concisely skill if available
* Commit the `CLAUDE.md` to git
* Ask if the user would like to start brainstorming requirements or an implementation plan. Use `obra/brainstorming` or `obra/writing-plans` if they say yes.

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **DRY ruthlessly** - Remove any repetition of instructions
- **Incremental validation** - Present `CLAUDE.md` in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense
