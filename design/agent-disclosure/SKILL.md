---
name: agent-disclosure
description: "Disclosing a surface's existing fixed AI jobs in the shell's top Agents menu. Use when a page, panel, overlay, or window already runs a mandate behind a button, assist, automatic action, or mode; when the agent-disclosure guard names a file; or during a surface check."
---

# Agent disclosure — register existing fixed jobs in the top menu

## The non-negotiable boundary

🚨 **DISCLOSURE MUST NEVER CHANGE THE SURFACE'S VISIBLE CONTENT.**

Do not add an agent chip, badge, card, row, label, roster, callout, explanatory
copy, icon, toolbar item, or section to the page, panel, dialog, overlay, or
window. Do not move or resize existing content to make room for disclosure. Do
not create a new agent integration merely so a surface can be "complete."

The disclosure destination is the shell's **existing top Agents menu only**.
The job must already exist in the product surface. This skill records that
pre-existing fixed job so the user can inspect its mandate without leaving the
page. It is not authority to modify page content or product behavior.

**One owner-approved exception (Arman, 2026-09-25):** the small Intelligence
icon (`IntelligenceIndicator`, `features/mandates/feature-intelligence/FEATURE.md`)
may sit beside a control that runs a job. It is a door to where the job is
managed, not a disclosure roster — never add anything else under its name.

There is no inline disclosure component. `PageAgents` is forbidden and deleted.
If a task or old document tells you to render it, that instruction is stale and
must not be followed.

Cross-repo source of truth:
`../../../common-docs/systems/mandates/CLIENT-SURFACES.md` § THE
DISCLOSURE LAW. Frontend detail:
[`features/surfaces/FEATURE.md`](../../../features/surfaces/FEATURE.md).

## Decide whether a roster exists

### Fixed surface job — disclose in the top menu

A fixed job is an AI action the surface itself owns: for example, a specific
mandate behind "Assign topics" or a recurring agent that performs the same job
for this page. Confirm the integration already exists before registering it.

- Static job: declare a manifest `agentRole` carrying its `mandateKey`.
- Runtime-selected fixed job: call `useDeclaredSurfaceMandates` from the
  existing action-bearing component. This call has no UI.
- Open the mandate through `useOpenMandateWindow`; never link away to a mandate
  route from a working surface.

### Agent-native and resident agents — explicit isolation

Chat, Agent Builder, runners, tests, and window-panel residents may host an
**outside helper** that works on the page's data. They are not blanket binding
exclusions. The page's native subject agent and any permanent resident helper
must never acquire ad-hoc surface values merely because it is placed on, shown
in, or bound to that surface. Their engineered state and context remain theirs.

Each invocation follows an approved context mode: `none`, `named_inputs`, or
`approved_surface_context`; the latter may use explicit mappings or a
user-approved task-appropriate page snapshot. A documented integration contract
or explicit user choice is approval provenance and persists until its scope
changes; it does not require a new prompt for every run. Placement or a saved
binding does not approve a mode or any value. Record the agent/job,
surface, purpose, mode, allowed value names, approval provenance, and evidence
before treating a helper context handoff as complete. This documentation sets
the required contract and evidence; it claims neither runtime enforcement nor a
unified tracker implementation.

- A native subject launch receives only its explicit engineered inputs. It never
  receives ambient or ad-hoc surface context; helper approval cannot create an
  exception.
- A permanent resident, including a window-panel helper, has no automatic
  inheritance. Its deliberate job contract may use named inputs or approved
  surface context when it works on page data.
- An outside helper may use any page, including Chat or Agent Builder, under its
  recorded integration contract. Binding availability and a data handoff are
  separate decisions; saving a binding does not require or grant context.
- When the approved purpose is agent definition work, the outside helper may
  edit every user-editable definition field, enter runtime variables and human
  input, and run the test. The contract records the actual installed targets;
  it does not pretend an unavailable target or runtime enforcement exists.
- Disclosure still names only an existing fixed job in the top Agents menu. It
  never adds visible agent content or invents an agent.

## Find the work

```bash
pnpm check:agent-disclosure
```

The guard scans UI surfaces that run mandates. It also fails loudly if the
forbidden `PageAgents` import or JSX pattern returns anywhere. Execution
machinery is excluded because it runs on behalf of a surface.

Before changing anything, inventory the surface's existing buttons, assists,
automatic actions, tabs, and modes. For every candidate, prove which fixed
mandate it already runs. Never infer a job from an agent-looking icon or from
the existence of an agent picker.

## Register a static fixed job

In the surface manifest:

```ts
agentRoles: [
  {
    name: "topic_assigner",
    label: "Topic assigner",
    description: "Places this surface's keywords onto the Offering tree.",
    kind: "single",
    defaultAgentId: null,
    mandateKey: "seo.topic_assigner",
    autoRun: "never",
    sortOrder: 100,
  },
],
```

- Use a mandate key, never a raw agent UUID.
- `does`/description says what the job does here in plain product language.
- `mandateKey` and a non-null `defaultAgentId` are mutually exclusive.
- Do not add a role when the surface merely lets the user choose an agent.

## Register a runtime-selected fixed job

Use this only when live state determines which already-existing fixed job the
surface runs:

```tsx
useDeclaredSurfaceMandates(
  engine.agents.map((agent) => ({
    mandateKey: agent.mandateKey,
    does: agent.does,
    surfaceName,
  })),
);
```

`useDeclaredSurfaceMandates` populates the top Agents menu and renders nothing.
Mount it in the existing action-bearing component. Do not add a wrapper or a
visible sibling. Do not use it for arbitrary picker choices.

## Open the mandate in place

```tsx
const openMandate = useOpenMandateWindow();
openMandate({
  initialMandateKey,
  mandateKeys,
  surfaceName,
  initialView: "yours",
});
```

The existing menu row is the door. A link from a working surface to
`/mandates` or `/administration/mandates` is a regression.

## Decision table

| Situation | Verdict |
| --- | --- |
| Any surface, including Chat or Agent Builder, has an existing outside helper | It may bind there; its data delivery follows its recorded approved integration contract. |
| The launch is the page's native subject agent | Give it only its engineered inputs; never an ambient or ad-hoc page snapshot. |
| The launch is a permanent resident helper | Use `none`, named inputs, or approved surface context only under its deliberate documented contract. |
| An existing fixed job runs on a surface | Register it in the top menu only; this is separate from context approval. |
| Runtime mode selects one of several existing fixed jobs | Register the live fixed job without rendering UI. |
| On an eligible ordinary product surface, service/thunk/tool machinery runs a mandate | Register on the calling surface, not in machinery. |
| No AI job exists yet | Do nothing; disclosure cannot invent one. |
| Agent uses a raw UUID with no mandate | Fix hardcoded-agent architecture first; do not invent a key. |

## Verify live

1. Capture the surface before and after. The page body's visible content,
   spacing, controls, and layout are unchanged by disclosure.
2. For a fixed job, open the existing top Agents menu and confirm the job
   appears exactly once. Open it and confirm the mandate window appears over
   the page.
3. For each helper invocation, verify the saved record and a run: allowed names
   arrive for `approved_surface_context`; no ad-hoc surface values reach a native
   or resident agent whose mode is `none`.
4. Confirm no `PageAgents` import, JSX, agent chip, or disclosure-only page
   content exists.
5. Run `pnpm check:agent-disclosure`, focused tests, and `pnpm type-check`.

## Sweep discipline

- One feature area per commit; stage only owned files in the shared checkout.
- Never add visible UI to reduce the guard count.
- Never register an agent the surface does not already run.
- Never add an exemption merely because a finding is inconvenient.
- Update the feature's `FEATURE.md` change log in the same commit.

## Where this runs from

- Standalone: `/agent-disclosure` or an undisclosed-surface sweep.
- Live UI work: `live-ui-iteration` routes here when the surface already has a
  fixed AI job.
- Certification: `surface-check` S5.
- Codex and Claude share this exact skill because `.agents/skills` points to
  `.claude/skills`; `agents/openai.yaml` supplies the Codex interface.
