---
name: timefold-write-report
description: >-
  Assembles any Timefold audit/review/comparison/explanation report with the standard conventions:
  a datetime-stamped filename, a metadata block (run date/time, who ran it, which source the findings
  came from, the version of the skill that produced them, and the requested scope) right under the
  title, and a footer crediting that skill. The metadata block is what makes the report re-groundable
  later, by a human reader or by an agent that picks the file up in a fresh session. Output is
  Markdown, either as a saved file or as chat output. Use whenever writing or updating a report from
  Timefold skills or agents, or when another skill's instructions say to follow this skill's report
  conventions.
---

# Write report skill

This skill governs *how a report is assembled, and whether/where it's saved*, not what its findings say.
Whatever skill/agent gathered the findings still owns the report's content and structure. This skill adds
the metadata block, the footer, the save-vs-chat decision, and file-placement conventions on top.

## Why this exists

A report has two readers, and the metadata block is what serves both.

The **human reader** needs to know whether to trust the findings. A report is a point-in-time snapshot: it
was produced by reading one specific state of a dataset or a codebase, evaluated against a checklist or a
process that itself changes over time. Without recording exactly *when* it ran, *against which source*, and
*with which version* of the skill, a reader can't tell a current finding from a stale one, or a full run from
a narrowly scoped one.

The **next agent** needs to pick the report up cold and keep working. A report often outlives the
conversation that produced it. Someone reads it a week later, has a specific follow-up question, and hands
the file to an agent. That agent has none of the original conversation. Everything it needs to re-fetch the
same source data and answer the follow-up correctly has to be written down in the report itself. Metadata
that identifies the source precisely is what turns a report from a dead document into reusable context.

Both readers are served by the same block, so every report-producing skill should carry it rather than each
one inventing its own (or, worse, omitting it).

The output is Markdown, either a file or chat. That is deliberate. Markdown reads well for a person and
loads cleanly as context for an agent. Rendering, styling, and combining the report with other data are the
user's call, not this skill's.

## When to use

Invoke this skill (or read it directly, if you're a skill/agent already in motion) right before presenting a
report, whether as a saved file or in chat, after the findings themselves are already gathered.

## Language

A report is prose written for a Timefold audience, same as any other doc this plugin produces. Write every
part of the report you control directly (the metadata block, the summary, the requested-scope line, the
footer) following the `language-guidelines` skill, which ships next to this one in the same plugin (US
English, no em dashes, active tense, contractions welcome but not required, serial commas, numbers one
through ten spelled out, and so on). If the calling skill/agent supplies the findings prose itself, point it
at the same skill rather than restating the rules here.

## Step 0: Confirm the user actually wants the report as a saved file or in chat output

The skill can report findings in two ways: either write a report file to disk, or just present the findings 
in chat. The latter is useful for quick checks, iterative runs, or when the user wants to see the findings 
before deciding whether to save them. The former is useful for permanent records, PR attachments, or when 
the user explicitly asked for a report file.

Before proceeding to Step 1, check:

1. If the user's instructions for this run already make the choice clear (e.g. "save this as a report",
   "write it to reports/", or conversely "just show me", "don't save it"), use that and skip the question.
2. Otherwise, ask the user which they prefer for this run.

This applies per run, not per session: a saved-file choice on an earlier run doesn't carry over to a later
re-run in the same conversation without asking again, since the user may be iterating and only want the
final run persisted.

Markdown is the only output this skill produces. Don't offer to render the report as a PDF, a Word document,
or a Google Doc, and don't offer to brand it. If the user asks for one of those, say that the skill writes
Markdown and let them convert or restyle it with whatever tool they already use.

## Step 1: Gather the metadata

Run these before presenting the report:

- **Run date + time:** `date "+%Y-%m-%d %H:%M:%S %Z"`
- **Run by:** prefer a logged-in user identity if the session exposes one (e.g. a `userEmail` context
  variable injected into the environment/system-prompt info at the start of the conversation) over the
  bare machine name. If a user identity is available, use it as the primary value and append the machine
  name in parentheses. If no user identity is exposed in this session, fall back to `hostname` alone. 
  Never call a tool or ask the user to fetch this. Only use what's already present in context. Guessing 
  or inventing an identity is worse than the machine-name fallback.
- **Source**: what the findings were read from, precisely enough that someone can go back to it. The
  calling skill names its own source. Two common shapes:
  - *A git repository*, when the report is based on code or docs read from one:
    ```bash
    git -C <repo_root> remote get-url origin
    git -C <repo_root> branch --show-current
    git -C <repo_root> rev-parse --short HEAD
    ```
    If the report spans multiple repos or multiple targets within one repo (e.g. a cross-model comparison),
    gather this once per distinct repo+branch. Collapse into a single bullet if every target shared the same
    repo+branch, otherwise list one bullet per distinct source. If the real repo genuinely isn't accessible
    (e.g. a simulated or dry-run report), say so as a separate sentence after the bullet's value, not as a
    dash-joined aside.
  - *A live source*, such as an API dataset. The calling skill supplies the identifiers, and it should
    supply enough of them to fetch the same data again: which tenant, which dataset, which model, which
    API base URL. See "Make the block enough to re-ground on" below.
- **Skill/plugin version**: identify the skill and plugin who produced the report's *findings* (not
  necessarily this skill), and read the version from where that skill is *installed*. Do not look in the
  working directory. Skills run inside the user's project, and that project is not the plugin, so a
  `.claude-plugin/plugin.json` lookup relative to the working directory finds nothing and the version comes
  out empty. Anchor on the generating skill's own directory instead: in Claude Code that is
  `${CLAUDE_SKILL_DIR}`, and `${CLAUDE_PLUGIN_ROOT}` is its plugin's install directory, both substituted
  into a SKILL.md body. Read the `version` field from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`.
  Some installs copy skill folders without the manifest, so if the generating skill ships a version stamp
  of its own, prefer that. The calling skill says where its version lives.
- **Requested scope**: a plain-language summary of what was actually asked of the generating skill/agent for
  this run: which target(s), which categories/types, any filters, exclusions, or non-default options.
  Pull this from the actual instructions the generating skill/agent was invoked with, not from what the
  skill/agent is capable of in general. If nothing was scoped down (e.g. the user asked for a full,
  unqualified run) say so explicitly (e.g. "No scope restrictions requested") rather than
  leaving it vague. This is what lets a reader later tell a partial/scoped run apart from a complete one
  without having to reread the conversation that produced it.

## Step 2: Metadata block

Insert immediately after the title (and italic subtitle, if the report has one), before the first content
section:

```markdown
## Report metadata
- **Run date:** 2026-07-16 11:23 CEST
- **Run by:** you@example.com (your-machine)
- **Source repository:** org/repo (branch `branch-name`, commit `abc1234`)
- **Skill plugin version:** plugin-name vX.Y.Z (`skill-name` skill)
- **Requested scope:** ...
```

A report based on a live source replaces the "Source repository" bullet with the source bullets its calling
skill defines, in the same position. Never drop the source entirely, and never omit the other four bullets.
If a date, identity, or version value is somehow unavailable, say so explicitly (e.g. "unknown, hostname
command unavailable") rather than dropping the line. "Requested scope" is never omitted, even for a full,
unscoped run. State plainly that it was unscoped.

**Merging extra metadata from the calling skill.** The bullets above are the minimum every report needs,
but the calling skill/agent may have its own context-specific facts worth recording (e.g. the customer or
tenant a report was generated for, an environment name, a dataset ID). Add those as additional bullets in the
same "Report metadata" list rather than a second block. Keep the standard bullets in the order shown
above, then append the calling skill's extra bullets after them, each with its own bold label.

### Make the block enough to re-ground on

Before moving on, apply this test to the assembled block:

> If someone hands only this file to an agent in a fresh session next week, with no access to the
> conversation that produced it, can that agent identify the exact source the findings came from and fetch
> it again to answer a follow-up question?

If the answer is no, a bullet is missing. Add it. A dataset ID with no tenant, or a tenant with no model or
API base URL, fails the test, and so does a report that names a codebase without a commit. Prefer stable,
resolvable identifiers (IDs, URLs, commits) over display names alone, and include the human-readable name
alongside the identifier so the block also stays readable.

Credentials are not metadata. Never write an API key, token, or password into the report, not in the
metadata block, not in an audit log, and not in an example command. The reader supplies their own.

## Step 3: Footer

End the report with one line crediting the skill that produced the findings (not this skill), linking to its
location in the repository it came from. For a skill in this plugin:

```markdown
---
Report generated with https://github.com/TimefoldAI/skills/tree/main/skills/<skill-name>
```

## Step 4: Write the file

This step only applies if the user chose "saved file" in Step 0. If they chose chat output instead, skip
this step entirely: present the assembled report (title, the Step 2 metadata block, the findings, the Step 3
footer) directly in the chat response and stop there. Nothing gets written to disk.

### Step 4a: Where to write the report

Default to `reports/<category>/` at the root of the repo the findings are about.
Don't guess at a different location on your own:

1. If the user already stated a preferred reports location earlier in this conversation, use it.
2. Otherwise, check whether you have a persistent memory of the user's preferred reports location (if you
   maintain a memory system) before asking. A stored preference should say which repo/directory to use as
   the base, not just a bare `reports/` folder name.
3. If you still don't know, ask the user directly before writing anything. Once they answer, consider saving
   the preference in memory (if you maintain one) so future runs don't need to ask again.

### Step 4b: File placement

Every filename carries the same run date/time gathered in Step 1, filesystem-safe (no colons/spaces):
`date "+%Y-%m-%d-%H%M"` (e.g. `2026-07-16-1123`). This keeps re-runs from silently overwriting a previous
report and lets multiple runs for the same target coexist and sort chronologically by filename.

- One file per reviewed target: `<reports-dir>/<category>/<target-name>-<run-datetime>.md`
- A cross-target synthesis, if one was produced: `<reports-dir>/<category>/comparison-<run-datetime>.md`,
  linking back to each individual report by relative path. Use the *same* run-datetime stamp across every
  file produced by one run, so it's obvious at a glance which target reports and comparison belong together.
- If `<reports-dir>/reports.md` exists, add or update a section there indexing the new category, following
  the existing table style (one row per reviewed target, linking into the category's subdirectory). 
  Link to the latest dated file per target; older dated files stay in the directory as history but don't 
  need their own index row.

## What this skill does not do

- It doesn't decide what the report says. That's the calling skill/agent's job.
- It doesn't run any audit, review, or comparison itself.
- It doesn't invent a new report structure. Apply these conventions on top of whatever structure the calling
  skill/agent already uses for its findings.
- It doesn't render, style, or brand the report. Markdown is the deliverable. What the user does with it
  next is up to them.
