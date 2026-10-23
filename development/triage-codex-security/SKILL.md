---
name: triage-codex-security
description: Triage Codex Security findings for one repository into evidence-backed, explicitly approved outcomes. Use when clearing or reviewing a Codex Security finding queue; leave repository issue management to the consumer.
---

# Codex Security triage

Use for one repository per run. Produce finding results and the
[`codex-security-triage/v1`](references/handoff-v1.md) handoff. Do not create repository issues,
apply labels, milestones, or projects, or shepherd pull requests.

## Establish the evidence boundary

- Select `origin` when it exists. Otherwise select the only remote. If there are zero remotes or
  more than one, stop and ask which remote is authoritative.
- Normalize a GitHub SSH or HTTPS remote to lowercase `github.com/owner/repo` without `.git`.
- For another host, lowercase the host, remove a leading slash and a trailing `.git`, and preserve
  the path's case and segments.
- Resolve that remote's default branch, fetch it, and record `selectedRemote`,
  `canonicalRepository`, `defaultBranch`, and the fetched immutable `evidenceSha`.
- A dirty checkout is useful only when the user explicitly selects it for analysis. It cannot prove
  a hosted action.
- Require the hosted finding/repository selector to prove the same `canonicalRepository` before
  any hosted action. Block on mismatch or ambiguity. Do not infer a repository from a finding.
- If input names more than one repository, partition it and stop until each partition has a matching
  checkout. Do not carry a finding or evidence SHA across repositories.

## Intake and analysis

- Prefer the official Codex Security plugin.
- When it is unavailable, use the trusted official `@openai/codex-security` CLI only for commands
  its installed version advertises, such as saved local findings, exports, and validation.
- Do not add a CLI, install software, or use a repository-local shadow executable automatically.
- For hosted findings, use a native authenticated browser only when one is available. Enumerate the
  queue read-only before proposing changes.
- If no browser is available, accept a user-provided export for analysis and block hosted writes.
- Do not use a browser-automation framework.
- Create one result for every finding before grouping:
  - `confirmed`: group a repository issue candidate, or use the provider's approved fix flow.
  - `needs_review`: group an investigation candidate. Do not close it.
  - `not_actionable`: record the exact supported reason and the evidence for closing it.
  - `overstated`: record why the finding is valid but its severity should be lowered.
- Trace the actual source, sink, boundary, and reachable controls. State the evidence paths and why
  they apply to the immutable `evidenceSha`. Uncertainty is `needs_review`, not a close.

## Approval and hosted changes

- Present the findings and the proposed action before every hosted write.
- Each approval wave contains at most 25 findings. Stop and wait for an affirmative response
  approving the exact finding IDs and actions in the current wave before any Close, severity, or
  provider pull-request write.
- Approval is session-bound. A restart, lost context, repository mismatch, changed state, or an
  ambiguous approval requires a fresh enumeration and a new approval.
- Re-read each finding immediately before and after a write. Do not retry a hosted write blindly.
- For a provider fix, use the provider UI to create the pull request, then verify and return its
  number, URL, and provenance in the handoff. The consuming repository decides whether to shepherd
  that pull request.

## Public boundary

Keep this plugin provider-neutral and public.

- Do not copy official prompts.
- Do not include credentials.
- Do not commit real findings, private paths, queue counts, or exports.
- Use synthetic fixtures for contract validation.
