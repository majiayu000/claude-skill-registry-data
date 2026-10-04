---
name: legal-brief
version: 1.0.0
description: Produce a decision-ready legal briefing — daily digest, topic research, or incident write-up — scoped to what a non-lawyer stakeholder needs to decide or act on.
author: matrixx0070
tags: [legal, briefing, research, summary, risk, escalation]
capabilities: []
---

## When to use
Use this when a non-lawyer needs legal context fast enough to act: a daily digest of active matters, a focused briefing on one topic (a new regulation, a contract type, a jurisdiction), or a write-up of an incident. Your output is a summary that drives a decision, not a law-review memo.

**Not for:** giving legal advice or opinions on liability (escalate to counsel), drafting the actual filing or contract (use `legal-review-contract` / `legal-response`), or rating a single risk in depth (use `legal-risk-assessment`).

## Method
1. **Fix mode and audience.** Daily / Topic / Incident, and who reads it (exec, PM, ops). *Decision point:* if the audience is a lawyer, drop the plain-language layer and cite primary sources instead.
2. **Gather sources with dates.** Active matters, statutes/regs, contracts, prior guidance, incident facts. Record each source's date — stale law is a trap.
3. **Extract only what the reader can act on.** Pull facts, deadlines, obligations, and risks that touch their decisions; discard background.
4. **Separate law from opinion.** Tag every point [requirement] (settled), [interpretation] (judgment call), or [open] (unresolved). *Decision point:* if the decision hinges on an [interpretation] or [open] item, route it to counsel before the reader acts.
5. **Surface deadlines and owners.** Every filing date, response window, or renewal trigger gets a named owner.
6. **Flag escalation.** List anything needing licensed-attorney review before action.

## Example
PM asks: "Can we launch the referral promo in the EU next week?" Topic brief, PM audience. Bottom line: "Launchable in 3 of 4 target countries; Germany needs a disclosure change; France is an open question." Key points: [requirement] GDPR consent for referral emails; [interpretation] German UWG may treat the reward as an unfair inducement; [open] French DGCCRF stance unconfirmed. Deadline: legal sign-off by Thu (owner: Priya). Escalate: German UWG interpretation to counsel.

## Pitfalls
- **Burying the decision under background.** The reader wants the answer first; context second.
- **Mixing settled law with your guess.** An untagged interpretation reads as fact and gets acted on as one.
- **Undated sources.** A regulation summary without an "as of" date silently rots.
- **Owner-less deadlines.** "File by the 15th" with no name means nobody files.

## Output format
```
Mode / Audience / Date:
Bottom line: <2-3 sentences>
Key points:
  - [requirement|interpretation|open] <point>
Deadlines & owners:
  | Item | Date | Owner |
Risks (ranked): <risk> — exposure: <impact>
Escalate to counsel: <items needing attorney review>
Sources: <source — as of DATE>
```

## Mode reference
Pick the mode before you write a word. Each mode has a different job, a different must-include set, and a different length ceiling. Overrunning the ceiling is a signal you have drifted from decision-scoped into memo territory.

| Mode | Purpose | Must include | Length target |
|------|---------|--------------|---------------|
| Daily digest | Keep a stakeholder current on the portfolio of active matters | Active matters (one line each), deadlines this week, new developments since last digest, explicit "nothing to action" flag when a matter is quiet | Scannable single page |
| Topic brief | Answer one focused legal question well enough to act | Bottom-line decision up top, the 3-5 load-bearing legal points (each tagged), a jurisdiction map where scope is multi-country, open questions | ~1 page |
| Incident write-up | Give responders a shared factual picture and the clocks that are running | Timeline of facts, what is known vs. unknown (kept separate), preservation / legal-hold status, notification obligations and their clocks, immediate actions, escalation path | As long as the facts require; keep the summary front-loaded |

For a daily digest, the "nothing to action" flag matters as much as the alerts — silence is ambiguous, an explicit "no action needed on X this week" is not. For an incident, never let a guess sit in the "known" column; unconfirmed facts live under "unknown" until verified.

## Tagging discipline
Every legal point you surface gets exactly one tag so the reader can tell settled law from your read of it:

- **[requirement]** — settled, black-letter obligation. *Example:* "[requirement] GDPR Art. 33 requires notice to the supervisory authority within 72 hours of becoming aware of a personal-data breach."
- **[interpretation]** — a judgment call where reasonable lawyers could differ, or where applying the rule to these facts is not obvious. *Example:* "[interpretation] The referral reward likely counts as a 'material connection' requiring disclosure, but the guidance predates this promo structure."
- **[open]** — unresolved; you do not yet know the answer. *Example:* "[open] Whether the French regulator treats this as a lottery is unconfirmed."

The rule: **any decision that hinges on an [interpretation] or [open] item routes to counsel before the reader acts.** A [requirement] the reader can generally act on directly; the other two tags are stop-and-ask signals, not footnotes. Never leave a point untagged — an untagged interpretation reads as fact and gets acted on as one.

## Breach / incident clocks
Incident write-ups almost always trigger a notification clock, and the clocks start early — usually on "awareness," not on confirmation or remediation. Use this as a general orientation table, then confirm the specific applicable law and its exact triggers with counsel; deadlines and thresholds vary by jurisdiction, sector, and the facts.

| Regime | Notification trigger | Deadline |
|--------|---------------------|----------|
| GDPR | Personal-data breach → supervisory authority | 72 hours from awareness; affected data subjects "without undue delay" if high risk to their rights |
| US state breach laws | Breach of defined personal information (varies by state) | "Most expedient time / without unreasonable delay"; some states cap at 30-60 days |
| HIPAA | Breach of unsecured protected health information | Individuals within 60 days; HHS within 60 days (large breaches) or annually (smaller); media for large breaches |
| SEC cyber disclosure | Determination that a cybersecurity incident is material | Form 8-K within 4 business days of the materiality determination |
| PCI DSS | Suspected/confirmed cardholder-data compromise | Notify your acquirer/card brands immediately |

These are reference points, not legal advice. Overlapping regimes can apply to a single incident, contractual notice duties may be shorter, and "awareness" is itself a legal determination — surface the clock, name the owner, and escalate the trigger question to counsel.

## Reference
- **Date every source.** Write "as of DATE" beside each authority. Law changes; a summary with no date silently rots and the stale-law trap is how confidently-wrong briefs happen. If you cannot date a source, say so.
- **Bottom line first.** Lead with the decision or answer, then the support. A reader who stops after the first paragraph should still have the actionable takeaway. Structure descends from conclusion → load-bearing points → detail, never the reverse.
- **Stay decision-scoped.** This is a briefing, not a memo. Include what the reader needs to decide or act; cut the background, the survey of every edge case, and the second lawyer's footnotes. If the reader is another lawyer who needs the full analysis, that is a different deliverable — escalate rather than expand.
