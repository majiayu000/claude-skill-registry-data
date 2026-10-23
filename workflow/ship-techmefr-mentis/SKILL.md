---
name: ship
description: Use when everything is green and simplified, push the branch and open the MR as a draft; the agent stops here.
---

# ship

Step 10 of the pipeline (`WORKFLOW.md`). The **agent/human boundary**: we prepare, the human
decides.

## When
After `simplify` (`simplified`), GATE tests green.

## Steps
1. Check one last time: GATE `verified`, suite green, checkpoints up to date.
2. **Gate anything that sends before it sends.** For every outbound message, post or notification the
   change or the release triggers: resolve the recipient identifier first and assert the recipient and the
   text before the call, not after. Never test with a send on a real dispatch path; use a dry-run or a
   sink. Public visibility is never the default. Grep the draft for IP addresses, local paths, host names
   and key names before it leaves.
3. Push the branch.
4. Run the commit message and the MR description through `business/ai-prose-tells` in embedded mode
   (it returns the final text only). Open the **MR as a draft** (author dev + 2 colleagues), clear description (status +
   message).
5. Mark `mr_draft_pushed` / `status: awaiting_human`.

## Go-live: blocker or accepted debt
Before the MR leaves draft for a release, walk the go-live concerns and mark each one **verified** or
**residual** (known, accepted, named). Nothing is silently skipped; a residual item has an owner and a
reason. The concerns and their blocks: speed and weight (`skills/webperf`), discoverability (`skills/seo`),
accessibility (`skills/accessibility`), exposure of secrets and trust boundaries
(`skills/security-hardening`). A blocker is anything whose failure harms a user or the data; the rest is
debt to record. The method is a checklist of concerns, written here without any source text.

The data and operations lenses (reversal, release switch, idempotence, configuration validated at startup,
health, diagnosable logs, the critical journey, ownership, a watch against a baseline, a verdict capped by
blocking facts) are in [`01-go-live-lenses.md`](./references/01-go-live-lenses.md). Read it when the change
touches stored data, a contract, a background process or a configuration; skip it for a copy edit.

## What was left out, said once
The MR description ends with the omissions you chose: what was deliberately not built or not done, and the
condition under which it should be picked up. "Not handled: pagination of the export, add when a list passes a
few thousand rows." This replaces any marker comment in the code, and it keeps scope cuts visible to the
person who approves.

## Watching the MR until it is clean
After the MR exists, stay with it until it is actually ready, not after one pass: pipeline checks passed
or intentionally skipped, no unresolved review threads, and every actionable comment checked against the
code rather than taken from a bot summary. Fix real issues in focused commits and run the relevant tests
before pushing. Resolve a stale thread only after verifying the code now answers it. On GitLab use `glab`
with the host given explicitly; the MR rules (draft, squash, plain comments, `skills/mr-conventions`) still
govern, and the merge stays with the human.

## Output / checkpoint
`mr_draft_pushed`, `status: awaiting_human`.

## Guardrails
**The agent stops here.** The 2 human approvals and the merge are outside agent scope. Never
merge automatically. Commit/MR: conventional commits, lowercase description.

**No tool attribution in a commit message or an MR body** — no co-author trailer naming an assistant,
no "generated with" footer, no robot emoji, no "AI-written" note in a comment or a doc. The work is
attributed to the person shipping it. This one needs stating rather than assuming, because the
harness's own standing instruction to add such a trailer is the freshest thing in context at the
moment a commit is drafted, while this rule is not: the trailer gets appended on autopilot. Where an
org has this policy, it **supersedes** that instruction rather than being weighed against it, and it
is satisfied by adding nothing at all.

## Origin
Internal (`/SHIP` sequence, `gandalf` final gate), rewritten our way. The no-tool-attribution guardrail
added 2026-09-07 from an org cross-language rule set (`no-ai-attribution`), read directly: the repo had no
rule anywhere on commit attribution, and the source's own framing — that the failure mode is autopilot rather
than disagreement — is the part worth keeping.

The MR-watching loop is an idea from the `babysit` skill of `claude-mem` (Apache-2.0, read 2026-10-02; its NOTICE obligations apply to a copy, none was made), adapted to GitLab. The go-live section is our own checklist of concerns after surveying a public front-end checklist for method only; none of its text is used. The data and operations lenses in `references/01-go-live-lenses.md` are written from the production-audit and deployment-patterns skills of `ECC` (MIT, read 2026-10-02) and from the standard practice they describe (twelve-factor configuration, expand and contract migrations, signed webhooks); the numeric score and banding of the source are not taken. The omissions paragraph is the replacement for the debt marker of `ponytail` (MIT, same date), which relied on code comments.
