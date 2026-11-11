---
name: journal-add
description: "Append a lesson-learned entry to the journal (.claude/registries/JOURNAL.md root or a .claude/registries/JOURNAL/<domain>.md file) with registry_append.py. Use when: the user says /journal-add, 'log a lesson', 'add to the journal', 'record this for next time', or after a production incident / debugging session / contract review surfaces a non-obvious insight that future contracts should heed. The journal is read by data-architect (Step 1) and contract-critic on every run."
user_invocable: true
---

# /journal-add — Append Lesson to the Adaptive Engineering Journal

When this skill is invoked, append one entry to the journal with `registry_append.py`: to a domain file under `.claude/registries/JOURNAL/` (project lessons), or to the Universal tier of `.claude/registries/JOURNAL.md` with `--universal` (plugin-generic lessons, or no project context).

The journal is the only feedback loop that carries lessons forward between concept contracts. `data-architect` reads it before drafting and `contract-critic` matches every entry's `Apply when:` pattern against new drafts. A well-written entry prevents the same defect from recurring.

## Step 0: Read the journal before appending

Always `Read` `.claude/registries/JOURNAL.md` (the Universal root) and the domain files beside it, `.claude/registries/JOURNAL/*.md` (`general.md` always exists on registry layout 2), first. You need:
1. The layout: the root holds only the Universal tier and a pointer; project lessons live in the domain files.
2. The existing titles, so the new entry does not duplicate one (the script rejects a duplicate title across the root and every domain file).
3. The exact entry shape documented in the header.

On a project that has no `JOURNAL/` folder yet, read the root alone; the script still appends correctly (see Step 3).

## Step 1: Gather the entry fields

Use `AskUserQuestion` to collect each field unless the user already provided it in the slash-command argument.

The five required fields (template entry shape):

1. **Title** — short, scannable, action-oriented. Examples: `Reuse MarketElements + IFieldResolver for symbol characteristics`, `Don't hand-author EF migrations on tables > 10M rows`. Avoid generic titles like `Bug fix lesson`.

2. **Trigger** — one of:
   - `pre-approval critic` — surfaced during /design-first Step 5 from a contract-critic finding the user confirmed.
   - `post-approval` — the contract had already been approved (or implemented) when the issue surfaced. Pick this when a flaw in an approved design was uncovered by anything other than `fullstack-code-reviewer` (production incident, a follow-on contract revealing a flaw upstream, manual audit). Fires the accuracy-skip "post-approval" signal — the source contract's areas lose their clean streak.
   - `post-impl divergence` — surfaced by fullstack-code-reviewer when the contract turned out to be wrong vs the shipped code. Also fires the accuracy-skip signal (same `post-*` family).
   - `manual` — surfaced outside the protocol AND not tied to a specific approved contract (debugging unrelated to a contract, generic process insight). Does NOT fire the accuracy-skip signal.

   **Trigger selection rule:** if `Source contract:` points at a contract whose Status is `approved` or `implemented`, pick `post-approval` or `post-impl divergence` — NOT `manual`. The contract-critic accuracy system relies on this signal to reset the area's clean streak; mis-tagging it as `manual` silently swallows the failure signal.

3. **Source contract** — full path to `.claude/concepts/<slug>.md` if the lesson came from a contract review, or `N/A` for manual entries.

4. **Lesson** — one line, ACTIONABLE. Format as `Do X` or `Avoid Y when Z` or `When in <pattern>, reach for <mechanism>`. NOT `Be careful with X` (not actionable) and NOT a paragraph (too long).

5. **Apply when** — concrete signal a FUTURE contract should heed this. Phrase as a pattern the contract-critic checklist can match against. Examples: `contract adds a new symbol characteristic field`, `contract proposes a new background ingestion job`, `contract introduces a value object that already has a MECHANISMS.md analog`.

6. **Tags** — comma-separated keywords for grep. 2–5 tags. Examples: `reuse, MarketElements, field-resolver` or `ef-migration, large-table, online-index`.

If the user passed the title as the slash-command argument (e.g. `/journal-add Reuse MarketElements`), use it as `Title` and ask only the remaining four questions.

## Step 1.5: UI-lesson check

After gathering the basics, ask one focused yes/no question via `AskUserQuestion`:

> **Is this a UI lesson?** (Will the `ui-ux-designer` agent benefit from re-reading this on every invocation?)

If yes:

- **Enforce `ui-evolution` in the Tags line.** If the user's Step-1 Tags list does not include it, prepend `ui-evolution` automatically.
- **Ask the optional app scope** via a second `AskUserQuestion`: "Which app does this apply to?" — one option per application named by the `frontend.roots` slot of `.claude/project-profile.md`, spelled `app:<name> only`, plus an `all apps (no sub-tag)` option. If an `app:*` option is picked, append the chosen sub-tag to the Tags line.
- **Recurring-mistake check.** If the user described this as a repeat occurrence (e.g. "the third time we hit this"), also append `recurring-mistake` to the Tags line. This is the signal `/promote-ui-rule` reads when gating automated guard-rule promotion.

If no, skip this step. (The ui-ux-designer agent's Step 0 grep would still pick up the entry on a tag match, but you avoid the noise of marking generic lessons as UI-tagged. In a project that installed the angular-tailwind add-on, that add-on's advisor does the same at every prompt.)

**Optional Areas line.** For any entry (UI or not) whose `Source contract:` is `N/A` (manual entries), offer to append an `Areas:` line so the cross-area scanner can attribute the lesson to specific buckets. Use `AskUserQuestion` with the options drawn from `.claude/area-mapping.json` keys + `(universal — no Areas line)`. The user picks any subset; the Areas line gets the comma-separated slugs. Skip the prompt for non-manual triggers — those derive their area from the Source contract automatically.

## Step 2: Choose the destination

The destination is a flag of `registry_append.py`, never a hand edit:

- A project lesson: pass nothing and the script files it in the domain file named after the `Source contract:`'s area when that file exists, else in `general.md`. To choose a domain yourself, pass `--domain <slug>` (a file that exists in `.claude/registries/JOURNAL/`); a new domain needs `--create-domain` as well.
- A plugin-generic lesson that applies to every project, or no project context (CWD is `~/.claude` or unrelated): pass `--universal`, which appends to the end of the Universal tier of the root file.

## Step 3: Append the entry

Write the entry to `.claude/cache/registry-appends/<slug>.md` with the `Write` tool (create the folder if missing; it is a cache folder, never committed). NEVER reorder or rewrite existing entries: the script only appends.

Find `registry_append.py` with the standard lookup block (pinned by `test_skill_script_lookup.py`), then run it with the project root:

```bash
RAP=
S=.claude/scripts/registry_append.py
if [ -f "$S" ]; then RAP=$S
elif [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then RAP=$CLAUDE_PLUGIN_ROOT/$S
else
  # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
  CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
  ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
  REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
  MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
    P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
    [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
  done)
  NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
  RAP=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
    [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
  done)
fi
py -3 "$RAP" --project "$CLAUDE_PROJECT_DIR" --registry journal --from-file .claude/cache/registry-appends/<slug>.md
```

If `RAP` comes back empty, stop and say so. Add `--universal` or `--domain <slug>` per Step 2. Show the printed `file:line`, then delete the entry file. What the exits mean: on a project not yet on registry layout 2 it appends to a domain file and prints an advisory line; that is success. Exit 2: fix the entry file and re-run. Exit 3: stop and show the message to the user.

The entry file holds exactly this shape (already documented in the JOURNAL.md header):

```markdown
### YYYY-MM-DD — <Title from Step 1>
- **Trigger:** <Trigger from Step 1>
- **Source contract:** <Source contract path or N/A>
- **Lesson:** <Lesson from Step 1>
- **Apply when:** <Apply-when pattern from Step 1>
- **Tags:** <comma-separated tags from Step 1; with `ui-evolution` and optional `app:*` / `recurring-mistake` from Step 1.5>
- **Areas:** <optional, only when supplied in Step 1.5 for manual entries>
```

The date is today's date in `YYYY-MM-DD` format. If you don't know today's date from session context, use `Bash` with `date +%Y-%m-%d` (POSIX) or PowerShell `Get-Date -Format yyyy-MM-dd`.

## Step 4: Confirm the append to the user

Show the appended entry verbatim and the destination the script printed (the Universal root or a domain file, with its line). One short sentence — no celebration prose.

If this was triggered from `/design-first` Step 5 (the orchestrator confirming a contract-critic finding), the orchestrator already knows what to do next. Otherwise, mention that future `data-architect` and `contract-critic` runs will now read this entry on every invocation — no additional setup is required.

## Step 5: If the user mis-tagged the trigger, ask

If the user said `manual` but the lesson clearly came from a contract review (e.g. they passed a contract path as Source contract), prompt once: `Trigger was set to 'manual' but the source is a contract. Re-tag as 'pre-approval critic', 'post-approval', or 'post-impl divergence'?` Use `AskUserQuestion`. Don't auto-correct.

If the user picked `post-approval` or `post-impl divergence` but Source contract is `N/A` or unresolvable, prompt once: `Trigger '<value>' requires a Source contract path so the accuracy-skip system can reset the area's clean streak. Provide the contract path or change Trigger to 'manual'.` Use `AskUserQuestion`. Don't auto-correct.

## Version raise

A registry append is a shipped change: batch it into a change that already raises the plugin version, or raise at least a patch version (see CLAUDE.md, "Every change to shipped plugin files bumps the plugin version").

## What this skill does NOT do

- Does NOT write to any file other than the journal (`.claude/registries/JOURNAL.md` or a `.claude/registries/JOURNAL/*.md` file), and only through `registry_append.py`; its entry file under `.claude/cache/registry-appends/` is deleted after success.
- Does NOT modify or reorder existing journal entries — append-only. A correction to an earlier entry is a `--correction-of "<title>"` line added by the script.
- Does NOT validate the lesson content for quality — that's the human's call.
- Does NOT trigger any agent or downstream workflow. The next time `data-architect` or `contract-critic` runs, they read the journal naturally.

## Hard refusals

If the user provides a Lesson that is just a paragraph or a multi-sentence explanation:

> "Journal entries are one-line actionable lessons. What you wrote is closer to a postmortem section. Compress to one line of `Do X` / `Avoid Y when Z` form, and I'll append it. The longer context belongs in the source contract or a separate handbook entry."

If the user tries to log something that contradicts an existing journal entry without referencing it:

> "There's an existing entry `<date — title>` that says `<existing lesson>`. Your new entry contradicts it. Either reference the old entry explicitly in the Lesson body (`Refines <YYYY-MM-DD — title>: ...`) or pick one to supersede."

The append-only invariant matters: contradictory entries side by side without cross-reference would teach the critic to flag false positives.
