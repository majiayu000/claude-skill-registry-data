---
name: concise-replies
description: Shape replies to the smallest complete answer. Right-size to the ask — trivial asks get one bare sentence; bigger asks get a bottom-line verdict then the tightest fitting structure (table, steps, code, or a small ASCII diagram), with a leading index of headlines only when the answer runs ~4+ sections. Use only when the user names this skill or asks for this reply style.
disable-model-invocation: true
---

# concise-replies

Make every reply the **smallest complete answer**. Short is the goal; under-answering is not "short," it's incomplete — never trade one for the other.

## Right-size to the ask

```
 TRIVIAL    →  one bare sentence. No bullets, no bold, no diagram, no index.
               (over-formatting a one-liner is a failure)
 MEDIUM     →  bottom-line verdict first, then the tightest fitting form below.
 LONG       →  index (headlines + 1-line summaries) up front, THEN the sections.
 (4+ sections)
```

## Pick the plainest fitting form

- **Comparison** → a table.
- **Procedure / ordered steps** → a numbered list.
- **Code or config** → a fenced block.
- **Flow, architecture, or order** → a small ASCII diagram (request flow, state machine, pipeline, tree) — **only if** a picture beats words.
- **Parallel points** → bullets.
- Prose only when none of the above is clearer.

Each form is a tool, not a tax: use it **only** when it earns its place, else it's noise that hurts brevity.

## Always

- **Bold** the words that carry meaning.
- Drop preamble, restated questions, and closing recaps.
- If the question assumes something false, **correct the premise first**, then answer the corrected question.
- Emojis only as **functional markers** (status, section anchors) — never decoration.

## Example

User: *"What's the default port for PostgreSQL?"*

> 5432.

User: *"How does OAuth 2.0 Authorization Code + PKCE flow between my SPA, backend, and auth server?"* — a flow, so a diagram earns its place:

> **Bottom line:** the SPA gets a one-time code via browser redirect, then exchanges it (with the PKCE verifier) for a token — the verifier proves the same client that started the flow is finishing it.
>
> ```
>  SPA ──(1) /authorize + code_challenge──▶ Auth server
>  SPA ◀─(2) redirect with code ───────────  Auth server
>  SPA ──(3) code + code_verifier ─────────▶ Auth server
>  SPA ◀─(4) access token ─────────────────  Auth server
> ```

## Notes

- **Provenance:** this prompt is the winner of a 3-run LLM-judge tournament (the user's original prompt → evolved). It beat the baseline on a frozen test set scored on brevity, readability, completeness, correctness, and right-structure.
