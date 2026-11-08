---
name: skill-review
description: "Adversarial review and evidence-based overhaul of an agent skill (SKILL.md + references). Fans out reviewers with distinct attack lenses, audits every reference against frontier-model defaults and current web guidance, then rewrites around hard gates + high-freedom principles. Use when asked to review, audit, simplify, or harden a skill or instruction file."
disable-model-invocation: true
---

# Skill Review

Review a skill the way an attacker reads a contract: find where it contradicts itself, where a lazy agent slips through, and where it steers a capable model into worse outcomes. Then rebuild it lean. Main agent owns synthesis and all edits; reviewers and auditors are read-only.

## Phase 1 — Adversarial review (parallel, distinct lenses)

Spawn one reviewer per lens — never N identical passes; diversity catches what redundancy can't:

1. **Contradictions** — rules conflicting with each other or with linked references; priority-order conflicts; hard gates the references quietly bend. Report both sides with file:line + the scenario where an agent gets incompatible instructions.
2. **Loopholes** — simulate a lazy, rationalizing agent. Escape hatches ("when feasible", "say why") bypassable with one throwaway sentence; completion-laundering paths; guards that live only in load-on-demand refs while the loophole sits in always-on text; undefined jargon.
3. **Reference integrity** — every path resolves (case-exact); orphans (grep-back before calling anything dead); cross-file links; SKILL↔reference duplication (drift risk); eval-case drift.
4. **Trigger/scope** — description false-fires and false-negatives (construct concrete prompts for both); overlap with sibling skills and always-loaded docs (CLAUDE.md/AGENTS.md); missing handoffs to dedicated skills.
5. **Over-steering** — where prescription beats judgment a frontier model would exercise better; compounding-constraint traps (construct a task where obeying everything yields the worst outcome); justification-ritual accumulation. Also mark load-bearing steering that must NOT be relaxed.
6. **Holistic** (strongest model available) — design coherence, what's missing entirely, what to cut, steelman-then-break the load-bearing design decisions.

Each finding: severity, file:line, concrete failure scenario, smallest fix. Synthesize: dedupe (two reviewers hitting the same line independently = high confidence), rank, report to user before touching anything.

## Phase 2 — Redesign + reference audit (on approval)

**Research first** when redesigning: current skill-authoring guidance (Anthropic & OpenAI best practices, prompting guidelines, instruction-budget findings, exemplar skills). Don't design from memory.

**Target shape** for the rewritten SKILL.md:

- Few absolute gates (3-6), front-loaded, CAPITALIZED, phrased affirmatively — "verify X before Y" persists in long context; "don't do X" decays. Each gate names the rationalization it blocks.
- Everything else high-freedom principles: outcomes + constraints, not procedure. Frontier models degrade when micro-managed.
- Budget: SKILL.md under ~80 lines; instruction-following cliffs around 150-200 simultaneous rules across ALL loaded context, so count what CLAUDE.md/AGENTS.md already say and don't restate it.
- Description: third person, states what AND when, names handoffs to sibling skills.
- If a rule must be absolute, prefer a hook or script over prose — prose asks, hooks enforce.

**Reference audit** — parallel auditors grouped by domain, each reads its files fully and web-verifies currency (language/framework refs rot fastest). Keep bar, applied per file:

- KEEP only if it improves outcomes beyond what a frontier model does by default, is currently correct, and doesn't duplicate SKILL.md.
- REMOVE files that restate default model behavior (role/persona files rarely survive this), duplicate siblings, or embed another project's code.
- Absolutes need a backing eval/failure case; unbacked absolutes demote to defaults-with-stated-reason.
- Auditors return KEEP / KEEP-WITH-EDITS (exact line edits) / REMOVE (+ merge target), with citations for currency claims.

## Phase 3 — Execute and verify

Main agent applies everything centrally:

1. Rewrite SKILL.md; apply audit edits; deletes via `trash`.
2. Before deleting anything, grep the WHOLE repo for inbound references — prompts, evals, agent manifests, sibling skills all break silently. Update or merge, never orphan.
3. Verify: every path in the new SKILL.md resolves on disk; repo-wide grep finds zero dangling references to deleted files; frontmatter parses (harness picks up the new description).
4. Commit in logical groups: rewrite / prune+merge / content corrections. Leave unrelated dirty files unstaged.

## Cheap single-pass variant

For a quick check without the fan-out: run lenses 1, 2, and 4 yourself against SKILL.md only, plus the path-resolution check. Escalate to the full workflow when findings justify it.
