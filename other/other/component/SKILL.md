---
name: component
description: Generate a standalone Angular component with signals and modern patterns
argument-hint: <library> <component-name>
---

# Generate Angular Component

Create a standalone Angular component following Momentum CMS conventions.

## Arguments
- First argument: Library path (e.g., "admin", "admin/components")
- Second argument: Component name (e.g., "data-table", "field-renderer")

## Steps

1. Create component files in `libs/<library>/src/lib/<component>/`:
   - `<component>.ts` (component class)
   - `<component>.html` (template, if complex)
   - `<component>.css` (styles)
   - `<component>.spec.ts` (tests)

2. Use this template for the component:
```typescript
import { Component, input, output, computed, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'mcms-<component-name>',
  standalone: true,
  imports: [CommonModule],
  template: `
    <!-- Template here -->
  `,
  styles: [`
    :host {
      display: block;
    }
  `],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class <PascalName>Component {
  // Signal inputs
  data = input.required<any>();

  // Optional inputs with defaults
  disabled = input(false);

  // Signal outputs
  valueChange = output<any>();

  // Internal state
  private _loading = signal(false);

  // Computed values
  readonly loading = this._loading.asReadonly();
  readonly hasData = computed(() => !!this.data());

  // Injected services
  private readonly http = inject(HttpClient);
}
```

3. Export from library's `index.ts`:
```typescript
export { <PascalName>Component } from './lib/<component>/<component>';
```

## Key Conventions
- Always use `standalone: true`
- Always use `ChangeDetectionStrategy.OnPush`
- Use `input()` and `input.required()` for inputs
- Use `output()` for outputs
- Use `signal()` for internal state
- Use `computed()` for derived values
- Use `inject()` for dependency injection
- Use `@for`/`@if`/`@switch` control flow
- Prefix selectors with `mcms-`
