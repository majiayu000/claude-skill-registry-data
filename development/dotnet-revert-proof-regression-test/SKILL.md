---
name: dotnet-revert-proof-regression-test
description: "Use when adding a .NET/bUnit regression test for a UI or component fix and proving it catches the bug by reverting the fix, or when a reverted-fix run fails every test or shows no pass/fail counts."
---

# Revert-proof a .NET regression test

A test that passes after a fix proves nothing on its own — it may pass against the
broken code too. Prove it *bites* by temporarily removing the fix and confirming
exactly the new tests fail.

Complication on Windows: a running app (dashboard, WPF client, `dotnet run`
service) holds its own build outputs open, so `dotnet build`/`dotnet test` can exit
non-zero **without ever running a test**. Mistaking that for "the test failed" gives
a false revert-proof. Read every run's verdict — pass/fail counts, compile errors,
MSB3021/MSB3026/MSB3027/CS2012 locks and the holder's PID — with
`dotnet-test-verdict-capture`.

## Procedure

1. **Write the test**, then run it filtered, capturing the verdict to a log:
   `dotnet test <proj> --filter "FullyQualifiedName~<Class>" > test-verdict.log 2>&1`
2. **Clear locks before trusting any failure.** Stop the holder MSBuild names only
   if you started it yourself (`hub stop web`, or `Stop-Process` on your own PID),
   then re-run. Never stop the user's dashboard or Visual Studio — report which
   suites were skipped instead.
3. **Neuter only the fix** — replace the added render block / logic with a marker
   comment. Do not delete the test or its parameters (that breaks compilation and
   yields a lock-like non-answer instead of a failure).
4. **Re-run the filter.** Expect: *new tests fail, all pre-existing tests pass.*
   The split is the proof. All-fail or zero-count = still a build problem.
5. **Restore the fix.** Verify the file tag/content matches the pre-revert state.
6. **Re-run full suites** and compare counts to the known-good baseline.
7. Restart anything you stopped in step 2.

## Verifying edits really landed

Truncated `git status ... | head -N` can drop alphabetically-late files and look
like a missing edit. Confirm per-path instead:

```
git status --short -- <path>
git diff --stat -- <path>
grep -n "<NewTestName>" <path>
```

Strong independent corroboration: if `dotnet test` *discovered and ran* the new
tests, they were on disk — the compiler reads disk, not editor state. For renderer
or rtk artefacts that fake a lost edit, see `prove-file-integrity-not-renderer-loss`.

## Anti-patterns

- Treating a non-zero exit as "test caught the bug" without a pass/fail split.
- Leaving the fix reverted. Always restore and re-verify green.
