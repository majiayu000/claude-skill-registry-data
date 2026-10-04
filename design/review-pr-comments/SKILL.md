---
name: review-pr-comments
description: Review and triage PR review comments (from Copilot, bots, or human reviewers) against the actual codebase. Use when a user wants to evaluate the validity, priority, or accuracy of PR review comments before deciding which ones to act on. Also handles applying approved fixes. Triggers on requests like "review all comments in this PR", "evaluate PR feedback", "which PR comments are valid", "apply the PR suggestions".
---

# Review PR Comments

Systematically pull, evaluate, and optionally apply review comments from a pull request.

## Workflow

### 1. Fetch PR Data

Use `github-pull-request_activePullRequest` (or `github-pull-request_openPullRequest` if not checked out).

Extract from the result:

- `comments[]` — inline review comments (attached to files/lines)
- `timelineComments[]` — general PR comments (overviews, bots, etc.)
- `changes[]` — the actual diff

### 2. Read Affected Code

For each comment with a `file` field, read the **current** file at the referenced location — not just the diff. The diff shows what was changed; the file shows what exists now.

Read enough context (±20 lines) to understand whether the suggestion is already satisfied, partially applied, or still needed.

If a comment references another file as a "pattern" or "example," read that file too to verify the claim.

### 3. Evaluate Each Comment

For every comment assess:

| Dimension     | Questions                                                                                                                            |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Valid?**    | Does the issue actually exist in the current code? Has it already been fixed?                                                        |
| **Accurate?** | Are file paths, line numbers, and named references correct?                                                                          |
| **Priority**  | Would ignoring it cause a bug / bad UX / policy violation (High), a maintainability issue (Medium), or is it purely stylistic (Low)? |
| **Action**    | Apply immediately / Apply optionally / Skip with reason                                                                              |

### 4. Report

Produce a summary table per comment:

```
| # | File | Key / Location | Valid? | Priority | Action |
|---|------|---------------|--------|----------|--------|
| 1 | foo.tsx | line 29 | ✅ Yes | Medium | Apply |
| 2 | bar.tsx | line 193 | ⚠️ Partial | Low | Optional |
```

Include a short rationale for each verdict. Call out inaccuracies in the comment itself (wrong line numbers, wrong file references) even if the underlying suggestion is valid.

### 5. Apply Fixes (if instructed)

When the user confirms, apply all approved changes using targeted edits (not wholesale file replacement). Re-read the current file state before editing — it may have changed since the PR was opened.

### 6. Generate Live Test Prompt (after fixes applied)

After all approved fixes have been applied, produce a **ready-to-paste agent prompt** that verifies the PR's actual runtime behavior inside LibrAgent.

**When to generate:**

- After Step 5 completes, OR
- When the user asks "테스트 프롬프트 만들어줘" / "give me a test prompt"

**How to construct the prompt:**

1. Read the PR `changes[]` diff to identify what runtime behavior changed (not just what code changed).
2. For each changed behavior, design a concrete, observable test step the agent can execute with its tools (shell commands, file search, browser, etc.).
3. Instruct the agent to report actual output for each step, not just "success/fail."

**Template:**

```
다음 변경 사항의 실동작을 순서대로 검증해줘.

## 테스트 N: [변경 이름]
1. [도구 호출 또는 명령]
2. [예상 출력 또는 확인 기준]
3. [엣지 케이스가 있다면 추가 단계]

각 단계의 실제 출력을 그대로 보고해줘.
```

**Rules:**

- Each test must be fully self-contained (set up its own fixtures if needed).
- Expected output must be **concrete and observable** — not "should work correctly" but "output contains `./subdir`".
- Cover the main success path AND at least one error/edge case per change.
- Clean up any temp files/directories created during tests at the end.

## Evaluation Heuristics

**Mark as High priority if:**

- Missing fallback/defaultValue on i18n keys that could surface raw key strings to users
- Type safety violations (unsafe casts, missing validation)
- Logic bugs or race conditions
- Accessibility regressions

**Mark as Medium priority if:**

- Inconsistency with an established codebase pattern
- Missing error handling that degrades gracefully
- Performance issues under realistic load

**Mark as Low / Optional if:**

- Purely cosmetic or stylistic (matches one valid style but not the only one)
- Suggestion is already covered by a neighboring line or fallback
- The referenced "pattern" doesn't actually match the claim

**Mark as Invalid if:**

- The issue no longer exists in the current file state
- The suggestion would introduce a regression
- The referenced example file/line doesn't exist or doesn't demonstrate what is claimed

## Notes

- Bot reviewers (Copilot, Jules, etc.) often reference incorrect line numbers — always verify against the actual file.
- `defaultValue` in i18next `t()` matters most for **plural keys** (`_one`/`_other` suffix). For simple interpolation keys that exist in all locale files, it is optional.
- When a comment says "follow the pattern in X:Y-Z", read those lines to confirm the pattern actually exists there before accepting the claim.
