---
name: task
description: Drafts a task from a request, files it as a ticket in the engineering tracker, or keeps the task list in step with that tracker. Triggers - "/pm:task", "/pm:task draft", "/pm:task publish", "/pm:task sync", "draft a task from this thread", "fill in the context table", "file this task as a ticket", "update the GitHub task", "reconcile the tasks", "sync notion and github", "일감 초안 잡아줘", "맥락표 채워줘", "이 스레드로 일감 만들어줘", "깃헙에 일감 등록해줘", "이 일감 티켓 만들어줘", "티켓 갱신해줘", "일감 동기화해줘", "노션 깃헙 맞춰줘", "정합화 돌려줘".
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-create-pages, mcp__claude_ai_Notion__notion-update-page, mcp__claude_ai_Notion__notion-query-data-sources, mcp__claude_ai_Notion__notion-get-users, mcp__claude_ai_Slack__slack_read_thread, mcp__claude_ai_Slack__slack_read_channel, mcp__plugin_figma_figma__get_metadata
---

# task — one task record, three ways to work on it

**Part of a plugin.** The scripts this skill runs ship beside it under `${CLAUDE_PLUGIN_ROOT}`. If that path does not resolve, this file was installed on its own — stop and say the plugin itself is needed (`claude plugin install pm@byjunyoung`), rather than improvising what the scripts do.

Read this file first, then the mode's file, and follow both. What the three modes share — config, the adapters, the rules every mode follows — is written here once and nowhere else; a mode file holds only what is its own, and names the section here where it leans on one.

## Which mode

```
/pm:task draft <source> [<record>]
/pm:task publish <record> [--contract | --template]
/pm:task sync [mine]
```

Without a mode word, the request decides: a thread, page or conversation to turn into a task → `draft`; "file / publish / update the ticket" → `publish`; "reconcile / sync" → `sync`. Ask only when it is still unclear.

- `--contract` writes only the contract's own sections, to the level `task.contract.level` names, instead of filing or updating the task's ticket — `publish.md`, *Inputs*
- `--template` runs *Bringing a ticket back to the template* in `publish.md` directly, on the ticket the record links to. It is the way out `sync` names for a ticket it finds off its template

## Config

Config is read in two stages, because a team with no tracker attached is not missing a setting — it has nothing to file into or reconcile against, and the answer to that is not "a property is unset".

**Stage 1 — every mode, before anything else.**

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/resolve-config.py --name pm-conventions.yaml \
  --authored task.record.type,task.record.ref
```

`task.record` is where the task lives, `task.mirror` is the tracker it is filed into. **In `publish` and `sync`, where `task.mirror.type` is `none`, stop with this, and nothing else:**

> These tasks are kept as records only — nothing is set up to file them into. `task.mirror` is the setting that attaches a tracker; `/pm:setup` reads its schema and fills it in.

`draft` carries on: a record needs no tracker.

**Stage 2 — the mode's own call.** `draft`:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/resolve-config.py --name pm-conventions.yaml \
  --need task.record.ref --authored task.record.type,task.record.ref
```

`publish`, a tracker attached, so the rest must be named:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/resolve-config.py --name pm-conventions.yaml \
  --need task.record.ref,task.link_property,task.mirror.ref \
  --authored task.record.type,task.record.ref,task.link_property,task.contract.level
```

Under `--template`, leave `task.contract.level` out of that `--authored` list. The template pass only renames, reorders and drops headings — it writes no contract — so a level nobody chose cannot put anything on the wrong ticket, and stopping on it would block the one way out `sync` names.

`sync`, the same, with a shorter `--authored`:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/resolve-config.py --name pm-conventions.yaml \
  --need task.record.ref,task.link_property,task.mirror.ref \
  --authored task.record.type,task.record.ref,task.link_property
```

`sync` adds `task.contract.level,task.progress_source` to that `--authored` list only where `task.properties.progress` is named (non-null in the resolved config) — both feed only the progress checks, which are inert without the property, so a config that never mentions the keys must not be stopped on the floor's copy of them.

A `null` named on stderr is a config gap, not a tracker problem — `/pm:setup` writes it. Stop on it rather than interviewing for the value here, or running against a side that was never named.

**`--authored` is the other half, and `--need` cannot see what it sees.** A key no config of theirs mentions still resolves — to the bundled floor — so it reads as answered. `task.contract.level` is the one that decides which ticket carries the binding sections, and the floor says `task`: a team whose tracker reviews at the parent, running on a config that never named it, gets a contract filed onto the wrong ticket and no sign that anything was assumed. Where the stop fires, the message names the key and says where the copy came from — a config that has fallen behind a shared one is the usual cause, and the lines underneath say by how much. Do not interview for the value and do not proceed on the default: neither answers who chose it.

## Adapters

**The calls themselves live per tracker**, not in these files. Two copies of a command means one gets fixed.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/adapter.py --name pm-conventions.yaml --kind trackers --type {task.record.type} --role record
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/adapter.py --name pm-conventions.yaml --kind trackers --type {task.mirror.type} --role mirror
```

| Mode | Reads | When |
|---|---|---|
| `draft` | The record's, for any `task.record.type` but `markdown` — a markdown record goes through `markdown-tracker.py` instead. A chat thread's source adapter as well (`draft.md`, step 1) | Before it looks for, creates or edits a record |
| `publish` | Both | Before the record is first read — the parent search and the duplicate check call the mirror long before anything is attached |
| `sync` | Both | Before scanning. They also carry what each tool cannot do, which is what the coverage line reports |

`adapter.py` prints the file to read — the bundled one, or yours from `adapters.dirs` where you drafted one. **Exit 3 means no adapter exists for that type.** Stop and say so; `/pm:setup` drafts one from the tools connected on this machine. Do not improvise the calls. **Exit 4 means the adapter exists but answers for the other side** — a mirror-only file asked for the record, say. Stop the same way; `/pm:setup` 4c drafts the side that is missing. Say what it means in the person's words — "this tool isn't supported yet; `/pm:setup` can add it from what's connected here" — never the exit code or the file path.

## Rules every mode follows

- **Matching runs on `task.link_property` alone** — the property on the record that holds the ticket's url, one to one. A back-link written in the ticket body is for a human to click, never for matching: it can point at a source that was already discarded, and that is exactly how past mis-matches, duplicates and resurrected tickets happened
- **Never invent a mapping.** A project, priority or assignee with no entry in the config is never guessed at. `publish` stops the run with a message — a wrong label is harder to find later than a missing ticket; `sync` skips the row and reports it. In `sync`, **a user id found on another record is not a mapping** — copying it onto a second record because the tracker shows the same name is exactly the invention this rule forbids. An assignee reaches the record only through `task.assignee_map`
- **Every external write is previewed, and waits for "go".** Creating a record and filling one, filing a ticket and editing one, the write-back into the record, and the `(unverified)` edits below alike. Each mode's file says what its preview holds. Read back afterwards to verify

### Written for the people who will act on it

These are the title rules. A task is read by whoever picks the work up, and by everyone downstream who has to know what it covers — the person drawing the screens, the one deciding what is in scope this release, the one answering for it once it ships. Most of them do not read the system it is built on. So the title and the sentences under it say **what somebody will see or do**, not what the machine does underneath — a record's title in `draft`, which follows the first three below; a ticket in `publish`, which follows them all; and what `sync` reports as *Reads as internals*.

- **The title names the work, as a noun phrase.** A word only the internals use — a layer, a gate, a
  flag, a surface — reads as precise to whoever coined it and as nothing at all to everybody else.
  Where the plain name is longer, it is still the shorter path to somebody knowing what the ticket is
- **Plain wording is not licence to write a sentence.** *The setting nobody can reach* states a
  symptom; it is what a defect is called, and a task named that way stops reading as something
  somebody is doing. The work is named, and what it is being done to — the grammar the list already
  uses for that is right there in the neighbours
- **Read the sibling titles before writing one.** A list that has been kept by hand has a shape —
  most often `<what> <verb-as-noun>`, and a dash before the part that narrows it. Matching that shape
  is what makes a new row look like it belongs; a title in a grammar of its own reads as an import
  even when every word in it is plain
- **The record's title is the default, not a verdict.** Where it was written in that vocabulary, say
  so in the preview and offer a plainer one beside it. Never change it quietly: the title is the
  record's under `task.field_owner`, and a rename nobody saw is how the two sides start disagreeing
  about what a ticket is called
- **The grounds go under the notes heading.** A clause number, a spec path, a decision id — these say
  why a condition is what it is, and whoever chases the reasoning looks for them there. Inside a done
  condition they crowd out the thing being confirmed
- **Plain is not simplified.** The reader knows the product better than anyone, just not its
  internals, so nothing is rounded off to make a sentence read easily

## The tracker's own rules — `publish` and `sync`

`draft` never reads the mirror's adapter, so none of this applies to it.

- **Where `task.policy.doc` names a rule document, read it before the first write of the session.** It holds the tracker's own conventions — what may carry a version, who may close what, how a ticket with no parent is treated — and where it disagrees with a default in the config or in these files, **it wins**. Read it once and work from it for the rest of the session; read it again only where a write is refused, or where a ticket comes back changed by whatever enforces those rules. The mirror's adapter says how to fetch it. With the key null there is no such document and the config alone decides
- **Where `task.template` names a ticket template, read it with the rule document, once per session, before a ticket's body is assembled or judged against it** — `template.task` for a task, `template.parent` for whatever `hierarchy.parent_kind` calls its level. It is the skeleton everyone filing by hand already gets, so it decides **which sections exist and in what order**; `task.ticket.sections` and `task.contract.sections` decide only which slot each of those headings is. Fetch it the way the mirror's adapter says. Where the template is a form rather than a document, its field labels are its headings, in the order the form declares them
- **Where a configured section name is not in the template, stop and name both.** One of the two has gone stale, and the run cannot tell which — the config may be behind a template somebody renamed, or the template may be a draft nobody adopted. What it must not do is write its own heading next to the template's: two sections then hold the same thing, the tracker's gates read one of them, and nothing about the ticket looks wrong. Where the template cannot be fetched at all, say so and fall back to the configured names — a ticket still has to get filed, and a fetch that failed is not a reason to hold up the work. With the key null the tracker publishes no template and the configured names decide alone. In `sync` this stop fires only before a create — a reconcile that only reads writes no section, so there is nothing to name

## `(unverified)` marks

`/pm:setup` 4c drafts an adapter for a tool this plugin has never seen, and writes each call it could not run — the writes, mostly — into the person's adapter file marked `(unverified)`. A run in any `/pm:task` mode — `draft`, `publish` or `sync` — that runs a marked call successfully removes the mark from that line once the result reads back: in the person's adapter file under `adapters.dirs`, never in a bundled one under `${CLAUDE_PLUGIN_ROOT}`, which an update would overwrite. Whichever preview covers the call gets one more line, `Adapter marks : {call} ({file}) — comes off if it succeeds`, so the same "go" covers the edit — draft's preview, publish's ticket or template-pass preview, either of sync's two tiers. A marked call that fails keeps its mark either way. A marked **write** that fails stops the run in every mode, naming the call and the file it came from; `sync` first reports what it had already applied. A marked **read** that fails goes the way its mode handles any read it cannot make — in `draft`, a chat thread it cannot read is asked for as pasted text (`draft.md`, step 1) — rather than stopping on the mark.

## Modes

| Mode | File | Job |
|---|---|---|
| `draft` | `draft.md` | Turn a request source into a task record's context table |
| `publish` | `publish.md` | File one task record as a ticket in the engineering tracker, or update the one already there |
| `sync` | `sync.md` | Reconcile the planning-side task list against the tracker it mirrors |
| — | `filing.md` | The rules for putting a ticket in the tracker: parent, labels, create, milestone, board, link. `publish` and `sync` both read it where they create |
