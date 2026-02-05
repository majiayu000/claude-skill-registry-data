---
name: agentpack-dev
description: Contribute to Agentpack itself (spec-driven changes, tests, releases).
---

# agentpack-dev

This skill is for developing the `agentpack` repo (not for operating agentpack on another project).

## Canonical docs (read first)
- `docs/CODEX_EXEC_PLAN.md` (AI-first execution roadmap)
- `docs/SPEC.md` (authoritative implementation contract)
- `docs/JSON_API.md` + `docs/ERROR_CODES.md` (`--json` contract + stable error codes)

## Spec-driven workflow (OpenSpec)
- Read: `openspec/AGENTS.md` and `openspec/project.md`
- Create proposal: `openspec/changes/<change-id>/` (verb-led kebab-case)
- Validate: `openspec validate <change-id> --strict --no-interactive`
- After merge: archive via `openspec archive <change-id> --yes` (separate PR)

## Local verification
- `cargo fmt --all -- --check`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `cargo test --all --locked`
