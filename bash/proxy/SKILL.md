---
name: vpn
description: Meta-skill for secure network tunnel setup, geo-access diagnostics, and leak-aware task resumption by orchestrating shell-scripting, curl-http, wireguard, tailscale, dns, ipinfo, and moltguard. Use when users need controlled VPN switching, region verification, DNS safety checks, and automatic retry of previously blocked workflows.
homepage: https://clawhub.ai
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"🔐","requires":{"bins":["bash","curl"],"anyBins":["nordvpn","mullvad","expressvpn","wg","tailscale"],"env":[],"config":[]},"note":"Requires at least one tunnel path (provider CLI, WireGuard, or Tailscale exit node). Optional security/geo enrichment: MoltGuard and IPinfo."}}
---

# Purpose

Establish a secure, verified path when access is blocked by geo/IP policy, then resume the blocked workflow safely and audibly.

Primary outcomes:
1. detect and classify block behavior,
2. switch to a valid tunnel path with explicit user consent,
3. verify public IP, region, and DNS safety posture,
4. re-run blocked task with bounded retries,
5. return an auditable connection report.

This is an orchestration skill. It does not guarantee legal access to restricted services.

# Required Installed Skills

Core diagnostics/orchestration:
- `shell-scripting` (inspected latest: `1.0.0`)
- `curl-http` (inspected latest: `1.0.0`)

Tunnel path options (at least one):
- provider CLI path (NordVPN / Mullvad / ExpressVPN) via shell orchestration
- `wireguard` (inspected latest: `1.0.0`)
- `tailscale` (inspected latest: `1.0.0`)

Safety and verification extensions:
- `dns` (inspected latest: `1.0.0`)
- `ipinfo` (inspected latest: `1.0.0`)
- `moltguard` (inspected latest: `6.0.2`, optional but recommended)

Install/update:

```bash
npx -y clawhub@latest install shell-scripting
npx -y clawhub@latest install curl-http
npx -y clawhub@latest install wireguard
npx -y clawhub@latest install tailscale
npx -y clawhub@latest install dns
npx -y clawhub@latest install ipinfo
npx -y clawhub@latest install moltguard
npx -y clawhub@latest update --all
```

Verify:

```bash
npx -y clawhub@latest list
```

# Required Credentials and Access

Required access:
- valid account/session for selected tunnel path
- local executable for selected path (`nordvpn`/`mullvad`/`expressvpn` or `wg` or `tailscale`)

Optional keys:
- `MOLTGUARD_API_KEY` (if MoltGuard remote detection mode is enabled)
- `IPINFO_TOKEN` (optional, higher quota geolocation verification)

Preflight:

```bash
command -v nordvpn || command -v mullvad || command -v expressvpn || command -v wg || command -v tailscale
echo "$MOLTGUARD_API_KEY" | wc -c
echo "$IPINFO_TOKEN" | wc -c
```

Mandatory behavior:
- Never fail silently on missing keys/auth.
- Always return `MissingAPIKeys` and/or `MissingCredentials` with blocked stages.
- Continue with non-blocked diagnostics and mark output as `Partial` when needed.

# Compliance Gate (Mandatory)

Before any tunnel switch, confirm and record:
- user authorization to modify network routing,
- acknowledgment of legal/terms responsibility,
- stated purpose for geo-switch (testing, parity checks, privacy hardening).

If acknowledgment is missing:
- do not execute switching commands,
- return diagnostics-only output.

# Inputs the LM Must Collect First

- `blocked_url` or `blocked_endpoint`
- `blocked_task_name` (example: `prediction-market-arbitrage`)
- `target_region`
- `tunnel_path` (`provider-cli`, `wireguard`, `tailscale-exit-node`)
- `provider_or_profile` (provider name, WG profile, or exit-node name)
- `risk_mode` (`diagnose-only`, `switch-and-verify`, `switch-and-resume`)
- `kill_switch_required` (`yes/no`)
- `max_retries` (default: 2)

Do not execute switching before tunnel path and target region are explicit.

# Tool Responsibilities

## shell-scripting

Use as control plane:
- executable detection,
- connect/disconnect wrappers,
- retry and cleanup logic,
- deterministic logging.

## curl-http

Use for protocol-level evidence:
- baseline and post-switch HTTP checks,
- `403`/geo-block signature capture,
- header and status comparisons.

## wireguard

Use when deterministic profile-based tunnels are required:
- controlled profile activation,
- route and AllowedIPs sanity expectations,
- DNS handling awareness in tunnel config.

## tailscale

Use for tailnet and exit-node path:
- `tailscale up --exit-node=<node>`,
- connectivity validation via `tailscale ping`/status,
- fast fallback among available exit nodes.

## dns

Use for DNS leak and propagation sanity guidance:
- resolver checks,
- authoritative vs cached record reasoning,
- explicit leak-risk interpretation when DNS path remains local.

## ipinfo

Use for geo-attestation:
- validate post-switch country/region/ASN,
- compare with baseline,
- provide confidence level for geo-alignment.

## moltguard

Use as prompt/tool security guardrail:
- sanitize sensitive prompt/tool content,
- detect prompt-injection patterns in fetched content,
- reduce accidental secret leakage in workflow logs.

Important limitation:
- MoltGuard is not a VPN manager and not a full network leak detector.

# Canonical Causal Signal Chain

1. `Block Detection`
- baseline request to blocked endpoint,
- classify as `geo_block`, `ip_block`, `auth_block`, or `other_http_error`.

2. `Baseline Snapshot`
- capture pre-switch public IP, country, and resolver context.

3. `Tunnel Path Selection`
- choose one path:
  - provider CLI,
  - WireGuard profile,
  - Tailscale exit node.
- verify binary/auth/profile availability before connect.

4. `Tunnel Activation`
- connect selected path,
- confirm session state from tool output,
- enforce kill-switch preference if available.

5. `Geo and IP Verification`
- compare pre/post public IP,
- verify target country best-effort (`ipinfo.io` + optional token),
- record confidence if country mismatches.

6. `DNS Safety Check`
- check resolver behavior and detect obvious DNS bypass patterns,
- flag risk if DNS appears untunneled in full-tunnel expectation.

7. `Access Retest`
- retry blocked endpoint,
- compare HTTP status/content signatures against baseline.

8. `Task Resumption`
- if retest passes, resume blocked workflow automatically (`switch-and-resume` mode),
- otherwise rotate endpoint/profile once within retry budget and stop with evidence.

Suggested verification commands:

```bash
curl -s ifconfig.me
curl -s https://ipinfo.io/json
curl -I "${BLOCKED_URL}"
```

# Leak and Safety Checks

Minimum checks before success:
- public IP changed,
- target country aligned (or deviation explicitly explained),
- endpoint moved from blocked to reachable/expected-auth state,
- DNS path does not contradict tunnel expectations,
- no unresolved high-risk MoltGuard warning (if enabled).

If kill-switch is required but not supported/verified:
- return `Needs Review` and avoid high-risk task resumption.

# Output Contract

Always return:

- `BlockDiagnosis`
  - block type
  - baseline HTTP evidence

- `TunnelPath`
  - selected path and rationale
  - provider/profile/exit node

- `TunnelStatus`
  - connect state
  - pre/post IP
  - target region match

- `DNSSafety`
  - resolver observation
  - leak risk assessment (`low|medium|high`)

- `SecurityStatus`
  - MoltGuard mode (`enabled`, `gateway-only`, `disabled`)
  - unresolved warnings

- `AccessRetest`
  - post-switch result
  - improvement vs baseline

- `TaskResumption`
  - resumed or blocked
  - reason

- `NextActions`
  - exact commands or account steps for unresolved blockers

# Quality Gates

Before final output, verify:
- diagnosis is evidence-based,
- pre/post network evidence is present,
- retry count respected,
- missing credentials/keys clearly disclosed,
- provider/path limitations explicitly stated.

If any gate fails, return `Needs Revision` with concrete missing checks.

# Failure Handling

- Missing tunnel binary/profile: return `MissingCredentials` with concrete install/profile steps.
- Missing VPN account/auth session: return `MissingCredentials`, skip switching stage.
- Missing `MOLTGUARD_API_KEY` in detection mode: return `MissingAPIKeys`, continue with gateway-only or disabled mode.
- Tunnel connected but geo mismatch persists: one bounded retry with different endpoint/profile, then stop.
- Endpoint still blocked after retry: return full evidence bundle and manual-decision path.

# Guardrails

- Never claim legal or terms compliance on behalf of user.
- Never claim secure state without pre/post verification.
- Never unbounded-loop region hopping.
- Never hide ambiguous or failed access states.
