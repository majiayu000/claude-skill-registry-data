---
name: segment-market
description: Divide a venture's possible customers into demand situations that change a commercial decision, with recognition criteria and an evidence-based commercial profile. Use when the venture needs segments for the first time, when customer or market evidence changes, or when a target, opportunity or offer decision needs a clearer customer distinction. Writes the segments document.
---

# segment-market

**Transformation:** customer-knowledge × market context × channel-map → [segments](../../../../.group/contracts/segments.md).

The document follows its contract and the group's [document rules](../../../../.group/contracts/document-rules.md).

## When to use

- Initial direction: candidate segments that define-differentiation and choose-targets will compare.
- A new observation (a customer group behaving differently, a new alternative, a channel change) suggests the current boundaries no longer separate decisions.
- A downstream skill reports that two targets or opportunities cannot be told apart, or that one segment hides two buying paths.

The question this skill answers: **which differences between customers change what the venture should do, and how will anyone recognise a member?**

## Inputs and authority

| Input | Use | Authority |
| --- | --- | --- |
| `customer-knowledge` (Evidence) | Situations, jobs, triggers, alternatives, buying roles, with strength of support | Evidence owns the observations; this skill interprets them |
| `market-landscape`, `market-size` (Evidence) | Alternatives and size factors where they exist | Evidence owns them |
| `channel-map` (Evidence) | Where a segment can be reached | Evidence owns it |
| `mandate` (Governance), `venture-definition` | Scope the segmentation must stay within; accepted customer breadth | Owner and Governance |
| Owner material | What the owner states about customers | Quote only what it contains |
| Product context (`documentation`, `roadmap`) | Delivery differences that would split a segment | Product owns capability |

When Evidence documents do not exist yet, owner material and direct reasoning from the venture's situation supply the candidates. Proposed segments are legitimate work; they are labelled `[proposed]` and never attributed to a source that does not contain them. Population counts, demand and triggers that no source supports stay `unknown`.

## Method

Record sources, exact owner quotes and calculation premises in the relevant table’s basis or source cells. Carry decision status in its status column and the document’s role; prose states choices and ambition directly.

### 1. Develop opportunities from direction and capabilities

Read the owner's purpose and ambition beside the venture's capabilities. Develop useful customer applications, including ones the owner did not list: who benefits, what becomes possible and how the venture could deliver it. Use those possibilities to frame the targeting, offer, channel and product decisions the segmentation must serve. Each boundary must change one of those decisions.

### 2. Recover situations, then group

Read the material for situations, not personas: circumstance, progress sought, current alternative, purchase conditions ([demand situations and segment distinctions](../../../knowledge/demand-situations-and-segment-distinctions.md), "The unit of analysis is the situation"). Then group situations that would receive the same decision.

Notice especially:

- **Who buys versus who uses.** A different buyer means a different purchase path, length and proof. This is the most frequent real boundary.
- **The trigger.** A situation with a trigger (deadline, failure, growth step) buys; the same need without a trigger waits.
- **The alternative and its switching cost.** Customers on paper and customers on a competing paid tool need different advantage chains.
- **Delivery differences.** A team needs shared templates or administration that a single user does not; that changes offer scope.

Add candidate segments the material does not list when expertise suggests a consequential difference (customers on a competing tool; a sub-situation inside a slow segment that buys faster). Record the reason in Basis; the candidate document carries their proposed status.

### 3. Contrast neighbours and cut what does no work

For each segment, write how it differs from its nearest neighbour in trigger, buyer, alternative, delivery or value. If no difference changes a decision, merge them. Demographic or firmographic attributes stay only where they mark such a difference. Overlap is allowed; record it in Boundaries with its consequence.

### 4. Characterise demand and accessibility with the evidence there is

For each segment, fill the commercial profile from sources:

- **Demand and value:** the indications relevant to this decision. Put the source of reported or observed demand in Basis; put the reasoning and strengthening action for an inferred need there.
- **Reach and purchasing:** the channel, the decision-maker and the buying path ([commercial accessibility and target choice](../../../knowledge/commercial-accessibility-and-target-choice.md), the accessibility chain). Name the link most likely to bind.
- **Size:** a range from grounded factors, run through `python3 workers/strategy/market-strategist/tools/market.py estimate FACTORS.csv`, or `unknown`, or `n/a: {reason}` when the decision does not depend on it ([evidence-sensitive comparison](../../../knowledge/evidence-sensitive-comparison.md), "Estimates and ranges"). The tool returns `unknown` and names the missing factor when any factor lacks a basis; copy that result, never a guessed number.
- **Delivery:** what serving the segment requires.

### 5. Test usability

For each segment ask: can Evidence recognise a member from the criteria? Can Engagement reach one? Can Product state what they need? Rewrite criteria that only the venture can see ("values our approach") as observable indicators, or mark them for Evidence to develop. Split or merge only when the answer changes a supported decision.

### 6. Evaluate and correct

Before delivering, check the document against these defects and correct at the step that produced them:

| Defect | Detect | Correct |
| --- | --- | --- |
| A boundary changes no decision | Two segments get the same target, offer and channel decision | Merge (step 3) |
| Solution-shaped segment | Segment named after the product feature | Restate as situation and progress (step 2) |
| Invented number | A size, count or rate without factors and basis | `unknown` or an estimate with factors (step 4) |
| Proposal attributed to a source | Basis attributes a construction to material that does not contain it | Record the proposal rationale in Basis and retain the candidate document's status (step 2) |
| Unrecognisable segment | Criteria nobody outside the venture could apply | Observable indicator, or flagged for Evidence (step 5) |

Then run `python3 workers/strategy/.group/tools/check.py venture/{v}/strategy --owner-material {paths}` from the repository root and resolve its errors at their source. A clean check establishes structure, references and quotes, not that the segmentation is good.

## Output

A candidate at `venture/{v}/strategy/candidate/segments.md`: segmentation logic, segment definitions, commercial profile, boundaries. The Conclusion names the distinction that matters most and the decision it serves. The answer names the open owner inputs and the observations Evidence could make to test proposed segments.

## Example

Illustrative fixture: fictional founder material and venture.

Brindlewick's direction is to make an inspector's own judgment and format practical throughout reporting. Its capture, assembly and template conversion capabilities open independent practice, team consistency and teaching applications.

| ID | Situation and need | Recognition criteria | Trigger | User and buyer | Alternatives | Basis |
| --- | --- | --- | --- | --- | --- | --- |
| SEG-1 | Independent inspector produces client reports in their own format | Writes and signs reports independently | A report due after an inspection | Inspector | Notes and a word-processor template | [owner: "three inspectors we know use it on their own jobs"]; [proposed] recognition rule |
| SEG-2 | Firm preserves a common reporting approach across inspectors | Several inspectors report under one firm | A team workflow decision | Inspectors use; firm owner buys | Firm templates | [owner: "Larger inspection firms with several inspectors have asked about team accounts"] |
| SEG-3 | Trainer helps new inspectors turn judgment into a well-structured report | Teaches inspection and reviews trainee reports | Preparing a report-writing lesson | Trainer buys; trainees use examples | Handwritten feedback on sample reports | [proposed] teaching application developed from the founder's direction and template capability |

| Segment | Demand and value | Reach and purchasing | Size | Delivery | Basis |
| --- | --- | --- | --- | --- | --- |
| SEG-1 | Useful report production; paid response to test | Contact through current users | n/a: first choice depends on purchase path | Available app and conversion | [owner: "They have not paid for it."]; [hypothesis] paid value; prepare a sample and offer |
| SEG-3 | Repeatable teaching examples | Identify a trainer and inspect a lesson | n/a: a worked lesson can test utility | Develop an annotated report example | [proposed] build a lesson specimen, then ask a trainer to apply it |

The trainer segment changes the deliverable and purchasing path. If it merely repeated the independent inspector's use, merge it; its teaching use must justify the boundary.

## Recovery

| Condition | Next action |
| --- | --- |
| No customer-knowledge exists | Build candidates from owner material and the venture's situation, labelled `[proposed]`; name the observations Evidence should collect to test them |
| Size factors lack a basis | Write `unknown`, or `n/a` with the reason the decision does not depend on size; name the deciding factor and how it could be obtained |
| Owner material contradicts Evidence | Keep both with their origins; proceed on the more likely reading and name the conflict for the owner |
| A segment would exclude an accepted customer group from the venture | Keep the group as a segment; a scope change is a proposed revision of the venture-definition by define-venture |
| The check reports ATTRIB-ABSENT | Remove the attribution or quote the passage the material actually contains |

## Final readable delivery

After this change's native documents and checks are final, follow the group's Human-readable result delivery: run `python3 {product-root}/.group/tools/result_html.py {state-directory} --open` once for the combined result and return `result.html` with the native files. The product root is this installed strategy group; the state directory is the current documents, with no automatic candidate overlay. Intermediate exports omit `--open`. Keep the complete file and report the exact path if the host cannot open it. This derived view changes no native record, decision, status or delivery contract.

For a final delivery that combines current documents and proposed revisions, pass `--candidate` explicitly to overlay matching files from `STATE_DIRECTORY/candidate/`. The HTML records those exact candidate source paths and statuses; generation grants no acceptance. Without this flag the current source set is exported. Point `STATE_DIRECTORY` directly at a standalone final/candidate document directory when that is the complete delivered result. Never substitute older current documents for the version actually delivered.
