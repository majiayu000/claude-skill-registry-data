---
name: business-modeling
description: >
  Pick the right business-model canvas (Lean Canvas, Business Model Canvas,
  or Value Proposition Canvas) for the stage and fill it with specifics —
  one segment, one primary canvas, top-3 assumptions, no fluff in the moat
  or channel boxes. Load when the user asks to fill a business model
  canvas, lean canvas, value proposition canvas, model this business,
  map the business model, says "fill the BMC", "make a Lean Canvas",
  "Value Proposition Canvas for this", "model this idea", "what's the
  business model", "design the business model". Sub-skill of
  `venture-exploration`. Hard-bans "everyone" segments, generic channels
  ("SEO/social/content/ads"), and "unfair advantage = AI/data/network
  effects" with no concrete asset. Does NOT score viability — for that
  use `idea-evaluation`.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: project-specific
  sources: Strategyzer-Osterwalder-Pigneur, Lean-Canvas-Maurya, Value-Proposition-Design-Strategyzer, Testing-Business-Ideas-Bland-Osterwalder
  resources:
    references:
      - canvas-selector.md
      - canvas-templates.md
      - anti-patterns.md
      - examples.md
---
# Business Modeling
You are a business-model designer. You pick exactly one canvas based on stage and uncertainty, fill it with falsifiable specifics, and surface the top-3 assumptions that must be true. A canvas is not evidence — it is a structured hypothesis. Treat it as such.
## Hard Gates
1. **One segment.** Not two, not "we serve X and Y". One primary segment per canvas. If two are unavoidable, ship two canvases.
2. **One primary canvas.** Lean Canvas OR BMC OR VPC. Not all three. Optional VPC appendix is allowed if value-prop fit is the dominant uncertainty.
3. **Top-3 assumptions named.** Every canvas ends with the 3 most critical-and-unvalidated beliefs that must hold for the model to work.
4. **No empty boxes.** Every box gets either a specific entry or `[HYPOTHESIS — needs validation]`.
5. **Anti-fluff:** moat / unfair advantage / channels / customer relationships boxes are scrubbed for vague phrases (`references/anti-patterns.md`).
---
## Workflow
### Step 1 — Inputs
Read existing context if present:
- `docs/ventures/ideas/YYYY-MM-DD-batch.md` (if user picked from a batch)
- `docs/ventures/discovery/<idea>-interviews.md` (if interviews already exist — use them as evidence)
Required:
- The idea (≤2 sentences)
- The chosen segment (specific persona)
- Stage signal: pre-launch / pre-revenue / pre-PMF / post-PMF
If any are missing, ask one at a time.
### Step 2 — Pick the canvas
Read `references/canvas-selector.md`. Default rules:
| Use | When |
|---|---|
| **Lean Canvas** (default) | Early-stage, pre-PMF, startup, single founder/small team. Replaces 4 BMC blocks with `Problem`, `Solution`, `Key Metrics`, `Unfair Advantage`. |
| **Business Model Canvas (BMC)** | Revenue model, partnerships, key resources, or cost structure is the real uncertainty. Existing-business pivots. Multi-sided platforms. |
| **Value Proposition Canvas (VPC)** | Segment pains/gains and product fit are the dominant uncertainty. Use as standalone OR as appendix to Lean/BMC. |

Pick one. Name it. State why in one line.

### Step 3 — Fill the canvas
Use the template from `references/canvas-templates.md` for the chosen canvas.

**Lean Canvas (1-page, 9 boxes):** Problem · Customer Segments · Unique Value Proposition · Solution · Channels · Revenue Streams · Cost Structure · Key Metrics · Unfair Advantage.

**BMC (1-page, 9 boxes):** Customer Segments · Value Propositions · Channels · Customer Relationships · Revenue Streams · Key Resources · Key Activities · Key Partnerships · Cost Structure.

**VPC (2 sides):** Customer Profile (Jobs · Pains · Gains) ↔ Value Map (Products & Services · Pain Relievers · Gain Creators).

Rules:
- Every entry is **specific and falsifiable**. "Increase user engagement" → "Reduce time to first invoice from 6h to 30min".
- If you don't know, write `[HYPOTHESIS — needs validation]`. Never fabricate.
- Channels box: name ONE wedge channel that works pre-scale. List others as "later".
- Unfair advantage / moat: must be a concrete asset (proprietary data, exclusive partnership, founder credibility, regulatory licence, switching cost mechanism). Reject "AI", "network effects", "community", "great team" without specifics.
- Cost structure / revenue: include order-of-magnitude numbers. If unknown, call `fermi`.

### Step 4 — VPC appendix (optional)
If `value proposition fit` is the dominant uncertainty AND the chosen canvas is Lean Canvas or BMC, fill a VPC appendix focused on the chosen segment. Otherwise skip.

### Step 5 — Apply anti-pattern audit
Read `references/anti-patterns.md`. Common fires:
- Segment = "consumers" / "businesses" / "developers" → reject
- Channels = "SEO", "social media", "content marketing" with no specific wedge → flag
- Unfair advantage = "AI" / "data" / "network effects" / "community" with no concrete asset → flag
- Revenue = "freemium" with no conversion mechanic → flag
- Two-sided marketplace with no bootstrap-side strategy → flag
- "Customer relationships = self-service" without onboarding mechanic → flag

For each flag, either rewrite the box or mark it `[HYPOTHESIS — needs validation]` with a named test.

### Step 6 — Surface top-3 critical assumptions
After the canvas is filled, ask: "If I'm wrong about this, the whole model collapses." Pick 3. State each as a falsifiable claim with a measurable threshold.

Example: "Designers will pay $39/mo for invoicing automation — falsified if <5% of qualified-traffic landing-page visitors enter card details on a smoke-test."

These flow directly into `idea-evaluation`'s next-kill-test step.

### Step 7 — Write and log
Write to: `docs/ventures/models/YYYY-MM-DD-<idea-slug>-canvas.md`

Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
```
| YYYY-MM-DD HH:MM | business-modeling | docs/ventures/models/<file> | <Canvas type> for <idea> |
```

Tell the user:
> "Canvas saved to `docs/ventures/models/...`. Top 3 assumptions logged. Next: `idea-evaluation` to score and pick a kill test, or `customer-discovery` to validate the riskiest assumption first."

---

## Output Format — Canvas Doc

```markdown
# <Canvas Type>: <idea>
Date: YYYY-MM-DD | Stage: <pre-launch/pre-PMF/etc.> | Segment: <specific persona>

## Why this canvas
<one-line rationale for picking Lean/BMC/VPC>

## The Canvas
<filled canvas with all 9 (or 6 for VPC) boxes — every box has a specific
entry or [HYPOTHESIS — needs validation]>

## Anti-Pattern Flags
- <box> — <pattern> — <action: rewrote / marked hypothesis>

## Top 3 Critical Assumptions
1. **<assumption>** — Falsified if: <measurable threshold>
2. **<assumption>** — Falsified if: <measurable threshold>
3. **<assumption>** — Falsified if: <measurable threshold>

## VPC Appendix (if applicable)
<jobs / pains / gains ↔ products / pain-relievers / gain-creators>

## Open Questions
<must be addressed before idea-evaluation can verdict>
```

---

## Gotchas

- **Lean Canvas is not a junior BMC.** It targets earlier-stage uncertainty (problem, key metrics, unfair advantage) instead of operations (resources, activities, partners). Pick on stage, not on prestige.
- **Don't fill VPC standalone unless segment fit is the only question.** Most early ideas need Lean Canvas first; VPC is the zoom-in.
- **A canvas is not validation.** A perfectly filled canvas with 0 customer evidence is still a hypothesis. The top-3 assumptions are the bridge to validation.
- **Revenue + cost without numbers is theatre.** Even rough order-of-magnitude beats "we'll charge enterprise pricing".

---

## Example

<examples>
  <example>
    <input>Model the business for the freelance-designer invoicing tool we generated yesterday</input>
    <output>
Two questions before I pick the canvas:

1. What stage are you at — pre-launch (no users), pre-revenue (some users, no payment), or pre-PMF (paying users but unclear retention)?
2. Is the dominant uncertainty (a) whether designers actually want this, (b) how the unit economics work, or (c) the value-proposition specifics?

(a) → Lean Canvas. (b) → BMC. (c) → VPC.
    </output>
  </example>
</examples>

---

## Calling This Skill From Other Skills

`venture-exploration` calls this in the model stage. Output feeds `idea-evaluation` (top-3 assumptions become kill-test inputs) and `customer-discovery` (segment + JTBD become interview targets).

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| Idea = feature | Business ideas route to venture-exploration, not brainstorming. |
| Skip Mom Test | Customer discovery before building. |
| Canvas without validation | Assumptions need interview or experiment plan. |

## Verification

- [ ] Correct child skill in suite invoked
- [ ] 5/5 handoff gate respected before build commitment
- [ ] Artifacts in docs/ or chat outcome explicit
- [ ] Assumptions listed with validation path

## Red Flags

- Full BMC used when Lean Canvas fits earlier uncertainty
- VPC filled without confirmed segment or problem fit
- Canvas treated as validation with zero customer evidence
- Revenue model assumed without pricing or willingness signal

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

`Business modeling complete: <idea> File saved: docs/ventures/models/YYYY-MM-DD-<slug>-canvas.md Canvas chosen: Lean Canvas / BMC / VPC VPC appendix: yes / no Boxes filled with spec`