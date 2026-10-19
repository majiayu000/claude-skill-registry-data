---
name: oss-project
description: >
  Scaffold, polish, and publish open-source projects with AI-first documentation,
  governance, and CI. Use when: Starting a new OSS package, polishing/publishing
  an existing repo, setting up AGENTS.md / CONTEXT.md / DECISIONS.md / ROADMAP.md,
  onboarding AI agents to a codebase, or creating standard community files
  (README, LICENSE, CONTRIBUTING, CHANGELOG, CI pipelines, issue templates).
  Outputs repo description and tags at the end.
tier: core
version: 0.1.0
kind: reference
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
---

# OSS Project

Bootstrap, polish, and publish open-source projects with AI-first documentation
and governance standard. Designed for AI-first development where documentation
is the primary interface for agent contributors.

> **Origin:** Extracted from a real AI-powered sprite restyling package
> and generalized as a reusable pattern for rapid PoC shipping.

## Sources & Attribution

| Source | What | URL |
|--------|------|-----|
| dec0dOS/amazing-github-template | `.github/` structure, community files, workflows | https://github.com/dec0dOS/amazing-github-template |
| othneildrew/Best-README-Template | README section conventions | https://github.com/othneildrew/Best-README-Template |
| anthropics/skills `doc-coauthoring` | Documentation co-authoring workflow | https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring |
| gitleaks/gitleaks-action | Secrets scanning workflow | https://github.com/gitleaks/gitleaks-action |

## Usage

```bash
# Scaffold a new project
/oss-project init --name my-project --lang typescript

# Add missing docs to an existing project
/oss-project audit --path ./my-project

# Polish an existing repo for open-source publishing
/oss-project polish --path ./my-project
```

## What It Creates

```
my-project/
├── AGENTS.md              # AI agent entry point (build, conventions, gotchas)
├── CONTEXT.md             # Static architecture overview + reading order
├── CONTRIBUTING.md        # Dev workflow, code style, testing philosophy
├── DECISIONS.md           # Architecture Decision Log (DEC-001, DEC-002, ...)
├── ROADMAP.md             # Priorities with acceptance criteria
├── README.md              # Product-level docs with badges
├── CHANGELOG.md           # Keep a Changelog format, populated from git history
├── CODE_OF_CONDUCT.md     # Contributor Covenant
├── SECURITY.md            # Vulnerability reporting
├── RELEASING.md           # Release runbook (Changesets)
├── LICENSE                # MIT (default)
├── .editorconfig          # Consistent formatting across editors
├── .gitattributes         # Line-ending normalization
├── .nvmrc / .node-version # Node.js version pinning (if applicable)
├── .github/
│   ├── workflows/
│   │   ├── ci.yml         # Build + typecheck + test + Gitleaks secret detection
│   │   └── release.yml    # Changesets auto-release + npm publish with provenance
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md  # Structured bug report (env, repro steps, logs)
│   │   └── feature_request.md  # Problem → solution → alternatives
│   └── pull_request_template.md  # Checklist + decision impact + contributor type
└── ...
```

All templates are in `templates/` and use `{{PLACEHOLDER}}` syntax for project-specific values.

### README Best Practices (Baked In)

The README template follows current OSS best practices:
- **Centered header** with project name + one-line description
- **Badge row** (npm version, license, TypeScript, CI status)
- **"How It Works"** -- visual pipeline diagram before any details
- **Feature list** with emoji markers for scannability
- **Install + Quick Start** -- copy-pasteable within 30 seconds
- **Environment variables table** -- not buried in prose
- **CLI reference table** -- command + description, no walls of text
- **Programmatic usage** -- import example for library consumers
- **CI & Security section** -- signals trust and professionalism
- **Roadmap link** -- points to ROADMAP.md (single source of truth)
- **Contributing link** -- split by audience (AI agents → AGENTS.md, humans → CONTRIBUTING.md)
- **Footer** with npm + GitHub + Issues links

**README rules:**
- Lead with what, not how. First sentence = value proposition.
- Badges: only include meaningful ones (CI status, version, license). No vanity badges.
- Code examples must be copy-pasteable and working.
- No "Table of Contents" for READMEs under 200 lines.
- Prefer a visual (screenshot, diagram, GIF) if the project has UI.

### CHANGELOG (Keep a Changelog)

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Initial public release
```

**Rules:** Populate from actual git history -- don't invent entries. Group by: Added, Changed, Deprecated, Removed, Fixed, Security. Link version headers to GitHub compare URLs when possible.

### Additional Files (Always Include)

#### .editorconfig
```ini
root = true

[*]
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
charset = utf-8

[*.{js,ts,jsx,tsx,json,yml,yaml,md}]
indent_style = space
indent_size = 2

[Makefile]
indent_style = tab
```

#### .gitattributes
```
* text=auto eol=lf
```

#### .nvmrc / .node-version (Node.js projects)
Pin the runtime version to match the project's target.

### CI Pipeline (Security-First)

The CI template includes:
- **Build + Typecheck** -- catches type errors before merge
- **Gitleaks secret detection** -- scans full git history for leaked API keys, tokens, passwords
- **Release automation** -- Changesets creates release PRs, publishes to npm with provenance
- **Branch protection ready** -- designed for required status checks on `main`

## Core Principles

### 1. AGENTS.md Is The Front Door

Every AI agent starts here. It must contain:
- Build & test commands (copy-pasteable)
- Architecture overview (10 files or less)
- Code conventions (strict, no ambiguity)
- Key decisions summary (with links to DECISIONS.md)
- Gotchas (things that will waste an agent's time)
- Reading order for deeper context

**Rule:** If an agent can't orient itself from AGENTS.md alone, it's incomplete.

### 2. Documentation As Interface

In AI-first development, docs are not afterthoughts -- they are the API.

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `AGENTS.md` | Agent entry point | Every architecture change |
| `CONTEXT.md` | Static background | Rarely (module map changes) |
| `DECISIONS.md` | Living decision log | Every non-trivial decision |
| `ROADMAP.md` | Priorities + acceptance criteria | When items change status |
| `CONTRIBUTING.md` | Dev workflow + testing | When process changes |

**Rule:** Inline TSDoc in source files is the source of truth for implementation.
Markdown docs are for orientation and decisions.

### 3. Lean Governance (Founder Mode)

For early-stage projects:

```markdown
## Governance

- **Owner / decision authority**: @<founder>
- **AI implementation agent**: @<agent>

Decision rules:
- Non-trivial changes require a DEC-xxx entry in DECISIONS.md
- New decisions start as `Status: proposed`
- Only @<founder> marks decisions as `accepted`
```

Scale governance only when the project demands it. Don't cargo-cult.

### 4. Decision Log Format

Every architecture decision gets a structured entry:

```markdown
## DEC-001: <Title>

- **Status**: proposed | accepted | superseded
- **Date**: YYYY-MM-DD
- **Owner**: @<founder>
- **Proposed-by**: @<agent-or-human>
- **Accepted-by**: (pending)
- **Decision**: <one sentence>
- **Rationale**: <why this over alternatives>
- **Supersedes**: DEC-00Y (optional)
- **Affected modules**:
    - `src/...`
```

**Rule:** Every PR must declare decision impact (none / implements existing / proposes new).

### 5. Roadmap With Teeth

Every roadmap item must have:
- **Priority** (High / Medium / Low)
- **Status** (Not started / In progress / Done)
- **Why** -- the problem it solves
- **Constraints** -- non-negotiable boundaries
- **Approach** -- high-level how
- **Acceptance criteria** -- measurable definition of done

Vague roadmap items ("improve performance") are not allowed.

### 6. Tests As Specification

```
Tests serve two purposes:
1. Verify correctness
2. Specify behavior for the next agent
```

An agent reading tests should understand what the code is supposed to do.
No manual verification steps. Everything automatable.

### 7. PR Checklist (Enforced)

Every PR:
- [ ] `typecheck` -- zero errors
- [ ] `build` -- compiles clean
- [ ] `test` -- all pass
- [ ] Changeset added (unless docs-only)
- [ ] TSDoc on new/changed public API
- [ ] Tests for new/changed behavior
- [ ] Decision impact declared

## Phase 3: Repo Description & Tags

**After all files are created**, output (NOT as a file -- print to the user) a suggested:

```
Description: <one-liner, max 350 chars -- what it does + key differentiator>

Topics/Tags:
  - <tag1>
  - <tag2>
  - ...
  (6-12 tags: include language, framework, domain, and discoverability terms)

Website: <docs URL or homepage if applicable>
```

**Tag rules:**
- Always include: primary language (e.g., `typescript`), framework (e.g., `react`), project type (e.g., `cli`, `library`, `framework`)
- Add domain tags (e.g., `ai`, `devtools`, `automation`)
- Use lowercase, hyphenated format
- 6-12 tags total

## Audit Mode

When running on an existing project, the skill checks for:

1. ❓ Missing `AGENTS.md` → Generate from source analysis
2. ❓ Missing `CONTEXT.md` → Generate architecture overview
3. ❓ Missing `DECISIONS.md` → Create with governance template
4. ❓ Missing `ROADMAP.md` → Create with priority template
5. ❓ Missing `CONTRIBUTING.md` → Generate from detected toolchain
6. ❓ Missing `CHANGELOG.md` → Generate from git history
7. ❓ Missing CI workflows → Generate based on language/framework
8. ❓ Missing PR template → Add standard template
9. ❓ Missing issue templates → Add bug + feature templates
10. ❓ Missing `.editorconfig` → Add standard config
11. ❓ Missing `.gitattributes` → Add line-ending normalization

## Language Support

Templates auto-detect and adapt to:

| Language | Build | Test | Lint | Package Manager |
|----------|-------|------|------|-----------------|
| TypeScript | `tsc` | `vitest` | strict mode | `pnpm` |
| Python | `uv build` | `pytest` | `ruff` | `uv` |
| Rust | `cargo build` | `cargo test` | `clippy` | `cargo` |
| Go | `go build` | `go test` | `golangci-lint` | `go mod` |

## Philosophy

> "Es zählt nicht, wer den schönsten Code schreibt.
> Es zählt, wer die meisten Menschen inspiriert."
> -- a wise co-founder

This skill exists because shipping 10 well-documented PoCs beats
one undocumented monolith. Every new project deserves a clean start
with the right structure from day one.

### Polish Principles

1. **Don't over-document** -- A 50-line CLI doesn't need SECURITY.md and 4 issue templates. Scale documentation to project size.
2. **Real content only** -- Never leave `[TODO]` or `Lorem ipsum`. Either fill it in from the codebase or skip the section.
3. **Badges must work** -- Only add badges for things that are actually set up (CI, npm, license).
4. **Match the project's voice** -- A fun side project gets casual tone; an enterprise library gets professional tone.
5. **Git history is truth** -- Populate CHANGELOG from actual commits, not imagination.
6. **Ask when uncertain** -- License choice, project name, target audience -- ask the user rather than guessing.
