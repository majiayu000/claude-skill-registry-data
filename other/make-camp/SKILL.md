---
name: make-camp
description: Appa's camp for pausing work safely. When the team sets down for the night, they leave camp so anyone can pick up in the morning. Use for pause-safely, "pause here", "stop for now", "save your place", "checkpoint this", going offline, a session restart, or imminent context compaction. Stops at a safe boundary, commits a wip checkpoint, and publishes a resume note a cold-start agent can read. Explicit pauses only.
---

# Appa's camp

When the team sets down for the night, they make camp. The fire is banked, the saddle is packed, and the map is out where anyone can read it. Whoever wakes first knows exactly where the trip left off. You own a clean stop. Leave a checkpoint a cold-start agent can resume from with `break-camp`.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

This runs only on an explicit pause. On "keep going", "going to bed, keep going", or "don't stop", do not pause.

## Steps

1. **Stop at a safe boundary.** Finish the current atomic step or back out of it. Start nothing new, and stop any characters you dispatched.
2. **Take no irreversible action to pause.** No new PR and no push unless you already had one out.
3. **Make the work durable.** Commit uncommitted edits as one clear `wip:` commit on the current branch, so nothing is lost. If the tree is broken, say so in one line of the commit body.
4. **Write the resume note outside your context.** Capture the intent, what you were doing, progress and what is verified, the current state, the next steps, the key files, and the gotchas. Use the checkpoint directory from [references/resume-storage.md](references/resume-storage.md), which defines the shared writer and reader locator for every runtime. It must survive the expected interruption. If a `battle-map` decision trail exists, point at it instead of duplicating it.
5. **Preserve what the user asked to keep.** Keep the artifacts the user explicitly requested for use after resume, such as questions, an acceptance checklist, or a procedure. Reuse the existing artifact when there is one. Otherwise save the requested material beside the resume note and link it. Preserve exact wording, completeness, and order when requested. This does not mean archiving every aside or pausing an ongoing task.
6. **Publish and read it back.** Publish the checkpoint through [scripts/resume.mjs](scripts/resume.mjs), which verifies links and files before it atomically updates the project pointer.

   ```bash
   node <this-skill>/scripts/resume.mjs begin --project <worktree>
   node <this-skill>/scripts/resume.mjs publish --project <worktree> --note <dir>/resume.md --artifact <file> ...
   node <this-skill>/scripts/resume.mjs read --project <worktree>
   ```

   Read it using only the project directory, and check the requested contents before you declare the checkpoint ready. Ten requested questions means all ten are reachable from the note alone.

## Reply

Where you are in the loop. What is on disk versus still only in your head (paths, no diff dumps). The commits you made and whether the tree is clean. The first action on resume. This is a pause, not a final report.
