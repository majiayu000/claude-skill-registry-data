---
name: add-tracked-event
description: Adds or changes an analytics event end to end, keeping the taxonomy, the typed schema, the code and the docs in sync. Use whenever a new event is needed or an existing one changes.
---

# Add a tracked event

1. Confirm the event is needed for the funnel or a guardrail in `docs/ANALYTICS.md` (draft taxonomy in
   `docs/PLAN.md` until Stage 6). If it is not, stop and say why.
2. Name it `object_action` in snake case. Decide where it is captured: the server for anything that confirms an
   outcome (conversion, profile update), the relay for interface events.
3. Add it to the shared event schema with typed properties. Properties are enums, booleans, numbers or opaque
   ids; never email, name or free text. Values read from the DOM must pass the schema.
4. Fire it from exactly one place. Server events fire only after the database write commits.
5. Add a test that fails if the event is not fired, and one that fails if a property outside the schema is sent.
6. Update the taxonomy table in `docs/ANALYTICS.md` in the same commit: name, trigger, where it is captured,
   properties.
7. Run the `analytics-auditor` agent and include its verdict in the stage report.
