---
name: component-structure-new
kind: pattern
rule: component-structure
description: Pattern of rule component-structure. Load when creating or editing *.component.ts — the ready-made decorator with property order, import grouping, class field layout, template conventions and qa-dataid. Not for state and streams — that is pattern angular-patterns-state.
---
<!-- rt-kit v0.34.0 · patterns/component-structure-new.md · a1cf27649e96 · правится надстройкой, не здесь -->

# The component file

Pattern of the rule `component-structure`. What must be true — the law
`docs/constitution/frontend-application.md`.

## When to use

- A new component is created.
- The decorator, the import list or the template of an existing one is edited.

## The decorator: order of properties

```typescript
@Component({
    selector: '<prefix>-component-name', // 1. selector
    templateUrl: './component-name.component.html', // 2. template
    styleUrl: './component-name.component.scss', // 3. style, singular
    changeDetection: ChangeDetectionStrategy.OnPush, // 4. change detection strategy
    imports: [
        // 5. imports, in groups
        // angular
        FormsModule,

        // rt-tools
        BlockDirective,
        ElemDirective,

        // components
        SomeChildComponent,
    ],
    providers: [], // 6. providers
    host: { class: '<prefix>-component-name' }, // 7. host bindings
})
export class ComponentNameComponent {
    readonly #someService: SomeService = inject(SomeService);

    public readonly data: InputSignal<Item[]> = input.required<Item[]>();
    public readonly save: OutputEmitterRef<void> = output<void>();

    protected readonly myButton: Signal<ElementRef | undefined> = viewChild<ElementRef>('button');
    protected readonly items: WritableSignal<Item[]> = signal<Item[]>([]);
    protected readonly itemCount: Signal<number> = computed((): number => this.items().length);
}
```

The grouping comments in `imports` are mandatory: `// angular`, `// rt-tools`, `// components`,
`// directives`, `// pipes`.

## The template

- Self-closing tags on components without content: `<<prefix>-gallery />`.
- No extra wrappers — `:host` works as the root, the block class comes with
  `host: { class: … }`.
- A complex template declares the block `<ng-container rtBlock="component-name">` at the root.
- One component in both branches of an `@if` is a conditional binding:

```html
<!-- ✗ -->
@if (isRangeMode()) { <<prefix>-calendar [rangeMode]="true" /> } @else { <<prefix>-calendar [rangeMode]="false" /> }

<!-- ✓ -->
<<prefix>-calendar [rangeMode]="isRangeMode()" />
```

- Scrolling within the document — through the router, not `href="#id"`:

```html
<a fragment="booking" [routerLink]="[]">…</a>
```

## `qa-dataid` — on every interactive element

```html
<button <prefix>Button qa-dataid="calendar-retry-prices" type="button" (click)="retryPrices.emit()">Повторить</button>
<div rtElem="grid" qa-dataid="admin-calendar-grid"></div>
```

- The value — kebab-case by the meaning of the element, without the name of the wrapping
  component: `calendar-day`, `booking-submit`.
- Uniqueness — within the screen; repeating list elements carry one anchor and differ through
  `data-*` (`[attr.data-iso]`, `[attr.data-state]`).
- A decorative element is marked `qa-skip` on the tag itself.
- On a component of the kit the anchor sits on the host, while for a directive the host is the
  element itself. The component's test aims inside — `[qa-dataid="x"] button` — and for a
  directive that lands in emptiness: there is no nested button under the host. They differ only
  in what the tag is marked with, and the anchor value does not show it.
- Replacing a wrapper component with a directive starts with a search for the anchor over the
  end-to-end suites. The markup looks whole after such a replacement, the anchor stays the same,
  and the test goes red on an empty selection — and it goes red for whoever did not touch the
  markup.

## Common misses

- `selector: 'app-component'` instead of `<prefix>-component`.
- `styleUrls: ['./component.scss']` instead of `styleUrl` — the plural is wrong here.
- A method call in a binding: `{{ getTotal() }}` is refused by the linter. The replacement is
  `computed()`, and where the value comes from the template context — a pure pipe.
- A wrapper that exists only to be a flex or grid container around all the children: its layout
  moves to `:host`.
- A deep relative import between libs instead of `@<scope>/<family>/<domain>/<layer>`.
- Own markup instead of a ready-made kit component — rule `reuse-first`.
