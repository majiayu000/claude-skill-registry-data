---
name: cli-subagent
description: Universal multi-account local CLI subagent router and provisioner. Balances quotas across locally installed CLIs (agy, codex, grok, gemini, claude, qwen, opencode), auto-discovers new model families with <1ms cache checks, protects scarce frontier quotas, circuit-breaks unauthenticated profiles with explicit user alerts, and offers standard Antigravity/Codex global host integration after first initialization and verified execution.
---

# Universal Local CLI Subagent (`/cli-subagent`)

`/cli-subagent` routes bounded subagent tasks across locally installed CLI coding tools and isolated multi-account profiles (`~/.cli-subagent`). All scripts inside `scripts/` are strictly internal plumbing: the user interacts exclusively through chat prompts.

Resolve `<SKILL_DIR>` to the directory containing this `SKILL.md`, and invoke `python "<SKILL_DIR>/scripts/cli.py" ...`.

## 1. Core Operational Laws

1. **Local CLIs Only:** Never configure or route through cloud API gateways, proxy scrapers, or third-party relays. Only locally installed CLI binaries enabled by the user in `~/.cli-subagent/config.json` are valid targets.
2. **100% Prompt-Driven UX:** Never instruct the user to run Python commands or edit JSON/Markdown config files manually. Run `cli.py` yourself on the user's behalf.
3. **Strict Tier Cost Protection:**
   - `--tier fast`: Regex/AST scans, file discovery, log triage, quick read-only checks.
   - `--tier workhorse` *(Default)*: Everyday coding, bugfixes, code review, root-cause investigation. Strictly forbidden from touching scarce `frontier` models (`Argon`, `Carbon`, `Astra`, `Opus`, etc.).
   - `--tier frontier`: Opt-in ONLY for critical architectural synthesis, `/battle` rivalries, or complex formal invariants.
4. **Host Self-Call Avoidance:** `cli.py` automatically skips spawning subprocesses on the active host's primary account (`agy` inside Antigravity, `codex` #1 inside Codex) and round-robins across external CLIs and isolated multi-home accounts (`codex2..N`, `grok..N`, etc.). Pass `--isolate-context` only when isolating noisy logs on the host CLI.
5. **Mandatory Dispatch Tag & Actionable Alerts:**
   - Emit the `dispatch_tag` field from `cli.py` output (`[DISPATCH: role=..., tier=PRIMARY|FALLBACK, tool=..., model=..., settings=...]`).
   - **Never mask broken profiles silently:** Whenever `alerts` contains `AUTH_REQUIRED` or `NETWORK_BLOCKED`, complete the user's task via healthy profiles (or built-in `invoke_subagent` / native subagent fallback when `status == "pool_exhausted"`), AND explicitly report affected profiles in chat, offering prompt-driven sign-in (`--login --account <name>`).

## 2. First-Run Initialization, Live Verification & Host Integration Protocol

Trigger this flow when `cli.py` returns `status: "uninitialized"` (`exit_code: 2`), or when the user asks via prompt to initialize or reconfigure `/cli-subagent`:

1. **Discover Installed CLIs & Host State:**
   ```bash
   python "<SKILL_DIR>/scripts/cli.py" --discover
   ```
2. **Ask Account Counts via Prompt:**
   Present installed local CLIs (`installed: true`), showing existing profile counts (`discovered_profiles`), `max_accounts` (`1` for native `agy`, up to `9` for multi-home CLIs), and auth readiness. Ask how many isolated accounts (`0..max_accounts`, `0` = disable) to configure per installed CLI.
3. **Provision Pool & Optional Sign-In:**
   ```bash
   python "<SKILL_DIR>/scripts/cli.py" --init --spec "agy:1,codex:2,grok:2"
   ```
   If selected profiles report `AUTH_REQUIRED` and the user wants to sign in now, run:
   ```bash
   python "<SKILL_DIR>/scripts/cli.py" --login --account <account_name>
   ```
4. **Execute Live Verification Run:**
   ```bash
   python "<SKILL_DIR>/scripts/cli.py" --verify
   ```
5. **Offer Global Host Instructions Update (After Successful Run):**
   When initialization AND the live run succeed (`status == "ok"`), check `host_integration_offer` in the JSON output. If `offer_pending` is `true`, ask the user via prompt whether to update the active environment's global instructions for standard subagent workflows:
   - **Antigravity (`~/.gemini/config/AGENTS.md`)**: Configures `/cli-subagent` delegation for `/goal`, `/teamwork`, `/owl`, `/battle`, `/boost`, and `/plan`, and automatically unlocks `/owl` and `/battle` in `~/.gemini/config/skills/` if unavailable.
   - **Codex (`~/.codex/AGENTS.md`)**: Configures `/cli-subagent` delegation for `review-agent` and multi-agent subagent workflows.
   - On confirmation: `python "<SKILL_DIR>/scripts/cli.py" --integrate-host` (creates timestamped backups in `~/.cli-subagent/backups/`).
   - On refusal: `python "<SKILL_DIR>/scripts/cli.py" --integrate-host --decline`.

## 3. Dispatching Subagent Tasks

Routine execution checks binary and native `models_cache.json` fingerprints in `<1ms` with zero discovery tokens:

```bash
python "<SKILL_DIR>/scripts/cli.py" \
  --provider auto \
  --tier workhorse \
  --role investigator \
  --mode plan \
  --workspace "<ABSOLUTE_WORKSPACE_PATH>" \
  --task "<SELF_CONTAINED_BOUNDED_TASK>" \
  --run
```

### Key Flags (`scripts/cli.py`)
- `--provider {auto,agy,codex,grok,gemini,claude,qwen,opencode}`: `auto` round-robins across healthy enabled pools; specify a provider when cross-vendor diversity is required.
- `--tier {fast,workhorse,frontier}`: Dynamic model selection across current and future model families.
- `--mode {plan,accept-edits,read-only,workspace-write}`: Use `plan` / `read-only` for research and reviews; use `accept-edits` / `workspace-write` only on partitioned files or isolated branches.
- `--role <label>`: Sets `role=<label>` in `dispatch_tag`.
- `--task-file <path>`: Pass large prompts via UTF-8 file.
- `--status` / `--refresh`: Inspect pool health, verification state, or force a zero-token native catalog rescan.
