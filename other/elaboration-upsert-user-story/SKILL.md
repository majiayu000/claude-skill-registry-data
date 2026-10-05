---
name: elaboration-upsert-user-story
description: >
  Create or draft new work items (stories, tasks, bugs, epics) as local markdown
  files under docs/discovery/, following the house story template, point scale,
  and conventions. Use this whenever the user wants a new work item: phrasings
  like "create" or "write up a story", "make a ticket", "log a bug" or "ops
  task", "create an epic", "raise a ticket", or any description of work that
  should be tracked as a new item, even when they only describe the work rather
  than naming a ticket. Do NOT use this for reading, searching, commenting on,
  transitioning, or reviewing existing tickets; for GitHub issues or pull
  items, GitHub issues or pull requests, Confluence pages, or PRDs; or for a
  bare "what points would you give" estimate when there is no ticket to create.
---

# Create a MindNova Work Item

Owned by the **Product Manager** persona (the upsert-user-story step). Invoked as `/elaboration-upsert-user-story`.

Create well-formed work items as local markdown files under `docs/discovery/`. The goal is a
work item that lands ready-to-refine: correct type, the house template filled in with real
detail, a defensible point estimate, the right epic, and links to related work, with no
duplicates created by accident.

## Directory layout

Work items live locally in the repo:

- **Epics:** `docs/discovery/epics/<epic-slug>.md`
- **Stories:** `docs/discovery/stories/<epic-slug>/<story-slug>.md`
- **Spikes:** `docs/discovery/spikes/<spike-slug>.md`
- **Backlog:** `docs/discovery/backlog.md` (ordered list of items by priority)

## Key convention

Each work item carries a sequential key in its front-matter: `key: MN-<number>`. To assign a
new key, scan existing files under `docs/discovery/` for the highest `key: MN-` number and
increment by one. The key is the stable anchor for `story:` edges in artifact front-matter
throughout the repo.

## Workflow

The order matters. Researching and confirming before creating is what keeps the backlog clean.

### 1. Research first, to avoid duplicates

Before drafting, search existing work items under `docs/discovery/` for the same theme. A
near-duplicate already in the backlog is common, and creating a second one is worse than
reusing the first. Grep for keywords in story titles and descriptions.

If you find a related or originating item, read it to understand the prior work, and plan to
link the new item to it via `relates:` in front-matter.

### 2. Surface collisions, do not silently pick

If an epic for the target quarter/theme already exists, or a placeholder story already covers
the same idea, stop and tell the user. Offer to reuse versus create-new rather than guessing.
The user owns that call.

### 3. Draft using the house template

Fill the template in `references/story-template.md` with real, specific detail. For MindNova
or platform engineering work, reference actual files, classes, and methods so the item is
dev-ready. Vague success criteria are the most common weakness; make them checkable.

For dev stories, verify load-bearing technical claims against the actual codebase before
writing them into "How we'll do it" or "Technical Implementation". A ticket that asserts a
field varies, an entity already exists, or a code path behaves a certain way, when the code
says otherwise, sends the implementer down the wrong road. Read the relevant file. Name the
file or symbol you checked. If a load-bearing claim cannot be confirmed, write it as an open
question in Risks & Blockers rather than stating it as fact.

### 4. Estimate points relative to real comparators

Do not guess a number in a vacuum. Pull the points of 3 to 5 comparable, recently completed
stories from `docs/discovery/` and place the new one among them. See "Story point scale"
below. Show the comparison so the estimate is defensible.

### 5. Confirm before creating

Present the full drafted work item (summary, type, epic, priority, points, and the rendered
description) and ask for a go-ahead. Proceed once the user confirms.

### 6. Create the file and update backlog

- Write the markdown file to the correct path based on type (epic/story/spike).
- Add a reference to the item in `docs/discovery/backlog.md` at the appropriate priority position.
- Report the new key and file path.

## Front-matter schema

```yaml
---
key: MN-42
type: story          # story | task | bug | epic | spike
status: backlog      # backlog | refined | in-progress | done
epic: MN-10          # parent epic key (omit for epics/spikes)
points: 5            # story points
priority: minor      # minor | high | critical
labels: [MindNova]
relates:
  - key: MN-38
    why: "shares the calendar domain model"
---
```

## Conventions

- **Priority**: default `minor` for most MindNova/platform stories. Use `high`/`critical`
  only for prod blockers or customer impact.
- **Labels**: `Refined` (groomed and sized), `ops` (operational task), `MindNova` (platform
  work). Apply `Refined` only when the item is genuinely detailed and sized.
- **Types**: `story` (user-goal feature), `task`, `bug`, `epic`, `spike`.

## Story point scale

- **2** trivial fix / small ops task (one-line change, retire a resource)
- **3** small multi-step task (update config + docs, small UI feature, single helper + tests)
- **5** medium task (new endpoint, moderate UI feature, retry helper + tests)
- **8** substantial feature (domain model + runtime hook + UI + tests)
- **13** large migration (multi-component data-model move)

## Writing rules (apply to all work item content)

- **No em-dashes** anywhere in summaries or descriptions. Use commas, colons, parentheses,
  or " - ".
- **No AI attribution** in any field. Write as if a human authored it.

## References

- `references/story-template.md` - the 6-section house template and a worked example.

## Next steps

- `/elaboration-upsert-user-story-acceptance-criteria` (PM/QA) - write the story's acceptance criteria and test traits.
- `/governance-enrich-ticket` (any) - link related items and artifacts with the why.
- When implementation starts, `/create-code-generation` (Developer) takes the story through build, tests, docs, and PR.
