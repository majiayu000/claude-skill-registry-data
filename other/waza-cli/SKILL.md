---
name: waza-cli
description: Drive the waza CLI (microsoft/waza) — the default skill-evaluation tool for this workspace — to check skill readiness for free (waza check, waza tokens), run behavioral eval suites with LLM graders, compare models A/B, measure quality with an LLM judge, and gate regressions in CI. Use when checking a skill before submission, running evals, comparing models, or auditing eval coverage. Do NOT use for post-hoc real-session efficiency telemetry (what a skill actually burned when it ran) — that is the copilot-session-telemetry skill (formerly agentic-workflow-benchmark), whose findings hand off here for eval refinement.
metadata:
  version: 0.2.0
---

# Waza CLI Evaluation

Run [waza](https://github.com/microsoft/waza) commands against a skill dir. Install via [release binary](https://github.com/microsoft/waza) (`install.ps1` / `install.sh`) or `go install github.com/microsoft/waza@latest`; update in place with `waza update`. Verified against **waza v0.38.10** (Oct 2026) — commands documented only on waza's `main` docs but not yet released (`preflight`, `new eval --scenario`) are marked ⚠️ *upcoming*; confirm with `waza <cmd> --help` before use.

USE FOR: check my skill, run my evals, compare models, gate CI regressions, score skill quality, find eval coverage gaps. DO NOT USE FOR: first-draft authoring (use skill-creator); **real-session efficiency telemetry** (use the `copilot-session-telemetry` skill).

## Choose the command

| Goal | Command |
|------|---------|
| Readiness, compliance, token budget | `waza check <skill-dir>` |
| Token audit / optimization | `waza tokens check`, `waza tokens suggest` |
| LLM-judge quality (5 dimensions) | `waza quality <skill-dir>` |
| Behavioral eval, real execution | `waza run <eval.yaml>` |
| Model A/B comparison | `waza run --baseline` |
| Eval coverage grid (which skills have evals) | `waza coverage` |
| Coverage vs SKILL.md requirements | `waza spec verify` |
| Adversarial / fault-injection packs | `waza adversarial` |
| CI regression gate | `waza gate` |
| Determinism check | `waza snapshot` + `waza replay` |
| Offline eval preflight (no agent) | ⚠️ *upcoming* — `waza preflight <eval.yaml>` |

## Runtime environment (CLI, COPILOT_HOME, BYOK)

### Default: waza's bundled Copilot CLI

With `COPILOT_CLI_PATH` unset, waza spawns its **bundled CLI** (e.g. v1.0.85 on waza 0.38.7 — the exact pin travels with each release, see [copilot-cli-resolution.md](references/copilot-cli-resolution.md)). This is the recommended default for eval: it is the exact CLI version waza was built and tested against, giving reproducible results across machines and CI runs.

**Do not set `COPILOT_CLI_PATH` by default.** The resolver script is an **opt-in override** for when you need a specific machine CLI (e.g., testing a feature only in a newer release). Machine-default is risky: it varies by box (1.0.92 on WinGet, 1.0.80 on npm-first) and may be newer than waza tested, with no version-compatibility check.

### Isolate COPILOT_HOME

waza does **not** modify `COPILOT_HOME` — it passes through to the CLI child process. If `COPILOT_HOME` is already set (e.g., `~/.copilot`), every eval run writes sessions and extracts the embedded CLI there. Set an isolated dir for eval:

```powershell
$env:COPILOT_HOME = "$env:USERPROFILE\.copilot-waza"  # or a temp dir
```

This redirects both eval session data and the embedded CLI extraction. Your main `.copilot` stays clean. See [copilot-cli-resolution.md](references/copilot-cli-resolution.md) for details.

**Important ordering:** BYOK profiles are stored in `$COPILOT_HOME/byok-profiles.json`. Select the profile **before** switching `COPILOT_HOME` to the isolated dir — otherwise the wizard/list will find zero profiles.

### Update check

waza performs a **background version check** after every command and prints an update notice if a new version is available (e.g., "A newer version of waza is available: v0.38.7 → v0.38.10"). The check runs in a goroutine but `Result()` blocks up to **100ms** synchronously, and the GitHub API call is cached for **24h**. This is low-overhead but not zero — no additional LLM tokens, but a small network call and sync wait on each invocation. **Do not add a separate update-check mechanism** to the skill; rely on the built-in notice.

For skill updates: re-run the workspace publish flow from the source (`scripts/publish/`, or the skills CLI). No runtime check is needed.

### BYOK mode (no Copilot subscription)

This workspace uses **BYOK** (Bring Your Own Key) by default — no Copilot subscription. waza's copilot-sdk executor passes the parent environment to the CLI child process, so BYOK provider vars set before `waza run` are inherited automatically. See the [copilot-byok](../copilot-byok/SKILL.md) skill for profile management and the full env-var reference.

**Mandatory profile gate:** Before running `waza run` or `waza quality`, you **must** stop and ask which BYOK profile to use — unless the user's prompt explicitly specifies a profile name (e.g., "use ollama profile", "run with opencode-go"). This is a hard requirement: never auto-select or assume a default profile.

**Two selection paths:**

1. **Interactive wizard** (recommended for terminal use) — dot-source with `-i` to launch the account-first picker. The wizard handles account scoping, disabled profiles, and `--account` auto-addition. Env vars are set in the current shell:
   ```powershell
   . skills/copilot-byok/scripts/byok-profile.ps1 set-env -i
   # → pick account (or skip) → pick profile → env vars applied to current shell
   ```
   **Note:** The wizard uses `Read-Host` for input and requires a real terminal. It will **not** work from the powershell tool (which doesn't support interactive input). Use the `ask_user` path below when running from a Copilot session.

2. **Copilot `ask_user`** (for automated selection) — list profiles, present them via `ask_user`, then apply:
   ```powershell
   $profiles = & skills/copilot-byok/scripts/byok-profile.ps1 list
   # → ask_user with the profile list as enum options
   . skills/copilot-byok/scripts/byok-profile.ps1 set-env <selected-profile>
   ```

**If no profiles exist:** The agent should ask the user to either create a profile (`byok-profile.ps1 add`) or specify provider details inline (base URL, model, API key).

**Wizard cancellation:** Press `q` at any menu to cancel cleanly. If the wizard is cancelled, fall back to `ask_user` or ask the user directly.

**Critical ordering:** Select the profile **before** switching `COPILOT_HOME` to the isolated dir. BYOK profiles are stored in `$COPILOT_HOME/byok-profiles.json` — if `COPILOT_HOME` is already set to the isolated dir, the wizard/list will find zero profiles.

Both paths converge on:
```powershell
# 1. Apply profile (COPILOT_HOME still points to main .copilot)
. skills/copilot-byok/scripts/byok-profile.ps1 set-env <profile>

# 2. Switch to isolated home for eval
$env:COPILOT_HOME = "$env:USERPROFILE\.copilot-waza"

# 3. Run waza
waza run skills/<name>/eval.yaml
```

Key BYOK env vars (see [copilot-byok environment-variables](../copilot-byok/references/shared/environment-variables.md) for full reference):
- `COPILOT_PROVIDER_BASE_URL` — provider endpoint
- `COPILOT_MODEL` — model identifier
- `COPILOT_PROVIDER_TYPE` — `openai` (default), `azure`, or `anthropic`
- `COPILOT_PROVIDER_API_KEY` — API key (omit for unauthenticated providers)
- `COPILOT_PROVIDER_WIRE_API` — `completions` (default) or `responses`
- `COPILOT_OFFLINE` — set `true` to prevent GitHub server contact

Note: the isolated `COPILOT_HOME` won't have your existing CLI auth. With BYOK this is fine — auth flows through `COPILOT_PROVIDER_*` vars, not CLI login.

## Quick recipes

```bash
waza check skills/<name>           # offline, no LLM cost
waza tokens check                  # token budgets across the workspace
waza tokens suggest skills/<name>
waza coverage                      # which skills have evals
waza spec verify skills/<name>     # eval coverage vs SKILL.md requirements

waza run skills/<name>/eval.yaml   # needs BYOK provider vars + isolated COPILOT_HOME (see above)
waza run --baseline skills/<name>/eval.yaml

waza gate --baseline baseline.json --current results.json
```

If `waza check` flags the 500-token budget on a large skill, set `tokens.limits.defaults` (a glob → limit map) in `.waza.yaml` — see [eval format reference](references/waza-eval-format.md#token-budget-override). Never use `tokens.limits.max`: it is not a schema key and makes `waza check` fail with `field max not found in type projectconfig.TokenLimitsConfig`.

## Decision rule

Run the zero-cost commands first — `waza check`, `waza tokens check`, and `waza coverage` are offline (no LLM cost). Escalate to `waza quality`, `waza run`, or `waza gate` only when real model execution is needed (the BYOK profile gate above applies).

Related skills: **real-session efficiency telemetry** (tokens/time/steps a finished run actually burned, plus waza-ready evidence for eval refinement) → the `copilot-session-telemetry` skill (formerly `agentic-workflow-benchmark`). `skill-eval` is deprecated — do not use it.

Read references when needed:
- [Eval format and graders](references/waza-eval-format.md) — authoring eval.yaml, task YAML, trigger tests
- [Full command surface](references/waza-commands.md) — flags/subcommands not covered above
- [CI integration](references/waza-ci.md) — wiring `waza gate`/`waza run` into GitHub Actions
- [Copilot CLI resolution](references/copilot-cli-resolution.md) — COPILOT_CLI_PATH override, COPILOT_HOME isolation, BYOK mode
