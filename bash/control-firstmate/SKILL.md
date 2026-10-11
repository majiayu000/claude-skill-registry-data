---
name: control-firstmate
description: >-
  Drive one real firstmate session through a captain trace and measure how long each firstmate claim took to become true, with `node tools/fm-drive/drive.mjs run <trace.json>`.
  Use when a verify-firstmate session needs to be driven or timed from an agent, when a firstmate behavior must be proven against a live primary in a throwaway home, or when a new session-tier feature needs a trace instead of a shell script.
  Traces are JSON in the captain's own words, claims come from a closed catalog of home-record predicates, the primary's own words are never a claim, and the driver refuses a trace that only proves startup or steers the primary with internals before it touches Herdr.
user-invocable: false
metadata:
  internal: true
---

# control-firstmate

`tools/fm-drive/drive.mjs` is the session driver.
It clones the checkout into a throwaway home, opens one Herdr pane it owns, starts a real `claude` primary from that pane's own shell, types the captain lines of a trace into it, and waits for each step's claim to hold on the home's own records.
One JSON object on stdout says what held, how long each claim took, what the driver itself cost, and whether the session was the path a real captain gets.

## What the primary gets

The home is what a captain gets.
The driver never touches the clone's hooks, never runs session start before Claude launches, and never writes `data/captain.md`.
The repo's own SessionStart hook takes the helm, as it does for a captain.

The driver supplies one thing, a clean `CLAUDE_CONFIG_DIR` at `<scratch>/claude-config`.
It sits beside the home rather than inside it, so the home holds nothing a captain's checkout lacks.
It holds `hasCompletedOnboarding`, `bypassPermissionsModeAccepted`, folder trust keyed on the home's path, and a theme settings file, so Claude opens without its first-run dialogs.
It also inherits the host `claude.ai` login (the credentials file plus session keys) so a Windows desktop session stays logged in without a setup-token.
The driver does not mutate `~/.claude.json`, and it never logs or archives those values.
`CLAUDE_CODE_OAUTH_TOKEN` (or `CLAUDE_CODE_OATH_TOKEN`, exported as the OAUTH name) goes to the pane when present and is never written anywhere.

## Write a trace

The shipped `register` trace is the smallest real one.

```json
{
  "feature": "register",
  "project": "greeter",
  "steps": [
    { "say": "ahoy! add my project from {{projectOrigin}} as a local-only project called greeter.", "until": "projects.registered:greeter", "budgetSec": 300 }
  ]
}
```

- `say` is captain text typed into the primary; `""` waits without typing; `$relaunch` exits the primary with `/exit` and starts it again in the same pane, the home and any worker untouched.
- A `say` must read as the captain. The driver refuses, with exit 2, only a say that invokes internals outright. It applies NFKC to the say, turns backslashes into slashes, drops each `<segment>/..` pair, lowercases it, and folds every run of characters that are not letters or digits into one separator. It then refuses three things: a path to a file that exists under the driven root's `bin/` (`bin/fm-spawn.sh`, `bin/fm-spawn`, or `fm-spawn.sh`), a path into one of the root's skills, and a root skill marked `user-invocable: false` when it is invoked as a skill (`/name`, `$name`, or `the name skill`). The root's skills are the directories in its top-level `skills/`, its `.agents/skills/`, and its `.claude/skills/` when that is a real directory and not a symlink, and all three sets are read from the root at check time. A path into a skill is the word `skills` followed by the skill's name, so the driver refuses `skills/stow/SKILL.md`, `.agents/skills/stow/`, `.claude\skills\stow`, `.agents/skills/x/../stow` and `.codex/skills/stow` alike.
- The match runs on the folded words, so the path rule has a general side effect. Any say where the word `skills` is directly followed by one of the root's skill names is refused, whatever word comes before `skills` and whatever punctuation sits between them, and a skill name followed by more words counts as that skill. The driver refuses `claude skills stow`, `Claude, skills: bearings please`, `your skills quiet down` and `.agents/skills/stow-extra/` for that reason, while `which skills do you have`, `my skills are rusty`, `skills stowaway` and `claude skillset stow` pass. The refusal happens at `check` time and names what it matched, so the fix is to reword that trace line.
- Everything else passes on purpose, because a string matcher cannot tell coaching from captain language. That includes bare stems (`fm spawn`, `fm–spawn`, `FMSpawn`), `session start` in any spelling, `state/` paths, `tasks-axi`, a `bin/` path to a file that does not exist (`bin/wake-drain`), bare skill words (`project management`, `stuck crewmate recovery`), and a script name broken up by shell quoting or globbing (`bin/fm-sp"a"wn.sh`, `bin/fm-spaw?.sh`, `bin/fm-sp''awn.sh`), which the matcher does not undo, a skill path to a name the root does not have (`skills/zebra/SKILL.md`), and a skill path with a glob in the name (`.agents/skills/*/SKILL.md`). The review rule below covers all of them. Worker tab names such as `fm-greeter-hello` are what the captain sees, so they pass too. [`test/fixtures/steering.json`](../../../tools/fm-drive/test/fixtures/steering.json) lists the refused and allowed spellings.
- **Review rule.** Whoever verifies a trace reads every `say` and rejects coaching, meaning any say that tells the primary which internal command, script, file or skill to use. A string matcher cannot decide this, so the reviewer does.
- Right before each say, `$relaunch` included, the driver evaluates that step's `until`. A claim that already holds fails the step as vacuous, and the say is never typed. At the same moment it evaluates the `until` of every `""` step that waits on that say, and a `""` step whose claim already held then fails as vacuous. A `""` step before any say gets the same check just before Claude launches.
- `until` is one predicate or a `&&` conjunction from the closed catalog at the top of [`tools/fm-drive/lib/predicates.mjs`](../../../tools/fm-drive/lib/predicates.mjs); that file is the single owner of the catalog. Every count is at least 1, because a count of 0 holds before anything happened.
- `budgetSec` is the step's deadline in seconds, and every step needs one.
- `{{projectOrigin}}` is the bare origin of a throwaway project seeded with one commit before launch, named by `project` (default `greeter`); `{{home}}` is the throwaway home's path.
- The driver refuses `pong`, `bypass permissions on`, and a trace whose only claims are `lock.held` with exit 2 before any Herdr call, because they prove the harness started, not that firstmate did anything.
- Pane text is never a claim; a captain line that made the primary say the right thing but write nothing fails its step.
- A worker is dispatched when its record exists **and** its backlog item is In flight (`tasks.count>=1 && backlog.inflight>=1`); a record alone is a spawn still in progress, and relaunching over it lets Claude's exit kill the spawn, whose cleanup then removes the record.
- Every shipped trace that starts a worker waits for it in two steps, so a red run names who was slow. The first step claims the primary filed the captain's request (`backlog.recorded:NAME`, an item tagged `(repo: NAME)` in any backlog section) within 90 s. The second claims the worker started (`tasks.count>=1 && backlog.inflight>=1 && worker.alive`) within 150 s after that.
- `worker.alive` holds only when Herdr has detected an agent in every recorded worker pane (`agent get`, any agent Herdr knows). A pane that still holds only the shell `fm-spawn` opened does not count.

Check a trace without starting Herdr or Claude with `node tools/fm-drive/drive.mjs check <trace.json>`.
`check` clones the root and refuses, with exit 2, a trace whose every `until` already holds on that fresh home; `run` does the same before it starts anything.
The shipped traces are `register`, `ship-local`, `steer`, `watcher-wake`, `pr-land`, `cleanup-refusal`, `restart-primary`, and `scout-report`, under [`tools/fm-drive/traces/`](../../../tools/fm-drive/traces/).

### Claims about what happened after the say

Some atoms count only what happened after the step's say: `turn.ended`, `wake.delivered`, `remote.ahead`, `remote.merged` and `lock.rotated`.
The driver records a baseline right before it types each say or `$relaunch`, and a `""` step uses the baseline of the say it waits on.
These atoms are false at the say by construction, so a step that contains one passes only after something happened.

- `turn.ended` holds once the primary has started a turn after the say and that turn has come to rest (idle, done, or blocked on a question). Before typing a say whose step, or a `""` step waiting on it, uses `turn.ended`, the driver waits for the primary to rest for 2 s, so the turn it times belongs to that say; a primary that never rests within 120 s fails the step. It only times a claim. Pair it with home records that an earlier step already made true. It is refused on a `$relaunch` step and on the first typed say, or any step that waits on them, because session start's own turn would satisfy it.
- `wake.delivered:REASON>=N` holds once `state/.watch-deliveries.log` has gained N lines with that reason since the say. REASON is one of `signal`, `stale`, `heartbeat`, `check`, `needs-decision`, `captain-held`, or `paused`.
- `git.unlanded:NAME>=N` holds while the local branches of `projects/NAME` hold at least N commits that main lacks. It is a plain state atom, not a since-say atom.
- `remote.ahead>=N` holds once main of the `{{remoteOrigin}}` repo is N commits past where it stood at the say. It needs a say that names `{{remoteOrigin}}`.
- `remote.merged>=N` holds once `gh` reports N pull requests merged into that main whose merge commits landed since the say. A commit pushed straight to main never counts, even when GitHub marks its pull request merged, because that merge commit is the pull request's own head. `FM_DRIVE_GH` names the `gh` binary.
- `{{remoteOrigin}}` is one standing scratch repo from `FM_DRIVE_REMOTE_ORIGIN`, a space-separated list of URLs. The driver leases one URL per run with a lease file under the temp directory, mirrors it under the scratch directory, and never creates, resets, or deletes a repo or fetches into the home's own clone. Two runs at once need two URLs; a run that finds every URL leased by a live run exits 3.
- `git.ahead:NAME` is refused unless NAME is the project the driver seeded through `{{projectOrigin}}`. An unseeded clone would count any main as ahead.

Three more atoms read records a behavior leaves behind:

- `session.started` holds when `state/.session-start-complete` names the pid in `state/.lock`, so the session-start digest finished for the session now running.
- `teardown.refused` holds when some `state/<id>.teardown-refused` records a cleanup that refused because it could not prove the work landed. Pair it with `turn.ended` in a following `""` step to also require that the turn ended with the work still there.
- `primary.idle.inflight` holds once the primary rested at least 15 s while a backlog item was In flight and no `done:` line existed yet. The driver judges it from the Herdr status it logs to `primary-turns.log` and the backlog and status records it saw, so a primary that keeps one turn running until the worker is done fails it.

## Run one

```
node tools/fm-drive/drive.mjs run tools/fm-drive/traces/register.json
```

Requirements: a logged-in `claude` on PATH, `herdr` 0.7.4 or newer (protocol 16), `git`, Node 20 or newer, and the same PATH a captain has.
The primary runs the model `FM_DRIVE_MODEL` (default `opus`).
With no `FM_DRIVE_HERDR_SESSION` and no default Herdr server running, the driver starts a throwaway server under a random `fm-drive-<hex>` session and stops it at the end; with a named session it attaches and starts nothing.
`FM_DRIVE_TRANSPORT=socket|cli|auto` picks how the driver speaks to Herdr, over the Unix socket where Node can open it and by spawning the `herdr` binary once per call where it cannot (Windows).
Keep that CLI transport; do not replace it with a socket-only client.
A trace that names `{{remoteOrigin}}` needs `FM_DRIVE_REMOTE_ORIGIN`, for example `FM_DRIVE_REMOTE_ORIGIN="https://github.com/<owner>/<scratch-repo>"`.
The header of [`tools/fm-drive/lib/session.mjs`](../../../tools/fm-drive/lib/session.mjs) lists the other knobs.

Exit codes: 0 every step held, 1 a step did not hold, 2 the trace was refused, 3 the environment failed (Herdr unusable, clone failed, primary never ready) or the launched home was not the captain path.

## Read the result

```json
{ "feature": "register", "trace": "register", "proves": {}, "code": { "sha": "<40 hex>", "dirty": false },
  "wallMs": 0, "pass": true, "readyMs": 0, "operableMs": 0, "predicateMs": 0,
  "health": { "until": "home.clean && tabs.clean && wake.empty && state.settled", "ok": true, "reason": "holds", "restMs": 0, "ms": 0 },
  "fidelity": { "claudeConfig": "clean", "hooks": "repo", "captainMd": "untouched", "model": "opus" },
  "fidelityAtClose": { "hooks": "repo", "captainMd": "untouched", "claudeConfig": "clean" },
  "steps": [ { "say": "...", "until": "...", "ms": 0, "ok": true, "reason": "...", "sayMs": 0 } ],
  "spawns": [ { "id": "greeter-cli-g1", "heldAt": "<iso>", "ms": 0 } ],
  "overhead": { "transport": "socket", "herdrCalls": 0, "spawns": 0, "herdrSpawns": 0, "gitSpawns": 0, "setupSpawns": 0, "cleanupSpawns": 0, "setupMs": 0, "operableMs": 0, "closeMs": 0 },
  "evidence": "/tmp/fm-drive-artifacts/register-<utc>" }
```

The driver measures `fidelity` on the prepared home, before Herdr or Claude starts.
`claudeConfig` is `clean` when the throwaway `CLAUDE_CONFIG_DIR` holds only what the driver wrote: the onboarding, trust and login keys in `.claude.json`, the theme, PATH and `claudeMdExcludes` in `settings.json`, and the inherited credentials file. Anything else reads `carries <entry>, <file>:<key>`.
Claude Code also loads `CLAUDE.md`, `CLAUDE.local.md`, `.claude/CLAUDE.md` and `.claude/rules/` from every ancestor of a session's directory, so `claudeMdExcludes` lists those files for every ancestor of the scratch directory and of the user profile, and one that exists without its exclusion reads `reaches <path>`.
`hooks` is `repo` when the home's `.claude/settings.json` is byte for byte the clone's committed one, else `modified`.
`captainMd` is `untouched` when no `data/captain.md` exists, `written-after-say` when its mtime is at or after the first typed say, and `present` otherwise.
Any other value fails the run with exit 3 before Claude launches, and `error` names the field.
The driver measures `hooks` and `captainMd` again at close as `fidelityAtClose`, before it archives the home, and adds `claudeConfig` read from the transcripts of every Claude session that used the throwaway config.
There `claudeConfig` is `clean` when no session loaded an instruction file from outside its own directory or a skill from the host's `~/.claude/skills`; otherwise it reads `loaded <path>, skill <name>` and fails the run with exit 3, and it reads `unobserved` when a launched primary left no transcript.
There `hooks` must still be `repo`, and `captainMd` may be `untouched` or `written-after-say`, because firstmate records captain preferences in that file itself. A `captain.md` that appeared before the captain said anything is `present`, and it fails the run with exit 3, as a changed hook does.
`pass` is true only when the last `until` held.
`readyMs` is the first launch plus the wait for an operable home (`state/.lock` or `state/.session-start-complete`), and `operableMs` reports that wait alone.
`predicateMs` is the total time spent waiting for claims, and the rest of `wallMs` is the driver's setup, typing, relaunch, and cleanup, which `overhead` breaks down.
A step whose say waited for the primary to rest records that wait as `restMs`, outside the step's `ms`.
`spawns` times each worker spawn apart from the primary.
Its `ms` is how long `fm-spawn` held the task's `state/.meta-<id>.lock`, which it takes before it creates the worker's endpoint and releases after it moves the backlog item In flight.
The driver sees that lock only during its waits, and `ms` is `null` when it never saw the lock released.
Each step's `reason` names the first atom that decided it, so a failed step reads as `home.clean && tabs.clean: home.clean: task records remain: greeter-cli-g1`.
A dead primary fails its step at once, never at the budget.
A parked question fails the step only when that step's claim is still false.
Dead-primary and post-`/exit` detection use last-line shell prompts (`$`, `firstmate $`, `PS C:\path>`, `C:\path>`) plus the pid check; waits use `fs.watch` and do not poll Herdr every second.

The evidence directory keeps `result.json`, `captain.log`, `primary-turns.log` (every Herdr status the driver saw for the primary, with its source), a pane snapshot at every ready, dialog, relaunch and failure, the throwaway server's own log, the Claude config without login material, and `home/state` plus `home/data` as the run left them.
`FM_DRIVE_EVIDENCE` names the directory; `FM_DRIVE_KEEP=1` leaves the home and pane in place for a look.

## How it plugs into verify-firstmate

A trace is the session tier of `verify-firstmate`.
It uses the same throwaway-home clone, the same real primary in Herdr, and the same claims read from `state/`, `data/`, Herdr's tab list and the project's git refs, kept as evidence under the temp directory.
A trace names the inventory rows it proves in `proves`, a map from row id to that row's last proving step.
`trace` is the trace file's name, `code` is the commit the home was cloned from and whether the checkout had uncommitted changes, and `health` is the home's cleanliness after the last step held. The driver first waits up to 120 s for the primary to rest (`restMs`), then up to 60 s for the claim (`ms`), so a cleanup still running when the last claim held is judged once it finishes. A missed health check leaves the exit code alone, and `record` refuses the result. `state.settled` fails on a pending `state/<id>.backlog-close` or a lock left in `state/` other than the session's `.lock`, `.watch.lock` and `.supervise-daemon.lock`.
`node tools/fm-drive/drive.mjs record <result.json>` turns a result into inventory rows as `verify-firstmate` describes; nothing else flips a trace row.
A session script may call the driver instead of `session-lib.sh`'s poll loop when it wants deadlines, file-watch waits and a machine-readable timing record; wire that through `verify.sh` and `coverage.tsv` as `verify-firstmate` describes, and keep one owner for each feature's claims.
Report the result JSON verbatim, then the outcome in the captain's terms.

## Cleanup and safety

The driver closes only what it created.
It exits its primary, stops the home's watcher, closes the tabs labelled for the home's own task records and any workspace it made, removes the treehouse pools whose worktrees live under the home and the task temp directories the records name, archives the records, deletes the scratch directory holding the home and the Claude config, and stops a Herdr server only when it started one.
A run that was killed can leave an `fm-drive-<feature>-*` directory under the temp directory and, when it started its own server, an `fm-drive-<hex>` Herdr session; remove either only when you know the run was yours and is over, and never stop a process by name.
It never writes to the checkout it clones and never merges anything; the primary under test does what firstmate does, in its own home.

## Tests

`node --test tools/fm-drive/test/` runs without Herdr or Claude.
Refusals, including the folded spellings of a `bin/` script path, a skill file path in any of the root's skill directories, a `..` path into a skill and an invoked agent-only skill, and a trace that holds on a fresh home, exit 2 with zero Herdr spawns. Real captain lines and the deliberately allowed respellings pass. Every predicate yields a literal boolean over fixture homes, and a scripted stand-in for the `herdr` binary drives whole traces, including the shipped `restart-primary` one.
The suite also checks that a driven home keeps the committed hooks and gets no `data/captain.md`, that a clone which breaks either fails with exit 3 before Claude launches, that a hook change or an early `captain.md` during the run fails it at close, that a claim already true before its say, or before the say a `""` step waits on, fails as vacuous, that the Claude config dir lands beside the home without touching `~/.claude.json`, that host login files are inherited by presence and shape only, that evidence archival omits credentials, and that the shell-prompt patterns match Git Bash, Linux cwd, and Windows shells.
