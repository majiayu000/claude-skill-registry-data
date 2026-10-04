---
name: plugin-submission
description: Govern discovery, eligibility, and submission of a plugin or skill to official directories, registries, marketplaces, and curated GitHub lists. Use when preparing or sending plugin listings, marketplace forms, directory PRs, or repository recommendations; require current policy evidence and a final human confirmation before every external submission.
---

# Plugin Submission

Treat every public listing as an external representation of the project. Submit only an
artifact that the destination's current policy accepts, and retain a receipt for every
send.

## Workflow

1. **Classify the destination and artifact.** Determine whether it accepts a full
   plugin, a repository, or one standalone `SKILL.md`. Do not describe a multi-skill
   plugin as one skill, or split a skill bundle without an explicit portable artifact.
2. **Read the current primary policy.** Use the destination's official submission
   instructions or `CONTRIBUTING.md`; record its URL, access requirements, licence and
   validation rules, and any limits on automated or AI-assisted submissions.
3. **Validate eligibility.** Check the public candidate URL, release/tag, licence as
   detected by the hosting platform, manifest/schema validity, documentation, and the
   destination-specific validator. Treat a mismatch or unmet requirement as `blocked`,
   not as an invitation to bypass it.
4. **Prepare one destination matrix.** For each target, record: destination, artifact,
   policy evidence, status (`ready`, `blocked`, `deferred`, or `human-only`), exact
   payload, and rollback action. Reuse the canonical repository description; minimise
   personal data and never add an email without explicit permission.
5. **Stage, then confirm.** Fill or draft public data only after the operator has
   approved the destination. Immediately before clicking a submit control, opening a
   PR, or sending a recommendation, restate the exact target and payload and obtain a
   final human confirmation. A single confirmation may cover multiple named sends only
   when the full set and payloads are shown together.
6. **Send through the permitted route.** Use a form, PR, issue, or API only when the
   policy permits that route. Never act where a policy requires a human-authored
   recommendation, prohibits AI-assisted submissions, or requires credentials/access
   the operator has not supplied.
7. **Verify and record the receipt.** Capture the submission URL/identifier and status.
   If a listing is rejected or stale, record the reason and next eligible action. Roll
   back a repository contribution by closing its PR/issue when appropriate; external
   directory records require the destination's own removal/update path.

## Submission Gate

Do not send until all applicable checks pass:

- The target policy is current and supports the proposed artifact.
- The public repository and exact release are accessible.
- Project licence intent and platform-detected licence agree.
- Required validation has passed, including the destination's validator where available.
- The project has not overstated supported platforms, usage, security review, or
  affiliation.
- The operator has given final confirmation for the exact outgoing entries.

## Outputs

- A destination matrix with evidence URLs and eligibility verdicts.
- A staged payload for every ready target.
- Submission receipts, or an explicit blocked/deferred reason and owner.

## Anti-rationalisation

| Temptation | Gate |
|---|---|
| “It is close enough to call the bundle one skill.” | Submit the artifact type the directory actually accepts, or create a deliberate portable export first. |
| “The README says Apache, so platform metadata does not matter.” | Directories evaluate the public repository; resolve detected-licence mismatches before broad listing. |
| “The user asked to submit, so the final click is implied.” | A final confirmation binds authority to the exact external payload. |
| “A PR is harmless discovery.” | A public PR is a durable representation of the project and must follow the contributor policy. |
| “We can automate a human-only form.” | Human-only and no-AI policies are hard stops. |
