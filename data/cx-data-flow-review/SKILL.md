---
name: cx-data-flow-review
description: Use to map where support conversation data actually goes — systems, vendors, countries, AI providers — and compare it against what the privacy notice and records say. Trigger for "where does our support data go", "map our data flows", "which vendors process our conversations", cross-border transfer review, ROPA accuracy for support, or a new tool that was connected without a review.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Where support data actually goes

Every support operation has a documented set of data flows and a real one, and they
diverge. The documented set was written at a point in time; the real one grows every time
someone connects an integration, trials a tool, or adds an AI feature that was already in
the product they use.

The gap matters because the documented set is what the privacy notice, the processing
records and the transfer assessments are based on. **A processor nobody registered is a
processor nobody assessed.**

## Build the real map from the systems, not from the register

Start from where the data is, not from what the register claims:

- **The helpdesk's own integrations list.** Every connected app is a potential recipient.
  Check what each one can actually read — most integrations request broad scopes and use a
  fraction of them.
- **Marketplace and plugin installs**, including ones installed for a trial and never
  removed.
- **Outbound webhooks and API consumers.**
- **The AI features inside tools you already pay for.** Summarisation, sentiment, reply
  suggestions, ticket classification. **These are the most commonly unregistered flows**,
  because they arrive as a product update rather than as a procurement decision — often
  enabled by default.
- **Analytics and BI**, and where those tools are hosted.
- **Transcription and voice** vendors.
- **Survey tools**, which see the conversation context alongside the response.
- **Vendor and BPO systems**, and their own subcontractors.
- **Data exports and reporting pipelines** into a warehouse, plus anything reading from it.
- **Search and vector indexes**, and where the embedding was computed — an embedding
  computed by an external API means the content went to that API.
- **Screen sharing, co-browsing and session replay**, which can capture far more than a
  conversation.
- **Local copies** — spreadsheets, extracts, screenshots. Ungoverned and real.

For each: what data, which fields, why, where hosted, who the sub-processors are, what
retention applies, and whether it is in the register.

## The questions that find the gaps

- **What is connected that nobody uses?** Dormant integrations retain access. This is
  cheap to check and usually finds something.
- **What was enabled by default?** Product updates that switch on a new AI feature. Check
  release notes against your configuration, and check the setting rather than trusting the
  release note.
- **Who has API credentials?** Long-lived tokens issued for a project that ended.
- **What does the free tool do?** Free and freemium tools frequently have permissive terms
  about using your data.
- **Where is support-adjacent data going?** Contact details pushed to marketing tools,
  conversation summaries into a CRM, quality scores into an HR system.
- **What crosses a border?** Including support agents accessing data from another country,
  which is a transfer even with no system involved. **Follow-the-sun coverage is a transfer
  arrangement**, and it is rarely documented as one.
- **What does the AI provider do with it?** Retention, whether it is used for training,
  whether a zero-retention arrangement exists and is actually configured. The default terms
  and the negotiated terms differ, and only the configured one matters.

## Compare against the documented position

Three comparisons, and each finds a different class of problem:

1. **Against the processing register.** Flows present in reality and absent from the record.
2. **Against the privacy notice.** Recipient categories and purposes the notice does not
   cover. If the notice does not describe what happens, the notice is wrong — and that is a
   more serious finding than a register gap, because it is a statement to customers.
3. **Against the transfer assessments.** Cross-border flows with no assessment, or with one
   that predates a change in the arrangement.

Report each gap with what the data is, where it goes, and how long it has been happening —
because the duration bounds how many customers are affected.

## Cross-border specifics

- **Determine the actual location**, not the vendor's headquarters. Region configuration,
  failover regions, support access locations and sub-processor locations all matter, and a
  vendor with an EU region may still have global support staff who can access it.
- **Include remote access as a transfer**, including your own staff and contractors.
- **Check the sub-processor list** for onward transfers, and check when it was last updated —
  most vendors reserve the right to change it with notice, and nobody reads the notice.
- **Whether a given transfer has a valid basis is a legal determination.** Map precisely and
  route it.

## Making it stay accurate

A one-off map is stale within a quarter. The durable output is the mechanism:

- **A gate on new integrations**, so connecting a tool triggers a review rather than
  following one.
- **Periodic reconciliation** of connected apps and credentials against the register.
- **A watch on product updates** that enable new processing by default. This is the one
  nobody has, and it is where the next gap will come from.
- **A named owner** for the support data map.
- **An offboarding step** that removes access and confirms deletion when a tool is retired.

## Guardrails

- **Do not conclude whether a flow is lawful.** Purpose, lawful basis, transfer mechanism and
  notice adequacy are legal determinations. Map precisely; route clearly.
- **An unregistered flow involving special-category data** — health or vulnerability
  disclosures in conversation content — is higher priority than an ordinary gap. Flag it
  separately.
- **A flow to a jurisdiction or vendor with no assessment at all**, running at volume, is
  potentially a live incident rather than an audit finding. Escalate rather than schedule it.
- **Do not disable a live integration to test what it does.** You will break a production
  support workflow.
- **Do not extract data to demonstrate a flow exists.** Configuration evidence, scopes and
  logs are sufficient, and copying content creates another flow.
- **Restrict the map's distribution.** It is a complete description of where your customer
  data is, which is exactly what an attacker would want.

## Present results to the user

1. **The real map**, system by system: data, fields, purpose, hosting location,
   sub-processors, retention, and register status.
2. **Unregistered flows**, with duration, special-category ones first.
3. **Flows the privacy notice does not cover** — the more serious gap, because it is a
   statement to customers.
4. **Cross-border flows with no current assessment**, including remote access by staff and
   contractors.
5. **AI provider terms as actually configured** — retention and training use — rather than as
   negotiated or assumed.
6. **Dormant integrations and stale credentials**, as a removal list.
7. **Default-enabled processing** found by comparing product changes against configuration.
8. **The mechanism to keep it accurate** — gate, reconciliation cadence, product-update
   watch, owner, offboarding step.
9. **What needs a legal determination**, and anything to escalate now rather than schedule.
