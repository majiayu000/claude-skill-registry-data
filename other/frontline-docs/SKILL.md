---
name: frontline-docs
description: >
    Where to find official Frontline documentation and how to use it.
    Two sites: docs.getfrontline.ai (REST API and CLI reference) and
    help.getfrontline.ai (UI walkthroughs and general app usage). Use when the
    user asks where to learn something, or when no other skill covers the
    question and you need to look up a behavior. Always check the other
    Frontline skills first — they are the authoritative source for anything
    they cover.
allowed-tools: WebFetch
---

# Frontline Documentation

Frontline maintains two public documentation sites. Each has a clear scope —
use the table below to decide which one to point a user at, or to fetch from
yourself when a skill doesn't have the answer.

| Site                                                     | Covers                                                                                      | Pick this when…                                                                                                                                     |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **[docs.getfrontline.ai](https://docs.getfrontline.ai)** | REST Public API (concepts + reference) and the `frontline` / `max` CLI (command reference). | The user is building an integration, hitting endpoints, scripting with the CLI, or asking about API behavior, rate limits, auth, schemas, payloads. |
| **[help.getfrontline.ai](https://help.getfrontline.ai)** | The Frontline web app: setup, channels, agents UI, billing, troubleshooting end-user flows. | The user is asking how to do something **in the app**, where a setting lives, how to set up a channel, configure WhatsApp, invite teammates, etc.   |

## How to decide between skill, link, and fetch

Apply the rules in order:

1. **A Frontline skill covers the topic** → use the skill. Skills are the
   source of truth for API, CLI, CRM behavior, flows, workflows, agents,
   tables, objects, relations, and the built-in CRM objects' automations.
   **Do not** open the docs to re-derive what a skill already documents.
2. **The user explicitly asks where to learn / read about something** → reply
   with the matching site link (and a deep link if you know one). You don't
   need to fetch — just point.
3. **No skill covers the question and you need the answer to keep going**
   (for example, a UI flow, a billing detail, or a non-CLI feature) →
   `WebFetch` the relevant page on the right site, then summarize.

If you can answer something from a skill but also reference a doc URL for
the user, do both: act using the skill, mention the link for further reading.

## Sections on `docs.getfrontline.ai`

The site has three top-level tabs. Useful entry points:

- **Docs** — concepts and getting started (the tab is labeled "Docs", URL still uses `/api/`)
    - `https://docs.getfrontline.ai/docs` — overview
    - `https://docs.getfrontline.ai/docs/getting-started`
    - `https://docs.getfrontline.ai/docs/authentication`
    - `https://docs.getfrontline.ai/docs/rate-limits`
    - `https://docs.getfrontline.ai/docs/errors`
    - Concept pages (nested under **Core Concepts** in the sidebar):
        - Agents: `…/api/concepts/agents`
            - Flows: `…/api/concepts/flows`
                - Flow Variables: `…/api/concepts/flow-variables`
                - Intents: `…/api/concepts/intents`
        - Workflows: `…/api/concepts/workflows`
            - Workflow Variables: `…/api/concepts/workflow-variables`
        - Tools: `…/api/concepts/tools`
        - AI Models: `…/api/concepts/ai-models`
        - Incoming Webhooks: `…/api/concepts/incoming-webhooks`
        - Objects: `…/api/concepts/objects`
        - Record Types: `…/api/concepts/record-types`
        - Tables: `…/api/concepts/tables`
- **API Reference** — auto-generated from the OpenAPI spec; sidebar groups: Agents Builder · Workflows Builder · Objects · Tables · Integrations · Core
    - `https://docs.getfrontline.ai/reference/openapi`
- **CLI** — getting started and per-command pages
    - `https://docs.getfrontline.ai/cli` — overview
    - `https://docs.getfrontline.ai/cli/getting-started`
    - `https://docs.getfrontline.ai/cli/authentication`
    - Per-command pages live under a **Commands** group split into two sub-groups:
        - `https://docs.getfrontline.ai/cli/frontline/{agents,workflows,tools,object,table,billing,api,ai-models,incoming-webhooks,setup,auth,util}`
        - `https://docs.getfrontline.ai/cli/max/{auth,chat,conversations,config-path}`

When you don't know the exact slug, link to the section root
(`/api`, `/reference/openapi`, `/cli`) — the sidebar exposes everything from
there.

## Sections on `help.getfrontline.ai`

This site is owned by the customer-success team and covers UI flows, channel
setup, troubleshooting, billing in-app, etc. Treat it as the canonical
reference for anything that lives **inside the Frontline app**, not in the
API. When in doubt, link to the homepage and let the user search:
`https://help.getfrontline.ai`.

## Response patterns

When the user asks _"where can I read about X?"_:

- **API / endpoint / payload / auth / rate-limit question** → link to the
  relevant page under `docs.getfrontline.ai/docs/...` or `/reference/openapi`.
- **CLI / `frontline …` / `max …` question** → link under
  `docs.getfrontline.ai/cli/...`.
- **App / UI / "how do I do this in Frontline" question** → link to
  `help.getfrontline.ai` (and a deep link if you know one).
- **The question spans both** (e.g. "how do agents work") → link to **both**:
  concepts in `docs.getfrontline.ai/docs/concepts/agents` for the data model
  and `help.getfrontline.ai` for the UI walkthrough.

Format the answer with the link inline and one short sentence describing
what they'll find:

> Read the API concepts here: <https://docs.getfrontline.ai/docs/concepts/agents>.
> For the UI walkthrough (configuring channels, publishing the agent, etc.)
> see <https://help.getfrontline.ai>.

## When to fetch vs link

Fetch with `WebFetch` only when:

- No skill answers the question, **and**
- You need the content to act (not just to cite).

Otherwise prefer linking — opening a page just to paraphrase a paragraph back
to the user wastes context and is slower than letting them click.

After a fetch, do **not** dump the raw page back at the user. Summarize, cite
the URL, and stop.

## What this skill is not

- It is **not** a substitute for the other Frontline skills. If a question
  is about the Public API or the CLI, the dedicated skills cover it in more
  depth and with the right command shapes. Read those first.
- Notable dedicated skills: `record-security` (FLS per record type),
  `agents-chat` (test agent flows from terminal), `max-chat` (Max assistant),
  `sharing` (resource and record sharing).
- It does **not** know internal employee docs, runbooks, or private wikis —
  only the two public sites listed above.
