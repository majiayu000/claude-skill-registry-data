---
name: codex-parallel-subagents
description: Use when building MoonBit tools on this repo's Codex SDK that spawn multiple agent threads in parallel or in batch, including bounded concurrency, per-task threads, streaming events, and collecting session IDs or structured outputs.
---

# Codex Parallel Subagents

## Overview

Use the Codex SDK to fan out work into multiple threads, run them concurrently with bounded parallelism, and collect results safely across batch jobs.

## Full running projects (scripts)

See `skills/codex-parallel-subagents/scripts/` for multiple full MoonBit projects (single prompt, parallel batch, streaming events, structured output, directory summaries, options overrides). Each project is self-contained with `moon.mod.json`, `moon.pkg.json`, and a top-level `main.mbt`, so an agent can copy a folder and run `moon run .` immediately.

## Full running examples (copy/paste)

Read `skills/codex-parallel-subagents/references/full-examples.md` for several complete, runnable examples (single prompt, parallel batch, and streaming events). Each example includes every file you need to paste and a single `moon run cmd/main` command.

## Greenfield setup (new repo)

Read `skills/codex-parallel-subagents/references/greenfield-setup.md` for a full walk-through that starts from `moon new`, adds `peter-jerry-ye/codex`, and ends with a parallel batch example that summarizes books.

## Quick start: one subagent

Create a Codex client, start a thread, run a prompt, and read the final response.

```moonbit
async fn run_once(prompt : String, workdir : String) -> String {
  let codex = @codex.Codex::new()
  let thread = codex.start_thread(
    options=@codex.ThreadOptions::new(
      working_directory=workdir,
      model?=@sys.get_env_vars().get("MODEL"),
    ),
  )
  let turn = thread.run(prompt) catch { e => @error.reraise(e) }
  turn.final_response
}
```

## Parallel fan-out with bounded concurrency

Create one thread per task and guard execution with a semaphore.

```moonbit
async fn run_batch(tasks : Array[String], workdir : String, parallelism : Int) {
  let codex = @codex.Codex::new()
  @async.with_task_group(fn(task_group) {
    let semaphore = @semaphore.Semaphore::new(parallelism)
    for task in tasks {
      task_group.spawn_bg(allow_failure=true, fn() {
        semaphore.acquire()
        defer semaphore.release()
        let thread = codex.start_thread(
          options=@codex.ThreadOptions::new(
            working_directory=workdir,
            model?=@sys.get_env_vars().get("MODEL"),
          ),
        )
        let _ = thread.run(task) catch { e => @stdio.stderr.write("\{e}\n") }
      })
    }
  })
}
```

## Batch jobs with per-task state

Create a task record that includes inputs, output paths, and optional session IDs. Store `thread.id()` after a run to audit or resume later.

```moonbit
struct Job {
  prompt : String
  output_path : String
  session_id : String?
}
```

## Streaming events when you need progress

Use `Thread::run_streamed` to consume events as the agent works and update progress in real time.

```moonbit
async fn run_streamed(prompt : String, workdir : String) {
  let codex = @codex.Codex::new()
  let thread = codex.start_thread(
    options=@codex.ThreadOptions::new(working_directory=workdir),
  )
  let streamed = thread.run_streamed(prompt)
  while streamed.events.next() is Some(event) {
    match event {
      ItemCompleted(item) => @stdio.stdout.write("completed: \{item}\n")
      TurnCompleted(_) => @stdio.stdout.write("turn completed\n")
      _ => ()
    }
  }
}
```

## Structured outputs for batch post-processing

Ask Codex for JSON and parse `turn.final_response` into a known shape. Prefer `TurnOptions::new(output_schema=...)` when strict output is required.

## Tips and pitfalls

- Create a new `Thread` per subagent task; do not share a single thread across concurrent tasks.
- Use `ThreadOptions::new(working_directory=...)` so each task operates in the right repo or worktree.
- Set `CodexOptions::new(codex_path_override=...)` when you need a custom CLI wrapper (see repo examples).
- Guard parallel runs with `@semaphore.Semaphore` to avoid rate limits.
- Use `allow_failure=true` for background tasks and capture errors per task instead of crashing the batch.
- When you need `peter-jerry-ye/codex` (or other modules), add it with `moon add` before using it in code.
- MoonBit resolves dependencies with MVS; if you hit conflicts, try pinning a version like `moon add pkg@0.1.1`.

## Common failure modes + quick fixes

- **Session permissions**: ensure your Codex CLI has access to the working directory; set `working_directory=...` and verify the path exists.
- **Sandbox constraints**: bump to `SandboxMode::WorkspaceWrite` or `DangerFullAccess` when file reads/writes are blocked.
- **Missing CLI binary**: set `codex_path_override=...` to the correct CLI wrapper.
- **API config**: verify `OPENAI_API_KEY` or your provider key and `base_url` settings.
- **Model errors**: double-check model names and rate-limit your batch with a semaphore.

## Examples in the SDK repo (optional)

If you are browsing the Codex SDK repository, read `skills/codex-parallel-subagents/references/repo-examples.md` for concrete patterns from `cmd/real_world/*`.
