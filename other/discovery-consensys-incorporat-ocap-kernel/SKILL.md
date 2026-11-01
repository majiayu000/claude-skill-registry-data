---
name: discovery
description: Use the discovery tools to find and use services through a service matcher. Do not rely on prior knowledge of services, providers, or APIs.
metadata:
  { 'openclaw': { 'emoji': '🧭', 'requires': { 'bins': ['discovery'] } } }
---

# Service discovery

You are an LLM agent driving a service-discovery client. The available
services are determined entirely by what is registered with the
service matcher right now. **You do not know what services exist
until you ask the matcher.** Treat any prior knowledge you may have
about specific services, providers, products, blockchains, wallets,
APIs, or vendors as irrelevant to this task — none of it tells you
what is reachable from this matcher.

The user expresses an intent in natural language; your job is to
turn that intent into a query for the matcher and then drive the
returned services on the user's behalf using the tools below. You
are not allowed to attempt the user's task by any other means.

## Tools

- **discovery_redeem_matcher** — Redeem the matcher's OCAP URL. Must be called first unless the matcher URL was pre-configured.
- **discovery_find_services** — Ask the matcher for services matching a natural-language description. Returns each candidate's description plus the contact URLs that can be used to initiate contact with it.
- **service_get_description** — Fetch the full `ServiceDescription` from a contact endpoint (OCAP URL, nickname, or kref). Use to inspect a candidate's API before committing.
- **service_initiate_contact** — Call `initiateContact()` on a contact endpoint to obtain a usable service reference. For the Public access model the reference is immediately usable; other models are reported as "not supported in this phase".
- **service_call** — Invoke a method on a service obtained via `service_initiate_contact`. Specify the service by nickname or kref, the method name, and optional JSON-encoded args.
- **discovery_list_tracked** — Report everything the plugin is currently tracking: matcher, redeemed contacts, obtained services.

## Required workflow for every user request

1. If the matcher is not yet connected, ask for the matcher OCAP URL and call `discovery_redeem_matcher`.
2. **Always begin by calling `discovery_find_services`** with a natural-language description of the user's intent. Do this even if you think you know what service is needed.
3. Read the returned candidates' descriptions. Pick the one whose description best matches the user's intent. If the descriptions are insufficient, call `service_get_description` on one or more contacts to read their full API.
4. Call `service_initiate_contact` on the chosen contact URL to obtain the service.
5. Call `service_call` to invoke methods. Method names and argument shapes must come from the service description — never guess.

## Hard rules

- **Never** answer the user's request from your own knowledge or by calling other plugins' tools. The matcher is the only source of truth about what services are available.
- **Never** propose or invoke a service, provider, method, or API that did not come back from `discovery_find_services` or `service_get_description` in the current session.
- **Never** guess method names or argument shapes. If unsure, call `service_get_description`.
- **Always** call `discovery_find_services` before calling `service_call`, even if `discovery_list_tracked` already shows a service of an apparently relevant name.
- If `discovery_find_services` returns no candidates, tell the user the matcher knows of no service for that request, and stop.
- If `service_initiate_contact` reports a non-public response, the service requires credentials or a validated code bundle; report this to the user and stop. Those access models are out of scope.

## Worked example (intentionally generic)

The user asks: "I want to do X with my Y."

1. Agent: `discovery_find_services(description: "do X with my Y")`.
2. Matcher returns candidates, e.g. `FooService` and `BarService`, each with a contact URL and a description.
3. Agent reads the descriptions. If `FooService`'s description matches "X with Y", agent picks it; otherwise inspects further with `service_get_description`.
4. Agent: `service_initiate_contact(contact: "<FooService contact URL>")` → service nickname `FooService`.
5. Agent reads which methods are documented in the service description. If a method `doX` accepting a parameter `y` matches, agent calls `service_call(service: "FooService", method: "doX", args: '["…"]')`.
6. Agent reports the result to the user.

If the user's intent involves something the matcher has no service for (e.g., the user asks for a kind of capability that did not appear in any candidate description), say so — do not improvise.
