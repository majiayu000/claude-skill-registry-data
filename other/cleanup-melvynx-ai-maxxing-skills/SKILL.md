---
name: cleanup
description: Tidy the user's brain. Finds finished, forgotten or empty projects, duplicates, misplaced folders, loose files and old scratch, proposes what to archive, merge or move, and does only what the user approves. Use when the user types /cleanup, says "fais le ménage", "range mon brain", "archive les vieux projets" or the brain feels messy.
metadata:
  internal: true
---

Keep the brain small, so every session finds the right project fast. The brain is the folder named in the `## Brain` section of `~/.claude/CLAUDE.md` (default `~/brain`): read its `AGENTS.md` first (layout, hubs, hygiene). Talk to the user in their language, without jargon. Never move, merge or trash anything before the user says yes, and never delete permanently: archive what has value, trash only scratch.

1. **Scan.** Run `python3 <brain>/.agents/skills/cleanup/scripts/review.py <brain>`. It reads every `projects/**/About.md` (status, `updated:`, open `Roadmap.md` boxes), takes the last modification date from git (`git log -1 --format=%cs -- <folder>`) and from the newest file on disk (whichever is later wins), writes `<brain>/.tmp/cleanup-review.html` and opens it. The page lists all projects, oldest first, each with a recommendation (Keep, Archive, Trash, Merge into..., Move to...) the user can change, plus a "Copy prompt" button that builds the instruction to paste back here. When `python3` is missing, collect the same facts yourself and skip the page. Then look for the candidates below that the page does not cover (merge, move, fix, tidy).
   - Archive: status `done` still in `projects/`; nothing changed for 60 days or more; `paused` for 30 days or more with no open task; a project whose About.md is still mostly "To fill" and never moved.
   - Merge: two projects about the same thing, or a sub-project that duplicates its hub.
   - Move: a project that belongs to a hub but sits at the `projects/` root, or in the wrong hub.
   - Fix: a project folder with no `About.md`, an `About.md` with no status.
   - Tidy: loose files or folders at the brain root that `AGENTS.md` does not list, empty folders anywhere, `.tmp/` files older than 7 days, `*-final*`, `*-v2*` and report files that duplicate an `About.md`, notes in `notes/ideas/` and `notes/todos/` older than 90 days.
2. **Propose.** Tell the user the page is open: they choose per project, click "Copy prompt" and paste it here. A pasted prompt that starts with "/cleanup : applique mes choix" is their yes (read the "Note générale" and the comment after each `->` as instructions, for example a merge target): skip the question below and go to step 3 with exactly their choices. Without a pasted prompt, also show one short numbered list grouped by Archive, Merge, Move, Fix and Tidy, each line with the project and the reason in a few words ("lumail/old-landing: nothing since 14 May"). Recommend a choice and ask in one message: "all", the numbers, or "none". When nothing needs doing, say the brain is clean and stop.
3. **Do** only what they picked.
   - Archive: fold the final outcome into `About.md` (what was done, where the deliverables are), set `status: done` and `updated:` to today, trash scratch files, keep deliverables, and move the folder to `archives/<folder-name>/` intact.
   - Merge: fold the facts of one `About.md` and `Roadmap.md` into the other (one fact, one place), move its files over, and archive the empty one.
   - Move: move the folder into the right hub.
   - Fix: write the missing `About.md` from what the folder holds, with "To fill" where you would have to guess.
   - Tidy: file each loose file into the project it belongs to, trash empty folders and old scratch, turn an old idea the user still wants into a project with the `create-project` skill, and trash the rest.
   - When the user says a flagged project is still alive, set its `updated:` to today and leave it.
4. **Fix the links.** Search the brain (and the global rules) for each old path you moved and update it.
5. **Save.** Commit with `git add -A` and `cleanup: <what was archived, merged or moved>`, and push when the brain has a GitHub copy.
6. **Report.** Tell the user in 3 to 5 lines what moved where, how many projects are active now, and that `/cleanup` once a month keeps it this way.
