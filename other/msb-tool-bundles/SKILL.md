---
name: msb-tool-bundles
description: "Agent tool bundles: ~/.config/msb/tools/<name>/ with bundle.toml (description, hosts, [env], pi_package — a pi package installed by pi in the guest via plan_pi_packages()/sync_pi_packages(), validated by bundle_problem()/bundle_host()), pi.ts and claude/SKILL.md; Sandbox.bundles from the registry's tools or [defaults] tools and never the project, its allow@host:tcp:port rules in net_rules() as source tools:<name>, its ports in --tls-intercept-port, bundle_env() under every [env], is_reserved_var() and the MSB_ prefix refused, apply_pi_bundles() copying msb-<name>.ts into STATE_DIR/pi/<name>/agent/extensions, apply_claude_bundles() copying skills/msb-<name>/SKILL.md into STATE_DIR/claude/<name> (the guest's ~/.claude), the STATE_DIR/tools/<name>.json marker that makes a disable take the adapter away, kandev getting none, section_tools/section_agent_tools, and spike 19. Use when changing how a capability reaches an agent, or when a tool an agent should have is missing or its endpoint is refused."
---

# Agent Tool Bundles

Detail carved out of `AGENTS.md`, which keeps only what has to hold in
every session. Repo-specific throughout; the facts here are verified against
msb 0.7.6 and re-checked on 0.7.7.

A bundle is one capability **this machine** owns and a project never names: a
folder under `TOOLS_DIR` (`~/.config/msb/tools/<name>/`) holding `bundle.toml`
(`TOOL_KEYS`: `description`, `hosts`, `[env]`), `pi.ts` (`PI_BUNDLE_FILE`) and
`claude/SKILL.md` (`CLAUDE_BUNDLE_FILE`), the last two optional. **Nothing is
shipped**: a bundle points at endpoints the operator runs, so shipping one
would aim every clone at someone else's server — the same reasoning as
`machine_only_groups`, and the reason `Sandbox.bundles_pinned` reads `tools`
from the registry entry only, falling back to `[defaults] tools`, and never
from a project's `sandbox.toml`. `available_bundles()` parses every folder but
never dies — a bundle that does not parse is `({}, "does not parse: …")` — so a
half-written draft stops only the sandboxes that name it. `bundle_status()` /
`Sandbox.bundle_status` give each named bundle's problem (unknown name, parse
error, `bundle_problem()`) with the file named; `Sandbox.bundles` dies on the
first one and is what every path that APPLIES a bundle reads (rules, env,
adapters), at every start. `show`/`show --json` read `bundle_status` and flag
the problem instead (a `problem` key per `tools` row). Both are
`functools.cached_property`: one start reads them half a dozen times.

`bundle_problem()` is the whole validation: slug folder name, no unknown keys,
one-line `description` (it is what the agent is told it has), non-empty `hosts`
parsed by `bundle_host()` (`HOST`, `HOST:PORT`, `[IPv6]:PORT`, never a scheme or
rule syntax, never port 80, then `rule_problem()`), and `[env]` whose names are
shell identifiers, are not `is_reserved_var()`, and do not start `MSB_` (msb's
placeholder for a bound secret is the literal `$MSB_<VAR>` — spike 13 — and a
bundle's env reaches the guest VERBATIM, so a mention in a body the interceptor
cannot substitute is a refused request). An env value that parses as a URL must
be https and its `host:port` must be in `hosts` (compared lowercased, as
`urlsplit().hostname` is), or the tool would be handed a
call egress denies — which from inside the guest reads as an outage, not as a
rule.

Everything is derived from those three keys. `net_rules()` appends one source
per bundle (`tools:<name>`, so a refusal names which `bundle.toml`), after the
groups and the `[llm]` rules and before `extra_rules`; its non-443 ports join
the `--tls-intercept-port` union with the model endpoints' (443 always
restated); `bundle_env()` is merged FIRST in `env_vars()`, under every `[env]`,
and like every variable is fixed at create — so `hosts`, `[env]` and
attaching/detaching a bundle are rebuilds, while adapter files and the
description refresh on the next start. `Sandbox.bundles` returns `[]` for a
Kandev sandbox: `kandev_provision()` builds its own argv with its own egress and
runs none of the per-boot seeding, so a bundle there would be rules with no
tool.

Delivery is host-side, into mounts that already exist — no new mount, no
`npm install`, nothing runs in the guest to install it.
`apply_pi_bundles(box, agent)` copies each adapter to
`STATE_DIR/pi/<name>/agent/extensions/msb-<name>.ts` (`BUNDLE_PREFIX`), which
pi discovers as `~/.pi/agent/extensions/`; `apply_claude_bundles(box)` (from
`ensure_profile()`, secret mode only) copies each Claude skill to
`STATE_DIR/claude/<name>/skills/msb-<name>/SKILL.md`, the guest's `~/.claude`.
The prefix on both keeps a bundle off a skill or extension the operator has
under the bundle's own name. A stale adapter whose removal fails stays in the
marker and is retried next start. Which ones msbctl wrote is recorded
in `STATE_DIR/tools/<name>.json` (`bundles_applied()`/`bundles_record()`), so a
disable deletes exactly those and leaves an extension or skill the operator put
there by hand; `rename_sandbox()` moves that marker and `purge` unlinks it.
`sandbox_profile_section(box, harness)` announces each bundle's `description`
— only to the harness it ships an adapter for — because an
agent that does not know a bundle exists reaches for the built-in web tools and
hits the deny.

A `pi.ts` adapter is **one self-contained file**: msbctl copies it and nothing beside
it, so a relative import dangles, and only pi's aliased imports
(`@earendil-works/pi-coding-agent`, which pi also aliases under the
`@mariozechner` name it used to have, and `typebox`), node builtins and
globals are available. Endpoints come from `[env]` at call time, never written into the
adapter, so the same copy serves every sandbox and a URL in the file cannot
hide from the rule list.

**`pi_package`** (`pi_package_problem()`: a bare npm name, optionally
`@<exact version>`; no range, tag or `npm:`/`git:`/path source) is the one
exception to "nothing runs in the guest". `plan_pi_packages()` merges
`npm:<spec>` into settings.json's `packages` (marker key `pi_packages` lists the
npm names msbctl declared, so a `pi install` of the operator's is never
touched) and drops a detached one HERE, so pi stops loading it whatever the
guest does. `sync_pi_packages()` then `msb exec`s only for real work: `PI_OFFLINE=0
pi install npm:<spec>` for one missing or off its pin, `npm uninstall
--prefix ~/.pi/agent/npm` for a detached one still there (not `pi remove`, which
exits 1 once the settings entry is gone). Installed-or-not is read from the
mount (`pi_package_installed()`: `agent/npm/node_modules/<name>/package.json`,
pi 1.4's `getNpmInstallRoot()`), never from an exit status; a miss warns and the
start carries on. The guest step runs only when `ensure_running()` actually
starts the sandbox or is `msbctl start` (`ensure_pi(box, packages)`), so a
failing install never delays a `shell`/`exec` into a running one; the marker
is kept either way. An entry the operator already has for the same npm name is
never adopted (it would be uninstalled on a detach): the bundle's is left out
with a warning. Two bundles naming one package die in `Sandbox.bundles`. `PI_OFFLINE=1` stays in `[agent_env.pi]` — it is exactly what
stops pi's own `installMissing()` and `updateConfiguredSources()` — so the
install and `UPDATERS["pi"]`'s `pi update --extensions` lift it for one command.
A `pi_package` counts as a pi adapter (`bundle_adapters(folder, spec)`), so the
bundle is announced to pi only, and `hosts` may be omitted for it. msbctl names
no package, fetches none on the host and resolves no dependency: that is the
line that keeps this from becoming a plugin manager. Package-specific switches
belong in the bundle's `[env]` (bili: `ACP_AUTO_UPDATE=0`, read by its
`checkForUpdate()` in 0.1.83).

UI: setup section "Agent tools" (`section_tools`, `_summary_tools`,
`BUNDLE_SKELETON` when `TOOLS_DIR` is empty — there is no TOML writer and no
picker can guess an endpoint) writes `[defaults] tools`; edit section "Agent
tools" (`section_agent_tools`) writes the registry's `tools` and asks for a
rebuild. `show` prints one `tool` line per bundle and `show --json` a `tools`
list (names of env variables only, never a reason to worry about values).
Tests: `tests/test_bundles.py`. `spikes/19-agent-tool-bundle.sh` checks what a
unit test cannot — the adapter under pi's own loader on the host (`SPIKE_LIVE=1`
also calls the endpoints), and with `SPIKE_SANDBOX=<name>` the emitted rules,
both adapter files and a search called from inside the guest, where only the
emitted rules apply.
