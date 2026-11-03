---
name: flisk-e2e-author
description: Guides an AI assistant through adding or changing an end-to-end test in flisk - deciding whether one is required, choosing the group, scaffolding a suite under tests/e2e from the agent reference suite, using the shared helpers, running cases on a real stack, and capturing passing and deliberate-break evidence. Use when adding a resource type, a command or MCP tool that talks to a running stack, a provider (language or framework), or a change to flisk up, Traefik routing or the engine.
license: MIT
compatibility: Requires the flisk CLI, Docker, Tilt, Node 22+, jq and curl to run suites. Writing and validating them needs only the checkout.
metadata:
  author: flisk-sh
  version: "1.0"
---

# Writing Flisk end-to-end tests

The human version of this guide is `docs/contributing/05-write-e2e.md`. Read it when you need the details. This skill is the procedure. The reference suite is `tests/e2e/resource-types/agent/`.

## 1. Decide whether an e2e is required

An e2e is **required** when the change:
- adds or changes a resource type (`VALID_RESOURCE_TYPES` in `cli/src/utils/constants.ts`). Report that a suite is required under `tests/e2e/resource-types/<type>/`;
- adds or changes a command or MCP tool that talks to a running stack;
- changes `flisk up`, `flisk down`, Traefik routing, or engine-generated Compose or Tilt files;
- adds a provider users select with a flag (backend language, backend or frontend framework).

It is **not** required when nothing starts a stack. Then write unit tests in `cli/src/**/__tests__/`. Say which case applies and why before writing anything.

## 2. Choose the group

`resource-types` (one type), `journeys` (multi-command flow), `examples` (real app), `platforms` (host), `scale` (large fixture or benchmark). A stackless CLI spawn test is `cli-integration` and stays in vitest. A suite lives at `tests/e2e/<group>/<suite>/` and nowhere else.

If the behavior is already covered by an existing suite, add cases there instead of creating a new suite. If the closest test still lives in a legacy location (`.github/workflows/*-e2e.yml`, `scripts/e2e/`, `scripts/verify-*.sh`, `tests/e2e/*.test.sh`), tell the user. Either extend it in place or move it first, in a separate pull request.

## 3. Scaffold from the reference

1. Create `run.sh` (executable) with the standard header: `SUITE_DIR=...`, `source "$SUITE_DIR/../../lib/lib.sh"`, `e2e_init <suite> <project>`, `RESOURCES=(...)`, then case functions, then `e2e_main "$@"`.
2. Create `suite.json` with exactly these keys: `group`, `suite`, `description`, `paths`, `cases` (CI order), `triggers` (`pr`, `nightly`, `release`, `manual`, `weekly`), `timeoutMinutes`, and `needsSecrets` (secret names, `[]` if none; no `pr` trigger if non-empty).
3. Run `node tests/e2e/lib/validate-suites.mjs` and `tests/e2e/<group>/<suite>/run.sh self-check`.

## 4. Write cases with the shared helpers

Never copy a helper into a suite. Use `tests/e2e/lib/lib.sh`, and add new shared helpers there with a test in `tests/e2e/lib/__tests__/`.

- One function per case, named like `A1`. Each case **creates its own preconditions**: check the state it needs (running container, data) and create it.
- `run <name> <flisk args>` records the output, then you check `$RC` yourself. `run_in <dir> ...` runs in another project.
- Wait only with `poll_until "<what>" <seconds> <command>`. Never use `sleep`.
- After `flisk restart`, call `wait_restarted <resource> "$before" "<desc>" <ready command>`. The old container answers until it is replaced.
- A request whose result a later assertion uses goes through `traefik_request_ok`. It fails on non-2xx instead of passing an error page on.
- Error paths: `assert envelope "$OUT/<name>.out" <CODE>`. Other checks: `assert check <file> "<js expr on j>" "<message>"`, `assert equal <a> <b>`.
- Fake upstreams: `with_stub <port> hang|stall|status <code> <msg>|json <body>`, then `stop_stub`.
- MCP: `mcp_session <name> '<calls json>' [cwd]`, then `mcp_structured <name> <index>`.
- A resource-type suite covers: scaffold with `flisk resource`, a bounded wait in `flisk status --json`, the type's observable contract, `flisk restart` with a replaced-container wait, and at least one error envelope. List any case that does not apply, with the reason.

## 5. Run against a real stack

```bash
make test-e2e GROUP=<group> SUITE=<suite> CASES="<case> ..."
```

Run every new or changed case, then `run.sh cleanup`. If Docker, Tilt or `flisk` is unavailable, say so plainly. Do not claim the suite passes based on `bash -n` or the validator alone.

## 6. Capture evidence

1. A passing run of the cases, as captured output.
2. A **deliberate break**: change the behavior under test locally, run the case, and capture the failure. Then revert the break and confirm the diff no longer contains it.

Put both in the pull request description. Also run `make test-shell` and read its exit code.

## 7. Wire into CI

Until the group workflows land, add each new case as a step in the suite's workflow, in the same order as `suite.json`, and add the suite's paths to the workflow's `paths:` filter. Check `openspec/changes/organize-e2e-suites/tasks.md` for what has moved.
