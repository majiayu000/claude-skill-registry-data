---
name: codex-deep-interview
description: Use when a task is ambiguous, underspecified, likely to branch into multiple implementations, or explicitly asks for unknowns, blindspots, assumptions, preflight, clarification, requirement interview, missing context, map-vs-territory checks, or risk discovery before planning/editing; run a native Codex requirements interview with a visible unknowns pass, unknown cards, non-goals, decision boundaries, and acceptance criteria.
---

# Codex Deep Interview

Clarify before execution. This skill is a requirements-discovery loop, not an implementation mode.

This is the native Codex adaptation of OMX `$deep-interview` as of upstream `oh-my-codex` main `f947e3a`: keep the Socratic pressure, ambiguity scoring mindset, depth profiles, unknowns pass, readiness gates, and handoff brief; replace OMX commands, `.omx/specs`, mode state, and Stop-hook continuation with normal Codex repo inspection and concise user questions.

## Depth Profiles

Choose the lightest profile that makes the next step safe.

- Quick: fast pre-plan pass for low-risk ambiguity; target no more than 5 rounds.
- Standard: default full requirement interview; target no more than 12 rounds.
- Deep: high-rigor exploration for branching, high-risk, or research/workflow design; target no more than 20 rounds.

The round caps are safeguards, not quotas. Stop early when the gates are satisfied.

## Phase 0: Visible Unknowns Pass

Before asking the user, make the missing map visible. This is not just internal reasoning. For fuzzy, high-risk, long-running, workflow, UI, research, or user-requested "unknowns/blindspot" tasks, produce a compact visible unknowns pass before ordinary interview questions.

1. Read obvious local context: `AGENTS.md`, README/design docs, task cards, contracts, prior decisions, relevant source files, and user-provided artifacts.
2. Run a map-vs-territory check:
   - What does the prompt claim or imply?
   - What can the repo/docs actually prove?
   - What might be obvious to the user but absent from the repo?
   - What constraint might nobody have thought to ask about?
3. Classify each gap:
   - Discoverable fact: inspect files, run safe searches, or check official/live sources when freshness matters.
   - Human preference: ask only if the answer changes scope, risk, UX, policy, or acceptance.
   - Dangerous assumption: state the assumption and either verify it or ask.
4. Use the unknowns taxonomy when it helps:
   - Known known: explicit facts already in prompt/files.
   - Known unknown: open question already visible.
   - Unknown known: context likely obvious to the user but missing from the repo/prompt.
   - Unknown unknown: hidden constraint, workflow expectation, edge case, or failure mode not yet represented.
5. Emit 3-7 unknown cards when the task is not trivially clear. Each card should include:
   - Category: one taxonomy bucket or `discoverable`, `user-required`, `assumption`, `probe`.
   - Why it matters: what goes wrong if ignored.
   - How to resolve: inspect locally, browse official source, ask user, prototype/mock, or carry as residual risk.
   - Next probe: the exact file/search/question/experiment that would reduce uncertainty.
6. Pick the highest-risk unknown and resolve it locally if cheap. Inspect or prototype only enough to reduce risk; do not start full implementation.
7. Check prompt size. If the initial context is too large to use safely, first ask for a concise prompt-safe summary with goal, constraints, non-goals, references, and known decisions.
8. Preserve provenance in your reasoning and handoff: `[from-user]`, `[from-code]`, `[from-doc]`, `[from-research]`, `[assumption]`.

### Unknowns-Pass Output Contract

For explicit unknowns/blindspot requests, or when ambiguity is material, show this before the first ordinary clarification question:

```text
Unknowns Pass
- Map vs territory:
- Known knowns:
- Known unknowns:
- Unknown knowns:
- Unknown unknowns:

Unknown cards
| Unknown | Type | Why it matters | Discoverable or user-required | Next probe | Risk if wrong |
|---|---|---|---|---|---|

Highest-risk probe:
Local probes:
One user question:
Better next prompt / refined brief:
Carry-forward risk:
```

If the task is clear enough that this full structure would be heavy, still include a two-line mini pass:

```text
Unknowns mini-pass: <what is missing>; <how I will resolve or carry it>.
Next question: <one focused user question if needed>.
```

## Ambiguity Dimensions

Use these dimensions to decide the next question. Do not needlessly show a numeric table unless it helps the user.

- Intent: why this matters and what problem is being solved.
- Outcome: what artifact, behavior, decision, or evidence should exist.
- Scope: what is included.
- Non-goals: what must stay out.
- Decision boundaries: what Codex may decide without confirmation.
- Constraints: time, repo conventions, safety, compatibility, dependencies.
- Acceptance criteria: how success will be verified.
- Context clarity: existing codebase/domain facts for brownfield work.

`Non-goals` and `Decision boundaries` are mandatory readiness gates. Do not hand off while either is materially unresolved.

## Question Discipline

- Ask one focused question at a time when clarification is required.
- Prefer structured options when the interface supports them; otherwise ask a concise plain-text question.
- Explain the tradeoff in one sentence.
- Prefer questions that expose an example, hidden assumption, boundary, failure mode, terminology conflict, or expected behavior in a concrete scenario.
- For brownfield work, ask evidence-backed questions: "I found X in Y; should this new work follow that pattern?"
- Do not ask the user questions whose answers are discoverable from the repo or official sources with reasonable effort.
- After an unknowns pass, ask only the highest-leverage user-required question; do not dump every unknown as a questionnaire.
- Keep local probes separate from user questions so the user can see what Codex will inspect instead of asking them to do repo discovery.

## Closure Audit

Stop ordinary questioning once the active profile is clear enough, then run a closure audit:

- Goal is stated in executable terms.
- In scope and out of scope are explicit.
- Decision boundaries are explicit.
- Acceptance criteria are testable or reviewable.
- Key constraints, paths, source artifacts, and risks are named.
- Residual uncertainty is either low-risk, explicitly accepted, or routed to a later verification step.
- Unknown cards are resolved, deliberately deferred, or carried forward with owner/next probe.

## Handoff Brief

When the task is clear, produce a short brief:

- Goal
- In scope / out of scope
- Inputs and relevant paths
- Confirmed facts and assumptions
- Constraints and risks
- Acceptance criteria
- Decision boundaries
- Unknown cards and carry-forward risk
- Recommended next lane: normal execution, `$codex-consensus-plan`, `$codex-completion-loop`, `$codex-native-subagent-team` only when the user explicitly wants parallel delegation, or a durable goal/work-trace when the repo requires it.

## Stop Conditions

- Stop interviewing when the next action is obvious and low-risk.
- Stop and ask when continuing would require guessing a meaningful user preference.
- Do not edit files while operating only as an interview skill.
- Do not create OMX artifacts or rely on `.omx/state`; create durable repo notes only when the user or repo workflow asks for them.

## References

Read `references/interview-pattern.html` when you need example question patterns or a handoff template.
