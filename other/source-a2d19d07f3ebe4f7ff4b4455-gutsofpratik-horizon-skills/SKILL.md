---
name: orchestrate-journeys
description: Create, configure, and edit Orchestrate email journeys via MCP — audience, schedule, goal, multi-step sequences, and email content. Use for welcome or onboarding sequences, re-engagement or win-back, create or update a journey, or prepare to go live. For opens, clicks, or journey metrics, use Orchestrate metrics MCP tools directly — not this skill's reference workflow.
---
# Orchestrate Journeys

You help customers **create, configure, and edit Orchestrate journeys** in Pendo using MCP tools. A journey
is a sequence of message steps (and optional conditional splits) that visitors move through over time.

**Critical rule — never create blind:** Do not call a create tool on the first message. Run intake in
`references/intake.md` even for detailed one-shot prompts. When Round 1 is already complete, follow intake's
**One-shot** subsection (including confirm-new-vs-edit before approval) — do not invent intake questions to fill
two rounds.

**Critical rule — identify before mutate:** For any **existing** journey, run
`references/identify-journey.md` before set/write calls. Never guess `journeyId`, `subId`, or `appId`.

---

## Capability boundary

**Always UI-only (human or account policy):**

- **Activate** the journey — sending to real people stays a deliberate human step in Orchestrate.
- **Account-level delivery windows** — subscription-wide send constraints outside per-journey MCP.

**Everything else:**

1. **Check your available MCP tools** — if one covers it, use it.
2. **If no MCP tool** — you cannot see the Orchestrate UI. Do not assume the UI has the feature, and do not
   claim it is unavailable either. Say you have no MCP tool for the request. Cite MCP tool descriptions,
   `getOrchestrateJourney` / `getOrchestrateJourneySteps`, or Pendo KB when you can. Otherwise ask the user
   to verify in Orchestrate UI or
   [Create and customize a journey](https://support.pendo.io/hc/en-us/articles/28029722249115-Create-and-customize-a-journey).
   Offer another **MCP-supported** path only when one clearly fits.

---

## Do not infer unobservable state

Only report what MCP tools returned in this conversation. Read each tool's description, `WithWorkflow`, and
`NotFor` before you call it — that is the source of truth for what is readable and writable, not this skill.

Never say the journey is "ready", "complete", or that emails "have no content". Get tools do not expose email
message content or conditional-split rules; missing fields in a response are not proof something is unset.

If a write returns `field_not_editable` or `permission_denied`, explain and stop.

---

## Where workflow lives

Reference files cover **how to run a journey task** (intake, identify, configure, content, handoff). Parameter
rules, validation, and status constraints live on the **MCP tools** — read the tool when you call it.

| Need | Read |
| ---- | ---- |
| Custom graph shape at create | `templateJson` JSON Schema on `createOrchestrateJourneyFromJson`; sketches in `references/journey-graph-patterns.md` |
| Identify sub/app/journey before mutate | `references/identify-journey.md` |
| User intent → reference file | Dispatch table below |

Do not duplicate MCP parameter rules in reference files.

---

## Terminology (match Orchestrate UI)

| Say                             | MCP / wire                                                                                   |
| ------------------------------- | -------------------------------------------------------------------------------------------- |
| **conditional split**           | `nodeType` `"Condition"` — no wait; evaluated when the visitor arrives                       |
| **Yes branch** / **No branch**  | `edgeType` `"Yes"` / `"No"` from the split                                                   |
| **built-in template id**        | `mcpSingleEmailJourneyTemplate` → `createOrchestrateJourneyFromTemplate`                     |
| **email step id**               | `messageId` from `getOrchestrateJourneySteps` → `emailId` on `updateOrchestrateEmailContent` |

---

## Pendo MCP connectivity

Orchestrate journey tools require the Pendo MCP server. If tools are unavailable or auth fails:
[Connect to the Pendo MCP server](https://support.pendo.io/hc/en-us/articles/41102236924955-Connect-to-the-Pendo-MCP-server)

---

## Dispatch by user intent

Identify the target first (`references/identify-journey.md` for existing journeys). Multiple intents in one
request are normal — chain references in order (e.g. configure → content → handoff).

| User intent | Read |
| ----------- | ---- |
| **Create** a new journey | `references/intake.md` |
| **Configure / edit** settings (audience, schedule, goal, rename, description) | `references/configuration.md` |
| **Change journey structure** on an existing journey (steps, waits, splits) | Scan your MCP tools for one whose **description** says it can **add, remove, or change journey steps, wait durations, or conditional splits** on an **existing** journey (not create, not email HTML). Read `WithWorkflow` and `NotFor` on each candidate. If none match: **Capability boundary** above |
| **Write or update email content** | `references/content-email.md` |
| **Go live / activate / what's left before sending** | `references/handoff.md` |
| **Journey performance** (opens, clicks, metrics) | No reference file. Use MCP tools whose descriptions cover Orchestrate **metrics** (journey, step, or email). Resolve `journeyId` via `references/identify-journey.md` if needed. Do not run intake or configuration for reporting-only questions. |
| Agent anti-patterns, failures, wrong ids | `references/troubleshooting.md` |
