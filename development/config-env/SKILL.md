---
name: config-env
description: Manage AICP's per-environment configuration — environment variables (`.env`, `AICP_*` family), config file overlays (default → profile → ~/.aicp/config.yaml → project .aicp/config.yaml → --config), per-environment profile selection (dev / staging / prod). Distinct from `config-secrets` (secrets specifically) and `config-deploy` (deployment-time profile selection); this skill is the broader env-var + config-file lifecycle. Loads when the operator says "set env var X" / "add a config" / "what env vars does AICP read" / "different config for dev vs prod" / "override config X for this run".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: low
---

# config-env

Manage AICP's environment-variable + config-file lifecycle. AICP loads
config from a 5-tier overlay (default.yaml → profile → user → project →
CLI), with `AICP_*` env vars overriding select keys. This skill is the
operational surface for "what env vars exist", "how do I override X for
this environment", and "how does the overlay resolve".

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "set env var X", "add a config", "what
  env vars does AICP read", "different config for dev vs prod", "override
  config X for this run"
- **Discovery**: operator wants to know which env vars AICP responds to
  (e.g., `AICP_DEFAULT_MODE`, `AICP_DEFAULT_BACKEND`, `AICP_PROJECT_PATH`,
  `LOCALAI_BASE_URL`, etc.)
- **Multi-environment setup**: prepare separate configs for dev / staging /
  production runs
- **Config debugging**: operator sees unexpected behavior — trace which
  overlay tier supplied the offending value

Do NOT load when:

- The concern is secrets specifically (load `config-secrets` for token
  rotation, .env hygiene)
- The concern is deployment-time profile activation (load `config-deploy`
  for the deploy-time workflow)
- The concern is profile DEFINITION (load `feature-document/feature-plan`
  if proposing a new profile YAML)

## Operations

### Operation 1 — Discover all AICP env vars

**When**: operator wants the complete inventory of env vars AICP reads.

**Process**:

1. Search the codebase: `Grep -nE "os\.environ\.get\(.AICP_|os\.environ\.get\(.LOCALAI_|os\.environ\.get\(.OPENROUTER_|os\.environ\.get\(.ANTHROPIC_|os\.environ\.get\(.HUGGINGFACE_"`
2. Categorize by purpose:
   - `AICP_*` — AICP's own runtime overrides (default mode, default
     backend, project path, profile)
   - `LOCALAI_*` — LocalAI backend connection
   - `OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`, `HUGGINGFACE_TOKEN` —
     cloud backend secrets
   - `NO_COLOR` — rich library standard
3. Cross-reference with `.env.example` (if present) to verify all are
   documented
4. Report any env vars referenced in code but missing from `.env.example`

**Quality bar**: every env var the code reads should be discoverable
from `.env.example` so operators know what to set without reading source.

### Operation 2 — Create or update an environment-specific config overlay

**When**: operator wants a different config for dev vs staging vs prod.

**Process**:

1. Identify the overlay tier per AICP's load order (CLAUDE.md `## Configuration Profiles → Config load order`):
   - `config/default.yaml` — base, always loaded
   - `config/profiles/<name>.yaml` — profile overlay (use this for
     environment-specific changes)
   - `~/.aicp/config.yaml` — user-global override (rarely needed)
   - `<project>/.aicp/config.yaml` — project override
   - `--config <path>` CLI override (per-invocation)
2. Per-environment changes typically live in `config/profiles/`:
   - `config/profiles/dev.yaml` — relaxed timeouts, verbose logging
   - `config/profiles/staging.yaml` — production-like with safety margins
   - `config/profiles/prod.yaml` — locked-down (use the existing
     `reliable.yaml` as starting point)
3. Activate via `aicp --profile <name>` or `make profile-use PROFILE=<name>`

**Quality bar**: NEVER edit `default.yaml` for environment-specific
changes — that pollutes the base. Use the profile overlay tier.

### Operation 3 — Trace which overlay supplied a value

**When**: operator sees unexpected config behavior — debug which tier
provided the value.

**Process**:

1. Run `aicp --profile-cmd show` to see the resolved config (per profile
   diff is also useful: `aicp --profile-cmd diff`)
2. The output shows the merged final config; the operator infers the
   source from comparison with default.yaml + the active profile yaml
3. For deeper trace: walk the load order manually:
   - Read `config/default.yaml`
   - Read `config/profiles/<active>.yaml`
   - Read `~/.aicp/config.yaml` if present
   - Read `<project>/.aicp/config.yaml` if present
   - Note: env vars override at the LOADER stage (AICP-specific keys);
     `aicp/config/loader.py` has the precedence logic
4. The first tier that defines the key wins (highest-precedence
   overlay)

**Quality bar**: the resolved config from `--profile-cmd show` is the
ground truth. If runtime behavior contradicts it, there's a bug —
investigate the loader, not the YAML.

### Operation 4 — Add a new env var to AICP's config protocol

**When**: a new feature needs an operator-tunable knob.

**Process**:

1. Decide if a CONFIG KEY is sufficient (preferred — version-controlled,
   profile-scoped) or an ENV VAR is needed (preferred when the value is
   secret-like or per-environment without a profile)
2. If env var: add reading code with sane default:
   `os.environ.get("AICP_<NAME>", "<default>")`
3. Add to `.env.example` with a comment explaining purpose + default
4. Add documentation: a row in CLAUDE.md or AGENTS.md describing the env
   var's role
5. If the env var has security implications, also load `config-secrets`
   and `infra-security` skills for review

**Quality bar**: NEVER read an env var without adding it to `.env.example`.
Undocumented env vars are an operational landmine — operators have no
way to know they exist.

## Gotchas

- **Detection**: agent edits `config/default.yaml` for a per-environment change.
  **Rule**: per-environment changes go in profile overlays, not default.
  **Reasoning**: `default.yaml` is the base for ALL environments; editing
  it for one environment leaks the change into all profiles.

- **Detection**: agent reads an env var without adding to `.env.example`.
  **Rule**: every env var AICP reads must be documented in `.env.example`.
  **Reasoning**: undocumented env vars are silent landmines — operators
  can't discover them without grepping source.

- **Detection**: agent confuses config tiers — overrides .env when they
  meant project config (or vice versa).
  **Rule**: read CLAUDE.md `## Configuration Profiles → Config load order`
  before any tier choice.
  **Reasoning**: AICP's 5-tier overlay has specific precedence. Wrong-tier
  edits don't take effect.

- **Detection**: agent puts a secret in a profile YAML.
  **Rule**: secrets go in `.env` (gitignored); profile YAMLs are
  version-controlled.
  **Reasoning**: profile YAMLs commit to git; secrets in committed files
  are immediately leaked.

- **Detection**: agent overrides global `~/.aicp/config.yaml` for a one-off run.
  **Rule**: one-off overrides use `--config <path>` CLI flag, not user-global.
  **Reasoning**: user-global affects every project; CLI overrides are
  scoped to the invocation.

## Reference exemplars

- `aicp/config/loader.py` — load order implementation (5-tier overlay)
- `config/default.yaml` — base config
- `config/profiles/default.yaml`, `reliable.yaml`, `dual-gpu.yaml` — profile examples
- `.env.example` — env var documentation (if present; otherwise operator should request creation)
- `aicp/cli/main.py` — env var reads (AICP_DEFAULT_MODE, AICP_DEFAULT_BACKEND, AICP_PROJECT_PATH)

## Domain context

AICP loads config from a 5-tier overlay:
`default.yaml → profile → ~/.aicp/config.yaml → <project>/.aicp/config.yaml → --config`.
Env vars provide a sixth dimension at the loader level for select keys
(mostly mode, backend, project path, base URLs). Profile activation is
operator-controlled via `aicp --profile <name>` (per-invocation),
`AICP_PROFILE` env var (per-shell), or `make profile-use PROFILE=<name>`
(persistent in .env).

## Related skills

| Skill | When to use |
|-------|-------------|
| `config-secrets` | When the concern is secrets specifically (.env, tokens, rotation) |
| `config-deploy` | When the concern is deployment-time profile selection |
| `config-feature-flags` | When the concern is per-feature toggle (different from per-env config) |
| `config-migrations` | When the concern is migrating config schema across versions |
| `infra-security` | When new env vars have security implications |
