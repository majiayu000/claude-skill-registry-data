---
name: sync-claude-sessions
description: 'Digest recent local Claude Code CLI history into /raw/sessions and index recurring mistakes in /wiki. Use when syncing session data or as part of /data-ingestion.'
---

# Sync Claude Sessions

Pipeline skill: turn recent Claude Code session transcripts into indexed
knowledge. Runs standalone or as step 1 of `/data-ingestion`.

## Process

1. **Find the last sync point.** Read `raw/sessions/.last-sync` (a single ISO
   timestamp). If missing, default to 14 days ago.
2. **Locate session data.** Claude Code stores transcripts under
   `~/.claude/projects/<project-slug>/*.jsonl`. List files modified after the
   last sync point.
   - **Cloud fallback**: in a fresh remote container (scheduled routine runs),
     that directory is missing or holds only this session — the owner's desktop
     CLI history is unreachable there. Do NOT report "nothing new"; instead
     digest the *current* session so far (its task, outcome, mistakes,
     corrections) as the sole entry, and state in the report that full local
     history syncs only when this skill runs on the desktop.
   - If there is genuinely nothing to digest (no history AND no meaningful
     current-session activity), record that and skip to step 6.
3. **Digest, don't dump.** For each new/updated session, extract only:
   - Date, project, one-line task description
   - Outcome (succeeded / abandoned / partial)
   - Mistakes or repeated corrections (user re-explaining, reverted edits,
     failed commands retried)
   - Skill opportunities (workflows done manually 2+ times that could become
     a skill or command)
   Use `jq`/`grep` to pull user messages and tool errors rather than reading
   whole transcripts into context.
4. **Write the digest.** Append one file:
   `raw/sessions/YYYY-MM-DD_session-digest.md` with a section per session.
   Never copy secrets, tokens, or credentials out of transcripts.
5. **Index.** Add a row to the **Session Digests** table in `wiki/index.md`
   summarizing the recurring mistakes and skill opportunities found.
6. **Update the sync point.** Write the current ISO timestamp to
   `raw/sessions/.last-sync`.
7. **Report.** Sessions processed, top recurring mistake, top skill
   opportunity. If run from `/data-ingestion`, keep this to 3 lines.
