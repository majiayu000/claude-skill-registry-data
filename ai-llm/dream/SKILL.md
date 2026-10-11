---
name: dream
description: Consolidation ("dreaming") for this project, at two levels. (A) Claude's file-based memory — replays recent sessions, extracts what should change future behavior, merges, updates and prunes memories, rewrites MEMORY.md. (B) The wiki — finds concept pages that are the same underlying idea (e.g. second-brain / company-brain) and merges them into one general page. Use on /dream, "consolidate memory", "consolidate the wiki", or at the end of a long working day.
---

# Dream: consolidate memory

The brain replays the day during sleep, keeps what matters, generalizes, and wakes up fresh. This skill does the same at two levels: Claude's memory directory (Part A) and the wiki's concept pages (Part B), where separately ingested episodes produced near-duplicate concepts that should become one general truth. It is built from the wiki's own synthesis: [[concepts/memory-consolidation]], [[concepts/agent-memory]], [[concepts/human-vs-ai-memory]], [[concepts/knowledge-rot]].

## Principles (from the wiki)

| Principle | Source |
|---|---|
| **Replay before writing.** Consolidation works on the day's actual experience, not on a guess about it. | Hippocampal replay ([[episodes/langtalks--60-brain-memory]]) |
| **Distill, don't hoard.** A growing stack of notes that gets reread every morning is the failure mode. Each memory must change future behavior. | Gilad Levi ([[episodes/explainable--164-gilad-levi-continual-learning]]) |
| **Learn from corrections.** Compare what Claude did with what the user changed, rejected or redid, and infer the rule. | Nightly correction job ([[episodes/langtalks--72-personal-assistant-agent]]) |
| **Merge episodes into general truths.** Several small session memories become one general rule. Digest *and* discard. | Itamar Friedman ([[episodes/langtalks--57-memory]]) |
| **Frequency over recency.** Resolve conflicts by how often and how consistently something held, not by which came last. Never overwrite silently. | Mem0 critique ([[episodes/langtalks--60-brain-memory]]) |
| **Earn your place.** A rule that isn't used or keeps getting overridden gets changed or deleted. | Usage/acceptance test ([[episodes/langtalks--57-memory]]) |
| **Fight rot.** Dropped projects, renamed files and finished work keep resurfacing unless someone says so. | Dana Maman ([[episodes/osim-tochna--second-brain-and-llm-wiki]]) |
| **Stay inspectable.** Plain-language files the user can read and veto. | [[episodes/langtalks--57-memory]] |

## Part A: Claude's memory

### 0. Load
Memory lives at `~/.claude/projects/<cwd with / replaced by ->/memory/` (the replay header prints it). Read `MEMORY.md` and every memory file. The format and the four types (`user`, `feedback`, `project`, `reference`) are defined in the system prompt's memory section. Follow it exactly.

### 1. Replay
Run `uv run tools/dream_replay.py`. It prints each human prompt since the last dream, after the tail of what Claude said just before, so a short "no, too heavy" reads in context. Use `--since YYYY-MM-DD` to widen the window. If it prints nothing, skip to step 4.

### 2. Extract
Go through the replay and list candidates. Look for:
- **Corrections:** "no", "not like that", "still not it", rejected tool calls, a redo after Claude's attempt. Write them as `feedback`, with **Why** and **How to apply**.
- **Confirmed approaches:** the user accepted an unusual choice without pushback, or picked one option out of several. These are `feedback` too. Don't record only failures.
- **Preferences and identity:** language, tone, review style, role. Write them as `user`.
- **Decisions and constraints:** what the project is for, what was ruled out and why. Write them as `project`, with absolute dates.
- **Pointers:** dashboards, URLs, artifacts the user will come back to. Write them as `reference`.

Salience test: *would a future session act differently knowing this?* If not, drop it. Also drop anything the repo already records (code, git history, CLAUDE.md, the wiki itself), one-off task details, and secrets.

### 3. Consolidate
For each candidate:
- **An existing memory covers it:** update that file. Repeated instances strengthen it: generalize the wording and note the evidence ("seen in 3 sessions").
- **New:** write a new file with frontmatter, and link related memories with `[[name]]`.
- **Conflicts with an existing memory:** keep the one with more and more-consistent evidence. If the user explicitly reversed themselves, the reversal wins. If it's genuinely unclear, keep both in the file under `**Open:**` and ask in the report.

### 4. Update
- Verify every file, function, flag or path a memory names still exists (`ls`, `grep`). Fix it or drop it.
- Convert relative dates ("tomorrow", "next week") to absolute ones.
- Update `project` memories whose status changed (shipped, abandoned, superseded).

### 5. Prune
Delete memories that are contradicted, obsolete (finished or abandoned work), duplicated by a merge, or that never mattered. Never delete a `feedback` memory the user stated explicitly unless they reversed it. List every deletion in the report.

### 6. Wake up fresh
- Rewrite `MEMORY.md`: one line per memory (`- [Title](file.md) — hook`), grouped by type, no memory content in it.
- Run `uv run tools/dream_replay.py --stamp` to record this dream, so the next replay starts here.

## Part B: The wiki

Episodes get ingested one at a time, so the same idea lands on several concept pages under different names (a person's *second brain*, an org's *company brain*, the *LLM wiki* that maintains either). Lint only checks that pages are well-formed. Dreaming generalizes them.

### 7. Find clusters
Read `wiki/index.md` and the Summary of every concept page. List clusters of 2+ pages that describe **the same underlying idea**, even at a different scale (personal vs org), from a different angle, or under a different name. The test: *would a reader learning this topic want one page, with the differences as sections?* Pages that only share a domain (both "about memory") are not a cluster. Wiki-structure pages belong to a cluster too. Check `wiki/log.md` for earlier "kept separate" decisions, and revisit them with this test.

For each cluster, propose: the surviving slug (the most general name, or a new one), the pages folded into it, and a one-line why.

### 8. Confirm
Interactive run: show the proposals as a numbered list and ask which to apply. Headless/nightly run (`claude -p`): don't merge. Put the proposals in the report and stop Part B.

### 9. Merge (each approved cluster)
1. **Write the merged page** to the template in `CLAUDE.md`. Rewrite the Summary as one synthesis. Keep **every** claim with its episode and person links. Differences become sub-headings under Key ideas (e.g. "Personal scale" / "Org scale") or go to Disagreements. Union the Takeaways and Related links. Set `hubs`, set `sources` to the number of distinct episodes linked, and set `updated`.
2. **Delete** the folded pages.
3. **Relink:** `grep -rl "concepts/<old>" wiki/` and rewrite every `[[concepts/<old>]]` (including `|alias` forms) to the survivor, in episodes, people, hubs, takeaways and other concepts. Drop self-links and duplicate links that this creates.
4. **Index and hubs:** remove the old lines and update the survivor's line.
5. **Log:** append `## YYYY-MM-DD — dream: merged <old>, <old> → <survivor>` to `wiki/log.md`.
6. Run `uv run tools/lint_wiki.py`, and fix it until it prints `clean`.

Never edit `raw/`. Commit the wiki changes as `dream: merge <old> into <survivor>`.

### 10. Report
Reply with a short table, *Added / Updated / Merged / Pruned*, one line each with the memory or concept name. Mark Part A rows `memory` and Part B rows `wiki`. Follow it with any open questions and any unapplied cluster proposals. The memory directory is outside the repo, so only Part B changes get committed.

## Scheduling
Dreaming fits a nightly run, when compute is idle and cheaper ([[episodes/langtalks--57-memory]]). It can be added to the existing launchd job as `claude -p "/dream"`, but only when the user asks.
