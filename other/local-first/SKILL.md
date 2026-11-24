---
name: local-first
description: Select existing Nx-affected tests, verify real isolated local behavior, then hand off an exact-source candidate to final CI.
---

# Local first: develop, verify, then CI

Use on all code changes under #2997; this skill does **not** replace `AGENTS.md`, the existing acceptance owner or protected CI.

1. In the task's authorized Linux cloud computer, run `pnpm local:plan` (defaults to the merge base with `origin/main`). It reuses `scripts/ci/graph.mjs` and `scripts/ci/select.mjs`; the reported Nx reverse dependents suggest **existing owning scripts**. A global/unknown source indicates broader final CI, **not** an instruction to run the entire CI matrix during debugging.
2. Reproduce the changed feature's real failure using the existing app/API/CLI, isolated PG17 `*_e2e` and Eve/daemon when applicable. Run a focused existing script, e.g. `pnpm local:check --test=test:groups`. Fix the root cause and repeat that script until successful. Always inspect the actual selected test count and exit code. No real model API keys for ordinary fake acceptance.
3. For visible UI or real user behavior, run the existing local production build and capture its screenshots/outcomes using the accepted `docs/acceptance.md` process. Reuse verified reports whose exact source and conditions match; do not invent an acceptance result from lint or a CI green.
4. Commit the actual source changes and push a Draft checkpoint. With a **clean** HEAD run `pnpm local:ready --test=<owning-script> --accept=test:local-loop` where that is the applicable local acceptance. Existing local evidence can be supplied via `--report=<path>` instead. When the change genuinely does not affect product behavior, use a precise `--no-product-change='tooling: <why>'` or `docs: <why>`. Failed tests, missing evidence or an uncommitted tree must fail.
5. Run `pnpm local:mark-ready --pr=<number>`, not a bare `gh pr ready`: it checks the ignored local evidence against the exact HEAD and committed diff before invoking GitHub. Include the source SHA, executed commands, exit codes, real acceptance results and any external-only gaps in the PR's **How it was checked** section.
6. Let required CI independently validate the Ready candidate; do not keep editing by waiting for every queued job. If CI reveals a locally reproducible failure, return to step 2 and generate fresh evidence bound to the new SHA. Separate code merge, Cloudflare staging and production acceptance.

`local:plan` is advisory; `local:ready` creates a local record, not a signed or remote attestation, and a human can still change a PR's status from GitHub. Existing branch protection and independent review remain authoritative. Never delete, skip or weaken required tests to make a PR pass.
