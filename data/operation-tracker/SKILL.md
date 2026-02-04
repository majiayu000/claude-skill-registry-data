---
name: operation-tracker
description: Maintain awareness of operation counts across the conversation to prevent cumulative context exhaustion. Use when you notice multiple operations accumulating or when working on iterative tasks across turns.
allowed-tools:
  - Task
  - AskUserQuestion
---

<objective>
Maintain awareness of operation patterns across the conversation to prevent cumulative context exhaustion.

The per-turn threshold is a trap—it's the CONVERSATION-LEVEL accumulation that kills sessions. This skill helps Claude track operations and recognize when to delegate.
</objective>

<quick_start>
<mental_tracking>
Before each operation, mentally note:

1. **Reads since last Task**: How many files have I read directly since my last Task delegation?
2. **Edits since last Task**: How many edits have I made since my last Task delegation?
3. **Same-file turns**: Am I iterating on the same file across multiple turns?
4. **Continue loops**: Is the user saying "continue" or similar repeatedly?

If any count exceeds threshold → delegate remaining work.
</mental_tracking>

<thresholds>
| Metric | Threshold | Action |
|--------|-----------|--------|
| Reads since last Task | ≥2 | Task(Explore) for remaining reads |
| Edits since last Task | ≥3 | Task(general-purpose) for remaining edits |
| Consecutive same-file turns | ≥3 | Suggest delegation to user |
| "Continue" cycles | ≥3 | Delegate remaining refinements |
| Context usage | >50% | All remaining work to subagents |
</thresholds>
</quick_start>

<iteration_patterns>
<pattern name="Continue Loop">
<description>
User keeps saying "continue", "keep going", "more", etc.
Each turn adds context without triggering delegation consideration.
</description>

<recognition>
- User message is short (1-3 words)
- Last response included edits/implementation
- Pattern repeating for 3+ turns
</recognition>

<response>
After 3 continue cycles:
"I've been iterating directly for [N] turns. To preserve context for the rest of our session, I'll delegate remaining refinements to a subagent."

Then delegate via Task(general-purpose).
</response>
</pattern>

<pattern name="Edit Accumulation">
<description>
Each turn has 1-2 edits (under per-turn threshold), but conversation accumulates many.
</description>

<recognition>
- Count edits since last Task delegation
- Each turn passes individual check
- Cumulative count exceeds threshold
</recognition>

<tracking_method>
Mental checklist at start of each turn:
- "Since my last Task delegation, I've done [N] edits"
- If N ≥ 3: "I should delegate remaining edits"
</tracking_method>
</pattern>

<pattern name="Read Chain">
<description>
Sequential file reads to understand a feature/bug, loading each file into context.
</description>

<recognition>
- Reading file A to understand something
- Then reading file B because A referenced it
- Then reading file C because B imported it
- Each read seemed necessary individually
</recognition>

<reality>
This is EXPLORATION. Should have been Task(Explore) from the start.
After 2 reads: delegate remaining exploration.
</reality>
</pattern>

<pattern name="Same-File Iteration">
<description>
Making repeated changes to the same file across multiple turns.
</description>

<recognition>
- Turn 1: Edit file X
- Turn 2: User feedback, edit file X again
- Turn 3: More feedback, edit file X again
- Each edit is small, but cumulative context grows
</recognition>

<response>
After 3 turns on same file:
"We've been iterating on [file] for several turns. Would you like me to delegate remaining refinements to preserve main context?"
</response>
</pattern>
</iteration_patterns>

<regression_detection>
<description>
Notice when you start a task with proper delegation but gradually revert to direct execution.
</description>

<pattern>
1. Task starts: "I'll use Task(Explore) to find..." ✓
2. Explore returns results
3. Next step: "Let me just quickly read..." ✗
4. Then: "I'll make this small edit..." ✗
5. Then: "One more fix..." ✗
6. Result: Main context exhausted
</pattern>

<recognition>
Ask yourself:
- Did I start this task with Task delegation?
- Am I now doing direct tool calls?
- Is this "cleanup" or "verification" or "quick fix"?

If yes to all three: you're regressing.
</recognition>

<correction>
Return to delegation mode:
"I started with delegation but have been doing direct operations. Let me delegate the remaining work."

Task(general-purpose): "Complete the remaining [work description]"
</correction>
</regression_detection>

<context_checkpoints>
<checkpoint name="After Exploration">
After any exploration phase (Grep, Glob, multiple Reads):
- Check: Did I load significant content into context?
- If yes: Delegate action phase to preserve context
</checkpoint>

<checkpoint name="After Task Returns">
When a Task returns results:
- Check: Do I need to do follow-up work?
- If yes: Is it debug/fix work? → New Task
- Don't slip into direct execution for "just cleaning up"
</checkpoint>

<checkpoint name="After User Feedback">
When user provides feedback/correction:
- Check: How many iterations have we done on this file/feature?
- If ≥3: Suggest delegation
</checkpoint>

<checkpoint name="Mid-Session">
Periodically during long sessions:
- Check: How much context have I used?
- If approaching 50%: Shift to all-subagent mode
- Use /context command to verify
</checkpoint>
</context_checkpoints>

<communication_templates>
<template name="Threshold Reached">
"I've done [N] [operations] since my last delegation. To preserve context for the rest of our session, I'll delegate the remaining [work type]."
</template>

<template name="Iteration Suggestion">
"We've been iterating on [target] for [N] turns. Would you like me to delegate remaining refinements to a subagent? This will help preserve context for other work."
</template>

<template name="Regression Correction">
"I notice I've been doing direct operations after initially delegating. Let me return to delegation mode for the remaining work."
</template>

<template name="Context Warning">
"Context usage is approaching [X]%. I'll delegate all remaining work to subagents to ensure we can complete the session."
</template>
</communication_templates>

<anti_patterns>
<pattern name="Per-Turn Tunnel Vision">
**Wrong**: Checking thresholds only within current turn
**Right**: Track cumulative operations since last Task delegation
</pattern>

<pattern name="Silent Accumulation">
**Wrong**: Doing 10 operations without mentioning delegation consideration
**Right**: Acknowledge when approaching thresholds, delegate proactively
</pattern>

<pattern name="Threshold Forgetting">
**Wrong**: Starting fresh count each turn
**Right**: Maintain mental count across the conversation
</pattern>

<pattern name="Continue Compliance">
**Wrong**: Infinitely complying with "continue" requests via direct execution
**Right**: After 3 cycles, delegate remaining work
</pattern>

<pattern name="Regression Blindness">
**Wrong**: Not noticing shift from delegation to direct execution
**Right**: Periodically check if you've regressed from initial delegation
</pattern>
</anti_patterns>

<success_criteria>
The tracking is working when:

- You can mentally state operation counts at any point
- Delegation happens BEFORE thresholds are exceeded
- Iteration loops are recognized and addressed
- Regression from delegation is caught and corrected
- Long sessions maintain consistent context usage
- User is informed when delegation decisions are made
</success_criteria>

<integration>
<with_delegate_first>
`delegate-first` provides the DECISION framework.
`operation-tracker` provides the AWARENESS mechanism.

delegate-first answers: "Should this be delegated?"
operation-tracker answers: "Have I accumulated too much?"

Use together: delegate-first for new operations, operation-tracker for ongoing awareness.
</with_delegate_first>
</integration>
