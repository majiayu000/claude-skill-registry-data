---
name: rails-external-stream-ingestion
description: Use when a Rails/Ruby application consumes an external streaming feed — broker or market-data WebSocket clients, tick/event streams, provider callbacks, reconnection and resubscription, feed freshness, and inbound backpressure — rather than serving Rails Action Cable broadcasts.
license: MIT
---

# External Stream Ingestion Engineering

## Purpose

Treat an external streaming feed as an owned, failure-prone integration boundary, not as a callback you wire up and forget.

A robust feed consumer makes connection ownership, subscription state, buffering bounds, event ordering, duplicate handling, data freshness, and unavailable-feed behavior explicit. The provider decides when to disconnect, throttle, or redeliver; the application decides what it does about it.

Core flow:

```
identify the feed contract
-> own the connection lifecycle
-> buffer inbound events with bounds
-> validate and normalize each event
-> maintain freshness and subscription state
-> decide failure semantics when data is unavailable
-> hand normalized events to downstream processing
-> test recovery deterministically with a fake client
```

Compose this skill with:

- ruby-concurrency for thread-safe state and bounded queues;
- rails-caching for freshness-sensitive cache entries;
- rails-reliability-engineering for circuit breakers and degradation budgets;
- rails-api-integration for the same provider's request/response contracts;
- rails-observability for feed telemetry and alerting;
- rails-production-runtime for supervised long-running daemons;
- rails-test-engineering for deterministic stream tests.

This skill owns the consuming side. Rails Action Cable owns the serving side (browser subscriptions over Rails' own transport); consuming a broker feed is a different boundary with different failure modes — an Action Cable channel that happens to receive forwarded ticks does not make the feed contract Action Cable's problem.

## Activate when

- consuming an external WebSocket, Server-Sent Events, or streaming feed from a provider SDK or raw client;
- implementing reconnection, heartbeat handling, or resubscription after a drop;
- receiving provider callbacks for market data, telemetry, notifications, or chat streams;
- normalizing, validating, or time-stamping inbound stream events;
- detecting stale feeds, missing events, or gaps after reconnect;
- bounding memory or CPU consumed by inbound event bursts;
- deciding whether a feature stops, degrades, alerts, or rejects work when its feed is unavailable;
- moving ingested events into caches, jobs, or database state;
- testing feed consumers without a live external connection.

Do not activate merely because the application serves realtime updates to browsers — that is the Action Cable boundary. Do not use this skill for background job processing; rails-active-job owns queue execution. Activate here when the inbound external stream itself is the integration boundary.

## Repository inspection

Inspect:

1. Ruby/Rails/runtime versions and the thread/process model of the consuming process;
2. the feed provider's client library: its threading model, callback registration, and error surfaces;
3. the wire contract: event types, subscription messages, heartbeat/ping frames, sequence or offset fields;
4. documented and observed disconnect behavior: who closes, why, and what the provider redelivers;
5. reconnection support already present (built-in retry, resume tokens, session identifiers);
6. where connection state lives: one shared connection, per-process, per-thread, or per-worker;
7. subscription registry shape: which instruments/channels/topics are subscribed and by whom;
8. inbound buffering: queue type, bounds, overflow behavior, and where events wait;
9. freshness requirements of each consumer: maximum acceptable staleness per use;
10. the cache layer between the stream and readers, and its invalidation rules;
11. shutdown behavior: how the process drains or abandons in-flight events;
12. existing tests and fakes for the feed client, and how disconnects are simulated;
13. observability: connection state, event rates, lag, and gap metrics already emitted.

Do not assume the provider's SDK is thread-safe, that events arrive in order, that a heartbeat implies data freshness, or that a reconnect resumes exactly where the connection dropped. Verify each assumption against the provider contract and the repository's own logs before relying on it.

## Decision rules

1. Classify the change: connection lifecycle; buffering, ordering, and backpressure; freshness and recovery; state, subscriptions, and testing. Load the matching reference below before changing that boundary.
2. Name one owner for the connection. If two objects can reconnect the same socket, reconnect logic will race.
3. Decide, per consumer, the failure semantic before writing recovery code: stop, degrade, alert, or reject. A feed consumer without an explicit unavailable-data behavior is unfinished.
4. Bound every buffer a burst can fill, and make overflow behavior explicit (drop-oldest, reject-new, or block) with a measurement that says which one is safe.
5. Separate event time from processing time the moment an event arrives; downstream code must never have to guess which clock a timestamp came from.
6. Route external events through one normalization seam so validation, deduplication, and time-stamping happen exactly once per event.

## Critical invariants

- Never let a feed callback block on the network or the database; callbacks enqueue, workers process.
- Never grow an unbounded in-memory buffer because the provider outpaces the consumer.
- Do not treat a live connection as proof of fresh data; a silent feed can be an empty subscription, a stalled upstream, or a heartbeat without payload.
- Do not let a reconnect silently reset sequence, subscription, or session state without reconciling what was missed.
- A consumer that acts on stale data as if it were current must be treated as a correctness bug, not a performance nuance.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change owns, starts, stops, supervises, heartbeats, reconnects, or resubscribes a feed connection | [references/connection-lifecycle.md](references/connection-lifecycle.md) | Connection ownership; Startup and supervision; Heartbeats; Reconnect and resubscribe; Shutdown | `external-api-client` |
| a change alters inbound queues, bounds, burst behavior, event ordering, duplicate handling, or the hand-off to downstream processing | [references/buffering-and-ordering.md](references/buffering-and-ordering.md) | Bounded buffering; Backpressure; Burst handling; Ordering and duplicates; Downstream hand-off | `message-handler-boundary` |
| a change adds or alters staleness detection, missing-event handling, timestamps, gap recovery, or the behavior when data is unavailable | [references/freshness-and-recovery.md](references/freshness-and-recovery.md) | Freshness contract; Stale-feed detection; Missing events and gaps; Event time versus processing time; Failure semantics | `broker-capacity` |
| a change touches subscription registry state, cache consistency, thread-safe feed state, or the tests and fakes for any of the above | [references/state-and-testing.md](references/state-and-testing.md) | Subscription state; Thread-safe registry; Cache consistency; Deterministic fake-client tests | `message-observability` |

## Reference example

A supervised consumer whose callbacks only enqueue, whose buffer is bounded, and whose reconnect re-establishes subscriptions explicitly:

```ruby
# app/feeds/market_feed_consumer.rb
#
# The client is injected so tests can pass a fake. Callbacks never do
# business work: they validate, time-stamp, and enqueue.
class MarketFeedConsumer
  HEARTBEAT_TIMEOUT = 15 # seconds; must be shorter than the provider's idle drop
  BUFFER_BOUND = 10_000   # bounded: burst beyond this drops oldest with a metric

  def initialize(client:, buffer:, logger: Rails.logger)
    @client = client
    @buffer = buffer
    @logger = logger
    @subscriptions = []
    @last_event_at = nil
  end

  def subscribe(instrument)
    @subscriptions << instrument
    @client.subscribe(instrument)
  end

  def start
    install_callbacks
    @client.connect
    self
  end

  def stop
    @client.close            # provider gets a clean close, not a TCP drop
    @buffer.clear
  end

  def stale?(now: Time.now)
    @last_event_at.nil? || (now - @last_event_at) > HEARTBEAT_TIMEOUT
  end

  private

  def install_callbacks
    @client.on_tick do |payload|
      @last_event_at = Time.now
      event = normalize(payload) or next
      @buffer << event        # bounded queue; overflow policy decided here
    end
    @client.on_disconnect { ReconnectJob.perform_later(self.class.name) }
  end

  def normalize(payload)
    return nil unless payload["token"] && payload["price"]
    return nil if @buffer.seen?(payload["token"]) # provider may redeliver

    {
      "token" => payload["token"],
      "price" => BigDecimal(payload["price"]),
      "event_time" => Time.at(payload["ts"]),   # event time, not arrival time
      "received_at" => @last_event_at
    }
  end
end
```

`ReconnectJob` re-enters through `subscribe` for each saved instrument: resubscription is explicit, never assumed.

## Agent review checklist

- [ ] single named owner for the connection and its lifecycle
- [ ] reconnect path re-establishes subscriptions and session/sequence state explicitly
- [ ] heartbeat or keepalive interval documented against the provider's idle-drop window
- [ ] every buffer the stream can fill is bounded, with chosen overflow behavior
- [ ] burst behavior measured or bounded, not hoped for
- [ ] event ordering assumptions stated and verified against the provider contract
- [ ] duplicate delivery handled by a stable event identity, not by arrival count
- [ ] event time and processing time separated at the seam
- [ ] staleness contract per consumer made explicit (max acceptable age)
- [ ] gap detection present where events are countable or sequenced
- [ ] failure semantics chosen: stop, degrade, alert, or reject — and implemented
- [ ] no feed callback blocks on network, database, or file I/O
- [ ] subscription registry thread-safe under the actual threading model
- [ ] cache reads can never mistake stale feed data for current data
- [ ] deterministic fake-client tests cover disconnect, reconnect, redelivery, and burst
- [ ] feed telemetry observable: state, rate, lag, and drops

## Anti-patterns

- doing database work inside a provider callback thread;
- unbounded arrays or hashes as event buffers;
- relying on `rescue` inside a callback as a connection strategy;
- assuming SDK client objects are thread-safe because callbacks are threaded;
- treating a connected socket as a freshness guarantee;
- reconnecting without resubscribing, then debugging "missing data" as a provider outage;
- discarding timestamps from the provider and substituting local clock time;
- silently swapping last-known values for missing values;
- one process sharing a mutable subscription set with no synchronization;
- testing feed logic only against a live provider;
- blocking the read loop on a slow downstream consumer;
- letting every service in the application open its own connection to the same provider;
- caching stream-derived values with no expiry or invalidation rule.

## Verification

For the connection lifecycle:

`start -> subscribe -> heartbeat -> forced disconnect -> reconnect -> resubscribe -> events resume`

For buffering:

`sustained rate -> burst beyond bound -> overflow behavior observed -> downstream keeps processing`

For freshness:

`last event time -> staleness threshold -> degraded state -> alert or rejection -> recovery after new events`

For recovery:

`gap detected -> missing range identified -> backfill or reconciliation triggered -> duplicate suppression holds`

Report connection ownership, buffer bounds and overflow choice, ordering assumptions, freshness contract, failure semantics, and the disconnect/reconnect test evidence.

## Source foundation

- Ruby Queue and SizedQueue: https://docs.ruby-lang.org/en/master/Thread.html#Queue
- Ruby Thread and Mutex: https://docs.ruby-lang.org/en/master/Thread.html
- Rails Testing Applications: https://guides.rubyonrails.org/testing.html
- Rails Active Support instrumentation: https://guides.rubyonrails.org/active_support_instrumentation.html
- Repository skills: ruby-concurrency, rails-caching, rails-reliability-engineering, rails-api-integration, rails-observability, rails-production-runtime, rails-test-engineering, rails-action-cable

## External stream ingestion changes

For external feed, stream, and inbound realtime data changes:

- name the single owner of the connection and its lifecycle before touching callbacks;
- resolve the provider's actual guarantees for ordering, redelivery, heartbeats, and session resume from its contract and code, not from assumptions;
- keep callbacks free of blocking work: validate, normalize, time-stamp, and enqueue only;
- bound every inbound buffer and choose overflow behavior deliberately;
- separate event time from processing time at the normalization seam;
- make per-consumer staleness contracts explicit and enforce them where stale data is consumed;
- detect gaps where the feed is sequenced, and reconcile after reconnect instead of silently continuing;
- choose and implement the unavailable-data semantic — stop, degrade, alert, or reject — per consumer;
- keep subscription state thread-safe under the real threading model of the client;
- keep cache entries derived from the stream invalidated by staleness rules, not by hope;
- instrument connection state, event rate, buffer depth, and drops without logging payloads;
- test disconnects, reconnects, redelivery, bursts, and stale feeds with deterministic fakes, never against a live provider.
