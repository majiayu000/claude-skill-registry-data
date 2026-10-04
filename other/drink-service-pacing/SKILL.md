---
name: drink-service-pacing
description: Run-sheet planning for pre-event drink service from supplied arrival waves, expected service requests, verified menu throughput, staffing, service points, and venue constraints. Use for planned openings, pauses, transitions, capacity shortfalls, venue-reviewed recovery options, or closure. Exclude purchasing, prep scheduling, live queue control, staffing ratios, and invented thresholds.
---

# Drink service pacing

Build a capacity envelope, then place each service state inside it.

The result is a pre-event review artifact. It never directs live service, contacts a venue, sends a guest message, changes staffing, or claims physical verification.

## 1. Confirm the job

Accept requests to build or validate a timed drink-service run sheet before an event.

Keep these adjacent jobs outside the procedure.

- Beverage quantities and purchasing belong to event quantity planning.
- Preparation dependencies belong to a drink-prep schedule.
- Staffing recommendations require the venue or service provider.
- Live queue decisions remain with the on-site service lead.

When a request mixes jobs, retain the run-sheet portion and record the excluded work without performing it.

Complete this step when the requested artifact is confirmed as a pre-event service run sheet and every excluded job is named.

## 2. Freeze the inputs

Record each value with one source label chosen from `venue confirmed`, `provider confirmed`, `measured rehearsal`, `host approved`, or `unknown`.

The capacity envelope requires all of the following.

- Event phases have fixed start and end times.
- Arrival waves include their time windows and expected service-request counts by service route.
- Any conversion from guest arrivals to expected requests is supplied and approved by the host or venue.
- Service points show active intervals, assigned workers, menu scope, and verified effective throughput.
- Menu states identify what is available at each service point during every phase.
- Venue rules state opening, pause, last-call, closure, and exit times where applicable.
- Transition buffers come from the venue, provider, or host.
- Each phase has an owner and a reviewer.
- Recovery options carry an approval state and the party responsible for review.
- Water and alcohol-free availability are specified through guest departure.

Treat a throughput rate as valid only for the stated service point, staffing configuration, active menu, and measurement basis.

If any required value is `unknown`, emit the missing-input stop defined in [the output contract](references/output-contract.md). Do not draft a partial run sheet, estimate the missing value, or continue to capacity arithmetic.

Complete this step when every required input is present, source-labeled, internally consistent, and tied to an event interval. Otherwise, completion is the missing-input stop.

## 3. Build the capacity envelope

Read [the capacity check](references/capacity-check.md) completely before calculating.

Split the timeline whenever demand, menu, staffing, service points, throughput, or service state changes. Reconcile each service route separately unless the venue confirms that demand and capacity are interchangeable across routes.

Label every interval `fits`, `shortfall`, or `uncertain`. Preserve the arithmetic and the source of each operand.

Complete this step when every expected request belongs to one interval and route, every capacity unit uses the same interval, and all interval labels reproduce from the recorded arithmetic.

## 4. Route capacity exceptions

When every interval fits, record that no recovery branch fired and continue.

If an interval has a shortfall, or a planned pause intersects expected demand, read [the recovery review](references/recovery-options.md) completely. Keep unapproved options at `REVIEW REQUIRED`. Recalculate capacity only after the venue or provider supplies an approved option and its verified effect.

An uncertain interval remains a review blocker. Do not convert uncertainty into a pass.

Complete this step when each exception has either an approved, recalculated resolution or an unresolved blocker with an owner and reviewer.

## 5. Sequence service states

Assign one state to every phase.

- `OPEN` means the approved menu and service points operate as specified.
- `LIMITED` means a reviewed menu or routing restriction is active.
- `PAUSED` means ordering is unavailable for a declared interval.
- `CLOSED` means service has ended.

Each state needs a start, end, active menu, service route, transition buffer, and draft communication cue. Assign an owner to every active route inside the state. A cue remains draft-only until the host and venue approve it.

Complete this step when the states cover the full event timeline without overlap or gaps, each active route has an owner, and every transition has a sourced buffer and review status.

## 6. Close responsibly

When alcohol is served, read [the responsible-close branch](references/responsible-close.md) completely. Use only venue-supplied deadlines and maintained official safety guidance.

For an alcohol-free event, record the final service time, water availability, and venue exit time without loading the alcohol branch.

Complete this step when closure timing, continued water and alcohol-free access, departure responsibility, and unresolved local-rule questions are visible in the review packet.

## 7. Emit the review packet

Read [the output contract](references/output-contract.md) completely and render the required sections.

Use `READY FOR HOST AND VENUE REVIEW` only when all inputs are complete, every interval fits after approved changes, and no recovery or local-rule blocker remains.

Use `NOT READY: REVIEW BLOCKERS` when the capacity arithmetic is complete but an approval, recovery effect, or venue decision remains unresolved.

Complete the skill when the packet passes every check in the output contract and no external action has occurred.
