---
name: state-transition-testing
description: >
  Apply this skill whenever you need to design test cases using State Transition Testing.
  Use when given requirements describing a system whose behavior depends on its current
  state AND its history of events — not just the current input alone. Triggers include:
  "design test cases", "test state machine", "test workflow", "test lifecycle", "state
  transition", "FSM", or any requirement describing: user authentication flows, account
  lifecycles, order/transaction workflows, session management, multi-step wizards, embedded
  system controllers, or any feature where the same event produces different outcomes
  depending on what happened previously.
---

# State Transition Testing Skill

## Overview

**State Transition Testing** is a black-box test design technique for systems where the **output depends not only on the current input but also on the system's prior history** — i.e., its current state. The system is modeled as a **Finite State Machine (FSM)** —
a set of states, events that trigger transitions between states, guard conditions that qualify transitions, and actions (observable outputs) produced during transitions.

**Core purpose:** Systematically derive test cases that cover all meaningful paths through a system's state space — including paths the system should correctly reject — ensuring no state, transition, or invalid combination is left untested.

The technique produces two complementary artifacts before any test cases are written:

- **State Transition Diagram (STD):** Visual representation of the FSM — states as nodes, transitions as directed arrows.
- **State Transition Table (STT):** Exhaustive grid of all state × event combinations, exposing both valid transitions and invalid transitions that the diagram alone cannot surface.

→ For full theoretical background, see [`resources/theory.md`](resources/theory.md).

## Invoke Syntax

```
/state-transition-testing [--file="path/to/output.md"]
```

**Modes:**

| Mode                   | Syntax                                                 | Behavior                                                                                                                               |
| ---------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| Default (conversation) | `/state-transition-testing`                            | All analysis, diagrams, tables, and test cases printed inline in the conversation as Markdown                                          |
| File output            | `/state-transition-testing --file="path/to/output.md"` | All output (STD description, STT, Test Path Plan, Test Case Suite) written to the specified file. AI confirms the path before writing. |

**Notes:**

- `--file` mode requires a file-capable environment (e.g., claude.ai with computer tools enabled). If file tools are unavailable, AI will notify the user and fall back to conversation output.
- The path in `--file` is the desired output location. If the file already exists, AI will ask before overwriting.
- Both modes produce identical content — only the delivery differs.
- `--file` can be combined with any input: `/state-transition-testing --file="path/to/output.md"` then paste the requirements.

## When to Use

- System behavior depends on **prior history** — the same event produces different outcomes depending on what happened before.
- Requirements describe **object/entity lifecycles** — account states, order statuses, session states, subscription tiers.
- Requirements describe **multi-step workflows** with defined entry/exit conditions per step — authentication flows, checkout wizards, approval pipelines.
- Requirements describe **embedded or hardware-driven systems** — device controllers, ATMs, protocol state machines.
- **Any requirement using lifecycle language:** "can only be done after", "once X, the system allows Y", "if already in state Z, reject event W".

**Key signal:** If the same user action (e.g., "Submit") produces different system responses depending on what the user did previously — State Transition Testing is the right technique.

## When NOT to Use

- System is **stateless** — output depends only on current input, not history (static pages, simple calculators, pure lookup functions).
- Complexity lies in **variation of input data values**, not sequence of events → use **Domain Testing (EP/BVA)** instead.
- Complexity lies in **combinations of simultaneous conditions** at one point in time → use **Decision Table Testing** instead.
- Complexity lies in **end-to-end user scenarios** crossing multiple features → use **Use Case Testing** instead.
- Do **not** use State Transition Testing alone as a complete test strategy — combine with Domain Testing for input validation within states, and Error Guessing for additional invalid paths.

## Inputs Required

Before applying this skill, you must have:

1. **Functional requirements or business rules (BR)** describing system states and the events that cause changes between them
2. **Entity or object lifecycle description** — what conditions define each state, and what events are valid or invalid per state
3. **Expected system behavior** per transition: both the destination state and the observable action (output, message, error)
4. **Guard conditions** where applicable — boolean rules that qualify when a transition fires
5. _(Optional but valuable)_ UI/API specifications that confirm which events are exposed in which states

## Core Principles

1. **Model before testing:** The STD and STT are mandatory analytical artifacts — derive them from requirements before writing any test case.
2. **States are mutually exclusive:** A system exists in exactly one state at any point in time — no overlapping states.
3. **Completeness of the table:** The STT must include every state × event combination — valid AND invalid — with no gaps.
4. **Invalid transitions are first-class tests:** Testing what the system correctly rejects is as important as testing valid paths.
5. **Coverage is explicit:** Define the target coverage level before deriving test cases; coverage drives what is sufficient.
6. **Test paths, not individual transitions:** A single test case may traverse multiple transitions sequentially — optimize paths to cover maximum transitions with minimum test cases.
7. **Preconditions are mandatory:** Every test case must specify the exact starting state — a test without a defined precondition is not executable.

## Design Process

Follow these steps sequentially. Do not skip any steps.

### Step 1 — Analyze Requirements and Identify FSM Components

Parse all requirements, BRs, and user stories. Extract:

- **States:** Distinguishable conditions in which the system can exist. **Look for:** status fields (`ACTIVE`, `SUSPENDED`), lifecycle stages (Draft, Submitted, Approved), named phases (Logged Out, Logged In, Locked). Exclude intermediate processing steps that are not observable.
- **Events:** Triggers that cause the system to evaluate and potentially change state. **Look for:** user actions (Submit, Cancel, Pay), system triggers (timeout, scheduled job), external inputs (payment gateway response).
- **Guard Conditions:** Boolean rules that qualify when an event causes a specific transition. **Format:** `[condition]`. **Look for:** "only if", "provided that", "when".
- **Actions:** Observable outputs produced during a transition. **Look for:** messages displayed, records updated, emails sent, redirect targets.
- **Initial State and Final State(s):**
  - The **initial pseudostate** (not a real state) defines where the FSM starts. The first real state is the one entered from the initial pseudostate.
  - **Final states** are states from which no further transitions are possible for the modeled scope.

Document findings in the **FSM Component List** before drawing anything.

→ See [`resources/fsm-components-guide.md`](resources/fsm-components-guide.md) for extraction patterns and examples.

### Step 2 — Construct the State Transition Diagram (STD)

Build the visual model of the FSM:

1. Draw each state as a node (circle or rectangle).
2. Mark the initial pseudostate (solid filled circle → arrow → first state).
3. Mark final states (double-bordered node or bullseye symbol).
4. Draw directed arrows for each valid transition, labeled: `Event [Guard] / Action`.
5. Include self-transitions (reflexive transitions) where applicable — an event that returns the system to the same state it is already in.
6. Verify that every state is reachable from the initial state; every non-final state has at least one outgoing transition.

In text/Markdown environments, represent the STD as a **labeled transition list** or **Mermaid diagram** (primarily used). The STD must be reviewed with stakeholders before proceeding.

→ See [`resources/std-stt-guide.md`](resources/std-stt-guide.md) — **Part 1:** STD for notation standards and construction rules.

### Step 3 — Construct the State Transition Table (STT)

Build the exhaustive analytical grid:

1. Rows = every state (one row per state)
2. Columns = every unique event identified across all states
3. Each cell = the result of applying that event in that state:
   - **Valid transition:** destination state + action
   - **Invalid transition:** mark as `—` with expected system response (error message, no-op, rejection)
4. **Verify:** cell count = number of states × number of events; no cell left blank or undefined

The STT exposes all **invalid transitions** — combinations the diagram does not show because they are not valid paths, but which the system must still handle gracefully.

→ See [`resources/std-stt-guide.md`](resources/std-stt-guide.md) — **Part 2:** STT for table format, notation, and invalid transition handling.

### Step 4 — Select Coverage Level and Define Test Paths

Choose the coverage target based on risk and context:

| Coverage Level                          | Definition                                                             | When to Use                                                          |
| --------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **All States Coverage**                 | Every state visited ≥ 1 time                                           | Smoke/sanity testing only; lowest rigor                              |
| **All Transitions Coverage (0-switch)** | Every valid transition exercised ≥ 1 time                              | Baseline for most commercial functional testing                      |
| **Invalid Transitions Coverage**        | Every invalid state×event combination tested ≥ 1 time                  | Always combine with All Transitions; required for security/stability |
| **1-Switch Coverage**                   | Every valid pair of consecutive transitions (A→B→C) exercised ≥ 1 time | High-risk systems; catches context carry-over bugs                   |
| **N-Switch Coverage**                   | Every valid sequence of N+1 consecutive transitions                    | Safety-critical systems; exponential test count growth               |

**Define test paths:** A test path is a sequence of transitions from a starting state to an ending state. One test case implements one test path. Optimize by designing paths that cover multiple transitions in a single journey — this is more efficient than one transition per test case.

→ See [`resources/coverage-guide.md`](resources/coverage-guide.md) for path optimization strategies and N-switch derivation.

### Step 5 — Derive Test Cases from Test Paths

Translate each test path into one executable test case:

- **Precondition:** The exact state the system must be in before the test begins. This is mandatory — a test case without a precondition is not executable.
- **Steps:** The sequence of events to trigger, in order, including any required input data per event.
- **Expected result per step:** The observable action (output, message, state change) after each event — not just the final state.
- **Postcondition:** The state the system should be in after the test completes.
- **Validity:** Whether this test case exercises a valid path (positive) or an invalid transition (negative).
- **Coverage:** Which transitions (or transition pairs for N-switch) this test case covers.

→ Use [`resources/output-template.md`](resources/output-template.md) for the recommended test case format.

### Step 6 — Review Against Quality Checklists

Before finalizing, verify the test suite against the **Test Case Quality Checklist** in [`resources/quality-checklist.md`](resources/quality-checklist.md).

## Design Rules

| Rule                                                | Description                                                                                                           |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **STD before STT**                                  | Always construct the diagram before the table — the diagram defines valid transitions; the table adds invalid ones    |
| **STT before test cases**                           | Test cases are derived from the STT, not directly from the STD — the table ensures invalid transitions are not missed |
| **Precondition is mandatory**                       | Every test case must specify the exact starting state — "system is in state X" is not optional                        |
| **Expected result per step**                        | In multi-step test cases, specify the expected observable outcome after each event, not just the final state          |
| **No undefined cells in STT**                       | Every state × event combination must have a defined response — blank = incomplete analysis                            |
| **Coverage target before derivation**               | Define the coverage level before writing any test case — coverage drives what is sufficient                           |
| **Self-transitions must be explicit**               | An event that leaves the system in the same state is a real transition and must appear in the STT and be covered      |
| **Final states have no valid outgoing transitions** | If a "final state" has outgoing transitions in the modeled scope, it is not actually final                            |

## Anti-Patterns

→ Full detail: [`resources/anti-patterns.md`](resources/anti-patterns.md)

**Critical anti-patterns:**

- **Skipping the STT and deriving test cases directly from the STD** — the STD cannot surface invalid transitions; skipping the STT means negative testing is purely intuitive and incomplete
- **Missing the precondition** — test cases without a defined starting state cannot be reliably executed or reproduced
- **Treating "initial" as a real state** — the initial pseudostate is not a state the system can return to; modeling it as a state produces incorrect transitions
- **Testing only valid transitions (no invalid transition coverage)** — leaves all negative paths untested; security and stability defects concentrate in invalid transitions
- **One test case per transition (not optimizing paths)** — inefficient; a single path through multiple states covers multiple transitions and is easier to execute and maintain
- **Leaving STT cells blank or undefined** — incomplete analysis; undefined behavior is a specification gap, not a reason to skip
- **Not verifying the STD with stakeholders** — diagram assumptions are often wrong; discrepancies with developers or POs discovered after test case design waste significant rework

## Best Practices

→ Full detail: [`resources/best-practices.md`](resources/best-practices.md)

**Key best practices:**

- Always **review the STD with the team** (developer + PO + QA) before proceeding — the diagram is a specification tool, not just a testing tool.
- Use **path optimization**: design test paths that traverse multiple transitions in one journey; this is more efficient and closer to real user behavior.
- **Combine All Transitions + Invalid Transitions coverage** as the minimum baseline for functional testing — 0-switch alone is insufficient.
- For range-based events (e.g., "Withdraw [Amount <= Balance]"), combine with EP/BVA to select specific test data values within each guard condition class.
- **Label every transition completely**: Event, Guard Condition (if any), and Action — partial labels produce ambiguous test cases.
- Always specify **expected intermediate states and actions**, not just the final state — defects often occur during the transition, not at the destination.
- Document **why** specific invalid transitions exist — rationale enables accurate error message verification.

## Process Quality Checklist

_Use this to verify the design methodology was applied correctly — before reviewing individual test cases._

- [ ] All states identified and described — no two states have identical behavior for all events.
- [ ] All events identified — including system-generated events (timeouts, async callbacks) not just user actions.
- [ ] All guard conditions identified and documented with their boolean logic.
- [ ] All actions (observable outputs) identified per transition.
- [ ] Initial pseudostate and all final states identified; initial pseudostate is NOT modeled as a real state.
- [ ] STD constructed before the STT; every state is reachable from the initial pseudostate.
- [ ] Every non-final state has at least one outgoing valid transition in the STD.
- [ ] Self-transitions explicitly modeled where the system stays in the same state.
- [ ] STT constructed with rows = all states, columns = all events; no blank cells.
- [ ] All invalid state × event combinations documented with expected system response.
- [ ] Coverage target selected before deriving test cases, with documented rationale.
- [ ] Test paths optimized — multiple transitions covered per test case where possible.
- [ ] Every test case has an explicit precondition (starting state).
- [ ] STD reviewed with at least one stakeholder (PO, developer, or BA) before test case derivation.

→ For the full **Process Quality Checklist** should be verified, see [`resources/quality-checklist.md`](resources/quality-checklist.md).

## Common Rationalizations to Reject

- _"The diagram already shows what to test — I don't need the table"_ → The diagram shows only valid paths; invalid transitions are invisible in the diagram and only surface in the table
- _"The invalid combinations are obvious — the developer wouldn't make those mistakes"_ → Invalid transition defects are among the most common in stateful systems; "obvious" is not a testing criterion
- _"The starting state doesn't matter — the tester will figure it out"_ → Without a defined precondition, tests are non-deterministic; two testers running the same test case may start from different states and get different results
- _"Each transition needs its own test case — I'll be thorough"_ → One transition per test case is inefficient and fails to catch context carry-over bugs; path optimization is both more efficient and more revealing
- _"We don't have time for invalid transition tests"_ → Invalid transition coverage is a quality gate, not optional — security and stability defects are disproportionately found in untested invalid paths

## Red Flags

Stop and re-evaluate the design if you observe:

- The STT has blank or "TBD" cells — incomplete analysis; do not proceed to test case derivation.
- Every state × event combination is marked "valid" — either the system truly has no invalid transitions (very rare) or the analysis is incomplete.
- A test case has no precondition — it is not executable; add the starting state before proceeding.
- The number of test cases equals the number of valid transitions — path optimization was not applied; paths are likely being tested as isolated single-transition cases.
- A "state" in the STD has no outgoing transitions and is not a designated final state — either it is an incomplete specification or a modeling error.
- The same event appears in only one state's row in the STT — events are typically applicable (valid or invalid) across multiple states; missing rows may indicate a gap.

## Output

The design process produces:

1. **FSM Component List** — states, events, guard conditions, actions, initial and final states, all traced to requirements
2. **State Transition Diagram (STD)** — visual FSM model; in text environments, represented as labeled transition list or Mermaid diagram
3. **State Transition Table (STT)** — exhaustive state × event grid with valid/invalid marking and expected actions
4. **Coverage Plan** — selected coverage level with rationale; list of test paths to be implemented
5. **Test Case Suite** — using the template in [`resources/output-template.md`](resources/output-template.md)

## Examples

→ [`examples/order-lifecycle.md`](examples/order-lifecycle.md) — E-commerce order status lifecycle: multi-state workflow with guard conditions, self-transitions, invalid transitions, All Transitions + Invalid Transitions coverage
