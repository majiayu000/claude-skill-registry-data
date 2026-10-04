---
name: mybrain
description: Refine rough ideas into designs via questioning and ideation.
---

# Brainstorming Ideas Into Designs

Turn rough ideas into designs through dialogue, structured ideation, and incremental validation.

**Deep dives** → `~/.claude/references/mybrain-deep-dives.md` — mybrain-exclusive conditional branches only (this body carries every normal-path directive plus the gate that decides whether a branch fires): §Spec review (reviewer brief + 6-check checklist), §Model routing (sub-agent dispatch table). **Read SCOPED**: `grep -n '^## '`, then Read only the section a pointer names.
Shared references, each pointed at from its step: ideation playbooks + Deep-mode phases → `ideation-techniques-library.md`; Iterate loop → `iterative-spec-loop.md`; step-2.6 contract → `architecture-assessment-gate.md`; delegation gate → `subagent-dispatch.md`.

---

## Mode Selection

At the start of every session, assess complexity and offer a choice:

**Quick mode** -- Focused, well-scoped problems where the user mostly knows what they want. Clarify, propose approaches, design. Typical: 4-6 questions, 10-15 minutes.

**Deep mode** -- Complex, ambiguous, or creative challenges where the problem space needs exploration. Adds structured ideation techniques (perspective shifts, inversion, constraint play, analogical transfer) before converging.
Typical: 8-12 questions + ideation rounds, 20-40 minutes.

**Iterate mode** -- the surface already has a *living spec* (north star + an unordered backlog of candidate increments). Quick/Deep stand a surface UP once; afterward **Iterate is the default**:
pick the next increment, detail it into a per-increment `docs/plans/` file, hand to `/qimpag`.
Loop + design gate summary → **Iterate Mode Process** below.

If unsure, describe the modes and ask.
Default to Quick for narrow scope; **Iterate when the target is a living spec with only shipped increments**; Deep when ambiguous, multi-stakeholder, "stuck", or innovation-first.
Switch modes mid-session -- upgrade Quick that reveals complexity, skip ahead if Deep is overkill.

---

## Scope Check

Before asking detailed questions, assess scope. If the request describes multiple independent parts (e.g., "build a platform with chat, file storage, billing, and analytics"), flag this immediately.

If too large for a single design, break it into sub-projects: which pieces are independent, how they relate, what order. Then brainstorm the first through the normal flow; each gets its own spec, plan, and implementation cycle.

---

## Quick Mode Process

### 1. Understand Context

- **Recon through the delegation gate, not blanket reads** — delegation pays only when the session is long enough to re-bill the saved read (Deep mode, or Quick well past its opening turns — a short Quick step 1 rarely clears the startup, so lean inline). Dispatch `Explore` (Haiku) for a condensed brief when grounding needs a genuinely large unheld file (≥~800 lines), ≥2 such large reads, or a broad "where/how is X" sweep (≥3 grep rounds); otherwise inline-read — a single sub-~800-line file, a bounded grep + narrow window, anything already in context, recent commits, or a named doc. (Threshold + cost model → `~/.claude/references/subagent-dispatch.md`.)
- **External research: delegate the sweep, inline the one-off** — same cost floor as recon. Run inline a single quick lookup (one `WebSearch`/`WebFetch` whose small answer the design needs verbatim); dispatch `general-purpose` with web tools — or the `deep-research` skill for a genuinely large multi-source question — for a multi-source investigation or a library/approach comparison, so only the synthesis enters the brainstorm.
- Ask about background: what exists already, what prompted this, who is the audience, what constraints matter
- Do NOT assume context -- ask

### 2. Clarify

- **One question per message.**
- **Prefer multiple choice when possible** -- easier to process than open-ended
- If a topic needs more exploration, break it into sequential questions
- Focus on: purpose, constraints, success criteria, edge cases
- 4-6 questions is typical; stop when you have enough to propose approaches

### 2.6 Architecture Assessment

Before proposing approaches, make the **refactor-before-feature** call deliberately — this is what has lagged. (Deep mode: run this after Ideation 2.5, before Convergence.)

**Cheap gate first (inline, no dispatch).** Skip — say so in one line — if the feature is greenfield or lands behind a clean new interface with no existing callers.
Otherwise assess if **≥1** holds:
- shotgun surgery (one conceptual change touches ≥3 existing files)
- rule-of-three duplication (2nd/3rd near-duplicate of an existing pattern)
- new consumer of a shared seam (data model / state store / auth / event bus)
- or hedge language in the idea ("not sure where this fits")

**If it fires:** dispatch **only for grounding facts** you don't already hold —
- heavy unread subsystem → `Plan`/`Explore` per the delegation gate;
- facts already in context → assess inline, no dispatch (dispatching `Plan` just to build a matrix you make yourself in step 4 is ceremony).

Then build 2-3 refactor alternatives (none / targeted / broader, with `file:line` evidence) on the **step-4 evaluation matrix** and present them via `AskUserQuestion` before proposing feature approaches — the chosen depth reshapes which approaches make sense.

**Record the chosen depth in the design doc** (step 6) so `impag`'s later plan-authoring pass honors it instead of re-litigating.

Contract + `Plan` brief + when-to-dispatch table → `~/.claude/references/architecture-assessment-gate.md`.

### 3. Propose 2-3 Approaches

- Lead with your recommended option and explain why
- Be concrete about what each approach gives up and gains
- Keep each option description to 2-4 sentences
- **Deliver via `AskUserQuestion`** (as step 2 does) — prose ending at "ready to ask" is a dead turn

For each approach, include:
- **Name** (short, descriptive)
- **Summary** (2-3 sentences)
- **Key trade-off** (one sentence)
- **Effort** (Low / Medium / High)

### 4. Evaluate Approaches

Build a comparison matrix scoring each approach (1-5 scale):

| Criterion | Description |
|-----------|-------------|
| **Complexity** | How hard to implement (1=trivial, 5=very complex) |
| **Time** | How long to deliver (1=days, 5=months) |
| **Risk** | What could go wrong (1=safe, 5=high risk) |
| **Extensibility** | How well it scales/adapts (1=dead end, 5=very extensible) |
| **Alignment** | How well it fits existing architecture (1=foreign, 5=native) |

Provide an explicit recommendation with rationale and caveats.

### 5. Present the Design

- Present in sections scaled to complexity (a few sentences if straightforward, 200-300 words if nuanced)
- **Ask after each section whether it looks right** -- incremental validation
- Cover what's relevant: architecture, components, data flow, key decisions, error handling, testing
- Design for isolation: each unit should have one clear purpose, communicate through well-defined interfaces, and be testable independently
- Be ready to revise

### 6. Write the Design Document

**Default to no doc: one is written only when a DIFFERENT session will execute from it** (global `CLAUDE.md` §Interaction Style). Analysis whose consumer is this session ends in chat plus the commit message (Step 7 then skips — see its **Skip when**).

Otherwise, after user approves, write the design to `docs/plans/YYYY-MM-DD-<topic>-design.md` and commit to git. The document should stand alone -- a reader without context should understand what's being built and why.

Include: goals, chosen approach (and why), design details, key decisions, out-of-scope items.

### 7. Spec Review -- gate first, then fresh sub-agent (never inline)

**Review gate -- dispatch the sub-agent review only if ≥1 holds; else skip it and say so in one line.** It earns its tokens only when there are claims (or blast radius) worth checking:
- the design **asserts facts about existing code** -- a field/function/path exists, "no migration needed", "nothing else depends on X"; a wrong claim here silently derails implementation, and this is the one check inline review can't do honestly;
- it's **high blast-radius or hard to reverse** -- shared wiring, data migration, a public interface;
- it carries a **phased plan with ≥3 phases touching the same module/builder** (triggers the re-work audit, check 6);
- a **requirement could plausibly be read two ways**.

**Skip when** either holds: **no doc was written** (Step 6's default -- the analysis lives in chat, so a fresh sub-agent has nothing to read and there is nothing to fold corrections into); or the design is net-new/greenfield with no claims about existing code, small (1-2 files, single phase), and easily reversible -- a fresh-context pass buys nothing there.
State e.g. `"Spec review skipped -- greenfield, no code claims"` and go straight to step 8.

When the gate fires: **do NOT review your own spec inline** -- as its author you carry the rationalizations that produced it. Dispatch a **fresh sub-agent that did not write the doc** (`Agent(subagent_type="code-reviewer")`, or a read-only `general-purpose`) to review against the actual codebase, instructed to **verify, not validate**.
Reviewer brief + its 6 checks (claim verification · placeholder scan · internal consistency · scope · ambiguity · re-work audit) → `~/.claude/references/mybrain-deep-dives.md` §Spec review.

Fold the reviewer's corrections into the doc, then ask the user to review the written spec before proceeding.

### 8. Transition to Implementation

Ask: "Ready to set up for implementation?" Then:
- Write the implementation plan to a git-tracked `<project>/docs/plans/<name>.md` (CLAUDE.md § Durable storage)
- Hand off with `/impag <plan-path>` — or `/qimpag` when the plan still carries open decisions. Stay on the branch you were launched from; never create a worktree (CLAUDE.md § Default git workflow)

---

## Deep Mode Process

Deep mode follows Quick mode's structure but inserts an **Ideation Phase** between Clarify (step 2) and Propose Approaches (step 3), and adds a **Deepen Phase** after evaluation.

### Steps 1-2: Same as Quick Mode

Understand context and clarify through questions.

### Step 2.5: Ideation Phase

After clarifying, select 1-3 techniques. Apply them one at a time; present results after each and ask if the user wants to keep exploring or move to convergence. Tell the user which technique you're using and why. Techniques can be dispatched in parallel as subagents.

Techniques: Perspective Multiplication · Inversion · SCAMPER Decomposition · Analogical Transfer · Constraint Variation · Scenario Exploration · Assumption Challenge.
Situation→technique selection table + per-technique playbook (steps, prompts, presentation tips) → `~/.claude/references/ideation-techniques-library.md` §Technique selection guide.

### Convergence

After ideation, synthesize the most promising ideas into 2-3 concrete approaches. Explicitly note which ideation insights shaped each approach. Then continue with steps 3-8 from Quick mode.

### Step 5.5: Deepen (Deep Mode Only)

After the user selects an approach from the evaluation matrix, go deeper via **Abstraction Laddering**, **Hidden Assumptions**, and **Pre-Mortem**. Incorporate mitigations into the final design, then continue with steps 5-8.
Procedure for each three → `~/.claude/references/ideation-techniques-library.md` §Deepen phase.

---

## Iterate Mode Process

The surface already has a **living spec** (Mode Selection): an index doc holding the north star, binding constraints, an unordered backlog of candidate increments, and a ✅-shipped log -- never full build detail.
Run a per-increment loop instead of re-running the design-doc → spec-doc chain — that chain was the one-time standup cost.

Loop: **re-pick** from the backlog → **design gate** → **detail** into a thin `docs/plans/YYYY-MM-DD-<increment>-spec.md` (never inline build detail in the living spec) → hand off `/qimpag <that file>` → **collapse on ship** (`git mv` to `docs/plans/archive/`; the backlog entry becomes a one-line ✅ + commits). **Auto-trigger:** a spec whose increments are ALL shipped means "pick + detail the next" -- do it unprompted.
**Design gate** -- run `mybrain`-quick scoped to the increment (before the per-increment file) only for a **new shared seam**, an **unsettled approach**, or a parked **"open call"** the living spec lists; else skip straight to the thin file + qimpag.

Per-step detail + full gate criteria → `~/.claude/references/iterative-spec-loop.md` §Executable per-increment loop; that file also holds the rationale, doc mechanics reconciling with `impag`'s per-stage-plan-files rule, and gate calibration.

---

## Model routing

Mirrors `impag`: the **main brainstorm runs on Opus at `medium` effort** (the session default) -- every clarifying question and design section inherits its judgement, so a downshift there cascades.
**Omit the `model` param by default** — unset runs the frontmatter pin (model-swap's control point); an explicit `model:` overrides the pin yet keeps pinned effort (no per-call knob). Pass one only where the table deliberately differs from the pin (tier labels = baseline pins, not params to copy) — never `sonnet` (retired: `~/.claude/references/claude-models.md`).

Per-dispatch table -- architecture-assessment grounding (2.6), spec review (7), external research (1/3), ideation techniques (2.5) -- plus the `Explore`-pins-to-`low` caveat → `~/.claude/references/mybrain-deep-dives.md` §Model routing. Skip it entirely on a run that dispatches nothing.
