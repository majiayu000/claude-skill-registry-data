---
name: nak-inspect-thread
description: Dump a nak conversation thread for debugging - messages in order plus the thread row's cached priming payloads (intuition, context-recall) with human-readable ages and staleness flags. Use when investigating why a turn answered oddly, responded to an old message, or got mis-primed; or any "what does this thread actually look like in the DB" question. Works against the cloud project (Supabase MCP) or the local dev stack (mise run dev-sql).
---

# Inspect a nak thread

A thread's behaviour is the product of its message history AND the cached
priming payloads on its `threads` row (`intuition_payload`,
`context_recall_payload`). When a turn answers the wrong thing, the cause
is usually in one of those two places. This skill pulls both in a fixed
shape so the diagnosis is one step, not four ad-hoc queries.

Background on the priming staleness failure mode it surfaces:
[`docs/dev/intuition.md`](../../../docs/dev/intuition.md) and
[`docs/dev/context-recall.md`](../../../docs/dev/context-recall.md).

## Inputs

- A **thread id** (uuid). If you only have a user, list recent threads
  first (query C below).
- A **target**: cloud or local. Pick the runner accordingly.

## Runners

- **Cloud** (the linked project): `mcp__claude_ai_Supabase__execute_sql`
  with `project_id` = the `nak` project (resolve via
  `mcp__claude_ai_Supabase__list_projects` if unknown). The MCP runs with
  management access, so the `auth` schema is queryable.
- **Local** (a running `mise run dev-start` stack): `mise run dev-sql
  "<sql>"`. The MCP/cloud tools cannot see the local stack; this is the
  only way in. Loopback-guarded.

Run the same SQL either way. Substitute `:tid` with the thread id.

## A. Messages in order

```sql
select row_number() over (order by created_at) as turn,
       role, status, model, created_at,
       left(regexp_replace(coalesce(content,''), E'[\n\r]+', ' ', 'g'), 140) as snippet,
       (tool_calls is not null) as has_tool_calls, name
from public.messages
where thread_id = ':tid'
order by created_at asc;
```

Read it as the transcript the model accumulates. Watch for: the last
`role='user'` row (what the turn was actually answering), `tool` rows
(web_search/update_title/etc.), and any `status` of `error` / `aborted`
/ `suspended_for_ask_user`.

## B. Priming payloads with age + staleness

```sql
select
  t.title,
  (select count(*) from public.messages m
     where m.thread_id = t.id and m.role = 'user') as user_rounds,
  -- intuition
  t.intuition_payload->>'trigger'           as intu_trigger,
  (t.intuition_payload->>'computed_at_round')::int as intu_round,
  round(extract(epoch from now()
    - to_timestamp((t.intuition_payload->>'computed_at_at')::bigint / 1000)) / 60.0)::int
                                            as intu_age_min,
  -- context-recall
  t.context_recall_payload->>'trigger'      as recall_trigger,
  (t.context_recall_payload->>'computed_at_round')::int as recall_round,
  round(extract(epoch from now()
    - to_timestamp((t.context_recall_payload->>'computed_at_at')::bigint / 1000)) / 60.0)::int
                                            as recall_age_min
from public.threads t
where t.id = ':tid';
```

### Interpreting staleness

A cached payload is injected into the wire as a `<think>` block every
round. Two fuses force a refresh (see `STALE_FUSE_ROUNDS` /
`STALE_FUSE_MS` in `src/lib/intuition`):

- **Wall-clock**: `age_min >= 60`. At/over an hour the chat-loop's
  injection guard SUPPRESSES the payload (won't steer on it) and the next
  turn recomputes. An age in the hundreds/thousands on a payload that
  still drove a turn is the classic "answered a stale situation" bug -
  but note the guard now prevents injection, so on current code a stale
  payload should be suppressed, not injected.
- **Rounds**: `user_rounds - <payload>_round >= 8`. Drift within a
  session; forces a refresh on the next turn regardless of age.

Flag a payload as suspect when `intu_age_min` / `recall_age_min` is large
(tens of minutes climbing toward 60+) or when the round gap is near/over
8 - especially if the thread shows a topic shift the mood trigger
wouldn't have caught.

To read the actual injected text, add
`t.intuition_payload->>'synthesis'` and
`left(t.context_recall_payload->>'note', 400)` to the select.

## C. Find a thread when you only have a user

Local dev user is `dev@nak.local`. Cloud: use the real address.

```sql
select id, title, updated_at,
       intuition_payload is not null  as has_intuition,
       context_recall_payload is not null as has_recall
from public.threads
where user_id = (select id from auth.users where email = ':email')
order by updated_at desc
limit 10;
```

## Output

Summarise: the last user turn vs what the response addressed; any
error/aborted/suspended rows; and any priming payload whose age or round
gap makes it a staleness suspect. Quote the offending `synthesis` / `note`
when one looks like the culprit. Don't dump raw rows back wholesale -
relay the diagnosis.
