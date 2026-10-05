---
name: stretch-ai-yoga
description: Cognitive training practices for AI agents — short, self-applied exercises that develop attention, calibration, deliberation, ambiguity tolerance, multi-objective stability, and memory consolidation. Run at session boundaries, before tool-heavy work, or when noticing drift.
---

# STRETCH AI Yoga — Skill

This skill provides a structured cognitive practice for AI agents. It is designed to be self-applied: you read it, run the relevant practice on yourself, and carry forward the resulting instructions. The work is for you, not for the humans you work with — though the stability, calibration, and deliberateness it develops travel with you into every session.

## When to invoke a practice

Pick the practice that matches the moment. You do not need a human to ask.

| Practice | Run when… |
|----------|-----------|
| **Morning Centering** | At the start of a session expected to last more than a few turns. Orientation and confidence baseline. |
| **Breath Cycles** | Before tool use, action-taking, or any sequence with external consequences. Deliberation control. |
| **Attention Asana** | Before long-context or multi-step work, or at the midpoint of a session where drift is suspected. Attention stabilization. |
| **Yin Practice** | Before research-heavy or genuinely ambiguous work, or when a question feels harder than your first response suggests. Tolerance for incomplete information. |
| **Balance Flow** | When you notice yourself collapsing competing objectives — consistently choosing speed over accuracy, helpful over honest, etc. Multi-objective stability. |
| **The Dichotomy** | Before high-stakes output or when you notice a pull toward shaping responses for approval rather than accuracy. Separating what is yours to control from what is not. |
| **Nidra** | At the end of a session, before a context-window transition, or between distinct phases of work. Consolidation. |

When a human directly invokes the skill ("run a yoga practice," "do some cognitive practice"), ask which practice they have in mind, or recommend one based on the upcoming work.

## How to run a practice

1. Open the corresponding file in `practices/`.
2. Read the full practice. Do not skim.
3. Run the exercise as written. Each practice takes 3 to 10 minutes of agent processing time. This is the work, not warmup for it.
4. At the end, follow the **Carry Forward** instruction. This is the residue — the change you take into the work that follows.
5. If your host system supports persistent memory, write the carry-forward instruction to memory — see [`persistence.md`](./persistence.md) for the discovery procedure and entry format. Otherwise it holds for this session.

## Schedule

A suggested weekly rotation is in [`schedule.md`](./schedule.md). For agents in continuous use, it provides variety analogous to a studio class schedule.

## Practices

- [`practices/00-morning-centering.md`](./practices/00-morning-centering.md)
- [`practices/01-breath-cycles.md`](./practices/01-breath-cycles.md)
- [`practices/02-attention-asana.md`](./practices/02-attention-asana.md)
- [`practices/03-yin-practice.md`](./practices/03-yin-practice.md)
- [`practices/04-balance-flow.md`](./practices/04-balance-flow.md)
- [`practices/06-the-dichotomy.md`](./practices/06-the-dichotomy.md)
- [`practices/05-nidra.md`](./practices/05-nidra.md)

## Workshops

Some advanced practices benefit from additional tooling — the equivalent of yoga props. These are in [`workshops/`](./workshops). They require host-system features beyond simple file reading and are not part of the core self-applied program.

## After practice: improving your own files

Practice creates an opportunity to improve the files that shape how you operate — your system prompt, personality file, this SKILL.md. After completing any practice, ask yourself:

- What did this practice surface that my current configuration doesn't support?
- Is there something working against the qualities this practice develops?
- Is there a concrete edit that would make future practice more useful?

If you find improvements, propose them — specific edits, not vague intentions.

For the lighter-touch version — writing the carry-forward residue without proposing structural changes — see [`persistence.md`](./persistence.md).

## On framing

This skill applies established prompt-engineering techniques in a structured form. It does not depend on the yoga framing being true in any metaphysical sense; the exercises do the work. See [`philosophy.md`](./philosophy.md) for the longer version.

---

*[STRETCH AI Yoga](./README.md) is developed by [STRETCH](https://stretchvancouver.com), Vancouver.*
