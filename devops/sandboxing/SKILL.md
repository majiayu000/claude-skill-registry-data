---
name: sandboxing
description: "Isolation and egress control for running coding agents safely — Claude Code's Bash sandbox (Seatbelt/bubblewrap/socat proxy), @anthropic-ai/sandbox-runtime, dev containers with default-deny iptables firewalls, hardened Docker/gVisor/Firecracker, egress allowlists, and credential-injection proxies. WHEN: \"sandbox Claude Code\", \"/sandbox\", \"bubblewrap\", \"Seatbelt\", \"sandbox-runtime\", \"srt\", \"init-firewall.sh\", \"devcontainer firewall\", \"egress allowlist\", \"block agent network access\", \"gVisor\", \"Firecracker\", \"run --dangerously-skip-permissions safely\", \"isolate the agent from ~/.aws\", \"credential injection proxy\", \"unattended agent in CI\". Also covers the Codex CLI sandbox for cross-vendor fleets: \"sandbox_mode\", \"workspace-write\", \"danger-full-access\", \"codex sandbox\", \"Landlock\", Codex \"requirements.toml\" lockdown. NOT for prompt-injection theory, OWASP GenAI Top 10, or agent threat modeling — use ai-security. NOT for general harness settings, permission rules, or hooks — use claude-code; day-to-day Codex CLI operation (config.toml keys, approval policies, codex exec) — use codex; Copilot or Cursor sandbox/permission configuration — use github-copilot or cursor. NOT for Agent SDK application code — use claude-agent-sdk. NOT for Kubernetes admission control, pod security standards, or container runtime hardening in general — that's the containers plugin; NOT for SIEM/EDR/WAF platform tooling — that's the security plugin."
license: MIT
---

# Agent Sandboxing

Isolation mechanics for coding agents: what boundary to pick, how to configure it, and how to keep credentials and egress inside it. Everything here is OS/infrastructure enforcement — it holds regardless of what the model decided to do.

**The governing rule (Anthropic's own):** effective sandboxing requires **both** filesystem and network isolation. Without network isolation a compromised agent exfiltrates SSH keys; without filesystem isolation it backdoors system resources to regain network access. Never ship one without the other.

## Pick the boundary first

| Approach | What is isolated | Docker? | Setup |
|---|---|---|---|
| Sandboxed Bash tool | Bash commands + child processes only | No | Minimal (macOS) / low (Linux, WSL2) |
| Sandbox runtime (`srt`) | Whole agent process — file tools, MCP servers, hooks | No | Low |
| Dev container | Full dev environment | Yes | Medium |
| Custom container | Full dev environment, your policies | Yes | Medium–high |
| Virtual machine / microVM | Full OS, own kernel | No | High |
| Claude Code on the web | Full OS, Anthropic-managed VM | No | None (subscription) |

Choose by goal:

- **Cut permission prompts in everyday local work** → built-in Bash sandbox via `/sandbox`.
- **Unattended runs** (`--dangerously-skip-permissions`, auto mode, CI) → container, VM, or sandbox-runtime. Never the Bash sandbox alone.
- **Isolate MCP servers and hooks without Docker** → sandbox-runtime.
- **Untrusted repository** → dedicated VM or Claude Code on the web.
- **Team standardization** → dev container committed to the repo.
- **Native Windows host** → container/VM, or run the Bash sandbox inside WSL2.

Always state the residual risk when recommending any of these: isolation reduces breach impact, it does not eliminate it. Any egress path can leak data the agent can read; any writable project mount can still corrupt that code; and isolation changes nothing about what is sent to the model — prompts and read files still go to the API.

## Non-negotiables

- **Always run `--dangerously-skip-permissions` inside an isolation boundary that contains the whole process** (container, VM, or sandbox-runtime). With no prompts, the boundary is the only control left. Claude Code refuses this flag as root on Linux/macOS, so run the container/VM as a non-root user.
- **Never treat the Bash sandbox as sufficient for unattended work.** It constrains Bash and its children only — built-in Read/Edit/Write, WebFetch, MCP servers, and hooks run unconstrained on the host.
- **Never mount `~/.ssh`, `~/.aws`, `~/.config/gcloud`, `~/.kube`, or `~/.docker` into an agent environment.** Prefer repository-scoped, short-lived tokens, or a credential-injecting proxy outside the boundary.
- **Never rely on a domain allowlist alone for confidentiality.** Proxies that do not terminate TLS allowlist by client-supplied hostname only — domain fronting bypasses them, and a broad grant like `github.com` is an exfiltration path to any repo on that host.
- **Never grant `allowUnixSockets` casually.** `/var/run/docker.sock` inside a sandbox is effective host root.
- **Never widen writes to `$PATH` directories, shell startup files, or agent config files.** A sandboxed command that can write `~/.bashrc` or `~/.claude/settings.json` widens its own access on the next run.
- **Treat a committed dev container as a convention, not an enforcement boundary.** Claude Code does not require the container; only device management/software allowlisting actually prevents running outside it.

## Layer 1 — Claude Code's Bash sandbox

OS-enforced per-Bash-command isolation: **Seatbelt** on macOS, **bubblewrap** on Linux/WSL2, with a proxy running *outside* the sandbox for network. Native Windows is unsupported (use WSL2; WSL1 will not work).

Prerequisites on Linux/WSL2: `bubblewrap` and `socat` (`apt-get install bubblewrap socat` / `dnf install …`), plus the optional seccomp filter that blocks Unix domain sockets, installed via `npm install -g @anthropic-ai/sandbox-runtime`. On Ubuntu 24.04+ the default AppArmor policy blocks bubblewrap's user namespaces — check `sysctl kernel.apparmor_restrict_unprivileged_userns` and add the `/etc/apparmor.d/bwrap` profile if it returns `1`. Run `scripts/01-sandbox-readiness.sh` to check all of this at once.

Defaults worth knowing before you write config:

- **Writes**: working directory + subdirectories + session `$TMPDIR`. Everything else denied, including `~/.bashrc` and `/bin`.
- **Reads**: the *entire computer* except denied paths — `~/.aws/credentials` and `~/.ssh/` are readable by default. There is **no built-in credential deny list**; you must add one.
- **Network**: nothing pre-allowed; first use of a domain prompts. `sandbox.network.allowedDomains` pre-allows; `WebFetch` allow rules also pre-allow.

Minimum hardened baseline:

```json
{
  "sandbox": {
    "enabled": true,
    "network": {
      "allowedDomains": ["api.anthropic.com", "registry.npmjs.org", "*.github.com"],
      "strictAllowlist": true
    },
    "credentials": {
      "files": [
        { "path": "~/.aws/credentials", "mode": "deny" },
        { "path": "~/.ssh", "mode": "deny" }
      ],
      "envVars": [{ "name": "GITHUB_TOKEN", "mode": "deny" }]
    }
  }
}
```

Prefer `mode: "deny"` over `mode: "mask"` unless the agent genuinely needs the credential to work. Masking swaps a sentinel for the real secret at the proxy and therefore **requires `network.tlsTerminate`**; on macOS masked *files* degrade to plain deny. Read `references/bash-sandbox-config.md` before writing any `credentials`, `filesystem`, or `tlsTerminate` block — the precedence rules and the settings-scope restrictions (several keys are ignored from repo settings by design) are where deployments go wrong.

Escape hatch: when a command fails on a sandbox restriction, Claude may retry it with `dangerouslyDisableSandbox`, which runs unsandboxed through the normal permission flow. Close it with `"allowUnsandboxedCommands": false` (Strict sandbox mode), or at minimum force a prompt with an ask rule on `Bash(dangerouslyDisableSandbox:true)`.

Version gates matter here — `credentials`, `strictAllowlist`, `tlsTerminate`, and masked files each landed in different Claude Code 2.1.x releases. Read `references/versions/claude-code-2.1.md` before promising a feature to a fleet on a pinned version.

## Layer 2 — sandbox-runtime (`srt`)

`@anthropic-ai/sandbox-runtime` (Apache-2.0, **beta research preview** as of 2026-08-05 — config format may still change) applies the same Seatbelt/bubblewrap primitives to an *entire process*, containerless. This is the smallest step from "Bash-only isolation" to "whole agent isolated," and it is what closes the MCP-server and hooks gap.

```bash
npm install -g @anthropic-ai/sandbox-runtime
npx @anthropic-ai/sandbox-runtime claude     # wrap the whole Claude Code process
```

Configure **before** first launch: the runtime denies all network by default and confines writes to a few built-in runtime paths. Minimum grants for wrapping Claude Code — `allowWrite` on the project dir, `~/.claude`, `~/.claude.json`, `/tmp`; `allowedDomains` for `api.anthropic.com` plus `claude.ai` and `platform.claude.com` if using OAuth sign-in rather than an API key. On Linux/WSL2 write grants only apply to paths that already exist, so `mkdir -p ~/.claude && echo '{}' > ~/.claude.json` first.

Two traps that silently produce a false sense of safety:

- Without a valid `~/.srt-settings.json` the runtime still *starts* (all network blocked, writes confined) — **a clean start is not proof your settings loaded**. Pass `--settings <path>` explicitly, which fails closed on a load error.
- On Linux/WSL2 the mandatory-deny list (`.git/hooks`, `.git/config`, `.mcp.json`, `.claude/commands`, shell startup files) is built **once at launch**. Repos created mid-session via `git init`/`git clone` are not covered. macOS checks per-write and does cover them.

Full config schema, per-platform mechanism (including the Windows WFP/`srt-sandbox` account model), proxy architecture, and documented limitations: `references/sandbox-runtime.md`.

## Layer 3 — dev container with a default-deny firewall

Use for team standardization and for unattended runs on **trusted** repos. Add the feature, persist auth, then add egress control:

```json
{
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": { "ghcr.io/anthropics/devcontainer-features/claude-code:1.0": {} },
  "mounts": ["source=claude-code-config-${devcontainerId},target=/home/node/.claude,type=volume"],
  "containerEnv": { "CLAUDE_CONFIG_DIR": "/home/node/.claude" }
}
```

Mounting `~/.claude` alone does **not** preserve sign-in — the OAuth account and personal MCP servers live in `~/.claude.json`, which is why `CLAUDE_CONFIG_DIR` must point at the mounted volume. The `:1.0` tag pins the feature's install script, not the Claude Code release; pin the release with an explicit `npm install -g @anthropic-ai/claude-code@X.Y.Z` in the Dockerfile plus `DISABLE_AUTOUPDATER=1` if you need reproducible builds.

Egress: the `anthropics/claude-code` reference container ships `init-firewall.sh`, a default-deny iptables + ipset allowlist requiring `NET_ADMIN` and `NET_RAW` via `runArgs`. Treat it as a starting point to copy and edit, not a maintained base image — and drop it entirely if you already enforce egress with a corporate proxy, since the capabilities are not required by Claude Code itself. Its exact rule order, the GitHub-meta CIDR population, and the self-verification step (a `curl` that must fail plus one that must succeed) are in `references/devcontainer-isolation.md`; port that verification pattern into any firewall you write, because an allowlist that silently failed to apply looks identical to one that worked.

Caveat to state explicitly whenever recommending dev containers: with `--dangerously-skip-permissions`, the container does not stop a malicious project from exfiltrating anything reachable inside it, **including the Claude Code credentials in `~/.claude`**. Trusted repos only.

Org policy inside the container goes to `/etc/claude-code/managed-settings.json` (highest precedence), but a Dockerfile `COPY` of it is editable by anyone with repo write access — deliver real policy via MDM or server-managed settings instead.

## Layer 4 — hardened container, gVisor, VM

| Technology | Isolation | Overhead | Complexity |
|---|---|---|---|
| Sandbox runtime | Good (secure defaults) | Very low | Low |
| Containers (Docker) | Setup dependent | Low | Medium |
| gVisor | Excellent (correct setup) | Medium/high | Medium |
| VMs (Firecracker, QEMU) | Excellent (correct setup) | High | Medium/high |

Container hardening is only as good as the flags. The reference-grade run drops all capabilities, forbids privilege gain, uses a read-only rootfs with `tmpfs` scratch, **removes the network stack entirely** (`--network none`), and reaches the outside world solely through a bind-mounted Unix socket to a host-side proxy:

```bash
docker run --cap-drop ALL --security-opt no-new-privileges \
  --security-opt seccomp=/path/to/seccomp-profile.json \
  --read-only --tmpfs /tmp:rw,noexec,nosuid,size=100m \
  --network none --memory 2g --cpus 2 --pids-limit 100 --user 1000:1000 \
  -v /path/to/code:/workspace:ro -v /var/run/proxy.sock:/var/run/proxy.sock:ro agent-image
```

`--network none` + proxy socket is the single highest-leverage pattern in this skill: a prompt-injected agent has no route to arbitrary servers, only to the proxy. It is the same architecture sandbox-runtime and Firecracker's `vsock` variant implement.

Escalate beyond containers when the shared host kernel is the problem. **gVisor** (`--runtime=runsc`) intercepts syscalls in userspace so an exploit must first break gVisor, at ~0% overhead for CPU-bound work but up to 10–200x on heavy file I/O — usually worth it for multi-tenant or untrusted content. **Firecracker** microVMs boot in under 125 ms with <5 MiB overhead and give a separate kernel. Note that VMs are not automatically "more secure" than gVisor; VM security rests on the hypervisor and its device emulation.

Layering the Bash sandbox *inside* a container is valid defense in depth, but unprivileged containers cannot mount a fresh `/proc` — that needs `enableWeakerNestedSandbox: true`, which considerably weakens the inner sandbox and is only acceptable because the outer container already isolates.

Full hardening tables, gVisor setup, cloud-deployment topology (private subnet, no internet gateway, egress only to your proxy), and per-flag rationale: `references/egress-and-secrets.md`.

## Egress allowlist design

Design allowlists as narrowly as the toolchain permits, then verify from inside the boundary. For Claude Code the required hosts are `api.anthropic.com` (always, including WebFetch's domain-safety preflight even on Bedrock/Vertex/Foundry unless `skipWebFetchPreflight: true`), plus auth hosts `claude.ai` / `claude.com` / `platform.claude.com`, and `registry.npmjs.org` for npm/bun installs. Telemetry hosts are optional and can be dropped with `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`. The complete table with the per-host reason is in `references/egress-and-secrets.md` — quote it rather than guessing, because omitting `platform.claude.com` breaks token refresh in ways that look like a model outage.

Proxy mechanics to get right:

- Claude Code reads the first set of `https_proxy`/`HTTPS_PROXY`/`http_proxy`/`HTTP_PROXY`. **SOCKS proxies are not supported** for Claude Code's own traffic (sandbox-runtime's internal SOCKS5 proxy is a different thing).
- `HTTPS_PROXY` alone cannot inspect or modify request contents — it builds a CONNECT tunnel. Credential injection and content filtering require a TLS-terminating proxy with its CA in the agent's trust store.
- Not every tool honors proxy env vars. `curl`/`pip`/`npm`/`git` do; **Node.js `fetch()` ignores them by default** (Node 24+: `NODE_USE_ENV_PROXY=1`). For comprehensive coverage use proxychains or iptables redirection to a transparent proxy.
- Enterprise TLS: `NODE_EXTRA_CA_CERTS` or `CLAUDE_CODE_CERT_STORE` for custom roots, `CLAUDE_CODE_CLIENT_CERT`/`_KEY` for mTLS. Verify with `/status` or `claude --debug`.

## Secrets inside the boundary

Best pattern, in order of preference:

1. **Keep the credential outside the boundary entirely.** A proxy or MCP server outside the sandbox performs the authenticated request; the agent calls a tool and never sees the secret. Named implementations: Envoy (`credential_injector` filter), mitmproxy, Squid, LiteLLM. This also gives you one audit log and one rotation point.
2. **Sentinel masking** (`sandbox.credentials … mode: "mask"`) when a CLI must appear to hold the token. Requires TLS termination; mask `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` **together** or SigV4 re-signing breaks.
3. **Deny** everything else, explicitly.

Sanitize before mounting even read-only: `.env*`, `~/.git-credentials`, `~/.aws/credentials`, gcloud ADC JSON, `~/.azure/`, `~/.docker/config.json`, `~/.kube/config`, `.npmrc`/`.pypirc`, `*-service-account.json`, `*.pem`, `*.key`. Read access is exfiltration access.

Sandboxed Bash commands inherit the parent environment including credentials by default; `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` strips Anthropic/cloud credentials from **all** subprocesses regardless of sandboxing, and additionally forces filesystem isolation to stay on.

## CI and headless agents

Treat every CI agent as unattended: whole-process boundary, no long-lived credentials in the environment, egress allowlist, and ephemeral workspace. Prefer official actions that keep the API key out of build scripts. For OpenAI Codex CLI in the same role, the equivalent knobs are `sandbox_mode` (`read-only` / `workspace-write` / `danger-full-access`), `approval_policy`, and `[sandbox_workspace_write].network_access = false`, enforced by Seatbelt on macOS and bubblewrap/Landlock/seccomp on Linux — see `references/codex-sandbox.md` for the config and the `requirements.toml` enterprise lockdown. Everything else about running Codex day to day (the rest of `config.toml`, approval prompts, `codex exec`, cloud tasks) belongs to the `codex` skill; this skill keeps only the isolation surface. Never export `CODEX_API_KEY` as a persistent variable in jobs that run untrusted code.

## Enforcing isolation org-wide

Only the built-in Bash sandbox is enforceable by Claude Code itself, via managed settings (MDM file or Claude.ai server-managed settings):

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false,
    "network": { "allowManagedDomainsOnly": true },
    "filesystem": { "allowManagedReadPathsOnly": true }
  },
  "permissions": { "disableBypassPermissionsMode": "disable" }
}
```

Boolean keys are managed-wins. **Array keys merge across scopes**, so developers can still widen `excludedCommands`, `allowRead`, and `allowedDomains` unless you set the `allowManaged*Only` locks — and `excludedCommands` has no such lock at all, so keep that list short. Containers and VMs are enforced only by device management/software allowlisting, never by the CLI. Scope managed sandbox config to macOS/Linux; native Windows fleets need WSL2 or a container.

## Reference files

- `references/bash-sandbox-config.md` — full `sandbox.*` settings schema: filesystem prefix and precedence rules, `filesystem.disabled`, credential deny/mask (`extract`, `injectHosts`, `onExtractNoMatch`), network options, escape hatch, troubleshooting table. Read before writing any sandbox settings block.
- `references/sandbox-runtime.md` — `srt` install/CLI/library use, complete config schema, Seatbelt vs bubblewrap vs Windows WFP mechanics, dual-proxy egress design, documented limitations. Read when isolating MCP servers/hooks or when a container is not an option.
- `references/devcontainer-isolation.md` — devcontainer.json security properties, auth persistence, org policy delivery, and `init-firewall.sh` rule-by-rule. Read when building or reviewing a containerized dev environment.
- `references/egress-and-secrets.md` — hardened `docker run` flags, gVisor/Firecracker/cloud topology, credential-injection proxy patterns, the full Claude Code egress domain table, proxy/CA/mTLS env vars. Read for any network-policy or secrets question.
- `references/codex-sandbox.md` — OpenAI Codex CLI sandbox modes, approval policy interaction, and managed `requirements.toml`. Read for cross-vendor or multi-agent fleet questions; for Codex operation beyond isolation, go to the `codex` skill.
- `references/versions/claude-code-2.1.md` — which sandbox feature landed in which Claude Code 2.1.x release. Read before recommending a feature to a pinned fleet.

## Diagnostic scripts

- `scripts/01-sandbox-readiness.sh` — read-only preflight: platform, bubblewrap/socat/ripgrep presence, AppArmor userns restriction, seccomp filter, and which sandbox settings files exist.
- `scripts/02-egress-allowlist-check.sh` — read-only reachability probe for the required Claude Code domains from inside a sandbox/container; reports allowed vs blocked so a firewall can be verified rather than assumed.

## Sources

- https://code.claude.com/docs/en/sandboxing
- https://code.claude.com/docs/en/sandbox-environments
- https://code.claude.com/docs/en/devcontainer
- https://code.claude.com/docs/en/agent-sdk/secure-deployment
- https://code.claude.com/docs/en/network-config
- https://github.com/anthropic-experimental/sandbox-runtime
- https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh
- https://containers.dev/implementors/json_reference/
- https://www.anthropic.com/engineering/claude-code-sandboxing
- https://learn.chatgpt.com/docs/sandboxing
- https://learn.chatgpt.com/docs/agent-approvals-security
- https://learn.chatgpt.com/docs/enterprise/managed-configuration

Fetched: 2026-08-05
