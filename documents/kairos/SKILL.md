---
name: kairos
description: Router for the kairos plugin's user-invoked skills — which to reach for, and when.
disable-model-invocation: true
---

The kairos plugin's user-invoked surface. Reach for:

- `/kairos:bootstrap` — first, in any repo not yet wired to a Kairos deployment (and after remote/team/board changes): configure the MCP endpoint, confirm auth (OAuth, or the agent key of the user on a deployment with no issuer), detect this repository from the git remote, discover boards, write `.claude/kairos.local.md`.
- `/kairos:grill-me` — before building: a relentless interview that stress-tests a plan or design until shared understanding is reached.
- `/kairos:grill-with-docs` — before building, when the design should leave a paper trail: the same relentless interview as grill-me, additionally capturing glossary terms (CONTEXT.md) and Kairos ADRs as decisions crystallise.
- `/kairos:grill-initiative` — before building, on a Kairos initiative or strategy: `/kairos:grill-initiative <short code | "title">`. The same one-question-at-a-time interview, but each settled answer goes into the item at once, under `## Decisions (<who>, <date>)`. A title creates the initiative first. The column sets the depth (context and goals in the entry column, the design later, no grilling in a done column), and the skill never moves the item. It ends with an offer of `/kairos:decompose`, then `/kairos:grill-decomposition`.
- `/kairos:to-initiative` — when a discussed plan is ready to become work: synthesize the conversation into a Kairos initiative with an attached PRD (no interview — grill first if it needs one).
- `/kairos:decompose` — when an initiative or plan needs breaking into tasks: tracer-bullet vertical slices, each created on a named board with a link to its repository (a slice for a different team is a request to that team), quizzed with the user, blocking edges wired, published in dependency order, then an offer of `/kairos:grill-decomposition`.
- `/kairos:grill-decomposition` — after decompose (or triage, or tasks from a person), before a Ralph loop: `/kairos:grill-decomposition <initiative short code>` reviews the open tasks as a set — slice boundaries, order and risk, correct `blocks` edges, criteria that the loop can check with a command (a manual check moves to the initiative), scope and repository leaks. Each settled answer goes into the task at once. A design question stops the review and points to grill-initiative. It never moves an item, and ends with an offer of `/kairos:ralph-initiative`.
- `/kairos:ralph` — when groomed tasks are ready to run without a stop between them: `/kairos:ralph <code>... [--max-iterations N]` runs them in the given sequence, each through the steps of `implement`. A `Stop` hook keeps the session going until each task is Completed, the loop stops with a written reason (a Blocked task, no checkable criteria, a design decision, a push, a deploy, another repository), or the iteration limit.
- `/kairos:ralph-initiative` — the same loop over the open tasks of an initiative, in the sequence of their `blocks` edges; a task whose blocker is not done is skipped.
- `/kairos:cancel-ralph` — stops the Ralph loop of this session; the next stop is not blocked.
- `/kairos:triage` — grooming the delivery board, this repository's slice by default: refine acceptance criteria (linking each item to its repository), prioritize bugs, weigh tech debt against its ~20% allocation, archive stale items, restock Todo, escalate cross-team blockers.
- `/kairos:architecture-review` — reviewing a codebase's structure: scan, classify by altitude, an HTML report of deepening candidates, then a grilling loop on the one you pick.
- `/kairos:diataxis-review` — reviewing a documentation tree: classify every page against the Diataxis spec, run the structural pass, optionally file findings as tech debt.
- `/kairos:writing-great-skills` — when writing or editing a skill: the normative authoring reference (invocation split, information hierarchy, leading words, pruning).
- `/kairos:handoff` — at the end of a session: bring the active Kairos items current, then compact the leftover conversation context into a note for the next session.
- `/kairos:kairos` — this router.

Model-invoked disciplines (the agent reaches these on its own; naming them works too): `grilling` (the interview loop behind grill-me), `kairos-vocabulary` (name work only by its short code and the Kairos words: quoted titles for work not yet created, no "Slice 2" or "D3", the column as the state, and a table from outside words such as "epic" to the Kairos item types), `implement` (pick up a Kairos task, work it with the task as working memory, complete through the verification gate), `code-review` (two-axis: repo standards + spec fidelity to the originating item), `tdd` (red → green test-first; slice progress lands on the task), `diagnosing-bugs` (reproduce → minimise → hypothesise → instrument → fix → regression-test), `prototype` (throwaway build to answer a design question), `research` (background investigation saved as a Kairos document), `domain-modeling` (glossary + ADR upkeep), `codebase-design` (deep-module design vocabulary and discipline).

**Sync rule**: this router maps the plugin's entire user-invoked surface. Adding, renaming, removing, or changing the behavior of a user-invoked skill without updating this router is a defect — a router that lies is a bug.

## Boards and repositories: the team decides the board

The team decides the board of a task, and the board decides its team (COLLIERY-A-0023). Name a board when you create a task. The repository of a task is an optional link: it says where the code is and changes nothing else. `set_repository` sets or clears the link. Every repository has exactly one owning team; that team is responsible for review, release and the standards of the repository. The directory of repositories is a different thing from the link: `add_repository` adds a repository to the directory, and `update_repository` changes its description, its default branch and its URL. The two are for a member of the owner team or an organization admin.

Your queue is the board of your team, filtered by the repository of the checkout. Call `board_items` with `board=<team_board>` and `repository=<slug>` (SessionStart context, from `/kairos:bootstrap`). `board_items` gives 200 items at most in one result. When the result is a part of the board, its first lines say so and give the `offset` of the next part. Call `board_items` again with that `offset` until you have each part. Then make the decision. The work of other teams in this repository is not in your queue. Find it with `search` (`filter.repository`). `get_repository <slug>` gives the owner of a repository, the "how to work here" description and the in-flight PRs.

## Documents: the board is the owner, the repository is what the document is about

Each document has an owner board, and `create_item` for a document needs `board`: a call with no `board` is refused, and `parent` does not give one. The owner board gives the right to edit the document (`manage_documents` on that board, which each member of the team of a delivery board has), and the code of the document gets the prefix of that board. The document is not a card of the board.

- **A document of a repository or a product as a whole** (its vision, its architecture overview): `create_item {item_type: document, board: <team_board>, template: "Product Vision", title: ...}`.
- **A document of one work item** (a PRD of an initiative, the findings of a research task): `create_item {item_type: document, board: <team_board>, parent: <short code>, ...}`. `parent` writes the `supports` edge. Use the board of your team, or the board of the item.

Then say what the document is about: `link_items {source: <document>, target: <repository slug>, relationship: impacts}`. The link goes from a document or an ADR to a repository. It gives no right, and you need no right on the repository. A task does not impact a repository: `set_repository` links a task.

In a checkout, read the documents that impact the repository before you plan work. `get_repository <slug>` lists them, and `get_item` gives each one. `search` with `filter.repository` finds them with the tasks of the repository.

## Initiatives and strategies: their teams

An initiative gets its teams from its tasks: the team of the board of each task below it. A strategy gets the teams of its initiatives. `get_item` shows them (`- teams:`), and `board_items` tags each card (`[teams: a, b]`) and filters with `team` or `no_team: true`. When you plan an initiative before it has tasks, and you know the team, call `set_team {short_code, team}`. `clear_team` removes a team set by hand; a team from tasks stays. A team gives no right on the item.

`move_item` gives a document to a different owner board. You need `manage_documents` on the board that owns the document now and on the new board.

**A request to a different team** — the recipe lives with the `implement` skill (model-invoked, so agents can reach it without this router): [workflow/implement/CROSS-TEAM-FILING.md](../../workflow/implement/CROSS-TEAM-FILING.md). In one line: `create_item {board: the delivery board of that team, parent: your initiative}` → `link_items blocks` back to your item → report the short code. The request goes to the entry column of that board, in the support lane.
