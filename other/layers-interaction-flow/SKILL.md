---
name: layers-interaction-flow
description: Maps interaction structure and flow — produces breadboard notation with edge cases, failure paths, and open decisions
---

# /layers-interaction-flow

*Assumes `/layers-intro` has been loaded for framework context.*

The interaction structure and flow layer defines how a person interacts with the product: the places they navigate, the affordances available, the content presented, and the flow between states. It sits above the conceptual model (which defines *what exists*) and below the surface (which defines *how it looks*).

**Decisions this layer needs to make:**
- What are the distinct places this flow moves through?
- What can the user do in each place, and where does each action take them?
- What content does each place need to show?
- What happens on failure paths, empty states, and edge cases?
- Is the flow as simple as it can be while still serving the job?

**Methods:**

| Method | When |
|---|---|
| **Breadboarding** (Ryan Singer / Shape Up) | Default for most flows. Text-based notation that forces interaction logic to be evaluated before visual design makes changes feel expensive. |
| **User story mapping** (Jeff Patton) | Complex product, many user types, planning incrementally. Maps activities → tasks → stories across a timeline. |
| **Task analysis** | Redesigning an existing flow. Decompose the current task to find where friction, errors, and workarounds concentrate. |
| **Service blueprinting** | Flow spans multiple channels or involves backstage operations (staff, systems, third parties) that affect the user experience. |
| **Critical User Journeys (CUJs)** | Deciding which flow to work on. A CUJ is the minimal path to realise core product value — types: high-traffic, high-revenue, or metric-critical. |

Default: **breadboarding**.

**Breadboard notation:**
```
Place name
- affordance → destination place
- affordance → destination place
[ content shown in this place ]
```

**Quality signals — what good looks like:**
- Every affordance has a named destination
- Failure paths are breadboarded — not left as afterthoughts
- Empty, loading, and post-action states are defined
- No broken objects — an object's attributes and actions are available together, not scattered across screens with no cross-linking
- No isolated objects — relationships from the conceptual model are visible and navigable in the flow
- The flow is minimal: more than 5–6 places for a single job story is a signal to look for what can be collapsed

---

## Guided session

*Tell me which user journey you're designing for, or say "guide me" to start a breadboarding session.*

Ask: *"Where should I capture the work from this session?"* (see `/layers-intro` for options)

Check the layer below: *"Do you have a conceptual model — defined objects, relationships, and vocabulary — to work from? Or are we designing the flow without a settled model beneath it?"* Flows built before the conceptual model is stable often need to be revisited.

Ask: *"Which user journey or job story are we designing for?"* A breadboard is always for a particular user in a particular situation doing a particular job.

---

**Phase 1 — Frame the flow**

1. Which job story does this flow serve?
2. Where does the user start? What situation are they in?
3. What does success look like — what has the user achieved when the flow completes?
4. New flow, redesign, or extension of an existing flow?

If redesigning: describe the current flow first, even roughly. Existing flows reveal decisions already made — some deliberately, many not.

**Phase 2 — Identify the places**

*"What are the distinct places — screens or states — this flow moves through? Don't think about layout yet. Just name the places."*

Ask: are any of these the same place in a different state? Should they be separate places or one place with states? Are there places elsewhere in the product that this flow connects to?

Naming places is itself a design decision. Descriptive, user-meaningful names: "Referral dashboard" not "Page 3."

**Phase 3 — Map affordances and connections**

For each place, work through what the user can do there and where each action leads. Use the breadboard notation above.

For each affordance: where exactly does this go? What happens if it succeeds? Fails? Is it always available, or only in certain conditions?

Conditions — when affordances are or aren't available — are often where the real design decisions hide.

**Phase 4 — Walk through the flow**

Narrate as the user: *"I'm a user who [job story situation]. I arrive at [starting place]. I see [content]. I want to [motivation]. So I [affordance]..."*

Walk the full successful path. Then walk the edges:

- *Empty states:* What does this place look like before any data exists? Often the first thing a new user sees.
- *Loading / async states:* What does the user see while data fetches or an action processes?
- *Post-action state:* After submitting, what happens? Stay here, redirect, inline confirmation? If redirected to a list — does it immediately show the change? If there's lag, could it look like the action didn't work?
- *Optimistic vs. pessimistic:* Show assumed result before server confirms, or wait? State the preference; flag as a named open question if implementation is uncertain.
- *Failure paths:* For each action — validation failure, server error, network disconnection, timeout, concurrent edit. Where does the user go? How do they recover? These are required breadboard steps.
- *Cancel path:* If the user wants to stop halfway, where do they go?
- *Alternative entry points:* Does the flow assume prior state that might not always be true?

Each gap is an unmade design decision. Name it explicitly.

**Phase 5 — Challenge the flow**

- Is there a step users are likely to abandon? Why is it there — is it necessary?
- Are there actions users would expect that the flow doesn't offer?
- Does the vocabulary in the flow match the conceptual model's ubiquitous language?
- Is there a simpler version that serves the same job?

**Check for broken objects:** For each object from the conceptual model appearing in this flow — are its attributes and actions available together, or split across screens with no cross-linking? If split, either consolidate or add explicit connections between the places where its parts appear.

**Check for isolated objects:** For each relationship defined in the conceptual model — does the flow make that relationship visible and navigable? If a relationship exists in the model but is invisible in the flow, either surface it or make a deliberate decision that it doesn't need to be navigable from this flow.

**Phase 6 — Generate the breadboard**

Produce the complete breadboard: all places, all affordances and destinations, content for each place, key conditional states noted.

Generate a flow diagram in left-to-right orientation — flow through time reads left to right. In Mermaid: `graph LR`.

Note: the diagram is for orientation — the text breadboard is the primary document. The diagram loses content and conditional detail.

---

### Completion

Produce:
1. **Job story** — the user need this flow serves
2. **Breadboard** — complete text notation
3. **Flow diagram** — Mermaid `graph LR`
4. **Open decisions** — gaps, edge cases, conditional states not yet resolved
5. **Risks** — dependencies on unsettled conceptual model decisions or surface assumptions

Close with: *"This breadboard defines interaction logic without committing to visual form. Whatever comes next — working in code, building in the real medium, or detailed visual design — make sure the conceptual model beneath this flow is stable first."*
