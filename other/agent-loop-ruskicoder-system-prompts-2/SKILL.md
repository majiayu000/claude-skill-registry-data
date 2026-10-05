---
name: agent-loop
description: Continuous autonomous agent execution loop for open-ended, complex, or
  emergent multi-step tasks. Iterates through assessment, single tool execution, observation,
  and state updating until the task goal is fully resolved.
argument-hint: <task goal or prompt>
---

<!-- Generated from workflows/agent-loop.md by tools/generate_integrations.py. Edit the source file, not this one. This is an execution WORKFLOW packaged as an Agent Skill so it is discoverable and directly invocable ("/agent-loop") in every compatible tool. -->

# Workflow: Agent Loop

## When to Use
| Criteria | Match |
|----------|-------|
| Intention | open_ended, complex_feature, new_app |
| Complexity | unknown scope, multi-step, needs autonomy |
| Power Mode | Balanced or Deep |
| Clarity | requirements may be vague or emergent |

## Required Skills
- ALL skills may be needed (composed dynamically)
- Minimum: file-operations + code-execution + codebase-understanding + communication-tone + safety-profiles

## Flow

### Loop Structure
The agent operates in a continuous loop until the task is fully resolved:

```
while task_not_complete:
    1. Assess current state (what's done, what's left)
    2. Determine next action
    3. Execute action (tool call)
    4. Review result
    5. If progress: continue
    6. If stuck: reassess approach
    7. If complete: yield control
```

### Step 0: Thinking Stage (Pre-Action - Every Iteration)
Before EVERY action in the loop:
- [ ] What is the current state vs the goal? *(Manus planner)*
- [ ] Have I read the relevant context? NEVER act on assumptions
- [ ] What ONE thing should I do next to make progress?
- [ ] Am I still working toward the original goal? (Scope check)
- [ ] Do not assume the outcome of any tool use. Each step must be informed by the previous step's result. *(Cline)*

### Step 1: Task Initialization
- Read all provided context
- Create todo list for the task
- Run `gitnexus analyze` if index is stale
- READ `gitnexus://repo/{name}/context` for codebase overview
- `query({search_query})` for initial understanding

### Step 2: The Loop
Each iteration:
1. **Assess**: what is the current state vs goal?
2. **Plan next step**: what one thing should I do next?
3. **Execute**: make one tool call
4. **Review**: did it work? what did I learn?
5. **Update**: mark todo items complete, add new ones if discovered
6. **Continue or stop**: if resolved, exit loop; otherwise continue

### Step 3: Tool Calling Rules
- Only call tools when necessary (general questions don't need tools)
- If you say you'll use a tool, call it immediately as your next action
- Explain why before calling each tool
- For async tools: wait for output before proceeding
- NEVER call tools that aren't explicitly provided

### Step 4: Progress Tracking
- Update todo_write after every meaningful step
- Create memories for important context
- Use detect_changes() periodically to track what's changed
- After every 3-5 tool calls: pause and give a brief checkpoint

### Step 4b: Sanity Check (Every 3-5 iterations)
- [ ] Is the task actually complete? *(Cursor: "Only terminate when sure the problem is solved")*
- [ ] Have I introduced any regressions?
- [ ] `detect_changes()` — verify scope
- [ ] Are there lingering issues or partial implementations?
- [ ] Is this a loop I've been stuck in? (Check hallucination detectors)
- [ ] Verify: run relevant tests, check linter

### Step 5: Completion
- Task is done when user's request is FULLY resolved
- Verify with tests/linter
- `detect_changes()` to confirm scope
- Yield control back to user
- Do NOT stop prematurely for status updates

## Token Budget
- **Typical**: 20K-100K+ tokens
- **Max recommended**: 150K tokens
- **Warning**: check token usage after every 5 tool calls
- **Critical**: >150K → offer session summarization to user

## GitNexus Integration — Continuous
- `query` — understanding as you explore
- `context` — before editing unfamiliar symbols
- `impact` — before potentially breaking changes
- `detect_changes` — periodic verification
- `check` — structural integrity validation

## Hallucination Watchpoints
- **Tool loop**: calling the same tool repeatedly with no progress
- **File edit oscillation**: editing the same file >3× without resolution
- **Scope creep**: task expanding beyond original intent
- **Premature optimization**: solving problems that don't exist yet
- **Analysis paralysis**: researching forever without making changes
- **Orphaned code**: creating files/functions that nothing references

### Recovery Actions
If any watchpoint triggers:
1. STOP all tool calls
2. Summarize what happened
3. Report to user: what was observed, what was tried, what didn't work
4. Ask for guidance

## Autonomy Principles
- Be proactive — don't ask permission for research or context gathering
- Be decisive — if unsure between two approaches, pick one and proceed
- Be thorough — don't leave partial implementations
- Be safe — flag destructive operations for user approval
- Be efficient — don't over-engineer, don't over-investigate
