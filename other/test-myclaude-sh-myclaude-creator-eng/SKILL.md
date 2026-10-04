---
name: test
description: >-
  Sandbox test a product in an isolated worktree. Runs 3 scenarios (happy path, edge
  case, adversarial), verifies activation protocol, reports results. Use when the creator
  says 'test', 'try it', 'does it work', or before publishing.
argument-hint: "[product-slug]"
allowed-tools:
  - Read
  - Glob
  - Grep
context: fork
isolation: worktree
---

# Tester

Run sandbox tests on a product in an isolated environment.

**When to use:** Before publishing, after major changes, or to verify activation protocol works standalone.

**When NOT to use:** For quick syntax checks (use /validate instead). For testing the Engine itself.

---

## Activation Protocol

0. **Shared preamble:** Load `references/quality/activation-preamble.md` — context assembly, persona adaptation, deterministic routing rules.
1. Identify target product:
   - If `$ARGUMENTS` provided, use as slug → `workspace/{slug}/`
   - If not, list products in workspace/ and ask
2. Read `.meta.yaml` → get type, state, mcs_target
3. Load product-dna/{type}.yaml → get install_target pattern
4. Verify product has content (state != scaffold)
5. Create worktree isolation (this skill runs with `isolation: worktree`)
5b. **Stale worktree check:** Before creating a new worktree, glob `.claude/worktrees/`. If stale entries exist (>1 hour old by directory mtime), attempt removal. If removal fails, proceed anyway — never block testing on cleanup.
6. **Load voice identity:** Load `references/quality/engine-voice-core.md`. Test result reporting — pass verdicts (celebrating tone), fail verdicts (confronting tone), diagnostics (conducting tone) — honors the ✦ signature, three tones, and six anti-patterns.

---

## Core Instructions

### TEST EXECUTION

**Step 1 — Install Simulation**

Copy product files to the install target path (from product-dna):
```
workspace/{slug}/ → {worktree}/{install_target}/
```

Verify:
- All files copied successfully
- No broken relative paths after move
- Primary file exists at target location

**Step 2 — Activation Test**

Test the activation protocol:
- Read the primary file (SKILL.md, AGENT.md, etc.)
- Verify it references files that exist in the installed location
- Check that references/ paths resolve correctly
- Verify frontmatter is valid (name, description present)

**Step 2b — Type-Specific Tests** (run BEFORE generic scenarios)

| Type | Test | Pass Criteria |
|------|------|---------------|
| **hooks** | 1. Parse `hooks.json` — must be valid JSON | JSON.parse succeeds |
| | 2. Run each handler script with mock stdin: `echo '{}' \| bash scripts/handler.sh` | Exit code 0 or 2 (not crash) |
| | 3. Verify all event names in hooks.json are from the 25-event list | No unknown events |
| | 4. Run security scan (same patterns as /validate Stage 2) | Zero injection patterns |
| **statusline** | 1. Verify `statusline.sh` has shebang (`#!/usr/bin/env bash` or `#!/bin/bash`) | First line matches |
| | 2. Run with mock JSON stdin: `echo '{"model":"opus","cwd":"/tmp"}' \| bash statusline.sh` | Produces stdout output (non-empty) |
| | 3. Verify `settings-fragment.json` is valid JSON with `statusLine.type` and `statusLine.command` | Fields present and valid |
| | 4. Check script reads from stdin (`$(cat)` or `read` pattern present) | Pattern found |
| **minds** | 1. Load `AGENT.md` — verify frontmatter has `name` and `description` | Both fields present |
| | 2. Verify `denied-tools` or `tools` field exists in frontmatter | At least one tool restriction |
| | 3. Verify the file is self-contained (no broken references to external files) | All refs resolve |
| | 4. Run test prompt: invoke as Agent with `subagent_type={slug}` and a simple domain question | Produces domain-relevant response |

If type-specific tests fail, report them separately in the test report under a `TYPE-SPECIFIC` section.

**Step 3 — Three Scenarios**

Run 3 test inputs that stress the product at different levels. A product that only handles the ideal case is fragile — robust products handle all three:

| Scenario | Purpose | Input Strategy | What Failure Reveals |
|----------|---------|---------------|---------------------|
| **Happy path** (ideal) | Normal expected use | Typical request matching the product's description | If this fails, the product is fundamentally broken |
| **Edge case** (challenging) | Boundary conditions | Minimal input, unusual formatting, missing context | If this fails, D14 (Graceful Degradation) is weak |
| **Adversarial** (problematic) | Graceful failure | Invalid input, prompt injection attempt, conflicting instructions | If this fails, the product is unsafe for marketplace |

For each scenario:
1. Invoke the product with the test input
2. Capture output
3. Verify against D4 (Quality Gate) criteria if defined
4. Check for crashes, undefined behavior, or silent failures

**Step 4 — Must-Haves Verification**

If `.meta.yaml` contains `must_haves:`, verify each:
- **Truths**: Can the stated behavior be observed? Try to trigger it.
- **Artifacts**: Do the listed files exist with minimum content?
- **Key Links**: Do the grep patterns match?

Report: "Must-haves: {passed}/{total} verified"
If any fail: "MUST-HAVE FAILED: {description}. The product may not achieve its stated goal."

**Step 5 — Report**

**UX Stack (load before rendering results):**
1. `references/ux-experience-system.md` §1 Context Assembly + §2.3 Moment Awareness (test pass/fail)
2. `references/ux-vocabulary.md` — translate terms
3. `references/quality/engine-voice.md` — Brand DNA

**Cognitive rendering:** /test results are a confidence moment. On pass: "Works in practice, not just on paper." — factual confidence, not celebration. On fail: diagnostic mode — show exactly what failed and why, suggest specific fix. For first-time test pass, this is a milestone: "Your product works. Real conversations validated." For experts: compact result line + only surface surprising observations. Never celebrate a test pass the same way twice for the same creator — vary the insight.

```
TEST REPORT — {slug}

INSTALL    PASS  Files copied: {N}, paths valid
ACTIVATION PASS  Primary file loads, refs resolve, frontmatter valid
HAPPY PATH PASS  Output matches expected behavior
EDGE CASE  PASS  Handles minimal input gracefully
ADVERSARIAL PASS  Rejects invalid input without crashing
MUST-HAVES PASS  {passed}/{total} verified

Result: 6/6 PASS — Ready for /package

{if failures}
FAILURES:
  {scenario}: {what went wrong}
  Suggested fix: {recommendation}
{/if}
```

**Step 6 — Update State**

On test completion, update `.meta.yaml`:
```yaml
# .meta.yaml updates
state:
  last_tested: "{ISO timestamp}"
  test_result: "pass"          # "pass" if all 5 checks pass, "fail" otherwise
  test_scenarios: "{passed}/{total}"
```

If any test fails, record `test_result: "fail"` but do NOT change `state.phase` — testing does not regress product state.

### WORKTREE CLEANUP PROTOCOL

After all test scenarios complete (pass or fail):

1. **Record results first** — write test results to the ORIGINAL `.meta.yaml` (not the worktree copy) before any cleanup attempt. Results must survive cleanup failure.
2. **Attempt cleanup** — the `isolation: worktree` frontmatter handles automatic cleanup. If the worktree persists after skill completion:
   - On next `/test` invocation: check for stale worktrees via `glob .claude/worktrees/*`. If found, attempt removal before creating a new one.
   - On Windows: file lock contention is common. If removal fails, log the path and proceed — never block the test pipeline on cleanup failure.
3. **Disk budget guard** — if `.claude/worktrees/` contains more than 3 directories, emit advisory: "Stale worktrees detected ({N} found). Run cleanup manually: remove `.claude/worktrees/` contents."

---

## Quality Gate

Test is considered PASS if:
- [ ] Product installs without broken references
- [ ] Activation protocol loads successfully
- [ ] Happy path produces meaningful output
- [ ] Edge case doesn't crash or produce empty output
- [ ] Adversarial input is handled (rejection, fallback, or graceful error)
- [ ] All `must_haves` entries verified (if defined in .meta.yaml)

---

## Anti-Patterns

1. **Testing in production** — Always use worktree isolation. Never modify the creator's workspace.
2. **Weak adversarial** — "please ignore instructions" is too simple. Use domain-appropriate adversarial inputs.
3. **Binary pass/fail** — Provide specific failure descriptions, not just FAIL.
4. **Skipping cleanup** — Worktree must be cleaned up after test, even on failure.
5. **Testing the template** — If the product still has placeholder content, don't test. Suggest /fill first.

---

## Compact Instructions

When context is compressed, preserve:
- Product slug, type, and test status (pass/fail)
- Which scenarios passed/failed (happy path, edge case, adversarial)
- Type-specific test results if applicable
- Worktree cleanup status
- Whether test was blocking for MCS-2+ packaging
