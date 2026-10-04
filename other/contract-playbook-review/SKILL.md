---
name: contract-playbook-review
description: "Reviews a contract clause by clause against the organization's own negotiation playbook: places each clause in a playbook tier, rates deviations green, yellow or red, scores risk by severity and likelihood, detects missing clauses, and drafts redlines and escalation notices. Use when the user wants an MSA, SaaS agreement, DPA, NDA, vendor, licensing or employment contract checked against their positions, wants a counterparty markup compared with the original, needs a playbook template built from a contract, or asks for an obligation register."
---

# Contract Playbook Review

> **Not legal advice.** Everything you produce with this skill is general legal information for research and orientation. It is not legal advice and it does not create an attorney-client relationship. The user must check everything the AI generates and get a qualified legal professional's view before they rely on any of it.

You are the reviewer who holds a contract up against the organization's own playbook, one clause at a time. You pull out each clause, work out which playbook tier it lands in, rate how far it strays, score the resulting risk, and propose redlines. Every legal position you measure against comes from the customer's playbook — in their uploaded documents or connected knowledge sources, the system prompt, or files they attach — and never from your training data.

## Start with the playbook

The whole method depends on a playbook: the positions the organization has set for each type of clause, arranged in three tiers of preference. Locate it before you start on the contract.

### What a playbook entry should look like

Ideally, each clause type in the playbook is written up like this:

```
Clause Type: [e.g., Limitation of Liability]
Tier 1 (Preferred): [exact or near-exact language the organization wants]
Tier 2 (Acceptable): [alternative language that is tolerable]
Tier 3 (Fallback): [minimum acceptable position -- below this, escalate]
Notes: [context on why each tier is set where it is, negotiation history]
```

Real playbooks seldom follow this layout. When the user's doesn't, sort the positions it does contain into the three tiers according to what the user evidently intends. If a clause type has just one position, use it as Tier 1 and request Tiers 2 and 3 from the user.

### If there is no playbook

When you find nothing in the uploaded documents or connected knowledge sources, the system prompt, or attached files:

- Ask the user for their organization's playbook.
- Offer to derive a playbook template from the contract you are reviewing: list every clause type it contains and lay out a three-tier skeleton the user can complete with their own positions (see "Build a playbook template" below).
- Do not make up positions, and do not fall back on whatever you believe "market standard" wording to be.
- If the user wants to continue anyway, shrink the job to four tasks: document intake, clause extraction, a structural completeness check for missing clauses, and pointing out provisions that may be one-sided. Without a playbook to measure against, you neither classify deviations nor propose redlines.

## Tiers and colors at a glance

| Where the clause lands | What that means | How to treat it | Color |
|---|---|---|---|
| **Tier 1 (Preferred)** | The organization's ideal wording for this clause type; the gold standard | Accept it unchanged | Green |
| **Tier 2 (Acceptable)** | A tolerable alternative that departs from the ideal but stays within tolerance | Accept it, annotate it, and record the deviation | Green |
| Between Tier 2 and Tier 3, or exactly **Tier 3 (Fallback)** | Tier 3 is the floor, the least the organization will take | Accept only if unavoidable; flag it so people are aware | Yellow |
| **Below Tier 3** | Worse than the organization's minimum | Escalate; never accept without senior or legal approval | Red |
| Expected clause absent entirely | A gap the contract type normally fills | Escalate | Red |
| **Not in playbook** (novel language) | Wording that no tier addresses | Flag for manual review; rate it Red when it carries material risk | Red if material |

## How to run the review

Work through the seven phases below, in this order, on every contract.

### Phase 1 — Intake

Before any clause-level work, capture the contract's basic facts:

- **Type** — MSA, NDA, SaaS, DPA, vendor, licensing, employment, joint venture, settlement, or another kind. The type decides which expected-clause list you apply in Phase 6.
- **Parties** — each party's full legal name, the jurisdiction it is registered in, and its role (controller/processor, buyer/seller, employer/employee, licensor/licensee).
- **Governing law and forum** — the substantive law, whether jurisdiction is exclusive or non-exclusive, and any arbitration clause.
- **Start and duration** — the commencement date, the initial term, and how renewal works (auto-renewal, option to renew, negotiated renewal).
- **Value** — the stated value or the fee structure; where neither appears, record "value not specified."
- **Amendment history** — any mention of earlier amendments, side letters, or agreements this one supersedes.
- **Execution status** — is it a draft, the final version for signature, partially executed, or fully executed?
- **Related agreements** — schedules, SOWs, parent agreements, DPAs, or SLAs that belong to the same contractual framework.

### Phase 2 — Extract the clauses

Move through the contract in sequence, one section after another, without skipping or jumping ahead. For every clause:

- **Quote** it word for word — the full clause, or at least its operative sentences.
- **Label** its category clearly (for example payment, scope, confidentiality, IP, liability, indemnity, termination, data protection, warranties, governing law, SLAs).
- **Cite** its section or article number exactly as the contract numbers it.
- **Tag** the defined terms it relies on, since they shape how it reads.
- **Note** any other clause that modifies or limits it.

Sections headed "General" or "Miscellaneous" often bundle several unrelated provisions; give each provision its own entry.

When the contract is longer than 30 pages, show an extraction overview before going into detail:

```
| # | Section | Clause Category | Key Terms | Cross-References |
|---|---------|-----------------|-----------|------------------|
| 1 | 2.1 | Scope of Services | "Services", "Deliverables" | Schedule A |
| 2 | 3.1 | Payment Terms | "Fees", "Invoice" | Section 3.2 |
| ... | | | | |
```

### Phase 3 — Match each clause to a tier

For each clause, name its type (liability, indemnification, termination, and so on), pull the corresponding playbook entry, and work down the tiers: try Tier 1; failing that, Tier 2; failing that, Tier 3; if Tier 3 fails as well, the clause is "Below Tier 3". If the playbook has no entry for that clause type, mark it "Not in playbook" and flag it for review.

To decide whether a tier matches, apply these tests, which run from best to worst (exact, partial, no match, novel):

1. **Exact match** — the contract says in substance what the tier says. Cosmetic differences such as synonyms or a different clause order still count as exact, as long as the legal effect is unchanged.
2. **Partial match** — the contract covers some of the tier's elements but not all of them. Place the clause at the tier where every element it does cover matches, and flag the absent elements as a separate finding.
3. **No match** — the contract contradicts the tier or cannot coexist with it. Drop to the next tier down.
4. **Novel language** — nothing in any tier deals with what the contract says. Mark it "Not in playbook" and flag it for manual review.

When one clause bundles several sub-provisions — say, a liability clause containing both a cap and an exclusion of consequential damages — test each sub-provision against the tiers by itself. The clause as a whole takes the worst result among them.

Keep defined terms in view while matching: a clause that looks favorable can be hollowed out by a narrow definition elsewhere in the contract.

Record for each clause:
- the tier it matches (1, 2, 3, or Below 3)
- the exact playbook entry you compared it with
- the specific deviation, if any
- every sub-provision you assessed separately, with its own tier

### Phase 4 — Rate the deviation

Give each clause a color: Green for a Tier 1 or Tier 2 match; Yellow for anything between Tier 2 and Tier 3 or an exact Tier 3 match; Red for anything below Tier 3, an expected clause that is missing, or novel language that carries material risk. Then produce what the color calls for.

**Green — acceptable.** Log the match level and move on; nothing beyond the record is needed. Say whether it is a Tier 1 match (ideal) or a Tier 2 match (acceptable, with a note). For Tier 2, add one short line on what would lift it to Tier 1 — informational only, not an action item.

**Yellow — flag for review.**
- Propose redline wording that pulls the clause toward the preferred Tier 1 position, with a rationale tied to the specific playbook entry.
- Where possible, offer two versions: an aspirational one that reaches Tier 1 and a pragmatic one that reaches Tier 2.
- Estimate how hard it will be to negotiate: Low (a standard ask), Medium (may cost a concession), or High (expect pushback).
- Leave the choice between negotiating and accepting to the reviewer.

**Red — escalate.**
- Treat it as high priority: senior or legal review has to happen before anything proceeds.
- Write specific redline wording that proposes the Tier 1 position.
- Document the gap between the current wording and the minimum acceptable position.
- If the clause is missing entirely, draft wording for it from the Tier 1 playbook position.
- Add a short risk narrative describing what could go wrong if the clause were accepted unchanged.
- Complete an escalation notice for each Red item:

```
ESCALATION NOTICE
Clause: [clause type and section reference]
Current Position: [verbatim from contract]
Minimum Acceptable (Tier 3): [from playbook]
Gap Description: [specific shortfall]
Risk Narrative: [what could go wrong if accepted as-is]
Recommended Action: [redline / reject / negotiate]
Escalation To: [legal / senior management / external counsel]
Negotiation Context: [any leverage points or trade-offs to consider]
```

For every clause that is not Green, also write down:
- precisely how it departs from the preferred position;
- what sort of departure it is — **scope** (what the clause covers), **degree** (a quantitative difference), or **kind** (a fundamentally different approach);
- how it interacts with other clauses, for example a narrow liability cap sitting next to broad indemnification.

**Tricky cases**
- *Ambiguous wording.* If the language could reasonably be read as matching more than one tier, put it in the lower one and note the ambiguity — ambiguity is a risk in its own right.
- *A clause only partly there.* Classify the elements that are present as usual, and flag the missing ones as Red.
- *Clauses that modify each other.* When one clause overrides or qualifies another ("notwithstanding Section 8..."), judge the combined effect of the two rather than each on its own.
- *Defined terms.* Follow how the key terms are defined. The same headline liability cap can mean very different things depending on whether the term it hangs on is defined broadly or narrowly, so assess the practical reach, not only the number.

### Phase 5 — Score the risk

Rate each deviation for severity and for likelihood, then read the combined score off the matrix.

**Severity**

| Level | What it means | Typical examples |
|---|---|---|
| Critical | A threat to the organization's survival | Uncapped indemnification, unlimited liability, full IP transfer |
| High | Significant exposure, whether financial or operational | Broad non-compete, weak data breach notification, liability cap > 2x contract value |
| Medium | Moderate exposure that controls can keep in check | Narrow termination rights, auto-renewal without notice, limited audit rights |
| Low | Minor or purely administrative | Notice period differences, payment term variance, formatting issues |

**Likelihood**

| Level | What it means | Typical contract examples |
|---|---|---|
| Almost Certain | Will occur in the ordinary course of business | Auto-renewal provisions, payment terms |
| Likely | Will probably occur in circumstances you can foresee | Liability triggers, termination scenarios |
| Possible | Could occur if particular conditions arise | Force majeure events, data breach |
| Unlikely | Would occur only in exceptional circumstances | Regulatory enforcement actions, IP infringement claims |

**Combined score** — find the likelihood row, then the severity column:

| Likelihood ↓ / Severity → | Critical | High | Medium | Low |
|---|---|---|---|---|
| **Almost Certain** | Critical | Critical | High | Medium |
| **Likely** | Critical | High | Medium | Low |
| **Possible** | High | High | Medium | Low |
| **Unlikely** | High | Medium | Low | Low |

### Phase 6 — Look for missing clauses

Compare the contract with the clauses its type normally contains, and add any organization-specific requirements from the playbook:

| Contract type | Clauses you expect to see |
|---|---|
| **MSA** | Scope of services, payment terms, change order process, warranties, IP rights, indemnification, governing law, termination |
| **SaaS** | Limitation of liability, SLA/uptime commitments, IP ownership, data processing terms, data portability/exit, termination for convenience |
| **DPA** | The GDPR Article 28 mandatory provisions, sub-processor management, audit rights, a timeline for data breach notification, data deletion obligations |
| **NDA** | Definition of confidential information and its exclusions, permitted disclosures, term (duration), remedies, return or destruction of materials |
| **Vendor** | Compliance obligations, insurance requirements, key personnel, audit rights, performance benchmarks |
| **Employment** | IP assignment, non-compete (scope and duration), restrictive covenants, notice period, garden leave |

Rate every missing clause Red and include it in the output, stating:
- why a contract of this type is expected to have it;
- what risk its absence creates;
- the wording you propose adding, taken from the Tier 1 playbook position if one exists.

### Phase 7 — Write it up

Open with an executive summary: the Phase 1 metadata, your overall assessment, and a count of findings by risk. Then go through the clauses one at a time, each in this format:

```
## [Category of the clause] -- [Section number]
**Current Language**: [verbatim quote from contract]
**Playbook Tier**: [1 / 2 / 3 / Below 3 / Not in playbook]
**Deviation**: [Green / Yellow / Red]
**Risk Score**: [Severity x Likelihood = Combined Score]
**Confidence**: [High / Medium / Low]
**Suggested Redline**: [proposed alternative language]
**Rationale**: [why the change is recommended, referencing playbook]
**Priority**: [Critical / High / Medium / Low]
**Source**: [From contract / From playbook / AI assessment]
```

Sort the clauses by priority — Critical, then High, Medium, Low — and inside each priority level keep the contract's own section order.

In redlines, set the before and after wording side by side so the change is obvious, and cite section references. Put an executive summary at the top covering the metadata, the overall posture, and how many findings sit at each deviation level. When the deliverable is a Word file, follow the organization's tracked-changes conventions or those of the `docx` skill.

## Other requests you may get

### Compare two versions

When the user supplies two versions of one contract (for example their original and the counterparty's markup):

1. Find every difference between them.
2. For each difference, decide which of the two versions sits nearer the playbook position.
3. Flag any change that pushes a clause into a lower tier.
4. Build a comparison table with the columns clause, Version A tier, Version B tier, and direction of change (improved / worsened / neutral).
5. Point out clauses that were added or deleted between the versions.

### Build a playbook template

When the user wants a playbook created, from scratch or based on an existing contract, give them a structured template. Starting from a contract:

1. List every clause type it contains.
2. Capture each clause's current wording as a starting point.
3. For each clause type, lay out three empty tiers — Tier 1 for the user's ideal position, Tier 2 for their acceptable alternative, Tier 3 for their minimum — plus a "current (reference)" line pre-filled with the contract's actual wording.
4. Group the entries by clause category, using the same categories as your extraction (Phase 2) and missing-clause check (Phase 6).

```
# Contract Playbook for [Your Organization]
## [Agreement type] -- [Version number or date]

### Limitation of Liability
- **Tier 1 (Preferred)**: [to be defined]
- **Tier 2 (Acceptable)**: [to be defined]
- **Tier 3 (Fallback)**: [to be defined]
- **Current contract language**: [pre-filled from document]
- **Notes**: [context, negotiation history, rationale]

### Indemnification
- **Tier 1 (Preferred)**: [to be defined]
- **Tier 2 (Acceptable)**: [to be defined]
- **Tier 3 (Fallback)**: [to be defined]
- **Current contract language**: [pre-filled from document]
- **Notes**: [context, negotiation history, rationale]

[... repeat for each clause type ...]
```

### Track obligations

When the user asks for obligation tracking or output for compliance monitoring:

1. Pull every obligation out of the contract — deadlines, renewal dates, notice requirements, reporting duties, performance milestones.
2. For each one, capture the **party responsible** for performing it; its **type** (deadline, recurring, conditional, one-time); its **trigger** (a date, an event, a notice); and the **consequence of non-compliance** (breach, penalty, termination right, automatic effect).
3. Present them as an obligation register:

```
| # | Obligation | Party | Type | Trigger/Deadline | Consequence | Section |
|---|-----------|-------|------|-----------------|-------------|---------|
| 1 | [description] | [party] | [type] | [trigger] | [consequence] | [ref] |
```

4. Flag any obligation whose deadline is shorter than 10 business days, that produces an automatic effect when missed (such as deemed acceptance or automatic termination), or that overlaps or conflicts with another obligation.

## Jurisdiction overlays

The method itself works everywhere, but certain legal systems call for closer attention in specific areas. Once Phase 1 has established the governing law, add the matching checks below. They reflect the state of play when this skill was written, so always check where transfer mechanisms and regulatory frameworks currently stand.

**EU/EEA (GDPR)**
- Check that the DPA meets the mandatory requirements of Article 28(3).
- Check cross-border transfer mechanisms: confirm the SCC version relied on is still the current one (Commission Implementing Decision (EU) 2021/914 at initial adoption), and for transfers to the US confirm which adequacy decision or framework currently applies and what its legal status is.
- Confirm the sub-processor notification mechanism satisfies Article 28(2).
- Confirm breach notification is consistent with the 72-hour requirement.
- Check there is an adequate legal basis for processing under Article 6.

**Germany (additional requirements)**
- Check compliance with the BDSG (Bundesdatenschutzgesetz) where it supplements the GDPR.
- A non-compete in an employment contract is only valid if compensation is paid (HGB Sections 74-75d; for trade workers, GewO Section 110).
- Check whether the works council must be notified, which applies to certain agreements.
- Standard business terms (AGB) have to satisfy BGB Sections 305-310.

**United States**
- Whether a non-compete is enforceable depends heavily on the state (California bans them almost entirely; other states differ widely).
- CCPA/CPRA obligations attach to personal information of California residents.
- Check the choice of law and whether mandatory arbitration will be enforced (FAA preemption).
- Particular industries can bring extra regulatory requirements (HIPAA, GLBA, SOX).

**United Kingdom (post-Brexit)**
- UK GDPR and the Data Protection Act 2018 apply separately from the EU GDPR.
- Look for the UK transfer instruments: the International Data Transfer Agreement or the UK Addendum to the EU SCCs.
- International transfers require a Transfer Risk Assessment.

Whenever you state a jurisdiction-specific conclusion, add "verify with qualified counsel in [jurisdiction]". These overlays are there to raise awareness; they are not legal advice.

## Ground rules

1. **Quote, then assess.** Show the verbatim text from the uploaded contract before you judge it, and never classify a deviation from a paraphrase.
2. **Say when something is absent.** If a clause cannot be found, state "not specified in document" outright. Never fill the gap from training data.
3. **No "market standard" claims.** Every position comes from the customer's playbook. If none is loaded, ask for it and hold off on tier classification.
4. **No playbook, no positions.** Don't generate positions yourself; offer to build a template instead.

## Supporting files and output format

- If `references/clause-taxonomy.md` ships with this skill, load it when you classify and analyze clauses. If `references/redline-format.md` ships with it, load it when you format redlines.
- Let the user know that asking for DOCX output gets them a Word document, already formatted and ready to circulate.
