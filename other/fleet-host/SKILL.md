---
name: fleet-host
category: compute
tier: D
description: >-
  Grow and shrink an agent fleet by GCP VMs with one command each way: `fleet_host.py add <name>`
  creates a private (Tailscale + IAP only), agentic-vps-hardened Compute Engine host with a full lane
  toolchain, per-host revocable credentials and a T3 server, and `remove <name>` drains it, saves
  unfinished work, revokes every credential with proof and deletes everything it created. Dry run by
  default; every step idempotent and re-runnable after a partial failure; all deployment specifics in
  one template file. USE WHEN adding heavy build/verify capacity to an agent fleet, spinning up or
  tearing down a cloud dev host for coding agents, "add a GCP host", "remove the fleet host",
  "grow/shrink the fleet", "mint per-host credentials", "revoke a host's tokens", or auditing that a
  removed host left nothing behind. NOT FOR hardening an existing non-GCP box (agentic-vps), one-off
  GPU jobs (remote-gpu, colab-remote), or Kubernetes/managed runners. Triggers on "fleet host",
  "add host", "remove host", "gcp fleet", "fleet_host", "grow the fleet".
latent_only: false
metadata:
  version: 0.1.0
  provenance: BRO-3651 (design, 3 cross-review rounds, live drill 2026-11-10)
---

# fleet-host — GCP VMs that join an agent fleet ready to work, and leave without a trace

Distilled from BRO-3651. A host joins **ready to run whole lanes, proofs included**, and leaves with
**every credential revoked and proven**. The procedure is code (`scripts/fleet_host.py`); this file is
the contract for running it and for extending it.

## The invariants

1. **The box is the sandbox** (composes `agentic-vps`). The agent gets passwordless sudo, docker,
   open egress and Claude `bypassPermissions`. Containment is the perimeter: the VPC admits only IAP,
   access is Tailscale with a tag whose hosts cannot reach the rest of the tailnet, a secret-free
   snapshot is taken before any credential lands, and `agentic-vps/scripts/verify.py` must pass.
2. **No long-lived secret in any environment.** Tokens live in 0600 files. A `~/.local/bin/<cli>`
   wrapper loads one token into its own process only; shells export only non-secret ids.
3. **Per-host credentials, never copied when they rotate.** Vercel and Neon are minted per host (Neon
   proven unable to read production before delivery). Claude, Codex and gh are interactive logins on the
   host: copying a refresh token breaks one of the two hosts. A shared key (Linear) is an explicit
   template choice.
4. **A ledger, not a hope.** A minted id is recorded before anything else can fail. A record is dropped
   only when the credential is *proven* gone. "Unknown" is never "absent": an unreachable host or a
   failed read blocks, it never counts as revoked.
5. **Never destroy accepted work.** Removal waits for active runs, then pushes dirty trees, local-only
   branches and detached HEADs to `wip/<host>/<worktree>/<branch>-<sha>` (`--push-wip`); otherwise it stops.
6. **An owner step stops the run.** With `--apply`, any `owner`, `blocked` or `FAIL` step ends the run;
   re-running resumes there.

## Procedure

1. **Template.** Copy `scripts/fleet-host/template.example.json` to `~/.config/fleet-host/template.json`
   (or pass `--template`) and fill in every `<...>`: GCP project and admin account, tailnet tag and
   suffix, repos, the credential set, fleet setpoints. It holds no secrets.
2. **One-time owner setup** (each through T3 `request_secret` into the Mac Keychain, never chat):
   - the tailnet policy owns the tag, and the allow-all source excludes it;
   - a Tailscale OAuth client (`devices:core`, `auth_keys`, limited to the tag);
   - a full-account Vercel *minter* token (the CLI's OAuth login cannot mint: 403);
   - `gcloud auth login` and `neonctl auth` on the Mac;
   - a spend approval: `$FLEET_DIR/meta/fleet-hosts/APPROVAL.json` with the approved shapes and ceiling.
3. **Dry run first:** `python3 scripts/fleet_host.py add <name>`. Every step prints `ok`, `would`,
   `owner` or `blocked` against the live state.
4. **Add:** `python3 scripts/fleet_host.py add <name> --apply` **from a terminal**, so the Claude,
   Codex and gh logins can prompt inline. Without a terminal it stops at `cred:logins` and prints the
   exact commands; `creds <name> --apply` resumes them.
5. **Link** the host's T3 environment from the Mac (`t3_environment_link`, `full-access`), record its
   environmentId in the host registry, and let the fleet's governor release the host hold.
6. **Remove:** `python3 scripts/fleet_host.py remove <name> --apply [--push-wip]`. The receipt in
   `$FLEET_DIR/meta/fleet-hosts/<name>/remove-<UTC>.json` lists every step and every revocation proof.

Also: `start` / `stop <name>` (stop refuses while a run or heavy job is active) and
`creds` / `revoke-creds <host>` for any ssh-reachable host.

## Extending

| To add | Change |
|---|---|
| a repo on every host | `repos` in the template |
| a minted credential | a `Minted` subclass in `scripts/fleet_host_creds.py` (`mint`, `listed`, `delete`, optional `scope_ok`, `env`, `wrapper`) plus its name in `credentials.enabled` |
| an interactive login | an entry in `_LOGIN_CMDS` (status, login, logout) and in `credentials.logins` |
| a machine shape | `shapes` (vCPU, GiB); the heavy-slot count follows from it |
| a different cloud project or fleet | another template |

Revocation always covers every credential kind, so a record left by an older template is still revoked.

## Evidence (live drill, e2-standard-8, 2026-11-10)

- Ready in about 2 minutes with all 16 tools present.
- The tailnet tag isolates the host: it cannot reach the other hosts' `:22`.
- 0 secrets in a login shell.
- `verify.py` PASS, including the public `:22` probe.
- A 3 GiB `tsc --noEmit` ran in 9.5 s; two in parallel took 14.4 s each with no swap. The 8-thread,
  15 GB host it relieves ran past 2 h with swap full on the same pair.
- Remove 15/15. An independent re-check found everything gone: Vercel token 404, Neon key unlisted,
  and the service account, IAM bindings, disk, snapshot, secrets and tailnet node all absent.

The drill caught three bugs that review did not:
- the Claude installer pre-writes `settings.json`, so the settings are now merged into it;
- `npx t3 service install` lays down no launcher, so the tool links one;
- a deleted service account answers `describe` with 403, so absence is proven from the account list.

## Validation

```
python3 -m pytest tests/ -v        # 23 tests: ledger, revocation proofs, WIP rescue on real git repos,
                                   # remove safety, template-driven behaviour
bash -n scripts/fleet-host/startup.sh scripts/fleet-host/idle-stop.sh
```

## Anti-rationalization

| Excuse | Reality |
|---|---|
| "Copy the Mac's tokens, it's faster." | Rotating OAuth tokens break one host when the other refreshes. Static tokens copied from the Mac carry its full scope and cannot be revoked per host. Mint, or log in on the host. |
| "The host is unreachable, so its credentials are gone." | Only a NOT_FOUND instance proves the disk is gone. An unreachable host blocks. |
| "Export the token so every tool sees it." | Every child process, postinstall script and error dump sees it too. Use the per-CLI wrapper. |
| "`--push-wip` will sort it out." | It refuses to continue until a re-scan is clean. A failed scan is unknown, never clean. |
