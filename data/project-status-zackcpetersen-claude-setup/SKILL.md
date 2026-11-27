---
name: project-status
description: Use when the user asks for a visual status of their projects, a project dashboard or status page, to refresh or republish it, or to add, change or finish a one-off item on it.
---

# Project status

A visual status page, published as a private Artifact. The home view is one laptop screen (about 1440x800) with no scrolling, built for a quick glance: one thing to do first, a short list after it, and everything else folded. Shapes before text: rings, bars, step segments and badges. Every count on the page opens the rows it counts in one click.

Home, in three columns:

- **Header**: the date, build time and count chips, each a link: "need you" with total minutes (`#need`), "late" (`#late`), "running" (`#running`), "wins today" (`#wins`), and "GitHub stats" (`#github`).
- **Do this first** (the hero): the single most important open item, with its one next action, a rough time in minutes, an Open button to its link and its project. When nothing needs the user it says "Nothing needs you" and points at what is running.
- **Up next**: the next 3 items that need the user, one row each with the action, the date and minutes. The rest fold behind "Show N more". Rows from a GitHub or Slack feed older than 24 hours carry an "old feed" badge, explained once in a note at the end of this card.
- **Shelf** (the user also says "parked" or "loose ends"): one collapsed section with one total count, capped at 5 when open. It holds the open items the page parks (tag "idea" or "later": a title that starts with "Idea" or "After", says "Parked", or is due more than 14 days out, config `focus`; tag "snoozed" with its "back MM-DD" date) and the loose ends from `shelf[]` in `projects.json` (tag "loose end", with its age in days and a quiet "over 14d" flag past `shelf.stale_days`). The summary shows "N of 12 loose ends" when `shelf.cap` is set. When empty it still shows, with "Shelf is empty".
- **Projects in progress**: one row per project, sorted by priority (P1 first): a ring (percent), name, priority and status, a step bar with "X of Y steps", the next milestone, its ticket and Slack channel links, and "late" and "for you" badges. The name opens the project's own page.
- **Running without you**: things in flight that need nothing from the user: today's dated milestones (with their position, "chunk 2 of 4" or "3 of 10 files", when the text says so, else "today"), long jobs, deliveries counting down to their confirm-by date ("day X of Y"), and the people we wait on (aging bars). 5 shown, the rest folded.
- **Wins today**: today's progress lines, one-offs finished today and the items cleared today, 5 shown, the rest folded. "N PRs merged this week" opens the GitHub page.
- **Footer**: minutes are rough, source problems, unlinked mentions, the config `source_note`.

Other pages (hash routes; each has a "Today" link back, and Esc goes home):

| Route | What it shows |
|---|---|
| `#need` | Every item that needs the user, in order, with its project |
| `#late` | Every late item (late asks and nudges, late milestones and jobs, passed project deadlines) with its date, link and project |
| `#running`, `#wins`, `#shelf` (also `#parked`) | The full list behind each home card |
| `#p-<id>` | One project: header (ring, priority, status, deadline, steps, all tickets and Slack links, summary), then Late (first, in coral, each with its date and link), Needs you, Next (with how the percent was worked out), Running, Breakdown, Recent progress, Decisions and Links |
| `#github` (also `#github-<me or team>-<30 or 90>`) | PR pipeline by stage (with CI failed and conflict flags), reviews asked of the user, and the stats: PRs merged, reviews given, time to first review and to merge (with sparklines), merged per week (chart and table), review load, turnaround (median and p90), PRs by repo group and the data range. Me or team, 30 or 90 days |

Older links (`#inbox`, `#stats`, `#prs`, `#waiting` and so on) open the nearest page.

Counts and lists: every list shows at most 5 rows by default (Up next shows 3). "Show N more" grows the same list in place (same rows, no inner scroll box) and turns into "Show less" at the end of the list; the page may scroll while a list is open. Nothing is dropped. The header's late count, each project's late badge and the late lists all come from one list (`focus.late_items`), so a count always matches rows one click away. Long titles clamp to two lines on home with the full text on hover, and wrap in full on the list pages and on phones.

Color rule: one accent means "needs you" (the hero, its button and the row dots); coral only for something late; progress and everything else stay calm; no color stands for a person. Every ticket key, PR, thread or page the page names is a link to its source (see "Links").

Nothing in this skill names a company, person or project. Those come from the data and config files.

## Files

| File | What it is |
|---|---|
| `template.html` | The page shell. `build.py` inlines `page.css`, `page.js`, the theme and the data into it, so the published page is one file |
| `page.css`, `page.js` | All styles and all page code: a few reusable parts (`row`, `list`, `section`, `subpage`) and a hash router (`ROUTES`). Neutral colors, no names or links baked in |
| `build.py` | Turns a data file (and optional config and home folder) into the page. The data format is in its docstring |
| `derive.py` | Every rule the page shows: inbox items, dedupe, bands, freshness, done today, job finish dates, waiting and delivery bars, mention links, and `focus_view` (hero, up next, running, wins, the shelf, the late list, project tiles with their tickets and Slack links, feed note) |
| `inbox.py` | The only way the session writes `inbox.json` |
| `add_oneoff.py` | Adds or finishes a one-off in the data file |
| `job.py` | Records progress on a long job (a backfill, a big export) in the data file |
| `apply_events.py` | Applies event-log events since `events_cursor` to the data file (progress, decisions, jobs, asks, waits, clears) and prints what it could not place |
| `datafile.py` | `locked_json`: the shared lock and atomic write that `job.py`, `add_oneoff.py` and `apply_events.py` use for the data file |
| `config.example.json` | Starter config: title, tracker and GitHub link bases, footer note, time zone, inbox and feed settings, shelf source and cap, logo, color overrides |
| `sample-data.json`, `sample-home/` | Made-up data, inbox and feeds to try the page with |
| `tests/` | `unittest` tests: `python3 -m unittest discover -s skills/project-status/tests` |
| `~/bin/status-feeds` | From `bin/` in this repo. Writes the GitHub and Slack feed files on a schedule, no model in the loop |
| `~/bin/eng-stats` | From `bin/` in this repo. Caches the org's PRs and writes `feeds/stats.json` (aggregates for me and my team only) once a day |

Per-machine files live outside the repo, in `~/.claude/project-status/`:

- `config.json`: copied from `config.example.json` and filled in. Also holds `artifact_url` once the page is published.
- `projects.json`: the current data.
- `inbox.json`: session-owned inbox items, written only by `inbox.py`.
- `feeds/github.json`, `feeds/slack.json`: written only by `status-feeds`. `feeds/stats.json` and `cache/`: written only by `eng-stats`.
- `state/build.json`: written only by `build.py` (first-seen times and what cleared today).

## Writing style

Every line the page shows is written by an agent into `projects.json` or `inbox.json`. Write it so it reads at a glance:

- Lead with the outcome or the next action: "Nudge Ana: the export file", "DE-12 shipped to prod".
- Short, plain sentences. One fact per line. No jargon where a plain word works.
- A line that needs the user names one action and a rough time (`effort`, `effort_min`): "Approve the agent" with "2m".
- Staged work says its position: "chunk 1 of 4", "step 2 of 3", "3 of 10 files". The page draws segments or a bar from it; without one the Running row only says "today".
- Wins are concrete: what shipped, merged or was confirmed, with its key. Not "made progress on X".
- Work that belongs to no project (a review for another team, an admin task) is a one-off, never a line under some project. A finished one-off with `done_on` set to today shows under Wins today (`add_oneoff.py --done` sets it).
- Status lines that are not wins ("no new chunk yet", "still waiting") belong in `next_milestone` or `waiting_on`, not `recent_progress`.
- Lists hold at most 5 shown rows; the page folds the rest. Never drop an item to make a list fit.
- Plain hyphens only, never em-dashes or en-dashes.

Pass these rules, word for word, to every gather and publisher agent.

## Setup (once per machine)

1. `mkdir -p ~/.claude/project-status`
2. `cp ~/.claude/skills/project-status/config.example.json ~/.claude/project-status/config.json` and fill in `title`, `tracker_url` (the prefix a ticket key is added to), `github_org` and `source_note`. Delete a line you do not need.
3. Colors: `theme.light` and `theme.dark` override the page's tokens (the full list is the `:root` block at the top of `page.css`). The groups: surfaces (`--canvas`, `--card`, `--line`, `--track`), ink (`--text`, `--strong`, `--muted`), needs you (`--rail` is the hero card, `--rail-ink` its small text, `--rail-on` its button and eyebrow, `--on-rail` its headline, `--accent` the row dots), done (`--accent-ink`), charts (`--chart-1`, `--chart-2`, `--chart-grid`, `--prog`), late (`--alert`, `--alert-ink`, `--alert-bg`), `--link` and `--font`. The repo ships a neutral palette in light and dark. A brand palette (from the user's design system) goes only in this local config, in both `theme.light` and `theme.dark`, never in the repo. Keep text pairs at 4.5:1 contrast.
4. Logo (optional): put the logo files next to `config.json` (never in the repo) and set `brand.logo` (the version for light backgrounds), `brand.logo_dark` (for dark backgrounds) and `brand.name` (alt text). Paths are relative to the config folder. SVG, PNG, JPEG or WebP, at most 60 KB each. The build inlines them and does a light tidy of SVG (not a full clean-up); the page only ever shows the logo as an image, which is what keeps it safe. The logo sits at the left of the header and switches variant with the theme. Leave `brand` out for a text-only header.
5. Try it with the sample: `python3 ~/.claude/skills/project-status/build.py ~/.claude/skills/project-status/sample-data.json <scratchpad>/project-status.html --config ~/.claude/project-status/config.json --home ~/.claude/skills/project-status/sample-home --no-state --now 2026-01-12T18:00:00Z`, then publish that file with the Artifact tool to see the look.
6. Feeds (optional): set `tz` in `config.json` (an IANA name), then `~/bin/status-feeds doctor`, then `~/bin/status-feeds run --force`, then install the schedule with the commands `~/bin/status-feeds schedule --print launchd` prints (Linux: `--print cron`, add it with `crontab -e`). Install it only with the user's yes. Set `inbox.github_orgs` when your PRs live in more than one org, and `inbox.slack_url` (for example `https://<workspace>.slack.com/archives/`) so Slack items link to their thread. A PR only shows as "Merge" once its checks have passed; list repos that have no checks at all in `inbox.no_ci_repos` (`owner/repo`) so their approved PRs can show as ready too.
7. Stats (optional): set `stats.org` (or rely on `github_org`) and `stats.team_slug` (the GitHub team that is "my team"; `stats.team_members` is the fallback list), then `~/bin/eng-stats doctor`, then `~/bin/eng-stats run` (the first fill takes about 25 minutes and about 150 of the 5,000 hourly GraphQL points), then install the daily schedule `~/bin/eng-stats schedule --print launchd` prints (Linux: `--print cron`). Install it only with the user's yes. Optional keys: `repos_include`, `repos_skip`, `repo_groups`, `bots`, `business_hours_clock`.
8. First real build: follow "Refresh" below. After the first publish, save the Artifact link as `artifact_url` in `config.json` so later sessions update the same page.

If `~/.claude/project-status/config.json` is missing, do steps 1 and 2 with the user before anything else.

## Refresh

1. **Gather** the data into `~/.claude/project-status/projects.json`, in the format from `build.py`'s docstring. First run `python3 ~/.claude/skills/project-status/apply_events.py ~/.claude/project-status/projects.json` so events logged since the cursor land and the cursor moves past them (it takes the file's lock, which the gather agent cannot); relay its `unplaced` lines. Running it before the gather, not after, means the gather's fresh lists are never stacked with the same facts again. Then dispatch one read-only agent for this (pass `model`); it writes only that file. Sources, in order: the user's project notes (for the `board` skill, the `Projects data source` line in `~/.claude/config/board.md` (older installs: `### Work board` in `~/.claude/CLAUDE.md`), plus today's board row), then the tracker and GitHub only for gaps. Rules for the agent:
   - `needs_me` holds only what the user must do or decide by hand. What waits on someone else goes in `waiting_on`. What an agent can do alone goes in neither.
   - `progress_pct` comes from real milestones or tickets, and `progress_basis` says how in one sentence. Never invent precision.
   - Keep `one_offs`, every project's `jobs` and the top-level `events_cursor` already in the file. They are the user's own list, `job.py`'s and the event log's cursor.
   - Set `next_milestone_date` (`YYYY-MM-DD`) when the next milestone has a date, so it shows under Running without you on that day. Start its first sentence with the position when the work is staged ("chunk 1 of 4").
   - Each project lists its tickets and Slack channel in `links[]` (`{"label": "#channel-name", "url": "<channel link>"}`), plus its `epic`. The page shows them on the project's row and page; a project without them shows "none in the data".
   - Slack links in `links[]` are labeled `#channel-name`, `Thread: <topic>` or `DM: <first name>`, at most 3 per project, links only and no message text. Take them from the project page's `Slack:` line.
   - Fill `shelf` from the loose-ends source named by `shelf.source` in `config.json` (for the `tidy` skill, the Projects row named by the `Loose ends` line in `~/.claude/config/tidy.md`): one `{title, added, link, done}` per checklist line (`- [ ] item (added YYYY-MM-DD) link`; a ticked line is `done: true`). Copy the lines as they are; never add or drop one. Without `shelf.source`, keep `shelf` as it is.
   - Every item carries a link to its source when it names one: `link` on asks and waits, `ref` or `links[]` for tickets, PRs, Notion pages, Slack threads, runs and docs.
   - Keep `link`, `effort` and `who_waits` fields when present, and set `needs_me[].link` and `waiting_on[].link` whenever the source line has a URL (a Slack thread, a PR), so items merge with the feeds instead of showing twice.
   - Follow "Writing style" above for every line (outcome or action first, one fact per line, "chunk X of Y" for staged work, concrete wins, plain hyphens). Leave out finished projects.
   - Do not show the loose-ends row as a project: skip the Projects row named by the `Loose ends` line in `~/.claude/config/tidy.md` (older installs: `### Tidy` in `~/.claude/CLAUDE.md`) (the `tidy` skill's catch-all list).
   - Return a short list of anything unsure or stale. Relay it.
2. **Check** the data before building: drop asks the user already answered in this session, and links that are not `https://`.
3. **Build**: `python3 ~/.claude/skills/project-status/build.py ~/.claude/project-status/projects.json <scratchpad>/project-status.html --config ~/.claude/project-status/config.json --home ~/.claude/project-status`. Relay any `warning: unlinked mention` lines it prints and fix them (see "Links").
4. **Publish** in a one-shot sonnet agent (general-purpose): it builds (step 3), publishes the file with the Artifact tool to `artifact_url` from config (it reads the artifact first when its session needs that), and returns only the link and the version. The main session never reads the artifact, the built HTML or `projects.json`. Without an `artifact_url`, the agent publishes new and saves the link to config. The page is private to the user.
5. Tell the user the link, what changed since the last build, and the unsure list. Percentages are estimates; say so once.

## Small updates (at checkpoints)

The page should never lag the work, but it is rebuilt at checkpoints, not per fact. Facts (a PR merged, a run finished, the user decided something, a reply arrived, a wait cleared) are appended to the event log as they land (`~/bin/board-event add`, see the `board` skill's "Event log"). At a checkpoint, do not gather again:

1. Dispatch one one-shot sonnet publisher agent for everything since the last checkpoint. It runs `python3 ~/.claude/skills/project-status/apply_events.py ~/.claude/project-status/projects.json` first: that applies every event since the file's `events_cursor` that needs no judgment (progress lines, decisions, jobs, new asks and waits, cleared ones), moves the cursor and sets `as_of`, and prints one `unplaced <id> <kind> <key>: <text>` line per event it could not place. Then it edits `projects.json` by hand only for those unplaced lines (a `failed` is relayed, not written as progress) and the judgment fields (`progress_pct` when a milestone or ticket closed, keeping `progress_basis` true; `status`; breakdown item `state`; `summary`; `next_milestone`, keeping a staged position, "chunk 2 of 4"), in the "Writing style" wording, never touching `events_cursor`. It builds and publishes as in Refresh step 4, and returns the link and one line on what changed.
2. The main session never opens the data file.
3. Say what changed in one line. Do not ask first.
4. While a publisher or gather agent is working, do not run `job.py` or `add_oneoff.py`. Those agents write the file without the lock, so a change made in that window is lost. Append an event instead; the next checkpoint applies it.

Do this without being asked at every checkpoint: a sync, the wrap, when the user turns to the board, and right away for an event `add` printed as `URGENT`. No publish for a single non-urgent event. Without `~/bin/board-event`, hand the publisher the change in one line, as before. The `board` skill runs it at its checkpoints, and writes the page link as the first line of each daily row's `## Your TODOs`.

## Inbox

The inbox is worked out at build time from these sources. Feed items clear themselves; nobody ticks them.

| Source | Writer | Items |
|---|---|---|
| `projects[].needs_me[]` | gather agent, session | ask |
| `one_offs[]` with `needs_me` and not done | `add_oneoff.py` | one-off |
| `waiting_on[]` whose `nudge_due` is today or past | gather agent, session | nudge |
| `feeds/github.json` | `status-feeds` | review requests aimed at the user; for the user's own PRs one of fix conflict, fix CI, reply to review, merge |
| `feeds/slack.json` | `status-feeds` (from the Slack poll's triage log) | Slack asks held as not-now |
| `inbox.json` | the session, through `inbox.py` | approve an agent, send a draft, confirm a delivery, a TODO, an ask |

The session writes `inbox.json` only through `inbox.py` (`python3 ~/.claude/skills/project-status/inbox.py --help`):

- `add --kind K --title T [--link URL] [--id ID] ...`: an agent is held on an approval, a draft is waiting to be sent, a delivery passes its confirm-by date, or the user asks for a TODO.
- `done <id or title text>`: at the checkpoint after the fact lands, the same moment as "Small updates".
- `snooze <id> --until YYYY-MM-DD`: the user says "later" with a date. Only `inbox.json` items can be snoozed.
- `meeting --title T --at ISO`: at rollover, only when the session knows the next meeting.
- `sync --origin board --file F`: the `board` skill's mirror on every sync.

Items with the same PR, Slack thread or other link merge into one (the session's words, the feed's live state). Ticket keys never merge, and neither does a tracker ticket link on its own: two asks that share a ticket link merge only when their titles match too, so each keeps its own words and date.

## Long jobs

A job that runs for days (a backfill, a big export) shows under Running without you as "done of total" with a bar and its finish date. The page works out the percent, the finish date (from `per_day`, counted from the last report, so a job that stops reporting goes late) and whether it is stale.

- Give `--total` whenever the size is known, so the row reads "3 of 10 files" and not just a label. When a milestone line names the same work, it carries the same position ("chunk 2 of 4").
- After each progress report: `python3 ~/.claude/skills/project-status/job.py ~/.claude/project-status/projects.json set <project_id> "<label>" --done N --total N [--unit files] [--per-day N] [--eta YYYY-MM-DD]`. Only the fields given change.
- When it finishes: `... job.py ~/.claude/project-status/projects.json done <project_id> "<label>"`. The job goes and a "Finished <label>" line lands in recent progress.
- Then hand the publish to the one-shot publisher (Refresh step 4).
- In a board session, append a `job-progress` or `job-done` event instead (`--field job=<label> --field done=N --field total=N`); the checkpoint's `apply_events.py` run records it through `job.py`'s own code.

## Links

Every ticket key, PR, Notion page, Slack thread, run or doc the page names is drawn as a link. The rule lives in `derive.py` (`link_mentions`), with the link bases from local config only:

- Ticket keys (`ENG-142`): `tracker_url` plus the key. Set `links.ticket_keys` (for example `["ENG"]`) to link only your tracker's keys; left empty, any `KEY-123` links except standards like `UTF-8` or `SHA-256`.
- `repo #123`: a PR in `github_org`, only when `repo` is in `links.repos` or in the GitHub feed, so "step #3" stays plain text.
- Slack triage keys (`C0123ABC:1768000000.123456`): `inbox.slack_url`.
- Anything else named by a key: `links.patterns`, a list of `{"match": "<regex with one group>", "url": "<base>{1}"}`.
- Notion pages, docs and threads have no key, so they link only through the item's own `link`, `ref` or `links[]` field.

The build prints `warning: unlinked mention <text> at <where> (<why>)` for a key with no base configured, or a row that names a thread, page or doc but has no link, and the page footer lists them. Fix the data (add the link) or the config (add the base); the build never fails on them.

## One-offs

When the user says "add a one-off", "put X on the status page" or "X is done":

- Add: `python3 ~/.claude/skills/project-status/add_oneoff.py ~/.claude/project-status/projects.json "Title" [--needs-me] [--due YYYY-MM-DD] [--note "..."] [--ref TICKET-1] [--state "in progress"] [--pct 40]`. Only the title is required.
- Finish: `... add_oneoff.py ~/.claude/project-status/projects.json --done "part of the title"`
- Then hand the publish to the one-shot publisher (Refresh step 4). No gathering needed.

A one-off that grows (several steps, other people, a deadline) becomes a project: add a `projects` entry with just `id`, `name` and `progress_pct`, and fill in more later. Every other field is optional.

## Changing the page

- Edit `page.css` and `page.js` for layout, `derive.py` for every number, date and rule the page shows, `build.py` for the data contract. `page.js` only lays out what `derive.py` worked out. Keep all of them generic: no names, links or brand colors.
- The design brief, from the user: ADHD-friendly. Visual first (shapes before text), one screen with no scrolling at 1440x800 by default, one hero that says what to do first, every list capped at 5 with the rest folded in place, every count a one-click path to exactly the rows it counts, each project on its own page. Low noise, one row anatomy (mark, text leading with the fact that matters, meta), no dead ellipsis. One accent for "needs you", coral only for something late, everything else calm. Works in light and dark and at phone width.
- A new page: add a renderer to `ROUTES` in `page.js` built from `subpage`, `section`, `list` and `row`, and a link to it from the count or card that leads there.
- After a change, run `node --check skills/project-status/page.js` and the tests, then build with `sample-data.json` and `sample-home/` and check it at 1440x800 (no scroll, hero on top) and 400px wide (no sideways scroll) before publishing.

## Common mistakes

| Mistake | Fix |
|---|---|
| Putting company colors, names or links in `page.css`, `page.js` or `template.html` | They go in `~/.claude/project-status/config.json` |
| Publishing a new Artifact on every refresh | Pass `artifact_url` as `url` so the link stays the same |
| Details creeping onto the screen | The default view fits one screen. Detail goes on a project's page, a list page or a "Show N more" fold |
| A count with no rows behind it | Every count links to the rows it counts; late counts come only from `focus.late_items` |
| Hand-editing `inbox.json` | Use `inbox.py`, the file's only writer |
| Adding a GitHub review or PR state by hand | The `status-feeds` GitHub feed does it |
| Building without `--home` | The page then shows no inbox.json, GitHub or Slack items |
| Coral for counts or needs-you badges | Coral only for something late; needs-you uses the one accent; counts stay neutral |
| Long, status-style lines in `recent_progress` or `needs_me` | Follow "Writing style": action or outcome first, one fact, a rough time |
| Listing things the user is waiting on under `needs_me` | Those are `waiting_on` rows |
| Overwriting `one_offs` during a gather | The gather agent keeps them as they are |
| Gathering, editing the data file or publishing in the main session | Agents do all three; the main session passes one line and relays the link |
| Running Artifact quickstart for the status page | It exists. Publish to `artifact_url` |
| Hand-editing `jobs` in `projects.json` | Use `job.py` (or a `job-progress` event and `apply_events.py`), so `updated` and the finish date stay right |
| Brand colors in `page.css` | They go in the local `theme.light` and `theme.dark` |
| A logo file in the repo | It sits next to the local `config.json`, named in `brand` |
| Per-person stats or names in `stats.json` | Stats are aggregates for me and my team only |
| A ticket key or thread named with no link | Add the link to the item, or the link base to config |
