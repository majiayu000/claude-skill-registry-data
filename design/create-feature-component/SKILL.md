---
name: Create Feature Component
description: Create a complete feature with ViewModel, View, and tests following Phoenix MVVM patterns. Use when building new UI features, panels, or components that manage their own state. Generates ViewModel with MobX, React view with observer, and comprehensive tests.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Create Feature Component

This skill scaffolds a complete feature following Phoenix MVVM architecture: ViewModel + View + Tests.

## When to Use

- Creating a new UI feature or panel
- Building a settings or configuration component
- Adding a new view with business logic
- Creating a component that manages collections
- Building forms with validation

## What Gets Created

1. **ViewModel** - State management and business logic (MobX)
2. **View** - React component (observer)
3. **Tests** - Unit tests for ViewModel
4. **Display Registration** - Optional panel/display registration
5. **Barrel Exports** - Updated index.ts files

## Prerequisites

- Determine library location (`faad.components`, `alpha.components`, etc.)
- Identify required entity ViewModels
- Understand data flow and services needed

## Process

### Step 1: Gather Requirements

**Ask user**:
- Feature name (e.g., "InitConfigEditor", "PlatformSettings")
- Library to create in (e.g., `faad.components`, `alpha.components`)
- Does it manage entity ViewModels? Which ones?
- Does it need to be a registered display/panel?
- What services does it need? (EventBus, Logging, etc.)

### Step 2: Choose ViewModel Pattern

**For UI-only state** (no entities):
- Extend `BaseViewModel`
- Manage local `@observable` state
- Example: Dialog, Modal, Filter panel

**For entity management** (wraps entities):
- Extend `BaseViewModel`
- Create entity VMs with `computeItemVMsFromItems` or `createVisualPlugin`
- Example: Equipment manager, Platform list

**For features** (combines both):
- Extend `BaseViewModel`
- Mix local UI state with entity VMs
- Example: Settings panel with multiple entities

**Reference**: [FRAMEWORK_GUIDE.md - ViewModel Types](../../ai-guide/_ARCHITECTURE/FRAMEWORK_GUIDE.md#viewmodel-types)

### Step 3: Create ViewModel File

**Location**: `{lib}.components/src/lib/{feature}/{FeatureName}ViewModel.ts`

**Template Structure**:
```typescript
import { IFrameworkServices } from '@tektonux/framework-api';
import { BaseViewModel } from '@tektonux/framework-shared-plugin';
import { action, computed, makeObservable, observable, runInAction } from 'mobx';

export class FeatureNameViewModel extends BaseViewModel {
    public static class: string = 'FeatureNameViewModel';

    // ========== UI State ==========
    @observable isLoading: boolean = false;
    @observable errorMessage: string | null = null;
    @observable selectedId: string | null = null;

    constructor(services: IFrameworkServices) {
        super(services);
        makeObservable(this);  // CRITICAL!
    }

    // ========== Entity ViewModels ==========
    // @computed required - derives collection from interactor
    @computed get entityVMs(): Record<string, EntityViewModel> {
        return this.computeItemVMsFromItems(
            'entityVMs',
            () => this._interactor.getAll(),
            item => {
                const vm = new EntityViewModel(this._services);
                vm.setEntityId(item.id);
                return vm;
            }
        );
    }

    // ========== Computed Properties ==========
    // @computed required - derives from observables
    @computed get selectedVM(): EntityViewModel | null {
        return this.selectedId ? this.entityVMs[this.selectedId] ?? null : null;
    }

    // ========== Actions ==========
    @action setSelected(id: string | null): void {
        this.selectedId = id;
    }

    @action async loadData(): Promise<void> {
        this.isLoading = true;
        try {
            const data = await this.fetchData();
            runInAction(() => {
                this.data = data;
            });
        } catch (error) {
            runInAction(() => {
                this.errorMessage = error.message;
            });
        } finally {
            runInAction(() => {
                this.isLoading = false;
            });
        }
    }
}
```

**Reference**: [COOKBOOK_PATTERNS_ENHANCED.md - Complete Feature Template](../../ai-guide/_DAILY/COOKBOOK_PATTERNS_ENHANCED.md#complete-feature-template)

### Step 4: Create View File

**Location**: `{lib}.components/src/lib/{feature}/{FeatureName}View.tsx`

**CRITICAL UI Component Rules**:
- ✅ ALWAYS use Phoenix shared components
- ✅ ALWAYS wrap with `observer()`
- ✅ ALWAYS use `SelectPortal` for Select dropdowns
- ❌ NEVER use native HTML (`<span>`, `<button>`, `<input>`)
- ❌ NEVER wrap Checkbox/Radio in Label

**Template Structure**:
```tsx
import { observer } from 'mobx-react';
import {
    Button,
    Label,
    TextInput,
    Select,
    SelectTrigger,
    SelectValue,
    SelectContent,
    SelectItem,
    SelectItemText,
    SelectPortal,
    SelectViewport,
    Card
} from '@tektonux/phoenix-components-shared';
import { FeatureNameViewModel } from './FeatureNameViewModel';

export const FeatureNameView = observer(({
    viewModel
}: {
    viewModel: FeatureNameViewModel
}) => {
    return (
        <div className="feature-container">
            <Card className="feature-card">
                <div className="feature-header">
                    <Label className="feature-title">Feature Name</Label>
                </div>

                <div className="feature-content">
                    {/* Example: Select with Portal */}
                    <Select
                        value={viewModel.selectedId ?? ''}
                        onValueChange={(id) => viewModel.setSelected(id)}
                    >
                        <SelectTrigger>
                            <SelectValue placeholder="Select item" />
                        </SelectTrigger>
                        <SelectPortal>
                            <SelectContent position="popper">
                                <SelectViewport>
                                    {Object.values(viewModel.entityVMs).map(vm => (
                                        <SelectItem key={vm.id} value={vm.id}>
                                            <SelectItemText>{vm.nameVM.actual()}</SelectItemText>
                                        </SelectItem>
                                    ))}
                                </SelectViewport>
                            </SelectContent>
                        </SelectPortal>
                    </Select>

                    {/* Action buttons */}
                    <div className="feature-actions">
                        <Button
                            onClick={() => viewModel.loadData()}
                            disabled={viewModel.isLoading}
                        >
                            LOAD DATA
                        </Button>
                    </div>
                </div>
            </Card>
        </div>
    );
});
```

**Reference**: [UI_COMPONENT_GUIDELINES.md](../../ai-guide/_DAILY/UI_COMPONENT_GUIDELINES.md)

### Step 5: Create Tests

**Location**: `{lib}.components/src/lib/{feature}/__tests__/{FeatureName}ViewModel.test.ts`

**Template Structure**:
```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { FeatureNameViewModel } from '../FeatureNameViewModel';
import { IFrameworkServices } from '@tektonux/framework-api';

describe('FeatureNameViewModel', () => {
    let viewModel: FeatureNameViewModel;
    let mockServices: IFrameworkServices;

    beforeEach(() => {
        mockServices = {
            logging: {
                info: vi.fn(),
                warn: vi.fn(),
                error: vi.fn()
            },
            eventBus: {
                publish: vi.fn(),
                subscribe: vi.fn()
            }
        } as unknown as IFrameworkServices;

        viewModel = new FeatureNameViewModel(mockServices);
    });

    describe('Initialization', () => {
        it('should initialize with default values', () => {
            expect(viewModel.isLoading).toBe(false);
            expect(viewModel.selectedId).toBeNull();
        });
    });

    describe('Actions', () => {
        it('should update selected ID', () => {
            viewModel.setSelected('test-id');
            expect(viewModel.selectedId).toBe('test-id');
        });
    });

    describe('Computed Properties', () => {
        it('should compute selected VM correctly', () => {
            // Setup
            viewModel.setSelected('test-id');

            // Assert
            const selected = viewModel.selectedVM;
            expect(selected).toBeDefined();
        });
    });
});
```

**Reference**: [TESTING_GUIDE.md](../../ai-guide/_DAILY/TESTING_GUIDE.md)

### Step 6: Display Registration (Optional)

If this is a panel or registered display:

**Location**: `{lib}.components/src/lib/{feature}/{FeatureName}Display.tsx`

```typescript
import { registerDisplayInfo } from '@tektonux/framework-visual-react-shared';
import { useViewModel } from '@tektonux/framework-visual-react-components';
import { DisplayTypes } from '../displayTypes';
import { FeatureNameViewModel } from './FeatureNameViewModel';
import { FeatureNameView } from './FeatureNameView';

registerDisplayInfo({
    id: DisplayTypes.FeatureName,
    tags: [],
    visible: true,
    ordinal: 100,
    Renderer: (props) => {
        const viewModel = useViewModel(FeatureNameViewModel);
        return <FeatureNameView viewModel={viewModel} {...props} />;
    }
});

export default {};  // REQUIRED for display files
```

**Add to DisplayTypes enum**:
```typescript
export enum DisplayTypes {
    // ... existing
    FeatureName = 'FeatureName'
}
```

**Reference**: [DISPLAY_REGISTRATION_GUIDE.md](../../ai-guide/_REFERENCE/DISPLAY_REGISTRATION_GUIDE.md)

### Step 7: Update Barrel Exports

**Update `{lib}.components/src/index.ts`**:
```typescript
export * from './lib/{feature}/{FeatureName}ViewModel';
export * from './lib/{feature}/{FeatureName}View';
```

**If display registered, also export display file**:
```typescript
export * from './lib/{feature}/{FeatureName}Display';
```

### Step 8: Create CSS (if needed)

**Location**: `{lib}.components/src/lib/{feature}/{FeatureName}.css`

**Use existing patterns**:
```css
.feature-container {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
}

.feature-card {
    padding: var(--spacing-lg);
    background: var(--neutral2);
    border: 1px solid var(--neutral4);
}

.feature-header {
    margin-bottom: var(--spacing-md);
}

.feature-title {
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: var(--neutral12);
}

.feature-content {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
}

.feature-actions {
    display: flex;
    gap: var(--spacing-sm);
    margin-top: var(--spacing-md);
}
```

**Reference**: [CSS_GUIDANCE.md](../../ai-guide/_REFERENCE/CSS_GUIDANCE.md)

### Step 9: Verify Build

```bash
# Check for errors
./tools/build-helpers/count-client-errors.sh
./tools/build-helpers/show-client-errors.sh 10

# Run tests
npm test {FeatureName}
```

## Common Patterns

### Pattern 1: Form with Apply/Cancel
```typescript
// ViewModel
@action applyChanges(): void {
    this.selectedVM?.publishLocal();  // Commit all local changes
}

@action cancelChanges(): void {
    this.selectedVM?.clearLocal();  // Discard all local changes
}

@computed get hasUnsavedChanges(): boolean {
    return this.selectedVM?.hasLocalChanges ?? false;
}
```

**Reference**: [PROPERTY_VIEWMODEL_GUIDE.md - Local Changes Pattern](../../ai-guide/_DAILY/PROPERTY_VIEWMODEL_GUIDE.md#local-changes-pattern)

### Pattern 2: Collection Management
```typescript
@computed get entityVMs(): Record<string, EntityViewModel> {
    return this.computeItemVMsFromItems(
        'entityVMs',
        () => this._interactor.getAll(),
        item => {
            const vm = new EntityViewModel(this._services);
            vm.setEntityId(item.id);
            return vm;
        }
    );
}
```

### Pattern 3: Filtered/Sorted Collections
```typescript
@observable searchTerm: string = '';

@computed get filteredVMs(): EntityViewModel[] {
    const all = Object.values(this.entityVMs);
    if (!this.searchTerm) return all;

    const term = this.searchTerm.toLowerCase();
    return all.filter(vm =>
        vm.nameVM.actual()?.toLowerCase().includes(term)
    );
}
```

## MobX Checklist

**Reference**: [MOBX_ESSENTIALS.md](../../ai-guide/_DAILY/MOBX_ESSENTIALS.md)

- [ ] `makeObservable(this)` called in constructor
- [ ] UI state properties marked `@observable`
- [ ] State modifiers marked `@action`
- [ ] Derived values use `@computed` (required for reactivity)
- [ ] Property VMs with configuration use `@computed` (prevents re-running config)
- [ ] Async updates use `runInAction` after `await`
- [ ] Arrays replaced, not mutated
- [ ] View wrapped with `observer()`

## Common Pitfalls

**Reference**: [COMMON_PITFALLS.md](../../ai-guide/_DAILY/COMMON_PITFALLS.md)

1. ❌ Forgetting `makeObservable(this)`
2. ❌ Not wrapping View with `observer()`
3. ❌ Using native HTML instead of Phoenix components
4. ❌ Forgetting `runInAction` after `await`
5. ❌ Not using `SelectPortal` for dropdowns
6. ❌ Wrapping Checkbox/Radio in Label

## File Structure Summary

```
{lib}.components/src/lib/{feature}/
├── {FeatureName}ViewModel.ts      # MobX state management
├── {FeatureName}View.tsx          # React UI component
├── {FeatureName}Display.tsx       # Display registration (optional)
├── {FeatureName}.css              # Styles (optional)
└── __tests__/
    └── {FeatureName}ViewModel.test.ts
```

## Ask User

- Feature name and purpose
- Which library to create in
- Does it manage entities? Which ones?
- Should it be a registered display/panel?
- What services are needed?
- Should it have Apply/Cancel buttons (local changes pattern)?