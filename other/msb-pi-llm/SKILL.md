---
name: msb-pi-llm
description: "pi and model endpoints: [bootstrap] pi and PI_PACKAGE, [llm.<name>] tables validated by llm_problem(), PI_PROVIDERS, Sandbox.llms turning each endpoint into an allow@host:tcp:port rule after the groups with --tls-intercept-port for a non-443 port and --tls-upstream-ca-cert-for for a LAN CA, the LLM_KEY_<NAME> binding and is_reserved_var(), ensure_pi() writing models.json, merging settings.json (including what it settles there for unattended runs: defaultProjectTrust, agent/trust.json, PI_CHANGELOG_SEEN) and copying the profile as AGENTS.md into the host-side STATE_DIR/pi/<name>/agent/ which is the guest's /root/.pi, transcript_hosts, and the section_llms and section_llm sections. Use when changing how pi is installed or configured, or how an endpoint or its key reaches it."
---

# Pi Llm

Detail carved out of `AGENTS.md`, which keeps only what has to hold in
every session. Repo-specific throughout; the facts here are verified against
msb 0.7.6 and re-checked on 0.7.7.

`pi` (`[bootstrap] pi`, `PI_PACKAGE`) talks to `[llm.<name>]` tables in
`config.toml` (`llm_problem()` validates: `base_url` HTTPS-only and `models`, or `provider` from `PI_PROVIDERS`), chosen per sandbox by `llm` in the registry entry, else `[defaults] llm` — machine-local only, never the project. `Sandbox.llms` turns each into an `allow@host:tcp:port` rule after the groups, `--tls-intercept-port` for a non-443 port (443 ALWAYS restated: one such flag replaces msb's default — spike 17), `--tls-upstream-ca-cert-for host=ca_cert`, `allow_private_dns` from `private_dns`, and a `LLM_KEY_<NAME>@host` binding (own env file, else `global.env`; `is_reserved_var()` reserves the prefix). Every binding's passthrough is `Sandbox.transcript_hosts` (Anthropic's plus each endpoint), not the bare constant. `ensure_pi()` writes `models.json` (a `$`-reference to the variable, never the value; see `llm_key_ref()`), merges `settings.json` and copies the profile as `AGENTS.md` into `STATE_DIR/pi/<name>/agent/` on the HOST, which is the guest's `/root/.pi`; no `msb exec`. Models are never a stored list by default: `served_models()` asks each custom endpoint on every start (`fetch_llm_models()`, host-side, real key, its `ca_cert`; cached in `STATE_DIR/llm/` as the fallback), `default_model` is the start model, and a stale one warns and falls back to the first served. `settings.json`'s default is set when msbctl's choice changed since `agent/.msbctl.json` recorded it, or when pi's names something gone; a switch made inside pi is otherwise kept.

**Nobody is at the terminal, so `ensure_pi()` settles pi's two startup questions.** `defaultProjectTrust = "always"` in `settings.json` plus this sandbox's `guest_project` and `TRUSTED_GUEST_DIRS` in `agent/trust.json` — a flat path→`true`/`false`/`null` map, needed ALONGSIDE the default because a saved decision outranks it and an interactive "do not trust" from an earlier run would otherwise keep the prompt alive; pi refuses to start on any other kind of value, so an existing file is filtered, never replaced. Trust goes to `always` because the VM and its egress policy are the boundary and the mounted folder is the operator's own checkout, whose `.agents/skills/` the profile tells the agent to go and read — and because with no terminal pi answers the same question *no* by itself, which used to drop those skills silently in `msbctl exec` runs. The post-update "What's New" block is silenced with `lastChangelogVersion = PI_CHANGELOG_SEEN` (`9999.0.0`): pi shows entries newer than the marker and rewrites the marker only when it shows something, so the sentinel outlives every `msbctl update -c pi` (`do_pi` installs `@latest`, unpinned) and `/changelog` still works. Checked against pi 1.4.0's `getNewEntries()`, `resolveProjectTrusted()` and `ProjectTrustStore`. Claude's equivalent is `onboarded_json()`/`MERGE_CLAUDE_JSON`. Setup section "Model endpoints" (`section_llms`: `_add_llm()` probes with `probe_llm_server()` — OpenAI `/v1/models`, `/models`, then Anthropic — and picks from the list with `pick_model()`; "choose a model" is `_choose_llm_model()`, no rebuild), edit section "Models for pi" (`section_llm`, a rebuild).

**The scope.** `PI_PACKAGE` is `@earendil-works/pi-coding-agent`: pi moved out of
the `@mariozechner` scope, which npm deprecates and which is frozen at 0.73.1, so
`@latest` there never moves. `bootstrap.sh`'s `do_pi` gets the name as
`MSB_PI_PACKAGE`. A guest still on the old scope is deliberately not migrated
(pi is pre-release here): `do_pi`'s `command -v pi` early return leaves it alone,
and a rebuild is the fix. Check any third-party pi package against
this before promising it: pi resolves an extension's imports through an alias map
of the scopes it bundles itself (`dist/core/extensions/loader.js`), 0.73 aliases
only `@mariozechner/*` while 1.x aliases both, so a package compiled against
`@earendil-works/*` cannot load on 0.73 and a `pi.ts` bundle adapter loads either
way. Same map is why `msb-<name>.ts` never had to change.

**The one silent break that came with it: `models.json`'s `apiKey` must be
`$LLM_KEY_<NAME>`** (`llm_key_ref()`). pi >=1.0 interpolates `$NAME`/`${NAME}` and
takes anything else as a literal key, where 0.73 looked a bare name up in the
environment — verified by running each version's `resolveConfigValue()`. No
spelling satisfies both; `!printenv NAME` does, at the cost of a shell per request
out of a config file, which is exactly the config-as-code this repo keeps out of
the guest. A guest left on 0.73 therefore sends the literal `$LLM_KEY_…` and gets
a 401 that names it; rebuild it.

**`PI_OFFLINE` earns its keep past 0.73:** it stops pi fetching `fd` and
`ripgrep` from GitHub releases for its grep and find tools, which refuse outright
with neither a download nor a system binary. Harmless — both are in
`bootstrap.sh`'s base package list.

**Third-party pi packages** come from a tool bundle's `pi_package`, installed by
pi inside the guest into `~/.pi/agent/npm/` (on the mount) — `msb-tool-bundles`
has the mechanism. `UPDATERS["pi"]` runs `PI_OFFLINE=0 pi update --extensions`
after the npm install, so `msbctl update -c pi` moves unpinned packages too.
