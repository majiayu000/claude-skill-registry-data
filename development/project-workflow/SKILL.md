---
name: project-workflow
description: Run a multi-ticket effort (a site rebuild, a new site, a launch) through docs/workflows — start a project from a template, file a block of the map as GitHub tickets with blocked-by links once nothing it needs is undecided, place unsorted tickets, sync, and answer "where are we" or "what can I take". Use when asked to start, plan, ticket, organise or report on a project tracked on the portal's Workflows page, or to build a new website or redesign or rebuild an existing one.
---

# Running a project through a workflow

The shape, the status rules and the file format are in
[`docs/workflows/README.md`](../../../docs/workflows/README.md). Read it first. This file is the order
to do things in and the traps.

## 0. Answering "where are we" and "what can I take"

Run `pnpm workflow:next <id>`. It reads GitHub live and prints *Waiting on you*, *Ready* (most
unblocking first), *In flight* and *Blocked*. Don't answer from memory, git log or an old snapshot.
Report it in three lines: what waits on the user, the top of the ready list, and the blocked count.
For the picture, run `pnpm workflow:sync <id>` and point the user at `/workflows/<id>` in the portal.

Never tune anything to how many agents are running. The ready list is the same for one agent or a
hundred. A *Can file now* section means blocks sit unfiled while agents could take them: file them
before answering (step 2).

## 1. Starting a project

1. Pick the template: `new-website` for a site started from nothing, `website-rebuild` when an
   old site's content and URLs come along, `custom` for anything else — a developer tool, a
   package, an internal feature — and then draft its map under
   [Drafting a map](#15-drafting-a-map-for-a-custom-project). Then ask for what the code can't tell you: the
   audience, the page readers land on first, which features are wanted, and the ticket size —
   `block` when a person reviews every PR, `supervised` when AI builds it under a review pipeline, `fast` for an internal tool or experiment nobody will review. Ask about every feature the same way, search no differently from
   storybook; each one's `summary` and `lessons` in the template is the question, in plain words.
2. Write `data/workflows/projects/<id>.yaml` by copying [`huella-legal.yaml`](../../../data/workflows/projects/huella-legal.yaml).
   Set `switches` only where the answer differs from the template's default; a rebuild without
   search, which that template turns on, is `search: false`. A blog is a page, not a switch: see [Adding the pages](#14-adding-the-pages). Features are set once; the project's Settings page in the portal is for the rare change after. Under `pnpm dev` the
   portal's new-project wizard, behind the plus card on the Workflows page, writes this same file, if the user would rather click through it.
   Put features only this project has under `extras`, each with its `dependsOn`. Set
   `ticketSize` unless it is `block`.
   Written by hand, open `data/workflows/projects/<id>.diary.md` beside it, copying
   [`marina-roustan.diary.md`](../../../data/workflows/projects/marina-roustan.diary.md)'s header
   and no lines; the wizard does this itself.
3. GitHub side: `pnpm workflow:setup <id>` prints the milestone and labels it would create. Show
   the user, and only on their go run it with `--yes`, since it writes to GitHub. Run it again after
   a feature is switched on, for the new blocks' `cap:` labels.

## 1.4 Adding the pages

A feature inventory or site brief ends with every page template, custom page and blog in the
project's `extras`, each naming a type from the template: `page-template`, `custom-page`, `blog` or
`blog-comments`. **A page on a template is not an extra.** The legal, about and privacy pages on one
layout are one `page-template`, whose `summary` names them; a page with a different layout is a second
template, and a page written in code, such as a landing, is a `custom-page`. Never suggest one extra
per content page. Comments are set up once, by the first blog that takes them, so a second one adds
no comments work. Show the user the list before the scope sign-off closes, since each extra becomes
its own block and ticket cost. A page that fits no type is an ordinary extra with its own
`dependsOn`, and a lesson for the template.

## 1.5 Drafting a map for a custom project

A `custom` project starts with six recommended blocks from the template — `scope-signoff`,
`error-pages`, `build-review`, `ai-review`, `docs-update` and `go-live` — and the rest of its map is the project
file's `extras`, which you draft and the user checks. Switch a recommended block off only where it
can't apply, such as `error-pages` on a dev-only tool or a package, with a one-line comment above
the switch saying why; never redraw one as an extra, since an extra can't reuse a template id.
Read the repo first, then ask only what the code can't tell you: what it is for, who uses it, what
done looks like, and what is still undecided.

1. **One block per thing an agent can finish and a check can verify**, at most 13 points on the
   [complexity scale](../../../docs/workflows/README.md#complexity). Anything bigger gets suggested
   `tickets` or becomes two blocks.
2. **Every open question is a `spike`, and every call only the user can make is an `owner` block**,
   such as scope, a provider or an API shape. Build blocks that depend on the answer go in
   `dependsOn`, so filing waits for them.
3. **Every block has `doneWhen`**, written as checks rather than tasks, and a `reuse` naming the
   precedent to copy — a package, a script folder, a layer — with a path that exists. Copy is
   written in place as the page is built and reviewed by the owner on that page, never approved
   up front as a list in the ticket.
4. **Write lessons only from issues that happened**, with their numbers. Leave them out rather than
   inventing any.
5. **Stages are `plan`, `build` and `ship`.** The template's `go-live` owner block needs every other
   `ship` block, so the release is a decision too; never add a second one.

Show the user the map in the portal at `/workflows/<id>` before running `workflow:setup`, and
change the file until they agree with it. If a second project of the same kind turns up, its map
becomes a template.

## 1.6 Every build ends in a review

Per-ticket review sees one block; nobody sees the build as a whole. Every template carries a
`build-review` owner block with `dependsOn: [stage:build]`, so it waits on every build block, the
project's own pages included; in `custom` it is a recommended block, switched off only for a build
too small to review.

When the build closes, the agent prepares the overview its `doneWhen` asks for and the user makes
the calls. The user may instead settle it as skipped in its panel, but that is their call; never
settle it yourself (`developer-portal-front-door` drew six build blocks over two designs and no
review).

Two AI reviews sit around it, both run by the agent with the tools
[`0043`](../../../docs/decisions/0043-impeccable-for-ai-made-designs.md) sets up. `lab-review` runs
Impeccable over every lab direction before `design-approval`, so the owner picks with the AI tells
already named. `ai-review` follows `build-review` and runs Impeccable on every page and no-ai-slop
on every string the build wrote, before `go-live`. Both list findings for the owner; neither
changes a typeface, colour or layout on its own. `custom` carries only `ai-review`, as a
recommended block.

## 2. Filing a block

File everything the map says can be filed, never one block at a time: the point of the map is that
every unblocked block has a ticket an agent can take in parallel. A block that needs only build
blocks can be filed as soon as those have tickets. In the portal a block that can be filed reads
*Can file now*; one that can't reads *Waits* and names what it waits on.

After any filing, any close and any merge, run `pnpm workflow:file <id>` with no block. It lists
every block that can be filed now; with `--yes` it files them, round after round until nothing more
opens.

1. `pnpm workflow:file <id> <block>` files one block. It prints the tickets, their labels and their blocked-by links
   without writing anything. Under a `ticketSize` other than `block` it is one ticket for the
   block and the others its size bundles it with, filed whole or not at all. It refuses a block still waiting on an open `spike` or `owner` block,
   because that decision can still change what the tickets say (#208, #242 → #299).
2. When a block has no suggested `tickets` in the template, the command drafts one from its title
   and `doneWhen`. If that would be too thin for an agent to act on, add `tickets` to the template
   first; the next project inherits them.
3. Show the user the dry run. Filing is outward-facing.
4. `pnpm workflow:file <id> --yes`, which re-syncs.

A dependency that turns up later is added on GitHub, on the issue's *Relationships* panel or with
`gh issue edit <n> --add-blocked-by <m>`, not in the project file. After filing, GitHub wins.

## 2.5 Redrafting once the design is approved

The map is drafted from the idea a project starts with, and the lab changes that idea. Once the user
picks a direction, and before `design-approval` closes, re-read every build block against the
approved lab and the decision reports. Where the two differ, the design wins (#479 built
the old plan and was thrown away).

| Block is | Do |
| --- | --- |
| Unfiled | Rewrite it in the project yaml, naming its lab page, then file it |
| Filed, not started | Edit the issue's body and criteria with `gh issue edit`, since GitHub wins after filing; close it as not planned if the design dropped it |
| In flight | Ask the user: re-scope it, or let it finish and file a follow-up |
| Closed | Never reopen it; file a follow-up if the design changed what it built |

A block the design added and the map lacks becomes an `extra`, and a lesson for the template.

## 3. Placing unsorted tickets

To organise lists milestone issues with no usable `cap:` label, and open issues with the project's
area label but no milestone — `pnpm issue:add` sets none, so that's where the user's own tickets land.
Propose a capability for each in a table (issue, title, proposed `cap:`, why). After the user
confirms, add them with `gh issue edit <n> --milestone "<Milestone>" --add-label cap:<id>` and sync
again.

A ticket that fits no capability is either an `extra` for this project, or a lesson for the
template. Say which.

## 4. Sign-offs and settling

- An `owner` block is the user's call, never yours. The user approves it either by marking it done
  in its panel on the project page under `pnpm dev`, with no ticket, or by closing its ticket on
  GitHub. Never do either yourself, and don't file an owner ticket the user would rather settle.
- Use `settled` with a one-line note and an `on:` date when a block was done or deliberately
  skipped without a ticket of its own, so the replay counts it from that day. Never settle
  something only to raise the %.

## 5. Feeding the template

When a project finds something the template didn't ask for (a late feature, a provider swap, a
redo, a dependency nobody drew), add it to the template as a block, a `dependsOn` link or a
`lessons` entry with the issue numbers. The next project learns it up front. That is the template's
whole point.

## 6. Abandoning a project

When the user drops a project, run `pnpm workflow:drop <id>` and show them what closes and what
stays. Only on their go, add `--yes`, then delete the project from its Settings page. In that order,
because `drop` reads the milestone from the project file. It closes as not planned and never deletes;
anything started or closed stays.

## 7. Keeping the diary

Every project has a `<id>.diary.md`. Append one line in the
[diary's shape](../../../docs/workflows/README.md#diary), dated from `date +%F`, when:

- the PR that closes a ticket is about to open (an `estimate` line). That PR closes the block: commit
  the line, `pnpm workflow:sync <id> --close` and any unfiled block the work proved wrong to its branch
  before `gh pr create` or `pnpm issue:ship`, never after the merge. `workflow-close.sh` refuses
  the PR otherwise;
- the user corrects or complains about the workflow, the tooling or your output, or says something
  went well, logged as it happens;
- the map, a ticket's text, a rule or a command turns out wrong, or plainly works.

Before appending, ask: does this line say something worked or went wrong? If not, don't write it.
What the work found (measurements, the decision, a green `pnpm check`) belongs in the decision report
or the commit. Never praise your own work.

## The design stage of a website rebuild

What the `website-rebuild` design capabilities expect, learned on Huella:

- **Data before taste.** The content audit and feature inventory close before any direction is
  drawn. Every element on an approved page should trace to an audit row.
- **Design in code** with dev-only `/lab` pages on real content, two or three directions under
  `/lab/attempts/`, reviewed as screenshots at 390, 768 and 1280 px. No Figma or Penpot.
- **Brand from the live site's computed styles** (`pnpm brand:extract <url>…`), then semantic
  tokens with a contrast table (`pnpm brand:contrast <main.css>`), and the raw-palette lint ban
  from day one. Copy
  [`apps/huella-legal/layers/design`](../../../apps/huella-legal/layers/design) and its
  `eslint.config.ts` rule.
- **The lab is a design, not code.** Production components are rebuilt on Nuxt UI from it, never
  copied.

## Verify

```sh
pnpm workflow:sync <id>
pnpm workflow:next <id>
pnpm exec nx collect @joinery/developer-portal   # invariants include every workflow file's rules
```
