---
name: agentic-vps
category: compute
description: >-
  Provision and harden a fresh Linux VPS into an autonomous-agent dev host using
  the capability-preserving model — the box IS the sandbox: full agent autonomy
  inside it (non-root sudo user, open egress, YOLO mode, any toolchain), contained
  by ISOLATION (non-root + VPN-only access + snapshot + no-long-lived-secrets),
  not by restricting the agent. Composes an idempotent provisioning script, a
  staged firewall/VPN lockout-safe sequence, and a deterministic verification gate.
  USE WHEN setting up a new VPS/cloud box for Claude Code / agentic development,
  hardening a machine to run coding agents unattended, "set up another machine
  like srv1692698", provisioning an agent dev host, or auditing whether a box
  meets the agentic-host security invariants. NOT FOR generic server hardening
  with no agent on it (that's standard CIS/Lynis), desktop/laptop setup, or
  Kubernetes/multi-tenant clusters. Triggers on "set up a vps for agents",
  "agent dev host", "harden a box for autonomous agents", "new agent machine",
  "provision agentic vps", "agentic-vps".
latent_only: false
metadata:
  version: 0.1.0
  provenance: BRO-1550 (srv1692698 hardening session, 2026-06-25/26)
---

# agentic-vps — provision & harden a box for autonomous agentic development

The verb for "make me another machine like the one we just set up." Distilled
from the srv1692698 session (BRO-1550). It does **not** reimplement server
hardening — it encodes the *capability-preserving model* and the *lockout-safe
staging sequence* so a future agent reaches for it instead of re-deriving it.

## The one invariant

> **The box IS the sandbox.** Security comes from *containing the blast radius*
> (non-root agent user · VPN-only access · snapshot rollback · no long-lived
> secrets in the agent's reach), **not** from *restricting the agent* (no tight
> egress allowlist, no permission prompts, no seccomp leashes). The agent gets
> the same freedom it has on a local machine — full sudo, open network, any dep,
> YOLO mode — because a compromise is *contained and reversible*, not *prevented*.

This is the user's standing constraint: **"secure but don't limit capability/autonomy."**
The model and its threat-model rationale live in
`research/entities/concept/lethal-trifecta-denial.md` and the playbook at
`docs/security/2026-06-24-vps-agentic-hardening-playbook.html`.

## Hard rules (the lockout-safety sequence)

These are non-negotiable ordering constraints. `scripts/staging_check.py`
enforces them deterministically — a plan that violates them fails the gate.

1. **Snapshot before any risky change.** A rollback point must exist first.
2. **VPN up + verified BEFORE closing public SSH.** Bring up the mesh VPN
   (Tailscale/WireGuard), then in a *second, independent* session confirm
   `ssh agent@<vpn-ip>` works — *only then* remove the public :22 rule.
3. **Allow the new path before removing the old.** UFW: `allow in on <vpn-if>`
   before `delete allow OpenSSH`. Edge firewall: add the VPN rule, verify, then
   drop TCP/22 and sync.
4. **Verify on a fresh connection after every SSH/firewall change** — never
   assume the change is safe from the session that made it.
5. **Out-of-band recovery must exist** (cloud Browser Terminal / recovery mode)
   before public SSH is closed, since there is no SSH fallback afterward.

## Procedure

### Phase 0 — pre-flight (latent: per-provider control plane)
- Identify the provider control plane (Hostinger VPS MCP, AWS, etc.).
- **Snapshot** the box (Hostinger: `VPS_createSnapshotV1`).
- Confirm out-of-band console access exists.

### Phase 1 — provision (deterministic: `scripts/provision.sh`)
Run as root over SSH — idempotent, safe to re-run:
```
ssh root@<host> 'AGENT_USER=agent bash -s' < scripts/provision.sh
```
Creates the non-root agent user (passwordless sudo + docker), installs the
toolchain (Node, Bun, Rust, gh, Docker, Claude Code + sandbox-runtime),
generous resource caps (host-survival, not throttle), a `bypassPermissions`
Claude config, and git identity. Tailscale is installed but **auth is
interactive** (prints a login URL).

> The config also sets `denyRead` on credential dirs, but that **only takes
> effect if you flip `sandbox.enabled=true`** — in the default capability-
> preserving (sandbox-off) mode it is inert. The *primary* secrets protection is
> **no long-lived secret in the agent's env** (Phase 2: interactive OAuth, scoped
> tokens), which `verify.py`'s `no_secrets_in_env` gate actually checks.

### Phase 2 — credentials (latent: user authenticates interactively)
The user SSHes in and logs into the CLIs themselves — **never paste long-lived
broad keys into env**:
- `claude` → `/login` (OAuth, stored in `~/.claude/.credentials.json`)
- `gh auth login && gh auth setup-git` (prefer a **fine-grained PAT** scoped to
  specific repos over a broad `repo` OAuth token)

### Phase 3 — perimeter (deterministic order; see Hard rules)
- `tailscale up --hostname=<name>` → user authorizes the printed URL.
- Verify `ssh agent@<tailnet-ip>` in a fresh session.
- UFW: `allow in on tailscale0` + `allow 41641/udp`, then `delete allow OpenSSH`.
- Edge firewall: add UDP 41641, remove TCP/22, sync.

### Phase 4 — verify (deterministic: `scripts/verify.py`)
Collect facts from the box and assert the capability-preserving invariants:
```
python3 scripts/verify.py --host agent@<tailnet-ip> [--public-ip <ip>]
```
Gates (required): non-root agent user · resource caps set · Tailscale up ·
public :22 closed · no long-lived secret in agent env. Recommended: snapshot
exists · sandbox config present · git identity set.

## What's deterministic vs latent

| Deterministic (scripts + tested) | Latent (agent judgment) |
|---|---|
| `provision.sh` — idempotent install steps | which provider / control plane |
| `staging_check.py` — lockout-safe ordering | which toolchains this box needs |
| `verify.py` — invariant evaluation | how the user authenticates (OAuth vs PAT) |
| the 5 hard rules | when to defer Tier-3 monitoring |

## Anti-rationalization

| Excuse | Reality |
|---|---|
| "Just close :22, the VPN's up." | Not until `ssh agent@<vpn-ip>` is verified in a *second* session. `staging_check.py` fails the plan otherwise. |
| "Lock the agent down hard." | That violates the one invariant. Contain the blast radius; don't leash the agent. |
| "Put the API key in `.bashrc` so it's always there." | Long-lived broad secret in the agent's reach = leakable by any injected command. `verify.py` fails on it. |
| "Skip the snapshot, it's a fresh box." | The snapshot is the only reversibility. Hard rule 1. |

## References
- `research/entities/concept/lethal-trifecta-denial.md` — the security model
- `docs/security/2026-06-24-vps-agentic-hardening-playbook.html` — full rationale
- `docs/security/srv1692698-runbook.html` — operations (access/recover/rebuild)
- `docs/security/srv1692698-provision.sh` — the original instance this generalizes
