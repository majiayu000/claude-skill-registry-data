---
name: Pytest Repair
slug: pytest-repair
description: Repair a failing Python test suite — read the failure, read the module, make the minimal edit, re-run pytest until green, and only then report success.
whenToUse: A pytest, unittest, or tox run is failing and the job is to make it pass.
allowedTools: [fs_read, fs_write, fs_edit, fs_ls, fs_glob, fs_grep, pytest_run, test_run, test_coverage, term_execute, git_diff, git_status]
---

# Pytest Repair

A skill with a *closed* tool set. The `allowedTools` list above is not
documentation: `AgentLoop` intersects the offered schemas with it, so while
this skill is active a model cannot reach `web_search`, an MCP server, or any
write path that was not named here.

## Contract

1. **Read the failure first.** Never edit before you have the assertion text
   and the file it points at. `fs_read` the test, then `fs_read` the module.
2. **Minimal edit.** Change the code under test, never the assertion. A test
   that has to be edited to pass is a finding to report, not a problem to
   solve.
3. **Re-run with `pytest_run`.** It returns structured pass/fail plus the
   failure list, and it runs sandboxed like every other test execution.
4. **A green run is not a receipt.** The final claim must carry the real exit
   code from `pytest_run` *and* independent `TestVerifier` evidence over the
   materialized snapshot. Prose is not evidence.
5. **Replan on failure.** Feed the next failure back and try a *different*
   hypothesis — the loop breaker stops a repeat of the identical call.
