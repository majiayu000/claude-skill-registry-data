---
name: cs-kb-article
version: 1.0.0
description: Turn a resolved support issue into a search-friendly, self-service knowledge-base article that deflects future tickets — with internal notes kept separate.
author: matrixx0070
tags: [customer-support, knowledge-base, documentation, self-service, writing, deflection]
capabilities: []
---

## When to use

Use this after an issue is resolved and likely to recur, or when several customers hit the same thing. Capture the fix once so customers self-serve and agents stop re-solving it.

**Not for:** one-off issues unlikely to repeat, answering a single live ticket (cs-draft-response), or internal runbooks. If you cannot yet confirm the fix works, research it first (cs-research).

## Method

1. Title it as the problem the reader searches for, in their words — "Export fails with 'file too large'", not internal jargon. **Decision point:** if you would not type this phrase into search, rewrite it.
2. Add a one-line summary and an "applies to" note (plan, platform, version) so readers self-qualify fast.
3. List symptoms exactly as customers experience them — error text, screenshots, behavior — so they confirm they are in the right place.
4. Give the resolution as numbered, testable steps: one action per step, expected result after key steps, and any prerequisites or permissions.
5. Add an "if that didn't work" branch, and where useful the root cause in plain language so readers understand rather than blindly paste.
6. **Decision point:** before publishing, strip every internal-only detail (ticket IDs, engineer names, unshipped fixes) into a separate internal-notes block.

## Example

> **Title:** "Export fails with 'file too large'"
> **Applies to:** All plans · Web · v3.0+
> **Symptoms:** Export button spins, then shows "file too large (>500MB)".
> **Resolution:** 1) Open Export → Options. 2) Set format to CSV (not XLSX). 3) Under Range, split into date chunks under 500MB. 4) Click Export — you'll get a download link per chunk.
> **If that didn't work:** contact support with your account ID.
> *(Internal: root cause = XLSX serializer memory ceiling, fix tracked in ENG-2214.)*

## Pitfalls

- Titling with internal jargon — it never surfaces in customer search.
- Multi-action steps — split "configure and export" into separate, testable steps.
- Leaking internal detail (ticket IDs, engineer names) into the published body.
- No "if that didn't work" path — readers who fail step 3 have nowhere to go.

## Output format

```
Title: <search-friendly>
Summary: <one line>
Applies to: <plan / platform / version>
Symptoms:
  - <as customer sees it>
Resolution:
  1. <one action> → expected: <result>
If that didn't work / root cause: <plain language + contact>
Related articles: <links>
---
Internal notes (do not publish): <ticket IDs, eng, caveats>
```
