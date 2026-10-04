---
name: no-dead-ends
description: "Recipe for THE DOOR LAW (every record the UI names opens; every detected problem ships its fix) and THE INVENTORY LAW. Use before building or fixing a surface that names a record or flags a problem (cell, row, dialog, badge, warning, id, count), or on 'no link to X', 'why can't I click this', 'dead end', EntityRef, peek. NOT for page chrome (use core-route-headers)."
---

# no-dead-ends — every identity is a door, every capability is on the table

**Read the doctrine first:** `../common-docs/policies/no-dead-ends.md`.
It is canonical and cross-repo. This skill is the *frontend mechanics*: which
primitive to reach for, how to wire it, and how to prove it. **Out of scope:**
page-level chrome (use the `core-route-headers` skill) and choosing WHAT data a
surface shows — this skill makes what is shown openable.

## The two laws, one paragraph

If the UI names a thing that has an id in our database, the user must be able to
reach it — **THE DOOR LAW**. And you may not build the surface before you know
what the platform already gives it — **THE INVENTORY LAW**. A surface that
prints "Deep Web Research Agent" as a `<span>` fails both: the agent has a
route, an icon, a peek, an action registry, a lineage index, and a sync window,
and the surface used none of them.

## Step 1 — the inventory pass (before the first line)

For every entity the surface names, run these and write the results into your
summary:

```bash
# Does it have a canonical route + icon?  → getEntityInfo(token).hrefFor
grep -n "hrefFor" features/scopes/registry/entityRegistry.ts

# Does it have a peek?
cat features/organizations/peek/kinds-list.ts

# Does it have an action registry / row-actions hook?
ls features/*/browse/*ActionRegistry.tsx components/official/item/

# Does it have an overlay opener or a window panel?
ls features/overlays/openers/ | grep -i <entity>
ls features/window-panels/windows/<entity>/
```

"Found nothing" is only acceptable when it names the queries you ran.

## Step 2 — put the doors on

**Use `EntityRef` (`components/official/entity-ref/EntityRef.tsx`).** It is the
Door Law made importable — name → route, plus new-tab, plus peek, all resolved
from the registries. Never hand-roll a name link.

```tsx
import { EntityRef } from "@/components/official/entity-ref/EntityRef";

<EntityRef token="agent" id={row.agentId} name={row.agentName} />

// Same record lives in two shells (system vs personal agents): override href.
<EntityRef token="agent" id={id} name={name} href={agentHref(id, agentType)} />

// Surface-specific extra doors go in `extraActions` — never forked into a copy.
<EntityRef token="note" id={id} name={title} extraActions={<OpenInWindowButton …/>} />
```

Safe inside clickable rows — every control stops propagation. Worked reference:
`features/mandates/admin/MandatesConsole.tsx` (Agent column, Pin column,
Health column, and the drawer's identity card).

**Missing a door?** Fix the *registry*, not the call site:

| Missing | Fix |
|---|---|
| Route | add `hrefFor` to the token in `features/scopes/registry/entityRegistry.ts` |
| Peek | add the kind to `features/organizations/peek/registry.ts` **and** `kinds-list.ts` (a dev-time guard screams if they drift) |
| Window | register an opener under `features/overlays/openers/` (see the `overlay-system` skill) |

**Never import `features/organizations/peek/registry.ts` for the availability
check** — it statically imports 19 peek components. Import `hasPeek` from
`kinds-list.ts` and render the one dynamic edge, `<ResourcePeekHost>`.

## Step 3 — the corollaries (where the real damage lives)

1. **Render every relationship you can resolve, with its own door.** For agents
   the lineage is free: `selectAgentLineageIndex` /
   `selectAgentLineage` (`packages/chat/src/agents/redux/agent-definition/selectors.ts`)
   derive parent / children / **systemTwin** from the slice — zero extra
   queries. The twin can be a PARENT (personal copy of a system agent) or a
   CHILD (system agent promoted from a personal one); handle both.
   Cold surface with no slice? `fetchLinkedCounterpart` (thunks.ts) round-trips.

2. **Ship the fix beside the complaint.** "NOT a system agent" must come with
   the rebind button and the twin's link, not a scolding badge.

3. **State the verdict, not the timestamp.** "Last synced Apr 29" is not an
   answer. Say identical / what differs / link to the diff.

4. **Never render an id you can't open**, and **never report green for data you
   couldn't read** — an unresolvable reference is its own loud state
   (`unresolved pin` in the mandates console), never `ok`.

5. **A count is a door.** `3 overrides` reaches those overrides.

6. **A SENTENCE is a door too.** Our servers write refusals and notes for
   people, and those sentences name records by raw id — "resolved system agent
   8f0bbfc2-… breaks the mandate contract". Printed as `{message}` that is a
   dead end with extra steps: the reader is told which record is wrong and then
   made to hand-copy a uuid into a URL bar. Print server prose through
   **`TextWithDoors`** (`components/official/entity-ref/TextWithDoors.tsx`)
   instead — it keeps every character verbatim and turns the ids into doors:

   ```tsx
   import { TextWithDoors } from "@/components/official/entity-ref/TextWithDoors";

   <p className="text-destructive">
     <TextWithDoors text={refusal} defaultToken="agent" />
   </p>
   ```

   The token comes from the sentence's own words ("… agent <id> …"); pass
   `defaultToken` only when the SURFACE knows what its sentences are about. An
   id whose type cannot be established stays plain text — a link to the wrong
   record reads as a fact and is a lie. `ServerNotes` already renders through
   it, so every door's notes block inherits this for free.

## Step 4 — prove it

- Browser: every named record shows Open / new-tab / peek. `read_page` and
  confirm the `link "Open X"` / `button "Quick look at X"` / `link "Open X in a
  new tab"` nodes exist per row.
- Data logic (lineage, twin resolution, health): a unit test, because the
  interesting rows are usually invisible to the test account under RLS —
  `packages/chat/src/agents/redux/agent-definition/__tests__/lineage-selectors.test.ts`
  is the pattern. Never claim a path works because it "should".
- Say plainly in your summary what you verified in a browser vs. by test.

## Anti-patterns — fix on sight

- `<span>{record.name}</span>` where `hrefFor` exists.
- A red badge naming a problem with no action next to it.
- A drawer that opens on a *picker* instead of showing what the user has.
- A local `<Dialog>` preview when a peek is registered for that kind.
- A hand-rolled row-action list beside an existing action registry.
- A bare UUID cell.
