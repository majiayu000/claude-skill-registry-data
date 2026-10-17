---
name: report-flow
description: Summarize a workflow or process as an easy-to-read sequence of steps
argument-hint: "[scope]"
related:
  - report
  - suggest-next-action
---

## Goal

Summarize a process, workflow, or set of working steps as an easy-to-read step-by-step list that is trackable and reusable

## Scope

Use when explaining the flow of a process, algorithm, user journey, or task to others in sequence

## Execute

### 1. Identify Flow

> Goal: Identify the process to summarize

1. Take the topic or process from the user or context
2. Identify the trigger or starting point
3. Identify the output or ending point
4. Identify the stakeholders or systems involved

### 2. Extract Steps

> Goal: Break the process into steps

1. Collect all steps from the source (code, docs, conversation, observation)
2. Order them by time/dependency
3. Filter out duplicated or unnecessary steps
4. If there are branches or conditions → identify decision points

### 3. Structure Steps

> Goal: Write steps in an easy-to-read form

1. Use continuous numbering `1.`, `2.`, `3.`
2. If there are sub-steps, use `1.1`, `1.2`
3. Each step states the action, responsible party, input, and output
4. Use `>` for decisions/conditions, e.g. `> if X → do A, if not → do B`
5. If there is a loop → state the condition that repeats

### 4. Add Context

> Goal: Add information that helps understand the flow

1. State the tools/systems used in each step
2. State the important input/output data
3. State any conditions or constraints
4. State the failure path if any

### 5. Format And Report

> Goal: Present the flow nicely and usefully

1. Use `/report` to summarize the overview: Step, Action, Input, Output, Tool
2. Show the step sequence as a numbered list
3. If there are branches → use a nested list or ASCII flow chart
4. Run `/suggest-next-action`

## Rules

### 1. One Action Per Step

- Each step should have one clear action
- If there are multiple actions → split them
- Do not merge multiple systems together without stating it clearly

### 2. Deterministic Flow

- State the condition whenever there is a decision
- Do not guess the flow if the input is unclear
- If there are multiple options → state the default path

### 3. Reusability

- Use general language, not too tied to specific tools
- State inputs/outputs clearly for reuse
- Keep the flow in `docs/flows/` files if it should be reused

- Final report via `/report-review` — one chat table (No./Action/Evidence/Severity/Risk/Priority/Owner skill/Status), no report files

## Expected Outcome

- The process is summarized into continuous steps
- Each step has a clear action, input, and output
- Branches, loops, and decision points are identified
- Beautiful, easy-to-read report with a next action
