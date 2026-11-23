---
name: prioritize-bets
description: Form, compare and select bets, each an intervention with an outcome mechanism toward a current objective, with its hardest assumption, the strongest alternative, a next commitment and continue, increase, change, hold and close conditions. Use after objectives exist and commercial choices are available, and when a review or new evidence changes which bets deserve concentration.
---

# prioritize-bets

Writes [`bet-portfolio`](../../../../.group/contracts/bet-portfolio.md) under the shared [document rules](../../../../.group/contracts/document-rules.md).

## When and what it decides

The question: **which interventions, run together, most credibly move the current objective, and what would make us continue, increase, change, hold or close each?** Consume only what the choice depends on.

## Inputs and authority

- `objectives` (required): the outcomes bets must serve.
- `opportunities`, `target-segments`, `positioning-decision`, `revenue-model`, `offer-catalogue`, `price-book`: the commercial configuration the bets act on. Read their statuses: a proposed offer is a proposal.
- `channel-map`, available capabilities, `experiment-result`, the current `focus-plan`.
- A bet never changes a member's choice; it states which choice it relies on and proposes changes to the owning member.

## Method

Record sources, exact owner quotes and calculation premises in the relevant table’s basis or source cells. Carry decision status in its status column and the document’s role; prose states choices and ambition directly.

1. **Develop routes to the objectives, ambition included.** Form each bet as condition → intervention → customer or operating response → objective contribution. Use [objective trade-offs](../../../knowledge/objective-tradeoffs-and-outcome-mechanisms.md) §2 to connect commercial progress with reach, adoption, authority or scale. Treat the hardest consequential assumption as a design input and specify the demonstration, comparison or market action that tests it. Record premises and estimates in Hypothesis and basis; record bet status in Disposition.
2. **Classify** each as establish, exploit or resolve ([portfolio choice](../../../knowledge/portfolio-choice-and-dependency-sequencing.md) §1). A resolve bet names the later decision it can change.
3. **Compare real alternatives**, always including continuing current work. Use the dimensions that differ: contribution, time to a readable result, delivery conditions, dependencies, reversibility, options opened. Use expected value only when outcomes, horizon and probabilities are defensible; otherwise compare scenarios and find the preference reversal (§2). Count learning once.
4. **Assemble the portfolio.** Keep bets that reinforce; resolve competition for the same customers' attention, product scope or owner decisions (§3). Name the strongest forgone bet and the condition that would revive it.
5. **Set controls before results.** For each bet: observation horizon, continue, increase, change, hold and close conditions with their basis, and the next commitment. A threshold placed where the bet already passes is not a control.
6. **Hand to focus.** Each selected bet has a next action and its actual dependency, ready for set-focus.

## Evaluate and correct

| Defect | Detect by | Correct by |
| --- | --- | --- |
| Restated goal as mechanism | "Do X to achieve the objective" with no customer behaviour | Write the customer or operating response that links them |
| Fabricated precision | Probabilities or response numbers without basis | Replace with scenarios and a reversal condition |
| Double-counted learning | Learning listed as a separate benefit beside the decision it improves | Keep only the decision consequence |
| Backfilled thresholds | Close condition already met or unreachable | Set it from the objective's decision point |
| Orphan bet | Objective reference missing or unresolved | Attach to an objective or drop; if no objective fits, report for set-objectives |
| Money in the bet | Amounts or hour estimates | Remove; name a needed purchase in the next action for set-focus |

Run the group check; REF findings on the Objective column are defects of this skill.

## Recovery

- **NeedData:** no objectives. Route to set-objectives first, or proceed on a proposed objective stated as such.
- **NeedData:** a commercial document is missing. Form the bet on what exists, mark the reliance as open and name the owning member.
- **Conflict:** two bets need incompatible choices (different target segments). Present both with the reversal condition; the owner chooses.

## Example

Illustrative fixture: fictional venture.

Brindlewick pursues wider use of own-format reporting (OBJ-1) and paid app use on real jobs (OBJ-2). A report demonstration serves both by making the professional idea inspectable.

```markdown
## Bets and mechanisms
| ID | Objective | Scope | Intervention | Expected outcome | Mechanism | Commercial references |
| --- | --- | --- | --- | --- | --- | --- |
| BET-1 | OBJ-1, OBJ-2 | Independent inspectors | Prepare a worked own-format report and a paid app offer | Inspectors reuse the approach and some buy the tool | A visible example shows how captured judgment becomes a client report; the app makes repeated production practical | TGT-1, OFR-1 |

## Commitment and comparison
| Bet | Disposition | Next action | Dependency | Rationale | Alternative |
| --- | --- | --- | --- | --- | --- |
| BET-1 | proposed | Build the worked report from the available app | An inspector-approved sample | Connects professional adoption to a deliverable commercial offer | A product feature page makes fewer professional ideas available to reuse |

## Evidence and control
| Bet | Hypothesis and basis | Observation horizon | Control conditions | Next commitment |
| --- | --- | --- | --- | --- |
| BET-1 | [hypothesis] inspectors can recognise and reuse the approach; [owner: "The desktop app works"]. Test the hardest assumption by having an inspector apply the example to a different report | First demonstration cycle | Continue when the approach transfers; revise the example if readers cannot apply it; reconsider the route if the result has no practical value | Produce the sample, then prepare the owner’s choice about publishing and the offer |
```

The hardest assumption shapes the demonstration; it leaves the useful report construction available to proceed.

## Final readable delivery

After this change's native documents and checks are final, follow the group's Human-readable result delivery: run `python3 {product-root}/.group/tools/result_html.py {state-directory} --open` once for the combined result and return `result.html` with the native files. The product root is this installed strategy group; the state directory is the current documents, with no automatic candidate overlay. Intermediate exports omit `--open`. Keep the complete file and report the exact path if the host cannot open it. This derived view changes no native record, decision, status or delivery contract.

For a final delivery that combines current documents and proposed revisions, pass `--candidate` explicitly to overlay matching files from `STATE_DIRECTORY/candidate/`. The HTML records those exact candidate source paths and statuses; generation grants no acceptance. Without this flag the current source set is exported. Point `STATE_DIRECTORY` directly at a standalone final/candidate document directory when that is the complete delivered result. Never substitute older current documents for the version actually delivered.
