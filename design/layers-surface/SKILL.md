---
name: layers-surface
description: Audits existing surface against lower-layer decisions and produces a surface decision inventory — vocabulary, object consistency, completeness, feedback, hierarchy, accessibility
---

# /layers-surface

*Assumes `/layers-intro` has been loaded for framework context.*

The surface layer is where everything decided in the layers below becomes something a person actually encounters: words, sounds, visuals, physical affordances, motion, feedback. It is the most medium-specific layer, but the most important decisions to make first are universal — they apply regardless of whether the surface is a screen, voice interface, physical device, or service touchpoint.

Surface violations are often symptoms of deeper problems. This skill distinguishes between issues you can fix at the surface and issues that require revisiting a lower layer.

**Decisions this layer needs to make:**
- Does the surface honour the vocabulary and objects from the conceptual model?
- Is every affordance from the breadboard present — and is there surface content with no model behind it?
- Does the surface convey the right emotional register for the jobs users are doing?
- How does the user know what happened, what's in progress, and what went wrong?
- What is most prominent, and should it be?
- Is every piece of information accessible to the users who need it?

**Methods:**

| Method | When |
|---|---|
| **Working directly in the real medium** (code, production UI) | When you need real feedback on real interactions. Avoids the gap between how something looks in a mockup and how it behaves in use. |
| **High-fidelity mockups** (Figma, etc.) | Exploring layout, visual hierarchy, and visual form — especially for novel patterns or stakeholder alignment. |
| **Design system / component library** | When the product has established components and tokens. Surface decisions must extend the system, not contradict it. |
| **Style tiles** | Establishing visual language early without committing to layout. Faster than high-fi for initial tone alignment. |
| **Prototypes** | Testing interaction behaviour — transitions, feedback timing, flow — that static mockups can't convey. |
| **Copy-first** | When language is the primary design material — messaging, onboarding, error states. Write copy before designing the container. |

**Quality signals — what good surface decisions look like:**
- Every term matches the ubiquitous language from the conceptual model
- Every object has a consistent representation across contexts — not a shapeshifter, not masked
- Every affordance from the breadboard is present; every surface element has a model behind it
- Emotional register matches the emotional and social jobs from user needs
- Error messages do three things: diagnose (what happened), explain (why), recover (what to do next). "Something went wrong" fails all three.
- Prominence reflects importance — what the flow needs the user to notice is what stands out
- Accessibility decisions are explicitly made, not left as defaults

---

## Guided session

This skill has two parts. Tell me what you need:
- **Audit** — assess existing surface work against lower-layer decisions (Phases 1–5)
- **Decision inventory** — work through open surface decisions (Phases 6–10)

*Describe what you have, or say "guide me" to start.*

Ask: *"Where should I capture the work from this session?"* (see `/layers-intro` for options)

Ask:
1. What product or feature are we working on?
2. What medium — screen UI, voice/conversational, physical, service touchpoints?
3. What do you have from the layers below? Conceptual model (objects + ubiquitous language)? Breadboard or flow? Job stories including emotional/social jobs?

---

## Part 1 — Audit

**Phase 1 — Frame the surface**

Does existing surface work exist — working code, deployed UI, copy, visual designs? Or is the surface not yet started? If not yet started, skip to Part 2.

**Phase 2 — Vocabulary and language**

Take the ubiquitous language list from the conceptual model. Ask the designer to share surface copy — labels, headings, button text, error messages, notifications, help text.

Check every term. Flag:
- **Direct violations** — a model term used incorrectly or inconsistently ("Account" in one place, "Workspace" in another)
- **Unlisted terms** — words on the surface not in the ubiquitous language. New terms to add to the model, or surface noise?
- **Tone misalignments** — technically correct but tonally wrong for the emotional/social jobs

For each violation: surface fix (rewrite copy) or deeper fix (update the conceptual model vocabulary)?

**Phase 3 — Object consistency**

For each object in the conceptual model: where does it appear on the surface? In how many forms?

- **Shapeshifters** — same object in significantly different visual or structural forms across contexts
- **Masked objects** — the object appears in a form where a user couldn't recognise it as that object type

For each: is this a surface decision (establish consistent treatment) or a conceptual model problem (the object's identity is unclear even in the model)?

**Phase 4 — Completeness check**

Take the breadboard. For each place and affordance:
- Is every affordance from the breadboard present in the surface?
- Is there surface content with no corresponding breadboard element?

Additions that weren't in the breadboard are often interaction-layer decisions that slipped through — flag them and recommend revisiting `/layers-interaction-flow`.

**Phase 5 — Emotional register**

Return to job stories, particularly emotional and social jobs.

*"What emotional job is the user doing here — not just the functional task, but how they want to feel?"*
*"What social job is in play — how do they want to be perceived?"*

Common misalignments:
- Surface emphasises the product's benefit ("we get a referral") over the user's job ("I help a colleague")
- Copy frames an interaction transactionally when the user's job is relational
- Tone feels expert/clinical when the user needs to feel reassured or confident

---

## Part 2 — Decision inventory

**Phase 6 — Feedback and errors**

For each significant action and state transition:
- *"How does the user know their action worked?"*
- *"How does the user know something is in progress?"*
- *"How does the user know something went wrong, and what to do about it?"*

Error messages must diagnose, explain, and tell the user what to do next. Flag every error state that doesn't meet all three. Produce a decision for each gap: *"We need to decide how to communicate [X] to the user. The options are [Y]."*

**Phase 7 — Hierarchy and emphasis**

For each key place:
- *"What is the most important thing a user needs to notice or act on here?"*
- *"Does the current surface make that thing most prominent?"*
- *"Is anything visually prominent that shouldn't be?"*

These are medium-agnostic decisions first (what should be primary) before they become medium-specific (how to make it primary visually, audibly, or tactilely).

**Phase 8 — Accessibility**

Flag relevant considerations for the declared medium:
- **Screen UI:** colour contrast, text sizing, touch targets, keyboard navigation, screen reader labels for interactive elements and images, focus management across flow steps
- **Voice/conversational:** all information conveyed verbally (no "click the button on the left"), error recovery without visual context
- **Physical:** reachability, tactile differentiation, visibility in varied lighting, operation without fine motor precision

Produce a list of accessibility decisions: *"We need to decide how [X] will be accessible to users who [Y]."*

**Phase 9 — Consistency**

- Are similar things treated similarly? (Same actions look and behave the same; same object types represented consistently)
- Are different things treated differently? (Primary vs. secondary, destructive vs. safe)
- Does this surface conform to the conventions of its medium? Violating platform norms is a decision with a cost — sometimes worth it, always intentional.

Distinguish: internal inconsistencies (fix within the surface) vs. convention violations (deliberate choice or oversight — decide which).

**Phase 10 — Open decisions**

Produce a consolidated list of all surface decisions still to make:
- **Cross-layer issues to resolve first** — root is in a lower layer; listed separately; require revisiting the relevant skill before the surface can be right
- **Surface decisions to make now** — what's the decision? what are the options? what constraints apply (from lower layers, the medium, brand/consistency)?
- **Deferred** — don't need to be made now but should be tracked

---

### Completion

Produce:
1. **Audit findings** — vocabulary violations, masked/shapeshifting objects, completeness gaps, emotional register misalignments — each categorised as surface fix or deeper-layer issue
2. **Decision inventory** — all open surface decisions, grouped and prioritised
3. **Cross-layer issues** — things to resolve at a lower layer before the surface can be right
4. **What's working** — surface decisions already made well; don't lose these in revision

Close with: *"The surface is the layer users encounter. Everything decided below either gets honoured here or undermined here. Revisit this skill after any significant change to the conceptual model or interaction structure."*
