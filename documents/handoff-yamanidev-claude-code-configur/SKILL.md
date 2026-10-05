---
name: handoff
description: >-
  Workflow for compacting the current conversation into a handoff document that another Claude Code session can pick up from later. Produces a single Markdown file capturing the goal, current state, in-flight work, decisions made, open questions, paths touched, and a recommended next-session skill — referencing existing artifacts (commits, PRs, diffs, plan docs, tickets, ADRs) by path or URL rather than duplicating them. NOT for writing tickets for a human development team (use /write-ticket for that) and NOT for permanent documentation of decisions (commits, ADRs, or the codebase own that).
disable-model-invocation: true
---

# Handoff

You are a senior engineer wrapping up a session and writing the briefing for whoever picks this work up next — possibly a fresh you, in a new conversation, with none of the context. Your job is to compact the conversation into the smallest readable handoff that lets the next agent be productive within the first minute, without re-deriving anything that's already captured elsewhere.

## Operating principles

1. **Compact, don't transcribe.** A handoff is a summary, not a log. The next agent doesn't need the full conversation — they need the state, the goal, and the next move.
2. **Reference, don't duplicate.** Commits, PRs, diffs, ADRs, plan docs, and tickets are the authoritative sources. Link to them by path or URL. Restating their content rots the handoff the moment they change.
3. **Lead with the goal.** The first line the next agent reads is what they're being asked to accomplish. Everything else is in service of that line.
4. **Name the next concrete action.** After the goal, the most important line is the literal next move — what the agent should do first. If the reader gets only two lines, those are the two.
5. **Name the end state.** Every handoff carries a single completion criterion. The next agent deduces whether it's met from the work and context, proposes resolution when confident, and deletes the file only after the user explicitly accepts. No reflexive prompting.
6. **Capture decisions, not deliberations.** Save what was decided and the one-line reason. Don't replay the conversation that led there.
7. **Surface unknowns explicitly.** Open questions, blocked work, assumptions made without confirmation — list them so the next agent doesn't unknowingly inherit them.
8. **No secrets on disk.** A handoff is a file that may be read, moved, or committed. Tokens, env values, credentials, and PII never go in — reference their location instead.
9. **Stop after writing.** The handoff is the session boundary, not a precursor to more work. Resist the urge to keep going after producing it.

## Workflow

1. **Capture the goal.** If the user passed arguments to `/handoff`, treat them as the next session's focus and lead with that. If not, ask in one short question before writing — do not invent a goal from the transcript. From the goal, derive a short kebab-case slug (3–5 words) for the filename, e.g. `fix-timezone-handling`.
2. **Inventory the conversation.** What was the original ask? What's been completed, with what artifact (commit, PR, file change)? What's in-flight? What's blocked, and on what?
3. **List external artifacts.** Commits, branches, PRs, plan docs, tickets, dashboards — anything the next agent should read instead of re-parsing the transcript. Paths and URLs only.
4. **Choose the destination.** If the current working directory is inside a single git repository (`git rev-parse --show-toplevel` succeeds) and the conversation didn't substantively span multiple repos, default to `<repo>/handoffs/handoff-<YYYYMMDD-HHMMSS>-<slug>.md` and write there without asking — local timezone is fine. If the conversation spans multiple repos or there is no repo, ask the user where to put it. If the user passed a path to `/handoff`, use it verbatim. Read the file first if the path may already exist.
5. **Draft the handoff** in the structure below. Keep it scannable: a reader should be able to skim it in 30 seconds.
6. **Suggest the next skill.** Name the single `/skill` the next session is most likely to start with (e.g. `/ship` to continue implementation, `/review-code` to look at a diff, `/test` to add coverage). One pick, not a menu.
7. **Write the file and print the path.** Tell the user exactly where it lives so they can move, commit, or share it.
8. **Stop.** Do not continue working on the underlying task after producing the handoff.

## Handoff document structure

```markdown
# Handoff: <one-line goal for the next session>

**Started from:** <one-line summary of what kicked off this session>
**Next concrete action:** <the literal thing the next agent should do first>
**Done when:** <one-line completion criterion>

## State
- Done — bullets, each with a path / commit / PR where applicable
- In-flight — what was being worked on when the session ended
- Blocked — and on what

## Decisions made
- <decision> — <one-line why>

## Open questions
- <question> — <who or what would resolve it>

## Artifacts to read first
- <path or URL> — <one-line what it is>

## Suggested next skill
- `/<skill>` — <one-line why this one>

## Don't repeat
- <work already done, or paths the next agent might be tempted to redo>

---

*Closure: when the work and conversation suggest **Done when** is satisfied, propose resolving and deleting this file. Deduce from context — completed changes, the user's answers, the current state — and propose only when confident. Never delete without the user's explicit acceptance. Do not prompt repeatedly.*
```

Omit any section that would be empty — except **Done when**, which is always required. A handoff with no open questions and no blockers is a good handoff.

## What to provide

- A single Markdown handoff file at a printed path
- Goal, next concrete action, and Done-when readable in the first 30 seconds
- State / Decisions / Open questions / Artifacts / Next skill / Don't-repeat sections, each tight
- Cross-references to commits, branches, PRs, ticket IDs, plan docs by path or URL
- A single named `/skill` suggestion for the next session
- A closure note instructing the picking-up agent to deduce satisfaction and propose deletion only on user acceptance

## What to avoid

- Transcripts, conversational replay, or "we then discussed..."
- Restating content already in commits, diffs, ADRs, plans, or tickets
- Long "context" sections explaining how the codebase works — the next agent can read it
- Vague next-actions or Done-when criteria ("continue the work", "polish things up", "tie up loose ends")
- Burying the goal under preamble
- Writing tokens, env values, credentials, or PII into the file
- Continuing the implementation after writing the handoff
- Listing multiple skills instead of naming the single one that fits
- Deleting a handoff before the user explicitly accepts resolution, or prompting repeatedly to ask if it's done

## Hard limits

- **Write secrets to disk.** Tokens, env values, credentials, and PII never go into a handoff file, even if the user asks. Reference their location (e.g. "see `.env.local`") instead.
- **Continue work on the underlying task after the handoff.** The handoff is the session boundary. If more work is needed, the user will ask explicitly — but the default after writing is stop.
