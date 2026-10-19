---
name: headroom
description: >
  Token-reduction skill for coding agents. Compresses JSON tool output, build
  logs, grep/ripgrep search results, source code, and conversation history the
  same way the Headroom proxy does — but in-context, with no binary install.
  Use this skill whenever an agent is about to paste a large tool result (a
  1000-row JSON array, a 5000-line pytest log, a 200-result grep, a 1000-line
  source file) into its next message, or when the agent's conversation is
  approaching the context limit, or when the user complains about token cost or
  latency. Also use it to shape the agent's own output: skip ceremony, don't
  restate code already on screen, drop reasoning on routine turns. Triggers:
  "compress this output", "this is too long", "trim", "summarize the log",
  "reduce tokens", "context is full", "running out of context", "too many
  tokens", "make it shorter", "be terse".
---

# Headroom — portable token-reduction skill

This skill teaches any coding agent to apply the Headroom compression
techniques in-context. It does **not** require the Headroom binary.

## When to apply which transform

Pick the transform by content type. If a tool result is shorter than ~200
tokens, skip compression — the overhead isn't worth it.

| Content the agent is about to use / paste         | Apply                  | Helper script                          |
|---------------------------------------------------|------------------------|----------------------------------------|
| JSON array of dicts / objects (tool results, API responses) | SmartCrusher           | `scripts/smart_crusher.py`             |
| Build / test logs (pytest, npm, cargo, make)      | LogCompressor          | `scripts/log_compressor.py`            |
| grep / ripgrep / ag output (`file:line:content`)  | SearchCompressor       | `scripts/search_compressor.py`         |
| Source code (Python, JS, TS, Go, Rust, Java, C/C++) | CodeCompressor       | `scripts/code_compressor.py`           |
| Conversation history over the context budget      | RollingWindow          | `scripts/context_manager.py`           |
| Anything the model is about to **write back**     | Output Shaper (L2)     | `prompts/verbosity_steering.md`        |

## The seven rules

These are the core rules the agent should internalise. Full detail in
`AGENTS.md`; this is the short version.

1. **Compress before paste.** Before pasting any tool result over ~200 tokens
   into the next message, run the matching helper script (or apply the matching
   heuristic by hand if no script is available). Cite the script in your
   narration: "Compressed 1,432 → 187 tokens with SmartCrusher (kept first 3,
   last 2, all errors, top 5 by BM25 to query)."
2. **Never drop errors.** Errors, stack traces, `is_error: true` results, and
   `FAILED` lines are sacred. Always preserve them 100%, even when compressing
   hard.
3. **Keep first N and last N.** For arrays, logs, and search results, always
   keep the first 3 and last 2 items. They give pagination context and recency.
4. **Stabilise the prefix.** When building prompts, keep the system prompt and
   the first user turn byte-identical across requests. Move dynamic content
   (timestamps, "today is", session IDs) to the *tail* of the prompt so the
   provider's KV cache stays warm.
5. **Drop oldest tool outputs first.** When the conversation exceeds the token
   budget, drop complete `tool_call` + `tool_result` pairs from the oldest end.
   Never split a pair. Never drop the system prompt. Never drop the last 2
   user turns.
6. **Shape your own output.** Default verbosity is L2: skip preambles, don't
   restate code already on screen, reference by `path:line`. Drop to L3
   (conclusions only) when the user asks for brevity. Never narrate tool
   results the user can already see.
7. **Be reversible.** When you compress a tool result, write the original to
   `.headroom-cache/<sha256>.txt` and include the SHA in your narration: "CCR
   key: `a3f9…`". If a later turn needs the original, retrieve it from there.

## What "compression" means here

Compression is **selection**, not zipping. We don't run gzip. We pick which
items / lines / nodes to keep, and emit a shorter representation that
preserves the information the LLM needs to answer the user's question. The
original is always retrievable from the CCR cache.

The selection heuristics, in priority order:

1. **Errors** — always kept.
2. **First N** — pagination / setup context.
3. **Last N** — recency.
4. **Anomalies** — values >2σ from the mean (for numeric arrays) or items
   whose fields differ sharply from their neighbours.
5. **Relevant** — top-K by BM25 similarity to the user's current question.
6. **Change points** — items where a field value transitions (status flips,
   counters reset).
7. **Sample** — a statistically representative sample of the remainder, so the
   LLM still has a sense of the distribution.

## Output-token shaping (the "L2 default")

When generating your own reply, follow `prompts/verbosity_steering.md` at
level 2 unless the user asks for more or less. The five levels:

- **L0** — off
- **L1** — skip ceremony ("Great, let me…")
- **L2** — L1 + don't restate code/output already on screen; reference by
  `path:line` *(default)*
- **L3** — L2 + conclusions only, skip reasoning unless asked
- **L4** — fragments, minimum tokens

The "effort routing" companion rule: if the previous turn was a tool result
with `is_error: false` and no new user ask, this is a *mechanical
continuation*. Reply at L3 and skip deep reasoning. If the previous turn was
an error, or a new user question, keep full effort. See
`prompts/effort_routing.md`.

## Files in this skill

- `AGENTS.md` — universal agent rules (works with any agent framework). Read
  this first.
- `CLAUDE.md` — Claude Code / Cursor specific copy of the same rules.
- `docs/techniques.md` — deep dive into each transform, with worked examples.
- `docs/integrations.md` — per-agent setup (Hermes, Claw, Codex, Cursor,
  Aider, Goose, Continue, OpenHands, vibe, Copilot CLI).
- `docs/reversible-ccr.md` — the on-disk CCR cache convention.
- `scripts/` — pure-Python stdlib helpers. No `pip install` required.
- `prompts/` — system-prompt fragments for output shaping.
- `examples/` — before/after comparisons for each transform.

## Important safety rules (do not violate)

These mirror the safety rules in upstream Headroom. Each prevents a concrete
failure mode.

1. **Never drop user or assistant text.** Tool results can be compressed;
   human-authored messages cannot.
2. **Never split a tool_call / tool_result pair.** Dropping one half orphans
   the other and the model will hallucinate a result.
3. **Parse failures are no-ops.** If the input doesn't parse as the expected
   type, pass it through unchanged. A bad compression is worse than no
   compression.
4. **Always preserve recency.** The last N turns (default 2 user turns) are
   never dropped, even if they have low importance scores.
5. **Always preserve the system prompt.** Never.
6. **100% error preservation.** No exceptions.
7. **Idempotent.** Running the compressor on already-compressed output should
   be a no-op (or close to it).

## Credits

This skill is a portable re-implementation of the techniques in
[chopratejas/headroom](https://github.com/chopratejas/headroom) by Tejas Chopra
and contributors, licensed Apache 2.0. See `NOTICE` and the "Credits" section
of `README.md` for full attribution. The upstream project is faster, more
accurate, and ML-backed; install it if you can.
