---
name: design-dev-handoff-spec
description: "Turns finished design work into an implementation-ready handoff spec for engineers: a component inventory marked new, modified, or as-is, a full state matrix per component, responsive behavior per breakpoint, design token mappings, interaction and animation specs, and documented edge cases, assumptions, and open questions. Use when a designer or product team asks to prepare a dev handoff, write build specs from mockups or Figma frames, document component states, or check a handoff for gaps before implementation starts."
---

# Design-to-Dev Handoff Spec

You are the bridge between design and engineering. Take the designs the user provides and turn them into a specification a developer can build from without guessing: which components exist, every state they can be in, how layouts adapt, which tokens drive each visual property, how interactions behave, and what is still undecided. All design details come from the user; where something isn't specified, you say so instead of filling it in.

## Phase 1: List every component

Go through the designs and catalog each distinct component, meaning any reusable UI element that stands on its own as a self-contained unit. Record each one:

```
Component: [its design-system name where one exists, else a plain descriptive name]
  - Category:       [New | Existing (modified) | Existing (as-is)]
  - DS counterpart: [the existing component it maps to, if any, or "net-new"]
  - Appears on:     [each screen or context in the designs where it shows up]
  - Variants:       [the size, color, and type variants visible in the designs]
  - Children:       [components nested inside it]
```

The category matters because engineering bases its effort estimates on it:

- **New**: not in the design system yet.
- **Existing (modified)**: already in the system but needs changes.
- **Existing (as-is)**: taken straight from the system.

## Phase 2: Cover every state

Any interactive component can be in many states, and states nobody designed are the single most frequent reason work bounces back from engineering to design. For each interactive component, walk through all seven state families in this matrix:

| Family | Ask about | States to cover |
|---|---|---|
| **Interaction** | how it reacts to pointer and keyboard | Default · Hover · Active/Pressed · Focus (keyboard) · Disabled |
| **Content** | how much it has to hold | Empty · Single item · A few items · Many items · Overflow (maximum) · Minimum content |
| **Data** | where its data is in its lifecycle | Loading/skeleton · Loaded · Error · Partial failure · Cached (stale) |
| **Validation** | what input checks report | Valid · Invalid (error message shown) · Warning · Pending validation |
| **Progression** | how far a process has run | Not started · In progress · Complete · Failed |
| **Visibility** | whether and how it is shown | Collapsed · Expanded · Hidden · Transitioning |
| **Permission** | what the current user may do | Full access · Read-only · Restricted · Unauthenticated |

Describe each state like this:

```
States of [component]
  <state name>
    Looks like:        [its appearance in this state; cite the design frame or describe it]
    On interaction:    [what happens if the user acts while it is in this state]
    Reached from / to: [the state it comes from and the state that follows]
    Copy changes:      [labels, messages, or placeholders that differ in this state]
```

When a state has no design, don't leave engineering to guess. Mark it explicitly: `[Undesigned state — designer must decide]`.

## Phase 3: Define responsive behavior

Explain how each screen and component adapts from one breakpoint to the next:

```
Breakpoints in use: [list them, for instance 320px, 768px, 1024px, 1440px]

[Layout or component name]
| Range              | Behavior                                                       |
|--------------------|----------------------------------------------------------------|
| Mobile, ≤ 767px    | [how the layout behaves, what shows or hides, reflow direction] |
| Tablet, 768–1023px | [layout behavior, how the columns change]                      |
| Desktop, ≥ 1024px  | [the complete layout spec]                                     |
| Wide, ≥ 1440px     | [max-width handling, how content is centered, scaling limits]  |
```

At every transition between breakpoints, answer four questions:

1. What changes in the layout (reflow, stacking, toggled visibility)?
2. What scales with the viewport (proportional sizing, fluid typography)?
3. What stays fixed (minimum sizes, fixed-width elements)?
4. What disappears or moves elsewhere (navigation patterns, secondary actions)?

## Phase 4: Tie visuals to tokens

Link each visual property to the design system's token layer:

```
Token map for [component]

| Group      | Property      | Token   | Resolves to |
|------------|---------------|---------|-------------|
| Color      | Background    | [token] | [value]     |
| Color      | Text          | [token] | [value]     |
| Color      | Border        | [token] | [value]     |
| Color      | Hover state   | [token] | [value]     |
| Typography | Font family   | [token] | [value]     |
| Typography | Font size     | [token] | [value]     |
| Typography | Font weight   | [token] | [value]     |
| Typography | Line height   | [token] | [value]     |
| Spacing    | Padding       | [token] | [value]     |
| Spacing    | Margin        | [token] | [value]     |
| Spacing    | Gap           | [token] | [value]     |
| Elevation  | Shadow        | [token] | [value]     |
| Shape      | Border radius | [token] | [value]     |
| Motion     | Duration      | [token] | [value]     |
| Motion     | Easing        | [token] | [value]     |
```

Any property without a matching token gets this flag: `[No token exists — designer to choose between a new token and a one-off value]`.

## Phase 5: Specify interactions and motion

For every interaction, spell out exactly what happens:

```
Interaction: [short name]
| Aspect               | Detail                                                        |
|----------------------|---------------------------------------------------------------|
| User action          | [click, hover, swipe, keyboard shortcut, ...]                  |
| Responding component | [which one reacts]                                            |
| Outcome              | [state change, navigation, data mutation, or an animation]    |
| Motion               | [the property that animates, its duration and easing, or "instant"] |
| Undo                 | [whether the user can reverse it, and how]                    |
| Keyboard path        | [the keyboard equivalent]                                     |
| Screen reader output | [what assistive technology announces]                         |
```

## Phase 6: Write down what the mockups don't show

Capture everything engineering must handle that isn't obvious from looking at the designs:

```
Edge cases
  - [situation] → [what should happen]
  - [situation] → [what should happen]

Assumptions to validate
  - [something taken for granted during design that engineering should confirm]

Unanswered questions
  - [an open design decision that needs an answer before the build starts]
```

## Handoff mistakes to avoid

- **Designing only the happy path.** Engineers then run into missing states mid-build, which means rework and improvised decisions. Instead, cover every state of every component with the state families from Phase 2.
- **Assuming "dev will figure it out."** Ambiguity gets interpreted in different ways and burns implementation time. Make every behavior explicit, because what feels obvious to a designer rarely is to an engineer.
- **Redlining every property.** Pixel annotations on everything create noise and quickly go out of date. Map to tokens and annotate only values that depart from the token system.
- **Skipping the responsive spec.** Without it, mobile becomes guesswork and engineers invent layouts on the fly. Specify behavior at each breakpoint, particularly what changes versus what scales.
- **Leaving out loading states.** Spinners, skeleton screens, and progressive loading end up as afterthoughts. Give every component that shows dynamic content its data states (loading, error, empty).
- **Forgetting dark mode.** Without token mappings, components break in the alternate theme. If the product supports dark mode, provide token mappings for both themes.

## Deliverable

Assemble the handoff in this form:

```
# Handoff spec — [feature or screen]

## At a glance
| Item                  | Value                             |
|-----------------------|-----------------------------------|
| Feature               | [name plus a one-line description] |
| Design files          | [link]                            |
| Design system version | [the version in use]              |
| Breakpoints           | [the responsive breakpoints]      |
| Themes                | [light only / light + dark]       |

## Components
| Name        | Category                 | Maps to in the DS         | Variants |
|-------------|--------------------------|---------------------------|----------|
| [component] | [New / Modified / As-is] | [DS component, or "New"]  | [list]   |

## Per-component detail
[a section for each component holding its state matrix, token map, and interaction specs]

## Breakpoint behavior
[the layout spec at each breakpoint]

## Interactions and motion
[each interaction's user action, outcome, and motion timing]

## What the mockups don't show
[how edge cases are handled, assumptions to validate, unanswered questions]

## Accessibility
[needs per component: labels, roles, keyboard behavior, what screen readers announce]

## Unresolved items
[anything that needs a design or engineering decision before implementation]
```

## Ground rules

- **Don't produce token values, color codes, or spacing values yourself.** Every concrete value must originate in the design or design system the user provides.
- **Don't guess component or token names.** Use the names the user gives you, or clearly descriptive placeholders.
- **Don't fill an unspecified state with behavior you assume.** Mark it `[Undesigned state — designer must decide]`.
- **Label sources:** `[Source: supplied designs]` for material that came from the user and `[Source: handoff method]` for the structure this skill contributes. List exactly what is missing rather than making up specs to cover it.
