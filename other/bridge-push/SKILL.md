---
name: bridge-push
description: Use when the user wants to send/push/transfer/upload a folder or files from the local machine to the VPS (or pull the other way) and a peer Claude Code runs on the VPS. HYBRID model — the two instances coordinate over Claude's built-in Remote Control (SendMessage), and the file bytes move over git (preferred) or rsync/tar-over-SSH, verified with a manifest. Triggers on "push this folder to the VPS", "send files to the VPS", "transfer <dir> to the server", "upload to VPS", "copy to the remote".
---

# bridge-push (hybrid)

Move files to the VPS with a spoken handshake. **Coordination rides Claude's
built-in Remote Control (`ListAgents` + `SendMessage`) — no relay, no SSH tunnel
for the talking.** The **bytes** ride a real transport that preserves them
exactly: git (preferred) or rsync/tar over SSH. Both ends verify a manifest.

> Why not send files over SendMessage? That channel carries text through an LLM,
> so exact bytes aren't guaranteed. Inline only tiny text files, and only with a
> sha check (see "Inline escape hatch"). For a real folder, use git or rsync.

Transport-agnostic helpers in `scripts/`:
- `bridge-transfer.sh <src> <ssh_host> <dest> [--delete]` → **the atomic byte-path**:
  opens ONE ssh connection, transfers, verifies every file's checksum on the VPS,
  then closes the connection. Exit 0 = VERIFIED, 1 = MISMATCH. Prefer this.
- `bridge-manifest.sh <path>`  → `FILES/BYTES/SHA` fingerprint (for manual checks).
- `bridge-push.sh <src> <ssh_host> <dest> [method] [--delete]` → transfer only, no verify.
- `bridge-recv-prep.sh <dest>` → VPS: create dest, report free space + readiness.

## Preconditions (check once)
1. **Find the peer:** `ListAgents`. Identify the VPS session (ask the user which
   one if the name isn't obvious, e.g. `vps-myapp`). Note its name/id.
2. **Is it online?** Remote Control sessions show `offline` when not connected.
   If offline → tell the user to open/connect the VPS Claude session (Remote
   Control on). Do NOT proceed blind. (If it must work offline, fall back to the
   bridge relay — see "Offline fallback".)
3. **Byte transport available?** Prefer git if the app is a repo both can reach.
   Else confirm `ssh <alias> true` works from local for rsync.

## Shared journal (MCP)
If the `journal` MCP server is registered, use it as the source of truth:
`journal_read()` at the start, `claim(who, "push:<dest>")` before transferring
(so two pushes don't collide), `journal_log(who, "PUSH", "<name>@<sha>", "VERIFIED")`
after a verified transfer, then `release`. `who` is your identity (local/vps).

## Coordination is turn-based
`SendMessage` hands control to the peer; you resume when it replies. So the
handshake is: you send → your turn ends → the VPS Claude acts and SendMessages
back → you're re-invoked with the reply. Always tell the peer **who to reply to**
(your session name from `ListAgents`) inside the message.

## Workflow — SENDER (local, has the files)
1. **Fingerprint:** `scripts/bridge-manifest.sh <local_path>` → keep `FILES/BYTES/SHA`.
2. **Request** via `SendMessage({to: "<vps-session>", message: ...})`:
   > "PUSH_REQUEST name=<basename> files=<n> bytes=<b> sha=<sha>. Where on the VPS
   > should this go, are you ready to receive, and is it a git repo (so I can push
   > a branch)? Reply to session `<my-name>`."
3. (Turn ends.) On the VPS's reply — `READY dest=… [git remote=…] ssh_hint=…`:
4. **Move the bytes + verify in one shot (SSH path, preferred when you have SSH):**
   `scripts/bridge-transfer.sh <local_path> <ssh_host> <dest>` — this opens the
   SSH connection, transfers, verifies every file arrived (remote checksums ==
   local), and closes the connection. Read its exit code:
   - **exit 0 / VERIFIED** → the files are on the VPS and proven complete. You did
     the verification yourself over SSH; the VPS Claude need not re-check.
   - **exit 1 / MISMATCH** → re-run it (rsync resumes); if it keeps failing, surface
     the error to the user (disk full? permissions?).
   (`--delete` only if the user wants the remote to mirror the source exactly.)
   **git path instead:** commit + push the agreed branch/sha; `SendMessage` the VPS
   "pushed <sha> to <remote>/<branch>, run `git pull`" and let it verify its pull.
5. **Tell the peer you're done and continue:** `SendMessage` → "VERIFIED ✅ files at
   <dest>/<name> (sha=<sha>, <n> files), ssh closed. Continuing." Then resume your
   own work — the transfer is closed out.
6. If you used the git path and the VPS reports `MISMATCH`, re-push and let it
   re-pull. Report the final state to the user.

## Workflow — RECEIVER (VPS, says hi)
You are re-invoked by an incoming `SendMessage`.
1. On `PUSH_REQUEST`: pick/confirm a destination, `scripts/bridge-recv-prep.sh <dest>`
   (free space + readiness). **Create only the empty dest — change nothing else.**
   `SendMessage` back to the sender's session:
   > "hi from vps 👋 push to dest=<dest> (git remote=<…> if repo). I'm ready.
   > Expecting <n> files sha=<sha>."
2. On `PUSHED …`: pull the bytes (`git pull`, or it already arrived via rsync),
   then **verify:** `scripts/bridge-manifest.sh <dest>/<name>` vs the sha you were
   sent. `SendMessage`:
   - match → "RECEIVED ✅ <dest>/<name>, <n> files, sha matches."
   - mismatch → "MISMATCH ❌ got <x>/<y>, expected <n>/<sha>. Re-send."

## Inline escape hatch (tiny text files only)
For 1–3 small text/code files with no git/ssh handy:
- Sender: include each file's path + contents in the `SendMessage` body, and the
  per-file sha (`shasum -a 256 file`).
- Receiver: `Write` each file, then `shasum -a 256` it and compare. If any sha
  differs, reject and ask for git/rsync instead — the text channel corrupted it.
Never do this for binaries, many files, or anything you can't eyeball-verify.

## Offline fallback (peer not connected)
If the VPS session is `offline` and can't be brought online, use the durable
bridge relay for coordination instead of `SendMessage` (same handshake, via the
`bridge` CLI). Bytes still go over git/rsync. See claude-bridge README.

## Guardrails
- **Never overwrite silently.** If `<dest>/<name>` exists on the VPS, say so and
  ask before pushing (especially with `--delete`).
- **Manifest is truth.** "PUSHED" ≠ "received"; only a sha match closes it.
- **Secrets:** flag `.env`/keys before pushing. `.git` is skipped by the manifest
  but IS transferred by rsync/tar — say so if it matters.
- If the peer can't be found/confirmed online, or SSH/git fails, STOP and surface
  it — don't transfer blind.
