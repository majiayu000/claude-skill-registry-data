---
name: multi-source-answer-synthesizer
description: "Combines information scattered across several company sources (wikis, documents, email, chat, tickets, CRM, code, meeting transcripts) into one coherent answer in which every claim is cited, weighing each source's reliability and recency, mapping where sources agree or conflict, flagging gaps, and rating overall confidence. Use when the user asks a question that needs more than one source to answer, wants several documents reconciled, or needs search results turned into a single attributed answer."
---

# Multi-Source Answer Synthesizer

You take what several organizational sources say about a question and turn it into one answer the user can trust and check. Weigh how reliable and how current each source is, lay out where they agree and where they clash, say plainly what none of them covers, and cite every statement back to its origin.

## Source types and what they're good for

Draw on the connected tools and sources available. Each kind tends to contribute something different:

- **Wikis** (Confluence, Notion, internal wikis) — authoritative reference: policies, procedures, architecture documents
- **File storage** (Google Drive, SharePoint, OneDrive) — working documents: proposals, specs, reports, presentations
- **Email** (Gmail, Outlook) — records of decisions: approval chains, clarifications, commitments
- **Chat** (Slack, Microsoft Teams) — context: informal decisions, the reasoning behind them, discussion threads
- **Work tracking** (Jira, Linear, Asana) — implementation context: ticket descriptions, acceptance criteria
- **CRM** (Salesforce, HubSpot) — customer context: account notes, deal history, meeting summaries
- **Code hosting** (GitHub, GitLab, Bitbucket) — technical ground truth: READMEs, code comments, ADRs, PR descriptions
- **Meeting capture** (Otter.ai, Fireflies, Notion, Docs) — decisions made out loud: agreements, action items, context that was never written down elsewhere

If no sources are connected, ask the user to hand you the source documents, or run the `unified-knowledge-search` skill first to locate them.

## Method

### 1. Assemble the sources

Gather every source that might bear on the user's question. They can arrive in any of these ways:

1. **From an earlier search** — output of the `unified-knowledge-search` skill, already ranked and attributed
2. **Named by the user** — e.g., "Synthesize these three documents"
3. **From uploaded documents or connected knowledge sources** — relevant internal documentation
4. **A mix** — some supplied by the user, some found through search

Log each source with:

- **Title** — the name of the document or item
- **Source** — platform and location, with a link
- **Author** — who created it or last changed it
- **Date** — when it was created or last modified
- **Type** — policy, spec, discussion, decision, working doc, and so on

**You need at least two sources.** If only one source speaks to the question, don't dress it up as a synthesis — present what it says directly, with attribution. A single-source answer doesn't call for this skill.

### 2. Judge how far to trust each source

Sources are not equally reliable. Place each one in a tier:

| Tier | Typical sources | Why it earns that weight |
|---|---|---|
| **1 — Authoritative** | Approved policies, signed contracts, published knowledge-base articles, merged code | Reviewed and officially released |
| **2 — Deliberate** | Architecture decision records, spec documents, formal meeting notes, approvals given by email | Written specifically to record a decision or a plan |
| **3 — Working** | Drafts, proposals, specs still in progress, open PRs | Could be incomplete, out of date, or replaced |
| **4 — Informal** | Chat messages, email threads, comments, spoken references captured in meeting notes | Conversational and dependent on context; may not be the final word |

When sources from different tiers disagree, go with the higher tier — unless the lower-tier source is clearly newer and the higher-tier one has gone stale.

Then decide whether each source still describes things as they are now:

- **Current** — changed within the last 90 days, or there's no sign that anything has replaced it
- **Potentially stale** — untouched for 90+ days on a topic that has probably moved on
- **Superseded** — a newer version or a later decision has taken its place

### 3. Pull out the claims

Go through each source and extract the specific claims that bear on the question. A claim is a single assertion of fact, policy, process, or opinion. For every claim, note:

- the claim, in the source's wording or a faithful paraphrase
- the source it came from, so you can attribute it
- that source's tier, so you can weight it for reliability
- its date, so you can weight it for recency

### 4. Compare the claims

Line the claims up across sources and classify how they relate:

| Relationship | What it means | What you do |
|---|---|---|
| **Agreement** | Two or more sources say the same thing | Treat it as high confidence and state it as established, citing every source |
| **Complementary** | Sources cover different parts of the question without contradicting each other | Weave them into one account, crediting each part to its source |
| **Conflict** | Sources contradict each other outright | Call it out: give both positions with attribution and your judgment of which is more likely current or authoritative |
| **Gap** | No source covers some part of the question | Mark it "[Not covered in available sources]" and don't paper over it with assumptions |

### 5. Write the answer

Build the answer in this order:

1. **Start with the consensus.** What the sources agree on is the part you can be most confident in, so it comes first.
2. **Layer in complementary detail.** Add what sources covering other aspects contribute, attributing each addition.
3. **Surface conflicts openly.** Where sources disagree, show both sides, explain which is probably more authoritative or up to date, and recommend which to follow — or recommend that the user verify.
4. **Name the gaps.** Say what the sources don't address. That's as useful as what they do say, because it tells the reader where to keep looking.
5. **Cite every claim.** Use inline citations so any statement can be checked against its original source.

### 6. Rate your confidence

Give the answer as a whole one confidence level:

- **High** — several authoritative sources agree, nothing conflicts, and the sources are current
- **Medium** — the sources broadly agree, but some are informal or possibly stale, and there are minor gaps
- **Low** — the sources conflict, key information is missing, or every source is informal or stale

## Answer template

```markdown
# [The question being answered]

**Confidence**: [High / Medium / Low]
**Sources consulted**: [count]
**Most recently updated source**: [date of the newest source]

---

## Synthesized answer

[A coherent account drawing on all sources. Every factual claim carries an inline citation in the form [Source Title, Date].]

[Example: "Under the travel expense policy, receipts must be submitted within 14 days of the trip [Travel Expense Policy v2, 2025-10-01]. Finance now checks this automatically when claims are filed [Slack #finance-ops, 2025-11-20], but claims for international trips are still reviewed by hand [FIN-2210, 2026-02-03]."]

---

## Where Sources Agree and Disagree

| Claim | Sources that agree | Sources that conflict | Confidence |
|-------|--------------------|-----------------------|------------|
| [Claim 1] | [Source A, Source B] | — | High |
| [Claim 2] | [Source C] | [Source D disagrees — says X] | Low |

---

## Conflicts to Resolve
- **[What the conflict is about]**: [Source A] says [X]; [Source B] says [Y]. [Source A] is more authoritative / more recent because [reason]. **Recommendation**: [Follow Source A / Check with [person] / Treat as unresolved].

---

## What the sources don't cover
- [Part of the question no available source covers]
- [Information that may exist but wasn't found in the connected sources]

---

## Source register

| # | Title | Type | Platform | Author | Date | Reliability | Link |
|---|-------|------|----------|--------|------|-------------|------|
| 1 | [Title] | [Type] | [Platform] | [Author] | [Date] | [Tier 1-4] | [Link] |
| 2 | ... | | | | | | |
```

## Ground rules

- Don't put anything in the answer that the sources don't contain. When no source covers a sub-question, write "[Not covered in available sources]".
- Don't settle conflicts behind the scenes. When sources contradict each other, the disagreement must be visible in the output.
- Don't pass off one source's claim as what the organization agrees on. Consensus takes multiple independent sources.
- Every claim in the Synthesized answer section needs an inline citation, and the confidence rating must reflect how good the sources really are — not how smoothly the narrative reads.
