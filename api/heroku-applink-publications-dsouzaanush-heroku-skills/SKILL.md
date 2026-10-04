---
name: heroku-applink-publications
description: Publish Heroku apps into Salesforce and Agentforce with Heroku AppLink. Use when the agent needs AppLink publication workflows, OpenAPI publication preparation, publish a Heroku app to Salesforce, review AppLink publication state, inspect shared publication endpoints or shared objects, or reason about Agentforce, Flow, Apex, Data Cloud, service mesh, and AppLink user-mode behavior.
---

# Heroku AppLink Publications

Publish Heroku apps to Salesforce through AppLink with careful attention to publication workflows, OpenAPI, shared publication endpoints, user modes, and org targeting.

## Start with publication prerequisites

Before publishing:

- confirm the app already has an AppLink add-on
- confirm the relevant Salesforce org is connected
- review the OpenAPI spec and any metadata directory
- confirm whether the target is Salesforce Flow, Apex, Data Action Targets, Agentforce, or a combination
- confirm which shared publication endpoints or shared objects will be exposed

## Preferred publish flow

1. inspect existing publications with `heroku salesforce:publications -a <app>`
2. confirm the intended connection name and client name
3. review the OpenAPI 3.0 spec for action shape, permissions, and Agentforce-specific behavior
4. publish with `heroku salesforce:publish <API_SPEC_FILE_DIR> -a <app> --connection-name <connection> -c <client-name>`
5. verify the resulting publication in Salesforce, API Catalog, and the AppLink dashboard

## OpenAPI and Agentforce guidance

- Use OpenAPI 3.0.
- Keep permission boundaries explicit in the spec and Salesforce-side configuration.
- Treat Agentforce actions as publication outputs, not as a substitute for connection setup.
- Be aware that Salesforce Spring '26 changed connected-app creation behavior for `heroku salesforce:publish`.

## Security and runtime guidance

- AppLink uses a service mesh in front of the app to validate inbound requests.
- Choose user modes intentionally: `user`, `user-plus`, or `authorized-user`.
- Only connected orgs can invoke published apps.

## Guardrails

Ask for confirmation before:

- publishing to a production org
- changing the API contract of an already-published app
- enabling permissions or connected-app behavior that broadens data access

## References

- Read `references/applink-publications.md` for publish commands, OpenAPI notes, and source links.
