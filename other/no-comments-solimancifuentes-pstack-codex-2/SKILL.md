---
name: no-comments
description: "Spawn Comment Sicko, fix accepted findings, and offer encodings for claimed constraints."
disable-model-invocation: true
---

# No comments

Use an independent Comment Sicko review and apply only accepted findings. Read [CODEX.md](../../CODEX.md) for delegation, model selection, and authority.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the actual base branch, defaulting to `main` only when that branch exists. Include authorized working-tree changes. The scope is the caller's fence, not permission to clean up the whole repository.

## Steps

1. Resolve this plugin's `agents/comment-sicko.md`. Launch an available host-native independent reviewer with its readable absolute path or supplied prompt contents, the exact scope, and an explicit read-only assignment. Tell it to read the prompt reference. There is no custom-agent subtype registration. The reviewer proposes deletions and flags and writes no files.
2. Inspect the report against the actual source. Reject scope escapes, application-code proposals disguised as comment deletions, exception-protected deletions, misstated `MUST KILL` reasons, and flags treating kept intentional code as guilty. Audit scoped lint and TypeScript suppressions. A suppression of a correctness or safety rule requires investigation and a root-cause fix, not blind removal. Preserve legal notices, public API contracts, proven external constraints, justified formatting directives, and constraint links. Before accepting thin `IMPORTANT` or `do not remove` kills or keeps, use `how` or `why` on the symbol. Ambiguous facts get the narrowest available evidence check. Rerun one rejected review with the failure named. A second rejected report leaves the workflow failed and open.
3. The coordinator applies accepted comment-only deletions within scope. It owns the resulting diff. For trivial accepted refactor flags, use the real API, remove a dead path, or drop an unused parameter only when that implementation work is within the caller's authority. If a fix needs a new shape, run `architect` once for the accepted set and stop at the sketch. Report proposals outside the scope as open.
4. Implement authorized root-cause fixes, then verify behavior and inspect the real diff. Preserve required correctness/safety suppressions until the underlying issue has been resolved and the relevant checker passes. `principle-fix-root-causes` and `principle-redesign-from-first-principles` guide the fix but never widen the scope. Do not add symptom guards solely to quiet the review.
5. For a comment that states a constraint such as `do not remove`, keep a proven external constraint. Offer an in-scope type, runtime check, test, or CI lint where it can enforce the claim. Wait for interactive approval unless that encoding was already approved by the caller. In an unattended run without that approval, leave the constraint intact and report the proposal open. Do not delete an unenforced constraint merely because approval is pending.
6. Report proposed and applied deletions separately, retained/restored comments, reruns, `MUST KILL` flags, any architect sketch, authorized fixes, encoding offers, accepted encodings, and remaining work. A report-only or blocked review is not a completed cleanup.
