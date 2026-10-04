---
name: foundation-deps
description: Install and configure all project dependencies — pick versions matching the architecture, separate dev/test/runtime groups, generate lock file, set up virtualenv (or equivalent), verify import + smoke-test on fresh install. Loads at project bootstrap when no dependencies are installed yet, or when the operator says "install deps", "set up the venv", "wire up requirements", "bootstrap from scratch".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# foundation-deps

The foundation skill that installs and configures a project's dependencies. AICP's pattern (per [pyproject.toml](../../../pyproject.toml)): minimal runtime deps + `[project.optional-dependencies] dev` group + Python 3.11+ floor + venv at `.venv/`.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **No deps installed**: project has `pyproject.toml` (or equivalent) but no `.venv/` / `node_modules/` / `target/` / `vendor/`. Operator wants to bootstrap.
- **Direct verb**: operator says "install deps", "set up the venv", "wire up requirements", "bootstrap from scratch", "make this runnable".
- **Foundation-stage of project-lifecycle**: a new sister project at the foundation stage; deps is a foundation deliverable.
- **Manifest exists but is stale**: `pyproject.toml` lists deps that are 2+ majors old or unmaintained — operator wants to refresh.

Do NOT load when:

- Single dep needs upgrading or removing — load `refactor-dependencies` (audit existing graph).
- A package has a CVE — load `refactor-dependencies` (security-flagged refresh) or `infra-security` (broader audit).
- Adding a new feature that needs a new dep — load `feature-implement` and add the dep there as part of the feature.

## Operations

This skill has 4 named operations. Execute in order.

### Operation 1: Read manifest + architecture; pick versions

**Trigger**: skill loaded; operator confirmed greenfield install.

**Process**:

1. Read the project manifest:
   - **Python**: [pyproject.toml](../../../pyproject.toml) (preferred) or `setup.py` / `requirements*.txt`.
   - **Node**: `package.json` + lock file if present.
   - **Rust**: `Cargo.toml`.
   - **Go**: `go.mod`.
2. Read [docs/architecture.md](../../../docs/architecture.md) Technology Stack section. Cross-check: every tech named in architecture should be either in the manifest already OR added now. Tech in the manifest but absent from architecture is suspicious — flag for removal in Operation 4.
3. Pick the language version floor (e.g., Python 3.11+ for AICP-domain) — read from manifest's `requires-python` / engines / rust-version / go directives.
4. Categorize each dep:
   - **runtime** (`[project] dependencies` in pyproject): needed to run the app.
   - **dev/test** (`[project.optional-dependencies] dev` or similar): pytest, ruff, mypy, type stubs.
   - **build** (build-system requires): only needed at build time.
   - **dev-tool** (installed via OS pkg or separate, NOT in app deps): docker, redis-cli, etc.
5. State the install plan to the operator: language version, package manager, group breakdown. Wait for "go".

**Quality bar (Operation 1 done when)**:

- [ ] Manifest read; every dep classified into one of the 4 groups.
- [ ] Architecture cross-checked: gaps and suspicious entries flagged.
- [ ] Language version floor stated (matches manifest, not lower).
- [ ] Operator approved plan.

### Operation 2: Install with pinning

**Trigger**: Operation 1 plan approved.

**Process**:

1. Create the isolation environment:
   - **Python**: `python3 -m venv .venv` at the project root. Activate scripts in `.venv/bin/`. Add `.venv/` to `.gitignore`.
   - **Node**: nothing — `node_modules/` works in-tree (already gitignored by convention).
   - **Rust**: `target/` populated by cargo (gitignore it).
   - **Go**: module cache is per-user; nothing project-local needed.
2. Install with the right command:
   - **Python**: `.venv/bin/pip install -e ".[dev]"` (editable install + dev extras). Use `pip install --upgrade pip` first if the venv ships an old pip.
   - **Node**: `npm ci` (preferred — uses lock file) or `npm install` if lock missing.
   - **Rust**: `cargo build` populates lock + build cache.
   - **Go**: `go mod download` + `go build ./...`.
3. Ensure version pinning:
   - **Python**: `pyproject.toml` should use lower-bound pins (`>=`) for runtime deps and tighter pins for dev tools when version-fragile (`ruff>=0.4,<0.5`). For full reproducibility, add `pip-compile` / `uv` to generate a `requirements.lock`.
   - **Node**: lock file (`package-lock.json` or `yarn.lock`) IS the pinning — commit it.
   - **Rust**: `Cargo.lock` IS the pinning — commit it.
   - **Go**: `go.sum` IS the pinning — commit it.
4. Verify the lock file is committed: `git ls-files | grep -E "(lock|sum)$"` shows the right one for the language.

**Quality bar (Operation 2 done when)**:

- [ ] Isolation environment created (`.venv/` for Python, etc.) and gitignored where appropriate.
- [ ] Install command exits 0 (no warnings about missing/incompatible deps).
- [ ] Lock file generated AND committed.
- [ ] Runtime and dev/test deps in separate groups (verify by reading manifest after install — not all collapsed into one).

### Operation 3: Verify import + smoke test

**Trigger**: Operation 2 install succeeded.

**Process**:

1. Verify the package itself imports cleanly:
   - **Python**: `.venv/bin/python -c "import <main_package>; print('ok')"` — should print `ok` and exit 0.
   - **Node**: `node -e "require('<main_module>')"`.
   - **Rust**: `cargo build` (already ran; verify exit 0).
   - **Go**: `go build ./...` (verify exit 0).
2. Run any standard smoke test:
   - **AICP-domain**: `.venv/bin/aicp --check` (or `aicp --version` for fastest signal).
   - General Python: `.venv/bin/python -c "import <package>; <package>.__version__"`.
3. Run the test gate to ensure dev deps are usable:
   - Python: `.venv/bin/pytest tests/ -x --tb=short -q` (must exit 0 OR have a clear "no tests yet" output for greenfield).
4. If anything fails, the diagnostic is:
   - Wrong Python version (verify `python --version` matches `requires-python`).
   - Missing system package (e.g., `libffi-dev` for cryptography, CUDA toolkit for torch).
   - Network/proxy issue (rare; usually obvious from pip errors).

**Quality bar (Operation 3 done when)**:

- [ ] Main package imports without error.
- [ ] Project's smoke command (e.g., `aicp --check`) exits 0 (or returns expected non-zero like "LocalAI not running" — meaningful output).
- [ ] Test gate exits 0 (or "no tests collected" for true greenfield).
- [ ] Each system-level dep (CUDA, postgres-client, etc.) verified present per architecture's prerequisites.

### Operation 4: Document and clean up

**Trigger**: Operation 3 verifications passed.

**Process**:

1. Document the bootstrap in README.md (if not already present):
   ```bash
   # Quick start
   python3 -m venv .venv
   .venv/bin/pip install -e ".[dev]"
   .venv/bin/<entry-point> --check
   ```
2. Remove any deps that are in the manifest but unused (per Operation 1 cross-check). Don't leave dead deps — they accrete and slow the install.
3. Add a comment in the manifest for any non-obvious dep (e.g., `# httpx — async HTTP client, used by all backends`).
4. Suggest the next foundation skill if applicable: `foundation-config` (env vars + YAML), `foundation-testing` (pytest fixtures), `foundation-ci` (workflow that uses these deps), `foundation-docker` (containerize the runtime).

**Quality bar (Operation 4 done when)**:

- [ ] README has a clear bootstrap recipe that worked from a clean clone.
- [ ] No dead deps in manifest (verify by `pip-deptree` / `npm ls --depth=0`).
- [ ] Non-obvious deps have a one-line comment explaining purpose.
- [ ] Next-step skill suggested.

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Editable install masks missing wiring

`pip install -e .` makes the package importable from source; running tests passes. But on production (where editable install isn't used), an unwired module can fail to import because some `__init__.py` doesn't export it. Editable + dev workflow hides the issue.

**The rule**: after the editable install, also do a NON-editable install in a throwaway venv (`pip install . && python -c "import X"`) at least once to verify the package works as a wheel, not just as a source dir. Or run the wheel build path in CI.

### Gotcha 2: System deps assumed installed

Architecture says "uses CUDA"; install command runs; on a GPU-less laptop the install succeeds (because `torch` resolves to the CPU wheel) but at runtime everything's slow. Operator confused — "install worked but the GPU isn't used".

**The rule**: enumerate system-level prerequisites in README/SETUP separately from Python deps. Verify each at startup (`aicp --check` already does this for AICP). Don't conflate "Python install succeeded" with "system has the GPU/redis/postgres the deps assume".

### Gotcha 3: Missing lock file

`pip install` against unpinned deps; CI passes today; tomorrow a transitive dep ships a breaking change; CI fails for "no reason". No lock = no reproducibility.

**The rule**: every project commits a lock (`requirements.lock` for Python via pip-compile/uv, `package-lock.json` for Node, `Cargo.lock` for Rust, `go.sum` for Go). The lock is the source of truth for "what versions actually got installed". Operators reproducing locally must use the lock.

### Gotcha 4: Globally-installed dev tool drift

Operator's machine has `ruff 0.3` system-installed; project's pyproject pins `ruff>=0.4`. CI uses 0.5. Each tool gives different warnings. "Works on my machine" syndrome.

**The rule**: dev tools must come from the project's venv, not the system. Make targets call `.venv/bin/ruff` (or `python -m ruff`), not bare `ruff`. CI installs the same `[dev]` extras, so versions match.

### Gotcha 5: One-shot install hides setup hooks

`pip install` runs `setup.py install`-style hooks that download wheels, build C extensions, configure paths. If any hook silently fails (downgrades to a fallback), the result LOOKS installed but is degraded.

**The rule**: read the install output. Look for `Successfully installed <package>-<version>` for every direct dep AND for warnings about "Failed to build", "falling back to", "binary wheel not available". Treat warnings as errors during foundation-stage.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

The canonical AICP-domain dep manifest: [pyproject.toml](../../../pyproject.toml) — minimal runtime (httpx, pyyaml, rich, mcp[cli]) + `[dev]` extras (pytest, ruff, mypy). Lock generation deferred (project is currently bound to upper version flexibility on its tools).

## Domain context

This skill operates in the **backend-ai-platform-python** domain. AICP standardizes on:
- Python 3.11+ floor (per `requires-python`).
- venv at `.venv/` (gitignored).
- `pip install -e ".[dev]"` as the bootstrap recipe.
- Lock file pending — currently uses lower-bound pins; reproducibility relies on CI matching `[dev]` exactly.

Sister fleet projects in the same domain follow the same pattern.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| refactor-dependencies | Existing graph needs pruning / refresh / CVE patch | Audits + cleans; foundation-deps INSTALLS for the first time |
| foundation-config | Wire config layer once deps include the YAML lib | Different concern; related |
| foundation-testing | Set up pytest fixtures + coverage | Uses deps installed here |
| foundation-ci | Pipeline that runs the install + test commands | Runs what foundation-deps establishes |
| infra-security | Audit dep tree for CVEs | Audits security; foundation-deps is bootstrap |
