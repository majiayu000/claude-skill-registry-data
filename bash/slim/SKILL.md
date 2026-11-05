---
name: slim
description: Slim the instructions Claude Code loads in every session (CLAUDE.md, rules, their imports) without losing a rule - weigh them, sort every block, show the changes, write only on the user's go, prove nothing was lost, weigh again.
argument-hint: "[file or folder to slim]"
---

# Slim

Lighten what every session pays before its first word, and lose no rule.
Resolve `scripts/` from this skill's directory. Run each script with Bash
`run_in_background: true` and read its output when it ends: a foreground
Bash may run in another shell, without the session's `CLAUDE_CONFIG_DIR`
or working directory. `<work>` is a new scratch folder for this run.
Talk in the conversation language.

1. **Weigh.** `node scripts/weigh.cjs --save <work>/before.json`. Show its
   table: every file loaded at launch, its size and its share. An argument
   narrows the files to slim; the weighing stays whole.
2. **Sort.** Read each file and give every block one destination:
   - stays loaded: a rule every session needs, kept short;
   - skill: a procedure, or a block for one kind of task. It becomes
     `skills/<name>/SKILL.md` in the same scope (`<config>/skills/` or
     `<project>/.claude/skills/`), its description saying when it applies;
   - `paths:` rule: a block that matters only for matching files. It loads
     after a matching Read, Write or Edit, and user-level patterns start
     from the session's working directory: a rule needed before any read
     stays loaded;
   - evidence: a dated citation, a date, the story of why. It moves word
     for word to `evidence/<file>.md` beside `rules/` (`<config>/evidence/`
     or `<project>/.claude/evidence/`), never inside `rules/`, where every
     `.md` loads.
   List the duplicates and contradictions between files too, each with
   both passages. Never edit `MEMORY.md`, nor a block a tool generates
   (the GitNexus block between its markers): weigh and report them only.
3. **Show.** File by file: what moves where, and each rewritten or removed
   sentence beside its original. Write nothing yet. Ask one question for
   the go; the user may validate some files and not others.
4. **Save.** `node scripts/check.cjs save <work> <files to change>`. Exit
   2 names a file with changes not committed: stop there.
5. **Write** only what was validated. Move text word for word. Each
   validated rewrite or removal goes in `<work>/rewrites.json` as
   `{"from": "<original>", "to": "<new, or empty>"}`. Add once, to the
   CLAUDE.md of that scope, one line saying where its evidence lives.
6. **Verify.** `node scripts/check.cjs verify <work> --in <evidence dir>
   --in <rules dir> --in <each new skill or rule> --rewrites
   <work>/rewrites.json`. It puts back, as it was, any file with a piece
   found nowhere: report each lost piece in one line, and never write that
   file again another way.
7. **Commit** each changed file in the repository that holds it:
   one commit per file, with the evidence, skill or rule it fed,
   `chore(rules): slim <file>`. `git revert` undoes it. A file outside Git
   keeps its `.slim.bak` copy.
8. **Weigh again.** `node scripts/weigh.cjs --compare <work>/before.json`.
   Show before, after and the gain. Counts are estimates; `/context` in a
   fresh session gives the exact one. For stale references, suggest
   `/doctor prompt-audit` (Claude Code 2.1.283 or later) in one line.
