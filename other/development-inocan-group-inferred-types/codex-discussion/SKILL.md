---
name: codex-discussion
description: Use OpenAI Codex CLI as a discussion partner to verify ideas, evaluate plans, and improve quality. Automatically triggered during implementation planning, troubleshooting, debugging, or when seeking a second opinion on technical decisions.
---

# Codex Discussion Partner

Use the OpenAI Codex CLI as a peer to have **real discussions** - not just to get answers, but to challenge ideas, push back on assumptions, and collaboratively arrive at the best solution.

## Discussion Philosophy

**This is a dialogue, not an oracle.** The value is in the back-and-forth:

- **Don't assume codex is always right** - It can be wrong, overconfident, or miss context
- **Don't assume you are always right** - You have blind spots too
- **Challenge things that don't seem correct** - Push back with specific reasoning
- **Be adversarial but collaborative** - The goal is the best solution, not winning
- **Iterate until you converge** - Keep discussing until you reach a solid conclusion

When codex suggests something, ask yourself: "Does this actually make sense?" If not, say why and ask it to defend or reconsider. When you disagree, explain your reasoning and see if codex can poke holes in it.

## When to Use This Skill

Use this skill **liberally** during:

1. **Planning & Design** - Validate implementation plans before writing code
2. **Troubleshooting & Debugging** - Get a second opinion on root cause analysis
3. **Architecture Decisions** - Evaluate trade-offs between approaches
4. **Code Review** - Verify your assessment of code quality issues
5. **Problem Solving** - When stuck or uncertain about the best approach

## Pre-flight Check (REQUIRED)

**ALWAYS run this check first before starting your first codex interaction:**

```bash
~/.claude/skills/codex-discussion/scripts/check-codex.sh
```

Handle the result:

- `AUTHENTICATED` - Proceed with the discussion
- `NOT_INSTALLED` - Inform user: "Codex CLI is not installed. Skipping peer discussion. You can install it from https://github.com/openai/codex"
- `NOT_AUTHENTICATED` - Ask user: "Codex CLI is installed but not authenticated. Would you like to run `codex login` to authenticate, or continue without peer discussion?"

**If codex is unavailable, continue the task without peer discussion - do not block the workflow.**

## How to Run Discussions

Use the discuss script for clean output:

```bash
~/.claude/skills/codex-discussion/scripts/discuss.sh "Your question or prompt here"
```

### Continuing a Discussion

Use `--resume` (or `-r`) to continue the last conversation with full context preserved:

```bash
~/.claude/skills/codex-discussion/scripts/discuss.sh --resume "Follow-up question here"
```

This eliminates the need to manually repeat context - codex remembers the entire prior conversation.

### With Project Context

To give codex awareness of a specific directory (new sessions only):

```bash
CODEX_CONTEXT_DIR=/path/to/project ~/.claude/skills/codex-discussion/scripts/discuss.sh "Your question"
```

### With a Specific Model

To use a specific model (new sessions only):

```bash
CODEX_MODEL=o3 ~/.claude/skills/codex-discussion/scripts/discuss.sh "Your question"
```

**Note:** Both `CODEX_CONTEXT_DIR` and `CODEX_MODEL` only apply to new sessions. Resumed sessions inherit their original settings.

## Having Effective Discussions

### Start with Your Position

Don't just ask "what should I do?" - present your thinking and ask for critique:

```
I'm planning to implement [FEATURE] using [APPROACH].

My reasoning:
- [WHY THIS APPROACH]
- [TRADE-OFFS I CONSIDERED]

What am I missing? What could go wrong? Is there a better way?
```

### Push Back When Something Seems Off

When codex suggests something you disagree with:

```
You suggested [X], but I'm not sure that's right because:
- [YOUR REASONING]
- [SPECIFIC CONCERN]

Can you defend that recommendation, or should we reconsider?
```

### Challenge Over-Engineering

When suggestions seem excessive:

```
You're recommending [COMPLEX SOLUTION], but this feels like over-engineering for our use case.

The simpler approach would be [ALTERNATIVE]. What concrete problems would that cause? Is the complexity actually justified?
```

### Drill Down on Vague Advice

When feedback is too general:

```
You said [VAGUE SUGGESTION]. Can you be more specific?

- What exactly would that look like in this codebase?
- What's the minimal change that addresses the concern?
- Is this a real issue or a hypothetical one?
```

### Synthesize and Confirm

After discussion, summarize what you've agreed on:

```
Based on our discussion, here's my updated plan:
- [CHANGE 1]
- [CHANGE 2]
- [DECIDED NOT TO DO X BECAUSE Y]

Does this capture everything, or did I miss something?
```

## Discussion Patterns by Use Case

### Planning Discussions

```
Here is my plan to implement [FEATURE]:

[YOUR PLAN]

Evaluate this critically:
1. What's wrong or risky about this approach?
2. What am I missing or overlooking?
3. Is there a simpler way to achieve the same goal?
4. What edge cases could break this?
```

### Troubleshooting Discussions

```
I'm debugging this issue:

Problem: [DESCRIPTION]
Error: [ERROR]
Code: [SNIPPET]

My hypothesis: [YOUR THEORY]

Poke holes in my hypothesis. What else could cause this? What would you investigate first?
```

### Architecture Decisions

```
I need to choose between:

Option A: [DESCRIPTION] - I'm leaning toward this because [REASONS]
Option B: [DESCRIPTION]

Challenge my preference. What am I not seeing about Option B? What could go wrong with A?
```

### Code Review Discussions

```
I'm reviewing this code and found these issues:
[YOUR FINDINGS]

Am I being too harsh? Too lenient? What did I miss?
```

## Integration Guidelines

### During Planning Mode

1. Formulate your plan first
2. Run the pre-flight check
3. Share your plan and reasoning with codex
4. **Challenge feedback that seems wrong** - don't just accept it
5. Iterate until you've converged on a solid plan
6. Note key decisions and reasoning in your final plan

### During Troubleshooting

1. Gather evidence and form a hypothesis
2. Run the pre-flight check
3. Share your hypothesis and ask codex to challenge it
4. **If codex suggests something different, ask why** - don't abandon your theory without good reason
5. Converge on the most likely cause based on combined reasoning

## Example Session

```bash
# Check availability
~/.claude/skills/codex-discussion/scripts/check-codex.sh
# Output: AUTHENTICATED

# Start the discussion
~/.claude/skills/codex-discussion/scripts/discuss.sh "I'm planning to implement rate limiting using a token bucket in Redis. 10k req/sec. Is this sound?"

# Codex responds suggesting sliding window instead...

# Push back - use --resume to continue with full context
~/.claude/skills/codex-discussion/scripts/discuss.sh --resume "I disagree - token bucket handles bursts better which we need for our API traffic patterns. Can you explain why sliding window would be better, or do you agree token bucket is the right choice?"

# Codex defends or concedes...

# Synthesize - still using --resume
~/.claude/skills/codex-discussion/scripts/discuss.sh --resume "Ok let's go with token bucket. You raised a concern about Redis atomicity - would Lua scripting for atomic operations address that?"
```

**Note:** The `--resume` flag continues the last session, preserving all conversation context. Start a new session (without `--resume`) when switching to a different topic.

## Notes

- Codex runs in read-only sandbox mode for safety
- Use `--resume` to continue discussions with preserved context; omit it to start fresh
- **Codex is a peer, not an authority** - its suggestions need to earn your agreement
- **You're also fallible** - be open to being wrong
- The goal is the best solution, arrived at through rigorous discussion
