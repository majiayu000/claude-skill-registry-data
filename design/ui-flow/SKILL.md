---
name: ui-flow
description: Specify a multi-screen user journey or flow — the screens the user moves through, the decision points, the success and failure paths, and the state that carries between them — before any individual screen is blueprinted or built. Use this skill whenever the user is building something that spans more than one screen (signup flow, checkout, onboarding, multi-step form, wizard, settings drill-down) and is about to design or build any individual screen, because designing screens in isolation is the fastest way to ship a UI where the screens don't actually connect into a coherent journey.
status: stable
---

# UI Flow

**Note: This skill is a recommended addition to the original 7-skill kit.** It fills the gap of multi-screen flow specification, which the rest of the kit treats one screen at a time.

Specifies the journey through multiple screens, including the decision points, the data state that carries between them, and the failure paths. Without this layer, individual screens get specced and built well but don't connect into anything coherent.

## When to use this skill

Use this skill when:
- The user describes a feature that spans more than one screen (signup, checkout, onboarding, wizard, multi-step form, drill-down navigation).
- A `ui-brief` has identified more than one primary action that happens across different views.
- Existing screens have been built but the transitions between them are confusing or inconsistent.

Do **not** use this skill when:
- The feature is genuinely one screen. Use `ui-blueprint` directly.
- The user wants to spec a single screen in a flow. Reference the flow, then run `ui-blueprint` for that screen.

## Core principle

**The flow is a graph, not a list.** Even simple flows have branches: success path, validation failure, network error, "go back", "skip this step". Capturing only the happy path silently invents the others.

## Pre-flight check

1. **Brief exists** — flow only makes sense in service of a goal.
2. **Number of screens estimated** — even a rough count (3? 7? 15?). Flows over ~10 screens probably need decomposition into sub-flows.
3. **Entry and exit points known** — where does the user start? Where does success deliver them? Where does abandonment leave them?

## Workflow

1. **List every screen** in the flow with a one-line purpose.
2. **Draw the graph** — which screen leads to which, with what trigger.
3. **List the decision points** — places where the path branches based on user input or system state.
4. **List the failure paths** — validation errors, network errors, permission denials, "go back".
5. **List the carried state** — what data does the user accumulate as they move through? What gets persisted, what's transient?
6. **Mark the points of no return** — actions that can't be undone, payments, account deletions.

## Output template

```markdown
---
spec_type: flow
spec_id: <slug>
based_on: brief-<slug>
created: <YYYY-MM-DD>
status: draft
---

# Flow: <descriptive name>

## 1. Goal of the flow
<One sentence — what the user has accomplished when they finish.>

## 2. Entry points
- <How the user arrives at the start of this flow>

## 3. Exit points
- **Success exit:** <where the user lands>
- **Abandon exit:** <where the user lands if they leave mid-flow>
- **Failure exit (terminal):** <if any path ends in a failure that isn't recoverable>

## 4. Screens

| # | Screen | Purpose | Primary action |
|---|---|---|---|
| 1 | Start | <one-line> | <verb> |
| 2 | Step A | <one-line> | <verb> |
| 3 | Step B (decision) | <one-line> | <verb> |
| 4a | Success | <one-line> | (terminal) |
| 4b | Failure | <one-line> | retry / abandon |

## 5. Flow graph

```
[Start]
   ↓ (user clicks "begin")
[Step A]
   ↓ (form submit)
[Step B — decision]
   ├── if X → [Path 1] → [Success]
   ├── if Y → [Path 2] → [Success]
   └── if validation fails → [Step B] (with errors)
[Any step]
   └── (back button) → previous step (state preserved)
[Any step]
   └── (close/cancel) → confirm dialog → exit
```

## 6. Decision points

| At screen | Decision | Branches |
|---|---|---|
| Step B | "Has the user uploaded a document?" | Yes → Path 1; No → Path 2 |
| Step C | "Is the user's account verified?" | Yes → continue; No → verify-email subflow |

## 7. Failure paths

| Trigger | What happens | Recovery |
|---|---|---|
| Validation error on Step A | Stay on Step A, show errors, don't lose other field data | User corrects and resubmits |
| Network error on Step B submit | Stay on Step B, show retry button, preserve form state | Retry, or save-as-draft and try later |
| Session expires mid-flow | Redirect to login with `?continue=<flow-step>` | After login, return to where they were |
| User clicks browser back | Treat as the in-app back button — preserve state | n/a |

## 8. Carried state

| Field | Captured at | Persisted? | Cleared at |
|---|---|---|---|
| Email address | Step A | Yes (server) | Account creation success |
| Selected plan | Step B | No (client only) | On reload |
| Payment method | Step C | Yes (encrypted) | Permanent |

## 9. Points of no return

- <Actions that can't be undone — list them so they can get extra confirmation in the screen-level specs.>

## 10. Open questions
- <Numbered>

## 11. Assumptions
- ⚠️ <flagged>
```

## Rules that prevent hallucinated decisions

1. **Every screen has at least one entry and one exit.** Orphan screens are flow bugs.
2. **Every failure path is named.** Don't write "if it works, go to next screen" without saying what happens if it doesn't work.
3. **Every "back" behavior is specified.** Browser back, in-app back, and "go back to start" can have different behaviors — pick.
4. **Don't invent screens the user didn't approve.** If the flow seems to need a "confirmation" screen but the user didn't mention it, raise it as an open question.

## Acceptance criteria for this skill's output

- [ ] Every screen listed has a purpose and a primary action.
- [ ] A flow graph exists (ASCII or markdown) showing direction of travel.
- [ ] At least one failure path is specified.
- [ ] Carried state is enumerated.
- [ ] Points-of-no-return are listed (or "none" is explicit).
- [ ] Entry and exit points are named.
