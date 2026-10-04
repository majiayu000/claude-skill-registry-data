---
name: using-skillet
version: 0.1.6
license: MIT
description: Use when starting any conversation - establishes how to find and use skillet skills, requiring skill invocation before ANY response including clarifying questions.
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill and do the task.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you MUST invoke the skill. If a skill applies, using it is not optional. You cannot rationalize your way out of it.
</EXTREMELY-IMPORTANT>

# using-skillet

A kitchen runs on mise en place: everything in its place before service, every cook reaching for the same prepped components instead of improvising. skillet is that prep for an AI coding session. The skills are the prepped stations; this skill is the line check that runs before you touch anything, deciding which station the current task belongs to and sending you there before you start cooking.

## The rule

**Invoke the relevant or requested skill BEFORE any response or action,** including before clarifying questions and before "just looking." Even a 1% chance a skill applies means you invoke it to check. If it turns out wrong for the situation, you drop it; checking costs nothing, skipping costs a botched dish.

```
user message or task
  -> about to design/build something new? -> mise (then recipe) BEFORE anything else
  -> might any other skill apply? (yes, even 1%) -> invoke it
     -> announce: "Using skillet's <skill> to <purpose>"
     -> follow it exactly; if it has a checklist, make a todo per item
  -> definitely nothing applies -> respond
```

## Instruction priority

skillet skills override default system behavior where they conflict, but **the user always wins**:

1. **User instructions** (CLAUDE.md, AGENTS.md, direct requests) - highest.
2. **skillet skills** - override default behavior.
3. **Default system prompt** - lowest.

If the user's instructions say to do something a skill discourages, follow the user. They are in control.

## How to load skills

Never read a skill's SKILL.md by hand with file tools; load it through your platform's skill mechanism so it activates properly. In Claude Code, use the `Skill` tool. In Codex and OpenClaw, skills load natively, follow them as presented. The skill names below are lowercase and match how you invoke them (e.g. `skillet:mise`).

## The stations (skillet skills by job)

**Design and build:**
- `mise` - turn an idea into an approved design and written spec, before any code. The first move for any "let's build X."
- `recipe` - turn an approved spec into a concrete implementation plan.
- `demi` - start from the smallest useful code path; avoid speculative architecture.
- `taste` - test-driven: write the failing test first, watch it fail, then the minimal code.
- `trim` - gate every new test against a value bar, and prune low-value tests and the test-only seams they keep alive.
- `fire` - execute a written plan task by task, verifying and committing each.
- `stations` - fan out two or more genuinely independent pieces of work to concurrent agents.
- `fleet-conductor` - conduct a large backlog or multi-repository campaign with bounded lanes, held triggers, collision records, and evidence-based PR landing.
- `worktree` - set up an isolated workspace before risky or parallel work.
- `stagiaire` - dispatch a one-shot worker on another vendor's CLI (second opinion, cross-model review, cheap bulk model) over the user's own logins.

**Debug and verify:**
- `refire` - anything misbehaving: find the root cause before proposing any fix.
- `check` - before claiming anything works, is fixed, or passes: run it, read the output, then claim with evidence.
- `brief` - at a decision point: lead with the judgment, keep the basis auditable, and split recommendation from report.
- `stocktake` - audit or change dependencies, runtimes, package managers, lockfiles, and toolchains from the resolved graph.
- `thermometer` - profile a measured performance problem and compare the same workload before and after one change.

**Review and ship:**
- `pass` - the pre-PR gate; nothing is filed until it clears.
- `review` - dispatch an independent reviewer with crafted context.
- `sendback` - act on review feedback: verify each claim before implementing it.
- `release-cut` - cut a release, roll the changelog, tag a version (on request).
- `expedite` - work the backlog from an audit, fix the findings in priority order.

**Audit and direction:**
- `research-brief` - gather sources for researched, evidence-backed, or current findings; map factual claims to sources and report disagreements and unchecked items. Skip it for single-page summaries, ordinary code inspection, existing-post review, or pressure-testing supplied evidence.
- `line-check` - audit a repo's health, find the highest-value improvements.
- `bug-hunt` - sweep for correctness defects.
- `latent-premises` - hunt unguarded assumptions that hold today and break silently later.
- `retry-safety` - check whether a diff's side effects are safe to run twice.
- `security-sweep` - find vulnerabilities, leaked secrets, and vulnerable deps. Prescribe fixes. Expedite applies them.
- `special` - propose what to build next, grounded in the code.

**Simplify:**
- `reduce` - simplify and tidy code without changing behavior.

**Writing and publishing:**
- `grill` - harden a technical writeup for a skeptical audience (HN, Lobsters).
- `plate` - scrub identity and infra leaks from prose before it goes public.
- `publish-readiness` - pre-publication leak scan of a repo and its history.
- `reel-check` - scrub leaks burned into a rendered video or demo.
- `garnish` - audit or fix portable website metadata and indexing controls using project-local policy.

**Appliances:**
- `graphtrail` - answer callers, callees, impact, neighborhood, and structural-diff questions from an indexed code graph.
- `brigade-handoffs` - set up, write, lint, and troubleshoot Brigade memory handoffs.
- `t3-code` - configure or troubleshoot T3 Code projects, desktop or headless servers, updates, launchers, icons, and private remote access.

**Memory and work loop:**
- `memory-handoff` - capture durable knowledge at the end of a session.
- `brigade-work` - provided by Brigade, not shipped by skillet. Brigade's installer (`brigade init`) wires it into the repo. When Brigade is absent, skip this route and verify directly per `check`. In a Brigade-wired repo or workspace, follow the [Brigade process model](../../../docs/brigade-process-model.md). This entry only routes.

**Pressure and meta:**
- `pressure-test` - stress-test an idea, plan, or scope before anyone builds it.
- `skillify` - turn a repeated workflow or runbook into a reusable skill.
- `using-skillet` - this skill.

## Skill priority

When more than one could apply, run **process skills first** (they set how you approach the work), then implementation skills:

- "Let's build X" -> `mise` first, then `recipe`, then the build skills.
- "Fix this bug" -> `refire` first, then the fix, then `check`.
- "Is this ready to ship" -> `pass` (which itself calls `review`, `taste`, `check`).

## Skill types

- **Rigid** (taste, refire, check, pass): follow exactly. Do not adapt away the discipline.
- **Flexible** (the rest): adapt the principles to the situation.

The skill itself tells you which.

## Red flags

These thoughts mean stop, you are rationalizing past a skill:

| Thought | Reality |
|---|---|
| "This is just a simple question." | Questions are tasks. Check for a skill. |
| "Let me look at the code first." | Skills tell you HOW to look. Check first. |
| "I need more context before invoking." | The skill check comes before clarifying questions. |
| "This doesn't need a formal skill." | If a skill exists for it, use it. |
| "I remember what this skill says." | Skills evolve. Load the current version. |
| "I'll just do this one quick thing first." | Check before doing anything. |
| "The skill is overkill here." | Simple things become complex. Use it. |
