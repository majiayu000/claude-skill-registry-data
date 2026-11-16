---
name: verify-pstack
description: "Prove that a change to a pstack skill in this repo works by running it in real Claude Code, Codex, and Grok sessions in the pstack testbed through Orca, then reading their session records. Use after editing anything under skills/ and before calling the change verified, or for verify-pstack. Internal to this repo, not shipped."
metadata:
  internal: true
---

# Verify pstack

pstack is a set of skills, so the app under test is an agent following one. A proof is a real session in the testbed, started the way a user starts it. Its evidence is what the session did (tool calls, subagents, Orca workers, its reply) and what it left behind (files, worker states, the shared `select-model`). This skill holds the commands, the rules for shared state, and the feature map in [`features/`](features/README.md). It is for agents changing this repo. `metadata.internal` keeps the `skills` CLI from offering it to users.

## Pick the runs first

Every run spends usage, and an earlier session already hit its monthly limit. Choose the runs from this table before you start anything. Add a run only when one fails or the change spans several rows.

| What changed | Minimum proof | Feature |
| --- | --- | --- |
| Wording only: a typo, a split sentence, a heading nothing links to | The four repo checks. No run. | |
| An `orca` command or flag that a skill tells agents to run | `check-orca-commands`, then one run that reaches the command | the feature that runs it |
| `poteto-mode` routing, the playbook list, or a playbook's steps | One entry check routed to that playbook, Claude terminal | [entry](features/entry.md) |
| The Subagents section of `poteto-mode` | One spawn check for each case the changed sentence covers (same agent, another agent with Orca, no Orca) | [spawn](features/spawn.md) |
| How `select-model` is read, or the fallback when it is missing | One runtime check with `select-model` present. Add the fallback check only when the missing-skill sentence changed. | [runtime](features/runtime.md) |
| `setup-pstack` or `create-model-selection-skill` | One generator run, Claude terminal, fake home | [generator](features/generator.md) |
| The generator's link question | One generator run that answers the link question, fake home | [generator](features/generator.md) |
| A cross-model skill (`arena`, `swarm`, `interrogate`, `reflect`, `architect`, `how`, `why`) | One run of that skill on a small read-only task, Claude terminal. `why` and `architect` stop at the plan. | [cross-model](features/cross-model.md) |
| `deslop`, `control-ui`, or `control-cli` | One run of that skill on its fixture, Claude headless, or an Orca terminal for `control-ui` | [team-kit](features/team-kit.md) |
| A line only Codex reads differently (`$name`, `update_plan`, `CODEX_HOME`, rollout paths) | The same check once more, Codex terminal | the same feature |
| Behavior only an Orca chat shows | The same check once more, `--surface chat` | the same feature |
| A rule for a session without Orca | The same check once more, plain surface, or headless when Orca must not start it either | the same feature |

The four repo checks run for every change, from the repo root:

```bash
node scripts/audit-cursor-deps.mjs
node scripts/check-orca-commands.mjs
node scripts/lint-rewritten.mjs
node scripts/prune-cursor-deps.mjs --check
```

Rules for spending:

- A run is one environment and one prompt.
- `vp launch` starts a terminal unless told otherwise, because the CLI can close a terminal and cannot close a chat.
- It starts Claude on `sonnet` and Codex on `gpt-6.1-sol`, both at `low`. These are the models of the earlier recorded runs, at the lowest effort each offers. Orca starts Grok on its own config and refuses both flags.
- A run that fails because the model skipped a step the skill states plainly may be rerun once with `--model default --effort default`, which leaves both flags off, to tell a weak model from unclear text. Report both runs. In a terminal that means the model and effort the user pinned in the product's settings (`opus` in `~/.claude/settings.json` today), so the rerun costs more than the first run. This happened in the first proof of this skill: `sonnet low` skipped the Orca check that the default effort made (see the runtime feature's Gotchas).
- Never repeat a passing run to be sure. Never run the whole map. The map lists what can be proved, not what must be.

## Where things are

- **Testbed.** `~/Documents/pstack-testbed`, a git repo outside this one. `calc.js` has a deliberate off-by-one and `calc.test.js` fails on it. `.agents/skills/<name>/` holds copies of this repo's skills and `.claude/skills/<name>` is a relative link to each copy. Codex reads the copies from `.agents/skills/`, Claude Code through the links. `.claude/settings.json` turns auto memory off so runs do not share memory, and `.codex/config.toml` does the same for Codex (`features.memories`, `memories.use_memories`, `memories.generate_memories`), which loads it because the testbed is a trusted project. Until 2026-10-27 Codex memory was on, and the Orca Codex account's memory held summaries of the 2026-10-23 testbed runs, including the arena answer and the old grader file names. C-why-131742 cited it. Grok keeps a workspace memory under `~/.grok/memory-v2/workspaces/pstack-testbed-*/`. It had no topics on 2026-10-27, and no per-project switch for it was found.
- **Helper.** `.agents/skills/verify-pstack/scripts/vp.mjs`. Every command below assumes `VP=.agents/skills/verify-pstack/scripts/vp.mjs` from the repo root. It names you, for locks and runs, by the first of these it finds: `VP_OWNER`, `ORCA_AGENT_SESSION_ID` (an Orca chat), `orca-tab:<ORCA_TAB_ID>` (an Orca terminal, which has no session id and keeps its tab id until the tab closes), and `claude-session:<CLAUDE_CODE_SESSION_ID>` (Claude Code anywhere). Set `VP_OWNER` when none is there. `$VP whoami` prints the name and how another session reaches you. The lock stores that contact.
- **Evidence.** `~/.cache/verify-pstack/evidence/<run id>/`. It sits outside this repo so no record gets committed, and in a hidden folder away from the testbed so a driven agent does not come across an earlier verdict. Until 2026-10-27 it was `~/Documents/pstack-testbed-evidence`, next to the testbed, and the F8-interrogate-171911 reviewers found it by searching the home folder. A hidden folder only makes that less likely, since an agent with a shell can read the whole home folder. Keep prompts from pointing anywhere near it.
- **Sample `select-model`.** [`fixtures/select-model-sample/`](fixtures/select-model-sample/), the output of generator run G-161639 on 2026-10-23 (Claude, Codex, and Grok, Orca present, links and proof skipped). It has no `references/` and points at `../resolve-capability/SKILL.md`. In a fake home that path holds nothing, so a reader takes its fallback to the folder that holds `poteto-mode`. In this computer's real home it resolves to the global install's copy, so a run that follows the link reads the global `resolve-capability`, not the testbed's (C-int-152804 and C-int-154641 did, while C-why-131742 and C-arena-155437 read the testbed's). It records both ways to start Grok: an Orca worker with no flags, or `grok -p` with a model and effort. Its `SKILL.md` is stored as `SKILL.sample.md` so no agent finds it as a skill, and it holds no `.verify-pstack-sample` file. `vp` renames `SKILL.md` and writes that marker, with the owner, each time it places the sample. Regenerate it with the generator feature when the template or the products' start methods change, because a stale fixture steers spawn checks (S-plain-160657).

## Shared state

### `select-model`

`~/.agents/skills/select-model` is one path for the whole computer. Every pstack skill reads it, so whatever sits there shapes every run in every session. The user's real one will live there.

- **Real or sample.** A sample carries a `.verify-pstack-sample` file naming its owner. Anything at that path without the file is the user's real skill. `vp` refuses to overwrite, remove, or move a real one except through the stash below.
- **Runs that only read it** (entry, spawn, cross-model, and the runtime check with it present) use whatever is there. `vp launch` records its state, and `vp read` compares. A run whose state changed in between is marked `VOID`. Rerun it.
- **Another session holds the lock.** `vp launch` refuses, because your run would read that session's sample. Wait, or message the owner with the contact the refusal prints: `orca orchestration send --to orca_session_id:<id> --subject "select-model lock" --type question --body "<when will you release it?>" --json` for a chat, or `orca terminal send --terminal <handle> --text "<message>" --enter --json` for a terminal.
- **Runs that need it absent or set to the sample** take the lock first with `$VP sm lock "<purpose>"`. Then one of these.
  - It is absent and the run needs it absent. Run.
  - It is absent and the run needs the sample. `$VP sm place`, or `$VP sm place --from <dir>` for a freshly generated one.
  - A real one is there. Ask the user before anything else. Offer a fake home, which is a stand-in that primes the model with the path, or a stash. On their yes to a stash, run `$VP sm stash --approved "<their words>"`. It moves the real skill to `~/.agents/verify-pstack-stash/select-model-<time>/`, writes a file manifest and a `RESTORE.txt` with the manual steps, and records the stash in the lock. `$VP sm restore` moves it back and checks every file against the manifest.
- **Always finish with `$VP sm release`.** It removes your sample, restores your stash, and frees the lock, in that order. Never end a session holding the lock, whether the runs passed, failed, or were abandoned.
- **Stale lock.** A lock older than two hours, or one whose owner is gone, is the user's call. On their yes, `$VP sm break --approved "<their words>"` removes it and logs the old lock to `lock-breaks.log` in the evidence root. A sample or stash it guarded stays where it was. `$VP sm status` shows both.
- **A fake home sidesteps the lock.** When another session holds the lock and your check only needs `select-model` absent or set to the fixture, run it from a fake home (`$VP fakehome <name>`, with `--sample` for the fixture) and launch with `--fakehome <dir> --ignore-lock`. Add the reader line `vp fakehome` prints to the prompt. Confirm in "select-model touches" that the run read only fake-home paths, and name the fake home as a stand-in in the verdict.
- **Generator runs use a fake home**, never the real path. `$VP fakehome <name>` makes `/tmp/vp-home-<name>/` and prints the prompt line that points the generator there. It needs no lock. Pass `--fakehome` to `vp launch` so cleanup keeps what the generator wrote.

The lock is a JSON file at `~/.agents/verify-pstack-select-model.lock` (owner, purpose, time, placed sample, stash). Without `vp`, create it only when absent (`set -o noclobber`) and delete it only when it is yours.

### The global install

The user installed pstack globally (`npx skills add <repo> -g -a claude-code -a codex -a grok`). Real copies sit in `~/.agents/skills/<name>`, and `~/.claude/skills/<name>` and `~/.grok/skills/<name>` link to them. Claude Code prefers a personal skill over a project skill of the same name, and P-prio-164109 confirmed it: in the testbed, `/poteto-mode` came from `~/.claude/skills/poteto-mode`, not the testbed's freshly synced copy. Its `../resolve-capability/SKILL.md` then resolves to the global copy too.

- A Claude run tests the global copies. `vp sync` still fills the testbed from the working tree, but Claude Code does not read those copies while a global one exists. An uncommitted change never reaches a Claude run.
- To prove a change in a Claude run, commit it, then run `$VP sync --global`. It exports `skills/` at git HEAD to `~/.cache/verify-pstack/head-export` and runs `npx skills add <that folder> -g -a claude-code -a codex -a grok -s '*' -y`. It never installs uncommitted work into the user's real skills. `--dry-run` only exports and prints the command.
- `sync --global` changes the install source the `skills` CLI records in `~/.agents/.skill-lock.json` from the repo path to the export folder. That is why the folder is kept. Say so when you run it. On 2026-10-23 the lock already named the export folder as the source of all 59 pstack skills, so never delete it.
- Never run `npx skills add -g` with `CLAUDE_CONFIG_DIR` set. Under Orca it points at an account profile whose `skills` folder links to `~/.claude/skills`. The `skills` CLI computes each link from the profile path and writes `../../../../../../../.agents/skills/<name>`, which resolves to nothing under `~/.claude/skills`, so Claude Code loses every pstack skill while Codex and Grok still see them. The 2026-10-23 install broke all 58 links this way. `vp sync --global` drops the variable. By hand, run `env -u CLAUDE_CONFIG_DIR npx skills add ...`. `vp doctor` warns about broken links.
- `npx skills add` never removes a skill. One the repo dropped (`orca-harness` on 2026-10-23) stays in the global folders and agents can still load it. `vp doctor` lists such orphans, and testbed copies the repo no longer has. Only the user removes a global one, with `npx skills remove -g <name>`.
- `vp doctor` lists the skills whose global copy differs from HEAD. `vp read` names the copy each pstack skill came from (testbed, global, or fake home) and prints a warning when it is not the testbed's.
- A Codex run read the testbed copy of the skill it was given (`.agents/skills/<name>/SKILL.md`) in every run on 2026-10-27, but took `resolve-capability` from either copy, depending on whether it followed the sample `select-model`'s link (see Sample `select-model` above). So a change to `resolve-capability` reaches a Codex run reliably only after a commit and `$VP sync --global`, as for Claude.
- The `select-model` rules above do not change. A global install puts no `select-model` in place.

### The testbed

- Other sessions launch runs in the same testbed. `vp` finds your session by the run id in the prompt and the launch time, so their sessions never mix with yours.
- Sync only the skills your change touched (`$VP sync <name>...`). A sync replaces the copy another session's run may be reading, so ask before syncing a skill another session is changing.
- A driven agent must leave the testbed's tracked files as they were. `vp read` lists every new change. `vp cleanup --revert` puts back only what your run changed.

## Launch

`$VP launch <label> --agent claude|codex|grok [--surface terminal|chat|plain|headless] --prompt "<prompt>"` starts one session, in a terminal unless `--surface` says otherwise. The run id is `<label>-<HHMMSS>`, with `-2`, `-3`, and so on when another run of that label started in the same second. It goes into the prompt as `[<run id>]`, at the end or wherever the prompt says `{marker}`. A prompt that needs the bare id, such as in a temp path, writes `{id}`. `{testbed}` becomes the testbed's absolute path, and `{home}` the fake home given with `--fakehome`. The launch output, the prompt, and the state before the run go to `run.json` in the run's evidence folder.

What `vp` runs for each surface, so you can run it by hand. `<testbed>` is `$VP_TESTBED`, by default `~/Documents/pstack-testbed`, and `<evidence>` is `$VP_EVIDENCE`, by default `~/.cache/verify-pstack/evidence`.

- **terminal** (Claude or Codex), the default. `orca agent launch --agent claude --worktree path:<testbed> --surface terminal --model sonnet --effort low --prompt "<prompt>" --json`, with `--agent codex --model gpt-6.1-sol` for Codex. Ready when `prompt.outcome` is `handed-to-terminal`. `outcome.handle` is the terminal, and `vp` records its tab for cleanup.
- **chat** (Claude), only for a check about what an Orca chat alone does. The same command with `--surface chat`. Ready when `prompt.outcome` is `journaled`. The result's `outcome.sessionId` is Orca's id for the chat, not the record's file name. A chat outlives the run (see Known limits).
- **plain** (Claude). `orca terminal create --worktree path:<testbed> --title vp-<run id> --command "bash <evidence>/<run id>/plain.sh" --json`. The script unsets every `ORCA_*` variable, swaps each `PATH` folder that holds `orca` for a copy without it, and runs `claude --dangerously-skip-permissions --model sonnet --effort low`. Ready when `$VP screen <run id>` shows `ORCA vars left 0, orca on PATH: none` and the prompt is running. The first screen can be the folder trust prompt or the bypass-permissions warning. Read it, move to the accepting option with `$VP key <run id> down`, and confirm with `$VP key <run id> enter`. Codex has a plain recipe in the script that no run has used yet. `--keep-orca-cli` unsets the variables but leaves `orca` on `PATH`, as in a terminal or desktop app outside Orca on a computer that has Orca installed. The screen then shows `ORCA vars left 0, orca on PATH: <path>`. When an `ORCA_*` variable is left, or `orca` is still on `PATH` without `--keep-orca-cli`, the script prints `vp: ORCA vars left <n>, orca on PATH: <path>` and exits before the agent starts.
- **headless** (Claude or Codex), the one surface that needs no Orca. `vp` starts `<evidence>/<run id>/headless.sh` itself through the user's login shell (`$SHELL -lic`), detached in its own process group, writes its output to `headless.log` in the run's folder, and records the process id and its start time in `run.json`. The shell starts from an empty environment (`HOME`, `USER`, `LOGNAME`, `SHELL`, `TERM=dumb`, a system `PATH`, and `LANG` and `TMPDIR` when set) and reads the user's profile and rc files. So the user's own settings apply and the calling session's do not. The script clears Orca as the plain script does, without `--keep-orca-cli`, because an rc file can put Orca's folder on `PATH`. It refuses to start the agent if a calling session's marker (`CLAUDECODE`, `CLAUDE_CODE_ENTRYPOINT`, `CLAUDE_CODE_SSE_PORT`, `CLAUDE_AGENT_SDK_*`, `CODEX_THREAD_ID`) is still set, and logs `vp headless: ORCA vars left 0, session markers left 0, orca on PATH: none, shell: <shell>`. It then runs `claude -p --dangerously-skip-permissions --model sonnet --effort low "<prompt>"` or `codex exec --skip-git-repo-check -C <testbed> -m gpt-6.1-sol -c model_reasoning_effort="low" --dangerously-bypass-approvals-and-sandbox "<prompt>" < /dev/null`. Session records stay on, because `vp` finds the run by its marker in them. Just before the agent starts, the script writes the `CLAUDE_CONFIG_DIR` and `CODEX_HOME` it starts it with to `headless-env` as NUL-ended `NAME=value` fields (an empty value when unset), because an rc file can move the record away from where `vp`'s own environment points. `vp` searches there as well as in its usual folders. `vp wait`, `screen`, and `cleanup` treat the run's process as running only while its pid is alive with the start time `run.json` recorded. When `ps` cannot answer, as in a sandbox that refuses it, or no start time was recorded at launch, `wait` keeps waiting and says so once, and `cleanup` signals nothing. `$VP screen <run id>` prints the end of the log. Grok has no headless recipe. A verdict on a headless run names the surface, and its Not covered line says that headless runs do not cover an interactive `ask-user`, since nobody can answer the session mid-run, or a background wake after the process exits.
- **Grok** as the driven session: `orca agent launch --agent grok --worktree path:<testbed> --surface terminal --prompt "<prompt>" --json`, with no model or effort. G-entry-131737 was the first, on 2026-10-27. Grok took `/poteto-mode` as a slash command and ran `grok-4.7` at `xhigh` from its own config. Before the prompt it stopped at its folder trust screen ("Do you trust the contents of this directory?"), because Orca does not pre-trust the worktree for Grok. `vp wait` then shows no record. Read `$VP screen`, and answer with `$VP key <run id> enter` (the first option is "Yes, proceed"). Grok remembers the answer per folder, so the testbed no longer asks.

Prompts:

- Claude takes `/name <args>`. Codex takes `$name <args>`. Quote a Codex prompt with single quotes so the shell keeps the `$`.
- A prompt bounds the scope (read-only, plan only, stop after a step) and answers every question the skill will ask, so the run never stops to wait. A terminal run that asks anyway can be answered with `$VP key`. A chat or a headless run cannot be answered from the command line.
- A prompt never tells the agent what the skill under test should make it do. "Read select-model first" in a prompt turns a check into a demonstration.
- The feature files keep prompts that already ran. Use them verbatim so results compare across runs. They are in Korean because the user works in Korean.

Known limits:

- No Orca command closes a chat. `orca terminal close --terminal <handle>` takes terminal handles only, and a chat handle (`structured-agent-session-...`) gets `terminal_handle_stale`. Every chat run stays in the testbed until the user closes it in Orca's window. That is why runs default to a terminal.
- `orca terminal close --worktree path:<testbed> --all --json` failed with `terminal_close_incomplete` and left orphaned terminal records that the CLI cannot remove. Do not use it for cleanup.
- Orca refuses `--model haiku --effort low` ("Agent claude model haiku does not support effort low"), though its catalog lists `low` for haiku. Use `--effort default` with haiku.
- Orca starts a terminal Claude with `--dangerously-skip-permissions`, so a terminal run does not stop at a permission prompt. S-pair-154658 started an Orca worker from a terminal Claude without one. A run you start some other way can stop at one, and `vp wait` exits 4.
- An Orca terminal sets `ORCA_CLI_BIN_DIR` but not `ORCA_CLI_COMMAND` or `ORCA_AGENT_SESSION_ID`. It sets `ORCA_TAB_ID`, `ORCA_TERMINAL_HANDLE`, and `ORCA_PANE_KEY`. An agent started in it inherits the same.
- A tab closed in Orca's window while its agent is alive leaves the PTY running with no tab. `orca terminal close` then answers `terminal_handle_stale`. `vp cleanup` types the agent's exit command and then `exit` into that PTY. It ended Claude (`/exit`) this way in S-ro-155230 and R-missing-155347, where the tab was already gone at cleanup. It ended Codex (`/quit`) in every Codex run on 2026-10-27 and Grok (`/exit`) in G-entry-131737. That day every terminal from `orca agent launch` had no tab at cleanup, though nobody closed one in Orca's window.
- Codex can end a turn with "Selected model is at capacity" (`server_overloaded`) partway through. C-swarm-152445 lost its report that way after both workers finished. Typing `$VP key <run id> "계속"` resumed it, as a user would, and the verdict names the nudge. `vp wait` reports such a run finished at once, because the record still ends with the aborted turn, so watch `$VP screen` until the new turn ends.
- Codex encrypts the brief it passes to `spawn_agent`, so the rollout never shows what a child was told. Each child writes its own rollout whose `session_meta` names the parent thread. `vp read` lists those children with their model and effort and copies their rollouts into `records/`. It finds `claude -p` and `grok -p` workers by matching the brief against records started during the run, wherever they ran (an arena runner runs in its `/tmp` folder), including ones a script started from an argument list.
- `vp wait` can report a run finished while the session waits on its own background job (a CLI worker, a background subagent). F8-interrogate-171911 resumed for ten more minutes after the first `finished`. For runs that start background work, wait with `--quiet 60` and read the summary's `finished:` line before judging.
- The testbed's git history once held an old `RUNBOOK.md` and `check.py`, and a driven agent could read them with `git show`. On 2026-10-27 the history was cut to one root commit and the old objects were pruned. Never commit a grader, a verdict, or an expected answer to the testbed, not even to delete it later.
- Claude Code rewrites its process arguments soon after it starts, so a run's process cannot be found by the run id in its command line.
- Closing a terminal without `--tab` left its tab in place. The tab came back under a new handle with the agent still running. `vp cleanup` closes with `--tab` and matches the run's terminal by its handle or by the `[<run id>]` marker in the tab title. The title alone is not enough, because Claude Code retitles its tab. It never matches by tab id, because Orca gave the id of a tab closed in its window to another session's terminal.

## Doctor

`$VP doctor` is read-only. It checks that Orca answers and matches the snapshot in `orca/VERSION`. When Orca does not answer, that is a `warn` line saying only `--surface headless` runs can start, the terminal and chat checks are skipped, and every other check still runs. It checks that the testbed is clean, which testbed copies differ from the working tree, that each `.claude/skills/<name>` link is the relative one, the state of `select-model` and its lock, any stash or fake home left behind, that `claude`, `codex`, and `grok` run, and your runs that were never cleaned. It compares each global copy under `~/.agents/skills` with git HEAD and lists orphans. It also counts the testbed's open terminals and chats. It warns about a terminal whose title carries a run id, about orphaned or disconnected terminal records, and about open chats, and says when only the user can close them in Orca's window. Run it before the first launch and again after anything surprising. Fix every `FAIL` line before you launch. With Orca down, a check whose runs are all headless can go ahead. A `warn` line about a copy is a problem only when your run reads that skill.

## Drive

1. Pick the runs from the table at the top.
2. Run `$VP doctor`. If it warns that Orca does not answer, launch only `--surface headless` runs, or start Orca first.
3. Sync the skills your change touched: `$VP sync <name>...`. `$VP sync --check <name>...` only reports. When `vp doctor` reports a global install, Claude runs read the global copies instead, so commit the change and run `$VP sync --global` before a Claude run (see The global install).
4. Set the `select-model` state the feature names, by the rules in Shared state.
5. Launch with the feature's prompt.
6. `$VP wait <run id>`. Exit 0 means finished. Exit 2 means still running, so call it again. Exit 3 means the session is waiting on a question. Read it with `$VP screen <run id>`. The question is the finding. Answer it with `$VP key` only to let the run finish. Exit 1 means a headless run's process ended without a finished record, and `vp` prints the end of `headless.log`. Exit 4 means a terminal run stopped at a permission prompt. `vp` prints the screen. Answer it with `$VP key`, and report it, because a driven agent should not need one. Give the Bash tool a timeout above `--timeout` (240 seconds by default). A foreground `sleep` longer than about 45 seconds is blocked in Claude Code, and `vp wait` polls inside node instead.
7. `$VP read <run id>`. Judge each pass criterion in the feature file against `summary.txt`, and write `verdict.md` (shape below).
8. `$VP cleanup <run id>`, then `$VP sm release` if you took the lock.
9. Report each run id, its verdict, and the evidence path. A failure names the tool call number and the skill sentence it contradicts.

## Evidence

`vp` writes these into `~/.cache/verify-pstack/evidence/<run id>/`.

- `run.json`, with the prompt, the launch output, and the `select-model`, lock, and testbed state at launch.
- `summary.txt`, the readable account: models and effort, the first prompt, every tool call (an `&` marks a Claude call sent in the same message as the one before, so the two started together), the skill files named in tool calls, every touch of `select-model`, the last todo list, native subagents with their model and effort, Orca workers with what was requested and what model actually ran (read from the worker's own record), CLI workers started from the shell (`grok -p`, `codex exec`, `claude -p`, `claude --bg`) with the model their output names, or for `grok -p` the model and effort in its own Grok session record, temp folders the run created, and the final reply.
- `facts.json`, the same as data.
- `records/`, copies of the session record, its subagent records, and each worker's own record.
- `fakehome/` and `tmp/` from cleanup, `testbed-residue.txt` when the run changed the testbed, and `cleanup.log`.
- `verdict.md`, which you write. Its first line is the verdict, because `vp runs` shows it.

```markdown
PASS|FAIL|VOID <run id> <feature> <sub-feature ids>
- <criterion>: pass|fail. <evidence: summary.txt call N, or a quoted line of the reply>
Environment: <agent> <surface> <model> <effort>, select-model <state>.
Stand-ins: <fake home, low effort, a model other than the user's>.
Not covered: <what this run did not exercise>.
```

Proof standards:

- Drive the real path. The prompt goes to a real session through the slash command or `$name`. Reading the skill yourself and predicting what an agent would do proves nothing.
- Capture the action and the result. The tool calls show the action. The reply, the files, and the worker states show the result.
- Check side effects from their own source. A worker's model comes from Orca's worker record and the worker's session record, not from the command text the agent wrote. A written file is checked on disk.
- A failure stays a failure. Do not reword the prompt until it passes. A precondition the testbed lacks goes into that feature's Gotchas, and the run is reported as failed.
- Name every stand-in. A fake home, low effort, or Sonnet in place of the user's model are differences a real user's run would not have.
- Records and evidence stay out of the repo.

## Cleanup

`$VP cleanup <run id>` does these, and logs each to `cleanup.log`.

- Closes the run's terminal with `orca terminal close --terminal <handle> --tab --json`, then checks the testbed's terminal list until the run's handle and marker are gone. A terminal still listed after that is reported as one the user must close in Orca's window.
- Leaves a chat open, because no Orca command closes it, and says so.
- Stops a headless run's process group if it is still running, with `SIGTERM` and then `SIGKILL`. It calls no Orca command for it. It sends nothing to a run already cleaned, or when the group's leader is alive with a start time other than the one `run.json` recorded, because the pid then belongs to another process. It also sends nothing when `ps` fails or no start time was recorded at launch, logs that the leader is unknown, holds the fake home copy-and-remove, the `--tmp` removals, and the `--revert` restore, because the run may still be using them, and leaves the run uncleaned, so a later `vp cleanup` can finish. A group whose leader has exited but whose members still run is still the run's, so it is stopped.
- Stops every Orca worker the run started with `worker-start` that has not settled.
- Copies the fake home into the evidence and deletes it.
- Lists temp folders the run created and named. Check that they are the run's, then rerun with `--tmp` to copy each into the evidence and delete it.
- Saves any new testbed change to `testbed-residue.txt`. `--revert` restores those paths.

It never touches `select-model`. `$VP sm release` does that. It prints the evidence folder's contents at the end, so you can see that the proof survived. Never kill a process by name, and never close a terminal `vp` did not record.

## Helpers

`vp.mjs` is executable. `$VP help` prints this list.

| Command | What it does |
| --- | --- |
| `doctor` | The read-only check above. |
| `sync <name>... \| --all [--check]` | `rsync -a --delete` each `skills/<name>/` from the working tree into the testbed, and create its `.claude/skills` link if missing. |
| `sync --global [--dry-run]` | Install `skills/` at git HEAD globally with the `skills` CLI. Never uncommitted changes. |
| `sm status` | The state of `select-model`, the lock, and any stash. |
| `sm lock "<purpose>"`, `sm place [--from <dir>]`, `sm remove`, `sm stash --approved "<words>"`, `sm restore`, `sm release`, `sm break --approved "<words>"` | The `select-model` rules above. |
| `fakehome <name> [--sample] [--from <dir>]` | A home under `/tmp` and the prompt line that points the generator at it. `--sample` puts the fixture inside. |
| `launch <label> --agent <a> [--surface terminal\|chat\|plain\|headless] --prompt "<p>" [--model <m>\|default] [--effort <e>\|default] [--fakehome <dir>] [--ignore-lock] [--keep-orca-cli]` | Start one run, in a terminal unless `--surface` says otherwise. `default` leaves that flag off. `--ignore-lock` is only for a run that never reads `select-model`. |
| `wait <run id> [--timeout 240] [--quiet 20]` | Poll the record until the turn ends and the record has been quiet for `--quiet` seconds. Exit 0 finished, 1 a headless process that ended unfinished, 2 still running, 3 a question, 4 a permission prompt. |
| `read <run id> [--width 160]` | Write and print the summary. `read --record <file> [--agent <a>]` reads any record without a run. |
| `screen <run id>`, `key <run id> down\|up\|enter\|"<text>"` | Read and type into a terminal or plain run. `screen` on a headless run prints the end of its log. |
| `cleanup <run id> [--tmp] [--revert]` | The cleanup above. Safe to run twice. |
| `runs` | Every run in the evidence root, with its owner, state, and verdict line. |
| `whoami` | The owner name `vp` uses in this session, and how another session reaches you. |

Records, for reading by hand:

- Claude Code: `~/.claude/projects/<testbed path with every / as ->/<session>.jsonl`. Tool calls are the `tool_use` blocks of `assistant` messages. Subagents keep their own records and a `.meta.json` with type, model, and effort under `<session>/subagents/`.
- Codex started by Orca: `~/Library/Application Support/orca/codex-accounts/<id>/home/sessions/YYYY/MM/DD/rollout-*.jsonl`, not `~/.codex/sessions`. Tool calls are `response_item` entries of type `function_call` or `custom_tool_call`. This Codex wraps shell commands in an `exec` call that runs JavaScript, and `vp` pulls the `cmd` strings out of it. `turn_context` holds the model and effort. `orca search "<run id>" --agent codex --since <iso time> --fresh --json` finds a session when the index is on.
- Grok: `~/.grok/sessions/<URL-encoded cwd>/<session>/`. `summary.json` holds `current_model_id` and `reasoning_effort`, and `chat_history.jsonl` the turns. Orca reports `launch.effective` as null for Grok, so this record is the only source for the model that ran.
- An Orca worker's first prompt starts with `You are working inside Orca, a multi-agent IDE. You are a dispatched worker.` and names its task id. `vp` uses that to tell workers from driven sessions and to find each worker's own record.
