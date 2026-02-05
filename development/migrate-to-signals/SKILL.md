---
name: migrate-to-signals
description: Convert RxJS observables or decorator-based code to Angular signals. Use when refactoring to signals, converting @Input/@Output to signal functions, or replacing BehaviorSubject with signal().
---

# Migrate to Signals Skill

Convert legacy Angular patterns to modern signal-based APIs.

## Input/Output Decorators → Signal Functions

### Before

```typescript
@Input() name: string = '';
@Input() count!: number;
@Output() clicked = new EventEmitter<void>();
```

### After

```typescript
readonly name = input<string>('');
readonly count = input.required<number>();
readonly clicked = output<void>();
```

### Key Changes

- `input()` for optional inputs with defaults
- `input.required<T>()` for required inputs
- `output<T>()` replaces `EventEmitter`
- Add `readonly` modifier
- Import from `@angular/core`: `input`, `output`

## ViewChild/ContentChild → Signal Queries

### Before

```typescript
@ViewChild('myRef') myRef!: ElementRef;
@ViewChild(ChildComponent) child!: ChildComponent;
```

### After

```typescript
readonly myRef = viewChild<ElementRef>('myRef');
readonly child = viewChild(ChildComponent);
// Access: this.myRef()?.nativeElement
```

## BehaviorSubject → signal()

### Before

```typescript
private items$ = new BehaviorSubject<Item[]>([]);
items = this.items$.asObservable();

addItem(item: Item) {
  this.items$.next([...this.items$.value, item]);
}
```

### After

```typescript
readonly items = signal<Item[]>([]);

addItem(item: Item) {
  this.items.update(current => [...current, item]);
}
```

## Observable Derived State → computed()

### Before

```typescript
totalCount$ = this.items$.pipe(map((items) => items.length));
```

### After

```typescript
readonly totalCount = computed(() => this.items().length);
```

## Subscriptions → effect()

### Before

```typescript
ngOnInit() {
  this.items$.subscribe(items => {
    console.log('Items changed:', items);
  });
}
```

### After

```typescript
constructor() {
  effect(() => {
    console.log('Items changed:', this.items());
  });
}
```

## Observable to Signal (interop)

```typescript
import { toSignal } from '@angular/core/rxjs-interop';

// Convert observable to signal
readonly data = toSignal(this.http.get<Data[]>('/api/data'), { initialValue: [] });
```

## Template Changes

### Before

```html
<div *ngIf="loading">Loading...</div>
<div *ngFor="let item of items$ | async">{{ item.name }}</div>
```

### After

```html
@if (loading()) {
<div>Loading...</div>
} @for (item of items(); track item.id) {
<div>{{ item.name }}</div>
}
```

## Testing Signal Inputs

```typescript
// Set input values in tests
fixture.componentRef.setInput('count', 5);
fixture.detectChanges();
```

## Checklist

1. Replace `@Input()` → `input()` or `input.required()`
2. Replace `@Output()` → `output()`
3. Replace `@ViewChild()` → `viewChild()`
4. Replace `BehaviorSubject` → `signal()`
5. Replace derived observables → `computed()`
6. Replace subscriptions for side effects → `effect()`
7. Update templates: `*ngIf` → `@if`, `*ngFor` → `@for`
8. Remove `| async` pipes (signals auto-unwrap)
9. Run tests: `npm test`
