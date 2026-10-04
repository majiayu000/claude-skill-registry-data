---
name: docs-update
description: Portable, language-agnostic docs updates for any project. Avoid duplicate doc paths, respect discovered ownership, branding, and terminology, and validate docs plus runnable examples.
triggers:
  - docs update
  - update documentation
  - fix docs
  - documentation update
  - write docs
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - write_file
  - search_replace
---

<!-- Provenance: generic, portable. It names no fixed documentation toolchain or project. -->

# Docs Update

## Purpose

Update project documentation without introducing duplicate topics, bypassing the project's ownership model, or publishing unvalidated examples. Discover the project's conventions from the workspace rather than assuming them.

This skill is the **portable, reasoning-driven** docs updater. A repository may also provide a project-bound docs skill backed by a fixed ownership registry, brand/naming rules, and a docs-check command. When one exists and the change is within its scope, defer to those project-specific contracts for mechanical gates; use this skill when no project-specific docs contract applies, or for the general reasoning, dedup, and validation it provides.

## Read First

- Target docs paths named by the user.
- Discover, do not assume: the project's documentation tree layout (for example `docs/**`, `README`, index/landing files).
- The project's documentation ownership or registry, if one exists (for example an OWNERS file, CODEOWNERS, or similar); do not invent owners.
- The project's naming, branding, and terminology conventions, if documented.
- The project's documentation validation command, if one exists (for example a docs linter, link checker, prose build, or a `docs-check` target).
- Any top-level contributor or style guide for documentation conventions.

## Method

1. Search for existing coverage before adding a new doc; prefer editing the existing canonical path.
2. For an existing topic, resolve its owner and canonical path from the project's documentation ownership or registry if one exists; stop if the registry is incomplete or contradictory. If no registry exists, follow the project's documented conventions.
3. For a genuinely new topic, follow the project's ownership process for new topics (for example registering it in the project's registry) before creating its canonical path. Do not invent an owner or create a document that bypasses the project's process.
4. Reject duplicate topics across the project's documentation tree (for example `docs/**`, the root `README`, and other index/landing files) unless one is the canonical pointer and the others link to it.
5. Follow the project's own naming, branding, and terminology conventions - discover them, do not assume them. If the project publishes a brand/terminology guide, conform to it; if it defines allowed or forbidden forms, enforce those exactly. Do not impose conventions the project does not declare.
6. Keep changes minimal; update indexes and links in the same change when paths move.
7. This skill declares no command execution. When the invoking agent has it, run the project's documentation validation command if one exists (for example a docs linter, link checker, or build). Validate any runnable command, flag, config example, or expected output shown in the docs with the narrowest safe evidence (for example the documented CLI's `--help`, the named build or test target, or a focused test). For touched links, run an available lightweight checker or inspect local targets; report any check that cannot run and has no manual fallback. Without command execution, report every such check as `NOT_RUN` with the reason rather than omitting it.

## Rules

- Never create a second doc that restates an existing canonical page; link instead.
- Respect the project's ownership model. A missing or contradictory owner entry for an existing topic where one is required is `BLOCK`; a new topic must follow the project's ownership process before its document is created.
- No unresolved drift markers (for example `TODO`, `FIXME`, or placeholder text) in committed docs.
- Severity never gates approval.

## Report shape

When a resource catalogue and its scoped reader are available, load
`report-template` before producing the update report. Without that capability,
use the inline report shape below.

### Result

`PASS`, `BLOCK`, `PARTIAL`, or `NOT_RUN`.

### Scope

- docs touched and the ownership model or registry used (or `none discovered`);
- the naming, branding, and terminology conventions applied (or `none discovered`).

### Checks executed

- exact command or method (with exit status);
- summarized result, not full successful output;
- the concern covered (ownership, dedup, naming, link validity, runnable example);
- list a check as not run only if it was required and could not be executed.

### Remaining risk

- skipped checks, unresolved ownership decisions, unverified links or examples, or `None identified within the executed scope`.

### Result semantics

- `PASS` - docs updated consistently, no duplicate topics, project naming/branding respected, and all available validation passed.
- `BLOCK` - a required owner is missing or contradictory, a duplicate topic is not the canonical pointer, unresolved drift remains, or a canonical link is broken.
- `PARTIAL` - a useful edit was made but a required ownership decision, validation command, or check remains.
- `NOT_RUN` - plan only, or no documentation conventions could be discovered.

Keep the report concise. Do not paste complete successful logs. Do not claim links or examples were verified unless the relevant check ran.
