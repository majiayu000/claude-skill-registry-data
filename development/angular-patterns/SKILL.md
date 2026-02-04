---
name: angular-patterns
description: Angular 21 development patterns for this project. Use when writing or reviewing Angular components, services, templates, or tests.
---

# Angular Patterns

## Component Design

- Use `input()`, `output()`, `viewChild()`, `contentChild()` signal-based functions instead of decorators
- Do not add `standalone: true`—it's the default in Angular 20+
- Use `ChangeDetectionStrategy.OnPush` for performance
- Use Angular control flow syntax (`@if`, `@for`, `@switch`) instead of `*ngIf`/`*ngFor`
- Use `host` object in decorator instead of `@HostBinding`/`@HostListener`
- Use `class`/`style` bindings instead of `ngClass`/`ngStyle`
- Use `providedIn: 'root'` for singleton services

## State Management

- Use `signal()`, `computed()`, and `effect()` for reactive state
- Use `update()` or `set()` on signals—never `mutate()`
- Use `toSignal()` when interoperating with RxJS observables

## Templates

- Keep templates simple; move logic to component classes
- No arrow functions in templates (not supported)
- No globals like `new Date()` in templates
- Use `@for` with `track` for efficient list rendering

## Styling

- Use Tailwind CSS with `@apply` for composite styles
- Reference styles: `@reference '../../../styles.css';`
- Support dark mode via `.dark:` variants

## Testing

- Use `TestBed` with standalone component imports
- Set inputs via `fixture.componentRef.setInput('name', value)`
- Mock HTTP requests and dependencies
- Run with `ng test --include path/to/file.spec.ts`

## Accessibility

- Must pass AXE checks and meet WCAG AA standards
- Ensure proper focus management and ARIA attributes
