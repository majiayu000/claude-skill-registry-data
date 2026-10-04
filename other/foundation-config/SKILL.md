---
name: foundation-config
description: Set up configuration management with multi-environment support — author the config schema (typed object), the loader with precedence chain, the `.env.example` placeholder file, the `.gitignore` rules, and startup validation. Loads when a project has no config layer yet, or when the operator says "set up config", "add multi-env support", "wire env vars", "we need a config loader".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# foundation-config

The foundation skill that authors a project's configuration system. AICP's pattern (per [aicp/config/loader.py](../../../aicp/config/loader.py)) is the canonical reference: YAML overlays + env-var overrides + typed access via `get_backend_config()`. Sister fleet projects use the same shape.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **No config exists**: project has no config loader, no `.env.example`, no `config/*.yaml`. Operator wants to bootstrap.
- **Direct verb**: operator says "set up config", "add multi-env support", "wire env vars", "we need a config loader", "where do settings live".
- **Foundation-stage of project-lifecycle**: a new sister project at the foundation stage; config is one of the foundation deliverables.
- **Single-config-bloat**: project has all settings hardcoded or in one giant `.env` and operator wants real environment separation (dev/staging/prod).

Do NOT load when:

- Config layer exists; you're adding a new key — load `config-env` (env-var lifecycle within existing system).
- Adding/rotating a secret — load `config-secrets`.
- Schema-evolving an existing config (rename keys, change shapes) — load `config-migrations`.
- Choosing which profile to use at deploy time — load `config-deploy`.
- Adding a feature flag — load `config-feature-flags`.

## Operations

This skill has 4 named operations. Execute in order.

### Operation 1: Read architecture and decide the config shape

**Trigger**: skill loaded; operator confirmed greenfield config layer.

**Process**:

1. Read [docs/architecture.md](../../../docs/architecture.md) (and any existing CLAUDE.md identity profile) to identify what config keys the system needs. Categorize:
   - **Backend connection details** (URLs, API base paths, ports).
   - **Credentials/secrets** (API keys, JWT secrets, passwords) — these go in `.env`, NOT YAML.
   - **Operational tuning** (timeouts, retries, batch sizes, thread counts).
   - **Feature toggles** (enabled flags).
   - **Per-environment overrides** (dev/staging/prod).
2. Decide the precedence chain. AICP-domain default (mirror this unless reason to deviate):
   ```
   config/default.yaml          (committed baseline)
   → config/profiles/<name>.yaml (committed profile overlay)
   → ~/.aicp/config.yaml         (operator user-level override, gitignored)
   → <project>/.aicp/config.yaml (per-project override, gitignored)
   → --config <path>             (CLI override)
   → environment variables       (per-process override)
   ```
3. Decide whether you need YAML profiles (multi-env separation) or just env vars. Rule of thumb: if more than ~5 settings change per environment, use YAML profiles; if fewer, env vars are enough.
4. State the plan: precedence chain / YAML vs env-only / list of categories. Wait for "go".

**Quality bar (Operation 1 done when)**:

- [ ] All config keys categorized into the 5 buckets (connection / secret / tuning / toggle / per-env).
- [ ] Precedence chain decided and documented.
- [ ] YAML-vs-env-only decision made with rationale.
- [ ] Operator approved.

### Operation 2: Author the schema and loader

**Trigger**: Operation 1 plan approved.

**Process**:

1. Author a typed config schema. Two viable patterns:
   - **dataclass-based** (AICP's choice): a `dataclass` per logical section (`@dataclass class BackendConfig: ...`). Type hints on every field. Validation in `__post_init__`.
   - **pydantic-based**: subclass `BaseSettings`. Auto-validates. More magic, more surface.
   Pick dataclasses unless the project already uses pydantic.
2. Author the loader (mirror AICP's `aicp/config/loader.py` shape):
   ```python
   def load_config(override_path: Path | None = None) -> dict[str, Any]:
       """Layered load: default → profile → ~/.aicp → project → override → env."""
       config = _load_yaml(DEFAULTS_PATH)
       if profile := os.environ.get("AICP_PROFILE"):
           config = _deep_merge(config, _load_yaml(profiles_path(profile)))
       config = _deep_merge(config, _load_yaml(USER_HOME_CONFIG))
       config = _deep_merge(config, _load_yaml(PROJECT_CONFIG))
       if override_path:
           config = _deep_merge(config, _load_yaml(override_path))
       config = _apply_env_overrides(config, prefix="<APP>_")
       return config
   ```
3. Author startup validation: every required key has either a default OR a clear failure message. Validate at `load_config()` exit, not at first use ("fail fast" — surface misconfig at startup, not 30 minutes later mid-task).
4. Author `.env.example` listing every env var the loader reads, with comments per var explaining purpose, default, and where to get the value (link to the upstream docs for API keys).
5. Add `.env` to `.gitignore`. Add `~/.aicp/config.yaml` and any operator-personal config to `.gitignore` if applicable.

**Quality bar (Operation 2 done when)**:

- [ ] Typed schema authored (dataclass or pydantic — not raw dicts at usage sites).
- [ ] Loader implements the precedence chain decided in Operation 1.
- [ ] Validation runs at load time and produces actionable errors (which key missing, where to set it).
- [ ] `.env.example` lists every env var with purpose + default + source-of-value comment.
- [ ] `.env` and any user-personal config in `.gitignore`.
- [ ] No literal secret values committed (`grep -rE "API_KEY\s*=\s*['\"][a-zA-Z0-9]{20,}" .` returns nothing).

### Operation 3: Wire the loader into the runtime

**Trigger**: Operation 2 schema and loader landed.

**Process**:

1. Identify the entry points that need config (CLI main, server boot, MCP server, agent server). Each one calls `load_config()` once at startup, passes the resulting object/dict to downstream code.
2. Replace any existing hardcoded values with config lookups. Keep the change scoped — don't refactor unrelated code.
3. For each call site that reads a config field, prefer the typed accessor (`config.backends.local.base_url`) over raw dict access (`config["backends"]["local"]["base_url"]`) — typed access fails at lint/type-check, raw dict fails at runtime.
4. Provide a sensible startup-error format: `Error: required config 'backends.local.base_url' is missing. Set in config/default.yaml or env LOCAL_BASE_URL.` Vague errors mean operators page you for trivia.

**Quality bar (Operation 3 done when)**:

- [ ] All entry points call `load_config()` once at startup.
- [ ] No hardcoded values that should be config (verify by grep for IP/URL/port/timeout literals).
- [ ] Errors at startup name the missing key AND where to set it.
- [ ] Typed access at use sites; no raw `config["..."]["..."]` chains.

### Operation 4: Document and test

**Trigger**: Operation 3 wiring landed.

**Process**:

1. Document the config system in README (or `docs/configuration.md` for richer surfaces):
   - Precedence chain diagram.
   - List of profiles (if YAML profiles).
   - How to override for local dev (`~/.aicp/config.yaml` example).
   - Env-var reference table.
2. Author tests:
   - `test_load_config_defaults`: load with no overrides, verify expected values.
   - `test_profile_override`: profile YAML overrides defaults.
   - `test_env_override`: env var overrides YAML.
   - `test_missing_required_fails`: load fails with actionable error.
   - `test_precedence_order`: assert env > project YAML > profile > default.
3. Run the project's standard test gate (AICP-domain: `pytest tests/test_config*.py -x`).
4. Suggest the next foundation skill if applicable: `foundation-deps` (install dependencies the config system uses), `config-secrets` (set up specific secrets).

**Quality bar (Operation 4 done when)**:

- [ ] Config system documented in README/docs with precedence chain and env-var reference.
- [ ] ≥5 tests covering: defaults, profile override, env override, missing-required, precedence order.
- [ ] Test gate exits 0.
- [ ] Next-step skill suggested.

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Secret in YAML

`config/default.yaml` contains `anthropic_api_key: sk-ant-...`. Committed to git. Once in history, compromised forever — even after rotation, anyone with old commits can use the old key.

**The rule**: secrets ONLY in `.env` (gitignored) or external secret store. YAML files have NO secret values, only references like `api_key_env: ANTHROPIC_API_KEY` (the env-var NAME, not the value). Verify on every commit: `git diff --cached | grep -E "(api_key|secret|password|token)\s*[:=]\s*['\"]?[a-zA-Z0-9]{20,}"` — empty result is the bar.

### Gotcha 2: Late validation

Loader returns OK; the missing required key is only detected when feature X tries to use it 30 minutes into a session. Operator gets a `KeyError` deep in a stack trace; spends 20 minutes finding the actual config issue.

**The rule**: validate at `load_config()` exit, BEFORE the first use site. Walk the schema, check every required field. If any missing, raise a single error listing all missing keys and where to set each.

### Gotcha 3: Raw dict access at use sites

Code reads `config["backends"]["local"]["base_url"]`. Refactor renames the key. Lint passes. Tests pass (because tests use the same raw dict). Production fails at first request.

**The rule**: typed accessors at use sites. Either dataclass `config.backends.local.base_url` (raises AttributeError at the use site, easier to find) or a typed wrapper. Raw dict access is allowed only inside the loader itself.

### Gotcha 4: Precedence-order surprise

Operator expects env vars to override everything. Loader implements env vars BEFORE project YAML. Operator sets env, restarts, sees the YAML value still applied. Spends an hour debugging.

**The rule**: env override is the LAST step in the precedence chain. Document the order explicitly in README. Test it (`test_precedence_order`). When in doubt, env wins — that's what operators reach for in incidents.

### Gotcha 5: `.env` not in `.gitignore`

`.env` with real keys gets committed in the first push. Visible to anyone who clones the repo (including bots scanning GitHub). Discovered when the keys start showing unexpected usage.

**The rule**: add `.env` to `.gitignore` BEFORE you create `.env`. Provide `.env.example` (committed, no secrets) as the template. Verify: `git check-ignore .env` should return `.env` (meaning yes, ignored).

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

The canonical AICP-domain config reference: [aicp/config/loader.py](../../../aicp/config/loader.py) (~150 lines, layered YAML + env, typed access via `get_backend_config()`, profile system at [aicp/core/profiles.py](../../../aicp/core/profiles.py)).

## Domain context

This skill operates in the **backend-ai-platform-python** domain. AICP's existing config layer ([config/default.yaml](../../../config/default.yaml) + 11 profiles + [aicp/config/loader.py](../../../aicp/config/loader.py)) is the canonical pattern this skill builds on for sister projects. See [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml) for stage gates.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| config-env | Add a single env var to existing config | foundation-config AUTHORS the system; config-env modifies it |
| config-secrets | Add or rotate a secret | foundation-config wires the loader; config-secrets manages secret values |
| config-deploy | Pick a profile at deploy time | foundation-config defines profiles; config-deploy selects one |
| config-feature-flags | Add a feature toggle | foundation-config provides the toggle plumbing; config-feature-flags uses it |
| config-migrations | Schema evolution (rename keys, etc.) | foundation-config authors v1; config-migrations evolves to v2 |
| foundation-deps | Install dependencies the config uses | foundation-config calls a YAML lib; foundation-deps installs it |
