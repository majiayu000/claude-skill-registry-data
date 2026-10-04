---
name: trust-and-safety-review
description:
  Review product designs and implementation for abuse through user-generated content and interactions, including
  phishing, scams, harassment, spam, and moderation failures. Use for content safety, reporting, blocking, consent, and
  policy enforcement reviews. Produce findings and recommendations. Route technical vulnerabilities to
  app-security-review when available.
---

# Trust and Safety Review

Review how people can misuse the project's content and interaction flows to harm others, including when the software
works as designed. Ground the review in the actual product, audience, and existing controls.

This skill has no required stack, runtime, hosting provider, browser, or tool. It can review source code, product
designs, API contracts, CLI workflows, or a running application using the access already available.

## Scope and routing

- Cover user-controlled profiles, forms, surveys, messages, uploads, links, listings, invitations, and other content or
  interactions that the project actually supports. Public publishing is not a prerequisite.
- Review harmful use, exposure, distribution, consent, and the moderation lifecycle. A legitimate form used to solicit
  passwords is a trust-and-safety concern. Script execution through that form is an application security concern.
- Route technical vulnerabilities such as injection, authentication bypass, or unauthorized API access to
  `app-security-review` when available. Neither skill requires the other to be installed.
- When a problem spans both domains, explain the connection and avoid duplicate findings. Stay within the requested
  review scope; flag an adjacent issue briefly without silently starting another audit.
- A review produces findings and recommendations. Apply fixes or change moderation settings only when the user's request
  also authorizes those actions.

## Understand the current project

Read the relevant project instructions, product documentation, policies, and implementation before choosing risks. For a
scoped feature or diff, follow its surrounding flows and existing controls without expanding to the entire project.
Infer what is supported by evidence and identify consequential unknowns.

Establish:

- Who creates content, who receives or discovers it, and which roles or accounts can moderate it.
- What users control, including display names, branding, destinations, files, form fields, and notification text.
- How content moves through creation, editing, publication, sharing, reporting, enforcement, appeal, and removal.
- Which surfaces distribute it, including APIs, command-line imports, embeds, search results, exports, and email.
- Existing visibility defaults, consent choices, blocking rules, quotas, review queues, and operational capacity.

Do not assume a public feed, payments, minors, direct messaging, or a staffed moderation team. Select risks according to
the supported product and audience. If only a design or one component is available, distinguish proposed safeguards from
implemented behavior and identify what cannot be verified.

## Review relevant abuse paths

For each plausible scenario, connect the actor, feature, audience, harm, and controls that prevent or limit it. Look for
paths that bypass the intended safety workflow, such as editing content after approval or publishing through an API or
CLI that omits the same checks.

- **Phishing, scams, and impersonation:** Misleading identities or platform branding, credential or payment collection,
  requests for identity documents, deceptive destinations, suspicious downloads, and off-platform scam funnels.
  Distinguish legitimate collection workflows from deception and unnecessary sensitive-data requests.
- **Harassment and unwanted contact:** Threats, hateful or targeted abuse, repeated contact after blocking, coordinated
  harassment, and ways to expose someone to an audience they did not choose.
- **Privacy and exploitation:** Doxxing, non-consensual sharing, sexual exploitation, coercion, and misuse of personal
  details or media. Consider age-related safeguards when the audience or feature makes them relevant.
- **Spam and manipulation:** Bulk invitations or messages, repeated uploads, fake identities, ban evasion, reputation
  manipulation, and incentives that amplify harmful content or reward abusive behavior.
- **Moderation failures:** Hard-to-find reporting, reports that expose the reporter, abusive mass-reporting, missing
  reasons or appeals, inconsistent enforcement, unsafe moderator exposure, and unmanageable review queues.
- **Content lifecycle gaps:** Rejected content resurfacing through edits, previews, notifications, caches, exports, or
  alternate clients; deleted or restricted content continuing to reach recipients.

Account for multilingual content, obfuscation, images, and linked destinations when those formats exist. Keyword
matching alone does not establish intent or reliably prevent abuse. Separate a credible abuse opportunity from evidence
that abuse has actually occurred.

## Recommend proportionate controls

Tie each recommendation to an identified path and to the project's existing architecture. Prefer controls that reduce
likely harm with manageable implementation and review effort. Preserve legitimate use and consider false positives,
language coverage, evasion, and the privacy cost of detection.

Keep four responsibilities distinct:

- **Detection:** Signals, user reports, contextual checks, and review triggers appropriate to the content.
- **Enforcement:** Warnings, publication limits, quarantine, removal, or account restrictions with clear scope.
- **Review and appeal:** Reasons, recourse, and human review for ambiguous or high-impact enforcement, with an explicit
  operating plan when human reviewers are not currently available.
- **Observability:** Useful decision records and abuse trends with appropriate access, retention, and redaction.

Identify where controls must be shared across entry points and reapplied after edits. Separate practical near-term
changes from longer-term options when that distinction helps prioritize work. Suggest policy categories only when
needed, and label proposed policy choices as proposals. Do not make definitive legal claims from content signals.

## Deliver the review

Use the user's requested format, or provide a concise report with:

- The scope, relevant product context, inspected evidence, and access limitations.
- Prioritized risks, each with the affected flow, actor, plausible harm, existing controls, and concrete gap. Cite code
  locations, design sections, or observed behavior; separate observed weaknesses from scenarios to validate.
- Recommended controls, their implementation points and tradeoffs, and how to verify that they work across the
  applicable interfaces without blocking legitimate use.
- Open questions or operational decisions that materially affect the conclusion.

Base priority on likely harm, reach, repeatability, and existing mitigations. State confidence separately. If no
actionable gaps are supported, say so and describe the review boundary without claiming the product is abuse-proof.
