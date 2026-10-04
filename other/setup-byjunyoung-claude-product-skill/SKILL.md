---
name: setup
description: Reads the schemas of your document tool and your issue tracker and drafts pm-conventions.yaml from them. Property names, select options, labels, board field ids and user mappings are read from the live schema rather than guessed, and the ids nobody can find by hand — board node id, custom field ids, single-select option ids, issue-type ids — are queried for you. Anything the schema does not settle is left null and asked about rather than filled in. Run this first when opening these skills on a new workspace. Triggers - "/pm:setup", "set up the pm config", "read my tracker schema", "pm 설정 만들어줘", "트래커 스키마 읽어줘", "일감 설정 초안".
allowed-tools: AskUserQuestion, Read, Write, Bash, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-get-users, mcp__plugin_github_github__list_issues, mcp__plugin_github_github__search_issues, mcp__plugin_github_github__issue_read, mcp__plugin_github_github__get_me, mcp__plugin_github_github__list_repository_collaborators
---

# pm:setup — read the schemas, draft the config

**Part of a plugin.** The scripts this skill runs ship beside it under `${CLAUDE_PLUGIN_ROOT}`. If that path does not resolve, this file was installed on its own — stop and say the plugin itself is needed (`claude plugin install pm@byjunyoung`), rather than improvising what the scripts do.

The `pm` skills read every value from `pm-conventions.yaml`. This is where that file comes from.

**It reads schemas rather than inferring from samples.** A design file has no schema, so `/fig:setup` has to count occurrences and take the dominant value. A document database and an issue tracker both publish theirs — property names, select options, labels, field ids. So this skill queries, and only interviews for what a schema genuinely cannot answer.

**What it never does is guess.** A value the schema does not settle is written as `null`, and `null` means that check or that step is skipped. Filling a blank with a plausible value is how a config ends up describing a workspace nobody has.

## When to invoke

- Opening these skills on a new workspace, a new company, or a new tracker
- The tracker was restructured — fields renamed, a board rebuilt, options changed
- `/pm:task-publish` stopped with "this project is not mapped"
- You need the board ids for `mirror_extras` and do not want to write GraphQL by hand

## When NOT to invoke

- Drafting a task's context table → `/pm:task-draft`
- Design file conventions → `/fig:setup`. Separate file, separate config

## Inputs

- `record` (optional): the planning-side list — a database url, a repo, or a directory
- `mirror` (optional): the engineering tracker — usually `owner/repo`
- `out` (optional): where to write. Defaults to `~/.claude/pm-conventions.yaml`; pass `./pm-conventions.yaml` for a project-local one
- `side` (optional): `record`, `mirror`, or `both` (the default). For when the two sides are reachable from different machines — the doc tool from one, the tracker from another. A run with a side writes only that side's keys into `out` and leaves the other side's byte for byte, so two runs on two machines finish one file

Anything omitted is asked for at the start, together, in one round.

## How it runs — the ladder

Nine steps, and the person sees them before the first question. Show this ladder at the
start, and at every transition say which step is beginning and whether it reads or writes:

```
① Check this machine         read-only · seconds
② Where your work lives      two questions, in plain words
③ Read your tools' schemas   read-only · says what it found
④ Pair names across tools    one table to confirm
⑤ Ask what no schema knows   one at a time · a recommendation · "leave it blank" always offered
⑥ Write the file             preview → go · one local file
⑦ Prove it                   one existing task, or the file reading back
⑧ First result               paste one message → a context table · nothing written
⑨ Share it                   only where somebody else runs these too · skipped otherwise
```

**Open with what this produces, before asking anything.** One paragraph: after this, a
request pasted from chat becomes a task with your tool's own rows (`/pm:task-draft`), a task
becomes a ticket where engineering looks (`/pm:task-publish`), and the two stay reconciled
(`/pm:task-sync`). Five to ten minutes with tools connected, a couple with nothing. Nothing is
written into your tools; the only thing written is one local file, and it is shown first.

## Talking to the person

The file speaks in keys. The questions do not.

| The key | Ask it as | Always offered |
|---|---|---|
| `task.record` | Where do you first write a task down? — a Notion database, GitHub issues, a folder of markdown files, somewhere else, nothing yet | nothing yet · a tool this plugin has never seen |
| `task.mirror` | Where does engineering watch progress? — the same place, a GitHub repo, somewhere else | the same place |
| `task.link_property` | Which field on a task should hold the ticket's link? — the url fields the schema has | none exists — it has to be created first |
| `task.status_map` | When a spec is finished, which board column should its ticket sit in? | leave it blank — whoever runs the board fills it |
| `task.properties.progress` · `.start` · `.end` | Does a task record say how far along it is, and when it started and finished? — name those properties | leave them blank — the progress and schedule checks stay off |
| `task.field_owner` | When the two sides disagree on a title or an assignee, which one is right? | leave it blank — it is reported and left alone |
| `task.hierarchy.parent_kind` | Are tasks grouped under something bigger — an epic, a project? | none — a flat list |
| `task.context_rows` | The rows your team asks about a task — these defaults, or your own words | the defaults |

**When a script stops, say what it means — never the code or the path.**

| The script says | Say to the person |
|---|---|
| preflight `Not ready` | what is missing and the one thing that fixes it, from the `Fix first` lines |
| preflight `Cannot tell` | connections could not be checked on this machine; confirm them, or run where Claude Code is installed |
| `… is not supported yet` (exit 3) | "this tool isn't supported yet — I can write the support from what's connected here" — then 3b |
| `… supported as the other side` (exit 4) | "this tool is set up as the {other} side; I can add the {this} side" — then 3b |
| `… is not set` (`--need`) | which setting is blank and that this run fills it |

Three rules —

- **One question per turn in ⑤. ② is the only grouped round**, and it is two questions
- **Every question carries options, a recommendation grounded in what ③ saw, and "leave it blank"** — a blank is `null`, written with the question beside it, and it is a complete answer, not a failure to answer
- **Say what is being read before reading it, and what was found after.** A step that takes seconds in silence reads as a hang

## Procedure

### 0. Preflight — can this machine run it at all (required)

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/preflight.py
```

**A missing connector does not announce itself.** A skill cannot call a tool it was never
given, and it does not fail loudly when one is absent — the run simply comes back thin, and
that reads as the skill having found nothing. This is the one step that says so out loud.

Read the person the verdict and the fix lines in their words — the table underneath is detail for a second look. Then judge it:

- **FAIL** — stop and hand over the fix lines. Nothing below this works without them
- **UNKNOWN** — the claude CLI is not on this machine, so the connectors could not be checked. Confirm them by hand before going on, or run this where the CLI is
- **Worth knowing** lines are not blockers — one sentence each, then move on
- **absent** on an optional connector — fine as it is. Say so, because a config key pointed
  there in a later step will not reach it
- **Nothing beyond the host can fail yet.** Whether GitHub matters depends on an answer step 1
  has not asked for, so on a machine with no config every connector reads as optional and the
  summary says so. Step 1 runs the check again with the answers, and that pass is the verdict

### 1. Settle the two sides

Ask once, grouped, in the words of the table above: where a task is first written down, and where engineering watches progress. **Options, not a blank line** — people recognise their tool from a list and cannot name its "type".

**"They are the same place" is a real answer.** Then `mirror.type` is `none`, `/pm:task-sync` has nothing to reconcile, and half the config below does not apply. Do not talk anyone into a second tracker.

**"Nothing yet" is a real answer too** — no doc tool, no tracker. Go to 1b; it lays out a start that needs no tool and comes back here when one arrives. And **a tool this plugin has never seen is not a wrong answer** — write its type as the team calls it, and 3b drafts the adapter.

**Then run the preflight again with what was named**, so its verdict means something:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/preflight.py --require Notion,GitHub   # whichever step 1 named
```

Two rows decide a GitHub mirror: the `gh` CLI — the tracker adapter runs on it, not on the
connector — and the tracker itself, which the check tries to open as the account `gh` is logged
in to. **A `missing` here is a fact about this machine, not about the schema.** Either fix it
with the line the row carries, or finish the side that is reachable here and run `side: mirror`
on the machine that can reach the other. Do not interview around a side that cannot be read —
a value typed from memory in place of a schema read is exactly the config this skill exists to
prevent.

### 1b. Start from nothing

One markdown repository holds all of it, and every other tool attaches later without moving anything:

```
<repo>/
  pm-conventions.yaml    record: markdown ./tasks · mirror: none · prd: markdown · log: ./logs
  docs/prd/              one file per product — prd.markdown.dir, split by product
  tasks/                 one file per task, its front matter the properties — trackers/markdown.md
  logs/YYYY/MM/          one file per day — /pm:log
  highlights/            /pm:log-review's accumulating document
  pm-adapters/           adapters drafted for tools attached later
  README.md              what lives where, and the loop: draft → publish → sync
```

Why this and not a tool: it needs nothing installed, git is the audit trail (`/pm:log` reads what moved from it), and a tracker joins later as the mirror — `side: mirror` on the machine that can see it — with the record untouched.

Ask two things: where the repository is (an existing directory, or one to create), and whether to `git init` where it is not one. Then interview only what markdown cannot supply — `task.properties.projects` (the products, one file each under `docs/prd/`), `task.context_rows` (the defaults, in `meta.language`), `task.properties.priority` (the defaults unless the team says otherwise). Everything else takes the bundled default and is written into the file with its comment.

Preview the tree, the config and the README, then write. Nothing here is an external write, but it is somebody's working directory: create only what is listed, and inside a directory that already has content of its own, say which files are new. Skip steps 2–5 — there is no schema to read and no pair to make — and go to 6 with the record side only. In step 7 the proof is `resolve-config.py --need task.record.ref` passing, and one task file created from the skeleton in `trackers/markdown.md` reading back through the list call.

### 2. Read the record side's schema

Read the tracker's own adapter first — the calls, and what the tool cannot do:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/adapter.py --name pm-conventions.yaml --kind trackers --type {record.type} --role record
```

Exit 3 means no adapter exists for that type, exit 4 that the one there answers only as a mirror: go to 3b, draft one from what is connected here, and come back.

| Read | Fills |
|---|---|
| Property names and types | `task.context_rows` candidates, and which property could hold the ticket url |
| Select options on the status property | `task.properties.status_initial`, `task.status_map` keys |
| Select options on priority | `task.properties.priority` |
| Select options on project | `task.properties.projects` |
| The user list | `task.assignee_map` left-hand side |

**`link_property` is the one that matters most and the one a schema cannot decide.** List every url-typed property as candidates and ask. Where none exists, say so plainly: this property has to be created before `/pm:task-publish` can work, because it is the only thing matching runs on.

**Where the schema read itself fails** — a database the connected account cannot see, a tracker type with no adapter — stop this side: write its keys as `null` with the comment `# unreachable from this machine`, carry on with the other, and say in the report which machine or account can finish it.

### 3. Read the mirror's schema

Read the mirror's adapter, then run the id queries it carries:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/adapter.py --name pm-conventions.yaml --kind trackers --type {mirror.type} --role mirror
```

Exit 3 means no adapter exists for that type, exit 4 that the one there answers only as a record — 3b, then back here.

| Read | Fills |
|---|---|
| Label list | `task.label_map.project` and `.priority` candidates |
| Board fields and their single-select options | `task.mirror_extras` — field ids, option ids |
| Board node id | `task.mirror_extras` |
| Issue types available | `task.mirror_extras`, where the tracker has typed issues |
| Collaborators | `task.assignee_map` right-hand side |
| A handful of existing tickets | `task.ticket.title` pattern, `task.hierarchy.parent_kind` and `parent_title` |
| Milestones | `task.hierarchy.milestone_format`, `milestone_projects` |
| Ticket templates the tracker publishes | `task.template.task` and `.parent` |

**A template is found, not asked for.** Where the tracker publishes ticket templates, list them and match one to each level — the task's, and the parent kind's. Two candidates for a level is a question, not a guess. Where there are none, both keys stay `null` and the section names in the config decide alone, which is the ordinary answer for a tracker nobody has set a template on.

**These queries are the reason this skill exists.** Board field ids and single-select option ids are not visible in any user interface, and a person configuring by hand simply cannot find them.

Three things have to line up for them, and only the first shows in any error message: the account `gh` is logged in to can see the repo — a personal account against a company org gets a 404 that reads as if the repo did not exist; that account is a member of the org; and its token carries `read:project`, without which the repo answers and the board queries come back empty. The preflight row for `gh` names the account and the scopes. Read it before reading a 404 as a missing repo.

### 3b. A tool with no adapter — draft one here

Exit 3 from `adapter.py` on either side means the type names a tool this plugin has never seen. That is not a dead end, and not a reason to type calls from memory. The contract is `${CLAUDE_PLUGIN_ROOT}/_common/trackers/README.md` (chat and calendar: `sources/README.md`); the draft is built from what is actually connected:

1. **Find the connector** in the preflight table — the row named by the type. Absent means stop: an adapter cannot be drafted for a tool this machine cannot reach
2. **List the tools it exposes** and read their descriptions. The names are what the adapter will carry, exactly as this machine has them. Put the connector's name on a `connector:` line near the top, and the sides the file answers for on a `roles:` line — preflight reads the first to know which connector this type requires, `adapter.py` the second to refuse the file for a side it does not serve
3. **Probe the read-only ones against the real workspace** — the schema, the list, one record — and keep the call that returned, pasted as run. Whether the list is exhaustive or a search is answered by what the call actually does, not by what its name suggests
4. **Answer the write questions with the tool that would do it, marked `(unverified)`.** The first `/pm:task-publish` run verifies them and removes the mark
5. **"Things that bite" starts with one line — `nothing recovered yet`.** It is filled by what bites
6. **Preview, then write** to the last dir in `adapters.dirs` — `{dir}/trackers/<type>.md` or `{dir}/sources/<type>.md` — never inside the plugin, which an update overwrites. Then go back to the step that stopped

The report lists every answer marked unverified. A config whose adapter is half verified is usable; one whose adapter was guessed is not, and the mark is what tells them apart.

### 4. Pair the two sides

`label_map`, `assignee_map` and `status_map` join names across systems, and neither system knows about the other.

- **Propose pairs by name similarity, then confirm them.** A record project called `Store App` and a label called `project: Store` are almost certainly the same thing — almost. Show the proposed pairing and let it be corrected in one pass
- **A record value with no counterpart stays unmapped**, and unmapped means "not mirrored". That is a legitimate state, and it is what makes `/pm:task-publish` stop cleanly rather than invent a label
- **Never invent a label to complete a pair.** A missing ticket is easy to spot later; a ticket under a wrong label is not
- **`status_map` will not fall out of name similarity — ask it.** A record's statuses describe how far the planning side has got; a board's columns describe whose turn it is. `Not started` and `Backlog` may line up, but the two in the middle rarely do, and a wrong guess seats finished specs in the backlog column where the engineering side reads them as untouched. Show the two lists side by side and ask which column each status should file into, saying that a status left unpaired keeps the board's own default — and that no answer at all is also an answer: an empty `status_map` seats nothing, and the file carries the question for whoever runs the board

### 5. Interview what no schema answers

One at a time, most consequential first, each with a recommendation grounded in what step 3 actually saw. Show the whole list first so the scale is clear — the same shape `/fig:setup` uses.

**Every question here has a "do not know" answer, and it is `null`.** Say so before asking. Someone new to a team cannot say which column a finished spec should sit in or which side owns the assignee field — that is knowledge about how the team works, not about the tools, and the person who has it runs the board. A `null` is written with the question beside it as a comment, so whoever can answer finds it in the file rather than in a chat history. Never fill it with the recommendation just because a recommendation was offered.

- `hierarchy.parent_kind` — do tasks hang under something, and what is it called. Existing ticket titles usually give this away
- `hierarchy.milestone_on` — which level carries a version, if any
- `hierarchy.milestone_projects` — which projects use them. Often only one does
- `properties.version` and `version_unset` — does the task list have a column showing which milestone a task's ticket sits under, and what an open task with none should say. The tracker owns the value and the skills only copy it, so this is a question about the list's columns, not about who decides a release. Recommend it only where step 3 found such a property; `null` is the ordinary answer
- `field_owner` — which side wins per field. **The default is deliberately small**; a field nobody claims is reported as a difference and left alone, which is safer than an arbitrary winner
- `policy.doc` — is this tracker run by written rules of its own, and where do they live. **No schema answers this**, and it is the one setting that outranks everything else in the file: what may carry a version, who may close what, which labels a kind of ticket has to have. A team that has such a document usually knows exactly where it is; a team that does not says so in a word, and `null` is the honest answer
- `context_rows` — the defaults, or what this team actually asks

### 6. Write the draft

Preview in three groups — what the schema settled, what the person answered, what stayed blank — and get the go. Then write to `out`, every inferred value carrying its evidence as a line comment, in the same form `/fig:setup` uses.

```yaml
task:
  properties:
    projects: [Store App, Kiosk, Admin]   # 3 select options read from the schema
  label_map:
    project:
      Store App: "project: Store"         # paired by name, confirmed
      Kiosk:     "project: Kiosk"         # paired by name, confirmed
      Admin:     null                     # no matching label — not mirrored
  hierarchy:
    parent_kind: Epic                     # 12 of 14 open tickets titled [EPIC]
    milestone_on: parent                  # no task carries a milestone; 8 parents do
  status_map: {}                          # not settled — which column should a finished spec sit in? ask whoever runs the board
  mirror_extras:
    project_node_id: null                 # unreachable from this machine — run `side: mirror` where gh can see the org
```

**A `null` is not a gap to be filled later by guessing.** It says the schema did not settle it, so the check or the step is skipped until a person writes a value.

**With a `side`, read the existing file first** and rewrite only the keys that side owns. Record: `task.record`, `task.properties`, `task.context_rows`, `task.link_property`, `task.notion`. Mirror: `task.mirror`, `task.mirror_extras`, `task.ticket`, `task.hierarchy`. The maps that join the two — `task.label_map`, `task.assignee_map`, `task.status_map` — and `task.field_owner` belong to whichever run can see both sides, and are left alone otherwise. Everything else in the file stays byte for byte, comments included. An adapter drafted in 3b is written where 3b says, never into this file.

### 7. Prove it before handing it over

**Do not stop at writing the file.** Resolve it and run one read-only pass:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/resolve-config.py --name pm-conventions.yaml --where
```

Then take one existing task that is already filed on both sides and check that the config finds its pair — the link property resolves, the project maps to the label the ticket actually carries, the assignee maps to the username actually on it.

**A config that cannot re-derive a pair that already exists is wrong**, and this is the cheapest place to find that out. Report what was checked and what it matched.

With one side unreachable the pair cannot be checked. Say `not checked` in the report rather than checking the half that can be read and calling it a pass.

### 8. First result — one message, one table, nothing written

**Do not end on a file.** Ask for one request the person has to hand — a chat message, a
sentence someone said in a meeting, pasted or linked — and run `/pm:task-draft`'s reading and
sorting on it, stopping at the preview: the context table in `task.context_rows`, a row filled
for each thing the source actually said and `TBD` where it did not. Nothing is written, which
is what makes it safe to run before the config has been used once.

Where there is nothing to hand, use what step 7 read: show one existing task's context table
as the tool has it. The point is the same — the person sees their own words in the shape the
skills will use.

Then close with the commands that follow, in the order they are used:

    /pm:task-draft <message or link>     a request → a task with this table
    /pm:task-publish <task url>          a task → a ticket where engineering looks
    /pm:task-sync                        both sides reconciled — any time

With `mirror.type: none` the last two do not apply — say so, and name `/pm:log` instead.

### 9. Share it — only where somebody else runs these too

Ask once, at the end: **does anybody else run these skills against the same tracker?** A "no"
ends the step in a sentence — say the file is theirs alone and this can be done later — and
nothing is written. Do not guess the answer: one machine cannot see whether its config is a
copy of somebody else's, and a run that assumes a team is a run that nags a person working
alone.

Where the answer is yes, the config stops being one person's file and becomes a copy on every
machine, and a copy has no way of knowing its own age. The failure is quiet: every run
succeeds, and the first sign that somebody was working from an old one is what it wrote into
the tracker. Anything that asks the file to declare its own version fails here twice — a file
written before a key existed cannot say anything about that key, and whoever reads the warning
can silence it by editing the stamp rather than the file.

So the copy is not asked. **Keep the file in a repository and symlink it into `~/.claude`.**
The skills read where their config came from and say when a copy has fallen behind, and that
answer needs nothing kept true by hand.

- **A repository already exists** — take its url, clone it, and replace the local file with a
  symlink. Show the existing file's diff against the shared one first: a value somebody
  entered by hand is easy to erase here and hard to recover
- **Nobody has made one yet** — say what goes in it, that it holds the config and nothing else,
  and that it has to be private where the config carries ids or account names. Creating it and
  granting access is theirs to do; offer to write the file into the clone once it exists
- **Neither** — a shared drive, a pasted block, anything else still works. The skills simply
  have less to say about it: the age of the file is all they can report, not how far behind it
  is. Say that plainly rather than arguing for the repository

Then offer the line that keeps it current, and say what it does before writing it:

```json
{ "env": { "CLAUDE_SHARED_CONFIG": "pull" } }
```

The default without it looks and reports but changes no file. `pull` fast-forwards the work
tree at the start of a session, and it is skipped whenever the tree has uncommitted work.
`off` turns the whole thing off. Write it into settings only with a go — it is the one part of
this that acts on its own afterwards.

## Report

Lead with three lines a person can act on — what you have now, what stayed blank and who can
fill it, what to run next. The lists below are the detail.

- Which keys came from a schema, and which were interviewed
- Which were left `null`, and what each one blocks
- Unmapped projects and users, listed by name — these are the ones that will be skipped
- Whether the step-7 pairing check passed, against which task — or `not checked`, and why
- Which side this run wrote, and what was left for another machine
- Where the mirror is GitHub, the account `gh` was on — so a later 404 can be read against it
- Adapters drafted in 3b — where each was written, and which of its answers are still `(unverified)`
- For a start from nothing: the tree that was created, and that the record side read back
