---
name: but-how
description: 'Use for "how does X work", code walkthroughs before changing something, and placement/ownership/layering questions ("where should this live", "which package owns this", "is this the right layer"). Explains subsystem architecture, runtime flow, onboarding mental models. Use but-why for motivation.'
disable-model-invocation: true
---

# But how

Explore the codebase to answer "how does X work?" questions. Write for a senior engineer onboarding onto a subsystem. Give them enough to build a working mental model. Stop before it reads like annotated source.

## Step 1. Assess complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. One explainer explores and explains in a single pass. Go to Step 2b.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): spawn parallel explorers first, then hand off to the explainer. Go to Step 2a.

When in doubt, take the simple path.

## Step 2a. Explore (complex questions only)

Split the question into 2 to 4 exploration angles, each a distinct slice of the subsystem. Spawn all explorers in a single message:

- `subagent_type`: `generalPurpose`
- `model`: your configured how-explorer model (default `grok-4.6-fast-xhigh`)
- `readonly`: `true`

Each explorer gets the prompt in `references/explorer-prompt.md` with its angle filled in. Then go to Step 3.

## Step 2b. Direct explain (simple questions)

Spawn one Task subagent that explores and explains in one pass:

- `subagent_type`: `generalPurpose`
- `model`: your configured how-explainer model (default `claude-fable-5-1-thinking-max`)
- `readonly`: `true`

Build its prompt from `references/explainer-prompt.md` without the explorer-findings section. Go to Step 4.

## Step 3. Synthesize (complex questions only)

Once all explorers have returned, spawn one Task subagent to combine their findings into one explanation:

- `subagent_type`: `generalPurpose`
- `model`: your configured how-explainer model (default `claude-fable-5-1-thinking-max`)
- `readonly`: `true`

Build its prompt from `references/explainer-prompt.md` with every explorer's findings filled in.

## Step 4. Present

Run the explainer's output through the `/farseer:deslop` skill and present it to the user. Light edits for clarity or conversation context are fine. Do not rewrite it.

## Output format

The explanation uses the sections defined in `references/explainer-prompt.md`: Overview, Key Concepts, How It Works, Where Things Live, Gotchas. Drop any that do not apply.
