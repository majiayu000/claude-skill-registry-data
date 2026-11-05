---
name: payprobe-build-and-env
description: >
  Recreate the PayProbe development environment from scratch and recognize the
  known environment traps. Load this skill when: setting up a fresh clone or
  fresh machine/VM/sandbox; pip install or editable-install errors
  (payprobe-worker / payprobe-common "No matching distribution found");
  ModuleNotFoundError or ImportError during pytest — i.e. INSTALLING or fixing
  a missing dependency ("tests fail locally but pass in CI" with
  crypto/EMV/pycryptodome/aiohttp symptoms; for triaging an UNKNOWN failure use
  payprobe-debugging-playbook instead); pytest collects zero
  tests or the wrong tests; npm ci / ng build / Prettier / Playwright problems
  in the Angular portal; corrupt node_modules; bringing the stack up with
  docker compose for the first time. Keywords: setup, install, venv, editable
  install, pip, pytest.ini, make install, make test, npm ci, e2e:install,
  docker compose, mock mode, Python 3.11, Node 20, pycryptodome, aiohttp.
---

# PayProbe — build the dev environment from scratch

All commands are relative to the repo root unless a `cd` says otherwise.
Facts below were verified against the tree on **2026-07-03** (see "Provenance
and maintenance" for re-check one-liners).

## When NOT to use this skill

| You actually want | Use instead |
|---|---|
| Meaning/defaults of env vars, flags, config files | `payprobe-config-and-flags` |
| Running/operating the platform (compose anatomy, what lands where, ops) | `payprobe-run-and-operate` |
| What counts as test evidence, adding tests, acceptance thresholds | `payprobe-validation-and-qa` |
| A failing test whose *environment* is fine | `payprobe-debugging-playbook` |

This skill stops at: interpreter + deps installed, suite collecting/passing,
portal building, compose stack answering health checks.

## 1. Prerequisites

| Tool | Version | Evidence |
|---|---|---|
| Python | **3.11+** (CI pins 3.11) | `.github/workflows/ci.yml` (`python-version: "3.11"`); every `packages/*/pyproject.toml` says `requires-python = ">=3.11"`. Service Docker images run `python:3.12-slim` — 3.11 and 3.12 are both in service. |
| Node | **20+** (CI pins 20; Angular 22 needs 20.19+ / 22.12+ / 24+) | `ci.yml` (`node-version: "20"`); portal image builds on `node:22-alpine`; version floor stated in `packages/portal/ANGULAR-UPGRADE-20-to-22.md` |
| npm | ships with Node; portal uses `npm ci` against the committed `package-lock.json` | `ci.yml` test-portal job |
| Docker + compose v2 | any recent (`docker compose`, not `docker-compose`) | `infra/docker/docker-compose.yml` quick-start header |
| make | any | `Makefile` at repo root |

A Python **virtualenv is strongly recommended** — the editable-install layout
below drops a `.pth` file into site-packages that puts the repo's `packages/`
dir on `sys.path` interpreter-wide.

## 2. Python path

### 2a. Understand the layout first (it explains every import error)

Packages live in `packages/` and are imported as **top-level modules**
(`import worker`, `import orchestrator`, `import report_service`,
`import payprobe_common`) — there is no `payprobe.` namespace. Two mechanisms
make that resolve:

1. **Editable installs** of `worker`, `orchestrator`, `report_service`,
   `payprobe_common` use hatchling `dev-mode-dirs = [".."]`, which writes a
   `.pth` adding the parent `packages/` dir to `sys.path` (comment block at the
   top of `packages/worker/pyproject.toml` explains why).
2. **Tests are run from `packages/`** (`make test` does `cd packages && …`),
   and per-package `tests/conftest.py` files insert their package dir on
   `sys.path` where needed (e.g. `packages/mcp-server/tests/conftest.py`).

Consequence: `pytest` from the **repo root** or from inside a package dir with
the repo-wide invocation will misresolve imports. Always
`cd packages` for the shared suite. `packages/pytest.ini` sets
`asyncio_mode = auto` and registers the `flaky` marker for the whole tree.

### 2b. Quick path — `make install` (worker suite only)

```bash
make install
# exact expansion (Makefile):
#   pip install -e "packages/worker[dev]" httpx fastapi structlog pyyaml
```

This is enough for `make test-worker`. It is **NOT enough for full
`make test`**: it installs neither `PyJWT`/`cryptography`
(scenario-service, orchestrator auth) nor `mcp` (mcp-server tests) nor
`uvicorn`. Most missing deps surface as collection-time ImportErrors if you stop here — EXCEPT the `mcp` SDK, whose absence silently drops 10 mcp-server tests via `importorskip` (956 → 946 collected, no error).

### 2c. Full path — editable installs, in dependency order (the trap)

`payprobe-worker`, `payprobe-report-service`, `payprobe-common` are **not on
PyPI** (verified: `pip download payprobe-worker` → "No matching distribution
found"). The orchestrator's `pyproject.toml` depends on all three by name, so
pip must find them already installed — install them editable **first**.
`ci.yml` carries the canonical comment: *"orchestrator depends on the local
payprobe-worker and payprobe-report-service packages (not on PyPI), so install
them editable first to satisfy the dependencies."*

```bash
python -m venv .venv && source .venv/bin/activate

# 1. leaf packages first (payprobe_common before the worker: since ADR-0011 the
#    worker imports its ISO 8583 codec from it)
pip install -e "packages/payprobe_common[dev]"
pip install -e "packages/worker[dev]"
pip install -e "packages/report_service[dev]"

# 2. now the orchestrator resolves its local deps
pip install -e "packages/orchestrator[dev]"

# 3. services with no local-package deps (any order)
pip install -e "packages/scenario-service[dev]"
pip install -e "packages/mcp-server[dev]"
pip install -e "packages/payprobe-assistant[dev]"
```

Notes and cautions:

- **CI drift (observed 2026-07-03):** `ci.yml` pre-installs only
  `worker` + `report_service` before the orchestrator, but
  `packages/orchestrator/pyproject.toml` now also lists `payprobe-common`
  (added later, commit `3152a5f`). Locally, install `payprobe_common` editable
  before the orchestrator regardless of what CI shows.
- **Do not editable-install `auth-service` into the same venv as
  `scenario-service`**: both declare wheel `packages = ["api", "models"]`, so
  the two installs collide on top-level `api`/`models`. CI never installs
  auth-service; its 13 tests run via conftest path insertion from `packages/`
  (`make test`-style invocation) or `cd packages/auth-service && pytest tests/`.
- **Optional extras:** `pip install -e "packages/worker[grpc]"` adds
  grpcio/grpcio-tools/grpcio-reflection for the protoc-dependent gRPC tests
  (they are `skipif`-guarded and simply stay skipped without it — plain
  `[dev]` already includes `protobuf` for the descriptor-only tests).
  `payprobe_common` needs `cryptography` only when `PAYPROBE_SECRET_KEY` is
  set (SecretBox is a passthrough otherwise); `[dev]` includes it.
- Editable installs are strictly required only for *dependency resolution and
  deployment parity*. The test suite itself resolves imports from the
  `packages/` cwd + conftests — a venv with just the third-party deps can run
  it. Prefer the editable route anyway; it is what CI exercises.

## 3. Known traps — with the stories behind them

| Symptom | What it actually is | The story / evidence |
|---|---|---|
| Crypto step "fails" with payload `{"error": "pycryptodome is not installed in this runtime"}` | Missing **import**, not broken logic. `worker/engine/crypto_tools.py` catches the `from Crypto.Cipher import DES, DES3` ImportError and degrades to an error dict instead of raising. | Baseline 2026-06-18 (`docs/history/PROGRESS.md`): 3 `worker/tests/test_engine.py` crypto tests failed because `pycryptodome` was **undeclared** in worker's pyproject while `crypto_tools.py` required it. Fixed in Iteration 1: `pycryptodome>=3.19` is now in `packages/worker/pyproject.toml`. **Lesson: crypto errors → check the import path before the logic.** |
| `test_engine.py` crypto/EMV tests fail locally, pass in CI | Environment, not regression: those tests need crypto key material / pycryptodome that some sandboxes lack. | `docs/history/project-review.md` reviews 3 and 4 record exactly this: "the only failures remain the 4 pre-existing `test_engine.py` crypto/EMV tests (missing key material in this sandbox; they pass in CI)". Discriminator: an `{"error": …}` dict about pycryptodome/key material = environment; an assertion mismatch on computed values = real regression. Never edit the expectation — fix the env. |
| HTTP simulator / HTTP participant-listener tests fail with `ModuleNotFoundError: aiohttp` | `aiohttp` powers the HTTP responder (`packages/worker/adapters/http/responder.py`: `from aiohttp import web`). It is declared in worker deps, but minimal/hand-rolled envs that skipped `pip install -e packages/worker` won't have it. | The orchestrator imports it lazily and returns a clear error ("HTTP participant listeners need 'aiohttp'…", `orchestrator/api/main.py`) rather than crashing at startup; the orchestrator Dockerfile installs it explicitly for in-process HttpResponder use. |
| Sandbox/CI-adjacent env cannot build the portal at all (`@angular/common` unresolvable, implicit-any cascade from rxjs, font fetch fails) | Sandboxed environments historically ended up with a **corrupt `node_modules`** (Angular packages sourcemap-only, `node_modules/rxjs` type declarations missing) and no network for the Google-Fonts inlining that a production `ng build` performs (`packages/portal/src/styles.scss` line 6 imports fonts.googleapis.com). | Recorded independently in `docs/history/GENERAL-ASSISTANT-BUILD-SPEC.md` ("sandbox can't resolve `@angular/common` for any file + Google-Fonts inlining is network-blocked; verify with `npm run build` locally"), `docs/history/CONNECTION-ADAPTER-EXTENSION-SCOPE.md`, `docs/history/CONNECTION-ENV-MIGRATION-PLAN.md`, `docs/history/PARTICIPANT-FLOW-BUILD-SPEC.md`. Recovery = `rm -rf node_modules && npm ci` on a real machine; `packages/portal/ANGULAR-UPGRADE-20-to-22.md` §0 documents the full cleanup incl. a stale `.git/index.lock` from an interrupted `ng update`. **Rule: portal TS changes made in a sandbox are unverified until a real `npm ci && npm run build` passes.** |
| Following CONTRIBUTING.md setup fails (`scripts/test-all.sh` not found) | CONTRIBUTING.md predates the current tooling; `scripts/test-all.sh` does not exist. (`infra/docker/docker-compose.dev.yml` appeared 2026-07-06 as an untracked hot-reload dev overlay — usable via `docker compose -f infra/docker/docker-compose.yml -f infra/docker/docker-compose.dev.yml up -d`; re-verify it was committed.) | Use `docker compose -f infra/docker/docker-compose.yml up --build` and `make test` instead. `npm run lint` is similarly stale — no angular-eslint target is configured (CI comment); use `npm run format:check`. |
| `docker compose -f infra/docker/docker-compose.mock.yml up` does nothing | That file is an **empty stub** kept so old references don't break. | Its own header says so: the main `docker-compose.yml` runs the platform in MOCK mode by default. |
| Full `make test` fails after only `make install` | See §2b — `make install` covers the worker suite only. | Missing `mcp`, `PyJWT`, `cryptography`, `uvicorn` show up as collection-time ImportErrors. |

## 4. Portal (Angular 22, zoneless, esbuild)

```bash
cd packages/portal
npm ci                    # against the committed lockfile
npm run build             # ng build --configuration production -> dist/payprobe-portal/browser
npm run format:check      # Prettier over src/**/*.{ts,html,scss} — the ONLY lint gate
```

- **Zoneless:** `src/main.ts` bootstraps with `provideZonelessChangeDetection()`
  — there is no zone.js. Builds use the `@angular/build` esbuild builder.
- **No angular-eslint.** CI comment in `ci.yml`: "The portal has no
  angular-eslint setup, so `ng lint` has no target. Enforce Prettier style
  instead." Don't "fix" this by adding eslint config casually.
- **Playwright is deliberately NOT in package.json** (CI comment: so it never
  enters the production image's `npm ci`). Install it the sanctioned way:

```bash
npm run e2e:install   # npm install --no-save @playwright/test@^1.48.0 + chromium download
npm run e2e           # backend-free golden-path smoke; Playwright starts ng serve on :4200
E2E_FULL=1 npm run e2e                       # full flows — needs the backend stack running
E2E_BASE_URL=http://localhost:4200 npm run e2e   # test an already-running app (skips webServer)
```

- History (why the tree looks like this): the portal was upgraded 20→21→22 one
  major at a time (`ANGULAR-UPGRADE-20-to-22.md`), and the ngx-graph flow
  canvas was replaced by a custom SVG canvas — `@swimlane/ngx-graph` is gone
  from `package.json`. Do not reintroduce it.

## 5. Docker path

```bash
docker compose -f infra/docker/docker-compose.yml up --build
```

- **Mock mode is the default** — in-memory adapters, no payment hardware or
  secrets. Portal at http://localhost:8080.
- Compose owns build order via `depends_on`; you never build images by hand.
  Two images build from the **repo root context** (`context: ../..`) because
  they need sibling packages copied in: the orchestrator (bundles the worker
  engine in-process) and the worker CLI image.
- Config template: `infra/docker/.env.example` → copy to `.env` for real
  secrets/endpoints (values themselves: `payprobe-config-and-flags`).
- Default service ports: portal **8080**, scenario-service **8000**,
  orchestrator **8100**, mcp-server **8200**, auth-service **8300**,
  insight-service **8500**, agent-hub **8600** (the assistant is mounted
  inside it at `/assistant`; the :8400 container was removed 2026-09-23).
- Profiles: `--profile full` (501 placeholder stubs), `--profile tools`
  (one-shot worker CLI), `--profile load` (load-worker fleet),
  `--profile observability` (Prometheus :9090 + Grafana :3000).
- Minimal backend-only bring-up (the CI mock-integration pattern):

```bash
docker compose -f infra/docker/docker-compose.yml up -d --build orchestrator
curl -fsS http://localhost:8100/health   # poll until 200 (CI allows 60 x 5s)
```

Operating the running stack (tokens, runs, worker provisioners) is
`payprobe-run-and-operate` territory.

## 6. Smoke-verify checklist

Run these in order; each has an expected shape.

| # | Command | Expected (2026-07-03) |
|---|---|---|
| 1 | `python --version` | 3.11+ |
| 2 | `cd packages && python -m pytest worker/tests orchestrator/tests scenario-service/tests mcp-server/tests payprobe-assistant/tests -q --collect-only \| tail -1` | `956 tests collected` with the `mcp` SDK installed (worker 308, orchestrator 274, scenario-service 267, mcp-server 89, assistant 18) — **or `946` without it**: `mcp-server/tests/test_registry.py` does a module-level `pytest.importorskip("mcp")`, silently dropping 10 tests from collection. 946 means the `mcp` SDK is missing, NOT a stale checkout. Counts grow over time; **collection errors = broken env**. |
| 3 | `make test` | All pass, exit 0. This is the CI gate and the suite-green non-negotiable. UNVERIFIED here: the full run was not executed in the authoring sandbox (Python 3.10 only); collection of all 956 + a 107-test sub-run (mcp-server + assistant) passed there. |
| 4 | `cd packages && python -m pytest report_service/tests auth-service/tests -q` | `make test` does NOT include these two (37 + 13 tests, 2026-07-03); CI runs report_service separately. Run them when touching those packages. |
| 5 | `python -c "from Crypto.Cipher import DES, DES3; print('crypto ok')"` | `crypto ok` — else the crypto/EMV tests will "fail" with error dicts (trap #1). |
| 6 | `cd packages/portal && npm ci && npm run build` | Build succeeds; output in `dist/payprobe-portal/browser`. Needs network (Google-Fonts inlining). |
| 7 | `cd packages/portal && npm run format:check` | "All matched files use Prettier code style!" |
| 8 | `docker compose -f infra/docker/docker-compose.yml up -d --build orchestrator && curl -fsS localhost:8100/health` | HTTP 200 within ~2 min of first build. |

## Provenance and maintenance

Authored 2026-07-03 against commit `1b377c8`. Everything above was read from
the tree; commands actually executed during authoring: `pytest --collect-only`
(full 956) and a live 107-test run of `mcp-server/tests` +
`payprobe-assistant/tests` (all passed) — executed on Python 3.10 in a
sandbox, so treat "full `make test` green on clean 3.11" as UNVERIFIED-here
(CI-verified path). PyPI-absence of `payprobe-worker`/`payprobe-common` was
verified live with `pip download`.

Re-verify volatile facts before trusting them:

```bash
grep -n "python-version\|node-version" .github/workflows/ci.yml   # interpreter pins
sed -n '30,32p' Makefile                                          # make install expansion
grep -n "payprobe-" packages/orchestrator/pyproject.toml          # local-dep install order
grep -n "pycryptodome" packages/worker/pyproject.toml             # trap #1 stays fixed
grep -rn "dev-mode-dirs" packages/*/pyproject.toml                # .pth editable layout
cat packages/pytest.ini                                           # suite-wide pytest config
grep -n "e2e:install\|format:check" packages/portal/package.json  # portal script surface
grep -n "provideZoneless" packages/portal/src/main.ts             # still zoneless
head -20 infra/docker/docker-compose.yml                          # mock-default quick start
cd packages && python -m pytest worker/tests orchestrator/tests scenario-service/tests mcp-server/tests payprobe-assistant/tests -q --collect-only | tail -1   # current test count
```
