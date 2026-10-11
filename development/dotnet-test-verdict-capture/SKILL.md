---
name: dotnet-test-verdict-capture
description: "Use when a dotnet test/build verdict is unclear (no Passed!/Failed! summary, tail shows only warnings, suspiciously fast) or it exits non-zero with MSB3021/MSB3026/MSB3027/CS2012 while an app runs."
---

# Capture a `dotnet test` verdict reliably

rtk compresses test output and a running app can lock its own DLLs, so neither the
exit code nor a `tail` is a verdict. Capture the run to a log and read its shape.

## Symptom
- `dotnet test ... 2>&1 | tail -1` shows a compiler/xUnit warning, never the `Passed!`/`Failed!` line.
- rtk's wrapper compresses test output; the verdict line gets swallowed.
- Wall time ~3s with no summary = the BUILD failed (compile error or lock); no tests ran at all. Don't hunt for a summary that was never produced.

## Procedure
1. Redirect to a file — no pipes, no `tail`:
   `dotnet test tests/X.Tests/X.Tests.csproj -c Release --nologo > test-verdict.log 2>&1; echo "exit=$?"`
2. Read the verdict with the grep TOOL (respects .gitignore, structured output):
   - pattern: `passed|failed|^ok|^fail|error CS|MSB302[167]|CS2012`, case-insensitive
     (covers `Passed!`/`Failed!`, `N passed, M failed` and the `ok`/`fail` summary lines)
   - path: `test-verdict.log`
3. Read the shape below, never the exit code alone.
4. Delete the log so it never lands in the tree: `rm test-verdict.log`.

## Reading the shape

| Signal | Meaning |
|---|---|
| `Passed!`/`Failed!`, or `N passed, M failed` with a runtime (`687 ms`) | tests genuinely **executed** |
| `error CS####` | compile error; the line names the exact file:line |
| `MSB3026` / `MSB3027` "Beginning retry N", `Exceeded retry count of 10` | copy-step **lock** — nothing ran |
| `MSB3021` | copy-step **lock** — nothing ran |
| `CS2012 Cannot open '<X>.dll' for writing ... locked by 'VBCSCompiler'` | concurrent build **lock** — nothing ran |

A locked build never emits pass/fail counts; `9 passed, 3 failed` is a real run.
MSBuild names the holder explicitly: `The file is locked by: "AntHill.Web (36272)"`.

- Stop the holder **only if you started it yourself** (`hub stop web`, or
  `Stop-Process -Id <pid>` on your own PID), re-run, and restart it afterwards.
- **Never stop the user's dashboard or Visual Studio.** Leave the locked suites
  unrun and report which were skipped.

## Traps
- Iterating on `tail -N` never converges — the xUnit/compiler warnings are emitted after the summary in the stream, so any tail shows warnings only; `| tail -3` can hide the `ok`/`fail` summary line.
- omp's bash interceptor (`bashInterceptor.enabled: true` in `~/.omp/agent/config.yml`) blocks a standalone shell `grep`/`rg`/`tail` on the log; use the grep TOOL. A piped `| grep` is exempt (omp v18.2.11, verified 2026-09-24), but a pipe hides the build's exit code: read `${PIPESTATUS[0]}`, not `$?`.
- Two `dotnet build`/`dotnet test` invocations in parallel on shared projects fight over `VBCSCompiler` and produce CS2012. Run sequentially.
- For warning inventories, plain `dotnet build AntHill.slnx --nologo -v minimal` (without rtk) reports the true count; rtk's aggregated count differs (e.g. "15 warnings" vs the real 2).
