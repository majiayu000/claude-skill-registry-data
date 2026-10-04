---
name: cursor-how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
---

## Codex runtime mapping

Use native read-only subagents only when authorized; the standing `model-capability-router` owns model and effort. Preserve simple versus complex paths, distinct exploration angles, cited synthesis and coordinator verification.

# How

Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

For each delegation, choose the model and effort through the standing `model-capability-router` and the native Codex inventory. Respect the operator's selection. If a requested model is unavailable, report the exact gap; do not invent a replacement slug.

## Step 1. Assess Complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. One explainer explores and explains in a single pass. Go to Step 2b.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): spawn parallel explorers first, then hand off to the explainer. Go to Step 2a.

When in doubt, take the simple path.

## Step 2a. Explore (complex questions only)

Delegate the 2 to 4 distinct angles to read-only Codex subagents in parallel when the task permits delegation. Select available model and effort under the standing `model-capability-router` policy. If delegation is unavailable, investigate the same angles sequentially and keep the evidence separate.

Each explorer gets the prompt in `references/explorer-prompt.md` with its angle filled in. Then go to Step 3.

## Step 2b. Direct Explain (simple questions)

Use one read-only Codex subagent when delegation is authorized and useful; choose model and effort under the standing `model-capability-router` policy. Otherwise explore and explain directly in one pass.

Build its prompt from `references/explainer-prompt.md` without the explorer-findings section. Go to Step 4.

## Step 3. Synthesize (complex questions only)

After all explorers return, synthesize their cited findings in the coordinator or one read-only Codex subagent chosen under the standing `model-capability-router` policy. The coordinator checks the source paths and owns the final explanation.

Build its prompt from `references/explainer-prompt.md` with every explorer's findings filled in.

## Step 4. Present

Check the cited source paths and explain the result to the user in the requested scope. Correct factual errors before presenting it; the coordinator owns the final answer.

## Output Format

The explanation uses the sections defined in `references/explainer-prompt.md`, dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.
