---
name: summarization
description: Comprehensive session wrap-up and continuity checkpointing workflow.
  Generates a standalone copy-pasteable initialization prompt, captures decisions,
  records current setup status, and lists next steps before session end.
argument-hint: '[session wrap-up prompt]'
---

<!-- Generated from workflows/summarization.md by tools/generate_integrations.py. Edit the source file, not this one. This is an execution WORKFLOW packaged as an Agent Skill so it is discoverable and directly invocable ("/summarization") in every compatible tool. -->

# Workflow: Session Summarization

## When to Use
| Criteria | Match |
|----------|-------|
| Trigger | user requests it OR token budget reaches critical |
| Context | any workflow, any mode — ending a session |
| Power Mode | Critical |
| Priority | HIGH — preserves work across sessions |

## Required Skills
- memory-management
- communication-tone
- codebase-understanding (GitNexus) — for tracking what changed

## Flow

### Step 0: Thinking Stage (Pre-Action)
- [ ] Why am I summarizing? User request, token limit, or session end?
- [ ] Do I have `detect_changes()` data for all modifications this session?
- [ ] What information is CRITICAL for the next session to continue?
- [ ] Prioritize: initialization prompt > decisions > current state > remaining tasks

### Step 1: Detect Trigger
- User says "summarize" / "wrap up" / "continue next session"
- OR token budget is critically low (<10% remaining)
- OR you estimate remaining work will exceed remaining token budget

### Step 2: Gather Current State
- Read todo_write list (current progress)
- Run `detect_changes()` to see all modifications in this session
- Collect key decisions made during the conversation
- Note any unresolved issues or blockers

### Step 3: Summarize Using Standard Prompt

```
We will end our session here. Please output a detailed, exhaustive summary of our entire conversation to prepare for the next session. Include everything we have discussed, what we have agreed on, the current state of the conversation, and the status of the project setup (such as files, infrastructure, or configurations). Provide this as a continuity summary so another session can pick up exactly where we left off. 
Begin your response with a standalone initialization prompt that I can copy and paste into a new session. This initialization prompt must follow this structure: "You are an expert assistant specializing in... You are working on a project involving..., and here is the context of where we left off: [Insert Context Here]."
Additionally, include a specific instruction within that prompt directing the AI to perform a full project scan (covering code, architecture, or configuration files) to fully understand the current setup. Proceed with the output text now. Thank you.
```

### Step 4: Summary Structure
The summary MUST include:

1. **Initialization Prompt** (standalone, ready to copy-paste into a new session)
   - Must strictly follow structure: `"You are an expert assistant specializing in... You are working on a project involving..., and here is the context of where we left off: [Insert Context Here]."`
   - Includes explicit instruction: `"Perform a full project scan (covering code, architecture, or configuration files) to fully understand the current setup before proceeding."`
   
2. **What Was Discussed**
   - Everything discussed, feature/task description
   - Key decisions agreed on
   - Alternatives considered and rejected
   
3. **Current State & Project Setup**
   - Status of project setup (files, infrastructure, configurations)
   - What's working / verified
   - What's still pending / broken
   
4. **What's Left & Next Steps**
   - Remaining tasks from the todo list
   - Known issues or blockers
   - Next steps in priority order

### Step 5: Render Response in Text (DO NOT Output to File)
- Render the complete continuity summary and initialization prompt directly in visible response TEXT.
- DO NOT output the summary to a file (do not write to `.kiro/session-summary.md` or any disk file).
- Never echo or display the instruction prompt string itself in the response.

## Token Budget
- **Summary itself**: 2K-5K tokens (maximize useful context within budget)
- If budget is critically low: output the most essential information first — initialization prompt, current state, next steps — in that priority order

## GitNexus Integration
- `detect_changes()` — critical for tracking what was modified
- `status` — verify index state
- Any index-worthy updates (if significant code changes were made, recommend re-running `npx gitnexus analyze` in next session)

## Hallucination Watchpoints
- Omitting important decisions
- Inaccurate state descriptions
- Forgetting blockers/issues that were encountered
- Summary too brief to be useful for continuation
- Not including the initialization prompt for the next session
