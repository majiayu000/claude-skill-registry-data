---
name: angular-patterns-state
kind: pattern
rule: angular-patterns
description: Pattern of rule angular-patterns. Load when declaring state and streams in an Angular class — ready-made signals, derived values, service state, a long-lived subscription with an action source. Not for the layout of a component file — that is rule component-structure.
---
<!-- rt-kit v0.34.0 · patterns/angular-patterns-state.md · c3f7838aa426 · правится надстройкой, не здесь -->

# State and streams

Pattern of the rule `angular-patterns`. What must be true — the law
`docs/constitution/frontend-application.md`.

## When to use

- The state of a component or a service is declared.
- A stream appears that has to be subscribed to.
- A value is computed from another value.

## The signal input and output API

```typescript
public readonly data: InputSignal<Item[]> = input.required<Item[]>();
public readonly isMobile: InputSignal<boolean | undefined> = input<boolean>();
public readonly save: OutputEmitterRef<void> = output<void>();

protected readonly myButton: Signal<ElementRef | undefined> = viewChild<ElementRef>('button');
```

The decorators `@Input()`, `@Output()`, `@ViewChild()`, `@ContentChild()` and their plural pairs
are not in the tree.

## A derived value — `computed`, not an effect

```typescript
protected readonly items: WritableSignal<Item[]> = signal<Item[]>([]);
protected readonly itemCount: Signal<number> = computed((): number => this.items().length);
protected readonly hasItems: Signal<boolean> = computed((): boolean => this.itemCount() > 0);
```

```typescript
✗ effect((): void => { this.count.set(this.items().length); });
✓ protected readonly count: Signal<number> = computed((): number => this.items().length);
```

No getter in a component: it is recomputed on every redraw, and its cost is visible nowhere in
the code.

## Service state

Outward — reading only:

```typescript
@Injectable({ providedIn: 'root' })
export class DomainStateService {
    readonly #items: WritableSignal<Item[]> = signal<Item[]>([]);

    public readonly items: Signal<Item[]> = this.#items.asReadonly();
    public readonly itemCount: Signal<number> = computed((): number => this.#items().length);

    public addItem(item: Item): void {
        this.#items.update((items: Item[]): Item[] => [...items, item]);
    }
}
```

## A subscription is declared once

The action method pushes a value into the source, the subscription lives in the constructor:

```typescript
readonly #loadSource: Subject<void> = new Subject<void>();
readonly #destroyRef: DestroyRef = inject(DestroyRef);

constructor() {
    this.#loadSource
        .pipe(
            switchMap((): Observable<IPromoCode.ListResult> => this.#api.getList(this.#query())),
            takeUntilDestroyed(this.#destroyRef)
        )
        .subscribe();
}

protected reload(): void {
    this.#loadSource.next();
}
```

The operator is chosen by what to do with the previous request: a list takes the last response
(`switchMap`), a button does not spawn duplicates (`exhaustMap`), neighbouring rows go
independently (`mergeMap`).

## Common misses

- `.subscribe()` inside a method: the linter rule refuses it, and with it the race of responses
  on fast presses is refused too.
- A subscription without `takeUntilDestroyed`: it outlives its owner and keeps the destroyed
  screen in memory.
- A stream field without the suffix `Source`: the stream and the value cannot be told apart in
  code.
- `inject()` instead of constructor parameters — everywhere, including base classes.
- `untracked()` where the effect needs no dependency on a signal: without it the effect wakes on
  every foreign change.
