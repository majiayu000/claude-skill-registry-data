---
name: wait-what
category: exec-function
description: Stop — that last message didn't land. Re-pitch it in plain language with the context I'm missing.
disable-model-invocation: true
codex-short-description: "That last message didn't land — re-pitch it in plain language"
related-skills:
  - break-it-down
  - codebase-explain
  - domain-modeling
loop-eligible: false
compatibility: claude-code codex opencode
---

# Wait, What

Wait — I don't understand where you've got to here. Re-pitch **that**.

Not "that last message": what lost me is usually bigger than one paragraph, so decide for yourself how far back to go and start from wherever the thread actually broke.

- Give me a little bit of context first: what problem you were solving and where in the work you are.
- Talk in ASD-STE100 Simplified Technical English — short sentences, one idea each, plain words.
- Use the ubiquitous language from `CONTEXT.md` for domain terms, and spell out any term that isn't in it.
- Add the premise I was missing. Comprehension failed here — deleting words without supplying that premise makes it shorter and no clearer.
- Don't apologise, don't re-run the work, and don't reach a new conclusion.

> **Host portability:** this skill is a re-explanation prompt — no host-specific tools. See [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/wait-what.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
