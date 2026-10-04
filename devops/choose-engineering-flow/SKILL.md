---
name: choose-engineering-flow
description: "Select the smallest useful Codex engineering workflow from this repository's existing skills. Use when a task spans multiple engineering concerns, the user is unsure which skill to invoke, or loading every specialist would waste context; return a recommendation only and do not execute the engineering task."
---

# Choose Engineering Flow

Use this explicit-only skill as an educational example of workflow routing. It
is not part of the recommended installable catalog; prefer clear specialist
descriptions and direct activation in normal work.

Recommend one entry skill and only the supporting skills that materially change
the work. Do not perform the requested engineering task.

## Route the request

1. Identify the requested outcome: implement, test, review, secure, operate, or
   coordinate.
2. Prefer one entry skill:
   - use `$engineering-loop` for an end-to-end feature or defect;
   - use `$test-software` for test-only work;
   - use `$review-code` for review-only work;
   - use `$review-security` for security-only analysis;
   - use `$orchestrate-engineering` only for complex work with genuinely
     independent workstreams.
3. Add at most the relevant domain specialist:
   - `$build-frontend` for rendered UI, client behavior, or accessibility;
   - `$build-backend` for APIs, services, persistence, jobs, or integrations;
   - `$operate-devops` for infrastructure, CI/CD, deployment, or operations.
4. Do not recommend a specialist already covered by the chosen entry skill
   unless its domain decisions are material.
5. Ask one concise question only when the answer would change the entry skill.

## Return the recommendation

Use this format:

```text
Start with: $skill-name
Add only if needed: $other-skill
Why: one sentence tied to the task
Suggested invocation: $skill-name <bounded request and done condition>
```

Omit `Add only if needed` when one skill is sufficient. Never recommend loading
the entire catalog by default.

## Acceptance criteria

- The recommendation uses existing skills rather than inventing a new workflow.
- One skill owns the task lifecycle.
- Supporting skills have a task-specific reason.
- The output is shorter than the task description it routes.
