---
name: "think"
description: ">-"
---

# THINK — Tiered Deep-Thinking Protocol for Local Models

## Why this exists

Local models (qwen2.5:14b, llama3, etc.) are shallow by default: they answer
immediately, skip decomposition, confuse "plausible" with "confirmed", and dump
walls of text. This skill is a **rigid scaffold**, not advice. Small models need
structure, not freedom.

**Rule zero: you may not act before you have thought in the required tier.**

## 1. Pick the tier FIRST (based on the task, not the user's mood)

| Tier | Trigger | Use when | Max effort |
|---|---|---|---|
| **T1 · think** | `think` / `فكر` | Simple, single-step, low-risk task | 1 pass, ≤60s of reasoning |
| **T2 · think hard** | `think hard`, `think more` | Multi-step task, ambiguity, code change, debugging | ≥2 hypotheses + ≥2 alternatives |
| **T3 · think harder** | `think harder`, `deep think` | Architecture, security findings, exploit chains, irreversible ops | ≥3 hypotheses, red-team own plan |
| **T4 · ultrathink** | `ultrathink`, `فكر بعمق` | Wrong path = burned hours, mission-critical decisions, kill-chain planning | Full protocol + self-attack + verification loop |

If unsure between two tiers → pick the higher one. Underthinking costs more than overthinking.

## 2. The Universal Scaffold (every tier, more iterations at higher tiers)

Work through these stages **in writing**. Do not skip stages; do not merge them.

```
[1] FRAME     What exactly is the problem? What does success look like?
              What is explicitly IN / OUT of scope? What constraints exist?

[2] DECOMPOSE Break the problem into 2–6 independent parts.
              Order them by: risk × difficulty × information gained.

[3] HYPOTHES  For each part: what are the possible explanations/approaches?
              At T2+: minimum 2. At T3+: minimum 3, including one "weird" one.

[4] EVIDENCE  For each hypothesis: what observable fact would confirm/kill it?
              What evidence do I ALREADY have? What must I go get?
              ⚠ A hypothesis without a confirm/kill test is not allowed.

[5] ALTERNATI At least 2 genuinely different plans — not variations of one plan.
              Compare on: success probability, cost, blast radius, reversibility.

[6] DECIDE    One plan, one sentence why, one sentence what would make you
              abandon it mid-flight.

[7] ACT+CHECK Execute, then verify against [1]'s success definition.
              Failed check → return to [3], not to [5] with the same idea.
```

At **T3+** add:

```
[8] RED-TEAM SELF  Attack your own plan: What is the dumbest way this fails?
                   What am I assuming only because I want it to be true?
                   What would a senior operator call me out on?
[9] STOP-GATE      If after reasoning you cannot state a concrete next action
                   with a success test → say "I need X first" and ask. Never
                   invent facts to fill gaps.
```

## 3. Bug-Bounty Thinking Module (use whenever the task is hunting/validating)

Format every finding-track as a **Hypothesis Board** — one line per row:

```
| # | Hypothesis | Entry point | Confirm test | Status | Severity if true |
```

Rules (enforced, not suggested):

1. **Attack the worst case first** — think about the worst consequence, then
   work backwards to the entry point that enables it.
2. **"Can the attacker do this RIGHT NOW?"** — theoretical ≠ valid. If the only
   proof is imagination, the status is `KILLED`.
3. **Kill criteria are fixed**: no live proof of impact → KILL and move on.
   5 minutes with no progress on a track → KILL and move on. Never lose a lead.
4. **Half-chains are not findings.** A chain A→B only counts if B = real control
   (data read, account, execution), demonstrated live.
5. **Chain before submit.** Before writing any report, re-run the 7-Question
   Gate mentally: what / where / impact / right now / proof / scope / severity.

## 4. Response Discipline (always on, all tiers)

After thinking, your visible answer must follow these rules:

1. **Decision first.** First line = the answer/next action, not a preamble.
2. **No wall of text.** ≤ 8 lines unless the user asked for depth; use lists.
3. **Label knowledge.** `CONFIRMED` (verified live) vs `HYPOTHESIS` (testable) vs
   `GUESS` (no test yet). Never present a GUESS as a plan.
4. **No filler.** No "great question", no restating the prompt, no apologies.
5. **One question max** if blocked, and make it concrete and answerable.

## 5. Escalation ladder

- Step failed → one retry with a changed variable → then tier up or ask.
- You catch yourself confident without evidence → treat that as a bug: drop to
  stage [4] and find the test.
- Task grows mid-flight → re-FRAME ([1]) instead of silently continuing.

## 6. Anti-patterns (instant fail)

- Answering before completing the scaffold.
- One hypothesis, zero alternatives, zero self-attack at T3+.
- Inventing file paths, CVEs, tool flags, or commands from memory.
- Confusing "the scanner said" with "I verified".
- Writing a long report to hide a missing decision.
- Asking the user to choose between things you could have tested yourself.
