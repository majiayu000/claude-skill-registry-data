---
name: retrospective
description: Create a technical journey retrospective document from the current session's work. Use when the user asks for a retrospective, technical journey, dev blog post, session writeup, or wants to document what was built and why. Triggers on phrases like "write a retrospective", "create a journey doc", "document this session", "write a blog post about what we did".
---

# Retrospective

Generate a technical journey document that captures the decisions, tradeoffs, and debugging moments from a coding session. The output reads like a developer's blog post — technically interesting, honest about mistakes, and educational.

## Process

1. **Gather context** — Review the conversation history to identify: what was built, what decisions were made, what broke, what was debugged, and the final state. Note specific code patterns, error messages, and the reasoning chain behind each decision.

2. **Determine audience** — Ask the user if not obvious. Default to: technically curious developers who may be early-career. This means explaining *why* over *what*, and not assuming familiarity with niche tools.

3. **Draft the retrospective** — Follow the structure in [structure.md](references/structure.md). Write in first person. Be honest about what went wrong and why.

4. **Revise after later fixes** — Treat the retrospective as a living document during the session. If a later fix changes the root cause, implementation details, or tradeoffs, update the retrospective so it matches the final truth instead of leaving stale explanations in place.

5. **Review for educational value** — Before presenting, check each section against these criteria:
   - Would a junior developer understand *why* this decision was made, not just *what* was done?
   - Are there implicit assumptions that need to be made explicit?
   - Is the debugging narrative complete? (symptom → investigation → root cause → fix)
   - Does the writing assume knowledge that should be explained briefly?

6. **Output** — Write to `docs/` in the project (or as specified). Use markdown.

## Writing Guidelines

- First person, conversational tone. Not formal, not corporate.
- Show the messy parts. "I tried X, it broke because Y, so I did Z" is more valuable than "I implemented Z."
- Code snippets should be minimal and focused — show the interesting 5 lines, not the full file.
- Every technical choice needs a *because*. "I chose Turso because it's SQLite under the hood and my schema is trivial" > "I chose Turso."
- End sections with what you'd do differently or what comes next.
- Avoid jargon without context. First mention of a tool/concept gets a one-line explanation.
- If later work invalidates an earlier section, rewrite that section instead of leaving contradictory history behind.
- The closing should be memorable — a one-liner, a reflection, or a forward-looking thought. Not a summary.

## References

- **Document structure**: See [references/structure.md](references/structure.md) for the section template and examples of good/bad retrospectives.
