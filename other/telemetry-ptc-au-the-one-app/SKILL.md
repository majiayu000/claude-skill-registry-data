---
name: telemetry
description: Read when someone asks what's failing, slow or broken in their network, how long something took, what AI cost, or to read a trace; and before looking into a bug or a slow tool.
metadata:
  title: "Telemetry"
  subtitle: "What's slow, failing or costly"
  about: "Shows what's failing or slow in your network, and what AI costs, for the last 14 days. It keeps names and timings, never what anyone wrote."
  category: Developer tools
---

Telemetry keeps what the network's servers, clients and apps did: a span for each tool call, numbers such as how
long each tool took and what AI used, and warnings, errors and crashes. Each part records it with OpenTelemetry's own
SDK, and it's kept as OTLP, an hour of each signal a blob (`otlp/<day>/<hour>/` in its artifact), which any
OpenTelemetry tool reads as it is. It's kept in the network for 14 days, up to 256 MB, and nothing about it leaves. It holds no one's data: names, sizes, durations and outcomes, never what
anyone wrote, was given or answered. What a server recorded arrives here about a minute later.

The network's edge, where assistants, browsers and sharing links come in over the web, is in it too: a span for
each request it handled (`POST /mcp`, `relay forward`, `POST /sign-in/auth/oauth2/token`), on the
server `edge`, with its route, status, duration, the server it was passed to and why it failed, even when it never
reached a server. A call that reached one is one trace with the server's span, and with the client's when the
client sent a `traceparent`. While none of the network's servers answers it, the edge keeps that too, once one does:
a span `network unreachable` from the first request none answered to the first a server answered, so an outage
nothing on a server saw is in `errors` and in `alerts` (a resolved `server` alert, past 5 minutes) with its own times.

- `overview` is what Telemetry's app shows: what's failing, what's slowest and what AI cost, over
  the last `hours` (24 if left out, up to 336).
- `errors` lists each kind of error once: where (a span's name, as `<app> <tool>`, or `<method> <route>` for the edge's, or what logged it, with
  the servers it was logged on), its message, how often, when it was first and last, how long it lasted, how often in each minute it
  happened in (`minutes`, a burst's timing, from the 14 days kept), and the trace of the newest. A kind is its message with numbers, ids and its stack left out, so one cause is one kind. A call refused
  for what it was given or who asked is the caller's mistake, not an error: its `one.tool.duration` outcome is
  `refused`, not `error`, and it doesn't count as a failure; so is one a tool refused itself (`OneCore.Call.Refused`),
  for what it was given or for a device that's off. Start a bug there. Each says where it's `from`: the server or the
  edge it happened on, or what a client reported says which ("App on Andre's iPhone", "claude-code (MCP) on linux"): its requests that
  failed or were slow, as MCP names them (`tools/call gmail_search`), whose trace runs on into the server's span;
  how long no server answered it (`one.client.unanswered`); what its window showed went wrong
  (`one.client.problem`), an app that never opened (`one.client.open`), a sign-in that failed (`one.client.join`),
  an app's page's error (`<app> page`) and a crash (`exception`). A client keeps them while it can't reach a
  server, and tells one once it can.
- `trace` reads one trace whole by its `id`, across every server it went through: each span's depth, server,
  start and duration in milliseconds, outcome, message and events. A call that one server passed to another is
  one trace, the other server's span under the first's.
- `slowest` lists tools by their 95th percentile, with their calls, failures and 50th and 99th percentiles in
  milliseconds, then how long each app took to open, from a tap to its first drawing.
- `metric` gives one metric over time, per step, as its count, sum and quantiles, of the data with the
  `attributes` given: `one.tool.duration` with `{"one.app": "backups", "one.tool": "now"}`, say. With no
  `name` it lists every metric there is, with its attributes.
- `spending` gives the tokens AI models took in and gave out, as apps record them, per model per day, and what they cost where the endpoint says
  (OpenRouter does). It has no prices of its own.
- Each server's machine reports its server's life, through `one serve run`, even while the server can't start, and
  keeps it until a server is told: `one.server.start` (how long it took, `one.server.restart.reason` why the run
  before ended, an error where it didn't start, with its last lines), `one.server.stop` (an error where nobody
  asked), `one.server.crash_loop` and `one.server.update` (`one.update.outcome`: `took`,
  `went_back` or `stayed`, with why). Each says `one.server`, the server's key. The network's update is
  `network update` on the edge, an error while a server is behind it. A database's lease moving to a server is
  `one.database.lease.moves` (`one.reason`), a call kept waiting by its holder `one.database.lease.wait`
  (`one.outcome` `not_answered`, warned of, or `gone`), and an app not answering a hook in time
  `one.hook.timeouts`, each by `one.app`.
- Telemetry keeps what needs a person as alerts, and tells no one: a server not running or restarting over and over, no server answering the edge,
  a server the network's update left behind or an edge that couldn't update itself, a kind of error not seen in 14 days, an app's tools failing, an app not answering, an app's
  deploys slow to show in its window (over 500 ms, `one.client.deploy.window`), a server that acts for someone unable to
  open what's encrypted for them, or one that doesn't able to (`one.encryption.access`). `alerts`
  lists them, the open ones and those resolved in the last `hours` (a day if not said), and each kind with what fires it; they're on
  Telemetry's screen, its widget and its badge too. A problem is one alert however long it lasts. Whoever wants
  them elsewhere has everything kept forwarded (`forward`).
- `forward` sends a copy of everything kept from then on to an OpenTelemetry endpoint the network's owner names
  (Grafana Cloud, Honeycomb, a collector of their own), as OTLP over HTTP, with the headers it wants filled in from
  a Vault item of theirs switched on for Telemetry; with no endpoint it stops. It's off until then.
- Whose a call was is shown to the network's owners, and to whoever it was: to anyone else, how the network is
  doing is open, and who did what isn't.

- An app that runs in the server's VM records more of its call with OpenTelemetry's API, as any Elixir library does
  (`OpenTelemetry.Tracer`, `OpenTelemetryAPIExperimental.Histogram`, `Logger` for warnings and errors), and the
  server's SDK exports it with the rest. An untrusted app, in a VM of its own, uses `record`:
  `OneCore.Call.tool(call, "telemetry", "record", %{"records" => records})`, where Telemetry is added
  (`OneCore.Call.apps/1`). Each record has a `name`, in OpenTelemetry's dotted lowercase and following its
  conventions where it has some (`gen_ai.client.token.usage`), and `attributes`: names, sizes and outcomes, never
  what anyone wrote, was given or answered, and never a secret. With a `value` it's a number, a histogram's by its
  name and attributes, read back with `metric`; with `took`, in milliseconds, it's
  something that ended now, a span under the call, with an `error` if it failed; and otherwise a log line of the
  call, read in its trace, and an error if it has one.
