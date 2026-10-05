---
name: delegate-cli
description: >-
  Delegate or consult through local codex and agy CLIs. Use when Anton asks
  either tool to implement, review, consult, or research, or when another skill
  needs model-tiered worker fan-out. Covers prompt construction, capability
  probing, safe launches, concurrency, artifacts, and review.
license: MIT
---

# Delegate through codex and agy

Use these peer CLIs for bounded work that benefits from an independent implementer, reviewer, or
researcher. Prefer codex for implementation and code review; prefer agy for web research and very
large-context synthesis. Honor a user's named tool.

Keep fan-out bounded to two or three **independent** units, meaning both: neither unit consumes an
output the other may create or modify, and their write scopes are disjoint. Disjoint writes alone are
not independence — a unit that reads what another is still writing has a dependency edge. Use a
patch-only deliverable when exclusive paths are unavailable. Treat network access, workspace writes,
and unsandboxed execution as separate authorizations.

## Prepare the prompt

The worker does not share the current chat. Create a file-backed prompt that states:

- the task and exact deliverable;
- the absolute working directory and scoped files;
- permission boundaries, including forbidden git writes, installs, network use, and out-of-scope
  changes;
- acceptance commands and expected results;
- expected output paths for every material artifact.

Run each acceptance command before delegating it. Scope checks to the files the worker may change.
Keep runtime prompts and logs temporary by default. Record durable decisions, deviations, and outcomes
in the project's existing memory structure when they carry lasting value.

Three rules apply to every implementer:

1. Put exact numeric targets in the prompt and require the worker to report a deviation instead of
   editing an artifact to match the stated number.
2. Forbid weakening or deleting tests. Require the worker to report any blocking test by name.
3. Arrange independent review for consequential work, then re-run the checks and inspect the touched
   artifacts yourself.

Match unit size to the worker: a smaller model wants smaller units with verification between hops, a
frontier one holds a broader multi-part unit. Read the configured model from the probe rather than
naming one, unless the task genuinely needs a specific tier.

## Probe codex capabilities

Resolve asset paths relative to this `SKILL.md`. Before each codex launch, run:

```bash
"$skill_dir/assets/probe.sh" --workdir "$workdir" --sandbox "$sandbox"
```

**Naming a model is deliberate; guessing one is not.** Three are in use:

| Model | For |
|---|---|
| `gpt-6-astra` | **the default** — delegations run on it unless you say otherwise |
| `gpt-5.6-sol` | the fallback where the installed codex is too old for astra |
| `gpt-5.5` | brainstorming, and discussions leaning on broad world knowledge |

`launch.sh` passes `-m gpt-6-astra` when you give no `--model`, rather than deferring to whatever
`~/.codex/config.toml` happens to hold. A fan-out should not change model because it ran on a
different machine.

**A model can outrun the CLI.** The server serves `gpt-6-astra` only to a recent enough codex; an
older one is refused *by name* — `The 'gpt-6-astra' model requires a newer version of Codex` — after
launch, with exit 1. Measured 2026-09-10: accepted on **codex-cli 0.154.0**, refused on **0.149.1**.
`launch.sh` classifies that refusal as **exit 33** and prints the installed version with the remedy,
so it reads as a version gap rather than a generic API error.

The probe prints `CODEX_VERSION` — the fact that decides this — and `CODEX_MODEL_CONFIGURED` from
the local config. A `--model` value comes back as `CODEX_MODEL_REQUESTED_VALIDATED=0`, and that zero
is the point: the flag's existence is checkable, its value is not. **Read `CODEX_VERSION` from the
probe before a large fan-out**; discovering the gap once is cheap, discovering it on every worker is
not.

**Reasoning effort has no flag of its own.** `codex exec` accepts neither `--effort` nor `--search`;
both ride the generic config override. The launcher's `--effort LEVEL` maps to
`-c model_reasoning_effort=LEVEL`, and its `--web` to `-c tools.web_search=true --enable
web_search_request` — which is what `WEB_MODE=config_enable` reports. Omit `--effort` when the config
already sets the level you want. For a combination you reuse, `codex -p <name>` layers
`$CODEX_HOME/<name>.config.toml` instead.

Add the probe's `--web` option when the task requires web access. Add `--file-read-check` before work
that depends on inspecting local files, especially in a Linux devcontainer. Stop on a nonzero result
and report the emitted facts and exit status. The probe may report that codex is absent; report that
condition without substituting another tool or installing software.

A bypass removes the sandbox and requires explicit user authorization. Prompt rules do not recreate
sandbox enforcement: asking a worker to behave as if sandboxed is not a sandbox.

**The sandbox is off, and that is settled.** Codex calls bwrap only to *enforce* a sandbox, and
bwrap cannot create a namespace in these containers — so an enforced sandbox means every file tool
fails while codex still exits 0, and the worker writes confidently about a repository it never read.
Three pilot scripts in Meta-Aging were authored that way.

`launch.sh` therefore passes `-s danger-full-access` by default. **The container is the boundary**, and
the owner accepted that on 2026-08-25. Do not deliberate about it per run, and do not ask.

Deferred, not forgotten: restoring an enforced sandbox needs the container policy fixed
(`scbio-docker docs/ai-integration.md`), which needs a rebuild. Until then two things stay available
and neither is part of the normal path — `--sandbox MODE` to opt back in, and
`probe.sh --file-read-check` to tell you whether reads work under it. The launcher still refuses to
call a run successful if its stream shows the sandbox blocking file access, so re-enabling one cannot
quietly reproduce the blind-run failure.

**What still bounds the worker:** `--workdir`. These paths are host mounts, so an unsandboxed worker
reaches whatever the workdir contains. Scope the workdir, not the sandbox.

## Launch codex

```bash
"$skill_dir/assets/launch.sh" --unit "$unit" --workdir "$workdir" --prompt "$prompt"
```

That is the whole normal path: **write a prompt, launch, read the final message.** The launcher runs
in the foreground, so it returns when the worker is done, and it prints the final message after a
`--- FINAL MESSAGE ---` marker. The `KEY=VALUE` head before that marker carries the run's paths.

No probe is required. Run `probe.sh` when a launch fails in a way you do not recognise, or before
web-dependent work, where `--web` needs the capability it reports.

The asset owns flag spelling, stdin delivery, final-message capture, stream logging, run directories,
status records and locks; `launch.sh --help` lists the options. Two are judgement rather than
mechanics:

- `--parallel-ok` **affirms independence as defined above** — no dependency edge in either direction,
  and disjoint write scopes. Withhold it whenever a dependency exists or is uncertain; the live-unit
  refusal then serializes the launches for you.
- `--bypass` additionally disables the approval path. `codex exec` already reports `approval: never`,
  so it buys nothing here and the default covers the sandbox. Reach for it only with a reason.

Use a stable, specific unit name. A repeated active unit means overlapping work, and resolving that
comes before relaunching.

### Keep the launcher attached

**`launch.sh` runs in the foreground. Background the attached launcher, never detach it.** Disk state
supports polling; only a harness task supplies wake-up. A detached launcher has neither, which is why
every long dead-time launch in the 2026-08-21 session was a run nobody was waiting on.

| Caller | What to run |
|---|---|
| Owner behind `!` | The foreground command, no `&` and no `nohup`. Timeout promotion supplies the task id. |
| Orchestrator launching the work | The same foreground command, submitted through the harness's own background-task facility, so the harness owns the process and notifies on it. |
| Orchestrator observing someone else's launch | `status.sh --file "$status_file" --wait` as a harness background task, shadowing the run. |
| Interactive shell | Foreground. A human using job control owns that terminal's observation. |

`--bg` is removed and refused with a message, because it created observable files and no completion
signal.

## Run agy headlessly

The agy surface below was verified against agy 1.1.10. Its prompt flag consumes the next token, the
last prompt flag wins, and the first bare argument ends flag parsing. Supply the prompt as the value
and place every other flag afterward:

```bash
agy -p "$(<"$prompt")" \
  --model "$agy_model" \
  --print-timeout 25m \
  > "$output" 2>&1
```

Observe these parser and runtime constraints:

- A bare prompt starts interactive mode and fails headlessly on `/dev/tty`.
- `--model` accepts the display label or the slug printed by `agy models`. An invalid value exits
  before the run. Interactive sessions may rewrite the configured default.
- Omit `--effort`; agy model names already encode their effort tier and reject that option.
- `--print-timeout` requires a Go duration with a unit, such as `25m` or `300s`.
- Print mode buffers output until completion. Capture stdout with shell redirection. Asking agy to
  write the output path in the prompt switches it into agentic file-write mode.
- Headless tool calls require the appropriate permission authorization. With
  `--dangerously-skip-permissions`, confirm the log records that permissions were auto-approved.
- Read `~/.gemini/antigravity-cli/cli.log` after the run to confirm the selected model; reading it
  before the run reports the preceding session.
- A denied shell command can end a headless run without a useful answer. Grant only the command
  prefixes the scoped task needs.

For agy fan-out, use unique prompt and output paths and independent sessions. Capture each background
PID at launch and wait on that PID or on the expected output artifact.

## Review the result

Read the run's state from disk, by unit or by the `STATUS` path the launcher printed:

```bash
"$skill_dir/assets/status.sh" --unit "$unit"
```

It prints one `SUMMARY` line — state, PIDs, elapsed, heartbeat and activity age, stream and final
bytes, `expected_present=n/m`, and the real codex and result exit codes — then one `ARTIFACT` line
per file with current and baseline bytes and mtimes. The `FINAL` and `STREAM` paths hold the output.

**It reports quantities and never a phase or a percentage,** because nothing on disk supports one.
Hung versus slow stays your judgement: a fresh heartbeat with old activity means the supervisor is
alive while codex may be computing, blocked or stuck; a stale heartbeat means the writer itself
stopped, so suspicion falls on the launcher, the host or the filesystem. A terminal state is
definitive — the launcher reaped the child and recorded its real status.

A final message is a worker report; acceptance depends on repository state and rendered artifacts.

For every delegated change:

1. Inspect every touched file and expected artifact directly from disk, including files in ignored
   directories.
2. Re-run the scoped tests and acceptance commands yourself. Report any stated count that differs
   from the observed count.
3. Check git state in every reachable repository. Treat each submodule as its own repository and
   inspect its HEAD, reflog, and worktree separately when git writes were forbidden.
4. Open rendered outputs when text length, row count, labels, or layout changed; text-only checks do
   not expose visual collisions.
5. Relay a concise result with the worker/model used, changed artifacts, verification evidence, and
   unresolved deviations.
