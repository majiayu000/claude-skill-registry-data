---
name: factory-human-digest
description: "Summarize configured work that needs human judgment. Use for a read-only decision queue."
license: MIT
compatibility: "Works in Claude Code, Codex, Cursor, and Agent Skills-compatible harnesses when the required host tools are available."
metadata:
  author: Builder.io
  source: BuilderIO/skills
  source-commit: fd8f20a879b507cf09feba08663a1edf7a949353
  owner: software-factory
  risk: low
  capabilities: builderio,factory-human-review
  installer-group: factory
---

# Factory Human Digest

> Start with the [Factory guide](../factory/references/factory-guide.md) for workflow
> setup and configuration.

Read `.agent-factory/config.yaml` and apply the optional
`skill_prompts.factory-human-digest` entry as additional project guidance.
Inspect only the repositories and sources it authorizes.

## Choose the scope

For a manual run with no narrower request or workflow settings, include all
configured source categories, use the **last 7 days**, and report at **balanced**
granularity. A user can narrow or expand the request in ordinary language, for
example, “PRs only, last 30 days, detailed” or “everything from this week, brief.”
Use configured repository and source boundaries even when the requested time
window or category changes. For scheduled runs, use
`workflows.human-digest` from the config.

Categories can include pull requests, issues, feedback, errors, telemetry, and
stalled or failed delivery work. A category filter selects records to inspect;
it does not expand access to another project or integration.

## Find items that need a person

Read configured sources and repositories completely for the selected window.
Follow pagination and record the actual dates, filters, counts, and any source
that was unavailable or truncated. Include items held outside the normal
agent-handled flows, such as:

- pull requests waiting for human review, approval, a merge decision, or product
  judgment;
- issues, feedback, or errors held for missing context, unclear intent, risk,
  conflicting evidence, or a decision outside the configured automation rules;
- new answers to information requests that have not yet been re-triaged;
- recurring incidents, UX concerns, or delivery work that stopped without a
  verified resolution or safe authorized next step.

Exclude work that has a verified terminal outcome unless it reopened, recurred,
or received new information during the window. A label or agent summary alone
does not prove an item is resolved. If the source cannot distinguish pending
from resolved, report that uncertainty instead of guessing.

## Group patterns and preserve evidence

Group related items by the underlying user impact or failure pattern, not by
similar words alone. For each group, preserve the date range, count of distinct
records, source links, representative evidence, and the human decision needed.
Separate event volume from affected people or sessions unless the source has a
reliable identity definition. Keep unrelated reports separate even when one
summary would be shorter.

Use the configured granularity, or **balanced** by default:

- **Brief:** top groups, why each needs a person, and links to the source items.
- **Balanced:** grouped summaries, representative evidence, and a linked list
  of each item needing a decision.
- **Detailed:** one entry per item with relevant context, prior handling,
  evidence, and the exact decision or next step.

## Report; do not take the actions

Start with coverage: window, categories, repositories, sources, filters, and
pagination status. Then report recurring themes and the decision queue. For each
entry include links, why the normal flow did not handle it, prior replies or
dispositions, the decision required, and an owner or due date only when the
source provides one.

This workflow is read-only. Do not reply, approve, merge, assign, close, change
status, or notify people from the digest. Route any requested action through
its owning Factory workflow and its separate configured policy. Missing or
partial source data must remain visible in the report; it is never evidence of
an empty queue.
