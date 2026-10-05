---
name: sync-claude-accounts
description: Distribute full OAuth Claude Code credentials (claude-accounts.json) from a single designated refresh-authority Mac to the rest of a fleet, and operate the scheduled automation that does it — the com.claude.fleet-refresh and com.claude.fleet-health LaunchAgents, their logs, and the proactive refresh that keeps receivers from ever rotating a token themselves. Use when syncing or propagating Claude Code logins across Macs or a fleet, when setting up, auditing, or reading a cycle of the recurring credential push, when a scheduled push seems to have stopped, when checking whether the fleet is healthy, or when the user mentions claude-accounts.json, cswap import, cux add, claude-swap, refresh authority, or fleet-refresh-credentials. To repair an account that is already dead — "re-login needed", EXPRD, null headroom — use the refresh-claude-account skill instead.
---

# Sync Claude Accounts

Distributing Claude Code OAuth credentials across a macOS fleet, and running the scheduled
automation that keeps them alive. The push mechanism and the agents that drive it are one
system, documented together.

> **The 29 hard-won constraints that make this fiddly live in [REFERENCE.md](REFERENCE.md).**
> Read it when something surprises you — an import that reports success but changes nothing, a
> `keychain unavailable` that isn't a lock, a cux slot number that doesn't match cswap's.

## The model this skill implements

Three decisions hold this together. Changing any one breaks the other two.

1. **Full OAuth credentials only — never setup-tokens.** Automatic rotation is driven by
   usage data. `cswap auto` is *purely usage-polling*, and cux is built around the `/login`
   credential bundle (`accessToken` + `refreshToken` + `expiresAt` + full scopes). A
   setup-token carries `user:inference` alone, so `/api/oauth/usage` answers **403** and the
   account is permanently unmeasurable — invisible to both rotators. Setup-tokens simply do
   not fit the model; the export must contain OAuth accounts.

2. **One machine refreshes; the rest only consume.** An OAuth refresh token is single-use and
   rotates server-side on every use, so N machines sharing an account means N−1 eventually get
   `invalid_grant`. Designating a single **refresh authority** that pushes its live credentials
   to everyone else removes the race at the source — a machine that only spends *access* tokens
   never rotates anything. This is the actual fix and it is independent of which rotator you run.

3. **cux provides unattended session continuation.** `cswap auto` only swaps credentials; it
   never wraps the `claude` process, so it cannot resume a session, retry a failed call, or
   wait out a reset. cux does (`auto_resume`, `auto_message`, `retry_on_api_error`,
   `wait_for_reset`, reactive rate-limit swapping), which is why this skill registers every
   account with cux rather than leaving rotation to cswap. **Do not run `cswap auto` as well** —
   two controllers swapping the same accounts fight each other.

## Where to run this

**On the refresh authority.** This skill and `refresh-claude-account` both belong on that one
machine:

- `refresh-claude-account` repairs a dead account there and emits `claude-accounts.json`.
- this skill distributes that file to the receivers.

Repairing or exporting on a *receiver* is wasted work — the authority's next push overwrites it.
Pick a machine with a GUI session (the keychain is readable without SSH gymnastics, and
interactive re-login is possible when an account needs it).

## Quick start

```bash
scripts/push-claude-accounts ~/claude-accounts.json \
    mac-mini-m2 archs-mac-mini 10.0.0.42
```

Per machine this: uploads the file to `/tmp/claude-accounts.json` (mode 600), installs
`~/.local/bin/sync-claude-accounts` if absent, runs it, and deletes the credentials file.
`127.0.0.1` / `localhost` / `local` / the machine's own hostname are handled with `cp`
and direct execution — no SSH. **Do not list the authority itself as a target**: it is the
source of the export, and importing its own credentials back over itself is at best a no-op.

To run the per-machine step alone (already on the box):

```bash
~/.local/bin/sync-claude-accounts            # defaults to /tmp/claude-accounts.json
```

> **Before you push, check two things.**
> 1. **No dead accounts in the export.** The recurring push uses `IMPORT_FORCE=1`, which
>    overwrites every receiver — so publishing a dead slot destroys working copies elsewhere.
>    `cswap list | grep -c 're-login needed'` must print `0`. Repair with
>    `refresh-claude-account` first.
>
>    **That count is a proxy, not the danger itself.** It reads cswap's *strike flag*, which is
>    permanent once set and says nothing about whether the credential still works. The actual
>    precondition is "no receiver holds a working copy I am about to overwrite." When the count
>    is non-zero, do not stop there — establish both halves directly, because the flag alone
>    will also block the one action that can recover a downed fleet. See "the ABORT interlock
>    can deadlock" below.
> 2. **No setup-tokens in the export.** If every account has an `accessToken` but no
>    `refreshToken`, cswap imports them but **cux cannot register them** — the run stops at the
>    cux step with exit 4, and those accounts would be unrotatable anyway. See point 1 above and
>    "cux cannot hold setup-tokens" below.

> **After you push, verify convergence.** Historically `done: N ok, 0 failed` did **not** mean the
> receivers took the credential — a machine whose active slot was the pushed account kept its old
> one and still reported success. Since 2026-08-19 the per-machine script imports twice and
> checks each slot's live credential against the export, so that case now surfaces as `MISMATCH`
> and exit 3 instead of passing silently.
>
> Spot-check by fingerprint anyway, especially after changing any of this. The in-script check
> confirms each slot at the moment it was made live; an independent read confirms what the
> machine is actually left holding:
>
> ```bash
> security find-generic-password -s "Claude Code-credentials" -w \
>   | /usr/bin/python3 -c 'import json,sys;o=json.load(sys.stdin)["claudeAiOauth"];print(o["accessToken"][-6:],o["expiresAt"])'
> ```
>
> Every machine must print the same value. Any host that differs did not converge; repair it with
> the switch-away/import/switch-back sequence below, then re-check.

## What the per-machine script does

1. Preflight `cswap` + `cux` (including that cux's native binary really downloaded).
2. Classify the export; warn early if it is setup-token-only (cux cannot register those).
3. Unlock the login keychain, *before* any write — cswap degrades to file-only storage if it
   is locked mid-operation, putting the credential where cux cannot see it.
4. Import **twice, around a switch**: switch off the active slot, `cswap import <file>`,
   switch back, import again. A single import cannot update the ACTIVE slot's live login, and
   the switch back clobbers the other slot's store — see the constraint below.
5. Re-probe the keychain, distinguishing `security` rc 36 (locked, retry) from rc 44 (no item
   — which is *not* proof of a setup-token; see below), repairing rc 44 where possible.
6. Discover all accounts via `cswap list --json`.
7. For each: `cswap switch <slot> --force`, **verify the live credential matches the export by
   access-token tail**, then `cux add`. Switch **by slot number, not email** — emails are not
   unique across slots. A mismatch logs `MISMATCH` and sets exit 3 rather than passing silently.
8. Restore whichever account was active before, and delete the credentials file.

## Prerequisites per machine

`uv tool install claude-swap` and `npm install -g @inulute/cux` (which needs Node ≥18 —
`brew install node`). `jq` is used when present; otherwise `/usr/bin/python3` is the fallback.

**`cux` must resolve on a non-interactive SSH PATH, not just in your shell.** The per-machine
script sets `PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"` and then hard-fails
with `cux not found`. A mise-managed node install satisfies an interactive login (mise activates
from your rc file) and fails over `ssh host 'command'`, where nothing activates it — so the
machine looks fine when you check by hand and dies on every push. Symlink it into `~/.local/bin`,
which is first on that PATH:

```bash
ln -sfn ~/.local/share/mise/installs/node/latest/bin/cux ~/.local/bin/cux
env -i HOME="$HOME" PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin" \
    sh -c 'command -v cux'      # must print a path
```

The `env -i` check is the one that matters: it proves resolution with no inherited environment,
which is what the push actually gets. Point at mise's `latest` rather than a pinned version so a
node upgrade does not silently break it.

## Options

| Env | Effect |
|---|---|
| `FORCE_INSTALL=1` | Reinstall `~/.local/bin/sync-claude-accounts` even if present (use after editing it) |
| `KEEP_ACCOUNTS_FILE=1` | Leave the credentials file in place instead of deleting it |
| `IMPORT_FORCE=1` | `cswap import <file> --force` — make the export authoritative on receivers instead of skipping accounts that already exist. Required for the recurring single-writer push |
| `SKIP_IF_CUX_BUSY=1` | Exit 5 without touching anything when a cux session is running, rather than swapping the login out from under supervised work |

## Recurring use: the single-writer refresh authority

Why this runs on a schedule rather than by hand (the model is in "The model this skill
implements" above): receivers must be topped up often enough that none of them ever reaches
its own refresh buffer, because the moment one does, it rotates the token and the fleet
starts dying again.

On this fleet that is `~/.local/bin/fleet-refresh-credentials` on **mac-mini-m2**
(LaunchAgent `com.claude.fleet-refresh`, every 15 min), paired with
`~/.local/bin/fleet-health-check` (`com.claude.fleet-health`, hourly). The push script wraps
this skill: it exports, then calls `push-claude-accounts` with `IMPORT_FORCE=1` per host,
deferring any machine with a live cux session unless its token is nearly expired.

**Pick a machine with stable power and network.** The authority moved off the MacBook Air on
2026-08-28: a laptop sleeps and roams, and the push log showed it dropping whole cycles in runs
of 5, 22 and 43 — up to ~10.75h in which no receiver was topped up at all and, until the same
day, nothing said so. That is how a receiver reaches its own refresh buffer and rotates the
shared token. mac-mini-m2 runs `sleep 0` with `autorestart 1` and still has the GUI session an
interactive re-login needs. The receiver list is simply the fleet minus whichever machine is the
authority, so moving it means swapping one name out of `FLEET_HOSTS` and the old authority in.

**Operating those agents — reading a cycle, what each alert means, changing the cadence — is
covered below**, from "What is running" onward. The push mechanism and the automation that
drives it were separate skills until 2026-08-19; they are one system and are documented together.

Three things that design must respect:

- **Never push from an authority holding a dead account.** `--force` overwrites receivers,
  so publishing a dead slot destroys working copies elsewhere. On 2026-08-17 this machine
  held a dead copy of one account while a single receiver held the only live one — pushing
  would have killed it fleet-wide. `fleet-refresh-credentials` aborts on any `re-login needed` locally.
  Re-seed the authority first with `cswap export <file> --account <email>` from whichever
  machine still has a live copy, then `cswap import <file> --force` — that is Path A of the
  `refresh-claude-account` skill, which is where this repair belongs.

  Caveat, learned 2026-08-19: that abort keys on the *strike flag*, so it also fires when the
  flagged credential still works — and then blocks the only push that could revive a downed
  fleet. Before treating an ABORT as correct, confirm a receiver actually holds a working copy
  worth protecting. See "the ABORT interlock can deadlock" above.
- **Receivers inherit the authority's *remaining* token life**, which sawtooths 8h → 0, so no
  cadence closes the trough completely. A tick landing just before the authority refreshes
  leaves receivers briefly holding a near-expired token. Bound the gap with the interval and
  monitor for it; do not assume it is impossible.

  **This fired on 2026-08-19 and took the whole fleet down.** Timeline, from
  `~/Library/Logs/fleet-refresh.out.log`: the `10:38` cycle correctly HELD (authority had 6m
  of life left — pushing would have synchronised everyone onto one fuse); the authority then
  refreshed at ~`10:40`, rotating the shared refresh token server-side; receivers expired at
  ~`10:45` and refreshed with the now-spent token → `invalid_grant` → permanent strike on all
  four. The next scheduled push was `11:08`, ~23 minutes too late. Every cycle from `11:08`
  onward then ABORTed on the authority's own strike flag — see "the ABORT interlock can
  deadlock", which is what turned a 23-minute gap into a multi-hour outage.

  The interval was cut 30 min → **15 min** on 2026-08-19 in response, and the **proactive
  refresh** below landed the same day. Cadence alone could never have fixed this: the interval
  bounds how long a receiver holds a stale token, but a receiver dies the moment *it* reaches
  its own refresh buffer, which can arrive before the authority's token has even expired.

- **The authority refreshes proactively; that is what makes the design self-sustaining.**
  Nothing used to *drive* the single-writer refresh. claude-swap refreshes only lazily — when a
  token is already inside its 5-minute expiry buffer (`OAUTH_EXPIRY_BUFFER_MS`), and only for a
  slot that is **not** the active one (`oauth.try_fetch_usage_for_account`). So the authority
  coasted to the edge of expiry while receivers held that same token with refresh buffers of
  their own, and whichever got there first rotated the single-use token and struck the rest dead.

  `fleet-refresh-credentials` now mints a fresh token *early* and pushes it in the same cycle:
  once any credential drops below `REFRESH_BELOW` (90m), `proactive_refresh()` exports, calls
  `~/.local/bin/claude-refresh-export` (which uses claude-swap's own
  `oauth.try_refresh_oauth_credentials`), and redistributes. Receivers are handed a fresh ~8h
  token long before anything of theirs comes due, so **no receiver ever has a reason to
  refresh**. A short cadence only made the old race less likely; this makes it unreachable.

  Three things that implementation must respect:

  - **Persist before verifying.** The refresh POST rotates the token server-side, so the
    previous generation is dead the instant it succeeds. `claude-refresh-export` writes the
    result to disk *before* probing it — a credential you hold but could not verify is
    recoverable, one you never persisted is not. An unverified refresh is kept, not discarded.
  - **Sync live → store before exporting.** The export reads *stores*. If the live login is a
    newer generation than the active slot's store, refreshing the store copy POSTs an
    already-spent token and strikes the account dead. `proactive_refresh()` switches away from
    the active slot first, which forces that sync.
  - **`REFRESH_BELOW` must stay ≤ `FORCE_BELOW_SECONDS`.** The moment the authority refreshes,
    every receiver is holding a spent refresh token, so all of them must be overwritten in that
    same cycle. If one instead *defers* for a live cux session and later hits its own expiry, it
    refreshes with the spent token and strikes itself permanently dead. Keeping the refresh
    threshold at or under the force threshold guarantees every receiver is already inside the
    force window whenever a refresh happens. The script checks this and raises
    `FORCE_BELOW_SECONDS` to match rather than proceeding with the thresholds crossed.
- **Only one rotator.** cux is the rotation layer (it is the one that can continue an
  unattended session); `cswap auto` must stay off on every machine. Two controllers swapping
  the same accounts fight, and the resulting swaps look identical to the race this design
  exists to prevent. `cswap auto --once --dry-run --json` is still safe and useful — `--dry-run`
  evaluates without ever switching or writing state, which is what the health check uses.

Exit codes from the per-machine script: `0` ok, `1` preflight/import failure,
`2` keychain locked (import still succeeded), `3` one or more accounts failed — a switch, a
`cux add`, **or a credential that did not take** (`MISMATCH`), `4` imported, but the live login
is a setup-token so cux cannot register it.

`2` and `4` both mean "cswap is fine, cux is not", but only `2` is worth retrying —
`4` is the structural limitation above and will recur on every run.

## What is running

Two LaunchAgents on the authority, both loaded and verified (`last_exit=0`):

| Agent | Cadence | Does |
|---|---|---|
| `com.claude.fleet-refresh` | 15 min | Exports live credentials, pushes to the 4 receivers with `IMPORT_FORCE=1` |
| `com.claude.fleet-health` | hourly | Alerts on dead slots / null headroom / unreachable hosts |

Backing files:

| Path | Role |
|---|---|
| `sync-claude-accounts/scripts/fleet-refresh-credentials` | The push cycle, version-controlled here. `--dry-run` reports what it would do without touching anything. `FLEET_HOSTS="a b c"` targets a different fleet |
| `sync-claude-accounts/scripts/claude-refresh-export` | Proactively refreshes near-expiry accounts inside an export, in place, using claude-swap's own OAuth code. Called by `proactive_refresh()`; must run on claude-swap's venv python, which the caller discovers |
| `sync-claude-accounts/scripts/fleet-health-check` | The monitor, version-controlled here since 2026-08-26. `NOTIFY=0` suppresses the desktop notification. Its `FLEET_HOSTS` default **must stay identical to the push script's** — a machine that is pushed credentials but never probed holds live tokens unobserved |
| `~/.local/bin/fleet-refresh-credentials`, `~/.local/bin/claude-refresh-export`, `~/.local/bin/fleet-health-check` | **Symlinks into the three paths above.** Deliberately not copies: a copy drifts silently, and on 2026-08-19 the deployed script and the repo had already diverged. A broken symlink fails loudly in the matching `.err.log` instead. `fleet-health-check` was the last copy still unmanaged — it was never tracked at all until 2026-08-26, having been missed by the `claude-fleet-health` merge |
| `sync-claude-accounts/launchd/*.plist` | The two agent definitions, version-controlled here with `__HOME__` in place of the home directory (launchd needs absolute paths and does not expand `$HOME`) |
| `~/Library/LaunchAgents/com.claude.fleet-refresh.plist` | Installed copy. `StartInterval` 900 (15 min; was 1800 until 2026-08-19), `RunAtLoad` true |
| `~/Library/LaunchAgents/com.claude.fleet-health.plist` | Installed copy. `StartInterval` 3600 |
| `~/Library/Logs/fleet-refresh.log`, `fleet-health.log` | Per-cycle transcripts |
| `…/fleet-refresh.err.log`, `fleet-health.err.log` | Should stay empty; content here means the agent itself is failing |

Check both are alive:

```bash
launchctl list | grep -E 'fleet-refresh|fleet-health'    # 3rd column = label, 2nd = last exit
grep -vE '^\s' ~/Library/Logs/fleet-refresh.log | tail -8
```

## Installing or re-installing the agents

The plists are checked in as templates, so unlike the scripts they cannot be symlinked —
launchd requires absolute paths. Render and load them:

```bash
REPO=~/github.com/soulmachine/skills/sync-claude-accounts/launchd
for f in com.claude.fleet-refresh com.claude.fleet-health; do
    sed "s#__HOME__#$HOME#g" "$REPO/$f.plist" > ~/Library/LaunchAgents/$f.plist
    plutil -lint ~/Library/LaunchAgents/$f.plist
    launchctl bootout  "gui/$(id -u)/$f" 2>/dev/null
    launchctl bootstrap "gui/$(id -u)" ~/Library/LaunchAgents/$f.plist
done
```

Because the installed copy is a copy, it **can drift** from the repo — the one thing the
symlinked scripts are immune to. Check with the same render:

```bash
for f in com.claude.fleet-refresh com.claude.fleet-health; do
    sed "s#__HOME__#$HOME#g" "$REPO/$f.plist" | diff -q - ~/Library/LaunchAgents/$f.plist \
        && echo "$f: in sync" || echo "$f: DRIFTED"
done
```

## Moving the authority to another machine

Done on 2026-08-28 (MacBook Air → mac-mini-m2). The move itself is small — swap one name out of
`FLEET_HOSTS` and the old authority in, stop two agents, start two agents. What costs time is
that **the outgoing authority has never been a receiver**, so none of the receiver-side setup
exists on it. All three of these were missing and each one fails differently:

| Missing on the ex-authority | How it shows up |
|---|---|
| `~/.claude/unlock-keychain.sh` | Every SSH operation hits a locked keychain (`User interaction is not allowed`), `cswap` reports `keychain unavailable`, and writes degrade to file-only storage where cux cannot see them. It never needed one: as the authority it only touched its keychain from a local GUI session |
| `cux` on a non-interactive PATH | `cux not found` on every push. See "Prerequisites per machine" |
| A current `~/.local/bin/sync-claude-accounts` | Its copy is whatever was installed the last time it *was* a receiver, because `push-claude-accounts` only installs on push targets. Fix with `FORCE_INSTALL=1` |

Order matters, and the one rule is **never two authorities at once** — two machines refreshing
the same account is precisely the race this design exists to prevent:

1. Prepare the incoming machine: `git pull` the repo, symlink the three scripts into
   `~/.local/bin`, and confirm `FLEET_HOSTS` in *both* scripts lists the fleet minus itself and
   plus the outgoing authority.
2. Prove it works before committing to it: `fleet-refresh-credentials --dry-run` from the new
   machine must read every host. A `WARN expiry unreadable` line is the ex-authority's locked
   keychain — fix that before going further.
3. Stop the old one **first**: `launchctl bootout gui/$(id -u)/<label>` for both agents, then
   rename their plists aside so a reboot cannot resurrect a second authority.
4. Start the new one: render the templates with `__HOME__` substituted, `plutil -lint`, then
   `launchctl bootstrap`. `RunAtLoad` fires a cycle immediately.
5. Verify a launchd-driven cycle reaches `DONE ok=N deferred=0 failed=0` and that `launchctl
   list` shows last exit `0` for both. A manual run exiting 0 proves nothing about the agent.

The brief gap in step 3→4 is safe: receivers simply are not topped up for a minute or two.
Leaving the ex-authority *out* of the fleet is what is not safe — it still holds credentials, and
the moment anything runs Claude Code on it, it refreshes and rotates the shared token out from
under everyone.

## Changing the schedule

```bash
launchctl unload ~/Library/LaunchAgents/com.claude.fleet-refresh.plist
# edit StartInterval, then:
plutil -lint ~/Library/LaunchAgents/com.claude.fleet-refresh.plist
launchctl load  ~/Library/LaunchAgents/com.claude.fleet-refresh.plist
```

`RunAtLoad` on the refresh agent means loading it fires a cycle immediately — convenient for
testing, but it also means a reboot does not wait out a full interval.

**`launchctl kickstart` does NOT pick up a changed `StartInterval`** — launchd caches it from
load time, so kickstart only re-runs the job on the old schedule. The unload/load above (or
`launchctl bootout gui/$UID/com.claude.fleet-refresh` followed by
`launchctl bootstrap gui/$UID <plist>`) is what actually applies it. Confirm with:

```bash
launchctl print "gui/$(id -u)/com.claude.fleet-refresh" | grep -i 'run interval'
```

Since the proactive refresh landed, **the interval is no longer the knob that governs safety** —
`REFRESH_BELOW` in `fleet-refresh-credentials` is. Raising it refreshes earlier and keeps more
headroom on the receivers; lowering it squeezes more life out of each token. If you raise it past
`FORCE_BELOW_SECONDS` the script will say so and raise the force threshold to match, because a
refresh with those two crossed can strand a spent token on a deferring receiver. The interval now
just bounds how quickly a *failed* cycle is retried. Do not add a second rotator:
cux is the rotation layer, and `cswap auto` must stay **off** (only its `--dry-run` probe is
used here) — two controllers swapping the same accounts fight, and the result is
indistinguishable from the race.

## Reading a refresh cycle

Each cycle logs one line per host plus a summary:

```
START exported 2 account(s)
  mac-mini-2018: token good for 4h — deferring if cux is busy
  mac-mini-2018: DEFERRED (cux session active)
  archs-mac-mini: token expires in 126m — forcing through any live session
  archs-mac-mini: OK
DONE ok=2 deferred=2 failed=0
```

- **`REFRESH`** lines mean the authority minted a fresh token *before* pushing — the normal,
  healthy path once any credential drops under 90 minutes:

  ```
  REFRESH lowest credential has 84m left (< 90m) — refreshing here first
        REFRESHED work@example.com ...a1b2c3 -> ...d4e5f6, 479m left (probe 200)
        cux resynced: work@example.com (cux slot 1)
  REFRESH complete — lowest credential now 479m
  ```

  `REFRESHED-UNVERIFIED` means the new credential was minted and kept but its probe did not
  return 200 — the credential is still the only live generation (the old one died on the POST),
  so it is deliberately retained. Check the next cycle; if it recurs, the account needs
  `refresh-claude-account`. A `FAILED … refresh error=invalid_grant` means that lineage is
  permanently dead and something else refreshed it — the single-writer invariant is broken.
- **DEFERRED** is normal, not a failure. Registering an account requires making it live, which
  would swap the login out from under a supervised cux session, so a busy machine is skipped —
  *unless* its access token has under 90 minutes left, at which point a momentary swap is
  cheaper than letting it refresh and rotate the token out from under the fleet.
- **A machine deferred every cycle for many hours** is the case to watch. It should get forced
  once its token drops under the threshold; if it never does, the expiry probe is broken.
- **`failed=` non-zero** → SSH or import trouble. Check `fleet-refresh.err.log` first: the agent
  runs without your interactive shell's PATH or ssh-agent, so unattended auth problems show up
  here and not in a manual run.
- **`ABORT`** → the authority itself holds a dead account. It refuses to push rather than
  overwrite healthy copies elsewhere. This is the one that needs you; see below.

**A run of `ABORT`s is a countdown, not a safe hold.** The guard is correct — publishing a dead
slot with `--force` would destroy working copies — but while it holds, *the top-ups stop*. The
receivers keep spending the last credential they were given, and once one reaches its own refresh
buffer it refreshes, rotates the single-use token, and the race the authority exists to prevent
restarts on its own.

That is not theoretical: on 2026-08-19 the authority ABORTed every cycle from Aug 18 15:26 to
Aug 19 02:44 — 11+ hours, at times reporting *2* dead accounts — and by the end two receivers had
each minted their own token for a shared account. The dead account and the drift were one
incident, not two.

So the deadline for repairing an ABORT is roughly the receivers' **remaining access-token life**
(~8h from the last successful push), not "whenever convenient". Check how long you actually have:

```bash
grep -c ABORT ~/Library/Logs/fleet-refresh.log            # how long has it been holding?
grep 'DONE' ~/Library/Logs/fleet-refresh.log | tail -1    # last cycle that actually pushed
```

After repairing, verify the receivers re-converged rather than assuming the next push fixed
everything — a push reports success even where it did not overwrite the live login.

## When an alert fires

| Symptom | Meaning | Fix |
|---|---|---|
| `ABORT … dead on the authority` | The authority can no longer seed the fleet | Repair it with `refresh-claude-account` — Path A (re-seed from a machine that still works) before Path B |
| Receiver has dead slots | The race fired on that machine | Usually self-heals on the next push (`cswap import --force` clears the dead-token strike). If it recurs, the single-writer invariant is broken |
| Null headroom, no dead slot | Usage unreadable — often a stray setup-token (403), sometimes transient rate limiting (429) | Confirm with `cswap list --token-status`; `refreshToken: no` means a setup-token got in and cannot rotate |
| `ALERT <email> has diverged across the fleet` | A machine holds a different generation of that account than the rest — it refreshed on its own, so the single-writer invariant is broken | Re-converge with a forced push (`IMPORT_FORCE=1`), then re-run the check. The per-machine script imports twice around a switch and reports `MISMATCH` (exit 3) if a credential did not take. If it recurs, something on that machine is refreshing outside the authority |
| Host unreachable | Cannot confirm credential health | Not benign — an unreachable machine still holds credentials and may refresh unobserved |
| `ALERT … missed N consecutive pushes` | Delivery to that host has been failing, so it is spending a credential nobody is refreshing | Fix the transport (SSH/scp/network) before it reaches its own refresh buffer. Fires at 4 consecutive misses (~1h), re-alerts every 4; tune with `PUSH_FAIL_ALERT` |

**Never repair on a receiver.** The authority's next push overwrites it. Repair the authority and
let the cycle distribute the fix.

## Monitoring (not optional)

`cswap auto --once --dry-run --json` is a safe read-only probe — it evaluates and reports but
never switches or writes state. Schedule it per machine and alert on:

- **`headroomPct` null for an account** → unreadable usage, caught *before* the account is
  needed. Observed in practice: a probe returning `{"1": null, "2": 35.0}` correctly flagged
  slot 1 while slot 2 was still healthy — days before anything tried to use it.
- **Two machines holding different generations of one account** → whichever is the odd one out
  refreshed on its own, meaning the race is live and the design has sprung a leak. This alerts
  as of 2026-08-28; see below for why the comparison has to be per account.

### Convergence is compared per account, not per live login

Until 2026-08-28 the check compared each receiver's **live** login against the authority's
**live** login. Two machines are routinely active on *different accounts*, so a mismatch there is
usually benign, and a signal that is usually benign can only ever be a note. It duly cost a
confirmed miss: on 2026-08-19 mac-mini-m2 and archs-mac-mini were each holding a **self-minted
token for the same account the authority held**, roughly 1h20m from expiry, and the check logged
nothing actionable. It was found by hand.

Keying on the account removes the ambiguity, because for one email there is no benign reason for
two machines to hold different generations. `fleet-health-check` now reports, per machine and per
slot, the remaining lifetime of every account it holds, groups those by email across the fleet,
and alerts when the spread exceeds `CONVERGE_TOLERANCE_MIN` (default 2 minutes), naming the
outliers:

```
converged: tech@archauto.com — all 6 machines within 1m
ALERT tech@archauto.com has diverged across the fleet — spread 400m across 5 machines,
      majority 480m, outliers: archs-mac-mini=80m, mac-mini-m2=80m
```

Three things about that fingerprint are deliberate:

- **Remaining minutes, not the clock.** `expires 08:34` is rendered in the local timezone of each
  machine — archs-mac-mini prints a different wall time for a byte-identical token — so clock
  times are not comparable across the fleet. The countdown is.
- **Every slot, not just the live one.** The keychain holds only the live login; the other
  account sits in a cswap store. Reading `cswap list --token-status` covers both, which is the
  entire point — the 2026-08-19 miss was on a *non-live* slot.
- **A tolerance, because the countdown is minute-truncated.** Machines probed seconds apart can
  legitimately differ by a minute. A self-minted token was minted at a different moment and
  differs by hours, so 2 minutes separates them cleanly with room to spare.

`cux-backup` is useless for this — those keychain items are not JSON. To spot-check one machine
by hand, the live login can still be fingerprinted directly:

```bash
security find-generic-password -s "Claude Code-credentials" -w \
  | /usr/bin/python3 -c 'import json,sys;o=json.load(sys.stdin)["claudeAiOauth"];print(o["accessToken"][-6:],o["expiresAt"])'
```

**A single null is not proof of a fault.** The usage endpoint rate-limits (429) under exactly
the load a busy fleet generates, and a rate-limited probe reports null for a perfectly healthy
account. Alerting on the first null produces false alarms — seen 2026-08-17, two machines
alerted while `cswap list --token-status` showed every account `fresh, refresh token yes`. A
monitor that cries wolf gets ignored, and then the real event is missed. So separate the
permanent conditions from the transient one:

| Signal | Meaning | Treatment |
|---|---|---|
| `re-login needed` | Refresh token dead — the race fired | Alert immediately |
| `http-403` | Credential lacks `user:profile` — a setup-token got in | Alert immediately |
| `http-429` (named in `fetchErrors`) | Usage endpoint throttled | Note it; **never** counted toward the streak |
| A bare null with no attribution | Cause unknown — could be either | Note it; alert only if it **persists** |
| Host unreachable | Cannot confirm health at all | Alert — it still holds credentials |

`fleet-health-check` implements this in two stages. First it **attributes**: `cswap auto
--once --dry-run --json` names the cause of each null in the poll event's `fetchErrors` map
(`{"headroomPct": {"1": null}, "fetchErrors": {"1": "http-429"}}`), and a null blamed on
http-429 is discarded outright rather than counted — it is a throttled probe, not a sick
account. Nulls with no attribution, or with any other cause, still count: absence of an
explanation is treated as suspicious. Then it **persists**: the surviving *unexplained* count
drives a per-host streak counter in `~/.local/state/fleet-health-nulls` — it increments, a
clean run resets, and it alerts once the streak reaches 3 consecutive runs (~3h hourly).
Early detection survives; the noise does not.

Attribution was added 2026-08-26 after mac-studio-m3 alerted for 4 straight hours on a
429-throttled probe while that very account answered a live `claude -p` call. Counting bare
nulls alone could not tell the two apart, even though cswap had already said which it was.

**Measure the account nearest death, not the live one.** The expiry probe driving the
force-vs-defer decision must take the **minimum across all slots** (`cswap list --token-status`
prints one `expires HH:MM in Xh Ym` per slot). Reading only the live login measures the wrong
thing whenever a machine's two accounts have different expiries: seen 2026-08-17, mac-mini-m2
reported "4h" from its live slot while its *other* slot's stored backup sat 60 minutes from
expiry — so it deferred every cycle, and cux swapping onto that slot would have activated a
dead token and rotated it out from under the fleet.

A healthy probe looks like this — two events per tick, and no nulls:

```json
{"event":"poll","active":{"number":2,"email":"…"},"headroomPct":{"1":35.0,"2":41.0},
 "threshold":90.0,"windowsPct":{"2":{"5h":27.0,"7d":65.0}}}
{"event":"no-switch","reason":"below-threshold","detail":"65% < 90%"}
```

Why this is not optional: the failure it catches is **silent and permanent**. A machine that
loses the rotation race looks fine until something actually calls the API — possibly days
later — and the dead-token verdict strikes on the first failure with no retry
(`AUTH_DEAD_STRIKES = 1`). Treat a gap in monitoring as an outage, not an inconvenience.

Run it by hand any time:

```bash
NOTIFY=0 ~/.local/bin/fleet-health-check     # exit 0 = healthy, 1 = alerts raised
```

## The residual gap this monitoring exists for

Receivers inherit the authority's *remaining* access-token life, which sawtooths from ~8h down to
0 and back. No cadence closes that trough completely: a tick landing just before the authority
refreshes leaves receivers briefly holding a near-expired token, and a receiver that runs Claude
Code in that window **will** refresh and rotate the token out from under everyone.

**As of 2026-08-19 that trough is closed at the source.** The authority no longer waits for its
token to age out: `proactive_refresh()` mints a fresh ~8h token once anything drops under 90
minutes and pushes it in the same cycle, so receivers are topped up long before they could reach
a refresh buffer of their own. Cadence (now 15 min) is a safety margin, not the mechanism.

Keep monitoring anyway. The guarantee holds only while its preconditions do: exactly one machine
refreshing, `REFRESH_BELOW` ≤ `FORCE_BELOW_SECONDS` (or a refresh strands a spent token on any
receiver that defers), and `cux` actually resolvable from the agent's PATH (it is *not* on the
default PATH — it ships under mise-managed node — and without it cux keeps its own stale copy).
A silent regression in any of those looks exactly like the old race, days later.

## Security

The export holds **unencrypted OAuth credentials**. It is written mode 600 and deleted
after import by default. Encrypted exports are rejected up front.

## Related

- `refresh-claude-account` — repair an account that is already dead (`re-login needed`, EXPRD,
  null headroom) and emit the `claude-accounts.json` this skill distributes. That skill owns the
  dead-account symptoms; this one owns distribution and the automation.
- `ssh-claude-auth` — installs `~/.claude/unlock-keychain.sh` (its Approach B). The keychain
  re-locks between SSH sessions, which is why every remote step here unlocks in the same
  invocation. Its Approach **A** (a `setup-token`) must never be used on a fleet machine — cux
  cannot register it and its usage reads 403, so that machine silently drops out of rotation.
- [REFERENCE.md](REFERENCE.md) — the non-obvious constraints catalogue.
