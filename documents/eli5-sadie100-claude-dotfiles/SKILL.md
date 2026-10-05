---
name: eli5
description: Explain a topic like I'm a 5 year old. Use when the user types /eli5 <topic> or asks for a dead-simple picture explainer of how something works.
---

# eli5

Explain like I'm someone who knows nothing about this topic, using a HTML artifact with big pictures and few words.

Topic: $ARGUMENTS

## Source of truth

When the topic is "how does X work in this codebase":

- Read the actual code first (the functions that run — not just file header comments or docs). Docs, design notes, and header comments are hints for *where* to look and *why*, not evidence of *what* happens.
- Order of trust: executed code > code comments > docs. When they disagree, describe the code and mention the disagreement.
- Trace the real call order (who calls what, with which inputs) before drawing steps — a numbered sequence in the picture must match the runtime order, not the document's section order.
- Don't stop at the core module: read the call sites too, since inputs decided by callers often change what the core does.
- In the explanation itself, keep code identifiers out of the main text; put file paths in a small footer so the reader can verify.
