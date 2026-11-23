---
name: design-category
description: Develop a proposed market category when choose-frame selects or develops it as a live option, or when the owner asks for one. Define its distinction, test membership on included and excluded cases, and develop its name, point of view, language and adoption path through the frame comparison. Writes category-definition.
---

# design-category

**Transformation:** positioning-decision × customer understanding × discourse × available capability → [`category-definition`](../../../../.group/contracts/category-definition.md).

Document form, basis and requiredness: [document rules](../../../../.group/contracts/document-rules.md).

## When to use

Run when choose-frame selects or develops a category option, or when the owner asks for one. Develop the option with choose-frame's comparison.

The question: **which distinction lets buyers recognise and compare useful approaches, who could belong, and how can the venture help people adopt it?**

## Inputs and authority

| Input | Use | Authority |
| --- | --- | --- |
| `positioning-decision` | The chosen or live category option, leading value and compared frames; develop the comparison with choose-frame for an owner request | This worker |
| `differentiation` | Advantages and availability | This worker |
| `customer-knowledge`, `discourse-snapshot` | How buyers name the problem; existing categories | Evidence |
| `documentation`, `roadmap` | What the venture can demonstrate now | Product |

You decide membership, name, point of view, language and adoption path as proposals. Meaning integrates the language, Identity expresses the name, Engagement executes adoption work; the owner accepts the category. Acceptance is decision status, never market adoption.

## Method

Use [buyer interpretation and category expectations](../../../knowledge/buyer-interpretation-and-category-expectations.md) for strong-category criteria, boundary tests and interpretation tests.

1. **State the hidden distinction.** Name the problem, approach or outcome that existing categories fail to communicate and what buyers could recognise or compare once it is named. If the distinction is only a feature of the venture, stop and return the finding to choose-frame.
2. **Define membership by the distinction.** Write conditions about the problem addressed, the approach taken or the outcome delivered. Never "has our features".
3. **Test boundaries on cases.** Write representative cases: at least one plausible member that is not the venture's offering, at least one plausible neighbour that is out, and one case near the boundary. Each is decided by a stated condition. If only the venture is in, the category fails; recommend staying in the existing or narrower frame.
4. **Relate to existing categories.** State what the new category is a kind of, what it is not, and which existing category buyers will compare it with first.
5. **Develop the name and point of view.** The name reveals the problem or approach in the buyer's words where possible. The point of view connects the current problem to the proposed approach in a few sentences. Define only the terms buyers need to understand and choose.
6. **Plan adoption.** Name the initial audience most likely to adopt the frame, what they must understand or do differently, the demonstration that shows it with available capability, the execution owner and how progress is observed. Compare the burden with staying in the existing frame; if the burden does not pay within the horizon, say so in the Conclusion.
7. **Record basis and decision status.** Put the source or reasoning for membership, language and adoption in the relevant basis or source cells. Carry proposed or accepted status through the category document’s role and status fields. Name predicted recognition and the action that tests it in the adoption basis; cite observed responses at their source.

## How the conclusions change the document

- Category purpose: the distinction it makes useful, in one or two sentences.
- Definition and boundaries: name and membership in prose; the test cases with in/out and the deciding distinction in the table.
- Point of view and language: the problem, the approach, the term table.
- Adoption path: one row per consequential step with audience, change, demonstration, owner, progress observation.
- Put sources, owner quotes and calculation expressions in the table's basis or source cells; carry decision status in the status column and document role. State the venture's choices and ambition directly in prose, qualifying only distinctions that change a decision.

## Example

Illustrative fixture: fictional venture and developed category option.

Own-format reporting makes professional judgment the organising principle of report structure. A report can be assembled from captured findings while retaining the inspector's approach; buyers gain a useful distinction when comparing tools and services.

| Case | Membership | Distinction | Basis |
| --- | --- | --- | --- |
| Brindlewick app with template conversion | in | Captured findings assembled in the inspector's structure | [proposed] category construction; available app and conversion supply the demonstration |
| Another tool importing a professional's template and filling it from site capture | in | Same approach through a different product | [proposed] plausible member, not a claim that a named competitor exists |
| Service connecting site capture to an inspector-owned report template | in | Same approach through a service | [proposed] membership follows the approach |
| Fixed vendor report layout | out | Structure is prescribed by the vendor | [derived: membership requires inspector-owned structure] |
| Template filled entirely by hand | out | Captured findings are not assembled into the report | [derived: membership requires capture-to-report assembly] |

| Audience | Change | Demonstration | Owner | Progress observation | Basis |
| --- | --- | --- | --- | --- | --- |
| Independent inspectors | Compare reporting approaches by who controls the report structure | A converted template filled from a sample inspection | Engagement | Inspectors explain and reuse the distinction in a fresh comparison | [hypothesis] test comprehension and reuse; owner acceptance records the category decision only |

The option is ready for Meaning to develop its language and for the owner to compare with the narrower commercial frame.

## Evaluate and correct

| Defect | Detect | Correct |
| --- | --- | --- |
| Feature-list category | Membership conditions name the venture's features | Rewrite as problem, approach or outcome; retest cases |
| Single-member category | No member other than the venture | Return to choose-frame with the finding |
| No excluded neighbour | Every case is in | Add the nearest neighbour and the condition excluding it |
| Planned demonstration | Adoption depends on a planned capability | Use an available demonstration or sequence the step after the build |
| Adoption from acceptance | Recognition claimed because the name was accepted | Relabel `[hypothesis]`; name the observation |

From the worker root run `python3 workers/strategy/.group/tools/check.py venture/{v}/strategy --owner-material {paths}`; correct every error. The boundary review above establishes the distinction; the check establishes structure and labels only.

## Output

A candidate `category-definition`, and in the answer: the distinction, the boundary verdicts, the adoption burden compared with staying in the existing frame, and what Meaning, Identity and Engagement each receive.

## Recovery

- Category option needs comparison: Develop the option with choose-frame's comparison.
- The boundary test fails: return a Failure result recommending the existing or narrower frame, with the cases that failed.
- No discourse evidence: write existing-category relations from the alternatives in `differentiation` and label them `[hypothesis]`; name the discourse-snapshot question for Evidence.

## Final readable delivery

After this change's native documents and checks are final, follow the group's Human-readable result delivery: run `python3 {product-root}/.group/tools/result_html.py {state-directory} --open` once for the combined result and return `result.html` with the native files. The product root is this installed strategy group; the state directory is the current documents, with no automatic candidate overlay. Intermediate exports omit `--open`. Keep the complete file and report the exact path if the host cannot open it. This derived view changes no native record, decision, status or delivery contract.

For a final delivery that combines current documents and proposed revisions, pass `--candidate` explicitly to overlay matching files from `STATE_DIRECTORY/candidate/`. The HTML records those exact candidate source paths and statuses; generation grants no acceptance. Without this flag the current source set is exported. Point `STATE_DIRECTORY` directly at a standalone final/candidate document directory when that is the complete delivered result. Never substitute older current documents for the version actually delivered.
