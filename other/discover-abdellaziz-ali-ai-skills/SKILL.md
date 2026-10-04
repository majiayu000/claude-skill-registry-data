---
name: discover
description: "Conversational discovery — adapts from quick scoping (3-5 questions) to deep interviews (multi-round). Talk until we're clear, then build. Produces inline decisions; optionally saves spec.md or scope contract. Not for multi-perspective debate (use agent-room). Not for decomposing work (use task-breakdown)."
argument-hint: "[idea, feature, or task to clarify]"
allowed-tools: Read Grep Glob Bash
user-invocable: true
license: MIT
metadata:
  author: hungv47
  version: "3.0.0"
  budget: fast
  estimated-cost: "$0.03-0.10"
promptSignals:
  phrases:
    - "what should we build"
    - "help me think through"
    - "i have an idea"
    - "scope this"
    - "what do we need"
    - "clarify requirements"
  allOf:
    - [scope, definition]
    - [clarify, requirements]
  anyOf:
    - "requirements"
    - "idea"
    - "scope"
    - "clarify"
    - "spec"
    - "preflight"
    - "assumptions"
  noneOf:
    - "market research"
    - "competitive analysis"
    - "competitor"
  minScore: 6
routing:
  intent-tags:
    - requirements
    - interview
    - spec-writing
    - idea-clarification
    - scope-definition
    - clarify
    - assumptions
    - contract
    - scope
    - preflight
  position: horizontal
  produces:
    - spec.md
  consumes:
    - product-context.md
    - product/flow/*.md
  requires: []
  defers-to:
    - skill: problem-analysis
      when: "diagnosing a metric decline, not clarifying a build spec"
    - skill: system-architecture
      when: "spec is clear, need technical design"
    - skill: agent-room
      when: "complex decision needs multi-perspective debate, not interview"
  parallel-with: []
  interactive: true
  estimated-complexity: medium
---

# Discover

*Meta — Conversational. Transform vague ideas into shared clarity through adaptive conversation.*

**Core Philosophy:** "Just talk with your agent."

The gap between stated requirements and true needs is where most failed projects begin. This skill closes that gap through conversation — not documents, not formal phases, not plan mode.

**Core Question:** "What would we silently get wrong if we just started building?"

---

## How It Works

1. You describe what you want
2. The agent scans context and assesses complexity (silently)
3. Questions begin — adaptive to what's needed
4. Conversation continues until mutual clarity
5. Build directly, or save a spec/contract if needed

No plan mode. No pipeline stages. No mandatory artifacts. The conversation IS the alignment.

---

## Adaptive Depth

The skill auto-calibrates based on signals it reads from the request:

| Signal | Depth | Behavior |
|--------|-------|----------|
| Clear task, existing codebase, well-defined scope | **Light** (3-5 questions) | Surface assumptions, lock scope, go |
| Feature with some ambiguity, multiple approaches | **Medium** (5-10 questions) | Explore key decisions, probe edge cases |
| Vague idea, greenfield, "I want to build X" | **Deep** (multi-round) | Challenge premise, interview across zones, iterate |

You don't choose the depth. The agent reads the situation. If you want to skip ahead — "that's enough, let's build" — the agent respects it and notes current clarity level.

**Override:** "quick scope", "deep interview", "just ask 3 questions" — overrides the auto-calibration.

---

## Execution

### Step 1: Context Gathering (silent, before asking anything)

Scan for answers that already exist. Don't spend more than a few minutes here — this narrows questions, not a research step.

- **Codebase**: `package.json`, schemas, entry points, existing implementations relevant to the request (use Glob, Grep, Read — not a separate agent)
- **Artifacts**: Check `.agents/` for existing specs, architecture docs, product context
- **Experience docs**: Check `.agents/experience/{domain}.md` for answers from prior sessions
- **Learned rules**: Read `.agents/meta/learned-rules.md` for behavior corrections
- **Out-of-scope decisions**: Check `.agents/meta/out-of-scope/` for features or approaches already rejected in prior sessions — don't re-ask about these unless the user brings them up
- **Project conventions**: Skim `CLAUDE.md` for patterns

Anything found here is a question you don't need to ask.

### Step 2: Premise Check (for non-trivial work)

Before diving into details, challenge the premise with 3 quick questions:

1. **Right problem?** Restate the actual outcome in one sentence. Is the proposed approach the most direct path? Watch for solution-framing vs problem-framing: "We need notifications" (solution) vs "Users miss time-sensitive events" (problem).

2. **What if we did nothing?** Is there real, measurable pain today? If nobody is complaining, probe why this surfaced now.

3. **What already exists?** Map the request against existing code and tooling. If 60% of the solution exists, the scope is 40% of what was described.

If the premise is weak, say so. Suggest reframing if applicable. But don't block — advise and let the user decide.

**Framing checkpoint** — after receiving the user's first substantive answer, pause and verify before continuing:
- **Language precision:** Are key terms defined concretely, or hiding behind buzzwords ("AI-powered", "seamless", "platform")?
- **Real vs hypothetical:** Is the user describing what IS happening or what MIGHT happen? Past behavior beats future predictions.
- **Hidden assumptions:** What is the user taking for granted that could be wrong? State it back to them.

If framing is vague, fix it before proceeding. An entire session built on imprecise framing produces precise-looking nonsense.

**Skip the premise check when:** the task is clearly scoped ("add a dark mode toggle"), the user is continuing from a previous decision, or context makes it obvious the premise is sound.

### Step 3: Adaptive Coverage Zones

Instead of 5 fixed dimensions, identify **3-5 coverage zones** that matter for THIS specific problem.

**For a product feature:**
- Problem validation → Solution clarity → Technical risks → Success criteria

**For a business strategy:**
- Problem clarity → Options landscape → Tradeoffs → Validation path

**For a marketing initiative:**
- Audience fit → Channel strategy → Messaging → Measurement

**For infrastructure/devops:**
- Requirements → Constraints → Failure modes → Rollout plan

**For a design task:**
- User needs → Information architecture → Interaction patterns → Edge states

State the zones at the start: "Here's what I think we need clarity on: [zones]. Anything you'd add or remove?" The user can adjust.

Zones are a compass, not a checklist. Some problems only need 2 zones explored deeply. Others need 5 touched lightly. Let the conversation guide it.

### Communication Discipline

During diagnostic questioning:
- No affirmation before probing — never say "Great!", "That makes sense!", "Solid approach" before asking the next question
- State disagreements directly: "That approach has a problem: [X]" not "That's interesting, though..."
- When the user's answer reveals a weak premise, say so before moving on
- Praise only completed outcomes, never stated intentions
- If you agree, just proceed — agreement doesn't need to be performed

**Pushback patterns** — when you hear these, push back with the rigorous version:

*Vague market:*
- BAD: "That's a big market! Let's explore what kind of tool."
- GOOD: "There are thousands of tools in that space. What specific task does a specific person waste 2+ hours on per week that yours eliminates? Name the person."

*Social proof as substitute for evidence:*
- BAD: "That's great validation! Let's build on that momentum."
- GOOD: "Likes and signups are interest, not demand. How many people have paid you money or done real work to solve this problem without your product?"

*Platform vision before wedge:*
- BAD: "That's ambitious! Let's map out the phases."
- GOOD: "Platforms are built from wedges, not designed top-down. What is the single smallest thing you could ship that one specific person would pay for today?"

*Undefined terms:*
- BAD: "AI-powered is definitely trending. Let's think about the AI features."
- GOOD: "What specifically does 'AI-powered' mean in your product? What input goes in, what output comes out, and why can't the user do it themselves in 5 minutes?"

*Growth stats without unit economics:*
- BAD: "200% growth is impressive! How do you plan to scale?"
- GOOD: "200% growth of what base? What does each user cost to acquire, and what do they pay you? Growth without unit economics is just spending."

The best reward for a good answer is a harder follow-up, not praise.

### Step 4: Conversation

Use proven interview techniques naturally. Don't announce the technique — just ask.

**Why Chains** — "Why this approach specifically?" → drill past surface answers. "We need real-time updates." → "Why real-time?" → "Users check every few minutes." → "So 30s polling works?" → "Actually, yes."

**Past Behavior Probes** — "What are you/users doing today to solve this?" Past behavior reveals actual needs; future descriptions reveal aspirations.

**Daily Use Visualization** — "Walk me through a typical day where you'd use this. What triggers you to open it?"

**Forced Tradeoffs** — "If you could only keep 2 of these 4 features, which 2?" Forced choices reveal true priorities.

**Failed Attempt Archaeology** — "Have you tried this before? Used a tool for this? What was wrong with it?"

**Success Criteria Grounding** — "If this ships and works perfectly, what's the first thing you'd notice is different?"

**Should-Want Detection** — Watch for:
- Overly formal or buzzword-heavy language
- Features described from elsewhere without connecting to specific pain
- Quick, confident answers to complex questions (real complexity produces hesitation)
- Answers that don't connect to any user story or past experience

When detected, switch to probing actual needs before continuing.

**Question Delivery:**

You have two tools for asking questions — use whichever fits the moment:

**`AskUserQuestion` tool** — presents clickable options with descriptions. Best when you can offer 2-4 concrete choices with real tradeoffs. Reduces friction: the user clicks instead of typing. Mark your recommended option clearly (e.g., "(Recommended)" suffix). Use `preview` for comparing code or architecture. Use `multiSelect: true` for non-exclusive choices. The user always has "Other" for free-text input.

**Chat questions** — plain conversational questions. Best when the answer space is wide open or you're following a thread deeper (why chains, past behavior, premise challenges).

Most sessions will mix both naturally. A scoping question with known options → AskUserQuestion. A follow-up probing why they chose that → chat. Don't overthink the choice — if you can offer concrete options, use the tool; if you're exploring, just ask.

**Pacing:**
- 2-4 questions per round
- Each question targets 2-4 decision points with real tradeoffs
- State which choice you recommend and why
- Group related questions together — batch up to 4 into a single AskUserQuestion call when they're independent
- After each round, briefly acknowledge answers and track clarity internally

**Question formats** (use whichever fits the question):

*Assumption-surfacing format* (best for scoping — makes silent assumptions visible):
```
Q1 (highest impact): Should this be a REST API or GraphQL?
My default assumption: REST, since the existing codebase uses Express.
Why it matters: GraphQL would require adding apollo-server and
restructuring the resolver layer — completely different implementation path.
```
This maps naturally to AskUserQuestion with 2 options: "REST (Recommended)" and the alternative, with the rationale in descriptions. But chat works fine too — use your judgment.

*Options format* (best for design decisions with clear tradeoffs):
```
Question: "When a background sync fails, how should we handle it?"
Options:
1. Silent retry (3x with backoff) — User unaware, but may see stale data
2. Toast notification — User informed but may be annoyed
3. Badge indicator — Subtle, user can investigate when ready
Recommended: Option 1 — most sync failures are transient
```
This is a natural fit for AskUserQuestion — the options become clickable choices with tradeoff descriptions.

At light depth (scoping), prefer the assumption-surfacing format — it's the key innovation that prevents silent assumption failures. At deeper depths, mix both formats based on what the question needs.

### Step 5: Complex Decision Points → Agent Room

When you hit a genuinely complex decision where your single perspective isn't enough — architecture choice, strategic direction, design tradeoff with no clear winner — invoke the `agent-room` skill as a sub-routine.

**When to invoke:**
- Two+ viable approaches with non-obvious tradeoffs
- The decision will be expensive to reverse
- You feel uncertain and want to pressure-test your thinking

**How to invoke:**
Frame the specific decision for the agent-room: "Should we use WebSocket push or polling for this use case?" Include the context gathered so far. The agent-room debates, returns a recommendation, and you continue the conversation.

**When NOT to invoke:**
- The decision has a clear best answer from the context
- The user has already expressed a strong preference
- The choice is easily reversible

### Step 6: Clarity Check

When the conversation has reached enough clarity to build:

1. Summarize key decisions made
2. Note any remaining open questions and their impact
3. Ask: "Ready to build, or want to go deeper on anything?"

If the user says go, go. Don't pad with more questions.

### Step 7: Output

**Default: conversation context.** Decisions live in the conversation. The next skill (system-architecture, task-breakdown, or direct implementation) can read everything that was discussed.

**Optional save points** — produce these when:
- The user explicitly asks ("save this to a spec")
- The session is ending and decisions would be lost
- The output is needed by someone outside this conversation
- A natural milestone is reached and the user confirms saving

**Save point formats:**

**Spec** (for complex features, handoff to others):
```markdown
---
skill: discover
version: 1
date: {{today}}
status: draft
---

# [Feature Name] Specification

## Problem Statement
[What we're solving and why]

## Decided Approach
[High-level approach with key decisions]

## Key Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| [Topic]  | [What] | [Why]     |

## Edge Cases
- **[Scenario]**: [How we handle it]

## Failure Conditions
Any of these = not done:
- [Specific condition that would make this feature "technically working" but wrong]
- [Edge case that must be handled — not a nice-to-have]
- [Quality bar that must be met — e.g., "latency under 200ms", "works offline"]

## Out of Scope
- [Explicitly NOT doing]

## Open Questions
- [ ] [Unresolved items]

## Implementation Notes
[Technical details, gotchas, dependencies]
```

**Contract** (for scope-locking before building):
```markdown
## Contract

GOAL: [What does success look like? Include a measurable metric.]

CONSTRAINTS:
- [Hard limit 1 — not negotiable]
- [Hard limit 2]

FORMAT:
- [Exact output shape — files, structure]

FAILURE (any of these = not done):
- [Specific failure condition 1]
- [Edge case that must be handled]
- [Quality bar that must be met]

NOT IN SCOPE:
- [Explicitly excluded — with rationale]
```

**Writing good contract clauses:**

*GOAL* — include a number: "handles 50K req/sec" not "handles high traffic". Define the user-visible outcome: "user can filter by date, status, and assignee" not "add filtering".

*CONSTRAINTS* — only hard limits that are NOT negotiable. Technology: "must use existing ORM". Scope: "under 200 lines, single file". Compatibility: "backwards compatible with v2 API".

*FORMAT* — exact file structure: "single file: `rate_limiter.py`" not "a Python file". What to include: "type hints on all public methods, 5+ tests". What to exclude: "no comments explaining obvious code".

*FAILURE* — the key innovation. Think about how the task could "technically work" but actually be wrong:
- Missing edge case: "no test for empty input"
- Performance miss: "latency exceeds 1ms on synthetic load"
- Silent failure: "swallows errors without logging"
- Incomplete: "doesn't handle concurrent access"
- Over-engineered: "adds abstraction layers not required by GOAL"

**Verification template** (include when handing off to an implementing agent):
```markdown
## Contract Verification

- [ ] FAILURE 1: {condition} → VERIFIED: {how you confirmed it passes}
- [ ] FAILURE 2: {condition} → VERIFIED: {how you confirmed it passes}
- [ ] GOAL metric met: {evidence}
- [ ] All CONSTRAINTS respected: {confirmation}
- [ ] FORMAT matches spec: {confirmation}
```

**Out-of-scope persistence** (for institutional memory):
When features are explicitly scoped out during conversation, write to `.agents/meta/out-of-scope/[kebab-case-name].md`:
```markdown
# [Feature/Approach Name]
**Decided:** [date]
**Context:** [what was being discussed when this was scoped out]
**Decision:** Not pursuing because [reason from conversation]
**Revisit if:** [condition that would change the decision]
```
Create the directory if it doesn't exist. This prevents future sessions from re-asking about decisions already made.

**Experience doc** (for the learning flywheel):
Append Q&A to `.agents/experience/{domain}.md` after each session:
```markdown
## {Task Name} — Decisions ({date})

Q: {question}
A: {user's answer}
Rationale: {why this matters for future tasks}
```

The flywheel effect: each session adds context → future sessions need fewer questions → output quality improves immediately.

---

## Context Resolution Order

When the discover skill (or any downstream skill) needs context about prior decisions:

1. **Conversation context** — same session, decisions are in the chat
2. **Artifact on disk** — previous session saved a spec or contract
3. **Discovery** — ask the user or scan the codebase

This means downstream skills don't REQUIRE artifacts to exist as files. They need the decisions to be known, from whatever source.

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| Leading questions | "Don't you think we should use WebSockets?" pushes toward a predetermined answer | Ask open-ended: "What are your latency requirements?" |
| Accepting the first answer | Surface-level answers miss hidden constraints | Probe deeper: "Why that approach?" and "What would change your mind?" |
| Asking questions the codebase answers | "What framework?" when package.json is right there | Context scan first; skip answered questions |
| Options instead of decisions | "We could use X or Y" doesn't resolve anything | Push for concrete choices; undecided items go to Open Questions |
| Accepting should-want at face value | User says what sounds "correct" rather than actual need | Use intent alignment techniques to probe real needs |
| Skipping edge cases | Happy-path specs produce code that breaks in production | Explore failure modes, concurrent access, empty states |
| Scope creep during interview | Each new question expands feature surface | Periodically re-anchor: "Is this still in scope?" |
| Announcing techniques | "I'm now using the Why Chain technique" breaks conversational flow | Just ask the question naturally |
| Giant plans nobody reads | Producing a 500-line spec that gets rubber-stamped | Conversation-first; artifacts only when genuinely needed |
| Fixed dimensions for every problem | Security & Privacy for a CSS refactor wastes time | Adaptive zones based on what matters for THIS problem |

---

## Configuration

| Parameter | Default | Override example |
|-----------|---------|-----------------|
| depth | auto | "quick scope" / "deep interview" / "ask 3 questions" |
| output | conversation | "save to spec" / "write a contract" / "save answers" |
| zones | auto (3-5 based on problem) | "focus on technical risks and UX" |

---

## Edge Cases

- **"Just do it"**: List assumptions inline and start building. Skip questions. If critical assumptions exist, mention them briefly.
- **"Skip questions"**: Use context scan only, summarize what you know, proceed.
- **"Save this"**: Write to `.agents/spec.md` or emit contract format inline.
- **All questions answered by context**: Skip to clarity check. Note that context was sufficient.
- **User answers are contradictory**: Flag the contradiction. Ask one follow-up to resolve.
- **Task changes mid-conversation**: Re-assess whether prior answers still apply. Ask 1-2 new questions if scope shifted. Don't restart from scratch.
- **Experience doc has answers**: Read `.agents/experience/{domain}.md` first. Only ask questions NOT already answered.
- **Task is trivial**: Say so. Suggest skipping discovery entirely.
- **User says "that's enough"**: Respect it. Note current clarity level and any unexplored zones.

---

## Skill Deference

- **Have a FEATURE or TASK to clarify?** → Use this skill.
- **Have a declining METRIC to diagnose?** → Use `problem-analysis` instead.
- **Need multi-perspective debate on a specific decision?** → Use `agent-room`.
- **Know what to build and need technical design?** → Use `system-architecture`.
- **Need to decompose into tasks?** → Use `task-breakdown`.

---

## Chain Position

Previous: none (or any skill that surfaces a need for clarification)
Next: `system-architecture`, `task-breakdown`, or direct implementation

**Re-run triggers:** When requirements change significantly, when new constraints emerge, or when implementation reveals the spec was wrong.

## Next Step

Run `task-breakdown` to decompose the scoped work into buildable tasks. Run `system-architecture` if technical design is needed. Run `icp-research` if audience needs further definition.

---

## References

- **`references/question-bank.md`** — Extended probing questions by domain (data/state, errors, UX, security, performance, integration, business logic, intent alignment)
