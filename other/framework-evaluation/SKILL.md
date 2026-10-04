---
name: framework-evaluation
description: Structured evaluation of external tools, frameworks, libraries, or patterns against Tessera's design — produces a decision ADR with adoption verdict and re-evaluate triggers
when-to-use: When considering whether to adopt an external framework, library, or pattern; when periodically reviewing the ecosystem for drift; when revisiting a prior decision because conditions changed
user-invocable: true
paths: []
effort: medium
---

# Framework Evaluation Skill

A structured methodology for evaluating external tools, frameworks, libraries, or patterns against Tessera's design. Produces an ADR that captures the decision, the reasoning, the concepts to steal (if any), and the conditions that would trigger re-evaluation.

This skill exists because frameworks drift. The world changes, new tools emerge, existing tools evolve, and a static design ossifies if it never reckons with the outside world. The skill is the systematic counterweight to ad-hoc evaluation.

---

## When to invoke

- **Cadence-based:** quarterly review of the agentic coding landscape, or whenever a meaningful new tool surfaces in your awareness
- **Contact-based:** you just heard about something new (released project, blog post, conference talk) and want to know if it matters
- **Trigger-based:** a prior evaluation's re-evaluate condition has fired
- **Decision-based:** a new project or work stream raises the question of which tool to use

If the question is "should we use this?" or "does this still apply?" — this is the skill.

---

## The methodology

Six dimensions, ~20 questions. Work through them in order. Each produces evidence; together they produce a decision.

### 1. Identity & maturity

Lightweight scan to understand what you're looking at:

- **Project basics.** Name, URL, license. Star count and trajectory (growing/stable/declining). Date of last meaningful release. Date of last commit.
- **Maintainer model.** Solo developer, small team, large team, corp-backed, foundation-backed, acqui-target. Where does the funding come from? What's the sustainability story?
- **Bias risk.** Who benefits from your adopting it?
  - Indie tool: maintainer wants users; risk is abandonment
  - Vendor loss-leader: company wants you in their ecosystem; risk is lock-in to a paid product later
  - Community project: collective ownership; risk is bloat and direction drift
  - Acqui-target: built to be acquired; risk is sunset or repositioning
- **Recent direction.** Read the last 3-6 months of releases or commits. Are they fixing bugs (mature), adding features (growing), or pivoting (unstable)?

Output: a one-paragraph identity summary.

### 2. Problem space overlap

The crux of the evaluation. Be honest about overlap before getting tactical:

- **What problem does it solve that Tessera also tries to solve?** List the overlaps explicitly.
- **What problem does it solve that Tessera does not address?** List the gaps in your design that it fills.
- **What problem does Tessera solve that it does not address?** List the gaps in their design that you fill.
- **For each overlapping problem, are the solutions compatible, conflicting, or just different bets on the same question?**
  - Compatible: both could coexist
  - Conflicting: choosing one means rejecting the other's approach
  - Different bets: both are plausible answers; the difference is taste or specific tradeoff

Output: a problem-overlap matrix with the four categories.

### 3. Integration cost

For each viable integration path, count the cost:

- **Adopt fully (replace Tessera with it):** what's the switching cost? What design work is wasted? What original IP (e.g., healthcare profile, override mechanism) needs to be ported or abandoned?
- **Adopt patterns (steal ideas, keep Tessera):** which specific patterns are worth lifting? How much work to implement them in Tessera's idiom?
- **Hybridize (run alongside):** does it coexist cleanly with Tessera? Are there conflicts at the hook/skill/runtime level?
- **Continue without (maintain own forever):** what's the cost of *not* adopting? What gaps remain? What maintenance burden is implicit?

Output: a cost-per-path comparison.

### 4. Pattern-level vs implementation-level

For each interesting pattern (from the overlap analysis), ask:

- **Is it the *idea* you'd adopt, the *implementation*, or both?** Most often it's the idea — implementations are usually replaceable, but a well-named concept (e.g., "phase loop," "subagent isolation") is a thinking tool that survives the specific code.
- **Can the idea live in Tessera with your own implementation?** If yes, you can adopt the pattern without the dependency.
- **Are there implementation details worth preserving from theirs?** Sometimes a specific trick (e.g., how they handle a tricky edge case) is worth keeping even if you reimplement the rest.

Output: a list of patterns marked *(idea-only / impl-too / skip)*.

### 5. Lock-in & maintenance

The honest sustainability question:

- **If you adopt, what depends on their continued maintenance?** Be specific. "Their hook script that fires on session start" is different from "their conceptual model of fresh-context subagents."
- **If they pivot, sunset, or stall, what's your exit?** Could you fork? Could you replace? Are you trapped?
- **If you don't adopt, what's the cost of building/maintaining the equivalent yourself?** This is the symmetric question — Tessera also has maintenance burden, and it's all on you.
- **What's the lock-in risk for each path?** Adopting fully is highest lock-in; adopting patterns with own implementation is lowest.

Output: lock-in and exit-cost per path.

### 6. Decision

Synthesize and commit:

- **Decision:** adopt fully / adopt patterns / watching / reject. Be specific about which.
- **Concepts to steal** (if any), with brief implementation notes for how they land in Tessera.
- **What to skip and why** (concepts you considered but rejected). Naming what you didn't take is as valuable as naming what you took — it's the trail of reasoning for the next reviewer (often future-you).
- **Re-evaluate trigger conditions:** what specific changes would cause you to reopen this question? Examples: "Re-evaluate if they add a healthcare-aware extension." "Re-evaluate if maintenance becomes corp-funded." "Re-evaluate at next quarterly cadence regardless."

Output: a complete ADR using the template at `docs/adr/_template.md`.

---

## Anti-patterns

A few failure modes worth naming:

- **Confirmation bias in framing.** When you write the eval, you'll have an instinct about which way you want it to land. Notice that instinct; treat it as evidence to scrutinize, not as the answer.
- **Sunk-cost protection.** "We've designed Tessera for four days; we can't switch now." That's not an argument. The sunk cost is unrecoverable either way. The only question is forward cost.
- **Excitement bias.** "This is shiny and new." Shiny doesn't mean better. Run the methodology even when it's tempting to skip to "yes, adopt."
- **Familiarity bias.** "Their docs are confusing and our design is clear." Yours is clear because you wrote it. Don't confuse familiarity with quality.
- **Single-dimension judgment.** "Their star count is high, therefore better." Or "they're a solo developer like me, therefore aligned." One dimension is never the answer; the methodology has six for a reason.
- **Skipping the re-evaluate trigger.** A decision without trigger conditions becomes a decision made forever. Always name what would change your mind.

---

## Output

The skill produces an ADR (Architecture Decision Record) following the template in `docs/adr/_template.md`. Each ADR is numbered sequentially, dated, and committed to the repo. The ADR becomes a permanent part of Tessera's design history — the trail of how the framework decided what it is.

When re-evaluating a prior ADR (because trigger conditions fired), do not edit the original — write a new ADR that references it. The history stays intact.

---

## Connection to other Tessera concepts

- **Principle #16 (Evaluate the ecosystem on a cadence; document the verdict)** — this skill is the implementation of that principle.
- **Suggestion-gate (#12)** — this skill should be invoked when external frameworks come up; it's heavy machinery, not silent default.
- **The Sources Consulted section of the design doc** — every ADR feeds back into the design doc's record of what we learned and from where.
