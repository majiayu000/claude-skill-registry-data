---
name: codex-discuss
description: >
  Consult Codex CLI (OpenAI) to get a second opinion on difficult problems. Use when facing
  complex debugging, architectural decisions, algorithm design, or any hard problem where
  cross-checking with another AI model would be valuable. Triggers on requests like "ask codex",
  "get a second opinion", "discuss with codex", "cross-check this", or when you determine that
  consulting another model would help solve a particularly challenging task.
---

# Codex Discuss

Consult Codex CLI to get alternative perspectives on hard problems. This enables multi-model
reasoning — use it to cross-check solutions, get fresh ideas, or break through when stuck.

## When to Use

- **Hard debugging**: You've been going in circles and need a fresh perspective
- **Architectural decisions**: Multiple valid approaches exist and you want to compare reasoning
- **Algorithm design**: Complex logic where a second opinion reduces risk of subtle bugs
- **Cross-checking**: Verify your solution approach before committing to implementation
- **Brainstorming**: Generate diverse ideas for solving an open-ended problem

## How to Invoke Codex

Use the Bash tool to run Codex in non-interactive mode:

```bash
command codex exec -s read-only "YOUR PROMPT HERE"
```

### Key Flags

| Flag | Purpose |
|------|---------|
| `codex exec "prompt"` | Non-interactive execution (required) |
| `-m MODEL` | Choose model (e.g., `-m o3`, `-m o4-mini`, `-m codex-mini-latest`) |
| `-C DIR` | Set working directory for context |
| `-s read-only` | Sandbox: read-only access (safest for analysis) |
| `-s workspace-write` | Sandbox: allow writes to workspace |
| `--dangerously-bypass-approvals-and-sandbox` | Full access (already aliased in this sandbox) |

### Important Notes

- The sandbox has a shell alias that adds `--dangerously-bypass-approvals-and-sandbox` automatically,
  which overrides any `-s` sandbox flag. To enforce read-only mode, bypass the alias with `command`:
  `command codex exec -s read-only "prompt"`.
- All examples below use `command codex exec` to bypass the alias and enforce read-only sandboxing,
  since this skill is for analysis and opinions, not file modifications.
- Codex has access to the same `/workspace` directory, so it can read your codebase.
- If you need Codex to write files, drop the `command` prefix and `-s` flag to use the auto-approve alias.

## Workflow

### Step 1: Formulate the Question

Write a clear, self-contained prompt. Include:
- The specific problem or question
- Relevant context (file paths, error messages, constraints)
- What kind of answer you want (analysis, code, comparison, etc.)

**Good prompt example:**
```
I'm debugging a race condition in /workspace/src/server.ts where concurrent WebSocket
connections cause duplicate entries in the session store. The store uses a Map with no
locking. What are the best approaches to fix this in Node.js without adding Redis?
Explain trade-offs of each approach.
```

### Step 2: Run Codex

```bash
command codex exec -s read-only "YOUR DETAILED QUESTION"
```

For questions that need codebase context:
```bash
command codex exec -s read-only -C /workspace "Analyze the error handling in src/api/ and suggest improvements. Focus on consistency and missing edge cases."
```

### Step 3: Analyze and Synthesize

After receiving Codex's response:

1. **Compare**: How does Codex's approach differ from yours?
2. **Evaluate**: Which points are strong? Which have gaps?
3. **Synthesize**: Combine the best ideas from both perspectives
4. **Present**: Share the synthesized conclusion with the user

### Step 4: Follow-up (Optional)

If the first response raises new questions, run another query. Each invocation is a new
session (no memory of prior queries), so include the relevant context:

```bash
command codex exec -s read-only "Context: For a race condition in a Node.js session store, approach X was suggested (using AsyncLocalStorage). How would that interact with Y constraint (multiple worker threads)? Compare with approach Z (mutex locks). What are the trade-offs?"
```

## Discussion Patterns

### Pattern A: Problem Solving
```bash
# Ask Codex for its approach
command codex exec -s read-only "Given this problem: [DESCRIPTION]. What's the best approach? Consider [CONSTRAINTS]."
```
Then compare with your own analysis and present a unified recommendation.

### Pattern B: Code Review Cross-Check
```bash
# Ask Codex to review specific code
command codex exec -s read-only -C /workspace "Review the implementation in [FILE_PATH]. Look for bugs, performance issues, and edge cases. Be specific with line numbers."
```
Then merge findings with your own review.

### Pattern C: Architecture Decision
```bash
# Present options and ask for analysis
command codex exec -s read-only "We need to choose between: (A) [OPTION_A], (B) [OPTION_B], (C) [OPTION_C]. Context: [REQUIREMENTS]. Analyze trade-offs and recommend one."
```
Then present both your reasoning and Codex's to the user.

### Pattern D: Brainstorming
```bash
# Open-ended idea generation
command codex exec -s read-only "Suggest 5 different approaches to [PROBLEM]. For each, give a 2-sentence description and list pros/cons."
```

## Output Handling

- Codex output can be long. Focus on extracting the key insights.
- If the output is truncated, the important parts are usually at the beginning.
- When presenting results to the user, clearly attribute which ideas came from Codex vs your own analysis.
- Frame it as a collaborative discussion, not just forwarding another model's output.

## Example: Full Discussion Flow

```
User: "This recursive function is too slow for large inputs. Help me optimize it."

1. [You analyze the function first and form your own opinion]
2. [Run Codex]:
   command codex exec -s read-only -C /workspace "The recursive function in src/utils/tree.ts:45
   has O(2^n) complexity. Suggest optimization strategies — consider memoization,
   iterative conversion, and any algorithmic improvements. Show code examples."
3. [Compare Codex's suggestions with your analysis]
4. [Present to user]:
   "I analyzed this from two angles. My approach would be X because...
    Codex suggested Y, which has the advantage of...
    Combining both, I recommend Z because..."
```
