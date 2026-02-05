---
name: Querying Web Search Agent
description: This skill guides the process of creating context-free queries for a web search agent (another Claude instance with web search tools). Use this when you need expert guidance from web research but the search agent has no access to the codebase or conversation history.
allowed-tools: [Write, Read, Edit]
---

# Querying Web Search Agent

This skill provides a structured approach to writing effective queries for a web search agent - a separate Claude instance that has web search tools but no access to your codebase or conversation context.

## What This Skill Does

- Creates standalone query documents with complete context
- Structures technical problems for optimal web research
- Includes all necessary details without assuming shared knowledge
- Produces markdown files ready to copy-paste to the search agent

## When to Use This Skill

Use this workflow when:
- You're stuck on a technical problem and need web research
- You want expert guidance from documentation, forums, or official sources
- The problem requires understanding of tools/libraries/platforms
- You need best practices or configuration recommendations
- You're debugging an error message or unexpected behavior

**Key indicator**: You say "feel free to draft a new query" or "let's ask the web searcher"

## Core Principle

The web search agent operates **independently** - it has:
- ✅ Web search tools (can find documentation, Stack Overflow, GitHub issues, etc.)
- ✅ General technical knowledge up to its training cutoff
- ❌ **NO** access to your codebase
- ❌ **NO** access to conversation history
- ❌ **NO** context about your environment or setup

Therefore, queries must be **completely self-contained**.

## Query Structure Template

Every query should follow this structure:

### 1. Title
Clear, specific problem statement (not "Help with X" but "X Fails with Y Error in Z Context")

### 2. Problem Summary (2-3 sentences)
Concise description of what's happening and why you need guidance.

### 3. Current Configuration
Include:
- Tool versions (specific numbers)
- Environment details (OS, containerization, etc.)
- Relevant configuration files (show actual config)
- Command-line flags or environment variables

### 4. The Symptom
Show:
- Exact error messages (copy-paste from logs)
- Unexpected behavior descriptions
- What's working vs what's not
- Log excerpts with timestamps and line numbers

### 5. What We've Tried
Document previous attempts:
- List each approach chronologically
- Show what changed (specific flags, config, etc.)
- State the result of each attempt
- Note any partial progress

### 6. Specific Questions
Frame 3-5 focused questions:
- Start with "Why does X happen when Y?"
- Ask "What's the correct configuration for Z?"
- Request "What flags should we use for A?"
- Avoid vague questions like "How do we fix this?"

### 7. Additional Context
Provide:
- Deployment environment (Docker, Kubernetes, bare metal)
- Constraints (no GUI, limited resources, etc.)
- Parallel execution considerations
- Known issues or past problems in this area

### 8. What We Need
Explicitly state:
- Root cause explanation
- Specific configuration/flags to change
- Documentation references or examples
- Alternative approaches if primary approach has issues

## Workflow Steps

### Step 1: Identify the Query Trigger

User says something like:
- "Feel free to draft a new query"
- "We should ask the web searcher"
- "Let's get expert guidance on this"
- "Can you write up a query for this?"

### Step 2: Create the Query File

```bash
# Use descriptive filename in current project directory
touch ci-optimization-[specific-problem]-query.md
```

**Naming convention**: `[project-prefix]-[problem-area]-[specific-issue]-query.md`

Examples:
- `ci-optimization-chromium-headless-query.md`
- `ci-optimization-angle-xcb-query.md`
- `ci-optimization-cdp-port-query.md`

### Step 3: Write Self-Contained Context

Remember: The search agent **cannot see**:
- Your codebase files
- Previous conversation
- Environment setup
- Tool output from this session

**Bad query** (assumes context):
```markdown
# The ports don't match

We're having the issue we discussed earlier. Can you help?
```

**Good query** (self-contained):
```markdown
# Cypress CDP Port Mismatch with Parallel Chromium Instances

## Problem Summary

Running Cypress 14.5.4 with Chromium 120 in parallel (3 instances) in Docker CI.
Chromium launches successfully and DevTools opens ports, but Cypress cannot
connect because it tries to connect to different ports than what Chromium opened.

## Current Configuration

Environment: Docker container, Debian 11.11, no X11

Chromium flags (via cypress.config.ts):
```javascript
'--headless=new',
'--ozone-platform=headless',
'--remote-debugging-port=0',  // Auto-select port
...
```

[... rest of complete context ...]
```

### Step 4: Include Concrete Evidence

Don't say "it fails" - show:
- Actual log lines with line numbers
- Error messages in full
- Conflicting values (opened ports vs attempted ports)
- Timing information (if relevant)

### Step 5: Document Iteration History

Show what you've tried:
```markdown
## What We've Tried

### Attempt 1: Include --remote-debugging-port=0
- Added flag via before:browser:launch hook
- Result: Port mismatch (same issue)

### Attempt 2: Remove --remote-debugging-port=0
- Let Cypress handle ports automatically
- Result: Port mismatch (same issue)

### Attempt 3: Consolidate all flags in config
- Moved ALL flags to cypress.config.ts
- Result: Port mismatch (same issue)
```

This helps the search agent understand:
- What doesn't work (avoiding duplicate suggestions)
- Patterns in the failures
- Your debugging sophistication level

### Step 6: Ask Focused Questions

Structure questions to get actionable answers:

**Good questions**:
- "Why does Cypress try to connect to different ports than DevTools opens?"
- "How should --remote-debugging-port=0 work with Cypress in parallel runs?"
- "What's the correct way to configure debugging ports for parallel Cypress instances?"
- "Are there known issues with Cypress 14.x + --remote-debugging-port=0?"

**Avoid vague questions**:
- "Can you help?"
- "What should we do?"
- "How do we fix this?"

### Step 7: State What You Need

Be explicit about the desired outcome:
```markdown
## What We Need

1. Root cause: Why does Cypress try wrong ports?
2. Correct configuration: Specific flags or settings to change
3. Best practice: Recommended approach for parallel Cypress runs
4. Workarounds: If current approach won't work, what alternatives exist?
```

### Step 8: Save and Inform User

After writing the query:
1. Save the file
2. Tell the user: "I've created [filename] - it's ready to send to the web searcher!"
3. Summarize what the query asks for

## Real-World Examples

### Example 1: GPU/Graphics Issue
```markdown
# Chromium ANGLE XCB Errors in Headless Mode - GPU Backend Selection

## Current Situation
Running Cypress 14.5.4 with Chromium 120 in headless mode on Linux (Debian 11.11)
in Docker CI environment. We've successfully eliminated Xvfb and got Chromium to
launch with headless Ozone platform, but now hitting GPU/ANGLE initialization errors.

[... complete configuration ...]

## The Errors
[... exact error messages with line numbers ...]

## What We've Tried
[... iteration history ...]

## Questions
1. Why is ANGLE trying to use XCB/X11 backends even though we specified
   --ozone-platform=headless and --disable-gpu?
2. What additional flags do we need to force Chromium to use software rendering
   without any X11 dependencies?
[... more focused questions ...]
```

### Example 2: Port Mismatch Issue
```markdown
# Cypress CDP Port Mismatch with Parallel Chromium Instances

## Problem Summary
Chromium launches and DevTools opens ports, but Cypress tries to connect to
**different ports** than what Chromium opened.

[... full details with evidence ...]

## What We've Tried
[... 3 documented attempts ...]

## Questions
1. Why does Cypress try to connect to different ports than DevTools opens?
[... more questions ...]

## What We Need
Specific configuration for parallel Cypress runs with correct port handling.
```

## Best Practices

### DO:
- ✅ Include exact version numbers (Cypress 14.5.4, Chromium 120, not "latest")
- ✅ Copy-paste error messages verbatim
- ✅ Show configuration files as code blocks
- ✅ Document iteration history (what didn't work)
- ✅ Ask specific, actionable questions
- ✅ State your constraints (Docker, no GUI, parallel execution)
- ✅ Request concrete outputs (flags, commands, config snippets)

### DON'T:
- ❌ Assume the agent knows about your codebase
- ❌ Reference "the issue we discussed earlier"
- ❌ Say "as you can see" (they can't see anything)
- ❌ Use vague descriptions like "it doesn't work"
- ❌ Ask only "how do we fix this?" (too broad)
- ❌ Omit environment details (OS, containerization, versions)
- ❌ Skip showing what you've already tried

## Common Pitfalls

### Pitfall 1: Assuming Shared Context
**Bad**: "The ports still don't match"
**Good**: "Chromium opened ports 46009, 44093, 38263 but Cypress tried 40289, 33475, ..."

### Pitfall 2: Vague Problem Statements
**Bad**: "Cypress isn't working"
**Good**: "Cypress fails to connect to Chrome DevTools Protocol with ECONNREFUSED after 62 retry attempts"

### Pitfall 3: Missing Version Numbers
**Bad**: "We're using Cypress and Chrome"
**Good**: "Cypress 14.5.4 with Chromium 120 on Debian 11.11"

### Pitfall 4: No Iteration History
**Bad**: "We tried some things but it didn't work"
**Good**: "Attempt 1: Added --flag=value, result: Same error. Attempt 2: Removed --flag, result: Different error [specific details]"

### Pitfall 5: Only Asking "Why"
**Bad**: "Why is this happening?"
**Good**: "Why is this happening? What flags should we change? What's the recommended configuration? Are there known workarounds?"

## Verification

After creating a query, check:

- [ ] Title clearly states the problem
- [ ] Version numbers are exact and specific
- [ ] Configuration is shown (not just described)
- [ ] Error messages are copy-pasted verbatim
- [ ] Iteration history shows what didn't work
- [ ] Questions are specific and actionable
- [ ] Constraints are stated (Docker, no GUI, etc.)
- [ ] No references to "as discussed" or "this codebase"
- [ ] File is saved with descriptive name

## Processing the Response

When the user pastes the web search response:

1. **Read the response file**
2. **Extract actionable recommendations**
   - Specific flags to add/remove
   - Configuration changes
   - Environment variables
3. **Implement changes systematically**
   - One logical change at a time
   - Test after each change
   - Update your own iteration notes
4. **Update documentation** with learnings
5. **If still failing**: Create a follow-up query referencing the first query and new findings

## Related Skills

- **Creating Claude Code Skills** - For turning repeated patterns into skills (like this one!)

## Tips for Success

1. **Be generous with context** - Err on the side of too much detail
2. **Show, don't tell** - Code blocks > descriptions
3. **Number your attempts** - Makes iteration history clear
4. **Copy-paste errors exactly** - Don't paraphrase or summarize
5. **Ask multiple questions** - Give the agent several angles to explore
6. **State your constraints** - No GUI, container, parallel execution, etc.
7. **Request specific outputs** - Flags, commands, config snippets, not just explanations

Remember: The web search agent is very knowledgeable but completely ignorant of your specific situation. Your query is their only window into the problem!
