---
name: brainstorming
description: Use before any creative or ambiguous work - new features, new components, or behavior changes - to explore intent, requirements, and design before implementation starts.
---

# Brainstorming Ideas Into Designs

Turn ideas into a fully formed design through collaborative dialogue, before writing implementation code.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what's being built, present the design and get approval.

<HARD-GATE>
Do NOT write implementation code, scaffold files, or take any implementation action until a design has been presented and approved. This applies to every task regardless of perceived simplicity.
</HARD-GATE>

## Anti-Pattern: "This Is Too Simple To Need A Design"

Every non-trivial change benefits from this process — a small endpoint, a single component, a config change. "Simple" tasks are exactly where unexamined assumptions cause the most wasted work. The design can be two sentences for a truly simple task, but state it and get a nod before touching code.

## Checklist

1. **Explore project context** — check relevant files, docs, recent commits before asking anything
2. **Ask clarifying questions, one at a time** — purpose, constraints, success criteria; prefer multiple-choice but open-ended is fine
3. **Propose 2-3 approaches** with trade-offs, leading with a recommendation
4. **Present the design** in sections scaled to their complexity, checking in after each
5. **Write the decision down** — a short design note before or alongside the change (a PR description, a comment at the top of a plan, or a file under `docs/` for anything non-trivial)
6. **Move to implementation** once the design is confirmed

## The Process

**Understanding the idea:**
- Check the current project state first (relevant `agent/`, `client/`, or `consumer/` source, `docs/`, recent commits)
- If the request bundles multiple independent pieces (e.g. "add a new job type and redesign the dashboard and add auth"), flag that immediately — decompose into separate design/implementation cycles rather than refining details of an oversized request
- Ask questions one at a time; only one question per message — if a topic needs more exploration, split it across messages
- Focus on: purpose, constraints, success criteria

**Exploring approaches:**
- Propose 2-3 different approaches with trade-offs
- Lead with the recommended option and explain why
- YAGNI ruthlessly — remove unnecessary scope from every approach

**Presenting the design:**
- Scale each section to its complexity: a sentence or two if straightforward, more if nuanced
- Check after each section whether it looks right so far
- Cover what's relevant: architecture, data flow, error handling, testing approach
- Be ready to revise if something doesn't hold up

**Design for isolation and clarity:**
- Break the system into units with one clear purpose each, communicating through well-defined interfaces, each independently understandable and testable
- For each unit: what does it do, how is it used, what does it depend on?
- If a file or module is already doing too much, that's a signal worth naming in the design, not silently working around

**Working in this codebase specifically:**
- `agent/` is Express + TypeScript + Sequelize/Postgres + Kafka producer; `client/` is Angular; `consumer/` is a TypeScript Kafka consumer. Follow the existing layering and patterns in whichever area the change touches.
- Where existing code has a problem that directly affects the work (a file that's grown too large, unclear boundaries), it's fine to include a targeted improvement in the design — but don't propose unrelated refactoring.

## After the Design

- Write the agreed design down somewhere durable before implementing — for anything more than a few lines, a short markdown note under `docs/` beats a paragraph that only exists in chat history
- Self-review the written design: any "TBD"/placeholder left in? Do sections contradict each other? Is any requirement ambiguous enough to be read two ways? Fix inline, no need to re-review.
- Get explicit approval on the design before moving to implementation — don't infer approval from silence
