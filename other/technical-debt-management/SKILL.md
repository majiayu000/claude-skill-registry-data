---
name: technical-debt-management
description: "Debt that exists only in engineers' heads cannot be prioritised, funded, or"
---

# Technical Debt Management (Verbose)

## Core Patterns

### The Debt Register

Debt that exists only in engineers' heads cannot be prioritised, funded, or
argued for. A register makes it a portfolio of items with carrying costs.

The financial metaphor is load-bearing, so use it precisely:

- **Principal** — the one-off cost to fix it properly. An estimate in
  engineer-days, produced the same way you estimate features.
- **Interest** — the recurring cost of not fixing it. Extra effort per change in
  the affected area, plus incident cost, plus onboarding drag. This is the number
  that decides priority, and the one teams usually skip.
- **Trigger** — the condition that makes paydown due. Without one, every item
  stays "someday".

A complete entry:

> **DEBT-114 — Order totals recomputed in three places**
>
> **Where:** `checkout/pricing.py:340-520`, `admin/order_edit.py:88-210`,
> `jobs/reconcile.py:55-190`. Three implementations of discount stacking and tax
> rounding that have drifted apart.
>
> **How it happened:** admin editing shipped under a deadline in 2024-03 and
> copied the checkout logic rather than extracting it; the reconciliation job
> copied the admin version a year later. Prudent-deliberate at step one, then
> reckless-inadvertent at step two.
>
> **Interest:**
> - Pricing rule changes cost ~3 engineer-days instead of ~1. Six such changes in
>   the last 12 months → **~12 engineer-days/year**.
> - 2 of the last 5 sev-2 billing incidents were caused by the three paths
>   disagreeing. Direct incident cost ~6 engineer-days plus ~$40k in manual
>   refund correction.
> - New engineers take an extra half-day to learn which path is authoritative.
>
> **Principal:** ~8 engineer-days. Extract a `PricingEngine`, run it in shadow
> mode against all three call sites for two weeks comparing outputs, then migrate
> and delete the duplicates.
>
> **Trigger:** the Q3 multi-currency epic touches pricing. Pay down before it
> starts, or every ticket in that epic costs roughly triple and a fourth copy
> gets created.
>
> **Growth:** interest rises with each new call site and each currency.
>
> **Owner:** payments team. **Reviewed:** 2026-06-02.

The estimates need to be defensible, not exact. Derive interest from evidence you
already have: `git log` frequency on the files, cycle time on tickets touching
that area versus the team median, incidents tagged to the component, and the
review comments where people ask "which one of these is real?".

Keep the register small — 15 to 30 live items. A register with 400 entries is a
graveyard nobody reads, and the act of pruning it is itself a prioritisation.

### Fowler's Quadrant, Applied

The four cells have genuinely different remedies, which is the whole reason to
classify.

|  | **Deliberate** | **Inadvertent** |
|---|---|---|
| **Prudent** | "We ship the hardcoded tax table to make the launch date and replace it in Q3." | "Now that we understand the domain, this aggregate boundary is in the wrong place." |
| **Reckless** | "There's no time for tests, merge it." | "What's a repository pattern?" |

**Prudent-deliberate** is legitimate engineering. It is a loan taken knowingly to
buy time-to-market. It only stays prudent if the register entry and the trigger
are written *at the moment of the decision* — that is the difference between a
loan and a default. In review: "fine, but the ticket and the trigger go in this
PR description."

**Prudent-inadvertent** is what learning looks like and cannot be prevented by
process. You did the reasonable thing with the knowledge available; the domain
turned out to be shaped differently. The remedy is to refactor when the next
change makes it cheap, not to hold a retrospective about it.

**Reckless-deliberate** is the dangerous cell, because it is a *process* failure
wearing a technical costume. Somebody decided the schedule mattered more than the
consequences. Fixing the code without fixing the pressure guarantees a repeat
next quarter. The escalation is about capacity and dates, not about tests.

**Reckless-inadvertent** is a capability gap. Refactor tickets do not address it —
pairing, review standards and design discussion do. Punishing it hides it; the
code keeps arriving, just less visibly.

Two useful consequences. First, in a retro, arguing about which cell an item is
in is time well spent, because it decides who acts. Second, a team whose register
is mostly reckless-deliberate has a management problem, and no amount of
refactoring budget will fix it.

### Funding Paydown

**The boy-scout rule is necessary and insufficient.** "Always leave the code
cleaner than you found it" handles debt at the scale of a confusing variable
name, a missing test, or an extracted function. It cannot handle structural debt:
nobody extracts a service, splits a 4,000-line module, or replaces an ORM
opportunistically while fixing a bug. And they shouldn't — a bugfix PR carrying a
large unrelated refactor is genuinely harder to review and riskier to roll back,
so reviewers push back correctly, and the rule quietly caps itself at the trivial.

Structural paydown needs budget:

| Model | Mechanism | Works when | Fails when |
|---|---|---|---|
| Percentage allocation | 15–20% of each sprint's capacity to register items | Debt is spread and continuous | Allocation is unprotected and gets cut |
| Debt sprint | One full sprint per quarter | A large item needs contiguous focus | It becomes the excuse to defer all paydown between sprints |
| Rider on feature work | Pay the debt in the area a feature touches, budgeted in that feature's estimate | Debt is localised to the feature's path | Feature estimates get squeezed, and the rider is the first thing dropped |
| Dedicated crew | A standing team on platform and debt | Debt is systemic and cross-team | The rest of the org concludes debt is somebody else's job |

The percentage allocation is the usual default, and it works only with four rules
enforced:

1. **Paydown items live on the same board**, estimated the same way, visible to
   the same stakeholders. Invisible work is unfundable work.
2. **The allocation is protected during crunch.** This is counterintuitive and
   non-negotiable: crunch is largely caused by debt, so suspending paydown during
   crunch guarantees more crunch. Suspend it once and it never returns.
3. **Never schedule paydown last.** Whatever is last in a sprint is what gets
   dropped. Put it first, and the feature work absorbs the overrun instead.
4. **Every completed item reports the interest it removed.** "Pricing changes now
   take 1 day, down from 3; two months of tickets confirm it." This is what buys
   the allocation for next quarter — without it, the budget is a matter of faith
   and will be cut by the first leader who doesn't share it.

### When Not to Pay Debt Down

Refactoring only returns value through future changes to the code. If there are
no future changes, the return is zero regardless of how bad the code is.

Do not pay down when:

- **The code is scheduled for deletion or replacement** within roughly two
  quarters. Refactoring something about to be deleted is pure loss.
- **It is stable and untouched.** One commit in three years, no incidents, no
  planned work. Ugly and quiet is not debt — it charges no interest. It may still
  be worth documenting so nobody "improves" it.
- **Payback exceeds the remaining lifetime.** A 20-day refactor saving 2
  engineer-days/year on a system with 3 years left loses 14 days.
- **The area is frozen for compliance or contractual reasons**, so changes carry
  a recertification cost that dwarfs the interest.
- **You cannot name the interest.** If nobody can say what it costs per change,
  either the analysis hasn't been done or the item is aesthetic preference. Both
  mean: not yet.

A rough ranking function:

```
priority ≈ (interest_per_change × changes_per_year + incident_cost_per_year)
           / principal
```

Change frequency is the dominant term. Identical duplication in a file touched
weekly and a file touched annually differ by roughly 50× in carrying cost. This
is why "refactor the worst code" is the wrong instinct and "refactor the code you
keep having to touch" is the right one. Overlaying `git log` change frequency on
complexity metrics finds the real targets in about an hour.

Be equally clear about what is *not* debt: code you dislike stylistically, an
older-but-working library with no CVEs, and a design you would do differently
today but never need to change. Calling those debt inflates the register and
devalues the entries that genuinely cost money.

### Making the Cost Visible to Non-Engineers

Executives do not decline to fund debt paydown because they don't care about
engineering. They decline because "the auth module is a mess" is not a
decision-shaped input. Convert every item to their units: money, time, risk,
delivery predictability.

| Engineering framing | Funder framing |
|---|---|
| "Pricing logic is duplicated three times" | "~12 engineer-days/year of rework and 2 of our last 5 billing incidents; ~8 days to fix; pays back in ~8 months" |
| "Checkout has no integration tests" | "Change failure rate is 28% in checkout versus 9% elsewhere; roughly one customer-visible checkout incident per month" |
| "Our release process is manual" | "6 engineer-hours per release × 40 releases/year = 240 hours, and it is why we can't release on a Friday" |
| "We're three majors behind on the framework" | "14 unpatched CVEs, blocks the SOC 2 control we committed to, and the upgrade cost roughly doubles per major version we fall behind" |

The sentence that works is always the same shape: **"This costs X per quarter and
is growing. It costs Y once to stop it. It pays back in Z months."** That is a
capital allocation question, and capital allocation is a thing executives are
good at.

Two amplifiers. **Show the compounding curve** for debt whose cost grows —
dependency drift, migrations that get harder as data volume rises, coupling that
worsens with each new caller. A flat cost is a trade-off; a rising cost is a
deadline. And **tie debt to delivery predictability**, since that is usually what
leadership feels most acutely: "the reason estimates in billing are unreliable is
that every change touches three code paths" connects debt to something they were
already unhappy about.

Finally, report paydown outcomes in the same units you used to request it. A
quarterly line — "we spent 40 engineer-days on paydown and removed an estimated
90 days/year of recurring cost" — is what turns the allocation from an annual
argument into a standing budget line.

## Common Anti-Patterns

❌ **A debt backlog with no estimates and no interest figures.** It is a list of
complaints; nothing on it can be prioritised against a feature.
✅ Every entry carries principal, interest, trigger and owner.

❌ **"We'll clean it up after launch" with no ticket.** Post-launch capacity goes
to post-launch problems, and the debt becomes permanent and undocumented.
✅ The register entry and trigger are written in the same PR that takes on the debt.

❌ **Relying on the boy-scout rule for structural debt.** It caps out at renaming
things, and large refactors in bugfix PRs get rejected in review — correctly.
✅ Budget an explicit, protected allocation for structural items.

❌ **Cutting the paydown allocation when the schedule slips.** Debt is a major
cause of the slip, so this accelerates the problem.
✅ Protect the allocation precisely when pressure is highest.

❌ **Refactoring the ugliest code rather than the most-changed code.** Carrying
cost is interest × frequency, and frequency dominates.
✅ Rank with change frequency from `git log` overlaid on the register.

❌ **Proposing a rewrite instead of incremental paydown.** Rewrites re-derive
years of undocumented behaviour, and the old system keeps changing underneath.
✅ Strangle incrementally with measurable checkpoints and shadow comparison.

❌ **Arguing debt on aesthetics or "best practice".** Nobody outside the team can
evaluate the claim, so it loses to anything with a number.
✅ Argue in engineer-days, incidents, change failure rate and CVEs.

❌ **Fixing reckless-deliberate debt without addressing the schedule pressure.**
The same pressure produces the same debt next quarter.
✅ Escalate the process cause; treat repeat recklessness as a capacity problem.

❌ **Refactoring a module that is being replaced next quarter.** All cost, no return.
✅ Check remaining lifetime before scheduling any paydown.

❌ **Never reporting what paydown achieved.** The budget survives on goodwill and
dies with the next reorg.
✅ Publish removed interest per item in the same units used to request funding.

## Technical Debt Checklist

- [ ] A register exists, is under ~30 live items, and is reviewed quarterly
- [ ] Each entry names what, where, principal, interest, trigger and owner
- [ ] Interest is derived from evidence (change frequency, cycle time, incidents), not intuition
- [ ] Each item classified in Fowler's quadrant, with the remedy matched to the cell
- [ ] Prudent-deliberate debt gets its register entry at the moment of the decision
- [ ] Recurring reckless-deliberate debt escalated as a process and capacity issue
- [ ] An explicit paydown allocation exists (typically 15–20% of capacity)
- [ ] The allocation is protected during crunch and is never the last item in the sprint
- [ ] Paydown items sit on the same board and are estimated like features
- [ ] Items ranked by interest × change frequency ÷ principal, not by how bad the code looks
- [ ] Remaining lifetime checked before scheduling paydown; doomed code left alone
- [ ] Stable, untouched, unlovely code explicitly excluded from the register
- [ ] Compounding items flagged with their growth curve
- [ ] Each item translated into money, risk, or delivery predictability for funders
- [ ] Large paydown done incrementally with shadow comparison, not as a rewrite
- [ ] Removed interest measured and reported after each completed item
