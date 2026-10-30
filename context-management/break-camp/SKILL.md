---
name: break-camp
description: Appa's morning departure for picking up paused or handed-off work. The team breaks camp, reads the map they left, and flies on from where they stopped. Use for session-pickup, "pick up where we left off", "resume", "continue the previous session", "take over this agent's work", or a handed-over transcript, cloud-agent URL, or pushed branch. Reads the checkpoint or prior trail, rebuilds state, and resumes without redoing finished work.
---

# Appa's breaking camp

In the morning the team packs up camp, reads the map they left by the fire, and flies on from exactly where they stopped. Nobody flies back to the last town to check it was really there. You own the resume point. Read the prior trail, and do not redo it. This is the other half of `make-camp`.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

## Steps

1. **Read the project checkpoint first.** Use [resume-storage.md](../make-camp/references/resume-storage.md) and run `node <make-camp>/scripts/resume.mjs read --project <worktree>`. A successful read gives the note and artifacts without needing a path from the previous session.

   If the pointer is missing (exit 2), find the prior trail another way.
   - A local transcript under Claude Code's per-project transcripts directory, `~/.claude/projects/<encoded-cwd>/*.jsonl`, where `<encoded-cwd>` is the workspace path with each `/` turned into `-`. Do not glob across other directories under `~/.claude/projects/`. That crosses workspace boundaries and reads private chats from unrelated projects. On Codex, sessions live under `${CODEX_HOME:-~/.codex}/sessions/`.
   - A cloud-agent URL.
   - A pushed branch.

   An unavailable or incomplete checkpoint (exit 1) needs diagnosis, not a silent fallback. For a transcript, read the metadata overview and the last messages first, then scan back for the decision points. Parse a long transcript in a dispatched character and keep only the reduced timeline in the main thread (Guard the Context Window, Fire in `four-elements`). Pick each dispatch's effort for the job, as `avatar-mode` describes.
2. **Rebuild the operational state.** The branch and worktree, what already landed (`git log` and `git diff` against the base), the open todos, and the decisions made. Use the prior trail to recover progress. A claim about a human ruling follows the rule for claims about human decisions in `past-lives`. An agent's summary is not the original ruling.
3. **Diff done against pending.** Compare what shipped against what was planned, and name the resume point. Do not rerun the prior repro or redo completed work. Recheck the claims that affect the remaining work without repeating finished investigations. Read every artifact the resume note links, including requested questions or checklists.
4. **Route the remaining work and pick the verdict.** Send the rest to the matching skill through `avatar-mode`. The verdict is one of these:
   - Continue the execution.
   - Ship a finished recommendation.
   - Ratify or override a prior conclusion.
   - Write a postmortem of a failed run (`redemption-arc`).

   This skill ends here. The routed skill owns the rest.
5. **Verify the inherited claims against the original goal on the real artifact** (Prove It Works, Earth in `four-elements`). A passing earlier self-report is not proof.

## Reply

Where the prior agent stopped. What you inherited and what you redid (ideally nothing). The resume point. The outcome.
