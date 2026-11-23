---
name: design-revenue-model
description: Design how the venture captures value - who uses, benefits, decides and pays, which event triggers payment and what it obliges, the charging unit, timing, recurrence and expansion, and the economic drivers - and write the revenue-model candidate. Use when targets or opportunities are new or changed, when an offer needs an exchange to implement, or when observed buying behaviour or delivery cost contradicts the current model.
---

# design-revenue-model

**Transformation:** `target-segments` × `opportunities` × value and delivery mechanism × economic basis → [`revenue-model`](../../../../.group/contracts/revenue-model.md).

The document follows its contract and the group's [document rules](../../../../.group/contracts/document-rules.md).

## When to use it

- A first commercial configuration is being built and targets or candidate targets exist.
- A target, opportunity or delivery capability changed in a way that changes who pays, when, or what payment obliges.
- An observation (a lost purchase, a procurement objection, a delivery cost) contradicts the current exchange.

A price change alone belongs to set-prices; a packaging change alone belongs to design-offers.

## Inputs and authority

| Input | Use | When missing |
| --- | --- | --- |
| `target-segments` (or candidate `segments` during initial direction) | Whose purchase is being designed | Work on candidate segments and mark the exchange provisional |
| `opportunities` | What value the exchange captures | Reason from the target's need; mark the value a hypothesis |
| Capability and delivery context (`documentation`, `roadmap`, owner material) | What can be delivered and what it costs to deliver | Available capability only; costs stay `unknown` |
| `customer-knowledge` buying behaviour | How the payer buys | Buying conditions become hypotheses with the observation that would settle them |
| `unit-economics` (Finance) | Observed costs and margins | Drivers are named with values `unknown`; Finance's definitions apply when it exists |

You decide the proposed arrangement. Charging mechanics are choices and need a rationale; predicted response and delivery-cost figures need their own basis. Agreed terms come only from accepted decisions; legal wording belongs to Governance.

## Method

Record sources, exact owner quotes and calculation premises in the relevant table’s basis or source cells. Carry decision status in its status column and the document’s role; prose states choices and ambition directly.

### 1. Frame the exchange

For each target, write the four roles (user, beneficiary, decision-maker, payer) and the event that makes the payer pay. Apply [payer, value and payment §1–§2](../../../knowledge/payer-value-and-payment.md): when the payer is not the beneficiary, the payer buys only the value that returns to them; when the decision-maker is not the user, a trial or evaluation step is part of the purchase. Write the obligation the payment creates beside the entitlement.

What to notice:
- Whether the buyer's own income arrives per job, per period or per project: a charging unit that follows their income lowers resistance.
- Whether anything recurs for the customer (service, hosting, updates they need). Without it, recurrence has no customer rationale.
- Whether the payer can predict cost before committing.

### 2. Compare charging bases

Compare at least the two strongest bases (one-off licence, access period, usage unit, service fee, outcome fee, or a justified combination) on measurability, budget predictability, procurement fit, cost-value alignment and expansion path ([§3](../../../knowledge/payer-value-and-payment.md)). Choose one, and write the condition under which the runner-up wins; that condition goes in the Economics and alternatives prose.

Decision rules:
- Prefer the basis the payer already uses for comparable purchases unless cost-value alignment clearly favours another.
- Choose a subscription only when the customer receives something recurring; seller preference for recurring revenue is not a reason.
- Choose usage pricing only when the unit is measurable by both sides and the payer can forecast it.
- A one-off purchase with a separately priced service is a complete model; it needs no recurring layer.

### 3. Develop timing, recurrence, expansion and drivers

- Payment timing: upfront, split or periodic. Lay out schedules with `python3 workers/strategy/business-model-designer/tools/commercial.py timing --price "{amount}" --schedule {upfront|split:A%,B%|monthly:N}` when an amount is under consideration. A service carries a deposit-and-balance option tied to delivery.
- Expansion: more seats, more units, add-on services. State it only where a real path exists; `none` is a valid value.
- Drivers: list each revenue and cost driver of the exchange from [entitlement, delivery and economics §1, §3](../../../knowledge/entitlement-delivery-and-economics.md). Put the value’s source or calculation in its row’s basis cell. For a decision-relevant unresolved value, record the research or measurement that supplies it and explain its effect on the choice.

### 4. Evaluate viability

Ask whether the arrangement attracts payment and keeps viable economics at plausible adoption levels. Where a calculation helps, compute contribution per transaction with `python3 workers/strategy/business-model-designer/tools/commercial.py contribution --price … --fee …|none|unknown --variable-cost NAME=VALUE|none`; put its expression in the relationship cell and its inputs and derivation in the row’s Basis cell; retain the consequential premises. When an input is unknown the tool returns `unknown`: report the driver, never a stand-in figure.

### 5. Connect

State what design-offers and set-prices can now do, and the observation that would most change the model (a procurement objection, a measured delivery cost). Finance receives the exchange as Strategy's reasoning and keeps its own records.

## Defects to detect and correct

| Defect | Correction |
| --- | --- |
| Payer, purchase event, entitlement and charging unit do not line up (a "licence" that implies endless updates) | Rewrite the entitlement and obligation, or change the basis to access |
| Subscription with nothing recurring for the customer | Change to one-off plus separate service, or name the recurring element |
| A driver carries a number with no origin | Replace with `unknown` and state its effect on the choice |
| Assumed sales volume used to argue profitability | Recast as a conditional scenario with its premise, or remove |
| Proposed payment terms written as agreed | Label `[proposed]`; agreed terms need an accepted decision |
| Strongest alternative missing | Add it with the condition that would make it win |

Run `python3 workers/strategy/.group/tools/check.py {strategy-dir} --owner-material {paths}` on the working view; fix every error at its source.

## Output

A candidate at `venture/{v}/strategy/candidate/revenue-model.md`, recorded in the request's work-result. Charging units are written as plain tokens (`licence`, `conversion`, `seat-month`) because price-book units must match them exactly.

Illustrative fixture: fictional venture.

```markdown
## Conclusion
Independent inspectors buy a desktop licence for repeated report production and a separately scoped conversion service to preserve their own format.

## Parties and exchange
| ID | Target | User | Payer | Entitlement | Purchase trigger | Basis |
| --- | --- | --- | --- | --- | --- | --- |
| RM-1 | TGT-1 | Inspector | Inspector | Perpetual use of the purchased app version | Choose the app for regular reporting | [proposed] repeated use suits a licence; paid response to test |
| RM-2 | TGT-1 | Inspector | Inspector | One existing report template converted | Bring an existing format into the app | [owner: "convert an inspector's existing report template into ours"] |

## Charging mechanics
| Model | Charging unit | Payment timing | Recurrence | Expansion | Basis |
| --- | --- | --- | --- | --- | --- |
| RM-1 | licence | At purchase | none | Additional template conversions | [proposed] entitlement is the purchased version |
| RM-2 | conversion | At agreed start | none | A further template is a new conversion | [proposed] payment follows bounded service scope |

## Economics and alternatives
| Driver | Kind | Value | Effect on the choice | Basis |
| --- | --- | --- | --- | --- |
| Licence purchases | revenue | unknown: measure first paid offers | Determines the commercial adoption route | [hypothesis] purchase response to test |
| Conversion effort | cost | unknown: measure a representative conversion | Determines viable fixed scope | [proposed] measure the sample before extending scope |

Per-report charging is the strongest alternative if metering becomes available and buyers prefer payment by job. The licence provides a simple purchase for repeated use; Finance applies its own definitions to the resulting transactions.
```

## Recovery

| Condition | Next action |
| --- | --- |
| No targets yet | Design on candidate segments; mark the exchange provisional and name the target decision it waits for |
| Buying behaviour unknown | Proceed with the role analysis; list the buying condition as a hypothesis and the Evidence observation that settles it |
| Delivery cost unknown | Keep the driver `unknown`, scope the obligation so the cost is bounded, and name the measurement |
| Owner material conflicts with an accepted decision | Follow the accepted decision, quote both, and name the owner decision needed |

## Final readable delivery

After this change's native documents and checks are final, follow the group's Human-readable result delivery: run `python3 {product-root}/.group/tools/result_html.py {state-directory} --open` once for the combined result and return `result.html` with the native files. The product root is this installed strategy group; the state directory is the current documents, with no automatic candidate overlay. Intermediate exports omit `--open`. Keep the complete file and report the exact path if the host cannot open it. This derived view changes no native record, decision, status or delivery contract.

For a final delivery that combines current documents and proposed revisions, pass `--candidate` explicitly to overlay matching files from `STATE_DIRECTORY/candidate/`. The HTML records those exact candidate source paths and statuses; generation grants no acceptance. Without this flag the current source set is exported. Point `STATE_DIRECTORY` directly at a standalone final/candidate document directory when that is the complete delivered result. Never substitute older current documents for the version actually delivered.
