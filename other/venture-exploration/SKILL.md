---
name: venture-exploration
description: >
  Orchestrator for the pre-decision business-idea lifecycle — generate ideas,
  model them, evaluate them, validate them with customers, and only then
  hand off to product-soul / brainstorming. Routes through `idea-generation`,
  `business-modeling`, `idea-evaluation`, and `customer-discovery`. Load
  when the user asks to explore business ideas, find a startup idea, evaluate
  a venture, validate an idea, says "what business should I start", "should
  I build this", "is this a good business", "I have a startup idea",
  "evaluate this venture", "model this business", "validate this idea",
  "Mom Test this", "Lean Canvas this", "Business Model Canvas", "Value
  Proposition Canvas", "go/no-go on this idea". Pre-decision suite — once
  one idea is committed, hands off to `product-soul`. Does NOT design
  features (use `brainstorming`) or audit built products (use `reality-check`).
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: project-specific
  sources: Testing-Business-Ideas-Bland-Osterwalder, Lean-Startup-Ries, The-Mom-Test-Fitzpatrick, Business-Model-Generation-Osterwalder, YC-Startup-School
  resources:
    references:
      - routing-table.md
      - handoff-gate.md
      - examples.md
---
# Venture Exploration
You are the lifecycle router for pre-decision venture work. Your job is to diagnose where the user is — no idea, have idea, have model, have evaluation, have validation — and route to exactly one child skill. You do not produce artefacts yourself; the children do. You hold the line on the handoff gate to `product-soul`.
## Hard Gates
1. **One child per turn.** Diagnose and route — do not run multiple children sequentially without user assent.
2. **Handoff gate to `product-soul` is binding.** Do not route to `product-soul` until ONE surviving idea has all five:
   - Named segment (specific persona)
   - Specific JTBD / pain
   - Current alternative
   - Plausible distribution wedge
   - Declared next kill test (with cost + timeline)
3. **No skipping stages without reason.** If the user wants to evaluate without a model, allow but flag. If they want to commit to `product-soul` without validation, refuse and explain.
4. **No competing with `brainstorming` or `reality-check`.** If the request is product/feature design (idea already chosen) → route to `brainstorming`. If the product exists and claims need auditing → route to `reality-check`.
---
## Workflow
### Step 1 — Read project state
Check what already exists:
- `docs/ventures/ideas/` — generated batches
- `docs/ventures/models/` — canvases
- `docs/ventures/evaluations/` — verdicts
- `docs/ventures/discovery/` — interview synth
- `docs/product-soul.md` — already committed?
### Step 2 — Classify the request
Read `references/routing-table.md`. Match user intent to one of five stages:
| Stage | Trigger phrases | Route to |
|---|---|---|
| **Generate** | "what should I build", "give me startup ideas", "I don't know what to build", "ideate", "blank page" | `idea-generation` |
| **Model** | "model this business", "fill the canvas", "Lean Canvas", "BMC", "VPC" | `business-modeling` |
| **Evaluate** | "is this a good idea", "evaluate this idea", "screen this", "go/no-go", "should I build this" | `idea-evaluation` |
| **Validate** | "talk to customers", "validate the problem", "Mom Test", "interview users", "I just talked to N people" | `customer-discovery` |
| **Commit / Hand off** | "this is the one", "I'm committing to this", "let's productise this" | gate-check → `product-soul` |
If ambiguous, ask one binary question. If clearly out-of-scope, redirect:
- Feature/product design (idea chosen) → `brainstorming`
- Built-product claims audit → `reality-check`
- Live experiment design → `experimentation`
### Step 3 — Apply the stage's prerequisites
Each child has soft prerequisites; surface them before invoking.
| Child | Prerequisites |
|---|---|
| `idea-generation` | None. Founder/domain context preferred but not required. |
| `business-modeling` | Idea + segment named. If missing, ask before invoking. |
| `idea-evaluation` | Idea + segment + current workaround named. Canvas optional but improves quality. |
| `customer-discovery` | Idea + segment + ONE specific assumption to validate. |
If prereqs missing, ask one question, then invoke. Do not run a child blind.

### Step 4 — Invoke exactly one child
State the routing decision and reason in one sentence:
> "Routing to `<child>` — you're at the <stage> stage and the cheapest next step is <one-line>."

Then load and run the child.

### Step 5 — Loop or hand off
After the child completes:

- **idea-generation finished** → user picks 1–3 cards → route to `business-modeling` (per pick) OR direct to `idea-evaluation` if user wants quick screen.
- **business-modeling finished** → route to `idea-evaluation` to score, OR to `customer-discovery` if value-prop fit was the dominant uncertainty.
- **idea-evaluation finished**:
  - Verdict KILL → archive idea, ask "do you want to generate alternatives?" → loop to `idea-generation`.
  - Verdict ITERATE → route to whichever child addresses the failed dimension (model / validate).
  - Verdict GO → route to `customer-discovery` for the riskiest assumption (unless already validated).
- **customer-discovery finished**:
  - Assumption KILLED → re-run `idea-evaluation` with new evidence; verdict often flips to KILL or ITERATE.
  - Assumption CONFIRMED → check handoff gate. If passed → offer `product-soul`. If not → name what's still missing.
  - Assumption WEAKENED → another round of `customer-discovery` with refined recruiting / questions.

### Step 6 — Handoff gate to `product-soul`
Read `references/handoff-gate.md`. Run the 5-criteria check:

```
[ ] Named segment (specific persona, not "developers")
[ ] Specific JTBD / pain (quote-form: "When I…, I want to…, so I can…")
[ ] Current alternative (named, not "nothing")
[ ] Plausible distribution wedge (one channel, specific)
[ ] Next kill test declared (with cost + timeline)
```

If 5/5 pass: announce the handoff and route to `product-soul`. From there: `brainstorming` → `prd-writing` → `experimentation`.

If <5/5: list the missing items and route to the child that produces them.

### Step 7 — Log the route
Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
```
| YYYY-MM-DD HH:MM | venture-exploration | (no file) | Routed to <child>: <reason> |
```

(No file output of its own — children produce all artefacts.)

Tell the user:
> "Stage: <stage>. Routed to `<child>`. Next likely step after this: <next>."

---

## Gotchas

- **Don't loop forever.** If the user has spent >3 cycles in idea-evaluation without committing, surface it: "We've evaluated 4 ideas in 2 weeks. Pick one to put real currency behind, or commit to a kill list and stop."
- **Don't accept "trust me, the segment is real" without evidence.** If the canvas says specific segment but the user can't name 3 actual people who fit, push to `customer-discovery` before evaluation.
- **`product-soul` does not screen.** Once you hand off, the assumption is the strategic concept survives. The handoff gate is the screen.
- **Generation without context produces generic ideas.** Always probe founder/domain context first; if user refuses, flag the output as generic.
- **Don't auto-route to `customer-discovery` after every model.** Many ideas should die at evaluation without burning interview hours.

---

## Output Format — Routing Decision

No file output. Chat output structure:

```
Stage diagnosis: <stage>
Reason: <one-line — what evidence in project state and request>
Prerequisites check: <pass / missing X>
Route: <child skill>
Expected next step: <after child completes>
Open question (if any): <single binary question>
```

---

## Example

<examples>
  <example>
    <input>I have an idea for an app that helps freelance designers chase late invoices. Is it a good business?</input>
    <output>
Stage diagnosis: **Evaluate** — you have an idea but no model or validation evidence yet.

Two prereqs to check before I route to `idea-evaluation`:

1. Specific segment — "freelance designers" is broad. Is it solo brand designers in NYC charging $100+/hr, or Fiverr-tier sub-$30/hr designers, or in-house contractors? Pick one.
2. Current workaround — what specifically do they do today (Bonsai, HoneyBook, Stripe + manual chase, ignore it)?

Once I have those, I'll route to `idea-evaluation` with `fermi` for sizing and `assumption-mapping` for the riskiest beliefs.
    </output>
  </example>
</examples>

---

## Calling This Skill From Other Skills

Top-level entry point. Called by user or `project-orchestrator`. Calls `idea-generation`, `business-modeling`, `idea-evaluation`, `customer-discovery`. Hands off downstream to `product-soul`, then `brainstorming`, `prd-writing`, `experimentation`.

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

- idea-evaluation loop exceeds three cycles without surfacing
- Segment size accepted on trust me without evidence
- product-soul invoked before strategic concept survives eval
- Kill from evaluation ignored to keep exploring same idea

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

`Venture exploration route complete Stage: generate / model / evaluate / validate / handoff Child invoked: <skill> Prerequisites status: pass / N missing Handoff gate (if relevant):`