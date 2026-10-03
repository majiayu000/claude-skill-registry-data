---
name: agent-client-security
description: Harden native agents running on machines you do not fully control. Covers installer integrity and code signing per platform, OTA update channels with rollback and kill-switch, mTLS with per-agent identity and rotation, local secret storage (Keychain, DPAPI, libsecret), anti-tampering signals, and telemetry hygiene. Invoke when shipping a monitoring agent, RMM tool, CI runner, or IoT controller.
---

# Agent / Client Security

When your code runs on a machine you do not fully control — a customer's laptop, a remote worker's server, a customer-deployed VM, an IoT device — the threat model flips. The local user can read your binaries, intercept your traffic, modify your config, and lie to your control plane about what they are. The defenses are different from web-server hardening.

Applies to: monitoring agents, RMM tools, CI/CD runners on customer infra, MDM agents, deployment agents, IoT controllers, sync clients, backup agents.

## When to invoke

- Shipping a new native agent / endpoint client for the first time
- Designing the installer or update channel for one
- After an incident where a client was tampered with or impersonated
- Auditing an agent product before integrating it (vendor review)
- Reviewing an inherited agent codebase

Pairs with [`distributed-system-audit`](../distributed-system-audit/SKILL.md) for the system view, [`ios-security`](../ios-security/SKILL.md) for mobile specifics, [`mcp-security`](../mcp-security/SKILL.md) for agent-like LLM tooling.

## The threat model — assume the host is hostile (eventually)

For each thing your agent does, assume:

- **The local user can read every file** the agent writes
- **The local user can intercept every network call** (their own machine, their own CA store, their own packet capture)
- **The local user can modify the agent binary** (replace, hook, debugger-attach, decompile)
- **The local user can run multiple instances** of the agent, or instances of a fake agent claiming to be a real one
- **Time on the local machine is what the local user says it is**

You cannot prevent all of this. You can ensure:

- The control plane never trusts the local user's claims without verification
- A compromised agent's blast radius is bounded
- Tampering is detectable, even if not preventable
- The credential the agent holds, by itself, cannot do too much

## Step 1 — Installer integrity

The first interaction between your software and the customer's machine. If you get this wrong, every subsequent control is moot — the user installed something else thinking it was you.

### Distribution channel signing

- **Windows**: Authenticode signing. Use an EV (Extended Validation) certificate for SmartScreen reputation. Cost: $300–700/year. Without a sign, SmartScreen warns the user every install — drives adoption pain *and* normalizes ignoring security warnings.
- **macOS**: Developer ID signing + notarization. Required for distribution outside the App Store. Apple-issued cert via a paid developer account ($99/year). Notarization is automated; do it on every build.
- **Linux package** (deb, rpm): GPG-signed packages, served from a signed APT/YUM repo over HTTPS. Customers verify with your public key (which they import once via your install script).
- **macOS package** (.pkg): Productsign + notarization.
- **Generic binary download**: HTTPS-only, plus a published SHA-256 (or SHA-512) hash next to the download. For higher trust, sign the binary with `cosign` or `sigstore` and publish the signature.

### Installer behavior

- **Verify what you install** — if your installer downloads stages, verify each stage's signature before executing
- **No `curl ... | bash`** as the primary install path. It's catastrophic if the network is hostile or your CDN serves a different file to different IPs. Provide it as a convenience; document the explicit two-step download-then-verify-then-execute path.
- **No SUID / setcap binaries** unless absolutely necessary and audited
- **Document what the installer does** — folders touched, services registered, network calls. Customer security teams will ask.

## Step 2 — Update channel (OTA)

Every agent ages out. The update channel becomes either a feature or a backdoor.

### Required properties

- **Updates are signed** with the same trust roots as the original installer
- **Verification before execution** — the agent verifies the signature on the update package before swapping
- **Rollback path** — if the new version refuses to start or crashes immediately, automatically revert to the previous version
- **Kill switch** — a way to halt rollout if a buggy or compromised update is detected. Server-side (release manager flips a flag) and client-side (agent honors a "do not auto-update until further notice" signal).
- **Version pinning support** — customer-side ability to pin a version range, especially for regulated environments
- **Update server authenticity** — TLS only, with cert validation; or pin the update server's public key

### Patterns to avoid

- **Self-replacement without verification** — agent downloads a binary, replaces itself, restarts. If the download was tampered with, the user has lost.
- **Update over HTTP** — even if the binary is signed, an HTTP channel lets an attacker downgrade to an old vulnerable signed version. Use HTTPS plus version-monotonicity check (new version >= current).
- **Updates with no logging** — when a customer asks "what version am I on, and when did it last update?" you need an answer.

## Step 3 — Code signing per platform

A quick mapping:

| Platform | Mechanism | Cost | Notes |
|---|---|---|---|
| Windows | Authenticode (EV cert preferred) | ~$300–700/yr | EV gives SmartScreen reputation faster |
| macOS | Developer ID + Apple notarization | $99/yr (Apple Developer) | Notarization automated via `notarytool` |
| Linux deb/rpm | GPG-signed packages + signed repo | Free | Customer imports your pubkey |
| Containers | Sigstore / cosign | Free | Increasingly expected for container distros |
| Generic tarballs | SHA-256 published + GPG sig | Free | Old-school but works |

For multi-platform products, plan all of these in advance. Adding code signing after the fact is painful — every existing customer becomes a "warn the user" event when they upgrade.

## Step 4 — Communication: mTLS and per-agent identity

The agent ↔ control-plane channel is where most of the security lives.

### Mutual TLS

- **Server presents a TLS cert**, agent validates against a pinned CA or pinned key
- **Agent presents a client cert**, server validates against an internal CA you control
- **Each agent has its own cert** — never share a client cert across agents

Provisioning the client cert is the hard part:

- **Bootstrap token** issued at install time, single-use, expires fast. Agent presents bootstrap token to a registration endpoint, receives a per-agent certificate, discards the bootstrap.
- **Cert rotation** — issue short-lived certs (24h–7 days) with automatic renewal. A compromised cert is useless after the window.
- **Revocation** — when an agent is decommissioned or compromised, revoke its cert at the control plane. CRL or per-request lookup, not just "trust the cert until it expires."

### Alternative: token-based auth

If mTLS is too operationally heavy, signed-JWT auth with per-agent keys can work:

- Each agent has a private key (generated at install, stored in OS keychain)
- Public key registered with the control plane during enrollment
- Every request signed with the private key (JWT or HTTP-message-signatures)
- Control plane verifies by public-key lookup
- Replay protection: include a nonce and a tight timestamp window

Avoid: API keys shared across agents, agent identity claimed in a header without cryptographic proof, "agent ID + secret" stored on disk where any local process can read it.

## Step 5 — Local secret storage

Secrets the agent needs (private key, refresh token, customer-specific credentials) must survive reboots but resist casual local access.

| Platform | Mechanism | Notes |
|---|---|---|
| macOS | Keychain (`Security.framework`) | ACLs by bundle ID; user must unlock |
| Windows | DPAPI (`CryptProtectData`) | Per-user encrypted; survives reboot |
| Linux (desktop) | libsecret (Secret Service) | GNOME-Keyring / KWallet |
| Linux (headless) | Encrypted file with key from systemd-credentials or a TPM | No standard "keychain" daemon |
| All | OS-level file permissions (`chmod 600`, owned by service user) | Last-resort baseline |

Patterns:

- **Never store secrets in the agent's config file in plaintext**
- **Encrypt with a key tied to the machine** (TPM, Apple Secure Enclave, Windows TPM key) if available
- **Don't share secrets across user accounts** on the same machine
- **Wipe secrets on uninstall** — leftover refresh tokens after the customer removed the agent is a finding
- **Document what the agent stores and where** — customer security teams will ask

A local attacker with root on the machine will eventually get the secret. That's accepted in the threat model. Aim is to raise the bar above "anyone with file-read access can grab it."

## Step 6 — Privilege model

Run with the minimum privilege the agent actually needs.

- **Most operations**: a dedicated unprivileged service user (`_myagent` on macOS, `LocalService` on Windows, a system user on Linux)
- **Privileged operations** (driver install, package install, port < 1024 bind): a separate helper binary that runs elevated, invoked only for the specific operation, with the request validated before execution
- **No always-root daemons** when not required
- **Capabilities-based instead of full root on Linux** where possible — `CAP_NET_ADMIN` instead of root for network tasks

A finding pattern: "agent runs as root because some operation 4 years ago needed it; that operation was removed, agent still runs as root." Audit periodically.

## Step 7 — Anti-tampering signals

Detection, not prevention. A determined local attacker will bypass everything; the goal is to make tampering noisy.

- **Integrity check at start** — agent verifies its own binary hash against the installed manifest. Tampered binary → refuse to start, report to control plane.
- **Configuration signature** — agent's config is signed by the control plane; agent verifies signature before applying
- **Anti-debug / anti-hook checks** — `IsDebuggerPresent` (Windows), `sysctl P_TRACED` (macOS / BSD), `ptrace(PT_TRACE_ME, 0)` race (Linux). Not a defense, a signal.
- **Heartbeat with health attestation** — agent reports its hash, version, config hash to control plane periodically. Anomalies (sudden binary mismatch, unsigned config) are visible centrally.
- **Watchdog process** — a second small process that detects if the main agent is killed/replaced

None of these stop tampering on a determined host. They turn "agent silently subverted" into "agent reported anomalies for two weeks before something happened, we just didn't look at the data."

## Step 8 — Telemetry hygiene

Agents collect telemetry to support themselves. Be careful what leaves the customer's machine.

- **No PII unless contractually agreed** — usernames, paths under `/Users/<name>`, machine names, IP addresses can all be PII
- **No content** of customer data (files, screen, keystrokes) by default
- **No secrets** in crash reports — Windows error reports, Apple's "send to Apple", Sentry, etc., can include memory dumps. Configure to exclude or redact.
- **Document what you collect** in your privacy policy, customer-readable
- **Aggregate / anonymize** where the data is for fleet-wide signals rather than per-machine debugging
- **Customer-side opt-out** for non-essential telemetry

For regulated customers (healthcare, finance, government), this becomes an explicit contractual requirement. Build the off-switch from day one.

## Step 9 — Uninstall and offboarding

The least-attended phase. A leftover agent is a leftover threat:

- **Full uninstall removes secrets**, services, config, scheduled tasks
- **Logs out at the control plane** — agent's cert/key is revoked at the server, not just deleted from the client
- **Customer-visible uninstall confirmation** — they need to know it's gone
- **Re-install does not inherit old state** — fresh install gets a fresh cert, not the old one resurrected from a leftover keychain entry

## Step 10 — Vendor / supply chain

If your agent depends on third-party libraries (most do):

- **Pin versions**, scan with the equivalent of [`dependency-supply-chain`](../dependency-supply-chain/SKILL.md)
- **Audit any library that touches network, crypto, or input parsing** — common CVE areas
- **Beware open-source libraries that bundle native binaries** without signing
- **For commercial SDKs** (analytics, telemetry, error reporting): read the privacy disclosures carefully — they're now part of your privacy story

## Findings on inherited agent products

Recurring patterns when auditing existing agent products:

- Installer unsigned or signed with an expired cert
- Update channel HTTP, or signed but not version-monotonic (downgrade attack)
- Shared API key across all customer installations
- Agent identity claimed by header alone, no cryptographic proof
- Refresh tokens in plaintext config files readable by any local process
- Agent runs as root with no operational need
- Heartbeat unauthenticated — anyone on the LAN can disrupt
- Crash reports include memory dumps with secrets
- No uninstall, or uninstall leaves the cert + tokens on disk
- Update mechanism downloads + executes without signature verification

Each maps to a Step above.

## Checklist

For an agent product going to production:

- [ ] Installer signed (Authenticode / Developer ID / GPG)
- [ ] Notarized (macOS)
- [ ] No `curl | bash` as the default path; documented signed alternative
- [ ] Update channel: HTTPS + signed + version-monotonic + rollback path + kill switch
- [ ] mTLS with per-agent client certs, short-lived, with revocation
- [ ] Bootstrap token single-use, fast-expiring
- [ ] Local secrets in Keychain / DPAPI / libsecret, not plaintext files
- [ ] Minimum privilege; helper binary for elevated tasks
- [ ] Integrity check at start; config signature verified
- [ ] Heartbeat includes health attestation
- [ ] Telemetry documented; opt-out for non-essential
- [ ] No PII or secrets in crash reports
- [ ] Uninstall is complete, server-side cert revoked
- [ ] Re-install gets fresh credentials
- [ ] Third-party libraries pinned, scanned, audited

## What this skill will not do

- Help build agents that evade detection or run without user consent
- Recommend running agents with root / SYSTEM privilege without operational justification
- Endorse "trust the client to enforce policy" for security-relevant decisions
