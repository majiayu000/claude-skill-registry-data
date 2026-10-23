---
name: mock-verification
description: "Smoke-walk a `web-application` in a real browser once it builds clean — stand it up in mock mode, walk the flows of its prototype, fix each failure where you find it, post progress item by item. Required for every change to a webapp component. Judging a DEPLOYED system is the `validation-task` skill's job instead."
metadata:
  aep:
    kind: platform
    audience: [coding]
---

# Mock verification

A clean build says the code is well formed and nothing about what the screens
do: a screen the prototype shows and the router never registered, a button wired
to nothing, a form that flips a row and sends no request. So you open the app
and use it. Mock mode stands it up on this machine with no cluster, no sibling
service and no IDP. You verify and repair in one pass.

**This is a smoke walk: breadth over depth.** You are looking for a screen that
is missing, an arrow that goes nowhere, a control that does nothing, a request
that never leaves the page. Data, layout and wording are not your questions.
Your prompt names the flows in scope: the flows of its item and of earlier
items. A cycle's regressions land in shared chrome and on pages nobody meant to
touch, so walk every flow in scope, whichever issue built it.

## What you verify

### The map

`specs/design/components/<component>/prototype.json`, under the project root:
your working directory, one level above the App Path you edit in. A flow is
one role (`roleId`) and the screens that role walks (`screenIds`), in order.
`prototype.tsx` beside the manifest shows what each screen holds: the
component for a screen id in `defineApp({ screens })` has the screen's
controls and, as `to` or `useNav().go(…)`, where each one leads.

**Each flow in scope is one item, by its `id`.** Walk it under its role
(`?role=<id>`) by clicking from its first screen through its `screenIds`, and
do what its `name` says. Two flows on one screen are two items: the screen is
not the unit.

**A flow starts where its control is.** Its start state is the state in which
its first screen shows the control that its `name` needs. `prototype.tsx`
gives that state as the branch around the control (`status === "draft"` around
`Publish menu`). When the seed data does not start there, put the data in that
state before you walk the flow:

1. Through the app's own controls, by clicking (a close, a delete, a create).
2. If no control of the app gets there, set that record of the seed in
   `mock/handlers.ts` to the state, as the contract allows it, and `restart`.
   After the flow, put the seed back as it was and `restart`. Change only the
   seed, never what a handler answers.

Open a screen in no flow at its route. Reach the shell screens (Account,
Settings when the prototype has one, Signed out) through the user menu.

The manifest lists the display states (`states`); `prototype.tsx` shows which
screen renders each. Walk the states that mock mode can show: the empty state,
and the validation error through the empty-submit probe. Mock mode cannot show
a failed or a delayed state (a request failure, a slow dependency). Such a
state is its own item, after its screen. Check it ONCE in the page source:
name the condition and the element that renders it. Record it **outside**,
with "mock mode cannot show it". Never try to force it: a forced failure costs
more tool calls than the rest of the screen.

**The manifest is your only map**: it sets what you walk. You open a source
file to repair, to find the route of a screen in no flow, or to check a state
that mock mode cannot show. A component with no `prototype.json` gives you its
registered routes instead, one flow per role. The prototype is the review's
copy, not the app's code: never edit it.

### Per screen

On each screen that a flow reaches, and on each screen in no flow, ask three
questions of the controls that the role sees there. A screen that an earlier
item answered under the same role and state needs only the controls that this
flow uses. Each question is one action and one snapshot with the first
plausible input. A screen is answered in a handful of actions; past that you
are past the smoke.

| | Question | Evidence |
|---|---|---|
| **Reach** | Did the step before this screen in its flow bring you here, and does every link it shows land on the screen it names? | the target's snapshot |
| **Act** | Does every control the prototype shows change something visible when used? A create is in the next list as that list opens, with no filter changed by hand; a filter narrows; a toggle flips a row. | the snapshot after the action |
| **Request** | Did a change leave the page as the request the contract declares, with the status it declares? A row that flips and sends nothing is the one defect a build cannot see. | `agent-browser network requests` |

### Once per app

- **Roles** (`mock/authz/roles.gen.ts` exists): each flow's entry screen under its own
  role (`?role=<id>`), and once under a role whose `roleIds` leave it out.
  Both directions are defects. Then three more, which the scope model makes
  walkable and which no build can see:
  - **Every role, and the no-role visitor.** Walk `?role=<name>` for each role
    in `mock/authz/roles.gen.ts`, then `?role=` (empty — signed in, holding nothing).
    The empty one must give **`NoAccess` replacing the shell**, naming the
    groups to ask to be added to. A shell with an empty nav around it is a
    defect; so is being let into a screen.
  - **Forbidden, by hand.** Open one screen a role must NOT reach, by URL,
    under that role. Expect that screen's **`Forbidden` state INSIDE the app
    shell** — the rail the role can use still there — naming the role that
    would unlock it. Never a redirect to sign-in, never a blank page, never the
    screen itself.
  - **The mock must have refused something.** None of this means anything
    unless the mock's gateway layer is actually enforcing. It reads the handles
    out of `openapi.yaml`, so they cannot be wrong — but it can be OFF, and an
    app where it is off is green everywhere and proves nothing. Two checks, and
    both are cheap: the dev server prints how many operations it enforces and
    from which contracts at startup, and one refusal shows in
    `agent-browser network requests` as a bare **401** with the reason on the
    console (`[mock gateway] 401 GET /claims — …`). See one before you trust
    the rest.

  A screen a role is *meant* to reach but cannot, because the design does not
  grant it the handle the operation declares, is **open**, naming the role, the
  screen and the handle. It is a design defect, not a code one: do not widen a
  mock handler or a route guard to make it pass.
- **Session** (an auth dependency): `?auth=out` on one entry screen runs the
  app's own guard and `signIn()` brings you back; then **Sign out** where the
  prototype puts it (the user menu) leaves the screen through `signOut()`. The
  mock signs the next load in again, so the session being gone is outside; the click leaving
  the page is not.
- **Probes**: submit one form empty; open one detail route with an id that does
  not exist. These are two states the happy path implies. The empty submit
  also walks `state.validation-error` where the manifest lists it.
- **Short window**: reload ONE screen that has a primary action low on the page
  at `agent-browser set viewport 1280 600`, and click that action. A layout that
  only works on a tall window is a layout most laptops do not have, and the way
  it fails is silent: a sticky footer sits over the button, the content pane does
  not scroll, and the click lands on the footer. Set the viewport back afterwards.
- **Deep entry**: load one nested route as a fresh page load in the address
  bar, not by clicking into it. Clicking never leaves the first document, so
  only this exercises the app booting at that URL — the path a bookmark, a
  shared link and F5 all take. A blank page is the finding; `agent-browser
  errors` names it.
- **Console** (`agent-browser console`, read whole, once, before you stop): a
  page that renders and throws is broken for whoever touches it next, and the
  error text is the finding.

### Outcomes

Every item ends in exactly one:

- **done** — what you did and what the page did back.
- **fixed** — what was wrong; what you changed; what it does now, re-walked.
- **open** — what happens, after three attempts.
- **outside** — the truth lives outside the app, or mock mode cannot show it.
  Outside the app: a computed total, a generated checklist, what the real IdP
  grants a real account. The mock answers to `openapi.yaml`, so it proves the
  request went out, never that the number is right; `validation-task` judges
  that against the deployed system. Mock mode cannot show a failed or a delayed
  state: name the condition in the source and the element that renders it. A
  **refusal is not outside** — the mock's gateway layer answers it from the contract's own
  handle, so `Forbidden` is something you walk and see.

An unreachable screen is **open**, naming the navigation that failed, never
**done** read off the source. A flow whose start state the walk did not reach
is **open**, naming that state: a flow whose control the screen did not show
was not walked, and it is never **done**. A fix does not remove or hide what
the prototype shows. If the app cannot fill an element the prototype shows, the item is
**open**.

## Progress

Your prompt says where progress goes. Post there, in these three shapes and no
other: the plan once, one line per item as it settles, the close once.

```text
Mock verification: <component> — <N> items
1. <flow id> · <flow name> (<role>): <Screen> -> <Screen>; starts at <the state its control needs>; states: <its states>
2. <Screen> · <state>: source check
3. <flow id> · ...
<k>. <Screen> (no flow): <its controls>; -> <the screens its `to`s name>
<N-4>. Roles
<N-3>. Session
<N-2>. Probes
<N-1>. Short window
<N>. Console
```

`<Item>` below is the flow id, the screen in no flow, the screen's state, or
the once-per-app item.

```text
<n>/<N> <Item>: done — <what you did and what the page did back>
<n>/<N> <Item>: fixed — <what was wrong>; <what you changed>; re-walked, <what it does now>
<n>/<N> <Item>: open — <what happens, or the start state not reached>, 3 attempts
<n>/<N> <Item>: outside — <the truth that lives outside the app>
<n>/<N> <Screen> · <state>: outside — mock mode cannot show it; <the condition> renders <the element>
```

```text
Mock verification done: <component> — <N> items · <d> done, <f> fixed, <o> open (<n> <Item>, ...), <t> outside
```

The newest line is where the walk is, and that is what the person watching
reads. An item with no line is a flow or a screen you never reached, and it
stays visible as one.

## 1 · Stand it up

```bash
cd <App Path> && bash "$AEP_SKILLS_DIR/mock-verification/scripts/walk.sh" up
```

The `cd` is part of the command, not advice around it: the script keys its
state off the working directory, so run from anywhere else it starts a second,
unrelated server and hangs waiting for one that was never yours.

It starts `npm run dev:mock` on a free port, reaps a stale server from an
earlier attempt first, and prints `READY <url>`. The url is what you open;
`?role=` and `?auth=out` go on it. If it prints the log instead, that is your
first finding: the harness is `react-webapp`'s `references/mock-mode.md`; fix
it and run `up` again.

**Done when:** `READY`.

## 2 · Plan

Before the browser opens, post the plan from the map alone: one numbered item
per flow in scope, by its id in the manifest's order, with its role, its
screens in walking order and the state it starts in, and one per state that
mock mode cannot show, after the flow that reaches its screen. Then screens in
no flow, the shell screens, Roles (with `mock/authz/roles.gen.ts`), Session (with an
auth dependency), Probes, Short window, and Console. Posting it first puts
your coverage in front of the person watching while there is still time to say
a screen is missing.

**Done when:** every flow id in scope has a number, every screen in scope is in
a flow item or has its own, and the plan is posted.

## 3 · Walk

Load `agent-browser` and follow it: open, snapshot, act on what the snapshot
shows.

**An item ends green, and posted.** Walk it; if it fails, fix it now, walk that
same item again, and see it pass; then post its line, and only then open the
next. A line posted at the end for an item settled an hour ago is a history,
not progress. Every failure is yours, whichever issue put it there.
**Repair the app, never the plan.**

**Three attempts on an item, then post it open and walk on.** The screens
behind it are still unopened. A fix is the wiring a screen is missing; a defect
that wants a redesign is open with its cause named.

**Click between screens.** Mock state lives in the page, so `open`, reload and
back restore the seed data: a record you created a moment ago is gone, and that
is the mock telling the truth, not the app. Spend full loads at the start of a
block, where there is no state to lose — a role switch, `?auth=out`, an unknown
id. The once-per-app items are walked off the plan like any other.

`restart` after a change to `vite.config.ts`, `mock/` or a dependency;
everything else hot-reloads.

**Done when:** every number has its line, each posted before the next item was
opened.

## 4 · Close

Post the closing line, then:

```bash
bash "$AEP_SKILLS_DIR/mock-verification/scripts/walk.sh" down
```

`down` stops the server, closes the browser and confirms the port let go. Hand
back to whoever dispatched you the closing line and the numbered list with each
item's outcome: the closing line is what the pull request quotes, and the open
items are what it carries.

**Done when:** the close is posted, `down` printed `STOPPED`, and the list is
in your reply.

## Never

- **Make the mock agree with the app.** `mock/handlers.ts` answers to
  `openapi.yaml`, the same document `src/generated/` came from, and to nothing
  else. A handler bent until a screen passes hides the defect from the deployed
  system too. A `501` is a handler you never wrote: write it against the
  contract.
- **Widen a scope to make a walk pass.** Not in `mock/authz/roles.gen.ts`, not in a route
  guard, and not by adding a check to a handler that overrides the gateway
  layer. Scope comparison is a whole-string match at the gateway, so a mock bent
  to accept a sibling handle passes a walk the deployed system 401s. A role that
  cannot reach its own screen is a **design defect**: post it open, naming the
  role, the screen and the handle.
- **Run `git`, commit, or open a pull request.** The record belongs to the agent
  that dispatched you. Progress, where your prompt says it goes, is the only
  writing you do outside the App Path.
