---
name: msb-egress
description: "Emitting, ordering, approving or debugging msb egress rules and secret bindings in msbctl — rule_groups, extra_rules, --net-rule, --tls-intercept, --tls-intercept-port, egress_mode and observe mode, allow_private_dns, --secret placeholders and transcript passthrough, and the policy pin. Use before changing any of these, or when a connection out of a sandbox is refused, or before deciding whether a settings change needs a rebuild."
---

# Egress rules and secret bindings

Everything here is verified against msb 0.7.6 and re-checked on 0.7.7. The
property that makes this area expensive: **almost every failure here looks
like something else.** A blocked host looks like an outage, a denied
placeholder looks like a network drop, and a silently-unapplied rule looks
like working code.

## Order the rules in exactly this sequence

`Sandbox.net_rules()` returns one flat ordered list; msb applies it
first-match-wins, so position is semantics:

1. `base` — DNS, the Ubuntu mirrors, and a **deny** of plaintext `:80`. Always
   emitted first, from `defaults.toml`. Nothing a project writes can precede
   it, so **a plaintext `:80` allow can never be added from a project**. The
   fix for a plain-HTTP URL is its `https://` form.
2. the sandbox's `rule_groups`, in listed order
3. `extra_rules`
4. one `allow@host:tcp:port` per `[llm.<name>]` endpoint (`Sandbox.llms`)

Then emit `--net-default-egress deny` **explicitly**. Allow rules alone do not
close egress.

## Names, DNS and interception are one coupled mechanism

- **A hostname rule means HTTPS and nothing else.** On 443, msb's TLS
  interception reads SNI, so a name backed by an address pool is fine. On any
  other port nothing inspects the payload and the rule degrades to *the
  addresses the name resolved to*, which breaks against pools. For SSH, write
  a rule by address.
- **DNS resolution is part of the rule.** msb allows a connection based on the
  addresses *it* resolved. An unresolvable name fails identically to an
  unallowed one: NXDOMAIN in the guest, then a refused connection. Never
  diagnose a refusal as an outage before checking the rule.
- **Without `--tls-intercept`, every HTTPS hostname rule is a silent deny.**
  The same flag is what makes secret placeholder substitution possible, so the
  two requirements coincide and neither can be dropped alone.
- **`--tls-intercept-port` REPLACES msb's default of 443, it does not add to
  it** (spike 17). Any non-443 interception must restate 443 or every other
  HTTPS rule quietly dies. This is the single easiest thing to get wrong here.
- `allow_private_dns` emits `--no-dns-rebind-protection`. Needed whenever an
  allowed name resolves to RFC1918 (a public record pointing at `192.168.x.x`
  is normal in a homelab): rebind protection drops the answer, and the failure
  is indistinguishable from a missing rule. `curl --resolve` does **not** work
  around it.
- A wildcard suffix does not cover the apex — list `*.example.com` and
  `example.com`.
- **A host only this machine knows goes in a machine-local group, never in a
  project.** A group defined only in the operator's `config.toml`
  (`machine_only_groups()`) is written to the registry's `extra_rule_groups`,
  which adds to the project's groups, and `private_dns_groups` brings
  `allow_private_dns` with it. That is how `msbctl add` lets a self-hosted
  forge through (`ensure_forge_egress()` writes `forge-<host>`). Don't use the
  registry's `extra_rules` for this: in a folder sandbox it *replaces* the
  project's list instead of adding to it.
- Published ports (`--port`) are **inbound**; the egress policy has no say in
  them, in either mode. The guest server must listen on `0.0.0.0`.

## Secrets: headers, or nothing

`msb --secret ENV[:OPTIONS]@HOST` puts a **placeholder** in the guest env and
substitutes the real value host-side, into **request headers only** (HTTP
Basic auth included) for the named hosts. Query strings and bodies are not
substituted unless the binding opts in with `:query` / `:body`. Never put a
credential in a URL, and never work around the restriction.

**A placeholder in a request body is destroyed, and that breaks coding
agents.** msb kills any request carrying a `$MSB_<VAR>` where substitution
isn't permitted. The guest just sees TLS drop, which Claude Code reports as
`API Error: Connection dropped (ECONNRESET)` — and an agent only has to read
`$MSB_GH_TOKEN` once for it to land in the transcript, which is resent every
turn: a fresh session works, then degrades permanently. Allowing the host does
nothing; this is the secret policy, not the network one.
`with_transcript_passthrough()` adds `passthrough=[AGENT_TRANSCRIPT_HOSTS]` to
every binding msbctl emits — that lets the harmless *placeholder* travel and
still never substitutes the value.

Two authority rules, both enforced in `secret_env()`:
- `is_reserved_var()` (`GH_TOKEN`, every `CLAUDE_CODE_OAUTH_TOKEN*`) may never
  appear in `secret_binds` **in any layer**: create dies, `modify` skips with a
  warning.
- a binding whose `bindings_layer == "project"` takes its value from
  `secrets/<name>.env` only. The `global.env` fallback is registry-only.

## Applying a change

Network rules, TLS interception, DNS rebind protection, mounts, published
ports, owned disks and the image are **create-time**: `msbctl allow` / `mount`
/ `port` record them and say a rebuild is needed. `msb modify` cannot change
them. Full verified matrix: [references/msb-change-matrix.md](references/msb-change-matrix.md).

Anything that writes a pinned key (`PINNED_KEYS`: egress, bindings, `[secrets]`,
resources, caches) must call `check_policy()` **before** writing — so a pending
foreign change is asked about alone — then `approve_policy()` on a **reloaded**
`Sandbox`. `refuse_before_create()` runs before a rebuild removes anything. The
project's `.msb/` is also mounted read-only (spike 15) as a tripwire only: root
in the guest can unmount it, so the pin is the actual control.

## Measuring instead of guessing

msb **never logs a denial at any log level** (re-checked on 0.7.7 at
`--debug`/`--trace`). It logs what it allows: at debug, `TLS intercept
sni=<host> dst=<ip:port>` and a `dns::` line for a resolved name, in
`~/.microsandbox/sandboxes/<name>/logs/runtime.log`. **Nothing is logged for a
plain TCP connect on a non-443 port** — off 443, a DNS lookup is the only
evidence. That asymmetry is exactly why `egress_mode = "observe"` has to
unblock before it can measure: no rules at all, `--net-default-egress allow`,
`--log-level debug`, `--no-dns-rebind-protection` (a rebind block is a block,
and would leave no trace). `msbctl observe <name>` reads it back, flags what no
rule covers, and prints the `msbctl allow` line.

`egress_mode` is written to **and read from** the registry entry only, never
`sandbox.toml` — that file is committed and guest-writable, so honouring it
would ship an unfiltered sandbox to everyone who clones the project. A
project's value is ignored with a warning.

## Anchors in msbctl

Names are the stable handle; grep rather than jumping to a line:

```bash
grep -n "def net_rules\|def egress_mode\|def secret_env\|def transcript_hosts\|with_transcript_passthrough\|^AGENT_TRANSCRIPT_HOSTS\|^PINNED_KEYS\|def check_policy\|def approve_policy\|def is_reserved_var" msbctl
grep -n -- "--net-rule\|--net-default-egress\|--tls-intercept\|--no-dns-rebind" msbctl
```

Related spikes (re-runnable PASS/FAIL, `./spikes/NN-*.sh`; several need
host-specific env vars like `ALLOW_HOST`/`ALLOW_PORT` on purpose, and each
asserts both the allowed and the denied half): `03-lan-allowlist`,
`05-hostname-rules`, `07-claude-token-secret`, `08-gh-token-secret`,
`10-private-dns`, `17-llm-endpoint`.

Tests: `tests/fake/msb` records argv, so assert what reaches `msb`, and use
`assert_not_in_argv()` to prove a planted secret does not.

## Do not

- never emit `--conf` (it is code, not data: it mounts host paths and
  interpolates `${VAR}` from msb's environment, which holds the bound secrets)
- never add egress or `egress_mode` to a project's `sandbox.toml` unless it is
  genuinely portable, and never a machine-only group there — every other clone
  dies on "unknown rule group"
- never move a credential into a query string to make it substitute
- never assume a hostname rule covers a non-443 port

## Background

- `docs/content/egress.md` — the user-facing page (same repo; read the file,
  the rendered site isn't reachable from a sandbox)
- `docs/content/configuration.md#the-policy-pin` — which keys are pinned
- `defaults.toml` — the shipped rule groups and the comments on what each is
  for; new groups go there, never in a template skeleton
