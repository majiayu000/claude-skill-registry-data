---
name: turbo-streams-patterns
description: Build targeted Turbo Streams correctly — model broadcasts over Action Cable, custom stream actions, authorized stream channels, and Kredis presence. Use when adding real-time/live updates (chat append, replace a card, toggle a class), writing a custom turbo-stream action, securing who can subscribe to a record's broadcasts, or debugging a stream that does nothing / a custom action that's ignored / broadcasts leaking to the wrong user. The surgical complement to the morph page-refresh model (see turbo-morphing).
---

# Targeted Turbo Streams

Surgical DOM updates: broadcast/render specific `<turbo-stream>` actions against
specific ids. Use this when you need precision (append a chat message, replace one
card, move a class); use **`turbo-morphing`** when a whole-page refresh-with-morph is
simpler. Full patterns: [`references/turbo-streams-guide.md`](references/turbo-streams-guide.md).

## When to use

- Live updates: model change → broadcast a partial to subscribers.
- A custom stream action Turbo doesn't ship (e.g. `switch_class`).
- A record's broadcasts are **private** — only authorized users may subscribe.
- Debugging: a stream that does nothing, a custom action the client ignores, or
  broadcasts arriving for the wrong user.

## Patterns (and their footguns)

1. **Model broadcast**: `after_create -> { broadcast_append_later_to parent, target:,
   partial: }`. The `_later` variants enqueue a job — **need an Active Job backend**.
   View subscribes with `turbo_stream_from parent, channel: "FooChannel"`.

2. **Authorize the stream** (security): `turbo_stream_from` only *signs* the stream
   name — it does NOT prove this user may receive that record's broadcasts. Use a
   custom channel that authorizes and `reject`s otherwise
   (`templates/authorized_channel.rb.tmpl`). The default `Turbo::StreamsChannel`
   streams from any signed name with no per-record check → eavesdropping risk.

3. **Custom stream action** = two halves that MUST match: a JS `StreamActions.X` and a
   Ruby helper registered via `Turbo::Streams::TagBuilder.prepend`
   (`templates/custom_stream_action*.tmpl`). One side alone fails silently.

4. **Stream tags inside a frame response**: to patch an element *outside* the frame
   you're rendering into, embed `turbo_stream.*` tags in the frame's HTML — no
   separate `*.turbo_stream.erb` needed.

5. **Kredis presence**: a `kredis_set` of online users (maintained in the channel's
   `subscribed`/`unsubscribed`) decides live-append vs also notifying/emailing.

## Lint an app

```bash
scripts/lint_turbo_streams.sh path/to/rails-app
```

Flags: custom stream actions wired on only one side; **channels that `stream_from`
without authorizing the subscriber** (broadcast eavesdropping — reported as an error);
`broadcast_*_later` without a job backend; and (response-stream path) a `*.turbo_stream.erb`
template whose literal slash-pathed `partial:` resolves to no file (→ `MissingTemplate`
when that stream renders) or a custom `turbo_stream.<action>` with no client-side
`StreamActions.<action>`. Heuristic grep scan (names its ceiling — bare/dynamic partials
and target-id existence aren't resolved). Verified: clean on the Piazza app and on a real
response-template app (miela_app, 14 templates), flags a synthetic leaky-channel +
half-wired + dangling-partial app.
