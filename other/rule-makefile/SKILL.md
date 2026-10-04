---
name: rule-makefile
description: MANDATORY when editing files matching ["**/Makefile", "**/*.mk"]. Conventions for top-level and sub-project Makefiles
---

# Makefile Rules

## Purpose

The Makefile is the project's canonical task runner for local dev and CI. ALWAYS prefer adding a Make target over documenting a raw multi-step command in README.

## Target Conventions

ALWAYS declare `.PHONY` for every non-file target. ALWAYS namespace targets by domain with a prefix or separator (`api-test`, `frontend-lint`, `infra-plan`). ALWAYS provide a `help` target (default) that lists available targets with descriptions.

Correct:
```make
.PHONY: help api-test frontend-lint

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
	  awk 'BEGIN{FS=":.*?## "}{printf "  %-20s %s\n", $$1, $$2}'

api-test: ## Run API tests
	cd api && poetry run pytest
```

Incorrect:
```make
test:
	cd api && pytest
	cd frontend && npm test
# no .PHONY, no help, no namespace
```

## Variables and Portability

ALWAYS use `:=` for immediate assignment of computed values and `?=` for overridable defaults. ALWAYS quote paths with spaces. NEVER assume GNU-specific features without documenting the required make version. Prefer POSIX-compatible shell inside recipes.

## Delegation

ALWAYS delegate complex logic to language-native tooling (`poetry`, `npm`, `terraform`, `docker compose`) rather than encoding it in recipe shell. The Makefile should be a thin dispatcher.

## CI Parity

ALWAYS use the same Make targets in CI workflows and local development so behavior stays in sync. NEVER duplicate command strings between `.github/workflows/*.yml` and the Makefile.

## Secrets and Environment

NEVER hardcode secrets. ALWAYS read environment from `.env` via `include .env` or explicit `export` and document required variables at the top of the file.

## Docker Interaction

For Dockerized workflows, ALWAYS provide paired `*-local` and `*-docker` targets when both are meaningful. See `docker.mdc`.

---

## Related Rules

- **`ci-cd.mdc`** — workflows that invoke Make targets
- **`docker.mdc`** — container build/run targets
- **`api-cli.mdc`** — CLI commands exposed via Make
- **`infra.mdc`** — Terraform wrappers

## Specialist Validation

**Simple (rename target):** None.
**Moderate (new namespace, new orchestration target):** Invoke `codebase-conventions-reviewer`.
**Complex (refactor entire Makefile, cross-subproject orchestration):** Invoke `architecture-strategist`.
