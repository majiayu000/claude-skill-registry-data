---
name: ideation
description: Generate ideas with structure when you're stumped — on what to build next, what the real problem is, or how to solve it. Pulls in research for context, diverges wide using matched frameworks, then converges on a prioritized few. Use when the user says "I'm stuck", "I'm stumped", "ideate", "brainstorm ideas", "help me think of", "what could I add", "what should I build", "I don't know what the problem is", "how could I solve", or wants idea generation on any topic (product, technical, business, writing, personal). For auditing an existing product against its users, use review-product instead.
argument-hint: '[topic] [--quick]'
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Ideation

Help someone who is stumped generate ideas — smartly and with structure, not a flat
list of the obvious. Works on **any** topic: features for an existing product, what
problem to even solve, how to solve a defined problem, business moves, writing, personal
decisions.

The method is always the same rhythm: **frame the stuck-state → gather just enough
context (research if needed) → diverge wide → push past the obvious → converge on a
prioritized few.** The frameworks change with the stuck-state; the rhythm doesn't.

This is **divergent-then-convergent**: generate broadly with judgment off, *then* narrow.
It is the broad counterpart to `review-product` (which audits a product against its users
in a specific direction). Where `superpowers:brainstorming` gates implementation behind an
approved design, this skill is upstream of that — it generates the ideas you'd then design.

`review-product` delegates here when its audit surfaces a **wide-open gap** — a user job the
product doesn't serve at all, whose fix isn't obvious — and needs a divergent spread of
approaches rather than a single evidence-anchored fix. It passes the specific job as the topic
and signals that the job is an already-validated unmet need, so the router lands in solution
mode and skips re-litigating whether the job is worth solving. That hand-off is the main
programmatic caller; a single named job must work as the whole scope.

## Usage

```
ideation                       # infer the topic from context, classify the stuck-state, ask if unclear
ideation pricing model         # ideate on a named topic
ideation --quick               # one fast diverge→converge pass, minimal questions, no research
```

## The router — match frameworks to the stuck-state

Classify which kind of stumped this is (it can be a mix — handle the dominant one first).
Then pull only the matched entries from `references/frameworks.md`.

| Stuck on… | Signals | Frameworks to load |
|-----------|---------|--------------------|
| **Problem** — what's the real problem / am I solving the right thing? | "not sure what to fix", vague goal, solving a symptom | JTBD, First Principles, Inversion, 10x reframe → then **How-Might-We** to open it |
| **Feature** — what to add to something that exists | a working product, "what's next", "what complements this" | SCAMPER, Multi-perspective personas, Morphological analysis |
| **Solution** — how to solve a defined problem | problem is clear, ways to solve it aren't | Crazy 8s (volume), Analogical transfer, Lateral provocation, TRIZ (if a trade-off blocks it) |

Every session ends with the **Convergence** methods (scoring + riskiest assumption).

## Workflow

Create a TodoWrite item per step. With `--quick`, collapse to steps 3 + 5 only.

### Step 1 — Frame the stuck-state
- Determine the topic (from the argument, the conversation, or the current project) and
  classify it against the router: **problem / feature / solution** (or a mix).
- **Adapt to how stumped they are.** If it's unclear what they're stuck on, ask **1-2 sharp
  questions** — prefer offering concrete options over open prompts. Don't interrogate; a
  stumped person wants momentum. If the topic and mode are already clear, skip straight ahead.
- A common trap: they ask for *solutions* but are really stuck on the *problem*. If the goal
  is vague, start in **problem** mode regardless of how they framed it, and say so.

### Step 2 — Gather just enough context
- Survey what already exists: for a codebase, the relevant code/docs (`read-docs` if a
  `docs/` tree exists); for any topic, what the user has already told you or tried.
- **Research when external context would sharpen the ideas** — and only then. Time-box it.
  - `research-tech` — technical/library/pattern questions, prior art in code.
  - `research-general` — markets, competitors, domains, non-technical topics.
  - `read-docs` — internal project conventions and constraints.
  - Skip research entirely on `--quick`, or when you already have enough to diverge.
- Pin down **constraints and the goal**: what does a good idea here have to respect (budget,
  stack, audience, time), and what outcome are we optimizing? Ideas are only as good as the
  goal they serve.

### Step 3 — Diverge (judgment OFF)
- Apply the **2-3 matched frameworks** from the router. Generate a wide spread — aim for
  quantity, defer all evaluation, force real variety (no two ideas sharing one mechanism).
- For each idea give a one-line **why** (its reasoning), per the output format. An idea with
  no rationale is noise.
- Use Multi-perspective personas liberally for cheap diversity even outside feature mode.

### Step 4 — Push past the obvious
- The first cluster of ideas is always the obvious one. Run **one** breakthrough technique to
  escape it: **Inversion**, **Analogical/cross-domain transfer**, **10x**, or **Lateral
  provocation** (see `references/frameworks.md`). Add the non-obvious ideas it surfaces.
- This step is what makes the skill "smart" rather than a list generator. Don't skip it
  unless `--quick`.

### Step 5 — Converge
- Switch judgment ON. Cluster and dedupe. Score the survivors and pick a **top 3-5**.
- For each, capture **impact** (H/M/L), **effort** (S/M/L), and the **riskiest assumption**
  — the one thing that, if false, kills it (this is the next thing to test). Lead with
  high-impact / low-effort.
- Optionally pressure-test the shortlist with **Six Thinking Hats**.

### Step 6 — Present (save only if asked)
- Show the result inline using the Output Format below: the full diverge list (brief) and the
  prioritized shortlist (the table).
- **Default to presenting inline only.** Don't write a file unprompted, and never create a
  dedicated `docs/ideation/` directory.
- **If the user asks to save it:** when a `docs/` tree exists, write into the best-fitting
  **existing** subfolder — match the topic (e.g. `docs/product/`, `docs/planning/`, a relevant
  area folder), appending to an existing file if one obviously belongs; use `date +%F` in the
  filename. If there's no `docs/` tree, or nothing in it fits, just present inline and let the
  user name a path — don't invent a folder or a new docs section.
- End by pointing at the natural next move: validate the riskiest assumption, or feed a chosen
  idea into `superpowers:brainstorming` / `review-plan` to design it.

## Output Format

Inline, and written to a file only if the user asks:

```markdown
# Ideation — <topic> — <date>

> Stuck on: problem | feature | solution · Goal: <what we're optimizing> · Frameworks: <which>

## Ideas (diverge)
Grouped by the framework or lens that produced them; one line of reasoning each.
- **<idea>** — <why / the reasoning>.
- ...
(include the non-obvious ones from the push-past step, marked ✦)

## Shortlist (converge)
| # | Idea | Impact | Effort | Riskiest assumption to test |
|---|------|--------|--------|------------------------------|
| 1 | <idea> | H | S | <the one thing that, if false, kills it> |
| 2 | ... | | | |

## Next move
- Validate assumption for #<n> by <cheapest test>, or design #<n> via brainstorming/review-plan.
```

## Examples

### Example 1: Stumped on what to build next
User says: "ideation — I don't know what feature to add to my note app next."
Actions: Classify as **feature** mode. Skim the app's existing features (Step 2). Run
SCAMPER on the core capability + generate ideas from PM/Designer/Power-user lenses (Step 3).
Push past the obvious with analogical transfer ("how do *email clients* handle this?") (Step
4). Converge to 4 ideas with impact/effort and a riskiest assumption each (Step 5). Present
inline; save only if asked, into a fitting existing docs folder.

### Example 2: Stumped on the problem itself
User says: "I want to build something for freelancers but I don't know the problem."
Actions: This is **problem** mode even though it sounds like a build request. Use JTBD to map
the jobs freelancers hire tools for, First Principles to strip assumptions, `research-general`
for context on the segment. Reframe candidates as How-Might-We questions. Converge to 3 sharp
problem statements, each with the assumption to validate with real freelancers.

### Example 3: Quick solution burst
User says: "ideation --quick how do I cut my build time?"
Actions: **Solution** mode, no research. Crazy 8s for 8 distinct approaches, one analogical
prompt for a non-obvious angle, converge to top 3 with effort + riskiest assumption. Present
inline, no file.

## Troubleshooting

### Ideas are all obvious / surface-level
**Cause:** Skipped Step 4, or judged ideas during divergence.
**Solution:** Run a breakthrough technique (inversion, analogical transfer, 10x, provocation)
and keep judgment fully off while generating. The obvious cluster is the *start*, not the output.

### The user keeps rejecting ideas as "not the problem"
**Cause:** Generating solutions for an ill-defined problem.
**Solution:** Drop back to **problem** mode (JTBD, First Principles) and nail the problem
statement before generating solutions again. Say you're doing this.

### Too many ideas, no decision
**Cause:** Diverged without converging.
**Solution:** Force Step 5 — cluster, score impact/effort, cut to a top 3-5, attach a riskiest
assumption to each. The deliverable is a prioritized few, never the raw dump.

### It wants to research everything first
**Cause:** Over-indexing on context before generating.
**Solution:** Time-box research to what genuinely sharpens ideas; for fast sessions or
well-understood topics, skip it. Momentum matters — a stumped person wants ideas, not a report.

## Notes
- `references/frameworks.md` holds the full method library (procedure + example per framework),
  organized by stuck-state. Load only the entries the router selects.
- Adjacent skills: `review-product` (audit a product against its users — narrower, evaluative),
  `superpowers:brainstorming` (design-gate an approved approach — downstream of this),
  `review-plan` (review a plan once an idea is chosen), `research-tech` / `research-general`
  (the context sources this skill calls).
