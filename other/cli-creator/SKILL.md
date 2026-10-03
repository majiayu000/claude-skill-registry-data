---
name: cli-creator
description: Use when designing, scaffolding, refactoring, or auditing Python CLI tools or CLI-related skills/templates, including command-first CLIs, configuration-driven tools, performance-oriented utilities, interactive assistants, data pipelines, LLM-enabled command line products, Typer, Click, argparse, uv, packaging, testing, and release workflows.
---

# CLI Creator

Router for building and auditing production-grade Python CLI tools and CLI-related skills/templates. Use it to decide CLI shape, keep the command surface small, preserve installability, and enforce review outputs. This skill stays lightweight: read only the references you need.

## When To Use

- New Python CLI or command tree.
- CLI refactor, simplification, or packaging cleanup.
- CLI review/audit, including UX, config, errors, cache, and release flow.
- Agent skill, scaffold, or template that behaves like a CLI package.
- Verification of install, wheel, or console-script behavior.

## CLI Type Selection

| Type | Bias |
|---|---|
| Command-first utility | Thin router, strict exit codes, JSON/plain output. |
| Configuration-driven tool | Config discovery, precedence, reproducibility. |
| Interactive assistant | Flow/state machine, prompts, recovery. |
| Hybrid CLI | Small command tree plus reusable orchestration. |
| Performance-heavy CLI | Lazy imports, bounded IO, cache/progress. |
| Plugin/extensible CLI | Stable extension contract and registry. |
| Agent/assistant CLI | One command registry feeding parser, slash commands, help, prompts, headless mode, and permissions. |

Do not force an assistant architecture onto a command-first tool. Do not force a single-script shape onto a growing product.

## Core Rules

- Prefer the smallest CLI that solves the user job.
- Use the minimal CLI/YAGNI path: if the tool has one or two commands, no persistent state, no network, no plugins, and no credentials, keep it tiny; do not add Rich, Pydantic, platformdirs, cache layers, `doctor`, or plugin registries unless they solve an immediate problem.
- Keep names, flags, exit codes, config keys, and output modes stable.
- Make defaults useful and safe.
- Separate routing, domain logic, IO, config, persistence, rendering, and integrations.
- Keep machine output scriptable with JSON or plain mode.
- Verify that the README command is the installed console script.
- For assistant, slash-command, or plugin CLIs, keep one command descriptor contract. Include name, aliases, description, visibility, enabled state, source, execution kind, non-interactive support, permission requirements, and lazy loader.
- Treat interactive and headless modes as separate product paths with shared command contracts. A command that renders a TUI picker should not silently appear in `--print`, CI, or remote/bridge mode unless it has a non-interactive implementation.
- Put dangerous capabilities behind a reviewable permission model: filesystem writes, shell execution, plugin loading, credential access, remote mutation, and generated artifact sends should have clear allow/deny/ask rules and safe failure behavior.
- Keep `--help` and machine modes import-light. Lazy-load heavy UI, analytics, provider SDKs, plugin registries, and report renderers inside the command body.

## Reference-Loading Rules

Read only the references needed for the task:

- Creation or refactor: `references/creation-playbook.md`.
- Review or audit: `references/review-rubric.md` and `references/pitfalls-and-solutions.md`.
- Implementation details, packaging, security, cross-platform behavior, Rich output, cache, or LLM providers: `references/technical-best-practices.md`.
- For skill/package maintenance, consult workspace-root governance folders `skill-ir/`, `evals/`, `scripts/`, `reports/`, and `registry/` when they exist. These are maintainer-side routing aids, not bundled inside an installed skill copy.

Do not duplicate those references here. Load them only when the current task needs them.

## New CLI Or Skill Creation Flow

1. Determine the product shape: who runs it, what pressure it is under, and what must be cached, remembered, or forgotten.
2. Design the command surface with a few stable commands and real examples.
3. Choose the smallest stack that fits.
   - Typer or Click for most CLIs.
   - argparse only for tiny stdlib-friendly tools.
4. Pick the smallest architecture that will survive the next two releases.
5. Implement the product loop: input, validation, execution, rendering, persistence, exit code, recovery hint.
6. Verify before shipping.

### Command Surface Examples

```text
my-cli run
my-cli init
my-cli config show
my-cli doctor
my-cli cache clear
my-cli check PATH
my-cli fetch QUERY --json
my-cli export ID --output result.md
```

Rules:

- Use arguments for required domain objects.
- Use options for modifiers, output modes, and optional behavior.
- Provide `--json` or `--format json` for automation.
- Provide `--quiet`, `--verbose`, and `--debug` consistently.
- Avoid surprising network or mutation in commands that sound read-only.

## Verification Expectations

Always verify the command surface, installation path, and wheel path when they matter:

- `--help` for the root command and each top-level command.
- Clean install into a new environment.
- Missing config or first-run path when the tool has config.
- Invalid config or error path when the tool validates input.
- Success path plus JSON/scriptable mode when supported.
- Cache refresh and cache clear when the tool has cache.
- Packaging metadata and console script.
- Wheel install from outside the repository when you want install confidence.

Use this compact pack when applicable:

```bash
uv venv /tmp/cli-audit
. /tmp/cli-audit/bin/activate
uv pip install -e .
cli-creator-skill --help
cli-creator-skill install
uv build
uv pip install dist/*.whl
python -m pytest
```

## Review Workflow

When auditing an existing CLI or CLI-related skill/template:

Before reviewing, read:

- `references/review-rubric.md`
- `references/pitfalls-and-solutions.md`

Read `references/technical-best-practices.md` when the audit touches implementation details, packaging, security, cross-platform behavior, Rich output, caching, or LLM providers.

Then:

1. Inspect repository shape: package layout, command entry points, config files, tests, docs, CI.
2. Run help: root `--help` and command-level help.
3. Trace one successful command from callback to domain service to renderer.
4. Trace one failure path and inspect error quality.
5. Check configuration precedence: flags, env, project config, user config, defaults.
6. Check security: secrets, shell execution, path handling, unsafe config/plugins, telemetry, subprocess timeouts, dependency supply chain.
7. Check performance: startup imports, network timeouts, cache behavior, file discovery.
8. Check automation: exit codes, JSON output, stdin/stdout/stderr separation, non-TTY behavior.
9. Check packaging: Python version, dependencies, scripts, wheels, README commands.
10. Score every rubric area with `references/review-rubric.md`.
11. Return findings first, then prioritized fixes.

## Required Audit Output

Audit output must include these sections, in this order:

```markdown
**Findings**

**Scores**

| Area | Score | Notes |
|---|---:|---|

**Repair Order**

**Test Gaps**

**Verification Commands**
```

## Maintenance Notes

- Keep this skill as a router; put implementation detail in the four references.
- Keep the command examples, audit headings, and verification pack in sync with the package release.
- For maintainer-side governance, use the workspace-root `skill-ir/`, `evals/`, `scripts/`, `reports/`, and `registry/` folders when present; do not pretend they are part of the installed skill.

## What This Skill Helps With

- Designing a new Python CLI from scratch.
- Reviewing an existing CLI for UX, packaging, errors, model setup, caching, and maintainability.
- Structuring Typer, Click, argparse, or hybrid applications.
- Building natural multi-turn CLI flows without making users feel like they are filling out a form.
- Adding diagnostics, cache, profile memory, and first-run setup flows when they are actually needed.
- Reviewing CLI-related skills and templates for trigger clarity, reference completeness, command templates, output contracts, and maintenance strategy.

## Design Basis

This skill distills maintainer experience and official documentation patterns for Python packaging, Typer, Click, Rich, uv, Ruff, Pydantic, and LLM provider integration. It does not vendor code or instructions from unofficial third-party repositories.
