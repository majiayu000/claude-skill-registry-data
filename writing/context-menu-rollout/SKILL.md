---
name: context-menu-rollout
description: "Fleet worker contract for wiring assigned files to the v3 right-click menu. Use when handed files from pnpm check:context-menu, or told to 'wire the menu on X', 'do your assigned rows', or 'clear your shard'. NOT for an unassigned one-off menu wiring (use context-menu-v3)."
---

# Context-menu rollout — the fleet worker's contract

You have been assigned one or more files. Your job for each: **the user can
right-click the thing this surface shows, and the menu that opens is the SAME
menu that identity gets everywhere else in the app.**

Read [`.claude/skills/context-menu-v3/SKILL.md`](../context-menu-v3/SKILL.md)
once for the wrapper mechanics. This file is the assembly line. Not this contract:
designing the menu system itself (`context-menu-v3` + `features/context-menu-v3/FEATURE.md`)
or a full surface audit (the `surface-check` skill).

## Your assignment is disjoint — do not wander

You own exactly the files you were given. Another agent owns the next file.

- **Never** edit a file outside your assignment, even to "fix something small".
  If you find a defect elsewhere, name it in your report; do not touch it.
- **Never** run tree-wide git commands. `git add <your exact paths>` and
  `git commit --only <your exact paths>`, always. Dozens of agents and a human
  share this checkout; `git add -A` steals their in-flight work.
- Commit each file as you finish it. Do not batch to the end.
- If your file no longer exists or already has a menu, say so and move on. That
  is a legitimate outcome, not a failure.
- 🚨 **DO THE WORK YOURSELF. Never spawn sub-agents to do your shard.**
  A worker that re-delegates breaks the two things that make this rollout safe:
  the coordinator's disjoint partition covers only the agents IT assigned, and
  nothing guarantees your children read this skill. One wave-2 worker delegated
  its 11 files to four sub-agents and returned a status update instead of a
  report — that is a failed shard, however the children turn out. Your shard is
  a dozen files; read them and edit them.

## The seven steps, per file

### 1. Find the PANE and name the IDENTITY

Open the file. Answer two questions before writing anything:

- **What is the pane?** The one element wrapping the whole list/table/editor.
  ONE menu goes around it — never one per row (nested Radix triggers open two
  menus and the inner one always wins, so per-row wrappers silently break the
  pane menu).
- **What does a row NAME?** A keyword? a page? a contact? a rule? a class? That
  is the *identity*, and it decides everything in step 2.

### 2. 🚨 CHECK THE REGISTRY — this is the step that makes the rollout worth doing

Open [`features/context-menu-v3/SECTIONS.md`](../../../features/context-menu-v3/SECTIONS.md).

| What you find | What you do |
|---|---|
| The identity **has a registered builder** | **Use it.** Import it, pass `getRow`, spread its section into `extraSections`. Never re-implement its items. |
| No builder, but the identity appears on **2+ surfaces** | **Extract** a shared builder (copy the shape of `useKeywordMenuSection`), register it in SECTIONS.md, use it. |
| No builder, identity is **genuinely page-local** | Inline `extraSections` is correct. Do not register a one-off. |

### 🚨 YOU MAY NOT ASSERT "page-local" WITHOUT RUNNING THE SEARCH

This is the step the first pilot wave got wrong on **every file**, so it is now
mechanical. "Page-local" is the RARE answer, not the default. Before you write
it, run the recurrence search and put the result in your report:

```bash
# the identity's table / type token / row-type name — try more than one spelling
grep -rl "workflow_run\|WorkflowRun" features app | grep '\.tsx$'
```

Count only files that **render that identity to a user**. Exclude tests,
`features/overlays/openers/**` (those are opener hooks), and pure type files.

- **2 or more → EXTRACT and register.** No exceptions, no "but the other one is
  a window", no "but they show slightly different columns". A window and a
  table showing the same record are exactly the case the registry exists for.
- **1 → inline is correct**, and your report states the command and the count.

If every file in your shard came back "page-local", you did not search. Two
agents in the first wave reported six page-local identities; five of the six
were wrong — `workflow run` renders on five surfaces, `activity event` on four.

Then, if you adopted an existing builder, do **THE GROWTH STEP** — the most
valuable thing you will do today:

> List every action a user would reasonably want for this identity **on this
> surface**. Compare against what the builder offers. It will almost always be
> missing some. **Add them to the shared builder**, so every surface that
> already uses it gains them too. Never bolt a private section next to the
> shared one for the same identity — that is the fork this whole system exists
> to prevent.

And **THE CONSISTENCY STEP** — for anything the shared section offers that
genuinely cannot work here:

```ts
import { unavailableHere, needs } from "@/features/context-menu-v3/utils/availability";

useKeywordMenuSection({
  …,
  unavailable: {
    "kw-pages": unavailableHere("the Keyword Workbench"),
    "kw-intel": needs("a library keyword"),
  },
});
```

The row stays **visible, in place, disabled**, with the reason as its tooltip.
**Never delete a row to make it fit your surface.** A missing row teaches
nothing; a disabled row naming where it works is a direction.

### 2b. THE THIN-WRAPPER CASE — when the rows are not in your file

Many windows and route pages are a **thin shell around a workspace component**
that actually renders the rows, and that component is in someone else's shard.
You cannot give those rows a per-row identity from your file alone.

Do this, in order:

1. **Mount the pane menu anyway.** A window without its own menu answers
   right-clicks with the page underneath — that is the harm, and mounting fixes
   it even with no per-row entity.
2. **Do NOT reach into the child** — with ONE narrow exception. You may follow
   into a child ONLY when all three hold: the child is the sole owner of the
   thing you were told to wire (e.g. it holds the textarea ref and setter, so
   no honest `EditableContextMenu` exists without it); you verified by grep
   that no other assigned file references it; and you disclose the crossing at
   the TOP of your report with that reasoning. When any of the three is in
   doubt, report instead — a second agent arriving at the same file produces
   nested menus, and the inner trigger silently wins.
3. **Report the exact child file and what it needs.** Almost always one line
   per row — the DOM sniffer means the child needs no resolver at all:

   ```tsx
   <tr data-entity-type="task" data-entity-id={row.id} data-entity-title={row.title}>
   ```

4. Grade yourself honestly as a shell and say WHY: "rows live in
   `ProjectsWorkspace.tsx`, out of shard".

⚠️ **A child that already mounts its own menu needs nothing from you.** If the
component you render wraps itself (e.g. `ChatThread`), adding an outer wrapper
creates a dead nest — the innermost trigger wins and yours never opens. Leave
it, and say so.

### 3. Wrap the pane

```tsx
import { NonEditableContextMenu } from "@/features/context-menu-v3/NonEditableContextMenu";
import { CONTEXT_MENU_ENTITY_KEY } from "@/features/context-menu-v3/types";
```

`EditableContextMenu` for a textarea/editor (it also auto-registers the
WidgetHandle, so agents can stream edits in). `NonEditableContextMenu` for
everything else. A surface with both modes uses both, one per mode.

```tsx
<NonEditableContextMenu
  sourceFeature="<feature>"        // REQUIRED
  contentSource={{ type: "raw" }}  // or the real source: note / chat-message / …
  contextData={{ content: "" }}
  resolveContextOnOpen={(target) => {
    const id = target?.closest("[data-row-id]")?.getAttribute("data-row-id");
    const row = (id && rows.find((r) => r.id === id)) || null;
    setClickedRow(row);            // STATE, not a ref — see the trap below
    if (!row) return null;
    return {
      [CONTEXT_MENU_ENTITY_KEY]: { type: "<entity_token>", id: row.id, title: row.name },
      content: [/* the row, as plain lines a human would read */].join("\n"),
    };
  }}
  extraSections={[section]}
>
  {/* the pane, untouched */}
</NonEditableContextMenu>
```

**Shortcut**: if the row element is yours to edit, you can skip
`resolveContextOnOpen`'s entity entirely by putting
`data-entity-type` / `data-entity-id` / `data-entity-title` on the row —
the shell reads them and Attach To targets that record. Explicit resolver
answers always win over the DOM.

`surfaceName` ONLY if the surface has a real manifest whose declared
`alwaysAvailable` values this pane actually emits. **Passing a `surfaceName`
you cannot back is worse than passing none** — the value-mapping guard will
scream, correctly.

### 4. 🚨 THE DENSITY LAW

A menu item is a **short verb phrase**. `Edit rule…` · `See its keywords` ·
`Open page workspace`.

**No `description` / subtext. Ever.** The single exception is a `disabled`
item, whose `description` is the reason it is off. If macOS would not put it in
a menu, neither do we. Machine-checked — a violation fails the build gate.

Labels must also *fit*: a label that renders as `Review in Keyword Workbe…` is
a defect. Keep them short enough to read whole.

### 5. Type-check

```bash
pnpm type-check
```

Errors in **your** files are yours. Errors in files you did not touch belong to
another session — isolate them in your report with exact paths, do not fix them.

### 6. Prove it with the detector

```bash
pnpm check:context-menu --json
```

Your file must now be **absent from its population** and, if it appears in the
shell list, must not be graded a shell for a slot it could fill. An empty slot
is legitimate only when the surface genuinely has no such thing (a chart has no
attachable record) — say which and why in your report.

### 7. Commit

```bash
git add <your exact paths> && git commit --only <your exact paths> -m "…"
```

## The traps that will get you

- **`resolveContextOnOpen` must write STATE, not a ref**, if any label or
  availability depends on the row. It runs during the event that opens the
  menu, and the lazy menu reads state during that same render — a ref does not
  re-render and your labels go stale.
- **It is called twice** on a plain right-click (mousedown, then contextmenu).
  Keep it cheap and idempotent.
- **`className` on the wrapper styles the POPUP, not your pane.** Never put
  layout classes there. Style the child you wrap.
- **A read-only menu yields inside live text fields** by design — right-clicking
  an `<input>` inside a `NonEditableContextMenu` shows the browser menu. Not a
  bug.
- **Nested menus: the innermost wins.** A pane menu wrapped around rows that
  mount their own menus will never open on those rows.
- **A `createPortal` child cannot be wrapped from its parent.** If the workspace
  portals itself to `document.body` (e.g.
  `features/pdf-extractor/components/PdfExtractorWorkspace.tsx`), a wrapper
  written in the window file has no real DOM child to attach to — Radix
  `asChild`/Slot needs an element, not a portal marker. The menu must be
  mounted INSIDE the portaling component. Report it; do not fake a wrap that
  provably cannot work.
- **An overlay/window must mount its OWN menu.** Without one, a right-click
  inside it is answered by the page underneath, handing the user that page's
  surface and agents — silently wrong, and it looks like it works.
- **`getApplicationScope` and `contextData` both feed the scope** (live wins per
  key), but if you pass a live builder make sure it reads the same clicked-row
  state your resolver writes.

## Your report

Per file, five lines. No prose essays.

```
<path>
  identity:  <what a row names>
  registry:  adopted <builder> | extracted <builder> (registered) | inline — `<grep you ran>` → N file(s)
  grew:      <actions added to the shared builder>  | none
  disabled:  <items + reason>  | none
  evidence:  type-check clean · gone from <population> · grade: wired | shell (<which slot, and why it is honestly empty>) · commit <sha>
```

Then, separately: anything you found and did **not** touch.


---

## For the coordinator — dispatching a wave

**Shard with the script, never by hand:**

```bash
npx tsx scripts/context-menu-shard.ts --agents 8 --population tables
```

It groups by directory before dealing (siblings usually share an identity, and
the agent holding the whole group is the one who spots the shared builder) and
it asserts the partition is disjoint. Two agents on one file is worse than a
conflict: both wrap the pane, the nested inner trigger wins, and the outer menu
never opens — a failure that looks fine in a screenshot.

**🚨 DISPATCH NEUTRALLY. This is a real lesson, not a nicety.** In the first
wave the coordinator wrote *"if each appears on only this one surface, inline
is the correct answer"* into two agents' prompts. Both agents returned
all-inline. The one agent told *"these almost certainly recur — extract and
register"* extracted a builder, registered it, adopted it across four files and
grew it. **The prompt decided the outcome more than the skill did.** Never hint
at the answer to step 2; let the grep decide. Say only:

> You are a fleet worker on the context-menu rollout in <repo>.
> FIRST: invoke the `context-menu-rollout` skill and follow it exactly.
> YOUR ASSIGNMENT — these files ONLY (another agent owns every other file):
> <paths>
> Return the report the skill specifies. Nothing longer.

Add per-shard notes ONLY for genuine hazards — a protected resource, a known
in-flight breakage to ignore — never for how step 2 should come out.

**Verify, do not trust the report.** Every wave, before dispatching the next:

```bash
pnpm type-check                    # errors in the fleet's files only
npx tsx scripts/check-context-menu.ts   # populations shrink; density stays 0
```

Then spot-check the "page-local" claims by running the recurrence grep
yourself. In wave one, five of six page-local claims were false.
