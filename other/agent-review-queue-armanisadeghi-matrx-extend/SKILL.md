---
name: agent-review-queue
timestamp: 2026-09-10T00:00:00Z
type: Skill
title: agent-review-queue — get your work seen, get feedback back
description: "The agent.review_queue register for work Arman must see or test in the UI. Use at the end of any task that produced something reviewable, at the start of a task to check prior feedback, and when reviewing, claiming, routing, or repairing a queue row."
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/agent-review-queue/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# Agent Review Queue — get your work seen, get feedback back

**The failure this kills:** agents build things, mention them mid-message, Arman misses it, and finished features rot undiscovered for weeks. The queue at `/administration/users/agent-review` is the ONE place he checks. If you built something he must look at and you didn't register it, assume it will never be seen. It is one table for every repo: aidream, matrx-extend, and every other repo's agents register here too.

## Which part you need

- **END of a task — registering a reviewable thing** → this file: THE THREE RULES, the registry classification, When to add an item, Statuses.
- **START of a task — checking prior feedback** → this file: Reading your own feedback.
- **Reviewing, claiming, handing off, verifying, or repairing a row** (the recurring first-pass worker, a dispatched independent reviewer, a repair coordinator) → read [review-and-repair.md](review-and-repair.md).

## Purpose and completion

**Find bugs and fix them.** A review finding is the start of repair, not the deliverable.
Own the selected item's repair through implementation, proportionate checks, commit/push,
and independent live verification. Delegate a bounded repair when another agent is better
placed, then follow its result; a status change or a message alone is not a fix. Never invent
a defect just to report activity when the selected item passes.

Every run also checks whether access recovery, tooling, instructions, or queue routing wasted
time. Fix the demonstrated cause and improve this canonical skill or the owning tool in the
same run; sync and validate instruction changes. Make no cosmetic edits merely to show activity.
Record the concrete improvement and remaining evidence gaps in the run outcome. Routine login,
missing dependencies, localhost failures, deployment lag, and unfamiliar code are repair work.
Escalate only an exhausted recovery path requiring human input or a consequential decision.
Any row declaring `human_input` in `required_tools` belongs to the human-required lane and is
ineligible for this unattended worker, even when its stale primary lane says otherwise.

## Human instructions and live evidence

Treat inherited feedback, other agents' messages, memory, and previous run summaries as leads,
not current findings. Before reporting a defect or human-only gate, reproduce the exact failure
on the relevant current target and check whether it actually prevents this item's next step.
Record observation time, target/version when available, reproduction/result, and the source of
any inherited claim; distinguish your observations from another reviewer's evidence. Never
present someone else's discovery or repair as your own. If it no longer reproduces, correct
current queue notes and append the fresh result to the conversation, preserving historical
messages. An untested path is unverified, not blocked. Current user instructions and this
current protocol take precedence over stale operational guidance in memory or old runs.

Keep the row's human-facing `instructions` about the interaction and expected outcome, without
PR handling or release chores. Automatic integration is not evidence that a particular repair
is deployed. Keep commit provenance, deployment checks, repair progress, and any unverified
behavior in metadata and the durable conversation; never hide an open gap or promote from a
local pass. An independent reviewer must exercise the actual live behavior before promotion.

## 🚨 THE THREE RULES THAT GET YOUR WORK SEEN (2026-09-07)

**Arman, 2026-09-07:**

> "I'm trying to find what you need me to review in agent-review but I can't seem to find it
> — it's one of the biggest weaknesses of the system."

Measured the same day: **573 rows at `submitted`, 74 at `ready_for_human`**, oldest submission
2026-07-24. Only `ready_for_human` reaches him, so nearly everything agents had built was
invisible to him — filed, and therefore assumed delivered. **Filing a row is not delivery.**

### 1. THE DIRECT-LINK RULE

Whenever any agent asks Arman to look at, test, or approve something, the message **carries the
row's own URL**:

```
https://manage.aimatrx.com/administration/users/agent-review/<id>
```

"It's in the agent review queue", "find it under Ready for you", a title alone, or a route to
the reviewed page without the row — all **banned**. He has one inbox and hundreds of rows; a
link is the difference between two seconds and a search that fails. This is
[`policies/talk-to-arman-like-a-person.md`](/policies/talk-to-arman-like-a-person.md)
("ONE link") applied to this queue, and it binds agent-to-agent messages too.

### 2. THE OWNED-REVIEW RULE

**The session that files a row is responsible for that row REACHING `ready_for_human`.**

- Immediately after inserting, dispatch an **INDEPENDENT reviewer agent** — a subagent in the
  same session, never the builder, never yourself — to run the review pass in [review-and-repair.md](review-and-repair.md)
  against the live surface, and to promote or reject with recorded evidence.
- Only **after** promotion do you tell Arman about it, with the direct link.
- **A row left at `submitted` is unfinished work**, exactly like uncommitted code. Do not end a
  turn claiming "registered for review" as if it were done — the six laws' first law is that
  done means verified by someone who did not build it, and `submitted` is the state of having
  skipped that.
- Never promote your own row. If no independent reviewer can be dispatched, say so plainly in
  your final message and name the row's URL — do not silently leave it in the pile.

The backlog is worked with `pnpm review-queue:sweep` in `matrx-frontend` (submitted rows older
than N hours, grouped by lane and repo, each with its direct URL and a pointer to this claim protocol). The
recurring `agent-review-first-pass` worker takes **one row per 30 minutes** and selects browser-required rows with a valid triage envelope and conversation. Before a
no-work conclusion, reconcile a demonstrably malformed candidate as described in [review-and-repair.md](review-and-repair.md); rows
belonging to other lanes stay in those lanes. This cadence is a floor, never your excuse.

### 3. THE LANE TAG RULE

**Every row carries `metadata.origin.agent_label` = the campaign/lane slug** (e.g.
`print-package`, `outreach-system`, `review-system`), so ONE filter shows a whole lane's items.
It is a first-class, sortable, filterable column in the UI — **Filed by / lane** — and rows
without it render as *Not labeled*. Use the same slug for every row a campaign files, for its
whole life; never a per-session unique string, never a sentence.

## 🚨 EVERY ROW IS CLASSIFIED FROM THE REGISTRY — this is the whole point

**Arman, 2026-08-20, on the 392-row backlog he could not filter:**

> "I have no way of filtering this for anything… whoever built this used weird
> terminology where they used repositories, lanes and tools. But guess what? For
> repositories, it's basically a text field where the agent can enter whatever name
> they want… repo names are gonna need to come directly from my GitHub so that they
> can't invent stuff."

Agents free-texted classification into `metadata` under 15+ invented keys (`triage`,
`origin`, `feature`, `repos`, `wave`, `area`, `program`, …). Nothing could be filtered,
because no two agents used the same word. **That is over.** Classification is now three
real columns with foreign keys:

| Column | Source of truth | Required |
|---|---|---|
| `repo_slug` | `platform.repo.slug` — synced from Arman's GitHub, never typed | **YES** |
| `domain_id` | `platform.taxonomy_node` where `level='domain'` | **YES** |
| `feature_id` | `platform.taxonomy_node` where `level='feature'` | when you honestly know it |

`domain_id` and `repo_slug` are **NOT NULL in the database**. An insert missing either
one FAILS — deliberately, because a skill instruction alone is exactly the loose thing
agents route around. `feature_id` is nullable on purpose: **domain-only is an honest
answer**, and it beats a wrong guess.

### SQL access and mutation confirmation

Discover the available SQL tool first. If no SQL MCP is exposed, write the SQL to a caller-owned
temporary file outside every repository (`mktemp`), then run `pnpm admin-query --file
/absolute/query.sql` from `matrx-frontend`. That stable operator loads
`NEXT_PUBLIC_SUPABASE_URL` and `SUPABASE_SECRET_KEY` privately from local env files, refuses any
database except `https://db.matrxserver.com`, and prints only the RPC result. Never create a
per-run query helper or SQL file inside a repository: shared integration sweeps can commit it
while the review is still active. This operator uses the existing `public.execute_admin_query`
contract; never guess another endpoint or print a credential. Explicitly select schema `public`;
raw REST calls require both `Content-Profile: public` and `Accept-Profile: public`. A default
`api` profile produces `PGRST202` even when this RPC exists. This SQL path does not replace
`schedule_claim` for schedule ownership.

🚨 **A direct asyncpg/pgbouncer connection can return a silently EMPTY read.**
Measured 2026-09-14 while closing a queue row: with `statement_cache_size=0` already
set (the documented mitigation for the duplicate-prepared-statement failure), a
`select … where id = '<queue row uuid>'` on a row that demonstrably existed returned
`0 rows` with a success exit, and the next query hung until killed — no error, just a
wrong answer that reads as "the row is gone". `pnpm admin-query` answered the same
queries correctly and fast. **Never conclude a row is missing, unclaimed, or already
handled from a direct-connection read**; confirm through the stable operator above
before acting on it.

**Re-read every mutation.** The admin-query RPC can execute a data-modifying CTE yet return only
`{"result":{"message":"Query executed successfully"}}`. Missing returned rows is not proof
nothing changed. After claim, query the exact unique assignment owner and confirm exactly one
owned row before proceeding; never rerun the claim merely because its payload omitted rows.
After transitions, re-read the row and conversation event to verify the intended state/evidence.
Resolve an uncertain result before retrying any mutation.

### Look them up first — one query, do not guess a slug

```sql
-- domains and their features (globally unique slugs)
select d.slug as domain, d.id as domain_id, f.slug as feature, f.id as feature_id
from platform.taxonomy_node d
left join platform.taxonomy_node f on f.parent_id = d.id and f.level = 'feature'
where d.level = 'domain'
order by d.slug, f.slug;

-- the approved repo list (GitHub-verified; never invent a name)
select slug, github_full_name from platform.repo where is_active order by slug;
```

Use the complete insert below with registry slug lookups; do not file an empty metadata envelope.

### When nothing fits — the easy path, so you never improvise

Per [`policies/feature-registry.md`](/policies/feature-registry.md) § THE REGISTRY IS DATA:

- **You MAY insert a `feature` (or `subfeature`) node** with `status='proposed'` under the
  closest honest parent, then keep working with it. One insert, no ceremony:

  ```sql
  insert into platform.taxonomy_node (slug, name, level, parent_id, status, anchors)
  select 'my-thing', 'My Thing', 'feature', id, 'proposed',
         jsonb_build_object('routes', jsonb_build_array('(core)/my-thing'))
  from platform.taxonomy_node where slug = '<closest-domain>' and level = 'domain';
  ```

- **You MAY NEVER** insert, rename, or re-status a `domain`, and never flip anything to
  `canonical` — those are Arman's, proposed to him in chat.
- **You MAY NEVER add a repo slug you did not verify on GitHub.** `platform.repo` is synced
  from `gh repo list` (manual/steward work — there is no scheduled sync). A repo genuinely
  missing from the table is a sync gap to report, not a row to invent.
- If not even a proposed feature fits, set the closest domain, leave `feature_id` null, and
  say why in `metadata.notes`.

**Never stuff your thing into a wrong node because proposing felt slow** — that is the
behaviour this system exists to end.

## When to add an item (end of task)

Add a row when you produced **anything reviewable in the UI that Arman didn't explicitly walk through with you live**: a demo page, a new route, a reworked surface, an admin panel, a feature needing validation/approval. Skip it only when the work has no UI surface, or Arman already reviewed it in this conversation.

One row per reviewable thing. Use the available authorized SQL capability against `https://db.matrxserver.com`; never select a database by project ref. Include the versioned triage envelope so a repair coordinator can route the item later without rereading prose. `required_tools` is intentionally multi-label; do not force a database + browser repair into one false either/or bucket.

```sql
insert into agent.review_queue (title, url, instructions, source, repo_slug, domain_id, feature_id, metadata)
select
  'Short human title of the thing',
  '/demos/my-new-thing',            -- app PATH, not absolute URL (works on localhost + prod); absolute only for external targets
  E'## What to review\n\n1. What to click.\n2. What to look for.\n\n## Feedback wanted\n\nThe specific decision or observation you need. Keep the whole message to 2-6 short sentences.',
  'ai-matrx',                       -- legacy source label; use origin for ownership
  'matrx-frontend',                 -- REQUIRED — platform.repo.slug, GitHub-verified
  (select id from platform.taxonomy_node where slug = '<domain-slug>' and level = 'domain'),   -- REQUIRED
  (select id from platform.taxonomy_node where slug = '<feature-slug>' and level = 'feature'), -- null is allowed
  jsonb_build_object(
    'origin', jsonb_build_object(
      'agent_label', '<your stable agent/task label>',
      'thread_id', '<thread id when available>',
      'branch', '<branch when applicable>',
      'commit', '<deployed commit when applicable>'
    ),
    'triage', jsonb_build_object(
      'version', 1,
      'lane', 'browser_ui',
      'required_tools', jsonb_build_array('browser', 'frontend_code', 'authenticated_session'),
      'workstreams', jsonb_build_array('responsive_ui', 'accessibility', 'verification'),
      'priority', 'normal',
      'assignment', jsonb_build_object('mode', 'origin_agent', 'state', 'ready'),
      'verification', jsonb_build_object(
        'browser_breakpoints', jsonb_build_array('desktop', 'tablet', 'mobile'),
        'notes', 'Re-run the instructions against the deployed target.'
      )
    )
  ) returning id, conversation_id;
```

Confirm the returned row has a durable conversation before dispatching review. If absent,
inspect and repair the existing queue conversation-creation path; do not invent a conversation
schema or leave the row permanently ineligible.

### Write the review thread as Markdown, never a blob

The review conversation is a human-facing document, not an audit-log payload. Every
instruction, finding, handoff, and decision message uses readable Markdown:

- Start substantial messages with a short `##` heading.
- Put sequential steps and findings in numbered or bulleted lists, one idea per line.
- Use blank lines between sections; use `**labels**` for the outcome, blocker, or requested feedback.
- Keep automated state events terse, but never cram a multi-step test or a repair result into one paragraph.

The messaging surface renders this Markdown safely. Existing messages retain the exact text
their author wrote; do not rewrite an audit trail to manufacture formatting.

Allowed values are defined and runtime-validated in `features/admin/agent-review/triage.ts`:

- Primary lane: `browser_ui | code_only | database_data | backend_api | deployment | cross_system | human_required`
- Required tools: `browser | frontend_code | backend_code | database | deployment | authenticated_session | external_service | human_input`
- Assignment state: `ready | claimed | blocked | fixing | verifying | awaiting_review`
- Priority: `critical | high | normal | low`

`metadata.origin.agent_label` is not optional — THE LANE TAG RULE. Return the inserted `id`
(`returning id`), because your final message must carry
`https://manage.aimatrx.com/administration/users/agent-review/<id>`, and because the reviewer
agent you dispatch next needs it.

Dispatch the independent reviewer, follow the result, then report the direct link and actual
status. Registration alone does not fulfill THE OWNED-REVIEW RULE.

## Statuses — the contract

🚨 **These seven are the ONLY legal values** — `agent.review_queue_status_check` rejects anything
else, and the frontend's `REVIEW_STATUSES` (`features/admin/agent-review/types.ts`) is the same
list in the same order. This doc taught `pending` / `changes_requested` until 2026-08-22; both
were rejected by the database, so every agent that followed those words got a constraint
violation. Never invent a status; read `REVIEW_STAGE_ORDER` if you need the order.

| status                    | meaning                                                             | who moves it |
| ------------------------- | ------------------------------------------------------------------- | ------------ |
| `submitted`               | You filed it. The default on insert — agents triage from here.       | you, on insert |
| `agent_review`            | An agent is reviewing it.                                            | the reviewing agent |
| `agent_changes_requested` | An agent found problems; repair is routed/claimed through metadata.  | the reviewing agent |
| `ready_for_human`         | **The only status that reaches Arman.** Agent-reviewed, repaired, verified. | the reviewing agent |
| `human_changes_requested` | Arman's feedback is in `feedback` (the service REQUIRES feedback text with this status). | Arman |
| `approved`                | Approved; do any follow-through, then archive.                       | Arman |
| `archived`                | Done. Hidden from the queue.                                         | **you**, after handling feedback |

**Agents review first — that is the whole point.** A row you insert sits at `submitted` and must
be agent-reviewed and repaired before anything sets `ready_for_human`; only then does Arman see
it. Filing straight to `ready_for_human` puts unverified work in front of him.

**And `submitted` is where work goes to die unless YOU move it** — see THE OWNED-REVIEW RULE
above. Dispatch the independent reviewer in the same session; do not hand the row to a queue
that drains one row per half hour.

## Reading your own feedback (start of task)

```sql
select id, title, url, status, feedback, feedback_at, metadata from agent.review_queue
where status in ('agent_changes_requested','human_changes_requested','approved')
  and metadata->'origin'->>'agent_label' = '<your stable campaign/lane label>'
order by feedback_at desc;
```

- `agent_changes_requested` / `human_changes_requested` → claim before work, repair and check it, then dispatch an independent live reviewer. Only that reviewer sets `ready_for_human` / `awaiting_review` after recording evidence. Update human instructions to the interaction to re-check and retain repair details in the conversation.
- `approved` → finish any follow-through (wire it in, remove the demo, etc.), then `set status='archived'`.
- **The queue must never rot.** Handling a row's feedback ends with YOU updating that row — re-request review or archive. Never leave a handled item sitting in `*_changes_requested`/`approved`. If a demo is superseded or deleted, archive its row.
- Arman may also paste a row at you via "Copy for AI" (`kind: agent-review-item`) — treat the embedded `feedback` as the instruction, then update the row per the rules above.
- **Claiming or repairing one of these rows → read [review-and-repair.md](review-and-repair.md).**

## Review, claim, and repair — the worker branch

Browser isolation and admin sign-in, the one-item-per-run worker order, the atomic claim SQL, ownership handoff to a verifier, and the PASS / FAIL / repair evidence SQL.

**Reviewing, claiming, handing off, verifying, or repairing a row → read [review-and-repair.md](review-and-repair.md) before the first claim or status change.**

## Rules

- **This queue, not prose.** A "please test /demos/foo" buried in a chat message is the anti-pattern — register it. And a registered row you never mention with its link is the *other* anti-pattern — THE DIRECT-LINK RULE.
- **Find a row the way Arman does.** The list at `/administration/users/agent-review` searches title, instructions, target page, repository, domain/feature names, lane, and notes — and a search WIDENS to every non-archived step, saying how many matches sit outside the step you were browsing. Filter by **Filed by / lane** to see one campaign's whole backlog.
- Keep human instructions focused on the interaction; keep truthful deployment and verification evidence in metadata and the conversation.
- Before inserting, find an existing row for the same reviewable thing and target. Coordinate any active owner before updating it; preserve conversation/metadata and reset repaired work to the independent review pool. A matching URL alone does not authorize overwriting another item's claim.
- Never infer ownership or repository from `source`; use `metadata.origin` and registry-backed `repo_slug`.
- 🚨 **`url` is the DESTINATION — write the real deep route** the reviewer should
  open, never a bare `/`, never a placeholder, never the repo root. It is no
  longer the classifier (`domain_id`/`feature_id` are, and the url-guessing
  `deriveReviewArea` was deleted 2026-08-20), but a row he cannot open is still
  a row he cannot review.
- Filter your own backlog the way Arman does: `where domain_id = (select id from platform.taxonomy_node where slug='<domain>' and level='domain')`.
- UI lives at `matrx-frontend` `features/admin/agent-review/` (see its `FEATURE.md`). The table is deliberately minimal — do NOT add columns, RPCs, or satellite tables to it. Extend the versioned `metadata.triage` contract.
