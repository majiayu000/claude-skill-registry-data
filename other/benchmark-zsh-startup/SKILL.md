---
name: benchmark-zsh-startup
description: Benchmark and attribute zsh startup and prompt latency. Use when asked to profile a slow zsh prompt, explain where shell startup time is spent, compare `zsh-bench` with `zprof` or xtrace, or decide which zsh plugin, hook, or startup file to optimize first. Also use when the task is to track which zsh features, widgets, completions, or plugin-provided commands are actually being used.
---

# Benchmark Zsh Startup

## Overview

Benchmark what the user feels first. Attribute cost only after you have a stable baseline.

Prefer `zsh-bench` for prompt responsiveness, then use `zprof` or xtrace to explain the result. Treat `hyperfine 'zsh -ic exit'` as a narrow regression tool, not the main startup metric.

## Workflow

### 1. Baseline the user-facing latency

- Prefer `zsh-bench` when the question is "why does my prompt feel slow?"
- Measure interactive login-shell behavior, not just process exit time.
- Report cold-start and warm-start behavior separately when caches or one-time plugin setup skew the first run.

Use `hyperfine` only when you need a quick regression check for a narrow shell invocation:

```bash
hyperfine --warmup 3 'zsh -ic exit'
```

Do not present that number as "prompt startup time." It excludes what matters most in an interactive shell: first prompt lag, first command lag, and input lag.

### 2. Attribute cost at the right layer

Use `zprof` for function-level attribution.

- Load `zmodload zsh/zprof` near the start of the startup path under test.
- Call `zprof` at the end.
- Prefer doing this in a temporary `ZDOTDIR` copy or an instrumented repo copy instead of patching the live dotfiles.

Use xtrace when you need sourced-file or line-level attribution.

- Set a rich `PS4`.
- Redirect xtrace output to a log file.
- Restrict it to the startup under test.
- Use it to answer "which sourced file or eval is slow?" not "is my prompt fast?"

To see the trace as a Perfetto timeline, write xtrace in the marker format of `scripts/trace/xtrace-to-perfetto` and convert it:

```sh
PS4='+DFX|v=1|ts=%D{%s.%9.}|pid=$$|sub=${ZSH_SUBSHELL}|src=%x|line=%I|name=%N|stack=${(pj:,:)funcstack}|ctx=${(pj:,:)zsh_eval_context}| ' \
  DOTFILES_SKIP_LAUNCHCTL_SYNC=1 zsh -o promptsubst -x -ic exit 2>xtrace.log
scripts/trace/xtrace-to-perfetto --output trace.json --summary-output summary.json xtrace.log
scripts/trace/open-perfetto trace.json
```

This traces the real startup files. `summary.json` ranks the slowest commands. Code that resets options (`emulate -L`) leaves `${...}` fields unexpanded, but times, files, and lines still parse. `scripts/trace/run-zsh` is a different tool: it replaces `ZDOTDIR` to trace zsh scripts a command launches, so it never sources your startup files.

When checking live widget state, use a real PTY login shell instead of `zsh -ic`.

- `zsh -ic` can report `zle` as on even when there is no tty.
- Deferred plugin state can also be missing until a real prompt cycle has run.
- Use non-PTY shells for micro-benchmarks and source-time probes, not for final truth about keymaps or widget ownership.

### 3. Separate one-time setup from steady-state cost

Call out first-run work separately from warm runs:

- plugin bootstrap or clone/update work
- first-time completion dump generation
- package manager lookups
- one-time migration logic

The optimization target is usually warm interactive startup, not the very first shell after a machine bootstrap.

### 4. Report findings in buckets

Summarize startup cost in this order:

1. User-facing latency metric
2. Largest startup files or hooks
3. External commands or `eval` calls
4. Deferred plugins that still affect first prompt or first command
5. Safe next experiments

Keep the recommendation surgical. Do not refactor the whole shell because one plugin costs a few milliseconds.

## Choosing a Tool

Use `zsh-bench` when:

- the user cares about prompt responsiveness
- you need a benchmark that reflects interactive behavior
- you want comparable before/after results

Use `zprof` when:

- shell functions, hooks, or prompt helpers are suspected
- you need function attribution after you already have a baseline

Use xtrace when:

- startup cost hides in `source`, `eval`, command substitutions, or generated shell code
- you need file-level or line-level attribution

Use `hyperfine` when:

- you are checking a narrow regression
- you want a quick comparison of a single command or shell entrypoint
- you are careful not to overstate what it measures

## Tracking Feature Usage

Do not assume startup cost equals feature value. Measure usage separately.

Use shell history for:

- commands
- aliases that expand into commands
- shell functions invoked by name

History will not tell you about:

- `<Tab>` completion behavior
- `ctrl-r` widgets
- vi-mode bindings
- prompt segments
- hooks that run automatically

For those, add lightweight counters around the actual entrypoints:

- wrap ZLE widgets and increment counters
- wrap prompt or directory-change hooks
- log counts to a state directory, not the repo
- keep the logging opt-in and cheap

Prefer simple counters over verbose logs. The useful question is usually "do you use this at all?" not "what happened on every keystroke?"

## Default Recommendations

- Start with `zsh-bench`.
- If the result is bad, use `zprof`.
- If the result is still ambiguous, use xtrace on a temporary startup copy.
- Use `hyperfine` only for micro-benchmarks and regression checks.
- Track command usage from history and track widgets or hooks with explicit counters.

## Source Of Truth

Treat these as authoritative when this skill needs a refresh:

- `zsh-bench` README for interactive benchmark semantics
- the zsh manual for `zprof`, `PS4`, and `XTRACE`
