---
name: livewire-development
description: Build, refactor, secure, optimize, and test Laravel Livewire v2-v4 components, including state, forms, events, uploads, pagination, Alpine, and v4 formats.
tags:
  - laravel
  - php
---

# Livewire Development

Use this skill for Laravel Livewire implementation, refactoring, debugging, security review, performance work, and tests.

This is the canonical Livewire skill in this repository. It consolidates the former `livewire-patterns` guidance and the public `laravel-livewire` topic into one version-aware workflow.

When the Livewire work is primarily UI/UX design, visual browser iteration, frontend flow shaping, or backend contract alignment, also use `ui-agent-browser`. Use `e2e-playwright` when browser behavior needs durable Playwright coverage.

## Detect The Project First

1. Read `composer.json` and `composer.lock` or run `composer show livewire/livewire` to confirm the installed major version.
2. Inspect existing components, routes, tests, layouts, and `config/livewire.php` before choosing syntax.
3. Detect whether the project uses class-based components, Volt, Livewire v4 single-file components, multi-file components, or a mixture maintained for compatibility.
4. Follow the project's Blade, Alpine, Tailwind, Flux, Filament, and testing conventions when present.
5. Use documentation for the installed major version. Do not introduce v4-only attributes, directives, component paths, or routing into v2/v3 projects.

Read [references/livewire-4.md](references/livewire-4.md) when the project uses Livewire v4 or the task involves v4 migration, component formats, directives, attributes, or routing.

## Implementation Workflow

1. Define one interactive surface and its user-visible states.
2. Choose the component format already used by the project; change formats only for a concrete maintenance benefit.
3. Model the smallest public state needed by the template.
4. Add validation and authorization before persistence or external side effects.
5. Delegate reusable domain workflows to Actions or Services.
6. Shape queries deliberately, add loading and error feedback, and keep DOM identity stable.
7. Test validation, authorization, persistence, events, redirects, and browser-only behavior at the appropriate level.

## Component Boundaries

A component may:

- hold UI and request-shaped state;
- validate input and authorize actions;
- call an Action or Service;
- dispatch focused events;
- coordinate rendering, pagination, uploads, and browser feedback.

A component should not:

- contain long multi-model workflows;
- build provider payloads inline;
- duplicate model-state authorization that belongs in Policies;
- keep secrets, unbounded collections, or large serialized graphs in public state;
- perform slow external calls during rendering;
- bypass a transaction for atomic writes.

## State And Security

- Treat every public property and action parameter as untrusted client input.
- Validate input and authorize the resolved model or operation inside every mutating action.
- Prefer model binding or explicit model lookup followed by a Policy check; never trust a submitted identifier by itself.
- Use `#[Locked]` only where supported to prevent client mutation of identifiers, but keep authorization because locking is not access control.
- Keep helper methods `protected` or `private` when they must not be callable as component actions.
- Store secrets and service credentials in configuration or injected services, never component state.
- Restrict mass-assignment payloads to validated, explicitly selected fields.

Read [references/testing-and-security.md](references/testing-and-security.md) for a secure action pattern, testing matrix, and browser-test boundaries.

## Forms And Data Binding

- Use Livewire validation for component-local forms.
- Use Form objects when a form has substantial state or rules; move reusable domain rules to shared rule objects or services.
- Normalize localized numbers, dates, booleans, and text before applying validation rules.
- Use plain `wire:model` when synchronization on the next action is sufficient.
- Use `.live`, `.blur`, `.change`, debounce, or throttle deliberately; avoid extra requests without a UX requirement.
- Reset or pull state after successful submission when the interaction should return to a clean form.
- Show field-level errors and disable or style in-flight actions to prevent accidental duplicate submissions.

## Queries, Rendering, And Performance

- Eager load relationships used by the view and select only required columns on hot paths.
- Paginate lists instead of storing unbounded Eloquent collections in public properties.
- Keep `render()` and computed properties free of hidden repeated or unbounded queries.
- Cache computed results across requests only when keys, authorization scope, invalidation, and staleness are understood.
- Add stable `wire:key` values to repeated components and dynamic list items.
- Re-key dependent controls when their available options depend on another field.
- Lazy-load below-the-fold or expensive components only when the installed Livewire version supports the chosen API.
- Prefer the project's existing loading-state pattern; Livewire v4 can style automatic `data-loading` attributes, while `wire:loading` remains useful for targeted visibility.

## Events, Nesting, And JavaScript

- Prefer direct props and actions for parent-child relationships; use events for decoupled UI coordination.
- Keep event names local, intention-revealing, and payloads small.
- Use reactive/modelable props only when the installed version supports them and the parent-child synchronization is necessary.
- Use Alpine for truly client-local state such as disclosure, focus, or transitions.
- Use Livewire JavaScript hooks or component scripts for browser APIs and third-party widgets; isolate initialization and cleanup so DOM morphing does not duplicate handlers.
- Use browser tests for focus management, modals, uploads, previews, drag/drop, navigation, and third-party JavaScript integration.

## Testing And Handoff

Test the smallest behavior that proves the risk:

- component rendering and initial state;
- validation failures and normalized input;
- authorization denial for properties and action parameters;
- successful database changes and transaction boundaries;
- dispatched events, redirects, pagination, uploads, and query-string state;
- loading, focus, modal, navigation, and JavaScript behavior in a browser test when component tests cannot prove it.

Use factories and Laravel fakes for files, queues, notifications, mail, and HTTP integrations. Run targeted tests, formatting, static analysis, and frontend checks supported by the project before handoff.

## Related Skills

- `actions-and-services` for reusable workflows and integrations.
- `database-transactions` for atomic multi-write actions.
- `filesystem-uploads` for storage and file lifecycle rules.
- `policies-and-authorization` for model access decisions.
- `ui-agent-browser` for stack-aware UI/UX implementation and browser inspection.
- `e2e-playwright` for durable browser workflow coverage.
- `responsive-ui-testing` for viewport and browser-state coverage.
- `testing` for test selection and handoff verification.
