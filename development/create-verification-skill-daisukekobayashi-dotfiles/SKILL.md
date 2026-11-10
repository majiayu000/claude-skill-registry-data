---
name: create-verification-skill
description: Use only when the user explicitly invokes create-verification-skill to create and exercise project-local verification of real UI, CLI, service, or library behavior.
license: MIT
disable-model-invocation: true
---

# Create a Verification Skill

Run only when the user explicitly invokes `create-verification-skill`, such as
`$create-verification-skill` in Codex or `/create-verification-skill` in Claude
Code. A generic verification request or a reference from another skill does
not activate this workflow.

Build a project-specific, rerunnable verification procedure and prove that its
instructions work. The generator is reusable in user scope; the generated
commands, feature map, and evidence rules belong to the target project.

## Discover the real execution path

Inspect repository instructions, state, README, wrappers, CI, and existing
tests before choosing commands. Use available execution-context-first and
runtime-isolation skills. Identify:

- the user-facing surface and one important behavior to verify;
- the documented build/start/stop entry points and readiness signal;
- existing drivers, fixtures, selectors, and observable results;
- authentication and dependencies needed, without reading secret values;
- ownership of processes, ports, data directories, and external side effects.

Prefer existing project tools. If dependencies, access, or startup are missing,
identify the exact gap. Do not fix unrelated setup or install a new framework
as part of generation without authorization.

## Choose project-local storage

Use the project's established skill location. Otherwise use
`.agents/skills/verify-<app>/` for Codex or
`.claude/skills/verify-<app>/` for Claude Code. When both are needed, prefer one
canonical project-owned directory and a relative link rather than two copies.

Resolve existing symlinks before writing: a project skill directory may point
to the user's global skill view. Never write through it into user scope.
Inspect any existing verify skill and preserve unrelated content. If its name
is owned by a profile or external package, choose a distinct project name.

Classify the verification skill and reusable helpers as durable project
operational documentation. Keep run logs and screenshots in an ignored
task directory or /tmp; do not stage or commit them automatically.

## Write the procedure

Use [the verification contract](references/verification-contract.md) to write a
complete SKILL.md with valid name/description frontmatter. Include exact commands
and real observable outcomes from this repository, not placeholders. Keep
variable runtime paths explicit and shell-safe.

Seed a small feature index and per-feature instructions for the important
user-facing behaviors actually discovered. Include alternate entry points when
they materially change coverage. Add helpers only when they make driving or
checking the behavior reliable; document their invocation.

Reference the documented build/test tools, not the user's personal paths.
Record required configuration by name, never by secret value.

## Exercise what was generated

Follow the generated procedure once: readiness check, owned launch if needed,
one mapped user path, assertions, evidence capture, and cleanup. After cleanup,
confirm that the evidence survives. Do cleanup after failed attempts as well.

Use [prove-it-works](../prove-it-works/SKILL.md). A generated procedure that was
never successfully executed is a draft. Report exactly which behavior ran and
which feature-map entries remain unverified; one successful path does not
certify the whole application.

If execution needs missing access, tools, or extra approval, complete the safe
authoring work and report the draft status and concrete remaining step.
Do not invent screenshots, outputs, or a successful run.

## Source

Adapted from Lauren Tan's [pstack create-verification-skill](https://github.com/cursor/plugins/blob/12d587dfb20741cafc376c42c696c5f6e2a64487/pstack/skills/create-verification-skill/SKILL.md).
Local changes: Codex/Claude project locations, existing wrapper reuse, protection
against global symlink writes, and explicit draft/coverage states. See [LICENSE](LICENSE).
