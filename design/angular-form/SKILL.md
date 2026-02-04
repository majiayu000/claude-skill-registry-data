---
name: angular-form
description: Use when creating reactive forms with validation, async validators, dependent validation, and FormArrays using platform patterns.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Angular Form Development Workflow

## When to Use This Skill

- User input forms (create, edit, settings)
- Complex validation requirements
- Async validation (uniqueness checks)
- Dynamic form fields (FormArrays)
- Dependent field validation

## Pre-Flight Checklist

- [ ] Identify form mode (create, update, view)
- [ ] **Read the design system docs** for the target application (see below)
- [ ] List all validation rules (sync and async)
- [ ] Identify field dependencies
- [ ] Search similar forms: `grep "{Feature}FormComponent" --include="*.ts"`

## 🎨 Design System Documentation (MANDATORY)

**Before creating any form, read the design system documentation for your target application:**

| Application                       | Design System Location                           |
| --------------------------------- | ------------------------------------------------ |
| **WebV2 Apps**                    | `docs/design-system/`                            |
| **TextSnippetClient**             | `src/PlatformExampleAppWeb/apps/playground-text-snippet/docs/design-system/` |

**Key docs to read:**

- `README.md` - Component overview, base classes, library summary
- `03-form-patterns.md` - Form validation, modes, error handling patterns
- `02-component-catalog.md` - Available form components and usage examples
- `01-design-tokens.md` - Colors, typography, spacing tokens

## File Location

```
src/PlatformExampleAppWeb/apps/{app-name}/src/app/
└── features/
    └── {feature}/
        ├── {feature}-form.component.ts
        ├── {feature}-form.component.html
        └── {feature}-form.component.scss
```

## Form Base Class Selection

| Base Class              | Use When                |
| ----------------------- | ----------------------- |
| `PlatformFormComponent` | Basic form without auth |
| `AppBaseFormComponent`  | Form with auth context  |

## Pattern 1: Basic Form

```typescript
// {feature}-form.component.ts
import { Component, Input } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { AppBaseFormComponent } from '@libs/apps-domains';
import { noWhitespaceValidator } from '@libs/platform-core';

// ═══════════════════════════════════════════════════════════════════════════
// VIEW MODEL
// ═══════════════════════════════════════════════════════════════════════════

export interface FeatureFormVm {
    id?: string;
    name: string;
    code: string;
    description?: string;
    status: FeatureStatus;
    isActive: boolean;
}

// ═══════════════════════════════════════════════════════════════════════════
// COMPONENT
// ═══════════════════════════════════════════════════════════════════════════

@Component({
    selector: 'app-feature-form',
    templateUrl: './feature-form.component.html'
})
export class FeatureFormComponent extends AppBaseFormComponent<FeatureFormVm> {
    @Input() featureId?: string;

    // ─────────────────────────────────────────────────────────────────────────
    // FORM CONFIGURATION
    // ─────────────────────────────────────────────────────────────────────────

    protected initialFormConfig = () => ({
        controls: {
            name: new FormControl(this.currentVm().name, [Validators.required, Validators.maxLength(200), noWhitespaceValidator]),
            code: new FormControl(this.currentVm().code, [Validators.required, Validators.pattern(/^[A-Z0-9_-]+$/), Validators.maxLength(50)]),
            description: new FormControl(this.currentVm().description, [Validators.maxLength(2000)]),
            status: new FormControl(this.currentVm().status, [Validators.required]),
            isActive: new FormControl(this.currentVm().isActive)
        }
    });

    // ─────────────────────────────────────────────────────────────────────────
    // INIT/RELOAD VIEW MODEL
    // ─────────────────────────────────────────────────────────────────────────

    protected initOrReloadVm = (isReload: boolean) => {
        if (!this.featureId) {
            // Create mode - return empty view model
            return of<FeatureFormVm>({
                name: '',
                code: '',
                status: FeatureStatus.Draft,
                isActive: true
            });
        }

        // Edit mode - load from API
        return this.featureApi.getById(this.featureId);
    };

    // ─────────────────────────────────────────────────────────────────────────
    // ACTIONS
    // ─────────────────────────────────────────────────────────────────────────

    onSubmit(): void {
        if (!this.validateForm()) return;

        const vm = this.currentVm();

        this.featureApi
            .save(vm)
            .pipe(
                this.observerLoadingErrorState('save'),
                this.tapResponse(
                    saved => this.onSuccess(saved),
                    error => this.onError(error)
                ),
                this.untilDestroyed()
            )
            .subscribe();
    }

    onCancel(): void {
        this.router.navigate(['/features']);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // CONSTRUCTOR
    // ─────────────────────────────────────────────────────────────────────────

    constructor(
        private featureApi: FeatureApiService,
        private router: Router
    ) {
        super();
    }
}
```

## Pattern 2: Form with Async Validation

```typescript
export class FeatureFormComponent extends AppBaseFormComponent<FeatureFormVm> {
    protected initialFormConfig = () => ({
        controls: {
            code: new FormControl(
                this.currentVm().code,
                // Sync validators
                [Validators.required, Validators.pattern(/^[A-Z0-9_-]+$/)],
                // Async validators (only run if sync pass)
                [
                    ifAsyncValidator(
                        ctrl => ctrl.valid, // Condition to run
                        this.checkCodeUniqueValidator()
                    )
                ]
            ),
            email: new FormControl(
                this.currentVm().email,
                [Validators.required, Validators.email],
                [
                    ifAsyncValidator(
                        () => !this.isViewMode(), // Skip in view mode
                        this.checkEmailUniqueValidator()
                    )
                ]
            )
        }
    });

    // ─────────────────────────────────────────────────────────────────────────
    // ASYNC VALIDATORS
    // ─────────────────────────────────────────────────────────────────────────

    private checkCodeUniqueValidator(): AsyncValidatorFn {
        return async (control: AbstractControl): Promise<ValidationErrors | null> => {
            if (!control.value) return null;

            const exists = await firstValueFrom(
                this.featureApi.checkCodeExists(control.value, this.currentVm().id).pipe(debounceTime(300)) // Debounce API calls
            );

            return exists ? { codeExists: 'Code already exists' } : null;
        };
    }

    private checkEmailUniqueValidator(): AsyncValidatorFn {
        return async (control: AbstractControl): Promise<ValidationErrors | null> => {
            if (!control.value) return null;

            const exists = await firstValueFrom(this.employeeApi.checkEmailExists(control.value, this.currentVm().id));

            return exists ? { emailExists: 'Email already in use' } : null;
        };
    }
}
```

## Pattern 3: Form with Dependent Validation

```typescript
export class DateRangeFormComponent extends AppBaseFormComponent<DateRangeVm> {
    protected initialFormConfig = () => ({
        controls: {
            startDate: new FormControl(this.currentVm().startDate, [Validators.required]),
            endDate: new FormControl(this.currentVm().endDate, [
                Validators.required,
                // Cross-field validation
                startEndValidator(
                    'invalidRange',
                    ctrl => ctrl.parent?.get('startDate')?.value,
                    ctrl => ctrl.value,
                    { allowEqual: true }
                )
            ]),
            category: new FormControl(this.currentVm().category, [Validators.required]),
            subcategory: new FormControl(this.currentVm().subcategory, [Validators.required])
        },
        // Re-validate these fields when dependencies change
        dependentValidations: {
            endDate: ['startDate'], // Re-validate endDate when startDate changes
            subcategory: ['category'] // Re-validate subcategory when category changes
        }
    });

    // Custom cross-field validator
    private dateRangeValidator(): ValidatorFn {
        return (control: AbstractControl): ValidationErrors | null => {
            const form = control.parent;
            if (!form) return null;

            const start = form.get('startDate')?.value;
            const end = control.value;

            if (start && end && new Date(end) < new Date(start)) {
                return { invalidRange: 'End date must be after start date' };
            }

            return null;
        };
    }
}
```

## Pattern 4: Form with FormArray

```typescript
export interface ProductFormVm {
    name: string;
    price: number;
    specifications: Specification[];
    tags: string[];
}

export interface Specification {
    name: string;
    value: string;
}

export class ProductFormComponent extends AppBaseFormComponent<ProductFormVm> {
    protected initialFormConfig = () => ({
        controls: {
            name: new FormControl(this.currentVm().name, [Validators.required]),
            price: new FormControl(this.currentVm().price, [Validators.required, Validators.min(0)]),

            // FormArray configuration
            specifications: {
                // Model items to create controls from
                modelItems: () => this.currentVm().specifications,

                // How to create control for each item
                itemControl: (spec: Specification, index: number) =>
                    new FormGroup({
                        name: new FormControl(spec.name, [Validators.required]),
                        value: new FormControl(spec.value, [Validators.required])
                    })
            },

            // Simple array of primitives
            tags: {
                modelItems: () => this.currentVm().tags,
                itemControl: (tag: string) => new FormControl(tag, [Validators.required])
            }
        }
    });

    // ─────────────────────────────────────────────────────────────────────────
    // FORM ARRAY HELPERS
    // ─────────────────────────────────────────────────────────────────────────

    get specificationsArray(): FormArray {
        return this.form.get('specifications') as FormArray;
    }

    addSpecification(): void {
        const newSpec: Specification = { name: '', value: '' };

        // Update view model
        this.updateVm(vm => ({
            specifications: [...vm.specifications, newSpec]
        }));

        // Add form control
        this.specificationsArray.push(
            new FormGroup({
                name: new FormControl('', [Validators.required]),
                value: new FormControl('', [Validators.required])
            })
        );
    }

    removeSpecification(index: number): void {
        // Update view model
        this.updateVm(vm => ({
            specifications: vm.specifications.filter((_, i) => i !== index)
        }));

        // Remove form control
        this.specificationsArray.removeAt(index);
    }
}
```

## Template Patterns

### Basic Form Template

```html
<form [formGroup]="form" (ngSubmit)="onSubmit()">
    <!-- Text input -->
    <div class="form-field">
        <label for="name">Name *</label>
        <input id="name" formControlName="name" />
        @if (formControls('name').errors?.['required'] && formControls('name').touched) {
        <span class="error">Name is required</span>
        } @if (formControls('name').errors?.['maxlength']) {
        <span class="error">Name is too long</span>
        }
    </div>

    <!-- Async validation feedback -->
    <div class="form-field">
        <label for="code">Code *</label>
        <input id="code" formControlName="code" />
        @if (formControls('code').pending) {
        <span class="info">Checking availability...</span>
        } @if (formControls('code').errors?.['codeExists']) {
        <span class="error">{{ formControls('code').errors?.['codeExists'] }}</span>
        }
    </div>

    <!-- Select dropdown -->
    <div class="form-field">
        <label for="status">Status *</label>
        <select id="status" formControlName="status">
            @for (option of statusOptions; track option.value) {
            <option [value]="option.value">{{ option.label }}</option>
            }
        </select>
    </div>

    <!-- Checkbox -->
    <div class="form-field">
        <label>
            <input type="checkbox" formControlName="isActive" />
            Active
        </label>
    </div>

    <!-- Actions -->
    <div class="actions">
        <button type="button" (click)="onCancel()">Cancel</button>
        <button type="submit" [disabled]="!form.valid || isLoading$('save')()">{{ isLoading$('save')() ? 'Saving...' : 'Save' }}</button>
    </div>
</form>
```

### FormArray Template

```html
<div formArrayName="specifications">
    @for (spec of specificationsArray.controls; track $index; let i = $index) {
    <div [formGroupName]="i" class="specification-row">
        <input formControlName="name" placeholder="Name" />
        <input formControlName="value" placeholder="Value" />
        <button type="button" (click)="removeSpecification(i)">Remove</button>
    </div>
    }
    <button type="button" (click)="addSpecification()">Add Specification</button>
</div>
```

## Built-in Validators

| Validator               | Import                | Usage                    |
| ----------------------- | --------------------- | ------------------------ |
| `noWhitespaceValidator` | `@libs/platform-core` | No empty strings         |
| `startEndValidator`     | `@libs/platform-core` | Date/number range        |
| `ifAsyncValidator`      | `@libs/platform-core` | Conditional async        |
| `validator`             | `@libs/platform-core` | Custom validator factory |

## Key Form APIs

| Method              | Purpose                   | Example                             |
| ------------------- | ------------------------- | ----------------------------------- |
| `validateForm()`    | Validate and mark touched | `if (!this.validateForm()) return;` |
| `formControls(key)` | Get form control          | `this.formControls('name').errors`  |
| `currentVm()`       | Get current view model    | `const vm = this.currentVm()`       |
| `updateVm()`        | Update view model         | `this.updateVm({ name: 'new' })`    |
| `mode`              | Form mode                 | `this.mode === 'create'`            |
| `isViewMode()`      | Check view mode           | `if (this.isViewMode()) return;`    |

## Component HTML Template Standard (BEM Classes)

**All UI elements in form templates MUST have BEM classes, even without styling needs.** This makes forms self-documenting.

```html
<!-- ✅ CORRECT: All form elements have BEM classes -->
<form class="feature-form" [formGroup]="form" (ngSubmit)="onSubmit()">
    <div class="feature-form__section">
        <div class="feature-form__field">
            <label class="feature-form__label" for="name">Name *</label>
            <input class="feature-form__input" id="name" formControlName="name" />
            @if (formControls('name').errors?.['required'] && formControls('name').touched) {
            <span class="feature-form__error">Name is required</span>
            }
        </div>
        <div class="feature-form__field">
            <label class="feature-form__label" for="code">Code *</label>
            <input class="feature-form__input" id="code" formControlName="code" />
            @if (formControls('code').pending) {
            <span class="feature-form__info">Checking availability...</span>
            }
        </div>
    </div>
    <div class="feature-form__actions">
        <button class="feature-form__btn --cancel" type="button" (click)="onCancel()">Cancel</button>
        <button class="feature-form__btn --submit" type="submit">Save</button>
    </div>
</form>

<!-- ❌ WRONG: Missing BEM classes -->
<form [formGroup]="form" (ngSubmit)="onSubmit()">
    <div>
        <div>
            <label for="name">Name *</label>
            <input id="name" formControlName="name" />
        </div>
    </div>
    <div>
        <button type="button">Cancel</button>
        <button type="submit">Save</button>
    </div>
</form>
```

## Anti-Patterns to AVOID

:x: **Missing BEM classes on form elements**

```html
<!-- WRONG -->
<div><label>Name</label><input formControlName="name" /></div>

<!-- CORRECT -->
<div class="form__field">
    <label class="form__label">Name</label>
    <input class="form__input" formControlName="name" />
</div>
```

:x: **Not using validateForm()**

```typescript
// WRONG - form may be invalid
onSubmit() {
  this.api.save(this.currentVm());
}

// CORRECT - validate first
onSubmit() {
  if (!this.validateForm()) return;
  this.api.save(this.currentVm());
}
```

:x: **Async validator always runs**

```typescript
// WRONG - runs even if sync validators fail
new FormControl('', [], [asyncValidator]);

// CORRECT - conditional
new FormControl('', [], [ifAsyncValidator(ctrl => ctrl.valid, asyncValidator)]);
```

:x: **Missing form group name in array**

```html
<!-- WRONG -->
@for (item of formArray.controls; track $index) {
<input formControlName="name" />
}

<!-- CORRECT -->
@for (item of formArray.controls; track $index; let i = $index) {
<div [formGroupName]="i">
    <input formControlName="name" />
</div>
}
```

## Verification Checklist

- [ ] `initialFormConfig` returns form configuration
- [ ] `initOrReloadVm` loads data for edit mode
- [ ] `validateForm()` called before submit
- [ ] Async validators use `ifAsyncValidator` for conditional execution
- [ ] `dependentValidations` configured for cross-field validation
- [ ] FormArrays use `modelItems` and `itemControl`
- [ ] Error messages displayed for all validation rules
- [ ] Loading states shown during async operations
