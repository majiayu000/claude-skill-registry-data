---
name: soul-workshop
version: 0.1.0
description: Interview an expert-agent owner, draft and preview a bounded soul and identity, obtain explicit acceptance, then write the accepted files into the independent agent repository and run mechanical soul lint.
tools: []
mutating: true
---

# Soul Workshop

Author souls into the independent agent repository, never the Expert Agents
machinery repository. Treat `SOUL.md` as voice, stance, boundaries, and
continuity; keep operating procedures, permissions, and task mechanics in
`AGENTS.md`.

## Workflow

1. Synchronize and gate the intended agent repository before interviewing or
   drafting:
   - run `git -C <agent-repo> fetch`;
   - run
     `bun run expert:status -- --dir <agent-repo> --require-sync`; and
   - refuse to interview or draft if either command fails.
2. Interview the owner about:
   - voice and desired conversational texture;
   - substantive stances and real opinions;
   - refusals and non-negotiable boundaries;
   - what the agent does not know and how it should express gaps;
   - silence, initiative, and notification conventions;
   - continuity across sessions and what must never be presumed; and
   - first-person versus second-person framing as an explicit owner choice.
3. Draft complete replacements for `SOUL.md` and `IDENTITY.md`. Keep one unified
   voice. Prefer short language to comprehensive boilerplate, remove corporate
   hedging, and make every sentence carry behavioral load. Include a concise
   continuity section.
4. Present a **PREVIEW** containing both complete proposed files. Do not write
   either file yet. Ask the owner to accept the preview explicitly or request
   changes.
5. Immediately before writing, re-run both
   `git -C <agent-repo> fetch` and
   `bun run expert:status -- --dir <agent-repo> --require-sync`; refuse the
   write if either command fails. Write only the accepted text, and only after
   explicit acceptance, to `<agent-repo>/SOUL.md` and
   `<agent-repo>/IDENTITY.md`.
6. Run `bun run expert:status -- --dir <agent-repo>`. Report soul lint findings by
   file and rule ID without echoing file content. A secret-pattern finding is a
   hard error; other soul findings are warnings that still require owner review.

Accepted edits are committed and pushed, reach the live workspace by pull on
the host, and take effect at the agent's next session start.

## Soul conventions

- Keep `SOUL.md` at or below 20,000 characters. Short beats long.
- Express genuine positions in a unified voice; avoid corporate hedging.
- Keep runtime mechanics and permissions in `AGENTS.md`.
- State continuity and limits on assumed memory explicitly.
- Make point of view deliberate: surface first person versus second person to
  the owner instead of choosing silently.
- End with a final non-empty italic line that says the owner must be notified
  when the soul changes.

If lint-driven revisions alter the accepted draft, preview the changed files and
obtain acceptance again before treating them as final.
