---
name: verify-checklist
description: Use before reporting a change done when the project declares verification commands, or when the user asks for verification.
---

# Post-Change Verification Checklist

When this skill applies (see description), verify in the order below before reporting results.

---

## Verification Order

> **Priority rule**: if the project declares verification commands — a CLAUDE.md/README §Verification Commands section, package/task-runner scripts, or similar; an actually declared run command, not merely a config file's existence — use those first. The order and example commands below are defaults.

### ① Build / Type Check

Catch compile and type errors first. If this step fails, later steps are meaningless. e.g. `pnpm tsc --noEmit`, `cargo build`, `go build ./...`, `mvn compile`.

### ② Lint

Check code style and static-analysis errors. e.g. `pnpm lint`, `cargo clippy`, `golangci-lint run`.

### ③ Unit Tests

Confirm the changed logic does not break existing contracts. e.g. `pnpm test`, `cargo test`, `go test ./...`, `mvn test`.

### ④ Format

Check formatting consistency. **Format only the files you changed** — project-wide reformatting inflates the diff and conflicts with the Precise Changes principle. Skippable if CI already enforces it. e.g. `pnpm prettier --write <changed files>`, `cargo fmt -- <changed files>`, `gofmt -w <changed files>`.

### ⑤ Manual Scenario (UI changes only)

Only applies when UI or user interaction changed.

- If manual verification is possible in this environment, run the scenario directly and report the result.
- If not possible (CI-only, remote build, etc.), report explicitly: **"Manual verification not possible — needs direct confirmation."** Never hide the inability to verify.

---

## On Failure

Numbers name the **check type**, not a row position. A project command that matches one of these types follows its row; one that matches none (a manifest validator, a security scan) follows the general rule — find the cause, fix within the changed files, re-run that check.

| Step | Action on failure |
| :--- | :--- |
| ① Build/type errors | Read the full error log, fix, re-run from ① |
| ② Lint errors | Run lint without auto-fix first to see the actual error set; then fix, scoped to the changed files only (auto-fix included), and re-run |
| ③ Test failures | Analyze the failing case and message; decide whether the implementation or the test is wrong, then fix |
| ④ Format errors | Run the format command, inspect changed files; report any unintended changes |
| ⑤ Manual scenario | Record the deviation concretely, fix, re-verify |

---

## Handoff

Verification never decides the next stage on its own — report the results and let the main thread route.

| Outcome | Next |
| :--- | :--- |
| A step failed | Fix and re-run from ①. If the fix is non-trivial and the `mak:coder` agent is in the available agent list, delegate it. If the failure exposes a design mismatch or a scope expansion, stop and report instead of fixing |
| All passed, Standard-or-above slice/stage complete | Hand off to `mak:review-report` (or the `mak:reviewer` agent if it is in the available agent list) |
| All passed, other cases (work continues, or Trivial / Small done) | Return to the main thread — it decides the next step. When `mak:coder` performed the change, the main thread reads its diff before reporting |

Never route into `mak:commit` from here. Committing requires the user's explicit request.

---

## Prohibited Commands / Cautions

> If the project CLAUDE.md defines allowed/denied command lists, those take precedence. Below are general principles.

- `npx <command>`, `npm run <script>` — if the project uses pnpm/yarn, use that package manager
- `node_modules/.bin/<tool>` — use package-manager scripts instead of direct paths
- Prefer platform-independent commands (package-manager scripts, task runners) over OS-specific shell invocations (`cmd.exe /c ...`, `powershell.exe -Command ...`). When an OS-specific command is unavoidable, note both platform forms (`cp` / `Copy-Item`, etc.)
- `git commit`, `git push` — only when the user explicitly says "commit"/"push". Otherwise the user runs these directly

---

## Self-Check Before Reporting

Ask yourself the following before writing the verification report. Clean up simple items caused by your own change before reporting. Do not silently fix scope expansions, design mismatches, or items needing user decisions — report them to the main thread instead. The design doc referenced below is located per the `mak:design-doc-template` save-path rule, which also owns the §5.0 status-column rule.

- [ ] Does every changed line connect directly to the user's request? (Precise Changes)
- [ ] Did any unrequested "improvement" of adjacent code/comments/formatting slip in? (Precise Changes)
- [ ] Are all unused imports/variables/functions introduced by your change cleaned up? (Precise Changes)
- [ ] Were unrequested features / speculative flexibility / impossible-scenario error handling added? (Simplicity)
- [ ] Are all items in the design doc §5.0 success criteria or `Step → verify` table actually met? (Goal-driven)
- [ ] For each step whose verify criterion just passed, was its §5.0 `Status` cell updated? (Goal-driven)

## Report Format

After verification, report in this format (render headings in the user's language). The first table records **every check that applies and whether it ran** — when the project declares its own verification commands (§Verification Order priority rule), report those in place of the default rows. Drop a row only when that check does not exist for this project.

```
## Verification Results

| Step | Command | Result |
| :--- | :--- | :--- |
| ① Build/type check | `<command run>` | ✅ pass / ❌ fail / ⏭ not run |
| ② Lint | `<command run>` | ✅ pass / ❌ fail / ⏭ not run |
| ③ Unit tests | `<command run>` | ✅ pass / ❌ fail / ⏭ not run |
| ④ Format | `<command run>` | ✅ pass / ⏭ skipped |
| ⑤ Manual scenario | — | ✅ confirmed / ⚠️ not verifiable |

## Predefined Success Criteria vs Results

| # | Step (design doc §5.0) | Success criterion | Actual result |
| :- | :--- | :--- | :--- |
| 1 | <Step> | <verify> | ✅ met / ❌ not met |
| 2 | <Step> | <verify> | ✅ met / ❌ not met |
```

If the design doc has no `Step → verify` table, replace the second table with a one-line statement of whether the success criterion was met.

When all steps pass and all criteria are met: `✅ All verification steps and success criteria passed`
