---
name: rails-action-cable
description: "Use when designing, implementing, reviewing, testing, or operating Rails Action Cable/WebSocket connections, channels, subscriptions, streams, broadcasting, authorization, reconnect behavior, pub/sub adapters, realtime capacity, or cable security."
license: MIT
---

# Rails Action Cable & Realtime Engineering

## Purpose

Treat Action Cable as a realtime distributed boundary rather than another controller endpoint.

Action Cable introduces long-lived WebSocket connections, channel subscriptions, pub/sub broadcastings, client reconnect behavior, and a separate runtime/capacity profile from ordinary request-response Rails.

Core flow:

```text
connection authentication
-> subscription authorization
-> explicit channel identity
-> bounded stream
-> domain event/state change
-> broadcast contract
-> client delivery
-> reconnect/resubscribe
-> observable lifecycle
```

Rails documents Action Cable around connections, consumers, channels, subscriptions, streams, and broadcastings. Broadcastings are online/time-dependent rather than durable message queues; clients that are not subscribed when a broadcast is emitted do not receive that past broadcast.

## Activate when
- configuring or reviewing Solid Cable as the Action Cable pub/sub backend

- adding or changing `ApplicationCable::Connection`;
- adding or changing an Action Cable channel;
- implementing `subscribed`, `unsubscribed`, or channel actions;
- adding `stream_from`, `stream_for`, or `broadcast_to`;
- exposing realtime notifications, dashboards, collaboration, chat, presence, or live status;
- changing WebSocket authentication or authorization;
- configuring Action Cable adapters or Redis/pub/sub;
- diagnosing dropped connections, duplicate subscriptions, missed broadcasts, or reconnect storms;
- changing Action Cable deployment/process capacity;
- reviewing channel parameters, tenant isolation, or client-controlled stream names;
- testing Action Cable subscriptions/broadcasts;
- deciding whether data belongs in durable messaging instead of realtime delivery.

Do not activate merely because a normal controller emits JSON. Use `rails-api-integration` or ordinary Rails request skills unless a WebSocket/realtime boundary exists.

## Repository inspection

Inspect before changing realtime behavior:

1. Ruby/Rails version and Action Cable APIs available in that version;
2. `ApplicationCable::Connection` and connection identifiers;
3. `ApplicationCable::Channel` and existing channel hierarchy;
4. channel subscription parameters and authorization conventions;
5. current_user/current_account/tenant resolution;
6. cookie/session/token authentication used by WebSockets;
7. Action Cable URL, allowed origins, mount path, and environment configuration;
8. subscription adapter and Redis/pub/sub topology;
9. stream naming and `stream_from` / `stream_for` usage;
10. broadcast producers and event/state ownership;
11. client-side consumers/subscriptions and reconnect behavior;
12. queue/job/event sources that trigger broadcasts;
13. deployment process model, worker/web concurrency, memory, and Redis capacity;
14. logging, metrics, connection lifecycle telemetry, and incident diagnostics;
15. existing channel/system/integration tests;
16. fallback behavior when realtime delivery is unavailable.

Do not introduce a parallel realtime framework or custom WebSocket transport without repository evidence that Action Cable cannot satisfy the contract.

## Decision rules

1. Classify the change: connection authentication and lifecycle, channel/subscription authorization, streams and broadcasts, delivery and reconnect semantics, fan-out and capacity, adapter topology and failure, or security/operations/testing.
2. Load the matching reference below before changing behavior; any new channel or stream needs the authorization reference.
3. Keep connection authentication separate from per-channel/resource authorization, and re-authorize at subscription time.

## Critical invariants

- Authentication proves identity; it does not grant subscription access.
- Never let a client select a broadcast namespace that it could not otherwise authorize.
- Do not use Action Cable as a durable queue.
- Do not claim a single broadcast after reconnect repairs all missed state.
- When a message represents committed database state, coordinate the broadcast with transaction semantics.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another. Consult a listed pattern from the pattern catalog only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change alters connection identification, authentication, or connection lifecycle | [references/connections.md](references/connections.md) | Connection authentication; Connection lifecycle | `action-cable-connection-auth` |
| a change adds or alters a channel, subscription authorization, channel parameters, or client actions | [references/channels-and-authorization.md](references/channels-and-authorization.md) | Channel boundary; Subscription authorization; Channel parameters; Client actions | `action-cable-channel-authorization`, `action-cable-authorization-boundary` |
| a change names streams, shapes broadcast payloads, or broadcasts after state changes | [references/streams-and-broadcasts.md](references/streams-and-broadcasts.md) | Stream naming; Broadcast contract; Broadcasting after state changes | `action-cable-stream-contract`, `action-cable-broadcast-contract` |
| a change depends on delivery guarantees, missed messages, or client reconnect/resubscribe | [references/delivery-and-reconnect.md](references/delivery-and-reconnect.md) | Realtime is not durable delivery; Client reconnect and resubscribe | `action-cable-reconciliation` |
| a change alters broadcast fan-out, connection counts, adapter topology, or failure handling | [references/capacity-and-failure.md](references/capacity-and-failure.md) | Broadcast fan-out; Backpressure and overload; Realtime capacity model; Redis and adapter topology; Failure behavior | `action-cable-capacity`, `action-cable-failure-boundary` |
| a change has realtime security/privacy, deployment, observability, or test-strategy impact | [references/security-operations-testing.md](references/security-operations-testing.md) | Security and privacy; Operational lifecycle; Observability; Testing | `action-cable-testing` |

## Reference example

A channel that authorizes the subscription before streaming, and pairs an implicit resource stream with an explicit lifecycle stream.

```ruby
class RoomChannel < ApplicationCable::Channel
  def subscribed
    room = Room.find_by(id: params[:room_id])
    return reject unless room && current_user.member_of?(room)

    stream_for room                      # broadcast_to(room, ...) reaches these subscribers
    stream_from "room:#{room.id}:system" # explicit stream for join/leave lifecycle events
  end

  def unsubscribed
    StopPresenceTrackingJob.perform_later(current_user.id, params[:room_id])
  end
end

# Server-side broadcast after a state change (never trust the client to echo state):
# RoomBroadcastJob.perform_later(room)  ->  RoomChannel.broadcast_to(room, payload)
```

## Agent review checklist

- [ ] runtime/Action Cable version resolved
- [ ] connection authentication identified
- [ ] channel authorization identified
- [ ] tenant/resource ownership verified
- [ ] channel parameters validated
- [ ] stream names bounded and isolated
- [ ] broadcast payload contract explicit
- [ ] realtime versus durable semantics explicit
- [ ] reconnect/resubscribe behavior defined
- [ ] state reconciliation defined
- [ ] transaction/broadcast ordering reviewed
- [ ] client actions treated as API boundaries
- [ ] fan-out and payload size measured
- [ ] WebSocket capacity estimated
- [ ] Redis/adapter topology reviewed
- [ ] failure/degradation semantics explicit
- [ ] allowed origins/security reviewed
- [ ] deploy/restart lifecycle reviewed
- [ ] lifecycle/broadcast telemetry bounded
- [ ] deterministic tests cover auth, isolation, subscription, and broadcast behavior

## Anti-patterns / failure modes

- authentication without channel authorization;
- client-selected arbitrary stream names;
- blob/resource IDs treated as authorization;
- broadcasting private data to broad tenant/global streams;
- using Action Cable as a durable queue;
- assuming disconnected clients receive missed broadcasts;
- broadcasting entire Active Record objects;
- domain writes embedded directly in channel callbacks;
- broadcast before committed state;
- unbounded per-record broadcast callbacks;
- ignoring Redis/pub/sub capacity;
- testing against live Redis in every CI run;
- synchronized reconnect storms after deployment;
- logging secrets or sensitive payloads;
- using raw user IDs or stream names as unbounded telemetry labels;
- making optional realtime delivery a hidden database transaction dependency.

## Verification

For a realtime feature:

```text
connection auth
-> channel authorization
-> stream contract
-> broadcast contract
-> state/reconciliation semantics
-> focused Action Cable tests
-> capacity model
-> security checks
-> deploy/reconnect verification
-> regression suite
```

For production incidents verify whether failure occurred at:

```text
client
-> WebSocket connection
-> authentication
-> subscription
-> pub/sub adapter
-> broadcast producer
-> serialization
-> client consumer
```

Never claim realtime delivery, fan-out capacity, or reconnect safety without runtime evidence.

## Rails 8 current framework considerations

- Solid Cable provides a database-backed pub/sub option for Action Cable. Treat its retention, polling/pub/sub capacity, failure behavior, and deployment topology as runtime concerns.
- Preserve the same authorization, stream identity, reconciliation, and overload protections regardless of whether Redis or Solid Cable is the transport.

## Source foundation

Primary Rails guidance:

- https://guides.rubyonrails.org/action_cable_overview.html
- https://api.rubyonrails.org/classes/ActionCable.html
- https://api.rubyonrails.org/classes/ActionCable/Channel/Base.html

Composed repository skills:

- `rails-security` skill
- `rails-security-engineering` skill
- `rails-active-job` skill
- `rails-event-driven-messaging` skill
- `rails-distributed-systems` skill
- `rails-reliability-engineering` skill
- `rails-performance` skill
- `ruby-performance` skill
- `ruby-concurrency` skill
- `rails-production-runtime` skill
- `rails-release-engineering` skill
- `rails-observability` skill
- `rails-test-engineering` skill
- `rails-test-engineering` skill

## Rails Action Cable changes

For Action Cable/realtime changes:
- inspect ApplicationCable::Connection, channel hierarchy, subscription parameters, stream naming, broadcast producers, client reconnect behavior, adapter/Redis configuration, process topology, capacity, and tests before implementation;
- keep WebSocket connection authentication separate from per-channel/resource authorization;
- treat all channel parameters and client actions as untrusted API input;
- authorize subscriptions through the owning resource/tenant and never treat a blob/resource ID or stream name as authorization;
- use bounded deterministic stream names and prefer framework resource primitives such as stream_for/broadcast_to when appropriate;
- treat broadcast payloads as versioned wire contracts and avoid serializing entire Active Record objects or sensitive fields;
- do not use Action Cable as durable messaging; define reconnect/refetch reconciliation when missed broadcasts matter;
- coordinate broadcasts with committed state and use outbox/durable event infrastructure when delivery correctness requires it;
- size WebSocket connections, subscriptions, message rate, payload bytes, Redis/pubsub, memory, CPU, and reconnect bursts separately from HTTP capacity;
- define degraded behavior when Redis/Action Cable is unavailable rather than making optional realtime delivery an accidental transaction dependency;
- review allowed origins, credential/session lifetime, tenant isolation, secrets, and sensitive payloads;
- avoid synchronized reconnect storms during deploys and test connection/channel/broadcast behavior with deterministic local adapters;
- never claim realtime delivery or capacity without runtime evidence.

## Book cross-reference: *Modern Front-End Development for Rails*

Chapter 9 demonstrates Action Cable integration with Turbo Streams, Stimulus, and React. Use it to identify client integration options, but keep authorization, durable server state, reconnect behavior, delivery guarantees, and broadcast scope governed by this skill and the application's current protocol. A browser update must not become the source of truth for a domain state change.
