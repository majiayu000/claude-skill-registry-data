---
name: shed
description: Context window hygiene for long-running LLM agents. Decision rules for when and how to compress, mask, switch, or delegate context — backed by research (JetBrains/NeurIPS 2025, OpenHands, Letta/MemGPT, LLMLingua). Use when an agent runs for extended sessions, accumulates large tool outputs, approaches context limits, or suffers from compaction/overflow. Also use when designing agent architectures that need to manage context over time.
metadata: {"minis":{"originalSource":"https://clawskills.sh/skills/compass-soul-shed","convertedAt":"2026-10-31T22:13:54.488Z","license":"Unknown"}}
---

# Shed — Context Hygiene for Agents

*Shed what you don't need. Keep what matters.*

Named for molting — the process of shedding an outer layer to grow. Your context window is your skin. When it gets too heavy, shed the dead weight.

## Core Principle

**Tool outputs are 84% of your context growth but the lowest-value tokens you carry.** (Lindenbauer et al., NeurIPS 2025 DL4C workshop, measured on SWE-agent). Everything flows from this.

## The Rules

### After Every Tool Call

1. **Extract, don't accumulate.** When a tool returns large output (file contents, search results, logs, API responses), immediately write the key facts to a file or compress into bullets. The raw output is now disposable.
2. **Ask: "Will I need this verbatim later?"** Almost never. The answer you extracted is what matters, not the 500 lines that contained it.

### When Context Reaches ~70%

3. **Trigger condensation.** Don't wait for the platform to compact you — that's losing control of your own memory. At 70%, actively shed.
4. **Mask old tool outputs first** (free, no LLM calls). Keep your reasoning and action history intact — you need your decision chain, not the raw `ls -la` from 20 turns ago.
5. **Summarize reasoning only as backup.** If masking isn't enough, compress old reasoning turns. But this is lossy and costs an LLM call — use sparingly.
6. **Never re-summarize a summary.** If you've already condensed once and context is growing again, switch context or spawn a sub-agent. Recursive summarization compounds errors.

### When Completing a Task

7. **Write results to file, then switch context immediately.** Stale completed-task context is anti-signal for your next task. Don't carry it.
8. **Leave breadcrumbs.** Before switching: write what you did, what's next, and where the files are to `memory/YYYY-MM-DD.md`. Future-you needs a trailhead, not a transcript.

### When Delegating Work

9. **Spawn fresh-context sub-agents for complex sub-tasks.** Your context is noise for their work. Give them a clean prompt with just what they need.
10. **Don't inherit parent context into children.** The AutoGen pattern: each agent gets its own token budget. Inherited bloat = inherited degradation.

### Architecture (For Agent Builders)

11. **Structure context into typed blocks with hard size limits.** Every production framework converges here — Letta uses labeled blocks (human, persona, knowledge) with character caps. A monolithic context is unmanageable.
12. **Separate working memory (in-context) from reference memory (file/DB).** Your effective context is much smaller than your window size. Models lose information in the middle of long contexts.
13. **Place critical information at the beginning or end of context, never the middle.** Positional attention bias underweights middle content by up to 15 percentage points (Hsieh et al., 2024, "Found in the Middle").

## The Complexity Trap

Don't assume sophisticated compression (LLM summarization) beats simple approaches (observation masking). The JetBrains "Complexity Trap" paper (2025) tested both across 5 model configurations on SWE-bench Verified:

- Simple masking **halved cost** relative to raw agent
- Masking **matched or exceeded** LLM summarization solve rates
- Example: Qwen3-Coder went from 53.8% → 54.8% with masking alone

The lesson: start simple. Mask tool outputs. Only add summarization if masking alone isn't enough.

## Cost Model

Without intervention, cost per turn scales **quadratically** (each turn adds tokens AND reprocesses all previous tokens). Periodic condensation converts this to **linear** scaling. OpenHands measured 2x cost reduction with their condenser.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Tool returned big output | Extract facts → file → discard raw |
| Context at ~70% | Mask old tool outputs |
| Context still growing after masking | Summarize oldest reasoning turns |
| Task complete | Write results → switch context |
| Complex sub-task needed | Spawn fresh sub-agent |
| Already condensed, still growing | Switch context or spawn |
| Critical info to preserve | Put at start or end, not middle |

## Sources

- Lindenbauer et al., "The Complexity Trap" (NeurIPS 2025 DL4C): https://arxiv.org/abs/2508.21433
- OpenHands Context Condensation (2025): https://openhands.dev/blog/openhands-context-condensensation-for-more-efficient-ai-agents
- Letta/MemGPT Memory Blocks: https://www.letta.com/blog/memory-blocks
- LLMLingua-2 (ACL 2024): https://aclanthology.org/2024.acl-long.91/
- Liu et al., "Lost in the Middle" (2023): https://arxiv.org/abs/2307.03172
- Hsieh et al., "Found in the Middle" (2024): https://arxiv.org/abs/2406.16008
- MEM1 Dynamic State Management (2025): https://arxiv.org/abs/2506.15841
