---
name: forms-implementation
description: Build reactive and template-driven forms, implement custom validators, create async validators, add cross-field validation, and generate dynamic forms for Angular applications.
sasmp_version: "1.3.0"
bonded_agent: 04-forms-directives
bond_type: PRIMARY_BOND
---

# Forms Implementation Skill

## Quick Start

### Template-Driven Forms
```typescript
import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-contact',
  template: `
    <form #contactForm="ngForm" (ngSubmit)="onSubmit(contactForm)">
      <input
        [(ngModel)]="model.name"
        name="name"
        required
        minlength="3"
      />
      <input
        [(ngModel)]="model.email"
        name="email"
        email
      />
      <button [disabled]="!contactForm.valid">Submit</button>
    </form>
  `
})
export class ContactComponent {
  model = { name: '', email: '' };

  onSubmit(form: NgForm) {
    if (form.valid) {
      console.log('Form submitted:', form.value);
    }
  }
}
```

### Reactive Forms
```typescript
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-user-form',
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <input formControlName="name" placeholder="Name" />
      <input formControlName="email" type="email" />
      <input formControlName="password" type="password" />
      <button [disabled]="form.invalid">Register</button>
    </form>
  `
})
export class UserFormComponent implements OnInit {
  form!: FormGroup;

  constructor(private fb: FormBuilder) {}

  ngOnInit() {
    this.form = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]]
    });
  }

  onSubmit() {
    if (this.form.valid) {
      console.log(this.form.value);
    }
  }
}
```

## Form Controls

### FormControl
```typescript
// Create standalone control
const nameControl = new FormControl('', Validators.required);

// Get value
nameControl.value

// Set value
nameControl.setValue('John');
nameControl.patchValue({ name: 'John' });

// Check validity
nameControl.valid
nameControl.invalid
nameControl.errors

// Listen to changes
nameControl.valueChanges.subscribe(value => {
  console.log('Changed:', value);
});
```

### FormGroup
```typescript
const form = new FormGroup({
  name: new FormControl('', Validators.required),
  email: new FormControl('', [Validators.required, Validators.email]),
  address: new FormGroup({
    street: new FormControl(''),
    city: new FormControl(''),
    zip: new FormControl('')
  })
});

// Access nested controls
form.get('address.street')?.setValue('123 Main St');

// Update multiple values
form.patchValue({
  name: 'John',
  email: 'john@example.com'
});
```

### FormArray
```typescript
const form = new FormGroup({
  name: new FormControl(''),
  emails: new FormArray([
    new FormControl(''),
    new FormControl('')
  ])
});

// Dynamic form array
const emailsArray = form.get('emails') as FormArray;

// Add control
emailsArray.push(new FormControl(''));

// Remove control
emailsArray.removeAt(0);

// Iterate
emailsArray.controls.forEach((control, index) => {
  // ...
});
```

## Validation

### Built-in Validators
```typescript
import { Validators } from '@angular/forms';

new FormControl('', [
  Validators.required,
  Validators.minLength(3),
  Validators.maxLength(50),
  Validators.pattern(/^[a-z]/i),
  Validators.email,
  Validators.min(0),
  Validators.max(100)
])
```

### Custom Validators
```typescript
// Simple validator
function noSpacesValidator(control: AbstractControl): ValidationErrors | null {
  if (control.value && control.value.includes(' ')) {
    return { hasSpaces: true };
  }
  return null;
}

// Cross-field validator
function passwordMatchValidator(group: FormGroup): ValidationErrors | null {
  const password = group.get('password')?.value;
  const confirm = group.get('confirmPassword')?.value;

  return password === confirm ? null : { passwordMismatch: true };
}

// Usage
const form = new FormGroup({
  username: new FormControl('', noSpacesValidator),
  password: new FormControl(''),
  confirmPassword: new FormControl('')
}, passwordMatchValidator);
```

### Async Validators
```typescript
function emailAvailableValidator(service: UserService): AsyncValidatorFn {
  return (control: AbstractControl): Observable<ValidationErrors | null> => {
    if (!control.value) {
      return of(null);
    }

    return service.checkEmailAvailable(control.value).pipe(
      map(available => available ? null : { emailTaken: true }),
      debounceTime(300),
      first()
    );
  };
}

// Usage
new FormControl('', {
  validators: Validators.required,
  asyncValidators: emailAvailableValidator(userService),
  updateOn: 'blur'
});
```

## Form State
```typescript
const control = form.get('email')!;

// Pristine/Dirty
control.pristine  // Not modified by user
control.dirty     // Modified by user

// Touched/Untouched
control.untouched // Never focused
control.touched   // Focused at least once

// Valid/Invalid
control.valid
control.invalid
control.errors
control.pending   // Async validation in progress

// Status
control.status // 'VALID' | 'INVALID' | 'PENDING' | 'DISABLED'

// Value
control.value
control.getRawValue() // Include disabled controls
```

## Form Display

### Showing Errors
```typescript
<div *ngIf="form.get('email')?.hasError('required')">
  Email is required
</div>

<div *ngIf="form.get('email')?.hasError('email')">
  Invalid email format
</div>

<div *ngIf="form.get('email')?.hasError('emailTaken')">
  Email already in use
</div>
```

### Dynamic Forms
```typescript
@Component({
  template: `
    <form [formGroup]="form">
      <div formArrayName="items">
        <div *ngFor="let item of items.controls; let i = index">
          <input [formControlName]="i" />
          <button (click)="removeItem(i)">Remove</button>
        </div>
      </div>
      <button (click)="addItem()">Add Item</button>
    </form>
  `
})
export class DynamicFormComponent {
  form!: FormGroup;

  get items() {
    return this.form.get('items') as FormArray;
  }

  addItem() {
    this.items.push(new FormControl('', Validators.required));
  }

  removeItem(index: number) {
    this.items.removeAt(index);
  }
}
```

## Advanced Patterns

### FormBuilder Groups
```typescript
this.form = this.fb.group({
  basicInfo: this.fb.group({
    firstName: ['', Validators.required],
    lastName: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]]
  }),
  address: this.fb.group({
    street: [''],
    city: [''],
    zip: ['']
  }),
  preferences: this.fb.array([])
});
```

### Directives for Template Forms
```typescript
<form #form="ngForm">
  <input
    [(ngModel)]="user.name"
    name="name"
    required
    minlength="3"
    #nameField="ngModelGroup"
  />

  <div *ngIf="nameField.invalid && nameField.touched">
    <p *ngIf="nameField.errors?.['required']">Required</p>
    <p *ngIf="nameField.errors?.['minlength']">Min length 3</p>
  </div>
</form>
```

## Testing Forms

```typescript
describe('UserFormComponent', () => {
  let component: UserFormComponent;
  let fixture: ComponentFixture<UserFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [UserFormComponent],
      imports: [ReactiveFormsModule]
    }).compileComponents();

    fixture = TestBed.createComponent(UserFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should submit valid form', () => {
    component.form.patchValue({
      name: 'John',
      email: 'john@example.com'
    });

    expect(component.form.valid).toBe(true);
  });

  it('should show error on invalid email', () => {
    component.form.get('email')?.setValue('invalid');
    expect(component.form.get('email')?.hasError('email')).toBe(true);
  });
});
```

## Best Practices

1. **Reactive Forms for Complex**: Use for validation, computed fields
2. **Template Forms for Simple**: Use for simple, data-binding heavy forms
3. **Always validate**: Server and client validation
4. **Disable submit until valid**: Better UX
5. **Show errors appropriately**: After touched/dirty
6. **Handle async validation**: Debounce, cancel on unsubscribe
7. **Test forms thoroughly**: Validation, submission, edge cases

## Resources

- [Angular Forms Guide](https://angular.io/guide/forms)
- [Reactive Forms](https://angular.io/guide/reactive-forms)
- [Form Validation](https://angular.io/guide/form-validation)
