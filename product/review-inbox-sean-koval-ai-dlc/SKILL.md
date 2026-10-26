---
name: review-inbox
description: Use when triaging incoming ideas, requests, or notes into actionable work.
---

# Review Inbox

Consult repository scope and selected tracker priorities before recommending work.
For each item, return these fields: **Item/source; Classification; Evidence and
user decisions; Hypotheses/missing context; Duplicate or related work; Priority
rationale; Next action and decision**. Link existing references only when known;
never invent a ticket identifier. Separate observed evidence from requested
features and unverified assumptions. Explain priority through user impact,
confidence, effort and dependencies without fabricated numeric scores.

Choose the next action explicitly:

- **Stop** for an explicitly declined item, duplicate, out-of-scope or infeasible
  request. Preserve the reason and known reference; do not reopen or republish it.
- **Investigate** for an unclear problem, insufficient evidence or contradictory
  requirements. Use discovery for a bounded brief and evidence goal, including
  current behavior and compatibility for existing products.
- **Proceed** for a worthwhile bounded outcome supported by evidence and resolved
  material constraints within existing authorization. Reuse the canonical brief's
  outcome/requirement IDs; use needs-spec and the configured formal provider before
  implementation where required. Use prd-draft only when more rationale is useful.

End each item with `Decision: proceed|investigate|stop — <reason>`. This is triage,
not invented approval or automatic ticket publication. Publication or external
replies require the user's authorization; use services to validate and link
reviewed work. Separate personal notes from durable design/decisions. Do not
silently turn every idea into a ticket or force a stopped item through a PRD.

Resolve provider-specific commands from the configured role provider’s instructions.
The agent supplies judgment; services store, validate, and link artifacts.
