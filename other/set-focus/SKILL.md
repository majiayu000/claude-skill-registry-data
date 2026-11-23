---
name: set-focus
description: Turn the selected bets into a focus-plan of concrete next actions with real executors, timing (now, parallel, after, deferred) and actual prerequisites, pairing every blocked action with an enabling step so independent work starts now. Use after bets are chosen, when a dependency completes, when results or execution conflicts change the useful next action, or when work is stalled.
---

# set-focus

Writes [`focus-plan`](../../../../.group/contracts/focus-plan.md) under the shared [document rules](../../../../.group/contracts/document-rules.md).

## When and what it decides

The question: **what can actually advance the objective now, with which available capability, and what waits for what?** The plan names focus and sequence; execution detail stays with the operating owner.

## Inputs and authority

- `bet-portfolio` (required): active and proposed bets with their next commitments.
- Available capabilities: installed workers and tools (from the registry), actual access, material and outputs that exist. An unbuilt group, uninstalled tool or missing access is not an executor.
- Actual dependencies and current results; the satisfied prerequisites known at the request.
- Money management belongs to Finance. The plan names a purchase an action needs; Finance decides it.

## Method

Record sources, exact owner quotes and calculation premises in the relevant table’s basis or source cells. Carry decision status in its status column and the document’s role; prose states choices and ambition directly.

1. **List candidate actions** from each bet's next commitment, plus the preparation and enabling work they need. Each action has one intended output.
2. **Assign real executors.** For each action name the installed capability or named person that performs it. Where none exists, the action is blocked: write an enabling action with the concrete missing condition, the enabling step or available alternative, its owner, and the work that continues meanwhile.
3. **Separate dependency from preference** ([portfolio choice](../../../knowledge/portfolio-choice-and-dependency-sequencing.md) §4). A prerequisite is an output, access or authority the action cannot proceed without. Preference sets priority only.
4. **Compute the ready set** (§5): `python3 workers/strategy/venture-strategist/tools/focus.py ready {focus-plan} --satisfied {ids or conditions known to hold}`. Ready actions get `now` (highest strategic contribution and enabling value) or `parallel`; waiting actions get `after` with their prerequisite; intentionally postponed ones get `deferred` with a reason in Change conditions. One blocked action never holds the others.
5. **Name human involvement precisely.** AI production is described by its output and elapsed execution. A person appears only as a named decision or contribution a specific action needs ("owner approves the offer text").
6. **Attach purchases to actions.** If an action needs an actual purchase or financial commitment, write it in that action's prerequisite or enabling step ("needs a payment-processor account: Finance decides"), with no amount. Independent actions remain `now` or `parallel`.
7. **State change conditions**: the observation or completed dependency that would change concentration or sequence.

## Evaluate and correct

| Defect | Detect by | Correct by |
| --- | --- | --- |
| Money or hour gate | Amounts, budget lines, hour or headcount estimates; check rule FOCUS-MONEY | Remove; keep the purchase need on its action |
| Global stop | Every action `after` one unresolved item | Rerun the ready set; give independent actions `now`/`parallel` |
| Phantom executor | Executor not installed or not a named person | Add an enabling action; mark the action `after` it |
| Preference as dependency | Prerequisite is "better after" rather than "needs" | Clear the prerequisite; set priority in Current focus |
| Timing disagrees with readiness | `focus.py ready` reports a now/parallel action with unmet prerequisites, or a cycle | Fix the timing or the prerequisite and rerun |

Run `focus.py ready` and the group check; both must report no errors.

## Recovery

- **NeedData:** no bets. Route to prioritize-bets, or sequence the preparation actions of a proposed bet stated as proposed.
- **NeedData:** executor availability unknown. Write the action with executor `unknown` and an enabling action "confirm the executor", owned by the router; continue with the rest.
- **Failure:** nothing useful is ready. Name the missing condition and its owner as the plan's first enabling action; that is the focus.

## Example

Illustrative fixture: fictional venture.

```markdown
## Current focus
Prepare the own-format report demonstration and paid offer for BET-1. A firm-trial outline can proceed alongside that work.

## Work sequence
| ID | Bet | Action and output | Executor | Timing | Prerequisite | Basis |
| --- | --- | --- | --- | --- | --- | --- |
| ACT-1 | BET-1 | Draft the paid offer with entitlement and first-value path | business-model-designer | now | none | [proposed] develops the selected bet's exchange |
| ACT-2 | BET-1 | Send the offer to current users | owner | after | ACT-1, ENB-1 | [proposed] requires the prepared offer and payment route |
| ACT-3 | BET-2 | Develop the firm-trial outline | owner with inspector co-founder | parallel | none | [proposed] independent preparation |

## Enabling actions
| ID | Action | Missing condition | Enabling step or alternative | Owner | Continuing work |
| --- | --- | --- | --- | --- | --- |
| ENB-1 | ACT-2 | Payment route | Prepare a payment account choice for Finance; assess manual invoicing as an available route | Finance | ACT-1, ACT-3 |
```

The ready-set check examines prerequisites. Finance receives the payment decision attached to ACT-2, while ACT-1 and ACT-3 have usable outputs to construct.

## Final readable delivery

After this change's native documents and checks are final, follow the group's Human-readable result delivery: run `python3 {product-root}/.group/tools/result_html.py {state-directory} --open` once for the combined result and return `result.html` with the native files. The product root is this installed strategy group; the state directory is the current documents, with no automatic candidate overlay. Intermediate exports omit `--open`. Keep the complete file and report the exact path if the host cannot open it. This derived view changes no native record, decision, status or delivery contract.

For a final delivery that combines current documents and proposed revisions, pass `--candidate` explicitly to overlay matching files from `STATE_DIRECTORY/candidate/`. The HTML records those exact candidate source paths and statuses; generation grants no acceptance. Without this flag the current source set is exported. Point `STATE_DIRECTORY` directly at a standalone final/candidate document directory when that is the complete delivered result. Never substitute older current documents for the version actually delivered.
