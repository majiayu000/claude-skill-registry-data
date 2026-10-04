---
name: threat-intelligence-report-en
description: Research, verify, assess, and publish evidence-based cyber threat intelligence from dark web forums, Telegram, ransomware leak sites, breach claims, threat campaigns, malware reports, vulnerabilities, and IOC/TTP data. Use when producing a threat intelligence report, validating an alleged data leak, identifying recycled or synthetic datasets, building an incident timeline, separating claims from evidence, drafting an internal briefing, or preparing a public TEAM_D4rkn3ttz post.
---

# Produce Threat Intelligence Reports

## Start with the intelligence requirement

Define the decision the output must support in one sentence. Examples:

- Determine whether an alleged breach is new and authentic.
- Explain a campaign's TTPs and its relevance to the target audience.
- Establish which facts are safe and sufficiently verified for public reporting.

If the target, period, audience, and output are clear, proceed without asking broad questions. Ask only when missing information would materially change the analysis.

Read the following references as needed:

- `references/verification.md` for source evaluation, breach validation, confidence, and risk scoring.
- `references/output-formats.md` for report, briefing, and social-post templates.
- `references/examples.md` for representative workflows and expected behavior.

## Apply the core rules

1. Treat every actor, seller, channel, and leak-site statement as a **claim** until verified.
2. Distinguish observed facts, third-party claims, analytical judgments, hypotheses, and unknowns at sentence level.
3. Separate the incident date, publication date, repost date, and analyst observation date.
4. Prefer primary sources: original posts, affected-organization statements, vendor advisories, government notices, technical reports, and research papers.
5. Do not count several articles repeating the same source as independent corroboration.
6. Use nuanced verdicts: `confirmed`, `partially confirmed`, `repackaged historical data`, `indicators of synthetic or manipulated data`, or `unverified`.
7. Attach evidence, limitations, confidence, and change conditions to every important conclusion.
8. Minimize and mask personal data, victim data, credentials, access details, and information that would enable abuse.
9. Do not recommend illegal access, purchasing stolen data, direct engagement with criminals, credential use, or malware execution.
10. Use conservative attribution. Reused handles, PGP keys, wallets, wording, or infrastructure indicate possible linkage, not confirmed identity or state sponsorship.

## Follow the workflow

### 1. Build a collection plan

Group sources into:

- originating claim
- original evidence
- official confirmation
- independent technical analysis
- contextual material

Write the working hypothesis and the evidence that would disprove it before expanding collection.

### 2. Preserve provenance and time

Record, when available:

- URL, platform, channel, account, and post ID
- authoring time, observation time, and timezone
- title, filename, file size, and cryptographic hash
- original capture and a separate redacted or translated copy

Use absolute dates. Display KST alongside the original timezone when the audience is Korean.

### 3. Create a claim-evidence ledger

| Claim | Source | Direct observation | Corroboration | Counterevidence or limitation | Status |
|---|---|---|---|---|---|

Do not draft the headline before the ledger supports it.

### 4. Verify the evidence

Apply the relevant checklist in `references/verification.md`.

For leaked datasets, examine schema, value realism, record-count plausibility, duplication, freshness, provenance, seller role, and abuse potential. Values such as `example.com`, sequential phone numbers, nonexistent addresses, and unnaturally clean distributions are indicators of synthetic data, but no single indicator proves fabrication.

For campaigns and malware, validate the intrusion path, execution chain, persistence, command-and-control behavior, payloads, affected versions, and IOC context against primary technical sources.

### 5. Assign a verdict and confidence

Present the evidence before the verdict. Assign `high`, `medium`, or `low` confidence and state:

- why the confidence level is appropriate
- what remains unknown
- what new evidence would change the assessment

Evaluate risk separately from authenticity. A false leak claim can still create reputational harm, customer inquiries, investigation costs, and media pressure.

### 6. Convert findings into intelligence

Answer:

- What happened?
- What is verified, disputed, or unknown?
- Why does it matter to this audience?
- What harm or attack path could follow?
- What should be checked or done now?

Provide IOC context, first/last-seen timestamps, confidence, and recommended defensive use. Do not publish raw personal data or high-risk access information.

### 7. Draft for the requested audience

Use the requested output format. If none is specified, produce a concise assessment first and offer a full report or public-post draft only when useful. Follow `references/output-formats.md`.

### 8. Pass the publication gate

Do not post, send, or publish without explicit user approval. Before publication, verify that:

- the headline is no stronger than the evidence
- dates and timezones are accurate
- claims are distinct from verified facts
- victim and personal data are protected
- citations appear close to the claims they support
- uncertainty and correction conditions are visible
- Korean and English versions express the same confidence

### 9. Learn from reviewed examples

When the user supplies a prior report or edited draft, extract:

- recurring structure and tone
- mandatory evidence checks
- phrases to avoid
- preferred length by channel
- differences from the current workflow

Apply one-off edits to the current output. Promote a preference to a reusable rule only after it appears consistently or the user confirms it.

## Completion criteria

Include at minimum: key assessment, supporting evidence, uncertainty, impact, recommended action, and sources. When evidence is insufficient, provide a current assessment, intelligence gaps, and next verification steps instead of presenting an unsupported finished report.
