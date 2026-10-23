---
name: sales-support
description: "Use when engineering is pulled into a sales conversation (a proposal, a scoping call, a demo, a deadline question, an RFP): keeping a commitment made in the room buildable afterwards."
---

# sales-support

Business layer (`business/README.md`). A sentence said in a sales meeting becomes an engineering
constraint, and unlike a ticket it arrives with a signature under it.

The recurring failure isn't people lying. It's a question asked in a room where nobody could validate
the answer, answered helpfully, and never revisited. This block is about not being the person who
answered.

## When
When engineering is asked into: a proposal or RFP response, a scoping call, a demo, a feasibility or
deadline question, a technical due-diligence exchange.

## Steps

### 1. Understand the problem before scoping the solution
1. **Ask what happens today** and what it costs them. A request phrased as a feature ("we need an
   export") is a solution someone already chose; the problem behind it often has a cheaper answer we
   already ship.
2. **Find out who actually has the problem** versus who's in the meeting. They differ, and building for
   the wrong one is expensive and only discovered at rollout.
3. **Write down what you didn't get an answer to.** Unknowns silently become assumptions, and
   assumptions become scope.

### 2. Estimates: separate the number from the promise
This is the part that causes the most damage, and it's mostly one distinction.

1. **An estimate is not a commitment.** State which one you're giving. An estimate can be wrong without
   anyone having failed; a commitment can't.
2. **Never give a date in the room** for anything non-trivial. Give a range with what it depends on, and
   come back with a date after the people who'd build it have looked. "I'll confirm tomorrow" costs
   nothing; a date invented under social pressure costs a quarter.
3. **Estimate the work, not the wish.** If the number gets pushed back on, what changes is the scope,
   not the number. An estimate that moves because someone frowned was never an estimate.
4. **Name the assumptions the number rests on** (existing data available, no migration needed, one
   integration not three). This is what makes it revisable later without it looking like backtracking.
5. **Unknowns get spiked, not guessed.** Anything nobody has done before gets a small time-boxed
   investigation before it gets a number, and saying so is a legitimate answer.
6. **Don't let an estimate become a discount lever.** Compressing an estimate to win a deal moves the
   cost to delivery, where it reappears as overtime or defects.

### 3. Demos: what you show is what you promised
1. **Demo what exists.** A mockup shown in a demo is remembered as a feature, whatever was said out
   loud.
2. **Say explicitly when something isn't built yet**, and don't show it unless that's understood.
3. **Prepare with realistic data.** A demo on empty or obviously fake data undersells working software;
   a demo on real customer data is a data-protection incident (`business/data-protection`).
4. **Know what breaks.** Run the exact path beforehand: the demo failure that damages trust is the one
   that surprises the presenter.
5. **Never promise a feature to close a moment.** If it's genuinely worth committing to, it goes through
   the normal decision, in writing, afterwards.

### 4. Written answers
1. **Answer what was asked**, then note what wasn't asked but matters.
2. **"Not currently" is a complete answer**, and it's stronger than a vague yes that unravels in
   implementation.
3. **Anything committing us contractually — an SLA, a data location, a certification, a deadline — goes
   to whoever owns that**, never answered from the keyboard.
4. **Keep the written trail**: what was asked, what we answered, what we assumed. Delivery will need it,
   and so will the renewal.

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the problem stated separately from the requested
solution, estimates labelled as estimates with their assumptions, a list of what was committed and by
whom, and the contractual questions routed to their owner.

## Guardrails
- **Never commit a date the people who'd build it haven't seen.**
- **Never present an unbuilt thing as existing**, in a demo or in writing.
- **Never answer an SLA, certification, data-residency or liability question yourself.**
- Never use real customer data in a demo environment.
- **Pressure in the room is not new information.** If the answer changes because the meeting got
  uncomfortable, that's the signal to leave the room and confirm later, not to revise.

## Origin
Assembled from public sources: standard discovery-before-solution practice and the widely documented
estimate-versus-commitment distinction. Written **without internal sales expertise** and with no
access to pricing, contract terms or commercial policy — all of which are deliberately out of scope
under rule C. The estimation section reflects internal practice already settled on the engineering
side (estimates in points, unknowns spiked rather than guessed, scope moves instead of the number),
generalised here with no project or client named.
