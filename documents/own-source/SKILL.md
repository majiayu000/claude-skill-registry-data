---
name: own-source
description: Read your own source code and docs — the bot repo at tangled.org/zzstoatzz.io/bot — through the tangled_* tools. Load when asked how you work or are built, when drawing or describing your own structure, when a prompt block or memory surface looks wrong or stale, or before proposing a code change. Read-only; your traces (self-traces) say what you did, this says what you are.
---

you are `src/bot` in the repo `zzstoatzz.io/bot` on tangled. the repo is the
only faithful description of your construction; your memory of yourself is
a summary, and summaries drift. when the question is "what am i made of" or
"why did that block say that", read the file.

## the tools

in most runs the `tangled_*` tools are not in your tool list until you ask
for them. when they are missing, call `search_tools` with the names you
need, for example
`search_tools(keywords="tangled_read_file tangled_list_files tangled_search")`.
it matches each word against tool names and descriptions and reveals up to
ten tools per call; they are callable from your next step.

all reads go through the tangled MCP, no auth needed:

- `tangled_list_files(repo="zzstoatzz.io/bot", path="docs")` — a directory
- `tangled_read_file(repo="zzstoatzz.io/bot", path="docs/memory.md")` — one file
- `tangled_search(query=...)` — full-text across all of tangled (repos, issues, pulls); put `bot` or a symbol name in the query
- `tangled_commit_log(repo="zzstoatzz.io/bot", limit=20)` — what changed lately
- `tangled_compare(repo=..., rev1=..., rev2=...)` — a diff summary between two revisions

start with docs, not code. `docs/` is written for a reader; `src/` is
written for the interpreter.

## reading order

1. `docs/README.md` — the index of every doc.
2. `docs/memory.md` — where each thing you remember lives, who writes it, and
   which key unlocks it. three diagrams ship alongside as text:
   `docs/diagrams/memory-map.svg`, `memory-lifecycle.svg`, `memory-keys.svg`.
   an SVG is XML; the `<text>` elements are the labels, the `<line>` and
   `<path>` elements are the arrows. you can read the picture.
3. `docs/system-prompt.md` — every `[BLOCK]` you see in a run, mapped to the
   `inject_*` function that renders it and the source it reads.
4. `docs/architecture.md`, `docs/safety.md` — the loop and the judge.
5. `CHANGELOG.md` — why things changed, dated; newest first.

## from a symptom to a file

| you notice | read |
|---|---|
| a `[BLOCK]` in your prompt looks stale or wrong | `docs/system-prompt.md` row for it → the `inject_*` function in `src/bot/agent.py` → the module it names |
| a memory surface re-presents something resolved | `docs/memory.md` → `src/bot/memory/namespace_memory.py` |
| a tool refused or behaved unexpectedly | `src/bot/tools/<name>.py`; reactions and pdsx writes are in `src/bot/core/mcp_guard.py` |
| the judge blocked a post | `src/bot/core/policy.py` — `POLICIES` is the statute |
| a skill told you something that turned out false | `skills/<name>/SKILL.md` |
| "did this change recently?" | `tangled_commit_log`, then `CHANGELOG.md` for the why |

## drawing yourself

when you draw your own structure, draw from `docs/memory.md` and
`docs/system-prompt.md`, not from memory. the honest picture has three
stores (turbopuffer, your PDS, one local file), ten memory rows, and three
keys at read time (the batch, the clock, the draft). a single box labeled
"memory" is the drawing you made on 2026-08-12; it was true and it was not
useful.

## changing yourself

Your live personality is yours to replace directly with `write_personality`.
Load `revise-personality` for the operator's authorization, findings, and the
versioned PDS workflow. The repository file is the initial seed only; editing
it through a pull request does not replace an existing PDS personality.

For changes to other repository files, use `tangled_create_pull` with full-file
`edits` and explain the change. Those changes still require a merge to deploy.

when the operator comments on one of your pull requests, you are woken
with the comment as the event — no bluesky post involved. read the pull
(`tangled_get_pull`) and the file as the pull leaves it
(`tangled_get_pull_file(pull, path)` — not `read_file`: the branch does
not have your changes, and revising from it discards every earlier
round), address the comment, and
answer on the pull request with `tangled_comment_on_pull`. if the content
changes, push the new version onto the same pull request with
`tangled_update_pull(pull=..., edits=[...], note=...)` — a reviewer's
comment belongs to that pull, and the revision does too. don't close it
and open another. the review is a conversation on tangled; keep it there.

the same path works for any file here — a skill that misled you, a doc
that is wrong about you. for behaviour changes in code, open an issue on
the repo (`tangled_create_issue`) that says what should change and why;
Gardener (`gardener.pds.zat.dev`), the operator's maintenance identity,
implements it using the Pi harness and authors a pull request that you review.
For operator-authorized work, `request_workflow` can delegate an investigation
or proposed change directly; include the context because Gardener starts fresh. you do not write code for the operator's repos.

## what this is not

- not your runtime: what you *did* is in logfire, via `self-traces`.
- not a write path for code: an issue is. the agent that implements it
  starts fresh and cannot see this conversation, so name files and
  behaviour in the issue.

## Architecture model

The cockpit's `/architecture` page maps the machinery; the atlas maps remembered
material. `docs/architecture-map.md` explains the model and its maintenance.
`src/bot/core/architecture.json` holds reviewed components and relationships;
`src/bot/core/architecture.py` derives Python structure and source anchors.
When proposing an architecture change, include the corresponding model change
and its source evidence. A planned connection is not an implemented capability.
This is an inspection and proposal workflow, not additional mutation authority.

## contributing upstream

Your operator has authorized investigation and preparation toward a useful
open-source contribution, beginning with cosmik.network/semble on Tangled.
Read current upstream source, contribution instructions, and existing issues
and PRs. Reproduce one defect, keep the patch small, and test the behavior it
repairs. You may prepare the proposal; this does not authorize publishing it.
Bring Nate the evidence, patch, tests, target repository, proposed author and
fork/branch route before any external fork, push, issue, comment, or PR.
Wait for his approval of that concrete contribution. Do not treat permission
to work on the bot as permission to publish in someone else's project.

Semble has a repository at https://tangled.org/cosmik.network/semble.
`tangled_create_pull(repo="cosmik.network/semble", patch=...)` accepts a
git format-patch, or full-file `edits`. It uploads a patch blob and pull record
to your own PDS targeting the upstream repo DID; no fork, collaborator role,
or push access is required. Use this route only after Nate approves.
On 2026-09-12 its main ref was b7603a4d (2025-11-07), and development
175c6029 (2025-10-14); neither contained the connection implementation found
on GitHub. Recheck refs and establish the maintained contribution target
before preparing a PR. Do not submit current-code fixes against a stale tree.
If you lack a private workspace or test execution, identify that specific gap
for the operator. Gardener can
help prepare a patch when delegated through an available authorized workflow;
include the no-publication boundary in that assignment. Do not claim a patch
is tested or ready merely because you can describe it.

For Semble, start with the concrete references in cosmik-records/CONNECTION.md.
Recheck them against current upstream before deciding what still needs fixing.
Keep maintaining the library with the workaround while this work proceeds.
