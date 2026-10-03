---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a cited Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to an isolated agent.
---

Delegate the research to the Pi `researcher` agent so the reading happens in an isolated context. The parent waits for the dispatch to finish; this is not a detached background job.

## Process

1. Decide where the repository keeps research notes. Match an existing convention. If none exists, choose a sensible final path and state it.
2. Create a unique scratch directory at `.scratch/pi-agents/research-<timestamp>/` and assign `research.md` as the agent's only writable artifact.
3. Capture `git status --short`, then invoke the Pi `subagent` tool with one `runs.run` child using agent `researcher`, `context: "fresh"`, `worktree: false`, and `async: false`. Include:
   - The exact research question and practical decision it informs.
   - Relevant repository paths and version constraints.
   - The scratch artifact's exact path.
   - The final destination you intend to use after validation.
4. The researcher must investigate **primary sources** such as official documentation, source code, specifications, and first-party APIs. Every material factual claim needs a citation to the source that owns it.
5. After delegation, compare `git status --short` with the captured state. The only new path attributable to the researcher must be the assigned scratch artifact. Stop and report any unexpected change.
6. Read the complete artifact. Check that it answers the question, separates fact from inference, cites every material claim, and records uncertainty.
7. Promote the validated report to the chosen final path. The parent performs this write so an existing project document is never replaced without review. Report both the final path and the scratch source.

If the `subagent` tool is unavailable, perform the same research in the current session and write the final artifact directly. Disclose that the research was not context-isolated.
