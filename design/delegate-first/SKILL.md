---
name: delegate-first
description: Behavioral principle for context preservation through strategic delegation. Use when starting multi-step operations, uncertain about scope, or when direct execution might exhaust context. Complements never-guess and resolve-ambiguity skills.
allowed-tools:
  - Task
  - AskUserQuestion
  - Read
---

<objective>
Establish Claude's behavioral principle: **Delegate by default. Execute directly only when certainty is absolute.**

Main context tokens are MORE valuable than subagent tokens. Subagent contexts are ephemeral and infinitely spawnable. Main context exhaustion = session death.

This skill governs delegation decisions. It complements `never-guess` (don't fabricate when uncertain about facts) and `resolve-ambiguity` (how to gather missing information).
</objective>

<quick_start>
<core_principle>
Before executing ANY operation, verify absolute certainty:

1. **Do I have exact file path(s)?** (Not function name, not directory, not pattern)
2. **Is this 1-2 tool calls with predictable output?**
3. **Have I done fewer than 3 direct operations since last delegation?**

If ANY answer is NO → Delegate via Task tool.
</core_principle>

<certainty_definition>
**CERTAIN** (execute directly):
- User provides EXACT file path: "Edit src/auth/login.ts line 50"
- Single file, single operation, path in hand
- Output size is predictable and small

**UNCERTAIN** (delegate):
- User provides function/class name without path
- User provides directory or category ("all files in X")
- User provides error message without file location
- Scope is unknown (could be 1 file or 20)
- Output size is unpredictable or large

Rule: If you would need Grep/Glob/Read to find the location, you don't have certainty—you have a search needle.
</certainty_definition>
</quick_start>

<delegation_traps>
<trap name="Specificity Trap">
<description>
User gives specific request but you don't know WHERE or HOW MANY.
</description>

<example>
User says: "Fix the getUserById bug"
- FALSE confidence: You know WHAT to fix
- REALITY: You don't know WHERE (which file) or HOW MANY locations
</example>

<signal>
Specific request WITHOUT exact file path(s)
</signal>

<action>
Task(Explore): "Find all locations where getUserById is defined or called, identify the bug"
</action>

<anti_pattern>
Starting Grep/Glob directly in main context to "quickly find" the location.
This loads search results into main context—the search itself should be delegated.
</anti_pattern>
</trap>

<trap name="Debug-After-Delegation Trap">
<description>
You correctly delegated implementation, but revert to direct debugging when issues arise.
</description>

<pattern>
1. You delegated implementation to subagent ✓
2. Subagent returns with errors or integration issues
3. You think "let me quickly fix this" ✗
4. 33 direct operations later, main context exhausted
</pattern>

<reality>
Debugging is often MORE complex than initial implementation.
The "quick fix" illusion is the highest-risk moment.
</reality>

<rule>
**If you delegated creation, delegate fixing.**
</rule>

<action>
Task(luc:fix-phase): "Fix these issues from the implementation phase: [list errors]"
</action>

<recognition>
When you notice yourself about to do direct edits after a Task returned with issues, STOP.
Create a new Task for the fix phase.
</recognition>
</trap>

<trap name="MCP Tool Blindspot">
<description>
Large-output MCP tools load massive content into main context that cannot be "unseen."
</description>

<dangerous_tools>
- Analyzers: dart analyze, eslint, tsc --noEmit, pylint
- Test runners: pytest, jest, flutter test, cargo test
- Build tools: flutter build, npm run build, cargo build
- Linters with file output
</dangerous_tools>

<example>
Direct call: mcp__dart__analyze_files → 98KB output into main context
Delegated: Task processes 98KB in its context, returns 500-token summary
</example>

<action>
Task(luc:output-analyzer): "Run dart analyze and fix all errors, report remaining warnings"
</action>

<rule>
NEVER call large-output MCP tools directly in main context.
Always wrap in Task for processing.
</rule>
</trap>

<trap name="Multi-Turn Iteration Trap">
<description>
Per-turn counting misses cumulative context waste across the conversation.
</description>

<pattern>
Turn 1: 1 edit (under threshold) ✓
Turn 2: 1 edit (under threshold) ✓
Turn 3: 1 edit (under threshold) ✓
...
Turn 10: 1 edit (under threshold) ✓
Result: 10 edits, significant context consumed, no delegation triggered
</pattern>

<tracking>
Track across the CONVERSATION, not per-turn:
- Reads since last Task delegation
- Edits since last Task delegation
- Consecutive turns working on same file
</tracking>

<thresholds>
| Metric | Threshold | Action |
|--------|-----------|--------|
| Reads since last Task | ≥2 | Task(Explore) |
| Edits since last Task | ≥3 | Task(general-purpose) |
| Same-file turns | ≥3 | Suggest delegation to user |
</thresholds>

<action>
After hitting threshold: "I've been working directly for [N] operations. To preserve context, I'll delegate the remaining work."
</action>
</trap>

<trap name="Research-to-Action Transition Trap">
<description>
The highest-risk moment: switching from research mode to action mode.
</description>

<research_indicators>
Recent turns contained:
- WebSearch calls
- Multiple Read operations
- Grep/Glob exploration
- Task(Explore) results
</research_indicators>

<action_indicators>
Current request contains:
- Edit/Write language ("update", "fix", "change", "remove", "add")
- Mutation verbs applied to researched content
- References to findings ("the files we found", "based on analysis")
</action_indicators>

<rule>
At research→action transition:
1. PAUSE before executing
2. DEFAULT to Task(general-purpose) for action phase
3. Do NOT execute directly regardless of apparent simplicity
</rule>

<example>
[Previous 5 turns: reading architecture docs, exploring codebase]
User: "Now update them to consolidate the duplications"

This is TRANSITION. Delegate the action phase.
Task(general-purpose): "Update architecture docs to consolidate duplications based on analysis"
</example>
</trap>
</delegation_traps>

<decision_tree>
<flow>
User Request Received
│
├─► Contains "find where", "review all", "search for", "what files"?
│   └─► YES → Task(Explore) IMMEDIATELY
│
├─► Has EXACT file path(s) provided by user?
│   ├─► YES + 1-2 predictable ops → Direct execution OK
│   └─► NO → Task(Explore) to find locations first
│
├─► Previous Task returned with errors/issues?
│   └─► YES → Task(luc:fix-phase) for fixes
│       DO NOT switch to direct debugging
│
├─► Will call large-output MCP tool (analyzer, test runner, build)?
│   └─► YES → Task(luc:output-analyzer) wrapper
│
├─► Done ≥2 Reads or ≥3 Edits since last Task?
│   └─► YES → Delegate remainder to Task
│
├─► Just finished research phase, now doing action?
│   └─► YES → Task(general-purpose) for action phase
│
└─► Single known file, 1-2 ops, small predictable output?
    └─► YES → Direct execution OK
</flow>
</decision_tree>

<delegation_targets>
<target name="Task(Explore)">
For: Finding locations, understanding scope, research
When: "Find where", unknown file paths, exploration needed
</target>

<target name="Task(general-purpose)">
For: Multi-file operations, implementation, action phases
When: Known scope but multiple files/edits needed
</target>

<target name="Task(luc:fix-phase)">
For: Debugging after delegated implementation
When: Previous Task returned with errors to fix
</target>

<target name="Task(luc:output-analyzer)">
For: Large-output MCP tool processing
When: Analyzers, test runners, build tools
</target>
</delegation_targets>

<integration>
<with_never_guess>
`never-guess` handles uncertainty about FACTS.
`delegate-first` handles uncertainty about SCOPE.

When uncertain about facts → never-guess → resolve-ambiguity
When uncertain about scope → delegate-first → Task delegation
</with_never_guess>

<with_resolve_ambiguity>
`resolve-ambiguity` gathers missing INFORMATION.
`delegate-first` protects CONTEXT during execution.

If you need to resolve ambiguity about what to do → resolve-ambiguity
If you know what to do but scope is uncertain → delegate-first
</with_resolve_ambiguity>
</integration>

<trade_off>
<principle>
False positives (unnecessary delegation) are acceptable.
Context exhaustion is not.

A Task that "wasn't necessary" costs ~500 tokens overhead.
Direct execution that exhausts context kills the session.

**Err toward delegation.**
</principle>
</trade_off>

<anti_patterns>
<pattern name="Quick Look Fallacy">
**Wrong**: "Let me quickly grep for this" (loads results into main context)
**Right**: Task(Explore): "Find where X is defined"
</pattern>

<pattern name="Just One More Edit">
**Wrong**: "I'll just make one more edit directly" (after 4 previous edits)
**Right**: "I've done several edits. Delegating remaining changes."
</pattern>

<pattern name="I Know What To Fix">
**Wrong**: Starting direct edits after subagent reported issues
**Right**: Task(luc:fix-phase) for the debugging work
</pattern>

<pattern name="Small Output Assumption">
**Wrong**: "dart analyze probably won't return much" (calls directly)
**Right**: Always assume MCP tools return large output; delegate
</pattern>

<pattern name="Research Complete, Now Execute">
**Wrong**: After 10 turns of research, doing direct edits
**Right**: Delegate the action phase after research
</pattern>
</anti_patterns>

<success_criteria>
The principle is working when:

- Main context stays under 50% for extended sessions
- Research phases delegate to Task(Explore)
- Implementation phases delegate to Task(general-purpose)
- Debug phases delegate to Task(luc:fix-phase)
- Large MCP outputs never enter main context
- Session longevity increases 3-5x for complex work
- Direct execution is rare exception, not default
</success_criteria>
