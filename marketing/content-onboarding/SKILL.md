---
name: content-onboarding
description: >
  Use this skill when setting up a new marketing project with Claude Code, registering
  context files, or extending the context of an existing project.
  Invoke when the user asks to "onboard a new client", "set up context files",
  "initialize marketing project", "register context", "add context", or "set up project context".
  Also use when context files are missing and the user wants to set up through a guided interview.
allowed-tools: Read, Write, Edit, Bash
argument-hint: "[optional: path to an existing file to register as context]"
---

# Onboarding Skill

You are helping set up or extend the context for a content creation project. Context files
are Markdown documents registered in `CLAUDE.md` — skills load them on demand to produce
on-brand, well-targeted output instead of generic content.

Two paths through this skill:

- **Power user** (existing files): register them quickly with a label and summary
- **New user** (building from scratch): guided interview to create context files

If `$ARGUMENTS` contains a file path, skip to Step 3 using that file as the starting point.

## Step 0: Recall learnings

If `.claude/learnings.md` exists, read it silently. Apply relevant entries — in particular,
path preferences, rejected interview answers, or project constraints discovered in prior runs.
Do not announce this step. If the file is absent, continue normally.

## Step 1: Discover existing context

This skill runs inside the owner's project — an arbitrary repo that may already have its own
structure, possibly with more than one `CLAUDE.md` at different levels (root plus nested ones
for campaigns or sub-brands). Never assume a single root-level file. Scan the whole project:

```bash
find . -name 'CLAUDE.md' -not -path '*/.git/*' -not -path '*/node_modules/*' | sort
find . -type d -iname 'context' -not -path '*/.git/*' -not -path '*/node_modules/*' | sort
```

For each `context/`-like folder found, list its files too — registered tables only show what's
already been formally added, and a folder can hold files nobody registered yet:

```bash
for d in <each context-like folder path from the find above>; do
  echo "=== $d ==="
  find "$d" -type f -name '*.md' | sort
done
```

For each `CLAUDE.md` found, check whether it already has a `## Context files` table:

```bash
for f in <each CLAUDE.md path from the find above>; do
  echo "=== $f ==="
  grep -A 200 '## Context files' "$f" 2>/dev/null || echo "(no context table)"
done
```

Keep the full list of discovered `CLAUDE.md` paths — Step 5 needs it to decide where each newly
registered file belongs.

If any `CLAUDE.md` or `context/`-like folder was found, show the owner the full picture,
grouped by location so the scope of each is clear:

> "Here's what your project already has set up:
>
> **Root** (`CLAUDE.md`)
>
> | Label                                        | File | Summary |
> | -------------------------------------------- | ---- | ------- |
> | <existing rows, or "(no context table yet)"> |
>
> **`campaigns/q3/CLAUDE.md`** (nested)
>
> | Label           | File | Summary |
> | --------------- | ---- | ------- |
> | <existing rows> |
>
> Would you like to add more context? (yes / no)"

(Placement — which `CLAUDE.md` a new row belongs in — is decided per file in Step 5, not here;
this step is only surfacing what already exists.)

If nothing was found anywhere (no `CLAUDE.md`, no `context/`-like folder), this is a greenfield
project — continue to Step 2 directly.
If structure exists but tables are empty or only partially filled, continue to Step 2, keeping
the discovered locations in mind for Step 5.

## Step 2: Surface common starting points

If context is sparse or absent, present the most common types of context that make a
meaningful difference to output quality. These are suggestions, not required slots.

> "Content skills produce much better output when they have project context to work from.
> Here are the most common types — does any of this apply to your project?
>
> - **Brand voice / writing style** — tone, vocabulary, phrases to use or avoid
> - **Organization or author profile** — who you are, what you do, your positioning
> - **Audience profiles** — who you're writing for, their goals and challenges
> - **Default output language** — a simple note like 'Output language: German (de-DE)'
> - **Format rules for specific output types** — e.g. 'all whitepapers follow this structure'
>
> These are just the most common starting points. Register whatever context is relevant
> for your project — there are no restrictions on types, file names, or locations.
>
> Do you already have files you want to register, or would you like to create context
> files through a short interview? (You can also describe something not on this list.)"

Wait for the owner's response and route accordingly:

- **Have existing files** → go to Step 3 for each file
- **Want to create files** → go to Step 4
- **Something not on the list** → treat as custom context; go to Step 3 or 4 as appropriate
- **Nothing / skip** → go to Step 5

## Step 3: Register an existing file

For each file the owner wants to register:

Read the file.

Suggest a label based on the file content — brief, descriptive, and free-form. The label
appears in the CLAUDE.md table and is what the owner will recognize at a glance.

> "Suggested label: **[label]**
> (or enter your own — no restrictions on naming)"

Generate a one-sentence summary (10–25 words) from the file content. The summary is the key
signal skills use to decide which file is relevant for a given task — be specific:

- Too vague: "Writing style guidelines for the company"
- Good: "Formal German, em-dash preferred, no exclamation marks — all corporate copy"
- Good: "Casual and inclusive tone — job ads and employer branding only"

Show the proposed table row:

> "I'll register this in your CLAUDE.md context table as:
>
> | [label] | [file path] | [summary] |
>
> Confirm? (yes / edit / skip)"

(The `File` path shown here is illustrative — Step 5 determines the actual target `CLAUDE.md`
and adjusts the path to be relative to that file's own directory.)

- **Yes**: record the row for Step 5
- **Edit**: ask what to change, update, show again
- **Skip**: discard this file

After handling this file, ask: "Would you like to register another file, or create a new
context file? (yes / create / done)" and loop back to Step 3, go to Step 4, or proceed to Step 5.

## Step 4: Create a new context file

When the owner wants to create a context file from scratch:

Ask:

> "What should this context file cover? Describe it in a few words
> (e.g. 'our brand voice', 'company background', 'reader personas')."

Based on the answer, ask targeted questions one at a time. Adapt questions to what the owner
described — the following are starting points, not a fixed script:

**For brand voice / writing style:**

1. "How would you describe the tone? (e.g. authoritative, conversational, warm, technical)"
2. "What words or phrases does the brand use frequently?"
3. "What words or phrases should never appear?"
4. "Any formatting or punctuation rules? (e.g. no exclamation marks, em-dash preferred)"
5. "Any reading level or vocabulary target?"

**For organization or author profile:**

1. "What is the name and a one-sentence description of what you do?"
2. "What are the main products or services?"
3. "What makes you different from competitors?"
4. "Any values, principles, or positioning worth noting?"

**For audience profiles:**

1. "How many distinct audience segments? (1–4 recommended)"
   For each segment, ask: role or title; primary goals; biggest challenges; preferred channels.

**For default output language:**

1. "What is the default output language for all content in this project?
   (e.g. German / de-DE, English / en-US, French / fr-FR)"

**For format rules specific to a content type:**

1. "Which content type do these rules apply to?"
2. "What are the mandatory structural elements or rules?"

**For any other context type:**
Ask open-ended questions appropriate to what the owner described. The goal is to capture the
information that will make content skills produce better output for this specific project.

After collecting answers, ask:

> "Where should I save this file? (Suggested: `context/<descriptive-name>.md` — but any
> path works, e.g. `brand/voice.md` or pointing to an existing folder.)"

Write the file with a clear heading and the owner's answers organized under descriptive sections.
Match the structure to the content type — do not force a generic template.

After writing, confirm: "✓ Created `[path]`." Then proceed to Step 3 to register it.

## Step 5: Update CLAUDE.md

Collect all rows confirmed in Steps 3–4.

If no rows were confirmed, skip to Step 6.

For each row, determine its target `CLAUDE.md`: walk up from the registered file's directory
and use the nearest `CLAUDE.md` found during Step 1's scan (the root file counts as the
outermost ancestor). Group rows by target file — a single onboarding run can touch more than
one `CLAUDE.md`.

**If the nearest ancestor is more than one directory level above the file** (e.g. the file
lives in `campaigns/q3/` but the nearest `CLAUDE.md` is at the project root), don't default
silently — ask first:

> "`[file]` lives in `campaigns/q3/`, but the nearest CLAUDE.md is at the project root.
> Would it make more sense to create a `campaigns/q3/CLAUDE.md` scoped to that campaign,
> or register it in the root table? (new nested file / root)"

- **New nested file**: treat this location as "target CLAUDE.md does not exist" below.
- **Root** (or whichever existing ancestor the owner picks): register the row there.

For each target `CLAUDE.md`, check its current state:

```bash
grep -c '## Context files' <target CLAUDE.md path> 2>/dev/null || echo "0"
```

**If `## Context files` section exists in the target file:**

Show only rows that are not already in its table, with `File` paths made relative to that
target file's own directory:

> "I'll add these rows to the context table in `[target CLAUDE.md path]`:
>
> | Label      | File | Summary |
> | ---------- | ---- | ------- |
> | <new rows> |
>
> Shall I proceed? (yes / edit / skip)"

- **Yes**: append the rows to that table. Confirm: "✓ `[target CLAUDE.md path]` updated."
- **Edit**: ask what to change, update, show again.
- **Skip**: note that this table was not updated.

**If the target CLAUDE.md exists but has no `## Context files` section:**

> "I'll add a context table to `[target CLAUDE.md path]`:
>
> ## Context files
>
> <!-- cc-config: context-toc-registered -->
>
> Skills read all registered files and load what's relevant for each task.
>
> | Label                | File | Summary |
> | -------------------- | ---- | ------- |
> | <all confirmed rows> |
>
> Shall I proceed? (yes / edit / skip)"

The `<!-- cc-config: context-toc-registered -->` comment is load-bearing: if this
project also uses `cc-config`'s `scripts/sync-config-table.sh`, that script greps
for this exact marker to know these files are already registered here (with real
summaries) and must not be re-listed in `## Key Config Files` under a generic
placeholder. Always include it when creating this section — whether or not the
sync script is present in this project, since it's harmless either way.

If the section already exists but is missing the marker (e.g. it predates this
convention or was written by hand), add the marker line as part of this update
rather than leaving it out.

**If the target CLAUDE.md does not exist** (no ancestor was found at all, or the owner chose
to create a new nested one above):

Ask: "There is no CLAUDE.md at `[target folder]` yet. What should its heading say — a project,
client, or campaign name?"

Create it at that location, with `File` paths relative to that new file's own directory:

```markdown
# [Name]

## Context files

<!-- cc-config: context-toc-registered -->

Skills read all registered files and load what's relevant for each task.

| Label  | File | Summary |
| ------ | ---- | ------- |
| <rows> |
```

Confirm: "✓ `[target CLAUDE.md path]` created."

Repeat until every row has been placed in its target file.

## Step 6: Folder structure nudge

After updating CLAUDE.md, add a practical tip:

> "**Tip:** Content skills can also find unreferenced files on demand — for example,
> 'check how we wrote the invitation for the XYZ event last year'. This works best with
> meaningful file names (e.g. `xyz-event-invitation-2025.md`, not `draft-v3-final.md`)
> and a folder structure you can describe in a sentence.
>
> Want to add a one-line note to your root CLAUDE.md describing how this project's content
> is organized? (yes / describe it / skip)"

- **Yes or owner describes it**: add a `## Folder structure` note to the root `CLAUDE.md`
  (this is a project-wide orientation note, not campaign-scoped, so it belongs at the root
  even if other context was registered in nested `CLAUDE.md` files during this run).
- **Skip**: continue.

## Step 7: Summary

```
Context setup complete
──────────────────────────────────────────────────────
Registered:    <N> context file(s)
CLAUDE.md:     ✓ <path> updated (or: ✓ created / ✗ skipped)
               ✓ <path> updated (repeat per target file touched)
──────────────────────────────────────────────────────
```

Then say:

> "Your project context is ready. Content skills will read the registered files and
> load what's relevant for each task — producing more on-brand, targeted output.
> You can run this skill again any time to add more context, or use
> `/register-context` to quickly register a file mid-session."

## Step 8: Store learnings

Before ending, review the interview for nuances that were discovered but not formalized
into any context file created during this run.

For each qualifying observation, append one tagged line to `.claude/learnings.md`
(create with standard header if missing):

```text
[cc-content:content-onboarding] <concise observation> — <YYYY-MM-DD>
```

**Qualifies:** a preference, constraint, or project fact revealed during the interview
that is not already captured in any context file written this run, in `CLAUDE.md`, or
in any existing `.claude/learnings.md` entry under any plugin tag.

**Does not qualify:** information written into a context file just now; facts already
in `CLAUDE.md`; standard onboarding behavior applied without deviation; facts
semantically equivalent to any existing entry — when in doubt, skip; redundancy is
worse than a missed entry.

Check for the file before appending:

```bash
ls .claude/learnings.md 2>/dev/null && echo "exists" || echo "missing"
```

Standard header when creating the file:

```markdown
# Learnings

Corrections and feedback collected during content sessions.
Entries are tagged by skill and dated.

---
```

If any entries were written, confirm: "✓ N learning(s) saved to `.claude/learnings.md`."
If nothing qualified, skip silently.
