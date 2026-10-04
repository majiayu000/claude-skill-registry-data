---
name: refactor-dependencies
description: Refactor AICP's Python dependencies — audit `pyproject.toml` / `requirements.txt`, prune unused, tighten/loosen pins, replace transitive direct-dependents, isolate security-flagged packages, separate dev/test/runtime groups. Distinct from `refactor-architecture` (package layering); this skill is package-graph hygiene. Loads when the operator says "audit dependencies" / "prune unused packages" / "tighten pins" / "package X has CVE" / "split dev vs runtime deps" / "why is X in the requirements".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# refactor-dependencies

Audit and reshape AICP's Python dependency graph — what's pinned, what's
unused, what's vulnerable, what's transitive-but-should-be-direct, what
belongs in dev-only vs runtime. Produces a cleaner, smaller, more
defensible `pyproject.toml` and lock file.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "audit dependencies", "prune unused
  packages", "tighten pins", "loosen these constraints", "split dev vs
  runtime deps"
- **Security**: operator says "package X has a CVE", "rotate dependency",
  "vulnerability scan flagged Y"
- **Footprint**: operator wants to reduce install size or import time —
  inspect what's actually used vs declared
- **Discovery**: operator notices an import path they don't recognize —
  trace which dependency owns it
- **Pre-fleet rollout**: before AICP runs on N fleet machines, audit
  dependencies for stability + security

Do NOT load when:

- The concern is package-level CODE refactoring (load `refactor-architecture`)
- The concern is a NEW dependency being added for a feature (load
  `feature-implement` — adding deps is part of implementation, not
  housekeeping)
- The concern is upgrading deps for a new feature requirement (load
  `evolve-integrate` — adding capability is different from cleaning graph)

## Operations

### Operation 1 — Audit declared vs actually-used dependencies

**When**: pre-cleanup discovery — see what's in pyproject.toml/requirements
that isn't actually imported anywhere in `aicp/`.

**Process**:

1. Read declared deps: `pyproject.toml` (project.dependencies +
   project.optional-dependencies)
2. Find imports across `aicp/` and `tests/`:
   `Grep -E "^(from|import) [a-z_][a-z0-9_]*" --type py`
3. Map each import to its owning package (e.g., `httpx` → `httpx`,
   `from rich.table import Table` → `rich`)
4. Compare: declared but not imported = candidates for removal
5. Imported but not declared = HIDDEN transitive deps (someone else
   pulled them in); these need to become direct or be replaced

**Quality bar**: a "candidate for removal" needs verification — sometimes
a dep is loaded dynamically (e.g., `importlib`), or used only in a
`try: import X` fallback path. Verify before removing.

### Operation 2 — Prune unused dependencies

**When**: Operation 1 produced a verified list of unused packages.

**Process**:

1. Remove from `pyproject.toml` `project.dependencies`
2. If using a lock file (e.g., `uv.lock` or `poetry.lock`), regenerate
3. Run `pytest` — must pass with zero changes (if a test fails, the
   package was actually used; restore)
4. Run `aicp --check` to verify CLI still loads
5. Document the removals (commit message + entry in
   `wiki/decisions/00_inbox/` if removing a "load-bearing" looking dep)

**Quality bar**: NEVER prune without running pytest. The verification
gate catches dynamically-imported deps that grep-based audits miss.

### Operation 3 — Tighten or loosen version pins

**When**: pin policy needs adjustment — too loose causes incompatible
upgrades, too tight blocks security patches.

**Process**:

1. Identify the pin policy intent: production (tight) vs library (loose)
2. AICP is a product (per CLAUDE.md `## Identity Profile` Type=product),
   so pins should be RELATIVELY tight (e.g., `>=X.Y.Z,<X.(Y+1)` or
   `~=X.Y` patch-level) for runtime deps; dev deps can be looser
3. Edit `pyproject.toml` per package
4. Regenerate lock file
5. Run pytest + `aicp --check` to verify the new pins resolve

**Quality bar**: NEVER pin to exact versions (e.g., `==X.Y.Z`) for runtime
deps unless investigating a specific bug. Exact pins block transitive
security upgrades.

### Operation 4 — Separate dev vs test vs runtime groups

**When**: dev-only or test-only deps are leaking into the runtime install.

**Process**:

1. Inspect current `pyproject.toml` structure — look for
   `project.optional-dependencies` groups (typical: `dev`, `test`,
   `lint`)
2. Re-categorize each declared dep:
   - Runtime (imported in `aicp/`, not in `tests/`): stays in
     `project.dependencies`
   - Test-only (imported only in `tests/`): move to `[project.optional-dependencies] test`
   - Dev-only (used by tooling, not imported): move to
     `[project.optional-dependencies] dev`
3. Update install instructions (Makefile, README, CI config) to use
   `pip install -e ".[dev,test]"` for dev environments
4. Verify CI still passes (CI install command may need update)

**Quality bar**: a fresh `pip install aicp` (no extras) should produce a
working AICP CLI. If something breaks, a runtime dep was misclassified
as dev/test.

### Operation 5 — Address a security-flagged dependency

**When**: a CVE or security advisory implicates a dep.

**Process**:

1. Identify the affected version range
2. Check for an upgrade: `pip index versions <package>` — is there a
   patched version compatible with the existing constraint?
3. If yes: bump pin in `pyproject.toml`, regenerate lock, run pytest
4. If no patched version exists yet: assess workarounds — disable the
   feature using the dep, or temporarily replace with a fork/alternative
5. Document the decision in `wiki/decisions/00_inbox/<cve-id>-response.md`
   (per Knowledge Evolution Standards — even short security responses
   benefit from a decision record)

**Quality bar**: NEVER ignore a CVE. If no patch exists, document the
risk acceptance + monitoring plan.

## Gotchas

- **Detection**: agent uses Bash `pip install -X` directly without updating pyproject.toml.
  **Rule**: dependency changes go through `pyproject.toml` first, then
  `pip install -e .` to reflect.
  **Reasoning**: ad-hoc pip installs don't survive environment recreation
  and produce silent drift between dev environments and CI.

- **Detection**: agent removes a dep without running pytest.
  **Rule**: every removal runs through pytest before declaring done.
  **Reasoning**: dynamically-imported deps (`importlib`, `try: import X`
  fallbacks) won't show in `Grep` audits. The test suite catches them
  if test coverage is reasonable.

- **Detection**: agent pins all deps to exact versions.
  **Rule**: use range pins (`~=X.Y`, `>=X,<X+1`) for runtime; only exact
  pin when investigating a specific bug.
  **Reasoning**: exact pins block transitive security upgrades and
  produce unfixable supply-chain risk.

- **Detection**: agent moves a runtime dep to the `[dev]` group "to clean up".
  **Rule**: only move to dev IF the dep is genuinely not imported in `aicp/`.
  Verify with `Grep` first.
  **Reasoning**: misclassifying a runtime dep as dev breaks `pip install
  aicp` (no extras) for end users — they get an ImportError they can't
  diagnose.

- **Detection**: agent skips lock file regeneration after pyproject.toml change.
  **Rule**: if a lock file exists (uv.lock, poetry.lock, requirements.lock),
  regenerate after every dep change.
  **Reasoning**: lock files are the reproducibility floor; stale locks
  produce divergence between developers and CI.

## Reference exemplars

- `pyproject.toml` — AICP's declared dependencies + extras groups
- `aicp/backends/localai.py` — uses `httpx` (runtime dep), motivates
  HTTP client choice
- `aicp/cli/main.py` — uses `rich` heavily for Tables/Console (runtime)
- `tests/conftest.py` — uses `pytest` fixtures (test-only)
- `wiki/decisions/01_drafts/localai-over-ollama-vllm-for-multi-model-orchestration.md`
  — example of a dependency-shaping decision documented

## Domain context

AICP runs as a Python 3.11+ product on Linux/WSL2. Dependencies
include: `httpx` (HTTP client), `rich` (CLI styling), `pyyaml` (config
parsing), `mcp` (MCP server framework), `chromem` or similar (vector
store via LocalAI), pytest + ruff (dev/test). The `pyproject.toml` is
the source of truth; CI installs via `pip install -e ".[dev,test]"`.

## Related skills

| Skill | When to use |
|-------|-------------|
| `refactor-architecture` | When the dep structure reflects a package-level architecture issue |
| `infra-security` | When the audit is part of a broader security posture review |
| `quality-debt` | When dep cleanup is part of debt inventory |
| `feature-implement` | When ADDING a dep for a new feature (different from cleaning) |
| `evolve-integrate` | When adding a dep to integrate a NEW capability |
