---
name: cgagentharness-otel-hardening
description: Statically re-verify CG-agent-harness's telemetry-kill contract — the per-spawn-site child environments (gh, git, sandboxed checks, MCP servers, desktop sidecar), the telemetry-free Cargo lock graphs, and a category-1-5 egress classification of every crate, binary and launcher — then sweep vendor docs. Use when asked to audit telemetry or phone-home leaks, after bumping a network crate, or when adding a dependency, spawn site or launcher. Not for the sandbox, write gates or dependency pins (invariant-guard, write-policy-redteam, verify-deps).
disable-model-invocation: true
---

# otel-hardening (CG-agent-harness)

Port of CyClaw's `otel-hardening`. Same contract, different mechanism: CyClaw's
Python dependencies phone home unless env vars are set before import, so its
kill switch is one canonical env block applied at every entry point. Rust crates
do not phone home; here the contract is (a) **no telemetry SDK in either lock
graph**, (b) **every child environment the harness builds carries the opt-outs
for the external binary it launches**, and (c) **every network-capable
component is classified** so a new crate, binary or spawn site cannot land
unlabeled. **No pair below is a network kill switch**: they silence vendor
telemetry readers, they close no socket. The sandbox denies network; the pairs
are its second layer, and on Windows (Job Object, sockets still work) the only
one.

## Where the contract lives

| Piece | File | What |
|---|---|---|
| shared builder | `src/common/child_env.rs` | one opt-out table per child kind (`Gh`, `VerificationCheck`, `McpServer`), applied last at each routed site; in `common`, so no `crate::agentic` (I6) |
| gh + git builder | `src/agentic/git.rs` `environment()` | runtime, GitHub auth/config and SSH-agent allowlist + git hygiene + `Gh` arm. git's `credential.helper` is `!gh auth git-credential`, so git's env is gh's env |
| gh builder | `src/agentic/gh_client.rs` `gh_env()` | Git allowlist without provider keys + `GIT_TERMINAL_PROMPT=0` + `Gh` arm; every `RunSpec` in `gh_client.rs`/`writer.rs` passes `env: Some(&gh_env())` |
| verifier builder | `src/agentic/executor/runner.rs` `scrubbed_env()` | `ALLOWED_ENV_VARS` (6) + `NO_PROXY=*`, `PIP_NO_INDEX`, `PIP_DISABLE_PIP_VERSION_CHECK`, `CARGO_NET_OFFLINE` + `VerificationCheck` arm |
| MCP stdio | `src/common/mcp.rs` `spawn()` + `mcp_worker.rs` | `env_clear()`, operator `env` through `filter_env()` (`SECRET_ENV` + `HIJACK_ENV` dropped), then `McpServer` arm (operator `env` cannot override it), fixed PATH/locale, scratch HOME |
| desktop | `desktop/src/backend.rs` `start()`, `main.rs` `prepare_cargo()`/`external_link()` | sidecar + python helper carry `RUSTUP_AUTO_INSTALL=0`; the opener runs `env_clear()` with a fixed PATH |
| lock graphs | `Cargo.lock`, `desktop/Cargo.lock` | no `opentelemetry*`, `sentry*`, `posthog*`, `*telemetry*`, `*analytics*` crate |
| oracle + inventory | `check_otel.py` | the independent second copy of every pair, allowlist and strip list, plus the category 1–5 row for every crate, binary, launcher and provider |

The builder closed parity O6. The oracle credits each site only with the arm
it actually calls, and an arm's names are never re-pinned at a site.

## Steps

1. **Static contract check** (offline; reads files, never builds):

   ```bash
   python3 .claude/skills/cgagentharness-otel-hardening/check_otel.py --strict --as-of $(date +%F)
   ```

   T1 builders present · T2 exact pairs per site, literals plus the arm it
   calls (missing / extra / flipped / unrouted all FAIL) · T3 allowlists and
   strip lists exact · T4 inventory
   staleness (120d) · T5 lock-graph telemetry-crate denylist, both crates · T6
   verified-pin drift (reqwest, rmcp, axum, rustls, hyper, keyring, tantivy,
   tracing-subscriber, tauri; `DEFAULT_MIN_GH`) · T7 every `Command::new(` file
   is listed and `src/server` has none · T8 no literal re-enable, `remove_var`
   or `set_var` of a kill name · T9 every gh/git `RunSpec` routes through its
   builder; the three external-binary sites carry `DO_NOT_TRACK=1` +
   `GH_TELEMETRY=false` · T10 every direct dependency, external binary and
   finetune requirement classified; dynamic launcher markers present · T11 MCP
   spawn/worker clear, opener clears, sidecar pins its home · T12 sandbox
   network-denial literals (`--unshare-net`, `deny network*`, `--net`) present.

2. **Mutation self-test** — a checker that cannot fail proves nothing:

   ```bash
   bash .claude/skills/cgagentharness-otel-hardening/verify.sh
   ```

   One mutation per rule, each asserting it changed the file. Neither script is
   in `.claude/settings.json`'s allowlist or any workflow: expect a permission
   prompt, and treat a red run as work, not as advisory.

3. **Live vendor sweep** (network) — for each category-1/2 row whose `reviewed`
   is old or whose pin drifted (T6), re-read the row's URL and confirm the
   control still exists with the same name, values and read timing:

   | Vendor | Re-verify |
   |---|---|
   | gh (floor 2.40.0) | `gh help environment` still documents `GH_TELEMETRY` true/false/log and `GH_NO_UPDATE_NOTIFIER`? The names were inherited from CyClaw's 2026-08-27 read, not re-read at port time. Is `GH_NO_EXTENSION_UPDATE_NOTIFIER` still separate? |
   | rustup | `RUSTUP_AUTO_INSTALL=0` still the auto-install switch? |
   | cargo / pip | `CARGO_NET_OFFLINE`, `PIP_NO_INDEX`, `PIP_DISABLE_PIP_VERSION_CHECK` unchanged? |
   | reqwest / rmcp / tauri | changelog since the verified pin: any new default egress (update checks, crash reporting, a telemetry feature flag)? |
   | huggingface_hub / chromadb | still the names a verified Python repo reads (CyClaw's rows are the reference) |

4. **Close a real gap** (additive, low-risk): change the Rust site AND
   `check_otel.py`'s oracle AND the inventory row (`reviewed`, evidence) in one
   commit, add a `verify.sh` mutation for any new rule, re-run steps 1–2, then
   `cargo test` (the sites have unit tests: `git.rs`, `mcp.rs`
   `secret_env_names_are_stripped`, `child_env.rs`). A new opt-out goes in a
   `child_env` arm, never a site literal. The lock-graph half is CI-enforced:
   `[bans].deny` in `deny.toml` and `desktop/deny.toml` lists the T5 families
   by exact crate name; a new family's names go in both files.

5. **Classify anything new; retire anything gone.** A new crate, binary,
   provider, connector or spawn site gets an `INVENTORY` row or alias with
   exactly one category: 1 unsolicited telemetry with an official control (the
   pair must be delivered by a `SITES` builder — never invent one) · 2
   update/version/toolchain-fetch egress · 3 intentional policy-gated feature
   traffic (controls stay empty) · 4 local-only, or network denied by the
   sandbox · 5 no mechanism found (evidence + date). T10 reads both manifests
   and `finetune/requirements.txt` itself, but an external binary is swept only
   if named in `KNOWN_EXTERNAL_BINARIES`, and a run-time-chosen executable
   (MCP servers, caller checks) lives in `DYNAMIC_LAUNCHER_SITES` with the
   source marker that proves it still spawns. Remove the alias and row when a
   pin or site goes.

## Guardrails

- **I6 is untouched by this skill**: it reads; it never adds a server-side
  spawn. T7 fails on any `Command::new(` under `src/server`.
- **Category-3 traffic is gated by harness policy**, never by a kill pair: the
  cloud providers, web search, webhooks, MCP clients, gh writes. Never block
  them with an env pair and never weaken a gate to simplify one.
- **Write gates stay closed**: `agentic.enabled`, `deepagent_github.enabled`,
  `allow_git_write_tools` ship false; this skill changes none of them.
- The checker keeps **zero side effects**: no cargo, no network, no writes.

## Gotchas

- **`Command::new(` is the sweep marker.** `Command::new` inside a string (the
  governance regex) or `use tokio::process::Command;` does not match; a spawn
  built another way (`posix_spawn` via libc) would not either — add a marker.
- **The bypass sweep strips from the first `#[cfg(test)]` to end of file.**
  A test-only item placed mid-file hides the production code after it from
  T7/T8 (false negative, never a false positive). Keep tests last.
- **`ANONYMIZED_TELEMETRY` is lower-case `false` here, `False` in CyClaw.**
  Both parse the same; do not "align" one side and break its oracle.
- **`NO_PROXY=*` bypasses proxies; it does not fail-close networking.** The
  sandbox does. Windows is env-only.
- **Ollama has no telemetry switch to set.** `POST /api/ollama/pull` asks the
  daemon to fetch a model; the daemon's registry egress is outside this
  process. Do not add a speculative `OLLAMA_*` pair.
- **`cargo deny` bans exact names; T5 matches patterns.** A telemetry crate
  under a name neither `deny.toml` lists passes CI until both list it; T5
  still catches it. Verify a name on crates.io before adding it.
- The desktop lock resolves two `reqwest` majors (0.12 via the harness, 0.13
  via tauri); duplicate versions are warn-only policy, reported as INFO.
