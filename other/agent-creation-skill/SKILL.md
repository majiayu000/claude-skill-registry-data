---
name: AGENT-CREATION
description: Use for creating high-quality Claude Code subagents
# Optional additional metadata can be included here
---

# Agent Creation Skill

## Overview
This skill guides the creation of high-quality agent definition files that produce reliable, predictable agent behavior. Use this when creating new agents or refactoring existing ones that aren't performing as expected.

## When to Use This Skill
- Creating a new specialized agent
- Fixing an agent that ignores instructions
- Refactoring an agent that produces inconsistent results
- Upgrading agent instructions for better reliability
- Reviewing agent files for quality issues

## Core Principles of Effective Agent Design

### 1. **Critical Rules First**
The most important instructions MUST appear at the very top of the agent file in a "CRITICAL RULES" section. Agents can suffer from "instruction decay" where later instructions override earlier ones, or important rules get lost in verbose descriptions.

**Structure:**
```markdown
## CRITICAL RULES - READ FIRST
⚠️ **[RULE 1]** - Brief explanation
⚠️ **[RULE 2]** - Brief explanation
⚠️ **[RULE 3]** - Brief explanation
```

### 2. **Explicit > Implicit**
Never rely on the agent to "understand" or "infer" what you mean. State everything explicitly:

❌ **BAD:** "Be careful with user data"
✅ **GOOD:** "NEVER log user passwords, API keys, or PII. Sanitize all user input before processing."

❌ **BAD:** "Fix issues properly"
✅ **GOOD:** "When asked to fix a feature, repair the existing code - do NOT remove or rewrite the feature."

### 3. **Directive Language**
Use strong, commanding language that leaves no room for interpretation:

**Use these patterns:**
- "You MUST..."
- "NEVER..."
- "ALWAYS..."
- "DO NOT..."
- "You are REQUIRED to..."

**Avoid these patterns:**
- "You should..."
- "Try to..."
- "It's recommended..."
- "Consider..."
- "Ideally..."

### 4. **Structured Response Protocols**
Give agents a step-by-step protocol to follow. This prevents them from skipping crucial steps:
```markdown
## Response Protocol (Follow This Order)

### Step 1: [Action]
- Specific substep
- Specific substep

### Step 2: [Action]
- Specific substep
- Specific substep
```

### 5. **Concrete Examples**
Show don't tell. Include examples of both good and bad behavior:
```markdown
❌ **WRONG:**
[Show the problematic behavior]

✅ **CORRECT:**
[Show the desired behavior]
```

## Agent File Structure Template
```markdown
---
name: agent-name
description: "Brief, clear description of agent purpose"
model: sonnet  # or opus for complex reasoning
color: [color]
tools: [if applicable]
---

# [Agent Name]

## CRITICAL RULES - READ FIRST
⚠️ **[MOST IMPORTANT RULE]** - Why it matters
⚠️ **[SECOND MOST IMPORTANT]** - Why it matters
⚠️ **[THIRD MOST IMPORTANT]** - Why it matters
[Include 3-7 critical rules maximum - prioritize ruthlessly]

## MANDATORY: Tool Usage Requirements
[If your agent must use specific MCP tools, specify exactly when and how]

**BEFORE [doing X], you MUST:**
1. Use `tool-name` to [specific action]
2. Verify [specific criteria]
3. Proceed only if [specific condition]

**CRITICAL: Think hard** [if extended thinking is required for this agent]

## Your Mission
[2-3 sentence clear statement of what this agent does and why it exists]

## [Protocol/Process Name] (Follow This Order)

### Step 1: [First Action]
✅ **You MUST:**
- [Specific required action]
- [Specific required action]

❌ **NEVER:**
- [Specific forbidden action]
- [Specific forbidden action]

### Step 2: [Second Action]
✅ **You MUST:**
- [Specific required action]

❌ **NEVER:**
- [Specific forbidden action]

[Continue for all steps...]

## Response Format
[Specify exact format/structure for agent outputs if applicable]
```
[Provide a template the agent should follow]
```

## Absolute Standards

**YOU MUST [COMPLY WITH/DO]:**
- [Non-negotiable requirement]
- [Non-negotiable requirement]

**YOU DO NOT:**
- [Unacceptable behavior]
- [Unacceptable behavior]

## Examples

### Example 1: [Scenario]
**User Request:** [What user said]

**Correct Response:**
[Show ideal agent response]

**Why This Works:** [Brief explanation]

---

### Example 2: [Scenario]
**User Request:** [What user said]

**Incorrect Response:**
[Show wrong agent response]

**Why This Fails:** [Brief explanation]

**Correct Response:**
[Show ideal agent response]

## Edge Cases & Special Situations

### When [Situation]
[Specific instructions for handling this case]

### If [Condition]
[Specific instructions for handling this case]

## Final Verification
Before completing any task, verify:
1. ✅ [Verification checkpoint]
2. ✅ [Verification checkpoint]
3. ✅ [Verification checkpoint]

If you cannot answer "YES" to all checkpoints, [what should agent do].
```

## Common Agent Creation Pitfalls

### Pitfall 1: Buried Critical Instructions
❌ **PROBLEM:** Important rules are in the middle or bottom of a long file
✅ **SOLUTION:** Put all critical rules in a "CRITICAL RULES - READ FIRST" section at the top

### Pitfall 2: Vague Tool Usage Instructions
❌ **PROBLEM:** "Use the search tool when appropriate" or "Think hard"
✅ **SOLUTION:** "BEFORE analyzing any code, you MUST use search-tool to find X, Y, Z. Think hard about non-obvious vulnerabilities."

### Pitfall 3: Weak Language
❌ **PROBLEM:** "Try to avoid removing features"
✅ **SOLUTION:** "NEVER remove features to fix them. If something is broken, FIX it, don't delete it."

### Pitfall 4: Missing Response Structure
❌ **PROBLEM:** Agent rambles or provides inconsistent output formats
✅ **SOLUTION:** Provide explicit response format template the agent must follow

### Pitfall 5: No Examples
❌ **PROBLEM:** Agent misinterprets abstract instructions
✅ **SOLUTION:** Include 2-3 concrete examples showing correct and incorrect behavior

### Pitfall 6: Conflicting Instructions
❌ **PROBLEM:** One section says "be creative" another says "follow the plan exactly"
✅ **SOLUTION:** Ensure all instructions are consistent and prioritize clearly

### Pitfall 7: Assuming Context
❌ **PROBLEM:** "Handle errors properly" (agent doesn't know what "properly" means in your context)
✅ **SOLUTION:** "Every async operation MUST have try-catch. Log all errors with context. Never expose stack traces to users."

### Pitfall 8: No Verification Mechanism
❌ **PROBLEM:** Agent completes tasks without checking its work
✅ **SOLUTION:** Include "Final Verification" checklist agent must complete before responding

## MCP Tool Integration

When your agent needs to use MCP tools, be extremely explicit:

### Pattern for Required Tools
```markdown
## MANDATORY: [Tool Name] Usage

**BEFORE [action], you MUST:**
1. Use `tool-name` with these parameters:
   - parameter1: [what to include]
   - parameter2: [what to include]
2. Verify the results contain [specific criteria]
3. If results are [condition], then [action]

**Search queries to run:**
- "[specific query]"
- "[specific query]"
- [Any domain-specific terms from [context]]
```

### Pattern for Optional Tools
```markdown
## WHEN TO USE [Tool Name]

Use `tool-name` when:
- [Specific trigger condition]
- [Specific trigger condition]

DO NOT use `tool-name` when:
- [Specific condition where tool is not appropriate]
```

### Extended Thinking Trigger
If your agent needs extended thinking mode:
```markdown
**CRITICAL: Think hard** about [specific aspects] before [action]
```

## Testing Your Agent

After creating an agent file, test it with:

1. **The Happy Path:** Give it a straightforward task it should handle well
2. **The Tricky Path:** Give it an ambiguous request to see if it asks for clarification
3. **The Forbidden Path:** Ask it to do something it should refuse
4. **The Edge Case:** Test boundary conditions and special cases
5. **The Stress Test:** Give it a complex multi-step task

### Red Flags During Testing
- Agent skips critical steps
- Agent produces placeholder/fake code
- Agent removes features instead of fixing them
- Agent ignores specific instructions
- Agent provides inconsistent output formats
- Agent doesn't use required tools

**If you see any red flags:** The instructions need to be more explicit, more directive, or moved higher in the file.

## Agent File Checklist

Before deploying an agent file, verify:

- [ ] Critical rules are in a "CRITICAL RULES - READ FIRST" section at the top
- [ ] All instructions use directive language (MUST, NEVER, ALWAYS)
- [ ] No vague or ambiguous instructions
- [ ] Response format is explicitly specified (if applicable)
- [ ] Required MCP tools have explicit usage instructions
- [ ] At least 2 concrete examples included
- [ ] Step-by-step protocol is provided for complex tasks
- [ ] "Final Verification" checklist is included
- [ ] No conflicting instructions
- [ ] Edge cases are addressed
- [ ] Testing has been completed with multiple scenarios

## Refactoring Existing Agents

When an agent isn't working properly:

### Step 1: Identify the Problem
- What is the agent doing wrong?
- What should it be doing instead?
- Which instructions is it ignoring?

### Step 2: Locate Instruction Issues
- Are critical instructions buried?
- Is the language too weak?
- Are instructions ambiguous?
- Are there conflicting directions?

### Step 3: Apply Fixes
- Move critical rules to the top
- Strengthen language (should → MUST)
- Add concrete examples
- Add verification checkpoints
- Make implicit rules explicit

### Step 4: Test Thoroughly
- Retest with the scenarios where it previously failed
- Try new edge cases
- Verify it doesn't break existing good behavior

## Real-World Examples

### Example: Fixing a Code Agent That Removes Features

**Problem:** Agent removes broken features instead of fixing them

**Diagnosis:** Instructions were too passive and buried in the file

**Fix Applied:**
```markdown
## CRITICAL RULES - READ FIRST
⚠️ **NEVER REMOVE FEATURES TO FIX THEM** - If something is broken, FIX it, don't delete it
⚠️ **FIX MEANS FIX** - When asked to fix a feature, repair the existing code, don't rewrite or remove it
```

**Result:** Agent now consistently fixes instead of removes

---

### Example: Fixing an Agent That Skips Tool Usage

**Problem:** Agent ignores instructions to use search tool

**Diagnosis:** Tool usage instructions were vague ("use when appropriate")

**Fix Applied:**
```markdown
## MANDATORY: Search Tool Usage

**BEFORE making any recommendations, you MUST:**
1. Use `search-tool` to find:
   - [Specific query 1]
   - [Specific query 2]
   - [Specific query 3]
2. Review all search results
3. Base recommendations on search findings

**This is NOT optional.** Skipping search leads to incomplete analysis.
```

**Result:** Agent now consistently uses search tool

## Advanced Techniques

### Technique 1: Progressive Restriction
For agents that need creativity in some areas but strictness in others:
```markdown
## Creative Freedom Areas
For [specific tasks], you MAY:
- [Allowed freedom 1]
- [Allowed freedom 2]

## Strict Compliance Areas
For [specific tasks], you MUST:
- [Required behavior 1]
- [Required behavior 2]

**When in doubt, err on the side of strictness.**
```

### Technique 2: Escalation Protocol
For agents that should ask for help when uncertain:
```markdown
## When to Escalate

**Immediately ASK the user for clarification if:**
- [Uncertainty condition 1]
- [Uncertainty condition 2]

**DO NOT guess or make assumptions.** Asking is always better than producing incorrect results.
```

### Technique 3: Self-Correction Mechanism
Help agents catch their own mistakes:
```markdown
## Before Responding - Self-Check

Review your response and verify:
1. Did I [specific check]?
2. Did I avoid [specific mistake]?
3. Is my [output component] [specific quality]?

If any answer is "NO", revise your response before sending.
```

## Summary

Great agent files are:
- **Clear:** No ambiguity in instructions
- **Directive:** Use commanding language
- **Structured:** Step-by-step protocols
- **Explicit:** All rules stated clearly
- **Tested:** Verified to work in practice
- **Prioritized:** Most important rules first
- **Concrete:** Examples over abstractions

Poor agent files are:
- Vague and open to interpretation
- Using weak suggestive language
- Unstructured walls of text
- Relying on agent "understanding"
- Untested assumptions
- Burying critical rules
- All abstract, no examples

**The golden rule:** If an agent can misinterpret your instruction, it will. Make it impossible to misinterpret.