---
name: integration-brief
description: Use after changing an API endpoint, contract, event, or message schema that another person or team will integrate with. Produces a short brief the integrating developer (frontend, mobile, another service) can implement from directly.
---

# Integration Brief

Goal: the person on the other side of the contract should be able to
integrate without reading your code or asking you what changed.

Write the brief whenever a task touched an integration surface: REST/GraphQL
endpoints, request/response shapes, events, queues, message schemas, shared
types, error contracts, auth requirements.

## Steps

1. **Identify the audience.**
   Who integrates with this? (mobile app, frontend, another backend team.)
   Write for them: they know their side, not yours.

2. **Write the brief** to `docs/briefs/<slug>.md` using
   `templates/integration-brief.md`. It must contain:

   - **What changed and why** — two or three sentences.
   - **The contract, before → after** — exact endpoints, methods, field
     names, types. Mark what is new, changed, and removed.
   - **A real example** — an actual request and response (or event
     payload), copy-paste ready. Not pseudocode.
   - **Errors and edge cases** — what failure responses look like, what is
     nullable, what limits apply.
   - **Migration notes** — is the old shape still accepted? Until when?
     What breaks if they do nothing?
   - **Open questions** — anything the integrating team must decide.

3. **Keep it honest.**
   Everything in the brief is verified against the actual implementation —
   copy the example from a real call you made, not from memory.

4. **Announce it.**
   In your Done report, include: `Brief: docs/briefs/<slug>.md — hand this
   to the <mobile/frontend/...> developer.`

## Do not

- Do not describe your internal implementation. The brief is the contract,
  not the code tour.
- Do not write "see the code for details". The brief's entire job is that
  they don't have to.
- Do not skip the brief because the change "is small". A renamed field
  breaks the other side just as hard as a redesign.
