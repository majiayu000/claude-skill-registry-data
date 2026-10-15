---
name: waterfall
description: "Implement anything end-to-end using two agents: planner cum reviewer (premium model) and an implementer (fast model)"
compatibility: Requires kolu
---

# Waterfall

This skill is invoked with an argument that tells us what to implement.

You will respond to the user with a plan (focusing more on architecture-level than walls of text), who then approves it (unless they pre-approve). After they approve you must finalize the plan to remove all ambiguities using the question tool, along with asking the user these questions:

- Which harness to run (e.g.: omp, codex --yolo, etc.)
- Which model to use for the selected harness
- Whether to auto-merge on green CI at end

Then you open a new Kolu split terminal, and run the implementor agent (in the same $PWD worktree as you) to implement the plan opening PR[^pr] and then wait[^debrief] for the implementor to finish. Then, you review the PR per repo's guidelines (e.g.: Cordis-perfection, /solidjs) posting it in the PR itself, and then ask the implementor to address it. Then you re-review. Once satisfied, you ask the implementor do a final refactor per https://kolu.dev/blog/hickey-lowy/ and then to run CI (to save time, we don't run full CI until reviews are fully done). Once the PR is green, our work is done (unless auto-merge is enabled).

**IMPORTANT**: 
- If you are Fable model, you must **NOT** use Fable for any subagents you spawn unless that subagent requires premium intelligence.
- Keep it cheap: the brief holds only what this skill and the repo rules require; tests run once per round and CI once at the end; mid-round asks wait for the next round; compact the implementor only when the context is large, or before a long new phase like CI

**BANS**:
- You are banned from doing any implementation yourself; that happens only through the implementor agent.
- You are banned from starting new agents or new PRs without human's approval.
- You are banned from terminating the implementor agent terminal *unless* the PR gets merged or closed.

[^debrief]: Use kolu debrief to wait on any kolu terminal running an agent to go idle.
[^pr]: PR title & body are a reviewed deliverable, optimized for a 20-second skim: table or diagram before prose, no
paragraph over 2 lines, evidence and incidents in `<details>` or a comment. The brief quotes this sentence verbatim; round-1
review gates on it.
