---
name: plan-from-scratch
description: Plan a new project before any code exists. Researches the domain, then has an architect, a product lead and a security lead plan it independently, and merges them into one PLAN.md that names where they disagree. Use when the user is starting something new and says "plan this", "help me start this project", "write a PLAN.md" or "what should the stack be". Not for changes to an existing codebase (use learn-this-codebase first).
---

# Plan a new project

## 1. Get the brief straight
Read `BRIEF.md` if it exists; otherwise ask for two or three sentences on what it is and who it's for. Then ask at most 5 questions, only ones whose answer changes the plan (users, scale, money, deadline, hard constraints). Don't ask what you can decide sensibly yourself.

## 2. Research first, alone
Before any planning, build domain context everyone else will read. Write `plans/research.md`:
- What already exists and where it falls short.
- The usual stack for this domain, what's emerging, and what to avoid and why.
- Integrations it will need (auth, payments, email, storage) and the regulations that apply.
- Hidden complexity: the parts that take 3x longer than people expect.

Cite sources for anything you looked up. Mark guesses as guesses.

## 3. Three leads plan independently
Give each the brief, the answers and `research.md`. If you can run subagents, run all three at once; otherwise write each in turn without reading the others first.

- **Architect** → `plans/architect.md`: system design, stack with a reason per layer, module boundaries and the interfaces between them, CI/CD, how it scales, technical risks.
- **Product** → `plans/product.md`: phases, each with tasks and acceptance criteria; success metrics; what's out of scope; assumptions.
- **Security** → `plans/security.md`: threat model (likelihood × impact), data classification, auth approach, compliance flags, concrete security tasks, anything urgent.

If one lead fails or stalls, carry on with the others and say what's missing.

## 4. Merge into one PLAN.md
`PLAN.md` at the project root:
1. Overview, in three sentences.
2. Decisions table: question, answer, who decided (user or lead).
3. Stack and architecture.
4. Phases with tasks and acceptance criteria. Phase 1 ships something a real user can use.
5. Security plan.
6. Success metrics.
7. Risks.
8. **Tensions:** where the leads disagreed, both sides, and your recommendation. Never smooth these over.
9. Boundaries, as a `boundaries` JSON block that `stay-in-the-lines` can check later.
10. Out of scope and assumptions.

## Rules
- The plan is for this team and this deadline, not a textbook system.
- Every phase ends in something you can test, not "set up infrastructure".
- Ask the user only the Tensions you can't resolve.
