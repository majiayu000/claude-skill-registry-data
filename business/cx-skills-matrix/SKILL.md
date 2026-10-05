---
name: cx-skills-matrix
description: Use to map support capabilities, plan cross-training, and size multi-skilling against real proficiency and routing cost — not headcount arithmetic. Trigger for "skills matrix", "who can handle what", "cross-training plan", "multi-skill our team", "build a capability map", routing coverage gaps, or deciding whether to train agents on another queue.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Skills matrix and multi-skilling

The usual skills matrix is a spreadsheet of checkboxes: who has been *trained* on what.
That tells you almost nothing about who can *handle* what at the level your customers
and SLAs require. Worse, it is read as free capacity — "we have 40 people and 60
skills, so we have coverage" — and routing is built on that fiction until quality and
handle time move in the wrong direction.

**Multi-skill is not free capacity.** Every additional skill on an agent's profile
carries proficiency decay, context-switch cost, and a training-and-nesting bill. The
matrix exists to make those costs visible before you commit.

## Step 1: define the capability units

List capabilities at the granularity routing actually uses — not org-chart labels.

| Level | What it means | Routing implication |
| --- | --- | --- |
| **Aware** | Can recognise the contact type; must transfer | Do not route here |
| **Supported** | Can resolve with macros, scripts, or escalation path | Route only with backup and low volume share |
| **Independent** | Sustains team-median quality and handle time on this work | Safe for primary routing |
| **Expert** | Handles edge cases; coaches others | Reserve for complex strata and overflow |

**Proficiency must be evidenced**, not self-declared. Options, in descending
defensibility: sustained QA score and handle time on that work type; supervisor sign-off
after a defined nesting period; certification assessment. "Attended training" is not a
level.

State the evidence rule in the matrix header so it does not drift by team.

## Step 2: build the matrix from work, not from people

Start from **contact drivers and channels** (or whatever your routing strata are).
For each stratum, record:

- Volume share and seasonality
- Current primary owners (team, site, or queue)
- Minimum **Independent** headcount needed for coverage (see below)
- Gap: strata with fewer Independents than the minimum

Then populate agents only where evidence exists. Empty cells are honest; checked boxes
without evidence are how you get surprise markdowns on unfamiliar work.

## Step 3: size coverage honestly

Coverage math most teams get wrong:

```
Required Independents ≈ (peak concurrent demand for stratum)
                        ÷ (effective occupancy for that stratum)
                        × (1 + shrinkage + absence buffer)
```

Use **your** occupancy and shrinkage — do not import industry defaults. An agent who is
Independent on five strata is not five agents; concurrent demand across strata
overlaps, but context-switching lowers effective occupancy on each. **Discount
multi-skilled agents** — a common operational rule is to count each additional
Independent skill at 70–85% effective capacity on that skill until you have measured
your own switch cost. State the discount you used; if you have no measurement, use a
conservative discount and plan to replace it with data.

**Supported does not count toward primary coverage.** It counts toward overflow and
business continuity only.

## Step 4: cross-training ROI

Before approving a cross-training wave, compare:

| Cost | How to estimate |
| --- | --- |
| Training and nesting time | Classroom + shadow hours × loaded rate |
| Proficiency ramp | Weeks at below-median output on the new skill |
| Dilution on existing skills | If multi-skill agents regress on primary work, add that |
| Routing complexity | More skills = more misroutes until proficiency stabilises |

| Benefit | How to estimate |
| --- | --- |
| Avoided hire or overtime | Only if the gap is persistent, not seasonal |
| Reduced repeat contact / transfer | Measure on strata with high internal transfer today |
| Schedule flexibility | Real only if WFM can actually use the skill in the roster |

**Cross-train when** the gap is structural (driver is not going away), the stratum has
enough volume to sustain proficiency, and the cost is less than the alternative
(hire, outsource, or accept SLA risk). **Do not cross-train** to paper over a routing
bug, a missing macro, or a queue that should be deflected.

## Step 5: routing implications

The matrix is not complete until ops agrees what changes:

- **Primary vs overflow routing** — which skills get offered first at skill-based route
- **Proficiency gates** — block Independent routing until evidence threshold met
- **Decay rules** — if an agent has not worked a stratum in N weeks, downgrade one
  level until re-nested (state N from your volume; do not guess)
- **New-work policy** — who gets the first tickets when a new driver appears

Document these in the matrix appendix. A matrix without routing rules becomes a
training record nobody uses.

## Traps

- **Checkbox matrix** — training attendance treated as capability.
- **Free capacity fallacy** — summing skills across agents as if they stack linearly.
- **Training without nesting** — agents marked Independent after classroom only.
- **Ignoring decay** — skills unused for months still routed as Independent.
- **Cross-training as a substitute for hiring** on sustained volume growth.
- **One matrix for internal and vendor** without noting system-access differences.

## Present results to the user

1. **Capability definitions and evidence rules** — the four levels and what qualifies.
2. **The matrix** — strata × agents (or teams), with proficiency level and date of
   last evidence, not checkboxes.
3. **Coverage gap analysis** — strata below minimum Independent headcount, with peak
   demand and shrinkage assumptions stated.
4. **Multi-skill cost model** — discount applied, nesting weeks assumed, and what you
   did not measure.
5. **Cross-training recommendations** — prioritised list with ROI logic (cost vs
   alternative), not a blanket "train everyone on X".
6. **Routing rule changes** — gates, decay, primary/overflow assignment tied to the
   matrix.
7. **What cannot be concluded** — proficiency inferred from volume alone, or coverage
   calculated without occupancy data.
