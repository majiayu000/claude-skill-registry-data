---
name: Fix MobX Reactivity Issues
description: Diagnose and fix common MobX reactivity problems including components not updating, state changes not triggering re-renders, and async update issues. Use when UI doesn't respond to state changes, computed values don't recalculate, or observer components don't re-render.
allowed-tools: Read, Edit, Grep, Glob
---

# Fix MobX Reactivity Issues

This skill helps diagnose and fix the most common MobX reactivity problems in Phoenix/FAAD HMI.

## When to Use

- React components not updating when state changes
- Computed properties not recalculating
- UI shows stale data after async operations
- Observer components not re-rendering
- "Object is not observable" warnings
- State changes appear to work but UI doesn't update

## The Three MobX Commandments

**Reference**: [MOBX_ESSENTIALS.md - Critical Rules](../../ai-guide/_DAILY/MOBX_ESSENTIALS.md#critical-rules)

1. **ALWAYS call `makeObservable(this)` in constructor**
2. **ALWAYS use `runInAction` after `await`**
3. **ALWAYS replace arrays, never mutate**

## Diagnostic Process

### Issue 1: Component Not Updating

**Symptoms**:
- Component shows initial value but doesn't update
- Props change but component doesn't re-render
- State changes in ViewModel but UI stays the same

**Check 1: Missing `observer`**
```tsx
// ❌ WRONG - Component won't react to observable changes
export const MyView = (props: Props) => {
    return <div>{props.viewModel.value}</div>;
};

// ✅ CORRECT - Wrap with observer
import { observer } from 'mobx-react';
export const MyView = observer((props: Props) => {
    return <div>{props.viewModel.value}</div>;
});
```

**Check 2: Missing `makeObservable(this)`**
```typescript
// ❌ WRONG - Properties won't be observable
export class MyViewModel extends BaseViewModel {
    @observable value: string = '';

    constructor(services: IFrameworkServices) {
        super(services);
        // Missing makeObservable(this)!
    }
}

// ✅ CORRECT - Call makeObservable
export class MyViewModel extends BaseViewModel {
    @observable value: string = '';

    constructor(services: IFrameworkServices) {
        super(services);
        makeObservable(this);  // REQUIRED!
    }
}
```

**Reference**: [MOBX_ESSENTIALS.md - Constructor Pattern](../../ai-guide/_DAILY/MOBX_ESSENTIALS.md#constructor-pattern)

### Issue 2: Async Updates Not Working

**Symptoms**:
- State updates after await don't trigger re-renders
- Console shows "Since strict-mode is enabled..." warning
- Async operations seem to work but UI doesn't update

**Problem: Missing `runInAction`**
```typescript
// ❌ WRONG - State change after await is outside action
@action async loadData(): Promise<void> {
    const data = await fetchData();
    this.data = data;  // Error! Not in action context
}

// ✅ CORRECT - Use runInAction after await
@action async loadData(): Promise<void> {
    const data = await fetchData();
    runInAction(() => {
        this.data = data;  // Now properly tracked
    });
}
```

**Alternative Pattern**:
```typescript
// ✅ Also correct - Inline runInAction
@action async loadData(): Promise<void> {
    const data = await fetchData();
    runInAction(() => this.data = data);
}

// ✅ For multiple updates
@action async loadMultiple(): Promise<void> {
    const [data1, data2] = await Promise.all([fetch1(), fetch2()]);
    runInAction(() => {
        this.data1 = data1;
        this.data2 = data2;
        this.isLoading = false;
    });
}
```

**Reference**: [MOBX_ESSENTIALS.md - Async Operations](../../ai-guide/_DAILY/MOBX_ESSENTIALS.md#async-operations)

### Issue 3: Array Updates Not Detected

**Symptoms**:
- Push/splice/sort on array doesn't trigger update
- Component shows old array contents
- Array seems to update but UI doesn't reflect it

**Problem: Mutating arrays instead of replacing**
```typescript
// ❌ WRONG - Mutating array (MobX may not track)
@action addItem(item: Item): void {
    this.items.push(item);  // Mutation - unreliable
}

@action removeItem(id: string): void {
    const index = this.items.findIndex(i => i.id === id);
    this.items.splice(index, 1);  // Mutation - unreliable
}

// ✅ CORRECT - Replace array
@action addItem(item: Item): void {
    this.items = [...this.items, item];  // Replacement - reliable
}

@action removeItem(id: string): void {
    this.items = this.items.filter(i => i.id !== id);  // Replacement - reliable
}

@action sortItems(): void {
    this.items = [...this.items].sort((a, b) => a.name.localeCompare(b.name));
}
```

**Reference**: [MOBX_ESSENTIALS.md - Observable Collections](../../ai-guide/_DAILY/MOBX_ESSENTIALS.md#observable-collections)

### Issue 4: Computed Not Recalculating

**Symptoms**:
- Computed value shows stale data
- Dependencies change but computed doesn't update
- Computed seems to calculate once and never again

**Check 1: Missing `@computed` decorator**
```typescript
// ❌ WRONG - Plain getter, calculates every access
get fullName(): string {
    return `${this.firstName} ${this.lastName}`;
}

// ✅ CORRECT - Computed, cached and reactive
@computed get fullName(): string {
    return `${this.firstName} ${this.lastName}`;
}
```

**Check 2: Not accessing observable properties**
```typescript
// ❌ WRONG - Accesses non-observable property
@observable items: Item[] = [];
private itemCount: number = 0;  // Not observable!

@computed get displayCount(): string {
    return `${this.itemCount} items`;  // Won't react to changes!
}

// ✅ CORRECT - Accesses observable
@computed get displayCount(): string {
    return `${this.items.length} items`;  // Reacts to items changes
}
```

**Check 3: Side effects in computed**
```typescript
// ❌ WRONG - Computed should be pure
@computed get activeItems(): Item[] {
    console.log('Calculating active items');  // Side effect - not terrible but avoid
    this.lastCalculated = Date.now();  // Side effect - WRONG!
    return this.items.filter(i => i.isActive);
}

// ✅ CORRECT - Pure computation
@computed get activeItems(): Item[] {
    return this.items.filter(i => i.isActive);
}
```

**Reference**: [MOBX_ESSENTIALS.md - Computed Properties](../../ai-guide/_DAILY/MOBX_ESSENTIALS.md#computed-properties)

### Issue 5: Double Decorator Error

**Symptoms**:
- Error: "The field is already decorated with '@action'"
- Build fails with decorator conflict
- Overriding method from base class

**Problem: Using @action on override**
```typescript
// Base class
export class BaseViewModel {
    @action doSomething(): void {
        // base implementation
    }
}

// ❌ WRONG - Double decoration!
export class MyViewModel extends BaseViewModel {
    @override
    @action doSomething(): void {  // Error!
        // overridden implementation
    }
}

// ✅ CORRECT - Only @override
export class MyViewModel extends BaseViewModel {
    @override
    doSomething(): void {
        // overridden implementation
    }
}
```

**Reference**: [MOBX_ESSENTIALS.md - Override Decorator](../../ai-guide/_DAILY/MOBX_ESSENTIALS.md#override-decorator)

### Issue 6: Performance - Unnecessary Re-computation

**Symptoms**:
- Property VMs with configuration reconfigure on every access
- Performance issues with complex property VM setup
- Derived values recalculate unnecessarily

**Problem: Missing @computed on getters with logic**

```typescript
// ❌ WRONG - Reconfigures every access
get modeVM(): ICommandedVM<ModeType, IEnumFormatOptions<ModeType>> {
    const vm = this.createPropertyVM('mode', CommandedEnumViewModel<ModeType>);
    vm.configure({  // This runs every time getter is accessed!
        labelConverter: ModeTypeLabel,
        defaultValue: ModeType.AUTO
    });
    return vm;
}

// ✅ CORRECT - Memoized with @computed
@computed
get modeVM(): ICommandedVM<ModeType, IEnumFormatOptions<ModeType>> {
    const vm = this.createPropertyVM('mode', CommandedEnumViewModel<ModeType>);
    vm.configure({  // Only runs when dependencies change
        labelConverter: ModeTypeLabel,
        defaultValue: ModeType.AUTO
    });
    return vm;
}

// ✅ Also correct - Simple forwarding, @computed optional
get nameVM(): IPropertyVM<string, IStringFormatOptions> {
    return this.createPropertyVM('name', StringViewModel);  // No config, @computed optional
}
```

**When to use @computed**:
- Getter includes `.configure()` calls (prevents re-running)
- Getter derives/computes from observables (required for reactivity)
- Getter filters/maps data (required for reactivity)

**When @computed is optional**:
- Simple forwarding to `createPropertyVM()` without configuration

**Reference**: [MOBX_ESSENTIALS.md - Computed Properties](../../ai-guide/_DAILY/MOBX_ESSENTIALS.md#computed-properties)

## Common Patterns That Look Wrong But Are Correct

### Pattern 1: Computed returning new object each time
```typescript
// This IS correct - MobX tracks the inputs, not the output
@computed get position(): { x: number; y: number } {
    return { x: this.x, y: this.y };  // New object each time - OK!
}
```

### Pattern 2: Accessing props in render
```tsx
// This IS correct in observer components
export const MyView = observer(({ viewModel }: Props) => {
    // Accessing observables in render - OK!
    return <div>{viewModel.value}</div>;
});
```

### Pattern 3: Nested observable access
```typescript
// This IS correct - MobX tracks deep access
@observable user: User | null = null;

@computed get userName(): string {
    return this.user?.profile?.name ?? 'Unknown';  // Deep access - OK!
}
```

## Diagnostic Checklist

Run through this checklist systematically:

- [ ] Component wrapped with `observer()`
- [ ] ViewModel calls `makeObservable(this)` in constructor
- [ ] Properties decorated with `@observable`
- [ ] Methods modifying state decorated with `@action`
- [ ] Async updates use `runInAction` after `await`
- [ ] Arrays replaced, not mutated
- [ ] Computed getters use `@computed` decorator
- [ ] No `@action` on overridden methods (use `@override` only)
- [ ] Component accesses observable properties (not local copies)

## Quick Fixes by Symptom

| Symptom | Most Likely Cause | Quick Fix |
|---------|------------------|-----------|
| Component never updates | Missing `observer()` | Wrap component with `observer()` |
| Initial render only | Missing `makeObservable(this)` | Add to constructor |
| Async updates fail | Missing `runInAction` | Wrap updates after `await` |
| Array changes invisible | Mutating arrays | Replace arrays instead |
| Computed stale | Not accessing observables | Access `@observable` properties |
| Decorator error | `@action` on override | Use only `@override` |
| Property VM reconfigures | Missing `@computed` | Add `@computed` to getter with config |

## Debugging Tools

```typescript
// Add to ViewModel for debugging
@computed get debugState(): string {
    return JSON.stringify({
        value: this.value,
        items: this.items.length,
        isLoading: this.isLoading
    }, null, 2);
}

// In component
console.log('---- ViewModel state:', viewModel.debugState);

// Check if object is observable
import { isObservable } from 'mobx';
console.log('Is observable?', isObservable(viewModel.items));
```

**Reference**: [MOBX_ESSENTIALS.md - Debugging](../../ai-guide/_DAILY/MOBX_ESSENTIALS.md#debugging)

## When to Escalate

If none of these fixes work, check:
1. Is the ViewModel being recreated unnecessarily? (should be stable reference)
2. Is there a parent component not wrapped with `observer()`?
3. Are you using `toJS()` somewhere, breaking reactivity?
4. Is the observable being replaced with a plain object?

## Ask User

- What specifically isn't updating? (component, computed, etc.)
- Are there any console warnings or errors?
- Does the state actually change in the ViewModel? (check with console.log)
- Is this after an async operation?

## Key References

- [MOBX_ESSENTIALS.md](../../ai-guide/_DAILY/MOBX_ESSENTIALS.md) - Complete MobX patterns
- [COMMON_PITFALLS.md](../../ai-guide/_DAILY/COMMON_PITFALLS.md) - Known issues and fixes
- [TESTING_GUIDE.md](../../ai-guide/_DAILY/TESTING_GUIDE.md) - Testing MobX components