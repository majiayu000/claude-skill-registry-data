---
name: layers-orient
description: Diagnostic audit across all seven layers — identifies the bottleneck layer and recommends where to focus
---

# /layers-orient

*Assumes `/layers-intro` has been loaded for framework context.*

Orient is a rapid diagnostic. It maps the current state of decisions across all seven layers, identifies the bottleneck — the lowest layer with unresolved or risky decisions — and recommends where to focus next.

It is not a deep dive into any layer. That's what the individual layer skills are for. Orient answers the prior question: *which layer deserves attention most urgently?*

**What it assesses:**
- Whether key decisions have been made at each layer, and how solidly
- Whether decisions treated as solid are actually assumptions
- Which layer is the most foundational with unresolved work, creating risk for everything above

**Quality signals — when orient is done well:**
- The bottleneck layer is specifically named, not vaguely gestured at
- Assumed layers are distinguished from Strong ones — they require different responses
- The recommendation connects to a specific skill with a clear reason

---

## Guided session

*Describe your design situation and what prompted you to pick it up, or say "let's orient" to start.*

Ask: *"Where should I capture the work from this session?"* (see `/layers-intro` for options)

Then ask:
1. What product or feature are you working on?
2. What design challenge are you facing right now?
3. How far along is this work — early exploration, active design, or fixing something in an existing product?

Listen for clues about which layers have already been worked through and which are thin or missing.

---

### Layer audit

Work through each layer with one or two targeted questions. Rate each as:
**Strong** / **Partial** / **Assumed** / **Weak** / **Not started** / **N/A**

**Observed behaviour**
*"What user research do you have? Have you spoken to users, observed them, or have analytics? Or is this mostly based on what the team believes users do?"*

**The domain**
*"How well do you understand the space this product operates in — the real-world concepts, terminology, and how users think before your product enters the picture?"*

**User needs**
*"Can you articulate what users are trying to achieve — not in features, but the underlying job and why it matters? Do you have job stories or equivalent?"*

**Product & service strategy**
*"Do you know which specific user need this work targets and what business outcome it's meant to move? Is the connection between opportunity and business goal explicit, or informal?"*

**Conceptual model**
*"Does the product have a clear model of the objects it works with — the things that exist, how they connect, and what vocabulary you use? Is this shared across the team, or does each person have their own version?"*

**Interaction structure and flow**
*"Do you have a clear picture of the key user journeys — places, steps, decision points? A breadboard, rough flow, working code, or a description you can narrate?"*

**Surface**
*"Is there an existing design system, visual language, or component library this needs to fit into?"*

---

### Decision landscape

Produce the audit as a table:

```
Layer                      | State       | Notes
---------------------------|-------------|----------------------------------------
Observed behaviour         |             |
The domain                 |             |
User needs                 |             |
Product & service strategy |             |
Conceptual model           |             |
Interaction structure      |             |
Surface                    |             |
```

---

### Bottleneck analysis

Identify the **bottleneck layer**: the lowest layer with Weak, Assumed, or Not started state. State it clearly: what decisions are missing, and what risk does that create for the layers above?

Also flag **assumed layers** — layers treated as decided but not verified. Assumptions that look solid are often where the most dangerous decisions hide.

If the designer has a deadline or constraint that changes the calculus, acknowledge it. Sometimes the right move isn't the most foundational one — name that tradeoff explicitly rather than ignoring it.

---

### Recommendation

Recommend a specific skill to run next and why:

- Conceptual model → `/layers-conceptual-model`
- Product strategy → `/layers-product-strategy`
- User needs → `/layers-user-needs`
- Domain → `/layers-domain`
- Interaction structure → `/layers-interaction-flow`
- Observed behaviour → `/layers-observed-behaviour`

Close with: *"Want to run [skill] now, or is there something in this picture to push back on first?"*
