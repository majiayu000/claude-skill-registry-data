---
name: eng-tech-docs
version: 1.0.0
description: Write or maintain technical documentation — READMEs, runbooks, API references, architecture docs — that a specific reader can act on without asking follow-ups.
author: matrixx0070
tags: [documentation, readme, runbook, api-docs, technical-writing, architecture]
capabilities: []
---

## When to use

Creating or updating any doc humans rely on to run, integrate with, or understand a system. Good docs answer the reader's next question before they ask it.

**Not for:** inline code comments, commit messages, or design debate that belongs in an ADR (use eng-architecture). This is reader-facing reference and how-to, not decision rationale.

## Method

1. **Identify the reader and their goal**: a new contributor getting set up, an on-call engineer mid-incident, or an integrator calling your API. Write for that one job; if two readers need different things, write two docs.
2. **Lead with the outcome.** Put "what this is and why you'd use it" in the first three lines. Bury nothing important below the fold.
3. **Make it runnable.** Every setup or usage step must be copy-pasteable and verified against a clean environment. If you can't run a step, mark it UNVERIFIED rather than implying it works.
4. **Match the form to the type:**
   - README → purpose, quickstart, config, common tasks, troubleshooting, links.
   - Runbook → alert/symptom, diagnosis steps, remediation commands, escalation, rollback.
   - API doc → endpoint, params, auth, request/response examples, error codes, rate limits.
   - Architecture → context diagram, components, data flow, key decisions (link ADRs).
5. **Show real (sanitized) values**, not `<placeholder>` soup a reader has to decode.
6. **State what's out of scope and add a "last verified" date.** A doc that lies is worse than none — if you can't verify a section, say so.

## Example

Runbook snippet for a "queue backing up" alert:

```
## Alert: order-queue depth > 10k
Symptom: OrderQueueDepth alarm; checkout latency climbing.
Diagnose: `aws sqs get-queue-attributes --queue-url $Q` → check
  ApproximateNumberOfMessages and consumer count in the orders dashboard.
Remediate: scale consumers → `kubectl scale deploy/order-worker --replicas=8`
Escalate: if depth still rising after 10m, page @payments-oncall.
Rollback: revert last order-worker deploy → `deploy rollback order-worker`
Last verified: 2026-07-11
```

## Pitfalls

- **Writing for no one** — a doc addressed to everyone helps no one; name the reader.
- **Steps that only run on your machine** because of an unstated prerequisite.
- **Placeholder soup** the reader must reverse-engineer into real values.
- **Stale docs left undated** — no "last verified" means readers can't judge trust.

## Output format

```
Doc type: <README | Runbook | API | Architecture>  Reader: <who + their goal>
<the document in Markdown, headings matched to the type above>
  - runnable examples with expected output
  - troubleshooting / FAQ where relevant
Out of scope: <what this doc does not cover>
Last verified: <YYYY-MM-DD>  Related: <links to ADRs / other docs>
```
