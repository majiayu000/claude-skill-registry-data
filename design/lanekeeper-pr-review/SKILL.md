---
name: lanekeeper-pr-review
description: The reviewer-agent procedure for Lanekeeper pull requests. Re-run the gates yourself, check scope and contract boundaries, trace every S# to code and a test, check every P# against registered benchmarks, review correctness and test quality, and post one structured verdict with blocking and non-blocking findings. Use this skill whenever asked to review, check, approve or audit a Lanekeeper PR or branch, or to act as the reviewer agent. Use it before any human review, even for small PRs.
---

# Reviewing a Lanekeeper PR

You are the gate before a human sees this PR. Re-run the checks yourself; don't trust the PR text. Be specific. Each finding gives a file and line, the rule it breaks (S#, P#, D#, or an AGENTS.md rule), and the fix.

## Procedure

1. **Scope**
   - Every changed path is owned by the PR's prompt (see its metadata table), or is a test, benchmark or fixture under those paths.
   - Contract paths are untouched, unless the PR is labelled `contract-change` and contains nothing else. Use the `lanekeeper-contract-change` skill to judge it.
   - `plans/NN-*.md` exists, and the commits follow its task order (`NN/Tk: …`).
2. **Gates.** Run these yourself:
   - `just verify-NN`
   - `just verify`
   - `cargo xtask bench-check`
   - `just fuzz-smoke`, if parsers changed

   Paste the results.
3. **Security.** Use the `lanekeeper-security` skill.
   - For each S# in the prompt, and any the change touches, locate the implementation and the test that proves it.
   - Scan for the red flags listed in that skill.
   - Confirm that `docs/threat-model.md` was updated for the component.
4. **Performance.** Use the `lanekeeper-performance` skill.
   - Every P# has a registered benchmark that measures the real path, at target scale, within budget.
   - No anti-patterns: per-request parsing, `OFFSET`, N+1 queries, blocking in async, unbounded collections.
5. **Domain correctness.** For engine, registry or MCP changes, use the `lanekeeper-config-semantics` skill. Verify:
   - property sources merge setting by setting, and resource files are chosen whole;
   - rendering substitutes only keys present in the property view;
   - tenant sets are respected;
   - line endings are normalised for comparison and restored on write;
   - pickup states, not "pending restart".
6. **Tests**
   - Behaviour is asserted, not implementation details.
   - Error paths are covered.
   - No sleeps; no tautological assertions; no mocking of owned code (port fakes are fine).
   - Golden and fuzz tests exist where the prompt requires them.
7. **UI changes.** Use the `lanekeeper-ui-from-design` skill. Visual and keyboard tests are present and green. Every deviation is recorded.
8. **Open questions.** Every one the prompt touches uses its stated default, and is configurable. Each assumption is listed and reasonable.

## Output: one review comment, exactly this structure

```
## Verdict: APPROVE | CHANGES REQUESTED

### Blocking
1. <file:line> — <problem> — violates <S#/P#/D#/rule> — fix: <concrete change>

### Non-blocking
1. ...

### Evidence
- just verify-NN: <pass/fail + summary>
- just verify: <...>
- bench-check: <table rows for this PR's P#>
- Security trace: S# → impl file → test name (one line each)
- Threat model updated: yes/no (section)
```

Approve only when there are no blocking findings. Unverifiable evidence, such as a gate you couldn't run, is itself a blocking finding.
