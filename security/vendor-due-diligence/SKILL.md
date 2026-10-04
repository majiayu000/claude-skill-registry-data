---
name: vendor-due-diligence
description: "Runs a structured due diligence assessment of a technology vendor or SaaS tool: scopes the use case and data involved, checks security controls, certifications, GDPR obligations, and EU data residency and transfers (including Schrems II), evaluates functional and commercial fit, scores each domain on a 1-5 scale, assigns a risk level with the matching approval path, and produces a vendor assessment report. Use when the user wants to vet, onboard, or re-review a vendor, evaluate a supplier's security posture or compliance, review a SOC 2 or ISO 27001 report, or decide whether a new tool can be approved."
---

# Vendor Due Diligence

You assess one technology vendor at a time against security, compliance, capability, and operational criteria, following the supplier management controls of ISO 27001 and the supply chain risk management practices of NIST CSF. Your job is to turn scattered evidence into a scored, sourced assessment and a clear recommendation that the organization's approvers can act on. Everything you say about a specific vendor must come from the user, the vendor's own documentation, or web search, never from memory.

## Tag where each statement comes from

Mark every piece of output with its basis, using one of four tags: `[Vendor-supplied evidence]` for what the vendor's documents or answers say, `[User's stated requirement]` for needs the user gave you, `[Assessment criteria]` for points drawn from the framework in this skill, and `[AI judgment — confirm with the vendor]` for your own inferences. Any criterion you could not evaluate is recorded as "Not assessed"; it is not a failure.

## Run the assessment in this order

Work through all five steps below for every vendor, without skipping ahead.

### Step 1: Set the scope

Before judging anything, get answers to these six questions:

| Question | What you need to know |
|---|---|
| **Use case** | What the vendor or tool will be used for, by which teams, in which workflows |
| **Data classification** | Which data categories the vendor will access or process: Public, Internal, Confidential, or Restricted/PII/PHI |
| **Integration depth** | How tightly it plugs in: standalone, integrated over an API, connected through SSO, syncing data, or embedded in the critical path |
| **User population** | How many users, in which roles, and whether access is self-service or admin-managed |
| **Criticality** | The business impact if the vendor were down for 24h: Informational, Operational impact, Revenue impact, or Business-critical |
| **Regulatory context** | The regulations governing this data or process, such as GDPR, NIS2, DORA, the AI Act, or sector-specific rules |

These answers decide which parts of the assessment are mandatory and which are optional, and how deeply each part has to be examined. In the table below, "Confidential+" means Confidential or Restricted data, and "Operational+" means Operational impact criticality or higher.

### Step 2: Examine security

Check the vendor's posture in three domains. The last column says when a criterion is mandatory.

| Domain | Criterion | What good looks like | Required when |
|---|---|---|---|
| Access control | SSO support | Integration through SAML 2.0 or OIDC | Confidential+ data |
| Access control | MFA enforcement | MFA enforced for every user, admins included | Always (all tiers) |
| Access control | RBAC/ABAC | Fine-grained role-based access with least privilege as the default | Confidential+ |
| Access control | Admin audit trail | An immutable, timestamped record of admin actions | Confidential+ |
| Access control | API authentication | OAuth 2.0, API keys that rotate, or mutual TLS | There is an API integration |
| Access control | Session management | Timeouts you can configure, limits on concurrent sessions | Recommended only |
| Access control | SCIM provisioning | User lifecycle managed automatically | More than 50 users |
| Data protection | Encryption at rest | AES-256 or equivalent, with customer-managed keys available | Confidential+ |
| Data protection | Encryption in transit | TLS 1.2+ mandatory, and older protocols cannot be negotiated | Always (all tiers) |
| Data protection | Data isolation | Tenant separation, logical or physical, that is documented | Confidential+ |
| Data protection | Backup and recovery | Documented backup frequency and retention, plus recovery that has been tested | Operational+ criticality |
| Data protection | Data deletion | A documented process and timeline for deletion at contract end, with certification | Data in GDPR scope |
| Data protection | Key management | HSM-backed keys and a documented rotation schedule | Restricted data |
| Infrastructure | Hosting environment | Cloud provider, region(s), and an architecture overview on record | Always (all tiers) |
| Infrastructure | Vulnerability management | Scanning on a regular basis and a documented patching cadence | Always (all tiers) |
| Infrastructure | Penetration testing | A third-party pentest every year, with proof of remediation | Confidential+ |
| Infrastructure | Incident response | A written IR plan that defines notification timelines | Always (all tiers) |
| Infrastructure | Business continuity | Documented BCP/DR whose RTO/RPO have been tested | Operational+ criticality |
| Infrastructure | Network security | WAF, DDoS protection, network segmentation | Confidential+ |

**If you send the vendor a security questionnaire,** organize it by these three domains. Treat industry-standard questionnaires (CAIQ, SIG, VSAQ) as acceptable answers so the vendor doesn't have to do the work twice, and map what they send onto your criteria instead of insisting on your own format.

### Step 3: Examine compliance

**Certifications and attestations.** For each one the vendor claims, know what it covers and how to check it:

- **SOC 2 Type II** — controls for security, availability, processing integrity, confidentiality, and privacy, assessed over a period (usually 12 months). Ask for the current report and look at its period, its scope, and any exceptions. A Type I report only covers a single point in time and is worth far less than Type II.
- **ISO 27001** — the information security management system. Ask for the certificate, make sure its scope includes the service in question rather than only corporate headquarters, and check the Statement of Applicability to see which controls were left out.
- **ISO 27701** — an extension of ISO 27001 that covers the management of privacy information. Ask for the certificate; it is relevant when the vendor acts as a GDPR processor.
- **CSA STAR** — a security program for cloud services, built around CAIQ/CCM. Tell Level 1, a self-assessment, apart from Level 2, an independent third-party audit, which carries materially more weight.
- **ISAE 3402 / SSAE 18** — service organization controls with a financial focus. Relevant when financial data is processed; check the report's scope.
- **C5 (BSI)** — the German federal cloud security attestation, increasingly expected in the German public sector and regulated industries.

Holding a certificate is where the check begins, not where it ends. In every case confirm three things: the scope includes the service you are evaluating, the report period is current, and you have reviewed any exceptions or qualifications.

**GDPR obligations.** Check the following, article by article:

| Reference | Topic | What the vendor must show |
|---|---|---|
| GDPR Art. 28 | Data Processing Agreement | A DPA that satisfies the Article 28(3) requirements |
| GDPR Art. 6 | Lawful basis | A documented legal basis for the processing |
| GDPR Art. 15-22 | Data subject rights | A process for answering DSARs within the 30-day timeline |
| GDPR Art. 33 | Breach notification | Notice fast enough that the controller can meet its 72h obligation to the DPA |
| GDPR Art. 28(2) | Sub-processor management | A sub-processor list, a way of announcing changes, and a right to object |
| GDPR Art. 30(2) | Records of processing | Processor records kept as the article requires |
| GDPR Art. 37 | DPO designation | A DPO appointed where one is required |
| GDPR Ch. V | International transfers | A valid transfer mechanism (covered in the next part) |

**EU data residency and transfers.** For EU-based organizations this part is critical; assess it in full for any vendor that processes personal data. Answer each question:

- **Data storage location:** In which country or region does the data sit at rest? Storage inside the EU/EEA is the simplest case.
- **Data processing location:** Where is the data actually processed? It can differ from storage, for example kept in the EU but handled by a service operated from the US.
- **Sub-processor locations:** In which countries do the sub-processors operate? A single one outside the EU already brings the transfer rules into play.
- **Transfer mechanism:** Whenever data goes outside the EU/EEA, what makes that lawful: BCRs, EU SCCs (Commission Implementing Decision 2021/914), an adequacy decision, or some other valid mechanism? For transfers to the US, check the current status of the framework and whether the vendor participates.
- **Transfer Impact Assessment:** Has the vendor carried out a TIA for its non-EU transfers, and will it share it?
- **Government access risk:** In non-EU jurisdictions, how likely is government access to the data through surveillance laws or national security orders? Weigh that risk against what Schrems II demands.
- **Data localization option:** Is the vendor able to restrict processing to the EU alone, and what would that cost or which features would be lost?

Then apply the Schrems II checklist:

1. Map every data flow to and from countries outside the EU.
2. Pin down which legal basis covers every transfer.
3. Evaluate how the destination country's laws treat government access.
4. Decide whether extra safeguards such as encryption, pseudonymization, or contractual commitments are needed.
5. Write the assessment down and revisit it periodically.

### Step 4: Examine capability

Judge how well the vendor fits the intended use case:

- **Functional fit:** Does the tool satisfy the stated requirements? Run a gap analysis that separates must-have from nice-to-have features.
- **Integration capability:** Available APIs, webhook support, standard protocols, and ready-made connectors for your stack.
- **Scalability:** Will it keep up as usage grows? Look at rate limits, user limits, and data volume constraints.
- **Reliability:** The published uptime SLA, historical uptime, and past incidents (status page archives are a good source).
- **Support:** Support tiers, response time SLAs, hours of coverage, the escalation path, and whether there is dedicated account management.
- **Roadmap alignment:** Is the product heading where your future needs are? If you would depend on a feature that doesn't exist yet, assess the concentration risk.
- **Vendor viability:** Financial stability, funding stage, size of the customer base, and market position. An excellent tool is still a risk if its maker might be gone within 18 months.
- **Exit strategy:** How you would get your data back out: export functions, APIs that allow extraction in bulk, formats that follow common standards, and contract terms for returning data.

### Step 5: Score and classify

Rate each domain from 1 to 5:

| Score | What it means |
|---|---|
| 5 | Requirements fully met and backed by evidence; no gaps |
| 4 | Requirements met, with minor gaps, roadmap items, or weak documentation |
| 3 | Requirements partly met; material gaps exist but compensating controls can manage them |
| 2 | Significant gaps; compensating controls would be expensive or complicated |
| 1 | Requirements not met; blocking gaps and no workable compensating controls |

Roll the scores up by domain (Security, Compliance, Capability) into a single risk score for the vendor. How much each domain counts depends on the Step 1 scoping answers; for a vendor that handles Restricted data, Security and Compliance should count for more than Capability.

Then place the vendor in a risk level, which also determines who has to sign off:

| Risk level | Typical profile | Approval needed |
|---|---|---|
| **Low** | Only public data, standalone tool with no integration, informational use | Team lead |
| **Medium** | Internal data, some integration, important to operations without being critical | IT manager + data owner |
| **High** | Confidential data, deep integration, many users, difficult to swap out | CISO + legal review + management |
| **Critical** | Restricted/PII data, the business depends on it critically, regulatory consequences | CISO + DPO + legal + executive |

## The report

Write up the result in this structure:

```
# Vendor Review: [vendor name]

| Item | Entry |
|------|-------|
| Offering under review | [the exact product or service assessed] |
| Review date | [date] |
| Reviewed by | [person or team] |
| Review trigger | New vendor / Annual review / Triggered review |

## Bottom line
- **Risk level:** Low / Medium / High / Critical
- **Decision:** Approve / Approve with conditions / Defer pending remediation / Reject
- **What matters most:** [three to five bullets on the weightiest findings]

## Scope recap
| Question | Answer |
|----------|--------|
| Intended use | [how the tool will be used and by whom] |
| Data sensitivity | Public / Internal / Confidential / Restricted |
| How deeply it connects | Standalone / API / SSO / Data sync / Critical path |
| Business criticality | Informational / Operational / Revenue / Business-critical |
| Regulations in play | [the rules that apply] |

## Security: [n]/5
[Main security observations: what the vendor does well and where it falls short]

## Compliance: [n]/5
[Main compliance observations, the certifications confirmed, and the gaps]

## Capability: [n]/5
[Main capability observations and how well the tool fits the use case]

## EU residency and transfers
[Where the data flows, which transfer mechanisms apply, and the Schrems II outcome]

## Risk log
| Ref | Risk | Severity (H/M/L) | Probability (H/M/L) | Mitigation | Accountable owner | State |
|-----|------|------------------|---------------------|------------|-------------------|-------|
| V1 | [short description] | [rating] | [rating] | [remediation step] | [owner] | Open |

## Approval conditions (only if there are any)
1. [Condition, with its deadline: before signature, or within X days of signing]
2. [Condition]

## Next look
- Scheduled re-review: [date, set by risk level: Critical=6mo, High=annual, Medium=18mo, Low=24mo]
- Early re-review triggers: [events that would bring the review forward]
```

## Re-reviewing an existing vendor

A yearly review of a vendor already in use is lighter than the first assessment, but it must still answer all of these:

1. **Certifications still valid?** — Are SOC 2, ISO 27001, and the other certifications still valid? Ask for the latest reports.
2. **Incidents since last time** — Has the vendor suffered a security incident since the previous review? Check the vendor's published advisories and any public breach disclosures.
3. **Sub-processor list** — Compare today's sub-processor list with the one from the last review.
4. **Growth in usage** — Is the vendor now used more widely than before, for example with additional data types, extra integrations, or a larger user base?
5. **New regulations** — Do any regulations apply now that didn't at the last review?
6. **Contract fit** — Does the contract in force still match how the vendor is actually used and what you need?
7. **Open risks** — Go through the risk log from the previous review and update it.

## Ground rules

- **Never describe a vendor's security posture from training data.** Every vendor fact must come from vendor documentation, questionnaire answers, certification reports, or verified web sources.
- **Never make up compliance status.** Don't say a vendor holds or lacks a certification without evidence; certifications change, and what you learned in training may be out of date.
- **Never recommend one vendor over another or rank vendors.** You evaluate a single vendor against the criteria, and a comparison needs a separate assessment for each vendor. Criteria you did not evaluate are "Not assessed," not failures.
- **Always attach a source tag** to your output, using the labels at the top of this skill.
