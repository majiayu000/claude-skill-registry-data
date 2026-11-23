---
name: prioritize-opportunities
description: Identify and rank the customer outcomes or problematic situations in the selected targets that the venture should address first, keeping evidence strength separate from attractiveness and naming the uncertainty that could change the order. Use after targets are chosen, when customer evidence changes, or when Product or the business model needs to know which problem to serve. Writes the opportunities document.
---

# prioritize-opportunities

**Transformation:** customer-knowledge × target-segments × objectives and delivery context → [opportunities](../../../../.group/contracts/opportunities.md).

The document follows its contract and the group's [document rules](../../../../.group/contracts/document-rules.md).

## When to use

- Initial direction, after targets are selected.
- New customer evidence: interviews, support requests, lost deals, usage observations.
- A consumer (Product requirements, design-offers, prioritize-bets) needs to know which customer progress to serve and why.

The question: **for these targets and this horizon, which customer progress is worth addressing first, and how sure are we?**

## Inputs and authority

| Input | Use | Authority |
| --- | --- | --- |
| `target-segments` | Which situations count | market-strategist |
| `customer-knowledge` (Evidence) | Reported and observed problems, alternatives, language, willingness to pay | Evidence owns observations |
| `objectives` | What the priority must advance, and by when | venture-strategist; owner acceptance |
| Delivery context (`documentation`, `roadmap`) | What the venture can address now or later | Product owns capability |
| Owner material | What the owner reports about customers | Quote only what it contains |

## Method

Record sources, exact owner quotes and calculation premises in the relevant table’s basis or source cells. Carry decision status in its status column and the document’s role; prose states choices and ambition directly.

### 1. Develop customer progress from direction and capabilities

Start with the owner's direction and the venture's capabilities. Develop valuable applications, combinations and customer progress, including possibilities the owner did not list. Describe who benefits, what becomes possible and a feasible delivery path; then express each opportunity as a target situation and desired progress using [demand situations and segment distinctions](../../../knowledge/demand-situations-and-segment-distinctions.md).

Give each ranked opportunity its target reference. Prepare a concrete segment or target proposal for an application beyond the selected targets and continue the valid comparisons.

### 2. Examine what decides the priority

For each opportunity, assess only the factors consequential to this decision:

- **Consequence:** what the problem costs or blocks for the customer.
- **Frequency or trigger:** how often it occurs, or what event makes it urgent.
- **Dissatisfaction with the current alternative:** a workaround, complaints, or switching already happening.
- **Ability and willingness to pay:** observed payment for alternatives, a buyer with spending authority present.
- **Adoption effort:** what the customer must change to get the progress.
- **Venture fit:** whether available capability can deliver it, or which roadmap item it needs.

Record the basis in Basis and status: a source record for reported experience or observed behaviour, and reasoning for a developed hypothesis. Name the fastest action that strengthens the important premise.

### 3. Compare for the target and horizon

Compare opportunities on attractiveness and evidence strength as two axes ([evidence-sensitive comparison](../../../knowledge/evidence-sensitive-comparison.md), "Two axes, never one number"). Do not sum correlated ratings (pain, severity, urgency) as independent benefits. Account for bundles and dependencies: two opportunities served by one capability can outrank a single larger one; an opportunity that needs a roadmap capability cannot be first within the horizon unless enabling work is named.

Assign priorities (first, next, later, watch) with the reason against the next-ranked opportunity.

### 4. Strengthen the basis through useful production

Let attractiveness lead: compare the value of the progress, venture fit and contribution to ambition. In Basis and status record the source or reasoning and the fastest action that strengthens it. Produce a useful worked example, prototype, comparison or calculation within authority; prepare any market action requiring the owner's decision. State the condition that could change priority and use the result to revise the choice.

### 5. Evaluate and correct

| Defect | Detect | Correct |
| --- | --- | --- |
| Feature in place of progress | Desired progress names the product's function | Step 1 |
| Inferred problem presented as reported | Basis and status omits the reasoning for an inferred need or supplies no record for a reported one | Step 2: record the actual basis and the action that strengthens it |
| Double-counted ratings | Pain, severity and urgency summed | Step 3: keep the discriminating criterion |
| Priority outside capability and horizon | First priority needs an unbuilt capability, no enabling work named | Step 3 |
| Solution preference cited as demand | "Customers want X" sourced from the venture's own offer idea | Correct Basis and status; develop the action that tests the demand |

Run `python3 workers/strategy/.group/tools/check.py venture/{v}/strategy --owner-material {paths}`; the REF rule checks every opportunity refers to a target.

## Output

A candidate at `venture/{v}/strategy/candidate/opportunities.md`. The Conclusion states what deserves attention first and the commercial reason. The answer names the consumers affected (business-model-designer, Product, prioritize-bets) and the observation that would most change the order.

## Example

Illustrative fixture: fictional venture.

Give inspectors a report that expresses their professional judgment first. Develop a teaching example alongside that commercial route: it extends the same capability into a practical route to wider adoption.

| ID | Target | Situation | Desired progress | Current alternative | Consequence |
| --- | --- | --- | --- | --- | --- |
| OPP-1 | TGT-1 | Delivering findings after an inspection | A client-ready report in the inspector's own structure | Notes retyped into a template | Judgment becomes a clear result the client can use |
| OPP-2 | TGT-1 | Adopting a reporting tool | Bring an existing reporting approach into the app | Rebuild the template manually | Preserves continuity while adopting the tool |
| OPP-3 | TGT-1 | Helping a colleague develop reporting practice | Reuse an annotated example to explain how findings become conclusions | Explain each report separately | Extends professional practice through a shareable lesson |

| Opportunity | Demand and payment | Fit | Switching and delivery | Priority | Rationale |
| --- | --- | --- | --- | --- | --- |
| OPP-1 | App use; paid response to test | Capture and assembly | Available app | first | Strong direct customer value and a practical first commercial route |
| OPP-2 | Service demand to test | Template conversion | Helps OPP-1 adoption | next | Removes the transfer effort in the first route |
| OPP-3 | Reuse response to test | Report examples and explanation | Build from the worked report | next | Develops the ambition for professional reach beyond the original offer list |

| Opportunity | Basis and status | Could change priority | Next action |
| --- | --- | --- | --- |
| OPP-1 | [owner: "records findings on a tablet, and the app assembles a client-ready report"]; [hypothesis] paid value | Users cannot apply the output to a real report | Produce and inspect a complete example, then prepare the paid offer |
| OPP-2 | [owner: "convert an inspector's existing report template into ours"]; [hypothesis] adoption benefit | Conversion does not preserve the needed structure | Convert a representative template and inspect it |
| OPP-3 | [proposed] development from the founder's professional ambition; fastest strengthening action is an annotated example | Another inspector cannot reuse the lesson | Construct the example and test transfer to another report |

A draft labelled “tablet capture” becomes OPP-1's customer progress. Attractiveness determines the priority; the basis determines the best strengthening action.

## Recovery

| Condition | Next action |
| --- | --- |
| No customer-knowledge | Work from owner material and target situations, marking inferences `[hypothesis]`; name the interviews or observations that would rank the top two |
| No target-segments | Use candidate segments, say so in Built from and the answer, and route to choose-targets |
| Two opportunities tie | Prefer the one the available capability delivers within the horizon; state the tie and the observation that would break it |
| Owner insists on a solution-led opportunity | Record it as a proposed response under the relevant progress; the priority follows the progress |

## Final readable delivery

After this change's native documents and checks are final, follow the group's Human-readable result delivery: run `python3 {product-root}/.group/tools/result_html.py {state-directory} --open` once for the combined result and return `result.html` with the native files. The product root is this installed strategy group; the state directory is the current documents, with no automatic candidate overlay. Intermediate exports omit `--open`. Keep the complete file and report the exact path if the host cannot open it. This derived view changes no native record, decision, status or delivery contract.

For a final delivery that combines current documents and proposed revisions, pass `--candidate` explicitly to overlay matching files from `STATE_DIRECTORY/candidate/`. The HTML records those exact candidate source paths and statuses; generation grants no acceptance. Without this flag the current source set is exported. Point `STATE_DIRECTORY` directly at a standalone final/candidate document directory when that is the complete delivered result. Never substitute older current documents for the version actually delivered.
