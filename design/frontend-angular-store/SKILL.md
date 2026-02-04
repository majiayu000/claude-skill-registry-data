---
name: angular-store
description: Use when implementing state management with PlatformVmStore for complex components requiring reactive state, effects, and selectors.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Angular Store Development Workflow

## When to Use This Skill
- List components with CRUD operations
- Complex state with multiple data sources
- Shared state between components
- Caching and reloading patterns

## Pre-Flight Checklist
- [ ] Identify state shape (what data is needed)
- [ ] Identify side effects (API calls, etc.)
- [ ] Search similar stores: `grep "{Feature}Store" --include="*.ts"`
- [ ] Determine caching requirements

## File Location
```
src/PlatformExampleAppWeb/apps/{app-name}/src/app/
└── features/
    └── {feature}/
        ├── {feature}.store.ts
        └── {feature}.component.ts
```

## Store Architecture

```
PlatformVmStore<TState>
├── State: TState (reactive signal)
├── Selectors: select() → Signal<T>
├── Effects: effectSimple() → side effects
├── Updaters: updateState() → mutations
└── Loading/Error: observerLoadingErrorState()
```

## Pattern 1: Basic CRUD Store

```typescript
// {feature}-list.store.ts
import { Injectable } from '@angular/core';
import { PlatformVmStore } from '@libs/platform-core';

// ═══════════════════════════════════════════════════════════════════════════
// STATE INTERFACE
// ═══════════════════════════════════════════════════════════════════════════

export interface FeatureListState {
  items: FeatureDto[];
  selectedItem?: FeatureDto;
  filters: FeatureFilters;
  pagination: PaginationState;
}

export interface FeatureFilters {
  searchText?: string;
  status?: FeatureStatus[];
  dateRange?: DateRange;
}

export interface PaginationState {
  pageIndex: number;
  pageSize: number;
  totalCount: number;
}

// ═══════════════════════════════════════════════════════════════════════════
// STORE IMPLEMENTATION
// ═══════════════════════════════════════════════════════════════════════════

@Injectable()
export class FeatureListStore extends PlatformVmStore<FeatureListState> {

  // ─────────────────────────────────────────────────────────────────────────
  // CONFIGURATION
  // ─────────────────────────────────────────────────────────────────────────

  // State factory
  protected override vmConstructor = (data?: Partial<FeatureListState>) => ({
    items: [],
    filters: {},
    pagination: { pageIndex: 0, pageSize: 20, totalCount: 0 },
    ...data
  } as FeatureListState);

  // Optional: Enable caching
  protected override get enableCaching() { return true; }
  protected override cachedStateKeyName = () => 'FeatureListStore';

  // ─────────────────────────────────────────────────────────────────────────
  // SELECTORS (Reactive Signals)
  // ─────────────────────────────────────────────────────────────────────────

  public readonly items$ = this.select(state => state.items);
  public readonly selectedItem$ = this.select(state => state.selectedItem);
  public readonly filters$ = this.select(state => state.filters);
  public readonly pagination$ = this.select(state => state.pagination);

  // Derived selectors
  public readonly hasItems$ = this.select(state => state.items.length > 0);
  public readonly isEmpty$ = this.select(state => state.items.length === 0);

  // ─────────────────────────────────────────────────────────────────────────
  // EFFECTS (Side Effects)
  // ─────────────────────────────────────────────────────────────────────────

  // Load items with current filters
  public loadItems = this.effectSimple(() => {
    const state = this.currentVm();
    return this.featureApi.getList({
      ...state.filters,
      skipCount: state.pagination.pageIndex * state.pagination.pageSize,
      maxResultCount: state.pagination.pageSize
    }).pipe(
      this.observerLoadingErrorState('loadItems'),
      this.tapResponse(result => {
        this.updateState({
          items: result.items,
          pagination: {
            ...state.pagination,
            totalCount: result.totalCount
          }
        });
      })
    );
  });

  // Save item (create or update)
  public saveItem = this.effectSimple((item: FeatureDto) =>
    this.featureApi.save(item).pipe(
      this.observerLoadingErrorState('saveItem'),
      this.tapResponse(saved => {
        this.updateState(state => ({
          items: state.items.upsertBy(x => x.id, [saved]),
          selectedItem: saved
        }));
      })
    ));

  // Delete item
  public deleteItem = this.effectSimple((id: string) =>
    this.featureApi.delete(id).pipe(
      this.observerLoadingErrorState('deleteItem'),
      this.tapResponse(() => {
        this.updateState(state => ({
          items: state.items.filter(x => x.id !== id),
          selectedItem: state.selectedItem?.id === id ? undefined : state.selectedItem
        }));
      })
    ));

  // ─────────────────────────────────────────────────────────────────────────
  // STATE UPDATERS
  // ─────────────────────────────────────────────────────────────────────────

  public setFilters(filters: Partial<FeatureFilters>): void {
    this.updateState(state => ({
      filters: { ...state.filters, ...filters },
      pagination: { ...state.pagination, pageIndex: 0 } // Reset to first page
    }));
  }

  public setPage(pageIndex: number): void {
    this.updateState(state => ({
      pagination: { ...state.pagination, pageIndex }
    }));
  }

  public selectItem(item?: FeatureDto): void {
    this.updateState({ selectedItem: item });
  }

  public clearFilters(): void {
    this.updateState({
      filters: {},
      pagination: { ...this.currentVm().pagination, pageIndex: 0 }
    });
  }

  // ─────────────────────────────────────────────────────────────────────────
  // CONSTRUCTOR
  // ─────────────────────────────────────────────────────────────────────────

  constructor(private featureApi: FeatureApiService) {
    super();
  }
}
```

## Pattern 2: Store with Dependent Data

```typescript
@Injectable()
export class EmployeeFormStore extends PlatformVmStore<EmployeeFormState> {

  protected override vmConstructor = (data?: Partial<EmployeeFormState>) => ({
    employee: null,
    departments: [],
    positions: [],
    managers: [],
    ...data
  } as EmployeeFormState);

  // Load all dependent data in parallel
  public loadFormData = this.effectSimple((employeeId?: string) =>
    forkJoin({
      employee: employeeId
        ? this.employeeApi.getById(employeeId)
        : of(this.createNewEmployee()),
      departments: this.departmentApi.getActive(),
      positions: this.positionApi.getAll(),
      managers: this.employeeApi.getManagers()
    }).pipe(
      this.observerLoadingErrorState('loadFormData'),
      this.tapResponse(result => {
        this.updateState({
          employee: result.employee,
          departments: result.departments,
          positions: result.positions,
          managers: result.managers
        });
      })
    ));

  // Dependent selector - filter managers by department
  public managersForDepartment$ = (departmentId: string) =>
    this.select(state =>
      state.managers.filter(m => m.departmentId === departmentId));
}
```

## Pattern 3: Store with Caching

```typescript
@Injectable({ providedIn: 'root' })  // Singleton for caching
export class LookupDataStore extends PlatformVmStore<LookupDataState> {

  protected override get enableCaching() { return true; }
  protected override cachedStateKeyName = () => 'LookupDataStore';

  // Cache timeout (optional)
  protected override get cacheExpirationMs() { return 5 * 60 * 1000; } // 5 minutes

  // Load with cache check
  public loadCountries = this.effectSimple(() => {
    if (this.currentVm().countries.length > 0) {
      return EMPTY; // Already loaded, skip
    }

    return this.lookupApi.getCountries().pipe(
      this.observerLoadingErrorState('loadCountries'),
      this.tapResponse(countries => {
        this.updateState({ countries });
      })
    );
  });
}
```

## Component Integration

```typescript
@Component({
  selector: 'app-feature-list',
  templateUrl: './feature-list.component.html',
  providers: [FeatureListStore]  // Component-scoped store
})
export class FeatureListComponent
  extends AppBaseVmStoreComponent<FeatureListState, FeatureListStore>
  implements OnInit {

  constructor(store: FeatureListStore) {
    super(store);
  }

  ngOnInit(): void {
    this.store.loadItems();
  }

  onSearch(text: string): void {
    this.store.setFilters({ searchText: text });
    this.store.loadItems();
  }

  onPageChange(pageIndex: number): void {
    this.store.setPage(pageIndex);
    this.store.loadItems();
  }

  onDelete(item: FeatureDto): void {
    this.store.deleteItem(item.id);
  }

  onRefresh(): void {
    this.reload();  // Inherited - reloads all store effects
  }

  // Loading states
  get isLoading$() { return this.store.isLoading$('loadItems'); }
  get isSaving$() { return this.store.isLoading$('saveItem'); }
  get isDeleting$() { return this.store.isLoading$('deleteItem'); }
}
```

## Template Usage

```html
<app-loading-and-error-indicator [target]="this">
  @if (vm(); as vm) {
    <!-- Filters -->
    <div class="filters">
      <input
        [value]="vm.filters.searchText ?? ''"
        (input)="onSearch($event.target.value)"
        placeholder="Search..." />
    </div>

    <!-- List -->
    @for (item of vm.items; track item.id) {
      <div class="item" [class.selected]="vm.selectedItem?.id === item.id">
        {{ item.name }}
        <button
          (click)="onDelete(item)"
          [disabled]="isDeleting$()">
          Delete
        </button>
      </div>
    } @empty {
      <div class="empty">No items found</div>
    }

    <!-- Pagination -->
    <app-pagination
      [pageIndex]="vm.pagination.pageIndex"
      [pageSize]="vm.pagination.pageSize"
      [totalCount]="vm.pagination.totalCount"
      (pageChange)="onPageChange($event)" />
  }
</app-loading-and-error-indicator>
```

## Key Store APIs

| Method | Purpose | Example |
|--------|---------|---------|
| `select()` | Create selector | `this.select(s => s.items)` |
| `updateState()` | Update state | `this.updateState({ items })` |
| `effectSimple()` | Create effect | `this.effectSimple(() => api.call())` |
| `currentVm()` | Get current state | `const state = this.currentVm()` |
| `observerLoadingErrorState()` | Track loading/error | `.pipe(this.observerLoadingErrorState('key'))` |
| `tapResponse()` | Handle success/error | `.pipe(this.tapResponse(success, error))` |
| `isLoading$()` | Loading signal | `this.store.isLoading$('loadItems')` |

## Anti-Patterns to AVOID

:x: **Calling effects without tracking**
```typescript
// WRONG - no loading state
this.api.getItems().subscribe(items => this.updateState({ items }));

// CORRECT - with loading tracking
public loadItems = this.effectSimple(() =>
  this.api.getItems().pipe(
    this.observerLoadingErrorState('loadItems'),
    this.tapResponse(items => this.updateState({ items }))
  ));
```

:x: **Mutating state directly**
```typescript
// WRONG - direct mutation
this.currentVm().items.push(newItem);

// CORRECT - immutable update
this.updateState(state => ({
  items: [...state.items, newItem]
}));
```

:x: **Using store without provider**
```typescript
// WRONG - no provider
export class MyComponent {
  constructor(private store: FeatureStore) { }  // Error: No provider
}

// CORRECT - provide at component level
@Component({
  providers: [FeatureStore]
})
```

## Verification Checklist
- [ ] State interface defines all required properties
- [ ] `vmConstructor` provides default state
- [ ] Effects use `observerLoadingErrorState()` for tracking
- [ ] Effects use `tapResponse()` for handling
- [ ] Selectors are memoized with `select()`
- [ ] State updates are immutable
- [ ] Store provided at correct level (component vs root)
- [ ] Caching configured if needed
