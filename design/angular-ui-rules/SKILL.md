---
name: angular-ui-rules
description: "The short Angular, Angular Material and Tailwind rule list, keyed by Rule ID, that the Angular agents preload. Use when: writing or reviewing Angular components, templates, state services or styles; or when an agent must cite a Rule ID. Points at the full rule documents installed by the angular-tailwind add-on."
user_invocable: false
---

Rule set: angular-ui-rules

# Angular UI rules (short list)

This is the short list. The full text of each rule, with examples, lives in the rule documents the `angular-tailwind` add-on installs. Cite the Rule ID when you apply or report a rule.

**Which rule wins.** The project's own instructions win over every rule document. A document the project wrote and lists in `review.documents` wins over this plugin document where they disagree. For what it checks, the guard's verdict is final.

**When the documents are missing.** Read the `review.documents` slot of `.claude/project-profile.md`. If the add-on's documents are not listed there, the add-on is not installed: say so once, and work from the short list below alone. Do not invent a document path.

**Per-app rules.** Before editing an application, read that application's `.app-rules.json` (the roots are the `frontend.roots` slot), including its `advisorRemindersAppendix`. Those entries apply on top of this list.

## Components and templates
- **A-001** Components are standalone.
- **A-002** `ChangeDetectionStrategy.OnPush`.
- **A-003** `templateUrl` and `styleUrl` in separate files; never inline `template:` or `styles:`.
- **A-004** `inject()`, not constructor injection.
- **A-005** `input()` / `input.required()`, not `@Input()`.
- **A-006** `@if`, `@for`, `@switch`; never `*ngIf` / `*ngFor`.
- **A-007** Every `@for` has a `track` expression.

## State and signals
- **A-009** State services keep private signals and expose them with `.asReadonly()`.
- **A-011** Clean up subscriptions (`takeUntilDestroyed`, `toSignal`).
- **A-012** No async pipe.
- **A-013** No `any`; use `unknown` and a type guard.

## Styling
- **T-001** No static `style` for layout, spacing or sizing; use Tailwind utilities.
- **T-003** No `text-gray-*` / `bg-gray-*`.
- **T-004** No hard-coded hex colours; use the theme-bridged utilities (`text-primary`, `bg-surface-container`, `border-outline-variant`).
- **T-010** SCSS files stay near-empty: `:host ::ng-deep`, `@keyframes`, `@media` / `@supports`, `@apply`.
- **T-011** A Material override that serves one component goes in that component's stylesheet.
- **T-012** Scrollable containers use the global `scroll-edge` classes, never inline `overflow-y-auto` or `sticky`.
- **T-014** Keep the height chain intact down to a scrolling child.
- **T-022** Do not use the classes an application's `.app-rules.json` bans.

## Data
- **Response envelope.** Check `<the success flag of the project's response envelope>` (named in the project's own handbook listed in `review.documents`) before reading the value.
- **Generated models.** Never hand-edit generated API or hub models; they regenerate from the server code.

## Layout (advisory)
For screen layout and density, `agentic-auto-improve:application-design` and `agentic-auto-improve:website-design` are advisory references; they do not override the rules above.
