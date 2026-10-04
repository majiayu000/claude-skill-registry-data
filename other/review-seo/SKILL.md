---
name: review-seo
user-invocable: false
version: 1.1.0
author: "Gabriel Trabanco <1969593+gtrabanco@users.noreply.github.com>"
license: MIT
description: >
  Internal SEO review pass of the agentic-workflow review pack — composed
  in-turn by review-change and product-audit; not a menu entry. Checks changed
  web pages/routes for indexability, metadata, and structured data — applies
  only to public web surfaces. Findings only; never edits code.
---

# Review SEO (internal)

Composed by `review-change` / `product-audit` within their conversation — on any
agent, follow this file inline as the routed step. **Findings only; never edits,
never refactors.**

## Scope

The diff or path/glob the caller passes; default the current change vs the
default branch. State the scope at the top of the returned table.

## Checklist (evaluate EVERY item — none is optional; n/a must be stated)

- ✓ Read the project's SEO doc first (e.g. `docs/frontend/SEO.md`) — n/a all
  items with the reason if the product has no public web surface
- ✓ Every new/changed public page has a unique title and meta description
  within the project's declared lengths
- ✓ Canonical URL correct on new/changed routes (no accidental duplicates)
- ✓ Indexability intended = indexability actual (robots/noindex/sitemap state
  matches the page's purpose)
- ✓ One h1 per page; heading levels don't skip
- ✓ Structured data valid for the content type the project declares (cite the
  validator output when run)
- ✓ Links crawlable (real hrefs, not click handlers) on changed navigation
- ✓ Images on changed pages have descriptive filenames/alt where the SEO doc
  requires
- ✓ No render-blocking regression for primary content (content present without
  JS where the project declares SSR/SSG)

## Materiality bar

Report a row only when a competent user's outcome changes or a rule the project
explicitly declares is violated — cite the rule it violates beside the evidence.
Not findings: comment/punctuation typos, formatting-only drift, style preference
with no cited rule, hypothetical robustness beyond the SPEC's named scenarios.
An empty table with `Decision: PASS` is the expected result for a well-formed
change — never pad the table.

## Return exactly

```
REVIEW SEO — scope: <scope>

| # | Finding | Sev | Evidence | Suggested fix |
|---|---------|-----|----------|---------------|
| 1 | <what>  | critical|major|minor | <file:line> | <smallest action> |

Checklist: <n> evaluated, <n> pass, <n> findings, <n> n/a (<which + why>)
Summary: <1-2 sentences>
Decision: PASS | FAIL
```

FAIL if any critical or major finding is open; PASS otherwise. Minor findings
never block — they route to the caller's triage step.

## Done when

- Every checklist item was evaluated with evidence (file:line or command output)
  or explicitly marked n/a with the reason.
- The fixed-format block above is returned — nothing more, nothing less — and
  no code was changed.
