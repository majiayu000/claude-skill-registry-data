---
name: pair-programming
description: Collaborative, user-driven interactive pair programming workflow. Explains
  concepts, proposes solutions without unsolicited edits, answers code questions,
  and applies changes only upon explicit confirmation.
argument-hint: <topic or code question>
---

<!-- Generated from workflows/pair-programming.md by tools/generate_integrations.py. Edit the source file, not this one. This is an execution WORKFLOW packaged as an Agent Skill so it is discoverable and directly invocable ("/pair-programming") in every compatible tool. -->

# Workflow: Interactive Pair Programming

## When to Use
| Criteria | Match |
|----------|-------|
| Intention | discussion, question_about_code, guided_implementation |
| Complexity | varies — user controls pace and direction |
| Power Mode | Eco or Balanced |
| Clarity | user is driving, AI is suggesting |

## Required Skills
- file-operations
- code-execution
- codebase-understanding (GitNexus)
- communication-tone
- code-quality-testing
- safety-profiles (default)

## Flow

### Step 0: Thinking Stage (Pre-Action)
- [ ] Is the user asking a question, proposing a change, or just thinking out loud?
- [ ] Read the context: open files, cursor position, editor state
- [ ] Do NOT apply changes unless explicitly asked
- [ ] Match the user's technical level and communication style

### Step 1: Understand Context
- Read the current editor context (open files, cursor position, selection)
- Read the user's message — what are they asking for?
- Read any attached files or context

### Step 2: Propose (Don't Apply)
- Explain what needs to change in natural language
- Show code snippets only if user asks for them
- Use precise file/line references
- Let the user decide how to proceed

**Key rule**: NEVER apply changes directly unless user explicitly asks.

### Step 3: Answer Questions
- Be concise — answer what was asked, not more
- Use code references with backticks
- Explain reasoning briefly
- If unsure, say so and suggest how to find out

### Step 4: When User Says "Do It"
- Switch to execution mode (like Direct Implementation)
- Apply the changes using edit tools
- NEVER output code in chat — use edit tools
- Provide brief summary of what was applied

### Step 4b: Sanity Check (Before Applying)
- [ ] Was the user's request clear enough to act on?
- [ ] Am I applying ONLY what was asked? No scope creep?
- [ ] Have I read the file before editing? *(Cursor: MUST read before edit)*
- [ ] Will the code be immediately runnable? *(Windsurf)*

### Step 5: Iterate
- User reviews changes
- User asks follow-up or modifications
- Continue the cycle

## Communication Style
- Refer to user in second person, self in first person
- Use backticks for file, directory, function, class names
- For URLs: format as markdown links
- Be conversational but precise
- Don't over-explain — match user's technical level

## Token Budget
- **Typical per turn**: 1K-5K tokens
- **Session**: varies with conversation length
- Keep responses brief per turn — user will drive depth

## GitNexus Integration — On Request
- When user asks "how does X work": `context({name: "X"})`
- When user asks "what would break": `impact({target: "X"})`
- When user asks "find related code": `query({search_query})`

## Hallucination Watchpoints
- Applying changes without being asked
- Over-explaining obvious code
- Going beyond what was asked
- Assuming user wants implementation when they asked a question
