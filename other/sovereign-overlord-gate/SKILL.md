---
name: sovereign-overlord-gate
description: When an agent needs to stop, roll back, or restrict access for a human — the real mechanisms are require-tier.sh's tier check, human-gate-policy.md's confirmation gate, and git's own revert/reset. Replaces an earlier design that instructed agents to implement ECDSA-P384 signed commands and a "freeze the swarm" API that was never built.
origin: yana-ai (rewritten 2026-07-03 — see "What changed" below)
license: Apache-2.0
version: 2.0.0
compatibility: yana-ai >= 0.43.0
---

# Sovereign Overlord Gate

## When to Use

- The human wants to restrict a specific command to sovereign/operator-only access
- An agent must block on human confirmation before an irreversible action
- Work needs to be rolled back to a known-good state
- A misbehaving subagent's session needs to end without waiting for it to finish on its own

## Do NOT use for

- Routine task approval — use `human-gate-policy.md`'s per-action confirmation directly
- Anything implying a persistent, always-on agent swarm to "freeze" — this repo runs one synchronous session at a time; there is no background process to suspend (see `agent-communication-policy.md`)

---

## The real mechanism: three separate, already-working tools

There is no single "Sovereign Overlord Gate" API to implement. The three things this skill used to bundle into one fictional class (`SovereignOverlordGate`) are three real, separate, already-working pieces:

| Need | Use |
|---|---|
| Gate a command to a minimum privilege tier | `bash core/gates/require-tier.sh sovereign "<command>"` — real SHA-256-hashed guest/operator/sovereign check |
| Block pending human confirmation | `core/rules/human-gate-policy.md`'s `human_gate()` pattern — a keystroke, not a signed token |
| Roll back to a known-good state | `git revert <sha>` or `git reset` (per `git-push-enforcement.md`'s Rollback Protocol) — gated by the same human-approval rules as any other destructive git operation |
| End a runaway subagent | Nothing to "quarantine" — a Task-tool subagent either finishes and reports, or the turn ends; there's no long-running process to kill (see `subagent-policy.md`) |

## Checking tier before a privileged action

```bash
# Real usage — require-tier.sh is a working script, not a design sketch
bash core/gates/require-tier.sh sovereign "git push origin main"
bash core/gates/require-tier.sh operator  "npm test"
```

`YANA_TIER` is set by `core/gates/identity-gate.sh` via a SHA-256 comparison against a hash stored in the script (never a plaintext secret in the repo) — see that file's own header for setup.

## Blocking on human confirmation

```bash
# human-gate-policy.md's real pattern — a terminal prompt, not a cryptographic exchange
human_gate() {
  local action="$1" detail="$2" risk="${3:-medium}"
  echo "Action: $action"; echo "Detail: $detail"
  read -r answer < /dev/tty
  [[ "$answer" =~ ^[Yy]$ ]] || { echo "Blocked by human gate."; exit 1; }
}
```

## Rolling back

```bash
# The real "restore to baseline" — no Merkle snapshot API, just git
git log --oneline -10          # find the known-good commit
git revert HEAD --no-edit      # never force-push, never git reset --hard on shared history
git push
```

## Anti-Fake-Pass Checklist

- [ ] Privileged command actually ran through `require-tier.sh`, not just documented as requiring it
- [ ] Irreversible action actually paused for a real human keystroke via `human_gate()`, not auto-approved
- [ ] Rollback used `git revert`/`git reset` — never claimed a "Merkle snapshot restore" that doesn't exist in this codebase
- [ ] No new signing/token/nonce scheme introduced for this — if a genuine need for cryptographic command authentication ever arises, that's a fresh design proposal, not a revival of this skill's old ECDSA-P384 sketch

## What changed

The original version of this skill instructed agents to implement `signSovereignCommand()`/`verifySovereignCommand()` (ECDSA-P384 over SHA384, 60-second expiry, nonce-replay tracking), a `SovereignOverlordGate` class dispatching `FREEZE_SWARM`/`WIPE_AGENT_STATE`/`FULL_ROLLBACK`/`RELEASE_QUARANTINE`/`EMERGENCY_SHUTDOWN`, and a `SovereignDeadManSwitch` class polling hourly for 72 hours of sovereign inactivity. None of that code exists anywhere in this repo, and the skill was teaching agents to write it as if completing a partially-built system — the same gap `core/rules/62-sovereign-overlord-gate-law.md` and `core/rules/50-financial-deadman-switch-law.md` had, all three now fixed together on 2026-07-03. The commands this skill exists to serve (restrict access, block-and-confirm, roll back) are real needs with real, already-built answers — see the table above.
