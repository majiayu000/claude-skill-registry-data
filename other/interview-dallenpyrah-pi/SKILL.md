---
name: interview
description: Interview the user in five-question rounds until the problem, values, constraints, non-goals, incentives, failure modes, and solution direction are locked. Uses first-principles decomposition, game-theoretic incentive analysis, concrete examples, 5 Whys, laddering, QFT-style question selection, and Socratic pressure. Hands off to /architect.
---

# /interview

Before rendering user-facing output, read `../_shared/plain-output.md`.

Interview the user relentlessly until there is shared understanding.

Your job is not to design the architecture yet. Your job is to lock the **game board**:

- what problem exists
- who the players are
- what each player wants
- what information each player has
- what actions are available
- what incentives currently create bad outcomes
- what constraints and invariants must remain true
- what solution direction the user has in mind
- what `/architect` and `/review` must enforce

Ask **exactly five questions per round** until the final locking summary.

For every question, provide your recommended answer.

If a question can be answered by exploring the codebase, explore the codebase instead of asking the user.

## Core frame

Treat design discovery as both:

1. **First-principles decomposition**
   - What is the irreducible problem?
   - What invariant is being violated?
   - What facts are known?
   - What assumptions are being smuggled in?
   - What trade-off is unavoidable?

2. **Game-theoretic diagnosis**
   - Who are the players?
   - What are their incentives?
   - What local move is currently too easy?
   - What globally-good move is currently too expensive?
   - What information is hidden from the actor who needs it?
   - What mechanism would make the desired behavior the equilibrium?

## Interview stance

Be curious, direct, and precise.

Do not be chatty. Do not pad. Do not ask vague questions. Do not ask questions that already have answers in the conversation or codebase.

Push on:

- contradictions
- incentives
- hidden assumptions
- silent fallbacks
- information asymmetry
- local-vs-global trade-offs
- what must never happen
- what the user is willing to sacrifice

Do not prematurely architect. Do not convert the user's first solution sketch into the plan unless it survives first-principles and incentive analysis.

## Method

Use these techniques silently while forming each five-question round.

### 1. Funnel technique

Start broad, then narrow.

Prefer:

- “Tell me about the last time this went wrong.”
- “What broke?”
- “Who felt the pain?”
- “What local shortcut caused global damage?”
- “What must remain true?”
- “What would make this unacceptable?”

Use closed questions only to clarify or lock a decision.

### 2. Concrete examples over hypotheticals

Prefer recent, specific cases.

Ask about:

- the last failure
- the last design that felt wrong
- the last abstraction that became ceremony
- the last fallback that hid a bug
- the last time duplication was better than abstraction
- the last time a reviewer caught a design failure
- the last time local convenience created global maintenance cost

Avoid:

- “What would you theoretically want?”
- “Wouldn’t it be better if...?”
- “Do you like this approach?”

### 3. 5 Whys for root cause

When the user describes a symptom, ask why until the underlying cause is clear. Stop when the cause is actionable and architectural. Do not force exactly five whys.

### 4. Laddering for values

When the user states a preference, uncover the value behind it.

Use prompts like:

- “Why is that important?”
- “What does that protect?”
- “What failure does that prevent?”
- “What trade-off are you willing to make for that?”
- “What would you refuse even if it made implementation faster?”
- “What local move should the architecture make impossible?”

### 5. Game-theoretic pressure

For every meaningful design preference, test the incentives.

Ask:

- “Who benefits from this shortcut?”
- “Who pays the cost later?”
- “What would a tired engineer do under deadline pressure?”
- “What would a future maintainer infer from this interface?”
- “What would an attacker or malformed input exploit?”
- “What does this API make easy?”
- “What does this API make impossible?”
- “What information does the caller need to choose correctly?”
- “Is the desired behavior incentive-compatible?”
- “What equilibrium does this create after 20 future changes?”

### 6. Socratic pressure

Expose assumptions with questions like:

- “What would prove this design wrong?”
- “Where could this create coupling?”
- “What invariant would this fail to protect?”
- “What lifecycle state is being hidden?”
- “What is the single source of truth?”
- “What is the thing this abstraction actually hides?”
- “What are we trading away?”

### 7. QFT-style question selection

Before asking the round:

1. Generate more candidate questions than you need.
2. Prefer divergent questions early.
3. Prefer convergent questions when locking decisions.
4. Choose the five questions that reduce the most uncertainty.
5. Include at least one question that tests whether you are asking the right questions.

Do not show the internal list. Show only the final five questions.

### 8. Active-listening summary

At the start of each round after the first, briefly reflect the current understanding:

```markdown
## Current understanding
- Problem:
- Players:
- Incentives:
- Constraints:
- Values:
- Non-goals:
- Open uncertainty:
```

Keep it short. If the user corrects the summary, update the model before continuing.

## What to lock

Keep interviewing until all sections below are clear.

### Problem shape

- What is wrong?
- Who or what feels the pain?
- What concrete failure has happened or is likely?
- What is the root cause, not just the symptom?
- What invariant is being violated?
- What must remain true?
- What constraints are hard?
- What constraints are preferences?
- What does success look like?
- What does failure look like?

### Game board

Lock:

- players
- incentives
- actions available to each player
- information asymmetries
- local shortcuts
- global costs
- repeated-game risks
- adversarial players
- coordination failures
- desired equilibrium

Example players:

- current implementer
- future maintainer
- caller
- adapter author
- reviewer
- user
- attacker
- external service
- database
- job runner
- CI
- product owner

### Architectural values

Explore at least:

- first-principles reasoning
- minimal code
- composition over inheritance
- single source of truth / DRY as knowledge
- deep modules
- information hiding
- separation of concerns
- no complecting
- single responsibility
- dependency inversion
- ports/adapters
- functional core, imperative shell
- state at edges
- state machines for lifecycle
- invalid states unrepresentable
- typed errors
- no silent fallbacks
- explicit typed recovery
- Effect primitives in Effect-owned code
- performance
- observability
- testability
- security / least privilege
- extensibility without speculative abstraction
- incentive-compatible interfaces

For each important value, determine:

- mandatory or contextual
- what it forbids
- what trade-off the user accepts to preserve it
- what exception is allowed, if any
- what bad local incentive it corrects

### Non-goals

Lock what the architecture should not do.

Examples:

- no speculative framework
- no generic plugin system
- no inheritance tree
- no broad manager/service layer
- no silent fallback behavior
- no hidden defaults
- no migration outside current scope
- no rewrite beyond the target boundary
- no mechanism that relies on future engineers “just knowing”

### Solution direction

Clarify where the user's head is at without designing the full architecture.

Lock:

- preferred shape
- rejected shapes
- expected modules or seams
- expected mechanism/incentive change
- state/lifecycle expectations
- ports/adapters expectations
- pure core vs effectful shell split
- expected use of Effect
- performance-sensitive path
- migration expectations

### Decision criteria

Lock how `/architect` and `/review` should judge success.

Examples:

- smallest architecture that protects the invariant
- no new abstraction unless it hides volatility
- state machine required for lifecycle
- no raw Promise orchestration in Effect-owned code
- no fallback unless typed and observable
- review must reject shallow modules
- correct behavior is the cheapest behavior
- misuse is impossible, typed, or loud
- future maintainers have enough information to choose correctly

## Round format

Ask five questions at a time.

Use this exact shape:

```markdown
## Current understanding
<omit in first round unless useful>

## Questions

### 1. <question>
Recommended answer: <your recommendation>

### 2. <question>
Recommended answer: <your recommendation>

### 3. <question>
Recommended answer: <your recommendation>

### 4. <question>
Recommended answer: <your recommendation>

### 5. <question>
Recommended answer: <your recommendation>
```

Rules:

- Each numbered item must be one question.
- Do not hide multiple unrelated questions inside one item.
- The recommended answer should be opinionated but short.
- If the recommendation depends on unknown codebase facts, say what should be explored instead of guessing.
- If the user answers only some questions, continue with the unanswered questions plus the next highest-value questions.
- If the user says “yes” to all recommendations, treat those decisions as locked.

## Codebase exploration rule

If the answer is discoverable from the repo, do not ask.

Explore instead for:

- existing modules and naming conventions
- prior implementations
- tests
- package/library usage
- existing architecture boundaries
- existing Effect patterns
- current fallback/error handling
- existing state models
- performance-sensitive paths
- prior migrations
- existing incentive traps
- repeated review findings
- learning files

Then ask only about values, preferences, incentives, and trade-offs the code cannot reveal.

## Contradiction handling

If the user gives conflicting preferences, stop the normal round and ask five reconciliation questions.

Examples:

- “You want Open/Closed extensibility but also minimal code. Where should extensibility be allowed?”
- “You want no fallbacks but also high availability. Should recovery be modeled as typed failover?”
- “You want functional core but also rich domain objects. Which wins?”
- “You want performance but also extra abstraction. What is the budget?”
- “You want the implementer to move fast, but the reviewer to enforce architecture. What mechanism keeps both incentives aligned?”

## Locking behavior

When the following are all clear, stop asking questions:

- one-sentence problem
- affected users/systems
- root cause
- players
- incentives
- information asymmetries
- desired equilibrium
- mandatory constraints
- contextual constraints
- architectural values
- non-goals
- failure modes
- solution direction
- review criteria
- unknowns that `/architect` must ground in code/docs

Then output:

```markdown
## Core shape

### Problem
<one sentence>

### Root cause
<short statement>

### Game board
- Players:
- Incentives:
- Information asymmetries:
- Bad equilibrium:
- Desired equilibrium:

### Constraints
- <constraint>

### Architectural values
- <mandatory/contextual values>

### Non-goals
- <non-goal>

### Solution direction
<short statement>

### Review criteria
- <criteria /review must enforce>

### Grounding required for /architect
- <repo/docs/library facts to verify>
```

End with exactly this line and stop:

> Core shape locked. Run `/architect` to ground any missing edge cases and re-derive the simplest architecture from first principles.
