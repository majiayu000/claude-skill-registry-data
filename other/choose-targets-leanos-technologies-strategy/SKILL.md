---
name: choose-targets
description: Choose which segments the venture concentrates on now, against the strongest alternative segment, for the current objective and horizon; write qualification rules that tell rejection from unknown, and the conditions that activate later segments. Use after segments and a first differentiation exist, when the objective or horizon changes, or when a review finds the target is wrong. Writes the target-segments document.
---

# choose-targets

**Transformation:** segments × differentiation × objectives, horizon and operating constraints → [target-segments](../../../../.group/contracts/target-segments.md).

The document follows its contract and the group's [document rules](../../../../.group/contracts/document-rules.md).

## When to use

- Initial direction, after candidate segments and their differentiation exist (target and differentiation may iterate inside one change).
- The objective, its horizon or the available capabilities change.
- review-strategy names the target as the owning cause of a weak result.

The question: **which customers can the venture win within this horizon, why them rather than the strongest alternative, and how does someone tell a fitting prospect from one that does not fit or is not yet known?**

## Inputs and authority

| Input | Use | Authority |
| --- | --- | --- |
| `segments` | Candidates, recognition criteria, commercial profiles | market-strategist |
| `differentiation` | The advantage each candidate values, and its availability | positioning-strategist |
| `objectives` | The outcome and horizon the choice must serve | venture-strategist; owner acceptance |
| `venture-definition` | The accepted market scope the focus sits inside | venture-strategist; owner acceptance |
| Operating constraints | What the venture can deliver and reach now | Product capability evidence; owner material |

The target choice is this skill's proposal. Qualification rules are `[proposed]` unless the owner supplied them (quoted) or Evidence established them.

## Method

Record sources, exact owner quotes and calculation premises in the relevant table’s basis or source cells. Carry decision status in its status column and the document’s role; prose states choices and ambition directly.

### 1. Frame the choice

State the objective and horizon the target must serve, and what accepting the choice will commit others to (Product requirements, Engagement programmes, offer scope). If no objective exists, take the mandate's horizon and say so.

### 2. Run the accessibility chain for each candidate

For each meaningful candidate segment, assess each link: importance of the need, trigger, reachable decision-maker, ability to purchase, sales and adoption time, switching effort, ability to deliver the advantage ([commercial accessibility and target choice](../../../knowledge/commercial-accessibility-and-target-choice.md), "Accessibility is a chain"). Connect them: attention without a possible purchase, or urgent pain without practical switching, does not make a target. Name the **binding condition** of each candidate.

Check horizon fit: can a purchase complete before the horizon ends? A candidate whose buying cycle exceeds the horizon cannot contribute to this objective, however attractive. Choose among sequence, bridge or a question to set-objectives (same file, "Horizon fit").

### 3. Compare against the strongest alternative

Name the strongest alternative target and why it loses under the current objective. Compare on the binding conditions, with evidence strength kept separate from attractiveness ([evidence-sensitive comparison](../../../knowledge/evidence-sensitive-comparison.md), "Two axes, never one number"). Use a score only when several criteria matter and scales can be declared; run `python3 workers/strategy/market-strategist/tools/market.py score OPTIONS.csv --scale 1-5 --weights …` and report the reversal condition it gives. State the assumption that would reverse the choice.

Where the market runs on references, account for buyers who reference each other: winning one can lower the cost of the next.

### 4. Write the focus inside the whole

The Target choice states the current focus and horizon. A beachhead is a scoped route; the venture-definition keeps its accepted breadth. A recommendation that would drop an accepted customer group or product line goes to define-venture as a proposed revision, not into this document.

### 5. Write qualification rules

For each target, write rules a person can apply to one prospect, individual or organisation:

- One observable or askable indicator per rule.
- Kind: qualifier or disqualifier.
- **When unknown:** the treatment when the indicator is not known (ask in the first conversation; treat as possible). Unknown never silently rejects.

Test the rules on two or three plausible prospects with `python3 workers/strategy/market-strategist/tools/market.py qualify target-segments.md PROSPECT.json --target TGT-n`. A prospect with a missing indicator must come out `unknown`, not `disqualified`. Each rule rests on the commercial mechanism (why a fitting prospect can buy and benefit); a claim that a rule predicts conversion needs observed outcomes.

### 6. Sequence the rest

For each deferred or subsequent segment, state its disposition, the strongest alternative, the commercial or capability condition that activates it, and the assumption that could reverse the preference. Calendar dates alone never activate a segment.

### 7. Evaluate and correct

| Defect | Detect | Correct |
| --- | --- | --- |
| Chosen on pain and size, timing ignored | No binding condition or horizon fit stated | Step 2 |
| Straw-man alternative | The rejected option is one nobody would pick | Step 3 with the strongest real alternative |
| Beachhead replaces the venture | Target choice reads as what the venture is | Step 4; route scope change to define-venture |
| Unknown treated as rejection | A rule lacks "When unknown", or the qualify run gives disqualified for a missing indicator | Step 5 |
| Rule attributed without source | Basis names an owner rule absent from the material | Put the proposal and its commercial mechanism in Basis; retain the document's decision status |
| Advantage reference to a planned capability presented as current | Advantage row availability is planned | Keep the target, state the enabling condition, or choose a target served by available capability |

Run `python3 workers/strategy/.group/tools/check.py venture/{v}/strategy --owner-material {paths}` and resolve errors at their source; the REF rule checks that targets refer to declared segments and advantages.

## Output

A candidate at `venture/{v}/strategy/candidate/target-segments.md`. The Conclusion names the focus, its horizon and its reason. The answer states the reversing assumption, the unknowns that bear on qualification, and which consumers (Product, Meaning, Engagement, Evidence, business-model-designer) the change affects.

## Example

Illustrative fixture: fictional venture.

Target independent inspectors for the first commercial cycle: the app serves their individual reporting work and they can decide on the purchase themselves. Develop the training application alongside it as a route to professional adoption.

| Target | Choice | Basis |
| --- | --- | --- |
| TGT-1 / SEG-1 | First paid-use route | [proposed] fits the available app and March outcome; [owner: "Our first goal is paying inspectors using the app on real jobs by the end of March."] |
| SEG-2 | Strongest commercial alternative; sequence after a workable trial and team capability | [owner: "decide slowly and want a trial on a few jobs first"]; [hypothesis] preference reverses if a firm can complete a fitting trial within the horizon |

| ID | Target | Kind | Indicator | When unknown | Basis |
| --- | --- | --- | --- | --- | --- |
| QR-1 | TGT-1 | qualifier | Writes and signs own reports | Ask in the first conversation; retain as possible | [proposed] the buyer controls reporting practice |
| QR-2 | TGT-1 | disqualifier | Employer mandates a different report tool | Ask before a demonstration; retain as possible | [proposed] mandatory tooling changes the purchase path |

| Segment | Disposition | Strongest alternative | Enabling condition | Reversing assumption | Basis |
| --- | --- | --- | --- | --- | --- |
| SEG-2 | later | SEG-1 | Firm agrees a trial using deliverable capability | Firm can decide inside the commercial horizon | [hypothesis] test through the trial decision |

With a longer horizon and available team capability, compare the firm route again; the changed delivery and purchase conditions can justify a different target.

## Recovery

| Condition | Next action |
| --- | --- |
| No objective exists | Use the mandate's horizon, state it as the frame, and name set-objectives as the owner of the missing objective |
| No differentiation yet | Produce provisional targets with the advantage column `none`; the change routes to define-differentiation and back |
| Every candidate's cycle exceeds the horizon | Propose the fastest sub-situation, and state for set-objectives that the horizon may not fit any segment |
| Qualify tool reports a rule without a target | Fix the Target column; rerun |
| Owner names a target the analysis does not favour | Present the comparison and the reversing condition; the owner decides scope |

## Final readable delivery

After this change's native documents and checks are final, follow the group's Human-readable result delivery: run `python3 {product-root}/.group/tools/result_html.py {state-directory} --open` once for the combined result and return `result.html` with the native files. The product root is this installed strategy group; the state directory is the current documents, with no automatic candidate overlay. Intermediate exports omit `--open`. Keep the complete file and report the exact path if the host cannot open it. This derived view changes no native record, decision, status or delivery contract.

For a final delivery that combines current documents and proposed revisions, pass `--candidate` explicitly to overlay matching files from `STATE_DIRECTORY/candidate/`. The HTML records those exact candidate source paths and statuses; generation grants no acceptance. Without this flag the current source set is exported. Point `STATE_DIRECTORY` directly at a standalone final/candidate document directory when that is the complete delivered result. Never substitute older current documents for the version actually delivered.
