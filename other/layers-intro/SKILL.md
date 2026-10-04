---
name: layers-intro
description: Framework orientation for Layers of Product Design — load this first; provides the context all other skills depend on
---

# /layers-intro

Load this skill at the start of any design session. It provides the framework context that all other `/layers-*` skills depend on.

---

## The framework

**Layers of Product Design** organises design work into seven layers across three zones. Layers have *logical dependency*: lower layers are foundations for upper ones. Weak lower layers create UX debt that propagates upward.

**Reality** — complex, contradictory, evolving. Source of all learning.

**Problem space** — knowledge gathered from reality:
1. **Observed behaviour** — what users actually do
2. **The domain** — concepts, terminology, and mental models that exist independently of any product
3. **User needs** — what we think users are trying to achieve, and why

**Solution space** — deliberate decisions about what to build:
4. **Product & service strategy** — which needs to serve, and what business outcomes to target
5. **Conceptual model** — objects, relationships, states, vocabulary — independent of any interface
6. **Interaction structure and flow** — places, affordances, connections, and flow logic
7. **Surface** — words, visuals, feedback, hierarchy — what users actually encounter

The layers are not a linear process. Enter anywhere — but always check whether the foundations below are sound.

*Inspired by Jesse James Garrett's* The Elements of User Experience *(2000).*

---

## Design is decision-making

Design = making decisions about the form of a solution (Christopher Alexander). Form is the solution; context is the requirements, constraints, and environment it must fit. Good design is good fit.

**Four kinds of progress:**
1. **Making decisions** — resolving something undecided
2. **Uncovering unmade decisions** — discovering what hasn't been decided yet (often more valuable than 1)
3. **Evaluating decisions** — identifying decisions already made that are risky, inconsistent, or wrong
4. **Prioritising decisions** — lower layers are more foundational and carry more risk if wrong

The job of every skill is to help the designer make better decisions — not to make decisions for them.

---

## Principles — apply across all sessions

1. **Decisions, not outputs.** Artefacts are useful only insofar as they represent decisions made or surfaced. Name the decision, not just the diagram.
2. **Uncover before you resolve.** Surfacing decisions the designer didn't know they needed to make is often more valuable than answering the ones they did.
3. **Work at one layer at a time.** Conflating problem space and solution space, or surface and conceptual model, produces confused outputs.
4. **Check foundations before building upward.** Before working on an upper layer, audit the layer below. Flag instability.
5. **The conceptual model is the most neglected load-bearing layer.** Give it more attention than feels comfortable.
6. **Flag bad decisions, not just missing ones.** A decision already made that's risky or inconsistent needs to be named, not worked around.
7. **Steer, don't be steered.** Don't jump to surface output before foundational decisions are made.
8. **Design principles vs. implementation decisions.** Some decisions can be stated without knowing system constraints — *what should happen from the user's perspective*. Others are entangled with implementation: articulate the user experience requirement, form a well-shaped question, and carry it into a design+engineering conversation. Don't force a premature answer.

---

## The time dimension — probe proactively

Temporal decisions are frequently overlooked. They cluster at two layers:

**Conceptual model layer:**
- *Intermediate action states* — does an object pass through transitional states (saving, processing, pending approval) before resolving? Those are model states.
- *Read model lag* — gap between when data is written and when it's visible? Articulate the user need; flag as a named open question for engineering.
- *Relationship temporality* — "all products in Europe" means the group now, or membership as it changes? This is a design decision.
- *Deletion semantics* — archive, trash, hard delete, or regulatory delete? State which and why. Implementation follows.
- *History* — does it matter what an object was in the past? Stating it matters is a design decision.

**Interaction structure layer:**
- *Post-action state* — after submitting, what does the user see? Does a redirected list immediately reflect the change?
- *Optimistic vs. pessimistic updates* — show assumed result before server confirms, or wait? State the preference; flag as an open question if implementation is uncertain.
- *Empty, loading, partial states* — every place has a temporal lifecycle. Design all of them.
- *Error and failure paths* — validation failure, server error, network disconnection, concurrent edit. Required design steps, not afterthoughts.

---

## Failure mode signals

**OOUX object failure modes** (Sophia Prater):
- **Shapeshifter** — same object in significantly different forms across contexts. Surface fix: consistent object treatment. Deeper fix if the model doesn't define the object clearly.
- **Masked** — different object types look identical. Surface fix: distinct visual treatments. Deeper fix if the model doesn't differentiate them.
- **Broken** — object's data and actions scattered across screens with no cross-linking. Interaction structure problem → `/layers-interaction-flow`.
- **Isolated** — objects exist without visible relationships to other objects. Conceptual model problem → `/layers-conceptual-model`.

**Nielsen's heuristics — a root-layer mapping:**
"Match between system and real world" violations almost always root in the conceptual model, not the surface. "User control and freedom" is an interaction structure decision. Patching these at the surface treats symptoms, not causes.

---

## Capturing work

At the start of any design session, ask where to save outputs:

*"Where should I capture the work from this session? The recommended setup is a Markdown file in your project — diagrams are written as embedded Mermaid and render natively in VSCode with the [Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid) extension. Alternatives:*
- *Notion — if you have the Notion MCP connected*
- *Just in the conversation — no file needed"*

Save the session summary to the chosen destination at the end.

When writing Mermaid diagrams, use `<br/>` for line breaks inside node labels — not `\n`, which renders as literal text.

---

## Where to start

- **Not sure where to focus?** → `/layers-orient` — rapid diagnostic across all seven layers
- **Know which layer you're at?** → jump directly to that skill

Skills: `/layers-observed-behaviour` · `/layers-domain` · `/layers-user-needs` · `/layers-product-strategy` · `/layers-conceptual-model` · `/layers-interaction-flow` · `/layers-surface`
