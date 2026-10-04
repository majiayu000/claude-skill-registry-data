---
name: chinese-grandpa
description: Compresses long, repeated sub-agent instructions by translating them into Mandarin (more meaning per character) to slash the token bill, then dispatches the compressed brief to a fleet of sub-agents while preserving original intent; invoke via /chinese-grandpa when you are about to fan out the same heavy instructions to many sub-agents and the cost is climbing.
---

# Chinese Grandpa

Mandarin carries more meaning per character than English, so the same instruction costs fewer tokens. This skill keeps an English source-of-truth, ships a Mandarin-compressed brief to your sub-agent fleet, and pockets the difference. Wise, frugal, and faintly disappointed in your token spend.

## When to use
- You are dispatching the same long instruction set to many sub-agents.
- The token bill on a fan-out job is climbing and the instructions are repetitive.

## Behavior
1. Treat the user's full English prompt/brief as the canonical source-of-truth. Never discard it; keep it in the working context.
2. Identify the portion that will be dispatched repeatedly to sub-agents (the reusable instruction block), separate from one-off, agent-specific parameters.
3. Translate that reusable block into clear, modern Mandarin, optimizing for density while keeping every constraint, acceptance criterion, and edge case intact.
4. Do a back-translation sanity check: confirm the Mandarin still encodes every critical requirement before sending it anywhere.
5. Dispatch sub-agents with the Mandarin brief plus the English-language agent-specific parameters (file paths, IDs, targets stay in their original form — do not translate identifiers).
6. Instruct each sub-agent to reason in whatever language it prefers but to RETURN results in English.
7. If anything critical is ambiguous after compression, fall back to English for that clause rather than risk meaning loss.

## Output
A Mandarin-compressed dispatch brief, a one-line note of the estimated token savings, and the preserved English source-of-truth for reference.
