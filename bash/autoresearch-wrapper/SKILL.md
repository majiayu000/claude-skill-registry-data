---
name: autoresearch-wrapper
description: Dependency-aware, worktree-backed autoresearch for any repo. Use when the user wants to find what in a codebase can be optimized, lock a measurable metric, and run an autonomous edit-measure-keep loop in Git worktrees; to compare feature implementations or a module deletion fairly (each tuned against a tuned control); or to inspect, resume, plot, monitor, merge back, or clean up such runs.
---

# Autoresearch Wrapper

Inspired by Karpathy's `autoresearch` (https://github.com/karpathy/autoresearch; clone it if you want to read the original loop): a fixed constraint, a mechanical metric, and autonomous iteration compound into real gains. This skill adds what a bare loop lacks: it understands the repo's dependency graph before touching anything, refuses to run without an explicit metric, isolates every experiment in a Git worktree, and keeps durable state so runs can be resumed, compared, and merged back.

The `autoresearch-wrapper` CLI does the bookkeeping (scanning, state, worktrees, measuring, keep/discard decisions). You, the agent, make the code changes inside the worktrees it hands out.

This skill set works in both Claude Code and Codex. Skills are invoked as `/<name>` in Claude Code and `$<name>` in Codex (e.g. `/autoresearch-wrapper-run` or `$autoresearch-wrapper-run`); examples below use the Claude Code form.

## Locating the CLI

Use the `run.sh` launcher in this skill's folder (the folder containing this `SKILL.md`). This block finds it in the standard Claude Code and Codex install locations:

```bash
AUTORESEARCH_RUNNER=""
if [ -n "${CLAUDE_SKILL_DIR:-}" ]; then
  AUTORESEARCH_RUNNER="${CLAUDE_SKILL_DIR}/run.sh"
elif [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then
  AUTORESEARCH_RUNNER="${CLAUDE_PLUGIN_ROOT}/skills/autoresearch-wrapper/run.sh"
else
  for dir in skills/autoresearch-wrapper .agents/skills/autoresearch-wrapper .claude/skills/autoresearch-wrapper "$HOME/.agents/skills/autoresearch-wrapper" "$HOME/.claude/skills/autoresearch-wrapper" "$HOME/.codex/skills/autoresearch-wrapper"; do
    if [ -f "$dir/run.sh" ]; then AUTORESEARCH_RUNNER="$(readlink -f "$dir/run.sh")"; break; fi
  done
fi
[ -n "$AUTORESEARCH_RUNNER" ] || { echo "Could not resolve the autoresearch-wrapper launcher" >&2; exit 1; }
```

Then use `bash "$AUTORESEARCH_RUNNER"` for all commands below. If the skill lives inside the current repo, `python3 scripts/autoresearch_wrapper.py` also works. Every command accepts `--repo <path>` (default: current directory) and most accept `--json`.

## When this skill is invoked

1. If invoked with no arguments (just `/autoresearch-wrapper` or `$autoresearch-wrapper`), route to the end-to-end wizard:

```bash
bash "$AUTORESEARCH_RUNNER" wizard
```

If you are operating without a real interactive stdin and the CLI cannot complete the prompts directly, emulate the same flow manually:
- Run `bash "$AUTORESEARCH_RUNNER" scan --no-interactive`
- Start from the compact core-functionality summary and focused dependency graph
- Only ask for the full language/directory listing if the user explicitly wants a broader scan
- Ask which functionality area they want to improve first
- Ask which specific part to optimize
- Ask for the metric name, metric command, metric goal
- Ask for execution mode (sequential / parallel / wild) and rounds or a stop rule
- Persist the configuration with `configure`
- Ask if the user wants to start the run immediately

If the user explicitly asks to inspect everything, rerun with:

```bash
bash "$AUTORESEARCH_RUNNER" wizard --full-summary
```

2. If the user provides extra text after the skill name, treat it as the high-level instruction and act accordingly.

3. If the user names a repo-local script path, wrap it (selects the script as the target and suggests a metric preset):

```bash
bash "$AUTORESEARCH_RUNNER" wrap <script-path>
```

4. If the user wants to add a feature with several candidate designs, or remove a module, use a comparison run (see "Comparison runs" below, or the `autoresearch-wrapper-create` / `autoresearch-wrapper-delete` skills).

5. For focused tasks, prefer the companion skills:

| Skill | Use it to |
| --- | --- |
| `autoresearch-wrapper-status` | show parts, readiness, runs, candidates |
| `autoresearch-wrapper-run` | start or resume a run, drive the loop, finalize it |
| `autoresearch-wrapper-flow` | show the metric history and an ASCII plot |
| `autoresearch-wrapper-create` | compare feature approaches, each tuned against a tuned control |
| `autoresearch-wrapper-delete` | compare deleting a part against keeping it, both tuned |
| `autoresearch-wrapper-monitor` | report a run's progress, or keep checking until it ends |

## Concepts

**Parts.** `scan` splits the repo into parts (one per source file) and builds a direct dependency graph: each part's dependencies, dependents, and unresolved imports. Each part is classified as:
- `surely optimizable`: the target, candidate space, and metric are all explicit and its important dependencies resolve;
- `probably optimizable`: something is unclear, usually the metric or the dependency boundary.

**The run gate.** `run` refuses to start until the part has a metric name, metric command, goal (`minimize`/`maximize`), execution mode, and either `--rounds` or an enforceable `--stop-rule`, and until its important dependencies are resolved. If the metric is unknown, ask the user; never guess one.

**The metric contract.** The metric command runs inside the candidate's worktree and must print a line matching the metric regex, by default `METRIC=<number>`. If it prints several, the last one counts. A non-zero exit, a missing value, or a timeout makes the candidate a `crash`.

**Runs and candidates.** A run owns a `seed` worktree (the baseline) and allocates candidates (`candidate-001`, ...) into their own worktrees on their own branches. New candidates branch from the current best (`keep`) branch, so improvements compound. Status per candidate: `keep` (beats the best so far), `discard`, or `crash`. `--status auto` decides from the metric.

**Snapshots.** `evaluate` commits any pending edits in the candidate worktree (respecting `.gitignore`) before measuring, so the measured code is exactly what the branch holds. Do not edit a worktree between its `evaluate` and `record`; `record` refuses if the branch moved.

**Execution modes.**
- `sequential`: one candidate at a time.
- `parallel`: `--parallelism N` candidates are preallocated so several agents or processes can work at once; state updates are locked and safe. Choose N from the machine that actually runs the metric command, not the one you are on (check `nproc` and `nvidia-smi` there, or the scheduler, e.g. `sinfo`/`squeue` on a Slurm cluster), and from how much each evaluation uses.
- `wild`: allocated like `parallel`. In addition, let each candidate change several parameters at once (up to `--wild-max-simultaneous`), and widen how much you change when progress stalls.

**Stopping.** A run ends (`completed`, with a `stop_reason`) when its `--rounds` target is reached or any clause of its `--stop-rule` holds:
- `metric<=X`, `metric>=X`, `metric<X`, `metric>X` (best metric so far)
- `stalled:N` (N recordings in a row without beating the best; crashes count)
- `minutes:N` (wall clock since the run started)

`--early-exit-patience N` (with optional `--early-exit-threshold`) ends a stalled run as `early_exit`. `--metric-timeout S` kills a hung metric command and its children and records a crash. After a run ends, `allocate` refuses; `finalize` it.

## Workflow: optimize one part

```bash
# 1. Find candidates and pick a target
bash "$AUTORESEARCH_RUNNER" scan --no-interactive
# 2. Lock the metric and budget
bash "$AUTORESEARCH_RUNNER" configure --part src/api.py --metric latency_ms \
  --metric-command "python bench.py" --metric-goal minimize --mode sequential \
  --rounds 20 --stop-rule "stalled:5" --metric-timeout 1800
# 3. Start (or resume) the run; read the generated program.md
bash "$AUTORESEARCH_RUNNER" run
# 4. Baseline
bash "$AUTORESEARCH_RUNNER" evaluate --candidate seed
bash "$AUTORESEARCH_RUNNER" record --candidate seed --status auto --description "baseline"
# 5. Loop: allocate, edit inside the returned worktree, evaluate, record
bash "$AUTORESEARCH_RUNNER" allocate
bash "$AUTORESEARCH_RUNNER" evaluate --candidate candidate-001
bash "$AUTORESEARCH_RUNNER" record --candidate candidate-001 --status auto --description "<what changed>"
# 6. When the run ends: merge the best back (staged, not committed) and clean up
bash "$AUTORESEARCH_RUNNER" finalize --merge
```

Commands default to the active run; pass `--run-id <run>` to target another. Each run writes a `program.md` with the locked config, the dependency neighbourhood, and the exact loop commands. Follow it.

Keep each candidate focused on the target part and its direct dependency neighbourhood. Write a one-line `--description` of what the candidate changed; it becomes the run's history.

## Comparison runs: create and delete

Adding or removing a module changes what the best settings of its neighbours are. A fair comparison tunes every option, including "no change", with the same budget:

```text
comparison run
├── control     setup: nothing                     → tuning run (budget B)
├── approach-A  setup: implement A                 → tuning run (budget B)
└── deleted     setup: remove part + fix imports   → tuning run (budget B)   (delete runs)
```

```bash
bash "$AUTORESEARCH_RUNNER" create --part src/api.py --feature "response caching" --candidates 3 \
  --metric latency_ms --metric-command "python bench.py" --metric-goal minimize --rounds 10
# implement approach-A in its setup worktree, then:
bash "$AUTORESEARCH_RUNNER" arm-ready --arm approach-A
# tune every arm (control included) with --arm; record the seed first for the setup score
bash "$AUTORESEARCH_RUNNER" evaluate --arm approach-A --candidate seed
bash "$AUTORESEARCH_RUNNER" record --arm approach-A --candidate seed --status auto --description "setup"
bash "$AUTORESEARCH_RUNNER" allocate --arm approach-A
# rank arms by tuned ceiling; ties go to control
bash "$AUTORESEARCH_RUNNER" compare
bash "$AUTORESEARCH_RUNNER" finalize --merge
```

- `delete --part <part>` creates arms `control` (part kept; the tuned pre-deletion baseline) and `deleted` (part removed and committed). Fix references in the `deleted` setup worktree, then `arm-ready --arm deleted`.
- During tuning, edits are limited to an enforced scope: by default the target and its direct neighbours (create) or the deleted part's direct dependents (delete), plus anything the arm changed during setup. Use `--tune-scope "a.py,src/config/"` when the knobs live elsewhere (e.g. a config file). `evaluate` rejects out-of-scope edits before running the metric. `--allow-out-of-scope` is for user-approved exceptions, and `compare` flags them.
- If `control` wins, say so plainly: no approach beat the status quo once both were tuned.

## Finishing a run

`finalize` works on an ended run (`--stop` ends a running one first):
- `--merge`: squash-merges the best candidate (for comparison runs, the winning arm's best, or `--arm X`) into the current checkout and leaves it staged for review. It refuses if tracked files have uncommitted changes, and rolls back a conflicting merge before anything is removed.
- It removes the run's worktrees; dirty ones are skipped unless `--force`. `--keep-best-worktree` keeps the winner's.
- `--prune-branches`: deletes every run branch except the best.
- Without `--merge`, it prints the `git diff` and `git merge --squash` commands instead.

Always confirm with the user before `--merge`, `--prune-branches`, or `--force`.

## Command reference

| Command | Purpose | Key flags |
| --- | --- | --- |
| `wizard` | guided scan → target → metric → run | `--full-summary` |
| `scan` | discover parts and the dependency graph | `--full-summary`, `--no-interactive` |
| `wrap <script>` | target a repo-local script with a metric preset | `--mode`, `--rounds`, `--stop-rule` |
| `configure` | lock metric and execution settings for a part | `--part`, `--metric`, `--metric-command`, `--metric-goal`, `--metric-regex`, `--mode`, `--rounds`, `--stop-rule`, `--parallelism`, `--metric-timeout`, `--early-exit-patience`, `--early-exit-threshold`, `--wild-max-simultaneous`, `--metric-preset`, `--use-suggested-command` |
| `status` | parts, readiness, runs, candidates | `--json` |
| `run` | start or resume the selected part's run | `--part` |
| `allocate` | create the next candidate worktree | `--run-id`, `--arm` |
| `evaluate` | snapshot and measure a candidate | `--candidate`, `--timeout`, `--arm`, `--allow-out-of-scope` |
| `record` | keep / discard / crash a candidate | `--candidate`, `--status`, `--description`, `--metric-value`, `--arm`, `--allow-out-of-scope` |
| `flow` | metric history, best-so-far, ASCII plot | `--run-id`, `--arm`, `--width` |
| `monitor` | live poller for a person at a terminal (blocks until the run ends; agents should use `status --json` instead) | `--interval`, `--output terminal\|file`, `--status-file` |
| `create` / `delete` | start a comparison run | `--part`, `--feature`, `--candidates`, `--rounds`, `--stop-rule`, `--tune-scope` |
| `arm-ready` | commit an arm's setup and start tuning it | `--arm` |
| `compare` | rank a comparison run's arms | `--run-id` |
| `finalize` | merge back and clean up | `--merge`, `--stop`, `--prune-branches`, `--keep-best-worktree`, `--force`, `--arm` |
| `preset-metric` | measure a script with a preset | `--preset runtime_seconds\|latency_ms\|throughput\|memory_mb`, `--script` |

## State and files

| Path | Contents |
| --- | --- |
| `.autoresearch-wrapper/state.json` | canonical state: parts, graph, configs, runs, candidates. Edit only through the CLI. |
| `.autoresearch-wrapper/STATUS.md` | human-readable summary, regenerated on every write |
| `.autoresearch-wrapper/runs/<run>/` | `program.md`, `results.tsv` (one row per record), `logs/` (metric output per evaluation) |
| `<repo>.autoresearch-worktrees/<run>/` | the run's worktrees, next to the repo |
| branches `autoresearch/<part>/<run>/<candidate>` | one branch per candidate |

## Troubleshooting

| Message | What to do |
| --- | --- |
| `run config is incomplete: ...` | `configure` the missing fields (a free-text stop rule does not count; use the stop-rule grammar or `--rounds`) |
| `dependency graph is incomplete for selected part` | rescan, or pick a narrower target |
| `run ... is completed` / `early_exit` on `allocate` | the budget is spent; `finalize` it, or start a new run |
| `HEAD moved since evaluate` | re-run `evaluate`, then `record` |
| `... is already recorded` | `allocate` a new candidate instead |
| `... is a comparison run; pass --arm` | add `--arm <arm>` |
| `arm ... is still in setup` | finish the arm's setup, then `arm-ready --arm <arm>` |
| `changes files outside the arm's tuning scope` | revert those edits and re-evaluate (or widen `--tune-scope` when creating the run) |
| `main checkout has uncommitted changes` on `finalize --merge` | commit or stash, then retry |
| `timed out waiting for state lock` | another command is stuck; check for hung processes |

## Guidelines

- Never optimize in the primary checkout; work only in the worktrees the CLI allocates.
- Do not start a run if the metric is unclear, and keep or discard strictly by the configured metric.
- Evaluate the baseline `seed` before any candidate.
- Respect the dependency neighbourhood and, in comparison runs, the enforced scope.
- Resume the persisted active run when the user asks to continue, rather than starting a fresh one.
- Large untracked outputs inside a worktree get committed by `evaluate`; add them to `.gitignore` or write them outside the worktree.
- Ask before anything that touches the user's checkout or deletes work (`finalize --merge`, `--prune-branches`, `--force`).

## Examples

- `/autoresearch-wrapper` (start the wizard)
- `/autoresearch-wrapper scan this repo and summarize the dependency-aware optimization candidates`
- `/autoresearch-wrapper wrap scripts/bench.py and use the suggested metric preset`
- `/autoresearch-wrapper optimize src/api.py for latency_ms, sequential, 20 rounds, stop when stalled for 5`
- `/autoresearch-wrapper compare three caching designs for src/api.py`
