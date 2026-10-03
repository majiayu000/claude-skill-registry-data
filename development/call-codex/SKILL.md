---
name: call-codex
description: Use when the codex CLI should be driven from the agent — as a reviewer giving a second, independent opinion ("ask codex", "call codex", "codex review", "get a second opinion", "challenge this finding"), or as an executor doing a scoped task in the repository ("have codex do this", "delegate this to codex", "let codex implement it"). Covers which flags codex actually understands, how much access each mode needs, how to write a prompt that produces verdicts instead of agreement, and the integration traps that waste a run.
---

# Call Codex

## Two modes

|                     | Reviewer                      | Executor                                 |
|---------------------|-------------------------------|------------------------------------------|
| Job                 | break a claim                 | do a scoped task                         |
| Sandbox             | `read-only`, or a throwaway worktree for experiments | `--approve-for-me` plus what the task needs |
| The output that matters | the disagreement          | the diff                                 |
| Verified by         | reading the code              | reading the diff and running the tests   |

One binary, one set of traps, two different grants and two different prompts. Picking the
wrong grant is the usual failure: a reviewer with write access starts fixing instead of
judging, and an executor without network dies on the first dependency fetch.

## Prerequisites

Check `which codex`. Report and stop if it is absent.

`~/.codex/config.toml` supplies defaults (`model`, `model_reasoning_effort`, `sandbox_mode`,
`sandbox_workspace_write.*`, `approvals_reviewer`, `web_search`). Pass everything the run depends
on explicitly anyway: behavior should not change because a default moved.

## The user's words map to flags

When the user names a setting, pass that setting — never a nearby one without saying so.

- **"ultra"** → `-c model_reasoning_effort="ultra"`. The model catalog describes it as "Maximum
  reasoning with automatic task delegation": codex spawns its own agents, and the run takes
  longer than `max`. `codex debug models` lists which models offer it. If the chosen one does
  not, say so before launching and offer one that does — the run header still prints `ultra`,
  and PR #41206 says the request then falls back to `max`.
- **"fast"** → `-c service_tier="priority"`, the catalog's Fast tier (1.5–2× speed, more usage).
  The legacy value `fast` is accepted too. Neither the run header nor the session file records
  the tier, so a run cannot confirm it was applied.
- **"max", "xhigh", …** → that `model_reasoning_effort`, if the model lists it.

---

# Mode 1 — Reviewer

A second reader for code that is already understood. Not a search tool, not a replacement for
reading the code. It earns its cost in one situation: a claim exists — a review finding, a
diagnosis, a design decision — and an independent model should try to break it.

Codex analyzes; the calling agent implements. Never let this mode write to the tree under
review.

## When to use

- A review produced findings and their reliability matters before acting on them.
- A diagnosis is plausible but unproven and a wrong fix would be expensive.
- Two explanations of the same failure both fit and the difference changes the fix.
- The user explicitly asks for codex.

## When not to use

- To find code or navigate a repository. Grep is faster and free.
- To confirm something already verified. A run costs minutes and real tokens.
- To decide anything the user has already decided.

## Invocation

Write the prompt into the run's own directory, then launch in the background and wait for the
exit — a `max` review usually takes 20–30 minutes (see *Launching and waiting*).

```sh
codex exec -m gpt-6-sol \
  --sandbox read-only \
  -c approvals_reviewer="user" \
  -c model_reasoning_effort="max" \
  -o "$RUN/answer.md" \
  "$(cat "$RUN/prompt.md")" < /dev/null > "$RUN/stdout.log" 2>&1
```

`read-only` holds only while nobody approves escalations. With `approvals_reviewer =
"auto_review"` in `config.toml`, exec runs `approval: on-request`, and the automatic reviewer can
grant a sandbox escalation — the `read-only` reviewer then writes. `-c approvals_reviewer="user"`
makes it `approval: never`. The `approval:` and `sandbox:` lines at the top of stdout show what
the run actually got.

Pinned that way, codex can run terminating read-only commands (`git show`, `rg`, `strings`), but
it cannot start a server, a tmux socket, or a daemon, and builds or tests that write caches fail.
State that limit in the prompt and ask for an exact manual reproduction plan instead — it
produces good ones — or let it run the experiment itself, as below.

## Reviewer that runs experiments

When reading cannot settle a claim — a test that should fail, a build that should break, a
behavior to reproduce — give the reviewer the executor's grant in a checkout nobody else uses:

```sh
git worktree add --detach "$RUN/wt" <SHA>
codex exec -m gpt-6-sol \
  --approve-for-me \
  -c sandbox_workspace_write.network_access=true \
  -c model_reasoning_effort="max" \
  -C "$RUN/wt" \
  -o "$RUN/answer.md" \
  "$(cat "$RUN/prompt.md")" < /dev/null > "$RUN/stdout.log" 2>&1
```

Codex can build, run tests, and write probe files there, and escalations go through the
automatic reviewer. The caller's tree stays untouched, and a fix made along the way cannot land.
The worktree at `<SHA>` also freezes the target. Keep the reviewer's prompt and add three lines:
experiments are allowed, fixes are not; every verdict that rests on a run quotes the command
and its output; list every file created or changed. Afterwards `git -C "$RUN/wt" status --short`
shows what it touched. Remove the checkout with `git worktree remove --force "$RUN/wt"` once the
answer has been read.

## Freeze the target

Name what is under review in the prompt — a commit SHA, a `base..head` range — rather than "the
current working tree". Then leave the reviewed files alone until the answer lands. A review runs
for half an hour; edits made meanwhile turn the verdict into one about a tree that no longer
exists, and codex will say the described state is stale. If the code must move on, commit first
and review the commit.

## Prompt shape

A prompt that only describes the task produces agreement. Four parts produce verdicts.

- **Role and stance.** Say the job is to break confidence in the claim, and that the
  skepticism points at the *claim*, not at the code.
- **Grounding.** Every verdict must quote code, spec text, or a command that was run.
  A verdict without quoted evidence is not a verdict. Inferences must be labeled.
- **A verdict vocabulary.** `CONFIRMED` / `REFUTED` / `PARTIAL` / `UNPROVEN`, one per
  claim, plus: when the stated *mechanism* is wrong but the *conclusion* survives (or the
  reverse), say so explicitly. That distinction is usually the most useful output.
- **Output format.** Name the sections and their order, and say "no preamble". Ask for
  what was MISSED and for a fix ranking that includes what NOT to fix and why.

For anything the code cannot settle — device behavior, runtime timing, a real TUI — ask
for the minimal live reproduction: the exact commands, what to observe, and **what result
would refute the claim**. A claim no observation can falsify is worthless; say that in the
prompt and codex will flag them.

Point codex at file paths, not file contents. It has the repository.

## Reading the result

Report to the user in this order: where codex **disagrees** with the current conclusion,
what it says was missed, and its ranking. Agreement is the least informative part.

Then check the disagreements against the code yourself before changing anything, and stop.
Codex findings are input for a decision, not a work order.

---

# Mode 2 — Executor

Codex does the work: writes files, runs the build, resolves dependencies. Worth delegating a
task that is well-specified, verifiable by a command, and separable from what the calling
agent is doing. Not worth it for anything that needs a conversation to pin down — exec mode
cannot have one.

## Invocation

```sh
codex exec -m gpt-6-sol \
  --approve-for-me \
  -c sandbox_workspace_write.network_access=true \
  -c web_search="live" \
  -c model_reasoning_effort="high" \
  -C /abs/path/to/repo \
  --add-dir /abs/path/to/second/checkout \
  -o "$RUN/answer.md" \
  "$(cat "$RUN/task.md")" < /dev/null > "$RUN/stdout.log" 2>&1
```

What each grant buys:

- `--approve-for-me` — `workspace-write` plus an automatic reviewer for every escalation; it
  sets `sandbox_mode="workspace-write"`, `approvals_reviewer="auto_review"` and
  `approval_policy="on-request"`. Writes land under the working root; the rest of the disk stays
  readable. `--add-dir` adds another writable root for this run;
  `sandbox_workspace_write.writable_roots` in `config.toml` is where build caches belong
  (`~/.gradle`, `~/.konan`, Kotlin caches; in past sessions also `~/.docker` and the Go and pnpm
  caches). Each root saves an escalation per command; without a reviewer the build fails with
  an error that names a path, not a permission.
- `-c sandbox_workspace_write.network_access=true` — dependency resolution, `git fetch`, curl.
  Without it the failure looks like a broken repository, not a blocked socket.
- `-c web_search="live"` — live results from the native web-search tool; the default is
  `cached`. `codex exec` has no `--search` flag; only the interactive CLI does. The older
  `tools.web_search = true` is still accepted and discarded (rule 7).
- `--dangerously-bypass-approvals-and-sandbox` — no sandbox at all. Only when the whole run is
  already isolated (container, throwaway VM). Never on a working machine.

**exec mode cannot ask.** Nobody answers an approval in `codex exec`, and it has no
`-a/--ask-for-approval`. Two settings decide what happens at the sandbox wall:

- `approvals_reviewer="user"` — the run is `approval: never`; the model is told escalation is
  prohibited and works around the wall or reports failure. The reading reviewer uses this.
- `--approve-for-me` — an automatic reviewer decides each escalation. The executor and the
  experimenting reviewer use this,
  because `workspace-write` on macOS blocks `ps`, `pgrep`, `pkill`, and `kill` of any process
  the run did not start, and past sessions show Chromium, Playwright and Docker failing there
  too; the automatic reviewer lets those steps through. It can still refuse — sending the
  repository to an outside service was refused in past sessions — and the run then reports.

Leaving the choice to `config.toml` is the one wrong option: the same command then behaves
differently on another machine. `--approve-for-me` cannot be combined with `-s/--sandbox`. When
a person should decide each escalation, run the interactive `codex -a on-request` instead.

## Containment

Give the executor its own branch or `git worktree` — it costs nothing and makes `git diff` and
`git checkout .` the entire rollback story. Never point one at a tree with uncommitted work
that matters: once its edits mix with yours, they cannot be told apart.

An approved escalation runs outside the sandbox, so its effects are not in the diff — a past
executor stopped and restarted host Docker services. Name in the prompt what it may touch
outside the tree.

## Prompt shape

Execution prompts fail in the opposite direction from review prompts: not agreement, but
scope creep. Pin the edges.

- **Scope.** Which files or directories it may touch, and what to leave alone.
- **Definition of done, as a command.** `./gradlew :module:test`, `kotlin build`, a script
  that must exit zero. A prose goal produces a prose report.
- **Behavior when blocked.** Stop and report; do not invent a workaround, do not widen the
  scope, do not disable a failing test to make the command pass.
- **Conventions.** Spell out the ones this task depends on. Codex picks up `AGENTS.md` on
  its own and nothing else (rule 3).
- **Hands off git.** No commits, no branch switching, no `git add` — leave the working tree
  dirty so the diff is the deliverable. If a commit is wanted, dictate exactly what goes in it.
- **Final report.** What changed and why, what was deliberately not done, what remains
  unverified.

## Reading the result

The final message is a claim; `git diff` is the evidence. Read the diff first, then the
report, then run the done-criteria command yourself. "Codex says it passed" and "it passes"
are two different facts, and only the second one is reportable to the user.

---

# Launching and waiting (both modes)

## One directory per run

Every run gets its own directory, `$RUN`, holding its prompt, its `-o` file, and its stdout log.
Fixed paths collide as soon as two runs overlap: a parallel launch overwrites the prompt
mid-flight, and codex carries out another agent's task. Keep the directory until the answer has
been read and acted on — scratch space under `/tmp` is cleaned within days, and a rerun then has
no prompt to reuse. When the host refuses the launch line as too complex to verify (a
worktree-isolated Claude Code subagent does), write the command into `$RUN/run.sh` and run that.

## Launch in the background, wait for the exit

Launch the codex command itself as the host's background task, with stdout and stderr in
`$RUN/stdout.log`, and keep that task's handle — the background task id, or `$!`. Use the handle
to check on the run and to stop it. Never match by name: `pgrep -f "codex exec"` also matches the
caller's own wrapper shell and every sibling run, and `pkill -f "codex exec"` has killed other
agents' runs mid-flight.

Stdout is not a progress signal. It holds hook lines and tool output, not how far the run is, and
reading it mid-run has cost 38k–132k tokens per look. Wait for the exit, then read `-o`.

Give each run a deadline and decide in advance what happens when it passes. macOS has no
`timeout`; enforce the deadline from the host.

In Claude Code:

- The completion notification of the background task is the wait. Nothing else is needed.
- Never wait in the foreground: a foreground command dies at 10 minutes with `exit 143`, and
  `sleep` polling is blocked.
- If something must watch, use Monitor on the `-o` file with a timeout above the expected run
  time; a Monitor that expires first reports nothing.
- A subagent keeps its turn while its run is live. Ending the turn to wait for the notification
  hands back no report.

Tell the user the realistic range when launching — "20–30 minutes, possibly an hour" — not the
best case.

## A run that produced nothing

Exit 0 is not success. The `-o` file must exist and answer the question. An executor that exits
after a single planning message, or leaves an empty `git diff`, failed. A run stopped from
outside — network loss, the host exiting, a kill — leaves no `-o` and possibly half-done edits:
read `git diff` before relaunching or salvaging.

---

# When the caller is Codex

This skill also runs inside Codex. There a nested `codex exec`, or `codex debug`, dies at startup
because the caller's sandbox blocks it — under `workspace-write` with network access too:

```
WARNING: proceeding, even though we could not create PATH aliases: Operation not permitted (os error 1)
Error: failed to initialize in-process app-server client: Operation not permitted (os error 1)
```

The launch needs the host's escalation (`sandbox_permissions: "require_escalated"`). That
escalation sends the repository to the model provider, and an automatic reviewer has refused it
as data exfiltration when the user had not agreed to it. What worked in practice: ask the user
before the first launch, say what will be sent and why, and cite that consent in the
escalation's justification. A caller that is itself a `codex exec` run with `approval: never`
cannot escalate — report that and stop, and say so in the final answer rather than reviewing
alone.

The PATH-aliases warning on its own is harmless.

---

# Integration rules (both modes)

These cost time to rediscover. Respect them.

1. **Always redirect stdin: `< /dev/null`.** `codex exec` reads stdin to append a
   `<stdin>` block even when the prompt is a positional argument. Under a background
   launch the inherited pipe never closes and codex blocks forever on "Reading additional
   input from stdin…". That line prints on every run, `< /dev/null` included; it means a hang
   only when nothing follows it.

2. **A literal NUL byte in the prompt truncates it at exec time.** `"$(cat prompt.md)"`
   carries the byte through the substitution in zsh, but `execve` ends every argument at the
   first `0x00` — codex receives what precedes the NUL and nothing else, silently. bash
   behaves differently: it prints `warning: command substitution: ignored null byte in
   input`, drops the byte, and passes the rest. Neither delivers what was written. This is
   easiest to hit in exactly the run that can least afford it: a review of path-handling
   code, where a finding about `%00` invites pasting the decoded byte into the prompt. Write
   it as `%00` or `<NUL>`, and check before launching:

   ```sh
   perl -0777 -ne 'print "NUL: ", scalar(()=/\x00/g), " bytes: ", length($_), "\n"' prompt.md
   ```

   Codex may notice and say the input ended mid-sentence — do not rely on it. A cut that lands
   on a section boundary reads as a complete prompt, and the answer is a confident verdict on
   a smaller question than the one that was asked.

3. **Codex reads `AGENTS.md`, and nothing else is yours to hand it.** It auto-loads
   `AGENTS.md` from the repository — unless `config.toml` marks the project
   `trust_level = "untrusted"`; then it drops the project's `AGENTS.md` without a warning. A
   `-c projects…` override does not change trust. `codex debug prompt-input` shows, with no
   model run, whether `AGENTS.md` is in the context; it fails inside a Codex sandbox.

   Do not paste `CLAUDE.md` into the prompt and do not
   point codex at it by path — neither the project one nor the global
   `~/.claude/CLAUDE.md`. Whether a repository carries guidance for codex is the user's
   decision, expressed by the presence of `AGENTS.md`; a repository without one is meant to
   run without one. Task-specific conventions belong in the prompt, written out.

   `@file` is inert in `codex exec` — it is literal text, not an import.

4. **Read the answer from `-o`, never from stdout.** Stdout carries hook lines, a `codex`
   marker, `tokens used` with a count, and the final answer **printed twice**. The `-o`
   file holds exactly the final message (no trailing newline).

5. **Budget the run.** A single `max` review: median ≈22 minutes, most runs over 15, some near
   an hour, and 110k–410k tokens; longer when codex fans out to installed review skills. An
   `xhigh` executor: 30–50 minutes. A trivial question at `low` answers in seconds but still
   costs 10k–20k tokens of context. Match the effort to the question — and for an executor, to
   the size of the diff, not to the difficulty of the phrasing.

6. **Verify what it claims.** Codex is a second opinion, not an oracle. When it refutes a
   finding, confirm the refutation in the code before acting on it — and when it confirms
   one, that is not proof either. Its value is the disagreement, which is where to look.

7. **An unknown `-c` key is ignored, not rejected.** A config key that a release removed or
   renamed still parses, still looks right on the command line, and does nothing. The run
   succeeds with the default, so nothing points at the flag. `stream_idle_timeout_ms` is the
   live example: through 0.146.0 it was a top-level key, and in 0.147.0 it is a
   `model_providers.<id>` field only — passing it at the top level is now a silent no-op, and
   built-in provider ids such as `openai` cannot be overridden to reach it. Add
   `--strict-config` when a `-c` override does not appear to take effect; it turns the silence
   into `unknown configuration field ... in -c/--config override`. Note that it also validates
   `config.toml`, so a stale key there will surface first.

   `--strict-config` checks names, not meaning. `tools.web_search = true` passes it and still does
   nothing: the key exists for domain and location settings, a boolean there is discarded, and
   the mode lives in top-level `web_search`.

## Flags that matter

| Flag | Meaning |
|---|---|
| `-m, --model <MODEL>` | model id, e.g. `gpt-6-sol` |
| `-c <key=value>` | any config override; value parsed as TOML, falls back to a literal string |
| `-c model_reasoning_effort=` | `low` … `xhigh`, `max`, `ultra` — per model, `codex debug models` lists each one's levels. `low` answers in seconds, `max` reasons for minutes, `ultra` adds automatic delegation to its own agents |
| `-c service_tier=` | `priority` is the Fast tier; legacy `fast` is accepted. Not shown in the header or the session file |
| `-c approvals_reviewer=` | `user`: exec runs `approval: never`. `auto_review`: escalations go to an automatic reviewer, even under `read-only` |
| `-c sandbox_workspace_write.network_access=` | network inside `workspace-write`; also `writable_roots`, `exclude_slash_tmp` |
| `-c web_search=` | `live`, `cached` (default), `indexed`, `disabled`; `exec` has no `--search` flag |
| `--strict-config` | fail on config fields this build does not recognize — **including `-c` overrides**. Without it an unknown key is accepted and ignored |
| `--approve-for-me` | `workspace-write` with an automatic reviewer for escalations: sets `sandbox_mode`, `approvals_reviewer="auto_review"`, `approval_policy="on-request"`. Conflicts with `-s`; `exec resume`, `exec fork` and `exec review` do not accept it |
| `-s, --sandbox <MODE>` | `read-only`, `workspace-write`, `danger-full-access`. `exec resume`, `exec fork` and `exec review` reject it, use `-c sandbox_mode=` |
| `--dangerously-bypass-approvals-and-sandbox` | no sandbox, no prompts; externally isolated environments only |
| `-o, --output-last-message <FILE>` | writes ONLY the final answer to a file — the one reliable way to read the result |
| `-C, --cd <DIR>` | working root; `--add-dir` adds another writable dir, `--skip-git-repo-check` allows running outside git. `exec resume`, `exec fork` and `exec review` accept neither `-C` nor `--add-dir` |
| `--json` | events as JSONL, for machine consumption |
| `--output-schema <FILE>` | JSON Schema the final response must satisfy |
| `-i, --image <FILE>` | attach screenshots to the prompt |
| `--ephemeral` | do not persist the session; `--ignore-user-config` ignores `config.toml`; `--ignore-rules` drops execpolicy `.rules` |
| `-p, --profile <NAME>` | layer `$CODEX_HOME/<name>.config.toml` on the base config |

## Subcommands

- `codex exec resume <SESSION_ID|--last> "follow-up"` — continue the same conversation
  instead of re-explaining the context. Use it for "you said X, but line N says Y", for
  "the build you handed back fails at line N — fix that, nothing else", and to deliver the
  rest of a prompt that arrived truncated (rule 2) without paying for the part already done.

  **`resume` accepts a smaller flag set than `codex exec` itself.** `-m`, `-o`, `-c`, `-i`,
  `--json`, `--output-schema` and `--ephemeral` are there; `-s/--sandbox`, `-C/--cd`,
  `--add-dir` and `-p/--profile` are **not** — passing the first one fails the run outright
  with `error: unexpected argument '--sandbox' found`. `--approve-for-me` is not there either.
  Pass the grant as config overrides instead: for a reviewer `-c sandbox_mode="read-only"
  -c approvals_reviewer="user"`, for an executor what `--approve-for-me` sets —
  `-c sandbox_mode="workspace-write" -c approvals_reviewer="auto_review"
  -c approval_policy="on-request"`. Without them a resumed run does not keep the session's
  sandbox: a `read-only` review session resumes with the `sandbox_mode` from `config.toml`.
- `codex exec fork <SESSION_ID> [PROMPT]` — a new session with the history of an existing one;
  the source stays unchanged. Use it to put a second question to a finished review without
  appending to it. Same restricted flag set as `resume`, same overrides.
- `codex exec review [--uncommitted | --base <BRANCH> | --commit <SHA>] [--title <T>]` —
  the built-in review, when a plain diff review is wanted and no custom stance is needed. A
  scope flag cannot be combined with a prompt (`error: the argument '--uncommitted' cannot be
  used with '[PROMPT]'`); a prompt alone works. With no `-s` and no `-C`, it takes sandbox,
  approvals, and effort from `config.toml` — which can mean `workspace-write` with
  `on-request`. Pin them and run it from the repository:
  `-c sandbox_mode="read-only" -c approvals_reviewer="user" -c model_reasoning_effort="high"`.
  The answer goes to `-o` as with `codex exec`. For a custom stance, use reviewer mode instead.

## When this file is wrong

Flags, config keys, and sandbox behavior above were checked against `codex-cli 0.157.0`. Run
times and token counts were observed in real sessions from August to September 2026, on
0.146–0.157. Flags, config keys, and sandbox behavior move between releases; `codex --version`
is the first thing to compare when something does not line up.

A mismatch is a finding, not an obstacle. Do not quietly route around it.

- Confirm it first: `codex exec --help`, or a probe that costs no model run —
  `codex sandbox -c sandbox_mode=<mode> -- /bin/sh -c '<command>'` settles sandbox and
  network questions in seconds. Run it from the directory in question: with `-C` it demands
  `--permission-profile`. It reads `config.toml` too, so pin `network_access` when testing it.
- If the correction is local and certain, edit this file in the same session and say what
  changed.
- Otherwise open an issue on `Heapy/kortex` with the version, the exact command, what was
  expected, and what happened.
- Either way, tell the user. A trap rediscovered in silence gets rediscovered again.
