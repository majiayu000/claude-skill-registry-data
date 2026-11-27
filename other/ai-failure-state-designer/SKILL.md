---
name: ai-failure-state-designer
description: "Maps an Artificial Intelligence (AI) feature's failure modes - hallucination, refusal, low confidence, latency, partial results, tool errors, and outdated knowledge - to detection signals, User Interface (UI) patterns, recovery actions, and ready-to-use microcopy. Use when designing error states for a chatbot, copilot, or agent; users hit dead ends after an AI failure; writing refusal or fallback copy; or preparing a failure-handling spec before launch."
---

# AI Failure State Designer

> An AI feature is judged by how it fails, because it will fail more often and more strangely than deterministic software.

## What this skill is

A workflow that inventories the ways an AI feature can fail, separates failures the system can detect from those only the user can catch, and assigns each one a UI pattern, a recovery path, and microcopy. It replaces the generic "Something went wrong" with failure states that preserve work, explain what happened in plain terms, and give the user a next best action.

## What it solves

- Every AI failure collapsing into one generic error message
- Hallucinations presented with the same confidence and styling as correct answers
- Refusals that lecture the user or give no alternative path
- Long waits with a spinner and no sense of progress or option to stop
- Partial results discarded entirely when one step or tool call fails
- Answers based on outdated information with no date context

## When to invoke

- Designing a new chatbot, copilot, search assistant, or agent
- Support tickets describe dead ends, lost work, or "it just stopped"
- Writing or reviewing refusal and fallback copy
- Adding tool use or retrieval, which introduces new failure surfaces
- Launch readiness review requires a failure-handling spec

## Phase 1: Inventory failure modes

Start from this taxonomy and add product-specific modes:

| Failure mode | Definition | System-detectable? |
|--------------|-----------|---------------------|
| Hallucination | Fluent output that is false or unsupported | Partially (grounding checks, citation validation) |
| Refusal | Model declines a request, correctly or not | Yes |
| Low confidence | Answer produced but evidence is weak or conflicting | Partially (retrieval scores, self-consistency) |
| Latency | Response exceeds expected time | Yes |
| Partial result | Some steps or items succeeded, others failed | Yes |
| Tool or integration error | External call failed, timed out, or lacked permission | Yes |
| Outdated knowledge | Answer reflects stale data or training cutoff | Partially (source dates, time-sensitive topics) |
| Misunderstood intent | Correct answer to the wrong question | Rarely; usually user-detected |

## Phase 2: Rate frequency and impact

For each mode, estimate from evaluation data or logs:

```
Failure priority = Frequency (1-5) x Impact (1-5) x Detection difficulty (1-3)
Detection difficulty: 1 = system detects, 2 = user can easily notice, 3 = user unlikely to notice
```

Undetectable, high-impact failures (typically hallucination and outdated knowledge) rank highest because the interface is the only defense.

## Phase 3: Assign UI patterns

| Failure mode | Primary pattern | Supporting pattern |
|--------------|-----------------|--------------------|
| Hallucination | Inline citations with verify-on-hover; unsupported claims visually distinct | "Check this" prompt on high-stakes facts (numbers, names, dates) |
| Refusal | Brief reason plus nearest allowed alternative | Link to the human or manual path |
| Low confidence | Hedged phrasing plus clarifying question or multiple options | Show sources that conflict |
| Latency | Staged progress (step names, not just a spinner) and stop control | Stream partial output; offer "notify me when done" past 20 seconds |
| Partial result | Show completed items, mark failed items, offer retry on failures only | Summary line: "7 of 9 done" |
| Tool error | Name the system that failed in user terms; preserve inputs | Retry, use alternative source, or continue without |
| Outdated knowledge | "As of" date on time-sensitive answers | Offer to search current sources if available |
| Misunderstood intent | Restate interpretation for ambiguous requests | Easy edit-and-resend on the original prompt |

Latency thresholds to design for:

| Wait time | Treatment |
|-----------|-----------|
| Under 1 second | No indicator needed |
| 1-5 seconds | Typing or thinking indicator; stream tokens if possible |
| 5-20 seconds | Named stages ("Searching 3 sources", "Drafting") and a stop button |
| Over 20 seconds | Background the task, notify on completion, keep the user unblocked |

## Phase 4: Define recovery actions

Every failure state needs at least one forward action. Rank options by user effort:

1. **Automatic recovery** - silent retry or fallback model, only if the result is equivalent
2. **One-click recovery** - retry, try a narrower request, use a different source
3. **Guided recovery** - suggested rephrasing, clarifying question, or form fallback
4. **Manual path** - link to the non-AI way to do the job
5. **Human path** - handoff to support with context preserved

Rules: never discard user input; never retry silently more than twice; never auto-retry an action with side effects.

## Phase 5: Write the microcopy

Microcopy formula:

```
[What happened, plainly] + [What it means for the user] + [What they can do next]
```

| Failure | Weak copy | Strong copy |
|---------|-----------|-------------|
| Tool error | "An error occurred." | "I couldn't reach your calendar, so this schedule skips your meetings. Retry, or continue without calendar data." |
| Refusal | "I can't help with that." | "I can't change payroll records. I can draft the request for your payroll admin instead." |
| Low confidence | "I'm not sure." | "I found two conflicting policies (2023 and 2025). The 2025 version says 30 days. Want me to show both?" |
| Partial | "Task failed." | "Updated 7 of 9 records. 2 were locked by another user. Retry those 2?" |

Voice rules: first person for the assistant is acceptable, but no apologies longer than three words, no blaming the user, no anthropomorphic feelings ("I'm so sorry, I feel terrible"), and no technical codes in the primary message.

## Output

- Failure mode inventory with detectability and priority scores
- Pattern assignment table per failure mode
- Latency treatment spec with time thresholds
- Recovery action ladder per failure mode
- Microcopy library (primary message, secondary detail, action labels)
- Instrumentation list to measure each failure's frequency in production

## Operating rules

**Always**
- Design for undetectable failures, not just the ones the system can catch
- Preserve user input and completed work through every failure
- Pair every refusal with an alternative path
- Show progress stages and a stop control for long waits
- Date-stamp time-sensitive answers

**Never**
- Use a single generic error for all AI failures
- Style unverified claims identically to cited ones in high-stakes contexts
- Auto-retry actions that have side effects
- Blame the user's prompt in error copy
- Hide a partial failure inside a success message
