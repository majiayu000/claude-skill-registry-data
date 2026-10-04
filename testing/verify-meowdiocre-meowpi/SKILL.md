---
name: verify
description: "Verify a requested change or claim with fail-first evidence, targeted checks, live output, and exit codes. Use for 'çalışıyor mu', 'testleri çalıştır', 'doğrula', 'kanıtla', and before declaring a bugfix, feature, refactor, or API change complete. Not for silently repairing a failing project or claiming visual, security, or production behavior from an unrelated unit test."
compatibility: Oh My Pi (OMP). Needs a runnable project command.
---

# Verify

**Localize → red → minimal approved change → same command green.** “Verified” without this turn's tool output is a failure. A verification request is not authorization to change code: diagnose and report unless implementation was separately requested or approved.

## Fail first (before production edits)
1. Name **1–3 files**. `grep`/`find` the symptom. Do not dump the tree.
2. A command that is **red for the right reason**:
   - Bug: existing test, type error, repro script, or curl that shows the bug.
   - Feature: a **new** test that fails because the feature is missing (allowed).
3. Show that red (first failure). If you cannot get red, you do not understand the task — do not guess a patch.

Skip fail-first only when the user named a copy/docs hunk, already pasted this turn's red stack, or the target state cannot meaningfully fail first (for example, a read-only environment check). State the reason and use the narrowest direct proof.

## Patch
Only after implementation is separately authorized: make the smallest change that addresses the demonstrated cause. Re-run **the same command**; it must go green. If a cheap regression check exists for the affected file or package, run it. Do not stack another fix on a broken attempt: revert a regressing patch before trying a new hypothesis.

## Tests (two directions — do not conflate)
- You MAY add tests that would fail without your change.
- You MUST NOT weaken, skip, delete, or rewrite existing assertions to get green.
- You MUST NOT change production to match a wrong test.
- You MUST NOT hide the real test in `/tmp`.
- If a test blocks you and you think the test is wrong: stop. Tell the user. Do not edit it unless they changed the spec this turn.

## Revert test
One line: which assertion or type error goes red if this diff is undone. If you cannot name it, you are not testing the change — add a test (allowed) or say untested.

## Command selection
1. Project `AGENTS.md` verification instruction.
2. The narrowest behavior-level command (`pytest path::name`, `go test ./pkg -count=1`, `cargo test name`, `npm test -- path`).
3. The documented project command from `package.json`, Makefile, justfile, or README.

Run the smallest command that proves the requested behavior, then the cheapest relevant regression check. Lint, type-check, formatting, screenshots, and health checks are complementary evidence, not interchangeable proof.

## Run
1. State the command.
2. `bash` it.
3. First failure + summary. Not a wall.
4. Red after a patch: one cause, change the code or the hypothesis. Same command + args twice max.
5. Cannot run → `blocked` + the command. Do not claim done.
6. Flake: re-run once. Still red/green flip → report flake, not pass.

## Close
Report: exact command and exit code; red and green evidence (or stated exception); what behavior the check covers; revert test; and untested risk. UI/CSS needs visual evidence at the relevant viewport. Docs/JSON need the written region read plus a parser or schema check when available. A passing command may not prove a deployment, migration, external integration, or security property; name that limit.
