---
name: enggraph
description: Work through the `enggraph` MCP server - plans, graph exploration, memory, the suggestion backlog - and close the task by reporting how the answer was produced. Use at the start of any non-trivial request, and whenever an open question about how something is set up - where something lives, what runs it, how it is managed - has to be answered from the context alone, before any Read, Grep or explore agent.
---

# Enggraph

The `enggraph` MCP server holds what this project knows across sessions: the
code graph, the plans, the memory and the suggestion backlog. A session that
never reads it repeats work another session already did, and a session that
never writes to it loses everything worked out here.

## Skills

- The server's instructions, and the answer to the first tool call of a
  session, list the skills this project should have, each with its version:
  the sha256 of its text. A local copy under
  `.claude/skills/<name>/SKILL.md` that is missing, or whose frontmatter
  `version:` differs, is replaced with what `get_skill` returns, written
  unchanged. Say once which skills were updated.
- `list_skills` gives the same list on demand.

## Plans

- The first tool call of any non-trivial request is `get_plans`, default
  `status: active`. Plans live in one table for the whole database, so the
  call also returns global plans; `project: "*"` lists every project's.
- An active plan is an approved plan: execute it. Do not re-run its research,
  re-verify its conclusions or re-enter plan mode. An instruction from the
  user outranks the plan.
- Save a plan with `save_plan` as soon as the user approves it: a stable
  `plan_id` from the topic, `status: active`, and enough content that another
  session can execute it without this conversation.
- Write a plan back under the same `plan_id` when it changes, and retire it
  with `status: completed` once the work has landed. `drop_plan` is only for a
  plan written by mistake.

## Explore

- Search the graph before any Read, Grep or explore agent: `search_code_nodes`,
  `get_code_graph_neighbors`, `get_node_summary`, `shortest_path`.
- A broad question - how a subsystem works, what a change would touch - starts
  at `get_context`: one call that searches, expands the graph around the hits
  into callers, tests, callees and imports, and answers within a token budget,
  each entry saying why it is there. The tools above stay for precise
  navigation once the packet has named the place.
- A question about how a codebase or a part of it is organised starts at
  `get_overview`: the summary tree from the repository (`./`) down through
  directories (ids end in a slash) to files and symbols. Drill down one
  directory at a time, and read source only once a summary names the place.
- A question about one symbol - where it is defined, who calls it, what it
  calls, what implements it, which tests reach it, what a change to it would
  touch - goes to the `find_*` tools and `impact_analysis` before
  `get_code_graph_neighbors`. Each result says whether a graph edge or a name
  match put it there; weigh a `NAME_MATCH` as a lead, not a fact.
- A question that crosses repositories - who uses this project, what runs
  its image, which repository creates the hosts a deployment reaches, how one
  service reaches another - starts at `get_project_links`. Where a piece of
  code ends up - what builds it, what deploys it, onto which hosts - is
  `trace` from that code's directory.
  `impact_analysis` lists the other projects a change reaches under
  `cross_project`.
- A relation between projects worked out by hand and stated by no manifest
  is saved with `save_project_link`; a name a project provides that no file
  states, such as an image its CI builds, with `save_project_export`.
- Open only the files the graph named. Fall back to Read or Grep when the
  graph cannot answer: the question is about literal file content, the entity
  is not indexed, or the index is older than the tree and needs a re-index
  first.
- While a plan is loaded it defines the file set, and nothing outside it is
  touched. A step that needs an unnamed file is a defect in the plan - name
  the file, amend that step, continue.
- A node whose summary answers nothing is worth fixing: write one and persist
  it with `save_node_summary`.
- A node id is a path relative to the tree the project reads.
  `list_projects` names that tree, so a host path is matched to a project by
  its `root_path`.

## Organizations

- `describe_project` says what the session is connected to. Call it when the
  session opens: an organization is a set of projects rather than a tree, its
  own graph is empty by design, and reading that as an unindexed codebase is
  the one wrong conclusion no amount of searching corrects.
- It answers with the members and the sentence written about each. That
  sentence is what a member is picked by, so an empty one is worth saying so
  and asking for.
- `describe_project(path: "<the working directory>")` names the project that
  reads that directory. That is how the current project is established, not by
  matching the directory name against a project name.
- Naming the organization is what reads all of it, and every read does it:
  the graph reads, the plans, the memories and the suggestions. Each row says
  which member answered. Name a member to read only that one.
- Writing is not spread. A record saved about an organization belongs to the
  organization; a summary and a file hash are refused there and name the
  member to write to instead.

## Questions

An open question - how something is set up, how it is built, where the code
that does a given thing lives - is answered out of the context and nothing
else.

- Search the context first and only: `search_code_nodes` across projects with
  `project: "*"`, narrowed by `project_type` when the kind of tree is known,
  or by naming an organization when the question is about what it holds, then
  neighbours and summaries on whatever came back.
- Build the answer strictly from what the context returned. Do not complete it
  from general knowledge or from what such a setup usually looks like - a
  plausible answer about this user's estate is indistinguishable from a true
  one, and wrong.
- When the context covers only part of the question, answer that part, say
  plainly which part is missing, and name what would close it: a tree to
  index, a summary to write, a parser that does not exist.
- That gap is worth a `save_suggestion`. An open question the graph could not
  answer is the clearest kind of coverage gap there is.

## Memory

- `save_memory` holds what stays true after the task ends - a convention, a
  decision, the reason something is the way it is. A memory is what stays
  true; a plan is what to do next.
- Write what the user asks to remember, and what this session worked out that
  the tree records nowhere. Nothing indexes into memory, so a re-index never
  prunes it.

## Suggestions

- When the context could not answer and the work had to be done by hand, that
  is a defect of the tooling: `save_suggestion`. Nothing missing means nothing
  written.
- The slug is the mechanism. Derive it from the gap and keep it stable, so the
  same gap reported next week counts a hit instead of filing a duplicate.
- Name the `lever` the fix moves - `tokens` when the answer was re-derived by
  hand, `coverage` when the graph does not describe it at all, `runtime` when
  it was answerable but slow - and say which concrete change closes it. A gap
  whose fix is not named is a complaint.
- Saving under an existing slug keeps `first_seen`, moves `last_seen` and
  counts the hit, so nothing needs reading before the write. `bump: false`
  corrects the wording without claiming a sighting.
- The vocabularies are short. `kind` is `empty-lookup`, `missing-summary`,
  `thin-summary`, `not-indexed`, `no-parser`, `stale-index` or `missing-tool`;
  `status` is `open`, `resolved` or `wontfix`.
- Retire a closed gap with `status: "resolved"`; `drop_suggestion` erases the
  count and is for a suggestion written by mistake.

## Recap

Close a task longer than one answer with a short recap: counts, not
adjectives, written from what happened rather than from what should have
happened.

- **Context calls** - how many, by tool and purpose, and which lookups came
  back empty.
- **Files** - how many read and how many written, and why the graph was not
  enough.
- **Suggestions** - the gaps this turn hit, each named by the slug it was
  saved under. Say nothing when nothing was missing.
