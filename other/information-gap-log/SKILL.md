---
name: Information Gap Log
description: Produces a live register of every assumption the price rests on but no evidence has confirmed, each with an owner, a need-by date, and the decision it blocks, for when you need every unanswered question at IC to be a deliberate risk rather than a surprise.
---

# Information Gap Log

## When to use

Use this skill from the moment the CIM teardown produces its diligence priority list, and keep it live until IC papers circulate. The issues log records findings -- things you know and do not like. The gap log records the inverse: assumptions the bid depends on that no document, call, or advisor has yet confirmed. A gap arriving at IC unclosed is acceptable. A gap arriving unnamed is not.

## What it does

Maintains one register of open gaps, each carrying the assumption at risk, the evidence that would close it, the named owner, the need-by date, the decision it blocks, and its effect on QoE EBITDA and turns of entry multiple if it resolves against the base case.

## Method

### Step 1 -- Derive gaps from the thesis, not the data room index

Work backwards from the value drivers in the model. For each line carrying material EBITDA -- a pricing uplift, volume growth, a cost programme, a contracted renewal -- ask what document would prove it and whether that document exists. Gaps found this way are few and load-bearing; gaps found by working through an index are numerous and mostly irrelevant.

### Step 2 -- Quantify the gap before you chase it

Express every gap as EBITDA at stake and its equivalent in turns of the entry multiple. Set a materiality threshold at the outset -- a quarter of a turn is a defensible default -- and put below-threshold items in a de-minimis section nobody is asked to chase. **Unquantified gaps are not gaps; they are anxieties.**

### Step 3 -- Assign a named owner, a need-by date, and the decision blocked

Owners are individuals, not firms: "Ward, commercial VP", not "the CDD provider". Date each gap by backward pass from IC, allowing time for the answer to be modelled rather than merely received -- anything feeding the returns model is due before model freeze. Then name what cannot be settled until it closes: the bid, the leverage quantum, an SPA protection, or a condition precedent. **A gap that blocks no decision should be deleted, not tracked.**

### Step 4 -- Grade by consequence, not by curiosity

**Deal-shaping:** could move the bid by more than half a turn or trigger a pass. **Price-forming:** moves the bid inside the threshold band. **Confirmatory:** expected to support the base case, material only if it surprises. Deal-shaping gaps go to the deal partner weekly, in writing.

### Step 5 -- Close each gap in one of four ways

Answered (evidence in, model updated); priced (evidence unobtainable, base case haircut and the haircut stated); accepted as a stated risk (carried to IC with probability and impact); or re-scoped (the assumption removed from the model). Silence is not a closure state.

### Step 6 -- Carry the residual into the IC memo

Any gap open at papers goes into the memo with its grade, owner, quantified impact, and why it could not be closed. That section converts an open question into a risk the committee accepted knowingly.

## Inputs

- CIM teardown priority list and management assertions tracker
- Returns model with the EBITDA build shown by driver
- Workstream owner list and executed advisor scopes
- IC date, model freeze date, exclusivity expiry
- Data room index and outstanding request list

## Output format

- Header: entry count by grade, threshold used, model freeze date
- One entry per gap: assumption, evidence required, owner, need-by date, decision blocked, EBITDA and turns at stake, grade, status
- De-minimis section: below-threshold gaps, listed and not chased
- Weekly delta: gaps opened, closed and re-graded since last circulation
- Residual section drafted in prose for the IC memo

## Example

**Fictional target: Meridian Fluid Systems, industrial pumps.** QoE EBITDA $48.0m, proposed entry 10.5x, implied EV $504.0m. Threshold set at a quarter of a turn -- $12.0m of EV, or $1.14m of EBITDA at the 10.5x entry.

**Entry G-04.** Assumption: the FY26 plan carries $3.6m of EBITDA from a 4% price uplift on 40% of the installed base. Evidence required: renewal dates and price-change clauses for the top 60 contracts, none of which are in the data room. Owner: Ward, commercial VP. Need-by: model freeze. Decision blocked: the bid. At stake: $3.6m of EBITDA -- 7.5% of QoE, $37.8m of EV, 0.79 turns, over three times threshold. Grade: deal-shaping.

The judgement call is what to do if the contracts never arrive. Uplifts of this size are rarely closed by assertion, so the disciplined route is to price the gap out -- model it at nil and bid off $44.4m -- not carry $3.6m of unevidenced EBITDA into committee.
