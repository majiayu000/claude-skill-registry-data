---
name: task-draft
description: Turns a request source — a chat thread, a page, a spoken agreement — into a task record's context table. Statements from the source are sorted into named rows, and what is fact, what is your inference, and what nobody has decided yet are labelled apart rather than blended. Creates a new record where none exists, or fills only the empty cells of one that does. Filing it in the engineering tracker belongs to /pm:task-publish. Triggers - "/pm:task-draft", "draft a task from this thread", "fill in the context table", "일감 초안 잡아줘", "맥락표 채워줘", "이 스레드로 일감 만들어줘".
allowed-tools: AskUserQuestion, Read, Write, Bash, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-create-pages, mcp__claude_ai_Notion__notion-update-page, mcp__claude_ai_Notion__notion-get-users, mcp__claude_ai_Slack__slack_read_thread, mcp__claude_ai_Slack__slack_read_channel, mcp__plugin_github_github__issue_read, mcp__plugin_github_github__issue_write
---

# task-draft — a request source into a task's context table

**Part of a plugin.** The scripts this skill runs ship beside it under `${CLAUDE_PLUGIN_ROOT}`. If that path does not resolve, this file was installed on its own — stop and say the plugin itself is needed (`claude plugin install pm@byjunyoung`), rather than improvising what the scripts do.

Takes a **request source** — a chat thread, a document, a conversation someone relayed — and fills the context table of a task record. It sorts what was said into the rows your team uses, and keeps **fact, inference, and undecided** visibly apart. With no existing record it creates one; with one that exists it fills only what is empty. Filing the task in an engineering tracker is out of scope — that is `/pm:task-publish`.

## Principles

- **Write only from what you were given. Never invent.** Every cell traces to something in the source. A cell you cannot fill is filled **by asking, or left empty** — not by guessing. Interpretation you added while sorting carries `labels.assumption`; what nobody has settled carries `labels.tbd`.
- **Properties are confirmed, not chosen.** Infer a recommendation for each property from the source, then let the user pick it in one short `AskUserQuestion` round. Never settle a property silently.
- **Product language.** No engineering vocabulary. Write as far as *what* is being asked for; *how* is undecided or delegated.
- **Cells are short.** A context table is a list of items, not a description. The sentence rules are in section 2.
- **Provisional stays provisional.** If whether to build the thing at all is still open, the scope rows are provisional and the preview says so.
- **Every external write goes through preview → "go".** Creating and filling alike. Read back afterwards to verify.

## Configuration

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/resolve-config.py --name pm-conventions.yaml --need task.record.ref
```

A `null` named on stderr is a config gap, not a tracker problem — `/pm:setup` writes it. Stop on it rather than interviewing for the value here.

`task.record.type` decides where the record lives, `task.context_rows` names the rows, and `task.properties` lists the values a record can take. Nothing is written into this document. A `null` means that lookup is skipped — say so in the result rather than stopping.

## Input and mode

What it takes: ① the source (a link or pasted content) ② optionally, an existing task record's URL.

    no record URL                  → [create]  make a record and fill the table
    record URL, empty cells        → [fill]    fill only the empty cells
    record URL, cells to revise    → [revise]  rewrite filled cells from new information

Fill and revise can happen in one run — empty cells get filled, and only the filled cells that new information actually touches get revised. If no source came in, ask which kind it is before anything else.

## 1. Read the source (zero writes)

Branch on the kind of link and read it. Do this first, without asking.

- **A chat thread** — read the whole thread, parent and replies, so the shape of the discussion is visible, not just the last message. For a threaded platform, resolve the thread root before reading. Attached images and video count only as filenames and context. The calls for the tool the link belongs to are in its source adapter — `adapter.py --kind sources --type slack --role chat` for a Slack permalink, the type from the link's domain or `sources.chat_type`. Exit 3 means no adapter for that tool: stop and say so rather than improvising the read.
- **A document page** — fetch the body.
- **Anything else** (a design link, pasted text) — take what you were given as the evidence.

## 2. Sort into the context table

Sort what you read into `task.context_rows`. Leave a row empty where nothing applies. The default rows and what belongs in each:

| Row | What goes in |
|---|---|
| Request source | The original link. In create mode, the link you were handed |
| Initial request | What is being asked for, in a sentence or two. Name who asked |
| Background (AS-IS) | Why the request came up — the incident, the symptom, the current limit. Dates and figures exactly as the source has them, and only if the source has them |
| Goal (TO-BE) | What should be different afterwards |
| Scope In | What this piece of work covers. Marked provisional if it is |
| Scope Out | What is being split off or deferred, grounded in something the source actually says |
| Undecided | The open decisions, with an owner where there is one |

- Break several items inside a cell onto their own lines, led by `cell.bullet`.
- **Do not invent a row the source does not support.** If a core row comes out empty, **ask** and fill it; what is still unsettled stays as `labels.tbd`. Peripheral rows may stay empty. Keep "not yet sorted", "not yet decided", and "does not exist" distinct from each other.

### Cell sentences — short and dry

A context table is scanned. Write items, not prose.

- One item per line, around `cell.max_chars`. Two clauses in a row means cut it
- End on a noun, no full stop
- Cut passive constructions and parenthetical insertions
- Attach an owner with `cell.owner_marker`, e.g. `confirm — engineering`
- The Undecided row is one line of the issue plus `labels.tbd`. Do not explain why it is undecided

| Drifting draft | Fixed |
|---|---|
| A and B are paired but C has no corresponding entry, so it is not confirmed which of them is in a usable state | A·B paired, C missing |
| A re-examination of the existing policy is required at this time | existing policy needs re-examination |
| That item requires confirmation through the engineering team | confirm — engineering |
| A decision on whether to do X as Y or as Z has not yet been made | X as Y or Z — TBD |

Finer points of style follow whatever writing standard applies where it is being written.

## 3. Preview → "go"

Show the target and the table as markdown. In create mode, show the properties you settled by interview **in the same preview**, and close the whole thing once with `shall I proceed? (go / changes)`. Where assumptions, provisional scope, or TBDs are mixed in, say so at the end of the preview.

## 4. Apply

### Fill

Replace the empty cells row by row, matching on the row label. A request-source row that is already filled is never touched.

### Revise

Rewrite a filled cell **only where new information arrived** — another source, a conversation, a decision. Never change existing content without evidence.

- Touch only the cells that change. Everything else, including the source row, stays.
- Move a newly settled fact into the row it now belongs in — something that was Undecided becomes Background or Scope, and comes out of Undecided. A resolved TBD is deleted.
- For a source that is not a link, note the origin in the cell itself.
- Preview a **per-cell before → after diff**, then go. Replace narrowly — the changed substring, not the whole row — and avoid matching on lines containing characters your document tool treats specially.

### Create

Create the record in `task.record`, writing properties and body in a single write.

**Properties** — infer a recommendation from the source, then confirm them **in one grouped `AskUserQuestion`**. Never settle silently. A property with no basis for a recommendation is asked plain, and if it is still unsettled, left empty.

| Property | Value |
|---|---|
| Title | A noun phrase naming the work, in the grammar the list's other records already use — read a few before writing one. Never a sentence stating the symptom: that is what a defect is called. Short, confirmed with the user |
| Project | One of `task.properties.projects`, recommended from context. Empty list means ask |
| Group | The feature grouping. Interview when unsure |
| Assignee | `task.properties.default_assignee`, or ask |
| Priority | One of `task.properties.priority` |
| Status | `task.properties.status_initial` |
| Version | `task.properties.version_unset`, where `task.properties.version` is named. A new record has no ticket and so no milestone to copy — not asked |
| Link to mirror | Left empty — `/pm:task-publish` fills it |

The calls are in the adapter for `task.record.type`:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/adapter.py --name pm-conventions.yaml --kind trackers --type {task.record.type} --role record
```

It prints the file to read — the bundled one, or yours from `adapters.dirs` where you drafted one. **Exit 3 means no adapter exists for that type.** Stop and say so; `/pm:setup` drafts one from the tools connected on this machine. Do not improvise the calls. **Exit 4 means the adapter exists but answers for the other side** — a mirror-only file asked for the record, say. Stop the same way; 3b drafts the side that is missing. Say what it means in the person's words — "this tool isn't supported yet; `/pm:setup` can add it from what's connected here" — never the exit code or the file path.

**Read the tracker's own schema immediately before writing** and match the option names it currently has. Never trust option values pinned in this document or in the config — they drift.

**The body skeleton** comes from `task.notion.body_template` where one is set. Where it is `null`, write the context table alone and say that no template was applied. Some tools do not apply a database template automatically, which is why the skeleton is written explicitly rather than assumed.

## 5. Verify

Read the record back and confirm the rows landed as intended and the table structure is intact. Report it in one line. In create mode, include the new record's URL.

## When NOT to invoke

- Filing the task in an engineering tracker → `/pm:task-publish`
- Reconciling many tasks across two trackers → `/pm:task-sync`
- Writing the requirements themselves → `/pm:prd`
- Auditing a design file → `/fig:lint`
