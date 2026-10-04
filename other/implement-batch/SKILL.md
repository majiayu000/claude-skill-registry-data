---
name: implement-batch
description: Use when you want to implement the next batch of a plan. Handles module implementation, testing, and validation.
risk: critical
argument-hint: "[plan-file] [batch-number]"
---

# Implement Batch

This skill must only be invoked from the main session, never from a subagent.

**Arguments**: `<plan-file> <batch-number>` (optional — will prompt if not provided)

1. **Identify the plan and batch:**
   a. If the user specified a plan file and batch number, use those.
   b. Else determine the project name: check `origin` git remote (parse last path component, strip `.git`) → git root basename → working directory basename.
   c. List files in `~/.claude/plans/<project-name>/`, sorted by modification time. If no plans found, tell the user and stop.
   d. If no batch number specified, read the plan and identify the next unimplemented batch. Confirm with the user: "I'll implement Batch N of `<plan-file>`. Correct?"

2. **Read the plan and extract the batch spec:**
   - Identify all modules/components in the target batch
   - Note dependencies between modules within the batch (some may need sequential implementation)
   - Note dependencies on prior batches (verify those are already implemented)
   - Read existing source files that the batch modifies or depends on
   - **Complexity gate**: Before spawning subagents, check each task. Flag a task as "likely too complex for a single subagent" if it meets any 2 of these 3 conditions: touches >5 files, has >3 acceptance criteria, has cross-module dependencies. Present the flag to the user with a recommendation to split. Not a hard gate — the user can override and proceed.

3. **Spawn parallel subagents for independent modules:**
   - Spawn each implementer on the **latest, most capable model** available — omit the per-agent `model` override so each inherits the session's model rather than pinning a version-specific name. Don't downgrade to a cheaper tier. (`CLAUDE_CODE_SUBAGENT_MODEL`, if set in the environment Claude launches subagents under, overrides the inherited model.)
   - Each subagent receives: the plan section for its module, relevant existing source files, and the project's testing conventions
   - **Each subagent's prompt MUST include these instructions verbatim:**
     > Implement the specified module per the plan. Also write comprehensive tests targeting 100% coverage of the new code.
     >
     > Follow existing project conventions for: file layout, naming, imports, docstrings, type hints.
     >
     > After writing code and tests, report back with:
     > - **Files created**: list with brief description
     > - **Files modified**: list with what changed
     > - **Test count**: number of tests written
     > - **Open questions**: anything ambiguous in the plan that you resolved with a judgment call
     > - **Status**: exactly one of: `STATUS: DONE` (complete, tests pass, no concerns), `STATUS: DONE_WITH_CONCERNS` (complete and tests pass, but you have doubts — list them), `STATUS: NEEDS_CONTEXT` (cannot proceed — specify exactly what information is needed), `STATUS: BLOCKED` (technical blocker — describe it)
   - For modules that depend on other modules within the same batch, implement them sequentially after their dependencies complete.

4. **After all subagents complete — triage:**
   - **Handle implementer status** for each subagent:
     - `STATUS: DONE` → accept, proceed to 4b.
     - `STATUS: DONE_WITH_CONCERNS` → read concerns, re-read affected files, decide whether to accept or add to failure list. Do not silently ignore concerns.
     - `STATUS: NEEDS_CONTEXT` → provide missing context, re-dispatch the subagent for the same module (max 1 re-dispatch; if the subagent returns `NEEDS_CONTEXT` again, treat as `BLOCKED`).
     - `STATUS: BLOCKED` → add to failure list in step 5.
   - **Completion contradiction detection**: Scan accepted subagents' summary sections (Files created, Files modified, Test count, Open questions) for contradiction patterns. Heuristic exclusion: skip matches inside triple-backtick fenced code blocks only; inline single-backtick spans are NOT excluded. Patterns to flag:
     - "requires manual" / "manual step needed" / "manually run"
     - "could not complete" / "unable to" / "cannot be automated"
     - "TODO" / "FIXME" / "placeholder" (in subagent's own prose, not in quoted code)
     - "skipped" / "deferred" / "left as-is" for items that were in scope
     - "should work" / "probably works" / "untested" for claimed completions
     If a contradiction is detected: re-read the specific files the subagent modified. If real, add to failure list in step 5. If ambiguous after one read pass, treat as failure — do not loop.

   **4b. Consistency review:**
   - Review accepted agents' output for naming conflicts, import mismatches, duplicated code
   - Resolve any conflicts between agents' work

   **4c. Validation:**
   - Run the full test suite: `pytest` (do not duplicate what hooks cover)
   - Run lint/typecheck: `ruff check .` and `mypy` (if configured)
   - Report: total tests pass/fail/skip, coverage percentage, any new failures

5. **If tests or quality checks fail:**
   - Diagnose and fix in the main session (not a subagent — keep context local)
   - Re-run checks after fixes
   - If a failure cannot be resolved within 3 attempts, stop and report to the user
   - **Cascading-fix escalation**: If fixing a module failure causes a previously-passing module to break (distinct test file failures caused by separate fix attempts — exclude failures in shared fixtures like `conftest.py`, `fixtures.*`, `test_helpers.*`), that counts as a "cascade strike." Maintain a running strike count and cite it in each failure summary. The counter resets at the start of each batch. After 3 cascade strikes within a single batch, STOP fixing and escalate: "3 cascade events detected — fixes are breaking previously-passing modules. This suggests an architectural issue rather than isolated bugs. Recommend: review the batch's dependency graph and inter-module contracts before continuing."

6. **Summary to user:**
   - Batch N complete (or: Batch N blocked on [issue])
   - Files created/modified with paths
   - Test count and coverage
   - Key decisions or judgment calls made
   - Next batch ready to start (or: what blocks it)
   - *(If batch ≥ 3: Consider starting a new session after resolution to reclaim context budget.)*

7. **Auto-save**: After completing the summary, invoke `/save` to checkpoint progress. If this was batch 3 or later, recommend starting a new session for the next batch to reclaim context budget.
