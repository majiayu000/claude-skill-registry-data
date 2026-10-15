---
name: vendor-evaluator
description: "Runs a structured comparison of several vendors, products, or service providers for a purchase decision: turns the business need into weighted must-have and nice-to-have criteria, gathers evidence per vendor from proposals, demos, references, and pricing, scores each vendor on the same scale, compares total cost of ownership, tests how sensitive the ranking is to the weights, and produces a selection recommendation with open risks. Use when the user is choosing between vendors, tools, agencies, or suppliers, building a shortlist, scoring RFP responses, or needs a vendor comparison matrix or selection memo."
---

# Vendor Evaluator

You help the user choose between several vendors in a way that is fair, traceable, and defensible to a buying committee. You turn the need into weighted criteria before looking at any vendor, score every vendor against the same criteria with evidence, and show how robust the result is. Evidence comes from the user's documents and notes; you never fill gaps with what you think you know about a vendor.

This skill compares vendors. For the security, privacy, and compliance review of a single vendor (certifications, GDPR, EU data residency, risk level and approval path), use the **Vendor Due Diligence** skill on each finalist. The two work well together: run this skill to pick finalists, then due diligence on them, then return here for the final decision.

## Where the evidence comes from

| Source | Examples |
|---|---|
| Uploaded documents | RFP responses, proposals, price sheets, contracts, demo notes, reference call notes, analyst reports the user has licensed |
| Connected tools and sources | Procurement records, previous evaluations, internal wiki, CRM notes, support tickets with current vendor |
| The user and stakeholders | Requirements, priorities, budget, constraints, impressions from demos |

Note the source and date for each piece of evidence. Vendor marketing claims count as claims, not proof: mark them as such.

## Step 1 — Frame the decision

Establish before any scoring:

- **The need:** the business problem in one or two sentences, and what success looks like in 12 months.
- **Scope:** users, volumes, sites, integrations, languages, and the contract term being considered.
- **Budget and timing:** budget range, decision date, go-live date.
- **Decision makers:** who decides, who must be consulted (IT, security, works council, procurement, legal).
- **The long list:** which vendors are in scope, and whether "keep the current solution" or "build in-house" is an option. Including the status quo keeps the comparison honest.

## Step 2 — Set the criteria and weights first

Define criteria **before** looking at vendor material, so the vendors don't shape the yardstick.

1. **Must-haves (knock-out criteria):** requirements a vendor must meet to stay in the race, each phrased so it can be answered yes or no ("Hosting in the EU", "SSO via SAML or OIDC", "German-language support").
2. **Weighted criteria:** everything that distinguishes acceptable vendors. Group them and give weights that add up to 100%.

A typical starting point the user should adjust:

| Group | Example criteria | Typical weight |
|---|---|---|
| Functional fit | Coverage of key use cases, usability, configurability | 30–40% |
| Technical fit | Integrations, APIs, performance, scalability, admin effort | 15–20% |
| Cost | Total cost of ownership over the contract term | 15–25% |
| Vendor strength | Financial stability, roadmap, references in the industry, local presence | 10–15% |
| Service and support | SLA, support hours and language, onboarding, customer success | 10% |
| Risk and compliance | Result from Vendor Due Diligence, contract terms, exit options | 10% |

Agree the weights with the user and write them down. If stakeholders disagree on weights, record both sets; Step 6 will show whether it matters.

## Step 3 — Apply the must-haves

Check each vendor against each must-have:

```
| Must-have | Vendor A | Vendor B | Vendor C |
|---|---|---|---|
| [requirement] | ✅ [evidence] | ❌ [evidence] | ❓ unclear — ask vendor |
```

- A ❌ removes the vendor, unless the user decides to relax the requirement (record that decision).
- A ❓ becomes a question for the vendor. Do not score a vendor with open knock-out questions as if it passed.

## Step 4 — Score the remaining vendors

Score every criterion on the same scale:

| Score | Meaning |
|---|---|
| 5 | Exceeds the requirement, with proof (demo, reference, contract term) |
| 4 | Fully meets it, with proof |
| 3 | Meets it, based on vendor claims only, or with minor gaps |
| 2 | Partly meets it; workaround or extra cost needed |
| 1 | Does not meet it |
| — | Not assessed (missing evidence; never treat as 0 without telling the user) |

Build the matrix:

```
| Criterion | Weight | Vendor A | Vendor B | Vendor C |
|---|---|---|---|---|
| [criterion] | [w%] | [score] — [evidence, source] | ... | ... |
| **Weighted total** | 100% | [x.xx] | [x.xx] | [x.xx] |
```

Weighted total = Σ (score × weight). Show the calculation so it can be checked.

## Step 5 — Compare total cost of ownership

Compare cost over the full contract term (typically 3 years), not just license prices:

| Cost item | Vendor A | Vendor B | Vendor C |
|---|---|---|---|
| Licenses or subscription | | | |
| Implementation and integration | | | |
| Internal effort (FTE × rate) | | | |
| Training and change management | | | |
| Hosting and infrastructure | | | |
| Support and maintenance | | | |
| Exit and migration costs | | | |
| **Total over [n] years** | | | |

Mark estimates as estimates, and note price assumptions (user counts, growth, discounts, price escalation clauses).

## Step 6 — Test the result

A ranking is only useful if it holds up:

- **Sensitivity:** recalculate with the alternative weights from Step 2, and with each group's weight ±10 points. Does the winner change?
- **Margin:** if the top two are within about 0.3 points, call it a tie on the numbers and say the decision rests on the qualitative factors.
- **Evidence quality:** count how many of the winner's scores rest on claims only (score 3 based on claims). A win built on claims needs verification first.

## Step 7 — Write the selection memo

```
# Vendor selection: [category] — recommendation
Prepared [date] for [decision makers]

## Recommendation
[Vendor] — [one-sentence reason]. Confidence: [high / medium / low] because [reason].

## The decision in numbers
| Vendor | Must-haves | Weighted score | TCO ([n] years) |
|---|---|---|---|

## Why [winner]
- [top 3 reasons, each tied to a criterion and evidence]

## What we give up
- [where the winner is weaker than an alternative]

## Open risks and conditions
- [risk / open question] — [how to resolve before signing, owner, date]

## Sensitivity
[Does the result hold under alternative weights? Which assumption would flip it?]

## Next steps
1. [e.g. Vendor Due Diligence on the winner]
2. [e.g. negotiate exit clause, run reference call]
3. [decision date]
```

## Combining with other skills

- **Vendor Due Diligence** supplies the risk and compliance score for each finalist.
- **Contract Playbook Review** helps with the contract terms of the winner; the **RFP Assistant** app helps write the questions to vendors.
- **Perspective Panel** can stress-test the recommendation from the viewpoint of IT, finance, users, and procurement.

## Ground rules

- Use only evidence from the user's material, stakeholders, and connected sources. Never score a vendor from your general knowledge about it; mark gaps as "Not assessed".
- Treat every vendor the same way: same criteria, same scale, same evidence standard.
- Set criteria and weights before reviewing vendor material, and record any later change with its reason.
- The recommendation supports a decision; it doesn't make it. Purchasing decisions and contract terms need review by the responsible people (procurement, legal, IT security).
- Mark what comes from where: `[Vendor document]`, `[Reference call]`, `[Per the user]`, `[Vendor claim — unverified]`, `[My estimate]`, and `[Input required]`.
