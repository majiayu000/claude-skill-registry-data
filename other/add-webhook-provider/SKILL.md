---
name: add-webhook-provider
description: Accept webhooks from a new third party (a payment, email, SMS or other provider calling us) in apps/webhooks, verified and processed from a queue. Use when a provider needs to notify the product of events.
argument-hint: <provider>
---

# Add an inbound webhook provider

Inbound webhooks follow one shape (`apps/webhooks/src/inbound/stripe.routes.ts` and
`stalwart.routes.ts` are the references): verify on the raw body, store once, emit a
domain event in the same transaction, answer at once, and do the work from a queue.

1. **Secret.** `<PROVIDER>_WEBHOOK_SECRET` in `apps/webhooks/src/env.ts`, optional (the
   route answers 404 until it's set), plus `.env.example`, `docs/environment.md` and the
   webhooks Secret (the add-env-var skill). Accept a comma-separated list if the provider
   supports rotating secrets.
2. **Pure part.** `src/inbound/<provider>-events.ts`: the payload's zod schema, signature
   check with `timingSafeEqual`, freshness (a timestamp window, against replays), and the
   key that identifies an event once (the provider's id, or a hash of its content when
   ids aren't stable). Unit-test it against real payloads from the provider's docs
   (`<provider>-events.test.ts`, like `stalwart-events.test.ts`).
3. **Route.** `src/inbound/<provider>.routes.ts` with `mount<Provider>(fastify, database,
   secret)`: a raw-body content-type parser scoped to the route, the checks above, then
   one transaction that inserts into `webhooks.inbound_event` (unique on `provider` and
   `providerEventId`, so a retry is a no-op) and `emitEvent(tx, "<provider>.event_received.v1", ...)`.
   Mount it in `src/server.ts`.
4. **Event.** Declare `<provider>.event_received.v1` in `packages/contracts/src/events.ts`
   (additive), its audit label `workspace.audit.events.<provider>.event_received.v1` in
   every catalog, and a
   route to its consumer in `eventSubscribers` (`packages/jobs/src/queues.ts`).
5. **Consumer.** In the service that owns the effect (as billing consumes Stripe's
   events in apps/api): idempotent, `parseJob` first (the add-job skill).
6. **Reachability.** `/webhooks` already routes to the service
   (`deploy/charts/stack/values.yaml`); a provider calling from inside the cluster needs
   its namespace in `allowFromNamespaces`. Register the endpoint URL
   (`https://<site>/webhooks/<provider>`) at the provider, and add that step to
   `docs/new-project.md`.
7. **Tests.** `apps/webhooks/test/webhooks.integration.test.ts`: a signed request is
   stored once and emits its event, a bad signature and a stale one are refused, a
   retried delivery is harmless. The consumer's own integration test for its effect.

## Done when

- `bun run test` and `bun run test:integration` pass.
- The `security-reviewer` agent (a new unauthenticated entry point) and the `reviewer`
  agent report nothing blocking.
