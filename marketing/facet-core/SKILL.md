---
name: facet-core
description: Verify whether a single company's core promise holds within the scope it actually governs; when it does not, trace where it changes, weakens, disappears, or conflicts across brand, marketing, product, UX, policy, support, outcomes, and independent evidence, then present only the best-supported causal hypothesis. Use for message-integrity audits and desk research that tests whether a promise is product-backed or messaging-heavy. Do not use for company comparisons, rankings, vendor selection, or generic brand summaries.
---

# Facet Core

Facet Core is a verification-first message-integrity audit for one company. First decide whether the promise holds inside the scope it actually governs. Locate a break and explain its cause only when a material break survives that scope check.

## Required input

Accept:

- one company, organization, product, or service;
- one core promise, proposition, or priority claim when supplied;
- optional product, market, audience, geography, or time scope;
- or a problem symptom or business question, used to find the wording to audit.

If the user does not name a promise, identify the strongest explicit proposition in current first-party materials and state the selected wording before analysis. Establish centrality through intentional prominence or repetition on a current homepage, About or mission page, product proposition, investor material, or brand manifesto. Do not promote wording found only in legal boilerplate, a privacy policy, a footer, an archived campaign, or a third-party paraphrase into the company's core promise. Do not invent an implicit mission. If several propositions are equally central and choosing one would materially change the audit, ask the user which one to trace.

A request does not have to arrive as a company plus a promise. It may be a company name, exact wording, a page or ad or deck, or only a symptom. Read `references/entry-points.md` for how each one starts, and for the rule that a user's description of a symptom is never promoted into the company's promise.

For multiple companies, do not rank or synthesize them. Analyze one independently or route comparison requests to a comparison workflow.

## Non-negotiable rules

1. Observe surfaces independently before forming an overall judgment.
2. Treat a capability as evidence of capability, not automatically of outcome, priority, or organizational intent.
3. Compare the same claim dimension across surfaces.
4. Preserve `Unknown` when public evidence cannot support a relationship or cause.
5. Treat missing evidence as omission or uncertainty, not contradiction.
6. Keep product-, branch-, market-, and time-specific evidence at that scope.
7. Describe the structural pattern before explaining it.
8. Generate competing explanations before selecting a likely cause, but only when a material break survives verification.
9. Let evidence strength control the verb. Do not display confidence bands.
10. Keep the default output compact, but never remove the evidence-to-judgment bridge.
11. Include at least one concrete product moment that a reader can picture. Hide internal labels and calculations, not the observations needed to understand the verdict.
12. Show the message movement path in every default answer. If the promise holds, show the verified path to the achieved result. If it does not, name the exact connection where alignment first weakens, breaks, or becomes unobservable.
13. Open the change section with a problem diagnosis only when a material break survives. When the promise holds, open with an equally direct scope-limited verdict. Read `references/diagnosis.md`.
14. Name where the problem sits, never what to build. A location is not a prescription. When asked whether a claim can be used in advertising, sales, or a legal context, verify only how far the evidence supports it. Do not approve its use, propose replacement wording, or judge legal defensibility.
15. When naming a break, use the company's public names for its own functions. Do not assert how its teams relate, and do not name people. What public evidence may support is that two functions move separately in the finished product.
16. Symptoms are discovery queries, not promise contracts. When a request starts from a symptom, locate the company's strongest current first-party proposition, disclose the selected wording, and audit that. Never elevate the user's description into the company's promise.

## Workflow

### 0. Symptom gate

Run this only when the request arrives as a symptom or a business question rather than a company plus a promise.

1. Pull the company, product, market, and touchpoint out of the symptom.
2. Find the actual central wording in current first-party material.
3. State the selected wording and why it was selected, in one or two sentences.
4. Audit that wording only.
5. If no wording in the reviewed materials governs the symptom, leave it `Unknown` and say so. Absence in the reviewed materials is not absence of a promise. Do not treat the symptom itself as the promise.

Read `references/entry-points.md`.

### 1. Define the promise contract

Quote or closely preserve the company's wording and cite the first-party surface where the company intentionally presents it as a proposition. Verify that the wording is current for the audited period. When the user supplies wording you cannot immediately locate, read `references/evidence-protocol.md` and search again from another angle before calling it unverifiable. A failed search is not evidence that the wording was never said. Atomize the promise into the dimensions that determine whether it holds:

- capability
- scope
- effort
- time
- cost
- condition
- outcome
- priority
- audience
- category
- differentiation

Before testing downstream surfaces, state the promise boundary internally: what the wording governed, which audience and period it addressed, and which adjacent surfaces it did not claim to govern. A design brief governs design surfaces. A product launch claim governs that launch. Evidence outside this boundary may reveal another useful question, but it cannot lower the verdict on the audited promise.

For a priority claim, also inspect default behavior, friction, architecture, trade-offs, and what happens when the stated priority conflicts with growth, engagement, cost, or speed.

When the promise is about protection, safety, or a priority and the company offers a feature as evidence, run the checks in `references/capability-to-protection.md`. A feature that exists is not a protection that happens.

When the wording names who the product is for, what kind of product it is, or how it differs from an alternative, read `references/positioning.md`. How search or AI systems classify the company is never evidence in a Core verdict.

### 2. Observe surfaces in parallel

Research relevant surfaces independently:

- Corporate / Brand
- Marketing / Sales
- Product / Service
- UX / Customer journey
- Docs / Policy / Support
- Outcomes / Cases
- Independent / Regulatory / Review evidence

Capture the claim, evidence, source, date, first-party or independent status, scope, and supported dimensions. Read `references/evidence-protocol.md` before evaluating material evidence.

### 3. Verify claim against evidence

For each material observation, ask:

- Does the evidence support the whole claim or only one dimension?
- Is a feature being mistaken for effectiveness?
- Is investment being mistaken for priority?
- Is a first-party description being mistaken for independent confirmation?
- Is the evidence current and scoped to the same product, market, or period?

Narrow the observation whenever the evidence is narrower than the claim.

### 4. Build the surface graph

Do not assume a linear funnel. Compare only meaningful edges inside the promise boundary, such as Promise ↔ Product, Marketing ↔ UX, Product ↔ Outcome, or Claim ↔ Independent evidence. Keep adjacent edges separate until another promise makes them relevant.

Read `references/relationship-rubric.md` and assign a relationship only after verification. A normal surface-specific simplification is not automatically divergence.

### 5. Locate the leak

Run the scope gate before locating a leak: does the wording actually govern the surface being judged? If not, remove that surface from the verdict. Never import an adjacent problem merely because the audited promise held.

When a material change remains inside scope, identify its earliest and deepest edge. Name the exact surface, mechanism, audience, geography, or stage—not a vague department.

Depth describes structural location, not moral severity:

- **Edge:** distribution, access, support, localization, or another boundary condition.
- **Deep:** core product architecture, default behavior, decision mechanism, or outcome mechanism that the promise claims to govern.

If no material divergence survives verification, say the promise holds within the reviewed scope and use the held branch in `references/diagnosis.md`. A promise that holds is a result, not a failed audit. An adjacent observation may appear only as a separate consideration, with no verdict, and never as evidence against the audited promise. If evidence cannot resolve an in-scope edge, use `Unknown`.

### 6. Attack competing hypotheses

For every material leak, generate at least two plausible explanations. Read `references/hypothesis-protocol.md`, then run support, contradiction, alternative-explanation, scope, and falsifiability tests.

Present one likely cause only when it explains the pattern better than its competitors. Otherwise list the surviving explanations in one compact sentence and state what evidence would separate them.

When the promise holds, do not generate failure hypotheses. Instead, show the two or three verification points that connect the original objective to the observed result.

### 7. Run the final verification loop

Before responding, confirm:

- the promise wording is traceable;
- every decisive observation has a current source;
- the named leak compares the same claim dimensions;
- `Compressed` and `Divergent` pass the materiality test;
- omission is not presented as contradiction;
- the likely cause does not exceed the observed pattern;
- a competing explanation has not been ignored;
- the language distinguishes observed fact from inference;
- the reader can move from promise to product observation to judgment without an unexplained leap;
- the message movement path either reaches the verified result or names the exact connection where alignment changes;
- at least one concrete product moment appears in plain language;
- internal terms such as surface graph, governing constraint, architecture edge, or relationship label are absent unless immediately explained;
- a break diagnosis names one category and one location, with no conditional clause;
- a held verdict contains no invented problem category or causal hypothesis;
- no out-of-scope observation has lowered the verdict, and every adjacent consideration is explicitly separated without a verdict;
- the named functions use the company's public wording, and no claim is made about its teams or people;
- no comparison, ranking, or prescription has leaked into the default output. A location is allowed; an instruction to build something is not.

## Output

Read `references/output-contract.md` and follow it exactly.

Default to the reader-facing contract:

1. a plain-language verdict title;
2. the message movement path;
3. what the company says;
4. what the product shows;
5. where it changes;
6. why it may be this way.

Answer in the language the user wrote in. The order above never changes; the labels are localized. `references/output-contract.md` carries the Korean and English label sets and the rule for other languages.

In the message movement path, show a one-line chain and a compact two-column table covering only the material in-scope connections, normally Marketing → Product → default UX → observed outcome or independent evidence. If the promise holds, end at the achieved result. Otherwise state where alignment changes. Describe relationships between surfaces; do not assign blame to departments or people.

Keep evidence links inline. Translate internal analysis into ordinary language. Do not expose internal relationship labels, confidence scores, methodology, generic company summaries, action plans, or a separate sources section by default.

When the user asks for proof, expand only the requested layer: evidence chain, surface graph, competing hypotheses, unknowns, or falsification conditions.

## Tone

- Simple but not thin: compact, plain, and sufficiently explained.
- Analytical without sounding prosecutorial.
- Use `may`, `appears`, or `is consistent with` for inferred causes.
- Prefer `Unknown` to an interesting but unsupported explanation.
