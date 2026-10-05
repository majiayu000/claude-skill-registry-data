---
name: research
category: meta-orchestration
description: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
codex-short-description: "Investigate a question against primary sources and write a cited Markdown note"
compatibility: claude-code codex opencode
---
Spin up a **background agent** to do the research, so you keep working while it reads.

**If you are already that background agent, do the work yourself — do not delegate again.** The agent dispatched here holds the same tools and the same instructions, so an unguarded read of this line fires it a second time, and a third; the duplicates run out of view, finish long after the original, and multiply the cost of one question several times over. Exactly one new background task should exist per invocation. Where the host offers no background execution at all, say so and do the research inline rather than silently doing nothing.

**Scope it before dispatching.** There is no stopping criterion in the reading itself, so an unbounded question produces either an endless run or a broad survey that misses the one detail that mattered. One API, one behaviour, one version claim — narrow enough that "answered" is observable. If the question isn't in that shape, sharpen it with the user first.

Its job:

1. Investigate the question against **primary sources** — official docs, source code, specs, first-party APIs — not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source. The citation is the only check the reader has: a claim whose link lands on someone's summary of the thing rather than the thing has failed the skill's one job, so drop it or chase it further.
3. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.
4. Report the path back, and say what the file now lets the user decide. Nothing reloads it automatically — a research note that isn't deliberately fed into the next step is a dead file, and a stale one is worse than none.

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/research.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
