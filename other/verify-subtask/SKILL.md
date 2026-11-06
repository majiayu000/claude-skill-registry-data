---
name: verify-subtask
description: User-invoked as /verify-subtask <path>. Reads the subtask spec, gathers the implementation diff, and spawns subtask-verifier to produce a spec-compliance report. Run after implementation, before /pr-review and /test-gap.
allowed-tools: Read, Grep, Glob, Bash, Agent
invocation: /verify-subtask <subtask-path>
---

# Verify Subtask (spec-compliance check)

Check that the implementation of a subtask matches its specification document.

## Steps

1. **Resolve the spec path** from `$ARGUMENTS`.
   - If the argument ends with `.md`, use it as-is relative to repo root.
   - Otherwise, expand to `docs/roadmap/$ARGUMENTS.md`.
   - If the file does not exist, error: "Spec not found: <path>. Pass the path relative to
     docs/roadmap/ without the .md extension, e.g. `0001-generic-implementation/03.2-aws-bedrock-backend/01-configuration-model`."

2. **Gather the diff scope.**
   Run `git diff --name-only HEAD` to get changed files. If the working tree is clean
   (no staged or unstaged changes), try `git diff --name-only HEAD~1` to capture the
   most recent commit.

3. **Spawn `subtask-verifier`** with:
   - The resolved spec path
   - The diff (changed file list + `git diff HEAD` or `git diff HEAD~1` output)
   Ask it to produce a full compliance matrix and verdict.

4. **Return** the agent's compliance report verbatim.
   - PASS → confirm to the caller that review/testing can proceed.
   - PARTIAL → list deviations; recommend fixing before merge but do not block.
   - FAIL → list blocking gaps; instruct caller to return to `python-expert` with the list.

## Output

The verbatim compliance matrix from `subtask-verifier`, plus one line:
```
→ Next step: [proceed to /test-gap | fix gaps then re-run /verify-subtask | proceed with caution]
```

## Completion checklist

- [ ] Spec file found and readable
- [ ] Diff scope captured (changed files list non-empty or commit diff used)
- [ ] `subtask-verifier` returned a verdict (not null / timed out)
- [ ] On FAIL: blocking gaps listed and next step is "return to python-expert"
- [ ] On PARTIAL: deviations listed and next step is "fix before merge"
- [ ] On PASS: confirmation that /test-gap and /pr-review can proceed
