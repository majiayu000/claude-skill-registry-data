---
name: config-and-flags
description: Treat configuration and feature flags as typed, validated inputs with a lifecycle — read once at startup, parse to types, fail fast on missing or malformed values, no scattered env reads or environment-name branching, flags default safe and get removed. Use when adding or reading an env var, config key, settings file, or feature flag; when behaviour differs per environment; when a value "will be set in prod"; and when reviewing code that calls process.env, os.environ, getenv, or a flag client.
---

# config-and-flags

Weak configuration is `process.env.TIMEOUT || 30` sprinkled across twelve files, a boolean read as the string `"false"`, and a feature flag from two years ago nobody dares delete. Strong configuration is one place that reads, validates, and types every external value at startup, fails loudly when something is missing, and treats every flag as a temporary branch with an owner and an exit condition.

## 1. One entry point, read at startup

- Find where the project already loads config (grep `process.env`, `os.environ`, `getenv`, `BaseSettings`, `dotenv`, `viper`, a `config/` dir). Add your key there; never read the environment at the call site.
- Load and validate at process start, not on first use. A missing value should fail the boot, not the 3am request that first reaches that branch.
- Every key has a name, a type, required-or-default, and one line saying what it controls. If the project has a schema (zod, pydantic, JSON schema), the key goes in it. If it has `.env.example` or a config table in the docs, update that in the same diff.

## 2. Parse to a type, never string-compare

- Env vars are strings. `if (process.env.ENABLED)` is true for `"false"`, `"0"`, and `"no"`. Parse explicitly: booleans through an allowlist of spellings, numbers with a range check, URLs by parsing, enums by allowlist, durations with the unit in the name (`TIMEOUT_MS`, not `TIMEOUT`).
- Reject malformed values at load with a message naming the key, the value, and the accepted forms (see error-message-quality). Silent fallback to the default on a typo is the bug that survives to production.
- Secrets are config but never defaults: no fallback value for a credential, never logged, never in the client bundle (see security-reflexes).

## 3. Defaults are a decision

- Default to the least-privileged, least-surprising behaviour: off, small, safe. Requiring an explicit value in production is fine; document that it is required.
- Never silently default something the operator must set. `DATABASE_URL || "sqlite://dev.db"` means a misconfigured production server writes to a local file and reports success.
- Environment-specific values live in per-environment config, not in `if (NODE_ENV === "production")` inside business logic. Branching on the environment name hides which behaviour the tests exercise; branch on the specific config value.

## 4. Feature flags have a lifecycle

- Before adding a flag, name its kind: gradual rollout, kill switch, experiment, or long-lived operator toggle. Only the last is permanent; the others get a removal condition written beside the definition ("remove after 100% for two weeks").
- Default off. Code behind a flag changes nothing for anyone until the flag is flipped.
- Evaluate once per request or unit of work and pass the result down. Evaluating inside a loop or in several places lets a mid-request flip produce a mixed state.
- Both branches are tested: the guarded code runs with the flag on and off, and the off path still passes after the on path was added.
- Removing a flag deletes the dead branch, the definition, the config entry, and the off-path tests in one commit (see surgical-refactoring).

## 5. Exercise the config path

Before done, start the process three ways — key unset, key malformed, key set to the intended value — and paste what happened each time. Then confirm the key is reachable everywhere it is needed: CI secrets, deploy manifests, `.env.example`. A key set locally and nowhere else is "works on my machine" with a delay.

## Reporting

List every key added or changed: name, type, required or default, where it is read, and which environments now need it set. List every flag added with its kind and removal condition.
