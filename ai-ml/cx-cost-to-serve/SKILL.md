---
name: cx-cost-to-serve
description: Use to build a defensible cost per contact and cost to serve by driver, channel or customer segment, for automation business cases and budget decisions. Trigger for "what does a ticket cost us", "cost per contact", "what would automating this save", "cost to serve by segment", building a business case for a bot or a process change, or a savings claim that looks too good.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Cost to serve

Cost per contact is the number that unlocks budget and justifies automation, which is
exactly why it is usually built to reach a conclusion. The two failure modes are a
denominator chosen to flatter and a savings claim that counts money nobody will stop
spending.

## Build the cost base explicitly

State what is in and what is out. The number varies by a factor of two or more
depending on this, so a cost per contact quoted without its basis is not comparable to
anything.

- **Fully loaded agent cost** — salary, employer taxes, benefits, and the paid time not
  spent on contacts (training, meetings, breaks, absence). Using base salary alone
  understates by a large margin.
- **Supervision and support** — team leads, QA, workforce management, training.
  Typically a meaningful share and usually forgotten.
- **Technology** — helpdesk, telephony, per-seat licences, AI or bot spend.
- **Facilities and equipment**, or the remote-work equivalent.
- **Vendor fees** for outsourced volume, on whatever basis the contract uses — which is
  often per-contact or per-hour and therefore not directly comparable to internal
  fully-loaded cost. Normalise before mixing.

Say which are included. "Agent cost only, excluding supervision and technology" is a
fine basis; an unstated basis is not.

## Get the denominator right

- **Count customer contacts, not tickets.** Transfers and reassignments create records,
  not contacts. If one customer issue produced three tickets, the cost of resolving that
  issue is the sum, and dividing by three flatters the per-contact number precisely
  where handling was worst.
- **Decide how repeat contacts count.** Cost *per contact* falls when customers have to
  come back — more denominator for the same problem. **Report cost per resolved issue
  as well**, using identity resolution and repeat-contact linking. The gap between the
  two numbers is the cost of not resolving things first time, and it is often the most
  useful figure in the whole analysis.
- **Exclude automated and spam traffic** from both sides, and say how much that was.

## Allocate by time, not by count

Contacts are not interchangeable. A two-minute password reset and a ninety-minute
dispute cost very different amounts, so allocating total cost evenly across contacts
makes cheap contact types look expensive and expensive ones look cheap — which
systematically points automation at the wrong work.

Allocate on **handle time**, including hold, wrap-up and any downstream back-office
work the contact triggers. Escalated contacts consume time in two or three teams; a
cost model that only counts the front line will understate the exact contacts that are
worth fixing, because escalation-heavy drivers are where the money is.

Where you cannot measure downstream time, say so and mark those drivers as understated
rather than presenting them as complete.

## Automation savings: the part that is usually wrong

A deflection business case typically multiplies contacts avoided by fully-loaded cost
per contact. That number is nearly always too high, for four reasons worth stating
plainly:

**1. Fixed costs do not fall with volume.** Licences, tooling, supervision and
management are largely fixed in the short run. Only the variable portion — mostly
agent time — is realisable, and only in step changes.

**2. Headcount is lumpy and its reduction is a decision.** Deflecting 8% of volume does
not remove 8% of a team. Savings are realised when a role is not backfilled, a shift is
retired, or a vendor's committed volume is renegotiated. **Say what specific decision
would realise the saving**, and if none is planned, the saving is capacity, not money.
Capacity is a legitimate benefit — absorbing growth without hiring — but it belongs in a
different line.

**3. Automation takes the cheap contacts.** Bots deflect the short, repetitive contacts
first, so the average cost of a *deflected* contact is well below the overall average.
Use the cost of the contacts actually deflected, not the blended average — this alone
often halves the claim.

**4. Deflection is not always avoidance.** A customer who fails with the bot and then
contacts anyway costs more than if they had come straight through. Net the leakage, and
add the cost of the automation itself.

Present the case as **realisable savings, capacity released, and one-off/ongoing cost**,
separately. A single headline saving number invites a challenge that the whole analysis
then fails.

## Where the money actually is

Rank contact drivers by **total cost** — volume × allocated cost — not by unit cost. The
expensive-per-contact drivers are usually rare, and the ranking by unit cost sends teams
to fix work that barely registers in the budget.

Then split the ranked list by remedy, because the owners differ:

- **Removable** — the contact should not have happened. A product or process fix.
  Highest value and usually the slowest.
- **Automatable** — the contact should happen, but not to a human.
- **Cheaper to serve** — better tooling, knowledge or routing.
- **Irreducible** — complex, regulated or relationship work that should stay human.

## Traps

- **Comparing your cost per contact to a published benchmark.** Bases differ wildly and
  almost none are stated. Compare against your own trend and your own segments instead.
- **Averaging across channels.** Voice, chat and email costs differ severalfold. Never
  present a blended figure as a single number.
- **Ignoring chat concurrency.** Agent time per chat is a fraction of wall-clock; using
  wall-clock overstates chat cost badly.
- **Counting the same time twice** across front line and back office.
- **Treating quality as free.** A cost reduction that raises repeat contact raises total
  cost. Always show cost per resolved issue beside cost per contact.

## Present results to the user

1. **The cost base** — what is in, what is out.
2. **Denominator definition** — contacts vs tickets vs resolved issues.
3. **Cost per contact and cost per resolved issue**, by channel, never blended.
4. **Drivers ranked by total cost**, with volume and allocated time visible.
5. **The remedy split**, with owners.
6. **For any automation case**: realisable savings, capacity released, and cost, as
   three separate lines — plus the specific decision that would turn capacity into
   money.
7. **What is understated**, especially unmeasured downstream and back-office time.
