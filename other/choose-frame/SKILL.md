---
name: choose-frame
description: Choose the competitive frame in which target buyers understand the venture's leading advantage, test the expectations it creates against the actual offering, and decide whether category design is warranted. Use after differentiation is set or when the frame, offer scope or leading advantage changes. Writes positioning-decision.
---

# choose-frame

**Transformation:** differentiation × target buyers' understanding × market discourse and offer scope → [`positioning-decision`](../../../../.group/contracts/positioning-decision.md).

Document form, basis and requiredness: [document rules](../../../../.group/contracts/document-rules.md).

## When to use

- A current or candidate `differentiation` has a leading advantage and the frame is unset, or the leading advantage changed.
- The offer scope changes in a way that changes what a frame would promise.
- A proposed category, tagline or name is offered as positioning: evaluate it here as a frame choice.

The question: **which frame makes the leading value obvious to the target buyer, creates expectations the actual offering meets, and carries an education burden the commercial path can bear?**

## Inputs and authority

| Input | Use | Authority |
| --- | --- | --- |
| `differentiation` | Leading advantage, alternatives, availability | This worker |
| `target-segments` | The buyer and situation | market-strategist |
| `customer-knowledge`, `discourse-snapshot` | How buyers describe the problem and what they compare | Evidence; `[observed: …]` |
| `offer-catalogue`, offer scope | What is sold and its status | business-model-designer |
| `venture-definition` | The audience and scope the frame stays within | venture-strategist |

You decide the frame and whether category design is activated. Meaning writes the messages; this document states the competitive choice and value, not copy.

## Method

Use [buyer interpretation and category expectations](../../../knowledge/buyer-interpretation-and-category-expectations.md) for expectation dimensions, frame kinds, education burden and criteria for a strong category, and [alternatives and value mechanisms](../../../knowledge/alternatives-and-value-mechanisms.md) for what the leading advantage is and against what.

1. **Start from the leading advantage and its best-fit buyer.** The frame exists to make that value obvious; if the leading advantage rests on a `planned` capability, stop and return to define-differentiation.
2. **Develop the three frame kinds.** List the existing frame, a narrower frame and a category grounded in the owner's perspective. Give each a real distinction, intended buyer interpretation and way to demonstrate the leading value.
3. **Test each frame's expectations.** For buyer, purpose, competitors, features, price and adoption, write what a buyer inside the frame assumes and set it against the actual offering and its availability. A frame that implies an unavailable feature, a different buyer, a different price model or easier adoption than delivery allows creates a false expectation: reject it, or name the resolution.
4. **Weigh the education burden against the route.** A self-serve route needs value visible on first contact; a guided route can carry more explanation. A frame whose burden the route cannot carry within the horizon loses even if it is elegant.
5. **Select and compare.** Choose the frame that makes the leading value understandable with accurate expectations and workable burden; state the strongest alternative frame and why it loses. It need not make every differentiator central.
6. **Keep scope.** The frame's audience stays inside the venture-definition. A frame for the initial target is a scoped focus; a frame that would redefine whom the venture serves is a proposed venture-definition revision for venture-strategist.
7. **Develop the category option. Compare it on the distinction it makes visible, its plausible members and its adoption path. Choose.** Carry a chosen category or a worthwhile live option to design-category; record the comparison with the existing and narrower frames in Choice rationale.
8. **Record basis and test interpretation.** Offering basis carries capability sources and the reasoning for expected interpretations; Implications names the comprehension test or demonstration. Record the chosen frame through the document’s decision role and the category option’s state in its comparison record.

## How the conclusions change the document

- Positioning choice: target and situation, frame, leading ADV, in one or two sentences.
- Frame meaning: one row per consequential expectation, with the offering basis and the mismatch to resolve (or `none`).
- Choice rationale: strongest alternative frame, education burden, remaining assumption.
- Implications: what Meaning must preserve, what Identity, Engagement or offer scope must reflect, and the category option to develop.
- Put sources, owner quotes and calculation expressions in the table's basis or source cells; carry decision status in the status column and document role. State the venture's choices and ambition directly in prose, qualifying only distinctions that change a decision.

## Example

Illustrative fixture: fictional founder material and venture.

Brindlewick's founder believes professional judgment should shape the report. Develop three frames for the capture-to-report advantage and compare what each makes visible.

| Frame | Distinction and expectations | Plausible members and adoption | Choice / basis |
| --- | --- | --- | --- |
| Inspection report software | Familiar purpose; buyers may expect standard report features | Report tools; explain the template advantage in a product demonstration | Existing-frame option; [hypothesis] test which capabilities readers expect |
| Report software in your own format | Makes preserving an inspector's structure visible | Configurable report tools; show before-and-after template conversion | Chosen first commercial frame; [proposed] useful distinction with a short demonstration |
| Own-format reporting | Professional judgment determines structure, carried from site capture to assembled output | Template-import tools and services integrating capture with custom assembly; teach through worked reports | Live category option; [proposed] develops the founder's conviction; write category-definition and test whether inspectors reuse the distinction |

**Positioning choice:** Brindlewick is report software in your own format: findings captured once become a client-ready report that preserves the inspector's way of working.

| Expectation | Offering basis | Mismatch to resolve |
| --- | --- | --- |
| On-site findings enter the report | [owner: "records findings on a tablet, and the app assembles a client-ready report"] | none |
| Existing report structure is retained | [owner: "convert an inspector's existing report template into ours"] | Inspect the converted sample before representing exact format fidelity |
| Phone photos flow automatically | [owner: "Photo sync from phones is planned for next year; it does not exist yet."] | Describe tablet capture and desktop assembly precisely |

The narrower frame serves the first purchase. The category gives Meaning a professional viewpoint and Engagement a demonstration to develop as a live option; test both with an inspector's unaided explanation of the same report.

## Evaluate and correct

| Defect | Detect | Correct |
| --- | --- | --- |
| Slogan instead of choice | Positioning choice lacks target, frame or leading value | Rewrite as the competitive choice |
| False expectation | A Frame meaning row with an unmet expectation and no resolution | Resolve it or choose another frame |
| Planned value in a present frame | `positioning.py check --positioning` reports a planned ADV | Lead with an available ADV, or state the planned capability as planned |
| Scope drift | The frame's audience differs from the venture-definition | Mark it a scoped focus or propose the revision |
| Interpretation as fact | A buyer reading without a label | Label `[hypothesis]`; name the test |
| Frame defended by default: an existing frame chosen without developing the category option | Comparison omits a meaningful category | Develop its distinction, plausible members and adoption path; compare and choose |

From the worker root run `python3 workers/strategy/positioning-strategist/tools/positioning.py check venture/{v}/strategy/candidate/differentiation.md --positioning venture/{v}/strategy/candidate/positioning-decision.md --offers venture/{v}/strategy/offer-catalogue.md` and `python3 workers/strategy/.group/tools/check.py venture/{v}/strategy --owner-material {paths}`. Review each `review` finding against the wording; correct each error.

## Output

A candidate `positioning-decision`, and in the answer: the frame, the strongest rejected frame, the expectations Meaning must preserve, the category activation decision, and the observation that would test the predicted interpretation.

## Recovery

- No differentiation: run define-differentiation first.
- No discourse or customer evidence: choose on the offering and alternatives, label buyer interpretations `[hypothesis]`, and name the discourse-snapshot question for Evidence.
- Offer scope unknown: write expectations against the venture-definition and capability; name business-model-designer for the offer.
- The best frame needs a capability that is only planned: choose the best frame the available offering meets now and record the planned frame as a bet implication.

## Final readable delivery

After this change's native documents and checks are final, follow the group's Human-readable result delivery: run `python3 {product-root}/.group/tools/result_html.py {state-directory} --open` once for the combined result and return `result.html` with the native files. The product root is this installed strategy group; the state directory is the current documents, with no automatic candidate overlay. Intermediate exports omit `--open`. Keep the complete file and report the exact path if the host cannot open it. This derived view changes no native record, decision, status or delivery contract.

For a final delivery that combines current documents and proposed revisions, pass `--candidate` explicitly to overlay matching files from `STATE_DIRECTORY/candidate/`. The HTML records those exact candidate source paths and statuses; generation grants no acceptance. Without this flag the current source set is exported. Point `STATE_DIRECTORY` directly at a standalone final/candidate document directory when that is the complete delivered result. Never substitute older current documents for the version actually delivered.
