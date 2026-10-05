---
name: prompt-versioning-hygiene
description: This skill should be used when the user mentions "prompt engineering", "prompt versioning", "prompt management", "system prompt", "prompt template", "manage prompts", or "prompts scattered in code". It provides a methodology for treating prompts as versioned, reviewable, testable code rather than magic strings buried in application logic.
---

# Prompt Versioning Hygiene

## Purpose
Prompts are the highest-leverage, least-governed artifact in most LLM apps: a one-line edit to a system prompt can change behavior across every request, yet prompts are typically inline string literals that ship with no version, no review, and no test. This skill standardizes treating prompts as code, externalized, versioned, diffable, reviewed, and tested, so a prompt change is a deliberate, traceable, gated event instead of a silent regression waiting to happen. It is the connective tissue between the eval-authoring skill (which grades prompts) and the day-to-day discipline of changing them.

## The core problem: prompts as magic strings
```python
# The anti-pattern: prompt buried in logic, no version, no test, no review trail
def summarize(doc):
    return llm(f"You are a helpful assistant. Summarize this in 3 bullets: {doc}")
```
Nothing here can be diffed meaningfully, reviewed as a unit, rolled back independently, or A/B-tested. A behavior change and a prompt change are indistinguishable in the git history. The fix is to give every prompt an identity.

## The hygiene checklist

| Practice | Why it matters |
|---|---|
| **Externalize** prompts from logic (dedicated files/modules or a prompt registry) | Makes prompts findable, diffable, and reviewable on their own |
| **Version** each prompt (semantic version or content hash) | Lets you pin, roll back, and correlate an output to the exact prompt that produced it |
| **Review** prompt changes like code (PR, required approval) | A prompt edit is a behavior change; it deserves the same gate as a code change |
| **Test** every prompt against the eval suite before merge | Proves the change improved rather than regressed (see eval-authoring) |
| **Separate** prompt data from prompt logic | Keep the template text apart from the interpolation/assembly code |
| **Environment-aware** rendering (dev/staging/prod) | Iterate safely without touching production behavior |
| **Log the version** with each request | An incident is traceable to the exact prompt version live at the time |

## How the pieces fit
- **Externalize + version** give a prompt an identity you can point at.
- **Review + test** make a change to that identity a gated event, the review catches intent, the eval catches regression.
- **Environment-aware + logged version** close the loop operationally: you can ship a change to staging, prove it on evals, roll it to prod, and trace any output back to the prompt that made it.

## Signals that a codebase needs this
- Prompts are f-strings/template literals scattered across handlers and services.
- The same instruction is copy-pasted into several call sites (drift is guaranteed).
- There is no way to answer "which prompt version produced this bad output?"
- Prompt changes ride along inside unrelated feature PRs with no separate review.
- There are no tests that run when a prompt changes.

## Additional Resources
### Reference Files
- **`references/prompt-management.md`**: how to externalize prompts (dedicated files, a prompt module, or a registry/management tool), version them (semver vs. content hash), render per-environment, and review prompt changes; the trade-offs of in-repo vs. hosted prompt management.
- **`references/prompt-testing.md`**: how to test prompts as code and wire a prompt change into the eval suite so a regression fails CI, including snapshot/contract tests, the diff-review workflow, and rollback.
