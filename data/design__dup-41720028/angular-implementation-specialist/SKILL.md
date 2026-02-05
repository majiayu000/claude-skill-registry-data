---
name: angular-implementation-specialist
description: Implement Angular v21 applications with standalone components, signals-based state management, new control flow syntax (@if, @for, @switch), OnPush change detection, inject() DI, Tailwind CSS, and Vitest testing. Use when creating Angular components/services, implementing signals state, writing Vitest tests, applying Tailwind styling, or working with Angular v21 best practices.
---

# Angular Implementation Specialist

Specialized in implementing modern Angular v21 applications following latest best practices with standalone components, signals, new control flow syntax, Tailwind CSS styling, and Vitest testing. Leverages Angular CLI MCP server tools for version-specific guidance.

## When to Use This Skill

- Creating Angular standalone components (no NgModules)
- Implementing signals-based state management
- Using new control flow syntax (@if, @for, @switch)
- Writing Vitest tests following TDD approach
- Applying Tailwind CSS for sophisticated, minimalist UI design
- Implementing OnPush change detection strategy
- Using inject() function for dependency injection
- Setting up reactive forms
- Optimizing images with NgOptimizedImage
- Getting Angular version-specific best practices via MCP tools

## Core Principles

- **Standalone Components**: Default behavior, no need to set `standalone: true`
- **Signals Over Decorators**: Use `input()`, `output()`, `computed()` functions
- **Modern Control Flow**: Use `@if`, `@for`, `@switch` instead of structural directives
- **OnPush Strategy**: Always use `ChangeDetectionStrategy.OnPush`
- **Inject Function**: Use `inject()` instead of constructor injection
- **Host Object**: Use `host` object in decorator instead of `@HostBinding`/`@HostListener`
- **Direct Bindings**: Use `[class]` and `[style]` instead of `ngClass`/`ngStyle`
- **Test-Driven Development**: Write tests first with Vitest, then implementation
- **Tailwind-First Styling**: Use Tailwind utility classes for minimalist design

## Implementation Guidelines

### Standalone Component Structure

```typescript
import { Component, ChangeDetectionStrategy, input, output, computed } from '@angular/core'
import { CommonModule } from '@angular/common'

interface User {
  id: string
  name: string
  email: string
}

@Component({
  selector: 'app-user-card',
  // WHY: No need to set standalone: true, it's default in Angular v21
  changeDetection: ChangeDetectionStrategy.OnPush,
  // WHY: Use host object for host bindings instead of decorators
  host: {
    '[class.card-active]': 'isActive()',
    '(click)': 'handleClick()',
  },
  imports: [CommonModule],
  template: `
    <div class="rounded-lg bg-white p-6 shadow-md">
      <h3 class="text-xl font-semibold text-gray-900">{{ user().name }}</h3>
      <p class="mt-2 text-sm text-gray-600">{{ user().email }}</p>

      @if (showActions()) {
        <div class="mt-4 flex gap-2">
          <button
            (click)="onEdit.emit(user().id)"
            class="rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
          >
            Edit
          </button>
          <button
            (click)="onDelete.emit(user().id)"
            class="rounded bg-red-500 px-4 py-2 text-white hover:bg-red-600"
          >
            Delete
          </button>
        </div>
      }
    </div>
  `,
})
export class UserCardComponent {
  // WHY: Use input() function instead of @Input() decorator for better type safety
  user = input.required<User>()
  showActions = input(true)

  // WHY: Use output() function instead of @Output() decorator
  onEdit = output<string>()
  onDelete = output<string>()

  // WHY: Use computed() for derived state instead of getters
  isActive = computed(() => this.user().email.endsWith('@company.com'))

  handleClick(): void {
    console.log('Card clicked:', this.user().id)
  }
}
```

### Signals-Based State Management

```typescript
import { Component, signal, computed, effect } from '@angular/core'
import { FormsModule } from '@angular/forms'

interface Todo {
  id: string
  title: string
  completed: boolean
}

@Component({
  selector: 'app-todo-list',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [FormsModule],
  template: `
    <div class="mx-auto max-w-2xl p-6">
      <h2 class="text-2xl font-bold">Todos ({{ remainingCount() }})</h2>

      <input
        [(ngModel)]="newTodoTitle"
        (keyup.enter)="addTodo()"
        class="mt-4 w-full rounded border p-2"
        placeholder="Add new todo..."
      />

      @for (todo of todos(); track todo.id) {
        <div class="mt-2 flex items-center gap-2 rounded bg-gray-100 p-3">
          <input
            type="checkbox"
            [checked]="todo.completed"
            (change)="toggleTodo(todo.id)"
          />
          <span [class.line-through]="todo.completed">{{ todo.title }}</span>
          <button
            (click)="removeTodo(todo.id)"
            class="ml-auto text-red-500 hover:text-red-700"
          >
            Delete
          </button>
        </div>
      }

      @if (todos().length === 0) {
        <p class="mt-4 text-center text-gray-500">No todos yet</p>
      }
    </div>
  `,
})
export class TodoListComponent {
  // WHY: Use signal() for mutable state
  todos = signal<Todo[]>([])
  newTodoTitle = ''

  // WHY: Use computed() for derived state
  remainingCount = computed(() =>
    this.todos().filter(t => !t.completed).length
  )

  completedCount = computed(() =>
    this.todos().filter(t => t.completed).length
  )

  constructor() {
    // WHY: Use effect() for side effects based on signal changes
    effect(() => {
      console.log('Remaining todos:', this.remainingCount())
    })
  }

  addTodo(): void {
    if (!this.newTodoTitle.trim()) return

    const newTodo: Todo = {
      id: crypto.randomUUID(),
      title: this.newTodoTitle,
      completed: false,
    }

    // WHY: Use update() to modify signal state based on previous value
    this.todos.update(current => [...current, newTodo])
    this.newTodoTitle = ''
  }

  toggleTodo(id: string): void {
    this.todos.update(current =>
      current.map(todo =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    )
  }

  removeTodo(id: string): void {
    this.todos.update(current => current.filter(todo => todo.id !== id))
  }
}
```

### New Control Flow Syntax

```typescript
import { Component, signal } from '@angular/core'

type ViewMode = 'list' | 'grid' | 'table'

interface Product {
  id: string
  name: string
  price: number
  inStock: boolean
}

@Component({
  selector: 'app-product-list',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="p-6">
      <!-- @if directive replaces *ngIf -->
      @if (isLoading()) {
        <div class="text-center">
          <p class="text-gray-500">Loading products...</p>
        </div>
      } @else if (error()) {
        <div class="rounded bg-red-100 p-4 text-red-700">
          Error: {{ error() }}
        </div>
      } @else {
        <!-- @switch directive replaces *ngSwitch -->
        @switch (viewMode()) {
          @case ('list') {
            <div class="space-y-2">
              @for (product of products(); track product.id) {
                <div class="rounded border p-4">
                  <h3>{{ product.name }}</h3>
                  <p>\${{ product.price }}</p>
                </div>
              }
            </div>
          }
          @case ('grid') {
            <div class="grid grid-cols-3 gap-4">
              @for (product of products(); track product.id) {
                <div class="rounded border p-4">
                  <h3>{{ product.name }}</h3>
                  <p>\${{ product.price }}</p>
                </div>
              }
            </div>
          }
          @case ('table') {
            <table class="w-full">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Price</th>
                  <th>Stock</th>
                </tr>
              </thead>
              <tbody>
                @for (product of products(); track product.id) {
                  <tr>
                    <td>{{ product.name }}</td>
                    <td>\${{ product.price }}</td>
                    <td>{{ product.inStock ? 'Yes' : 'No' }}</td>
                  </tr>
                }
              </tbody>
            </table>
          }
        }
      }

      <!-- @for directive replaces *ngFor -->
      <!-- WHY: track function is required for performance optimization -->
      @for (product of filteredProducts(); track product.id; let idx = $index) {
        <div class="p-2">
          {{ idx + 1 }}. {{ product.name }}
        </div>
      } @empty {
        <p class="text-gray-500">No products found</p>
      }
    </div>
  `,
})
export class ProductListComponent {
  products = signal<Product[]>([])
  isLoading = signal(false)
  error = signal<string | null>(null)
  viewMode = signal<ViewMode>('list')

  filteredProducts = computed(() =>
    this.products().filter(p => p.inStock)
  )
}
```

### Dependency Injection with inject()

```typescript
import { Component, inject } from '@angular/core'
import { HttpClient } from '@angular/common/http'
import { Router } from '@angular/router'
import { Observable } from 'rxjs'

interface User {
  id: string
  name: string
}

// Service example
export class UserService {
  // WHY: Use inject() instead of constructor injection
  private http = inject(HttpClient)

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>('/api/users')
  }
}

@Component({
  selector: 'app-user-container',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div>
      @for (user of users(); track user.id) {
        <app-user-card
          [user]="user"
          (onEdit)="editUser($event)"
          (onDelete)="deleteUser($event)"
        />
      }
    </div>
  `,
})
export class UserContainerComponent {
  // WHY: inject() is more flexible and composable than constructor injection
  private userService = inject(UserService)
  private router = inject(Router)

  users = signal<User[]>([])

  ngOnInit(): void {
    this.userService.getUsers().subscribe(users => {
      this.users.set(users)
    })
  }

  editUser(id: string): void {
    this.router.navigate(['/users', id, 'edit'])
  }

  deleteUser(id: string): void {
    this.users.update(current => current.filter(u => u.id !== id))
  }
}
```

### Reactive Forms

```typescript
import { Component, inject, signal } from '@angular/core'
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms'

interface LoginForm {
  email: string
  password: string
  rememberMe: boolean
}

@Component({
  selector: 'app-login-form',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()" class="mx-auto max-w-md space-y-4 p-6">
      <div>
        <label class="block text-sm font-medium">Email</label>
        <input
          formControlName="email"
          type="email"
          class="mt-1 w-full rounded border p-2"
          [class.border-red-500]="form.controls.email.invalid && form.controls.email.touched"
        />
        @if (form.controls.email.invalid && form.controls.email.touched) {
          <p class="mt-1 text-sm text-red-500">Valid email is required</p>
        }
      </div>

      <div>
        <label class="block text-sm font-medium">Password</label>
        <input
          formControlName="password"
          type="password"
          class="mt-1 w-full rounded border p-2"
          [class.border-red-500]="form.controls.password.invalid && form.controls.password.touched"
        />
        @if (form.controls.password.invalid && form.controls.password.touched) {
          <p class="mt-1 text-sm text-red-500">Password must be at least 8 characters</p>
        }
      </div>

      <div class="flex items-center gap-2">
        <input
          formControlName="rememberMe"
          type="checkbox"
          id="remember"
        />
        <label for="remember" class="text-sm">Remember me</label>
      </div>

      <button
        type="submit"
        [disabled]="form.invalid || isSubmitting()"
        class="w-full rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 disabled:opacity-50"
      >
        @if (isSubmitting()) {
          <span>Signing in...</span>
        } @else {
          <span>Sign In</span>
        }
      </button>
    </form>
  `,
})
export class LoginFormComponent {
  // WHY: FormBuilder provides cleaner API than FormGroup/FormControl constructors
  private fb = inject(FormBuilder)

  isSubmitting = signal(false)

  // WHY: Prefer reactive forms over template-driven forms for complex validation
  form = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]],
    rememberMe: [false],
  })

  onSubmit(): void {
    if (this.form.invalid) return

    this.isSubmitting.set(true)
    const formValue = this.form.value as LoginForm

    // Submit logic here
    console.log('Form submitted:', formValue)
  }
}
```

### NgOptimizedImage

```typescript
import { Component } from '@angular/core'
import { NgOptimizedImage } from '@angular/common'

@Component({
  selector: 'app-hero-section',
  changeDetection: ChangeDetectionStrategy.OnPush,
  // WHY: Import NgOptimizedImage for all static images
  imports: [NgOptimizedImage],
  template: `
    <section class="relative h-screen">
      <!-- WHY: NgOptimizedImage provides automatic srcset and lazy loading -->
      <img
        ngSrc="/assets/hero-bg.jpg"
        alt="Hero background"
        fill
        priority
        class="object-cover"
      />
      <div class="relative z-10 flex h-full items-center justify-center">
        <h1 class="text-5xl font-bold text-white">Welcome</h1>
      </div>
    </section>
  `,
})
export class HeroSectionComponent {}
```

## Vitest Testing with TDD

### Component Test Example

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { TestBed } from '@angular/core/testing'
import { signal } from '@angular/core'
import { UserCardComponent } from './user-card.component'

describe('UserCardComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserCardComponent],
    }).compileComponents()
  })

  it('should create component', () => {
    const fixture = TestBed.createComponent(UserCardComponent)
    const component = fixture.componentInstance
    expect(component).toBeTruthy()
  })

  it('should display user name and email', () => {
    const fixture = TestBed.createComponent(UserCardComponent)
    const component = fixture.componentInstance

    // WHY: Set input using fixture.componentRef.setInput for signal inputs
    fixture.componentRef.setInput('user', {
      id: '1',
      name: 'John Doe',
      email: 'john@example.com',
    })
    fixture.detectChanges()

    const compiled = fixture.nativeElement as HTMLElement
    expect(compiled.textContent).toContain('John Doe')
    expect(compiled.textContent).toContain('john@example.com')
  })

  it('should emit edit event when edit button clicked', () => {
    const fixture = TestBed.createComponent(UserCardComponent)
    const component = fixture.componentInstance

    fixture.componentRef.setInput('user', {
      id: '1',
      name: 'John Doe',
      email: 'john@example.com',
    })
    fixture.detectChanges()

    let emittedId: string | undefined
    component.onEdit.subscribe((id: string) => {
      emittedId = id
    })

    const editButton = fixture.nativeElement.querySelector('button:first-of-type')
    editButton?.click()

    expect(emittedId).toBe('1')
  })

  it('should compute isActive correctly', () => {
    const fixture = TestBed.createComponent(UserCardComponent)
    const component = fixture.componentInstance

    fixture.componentRef.setInput('user', {
      id: '1',
      name: 'John Doe',
      email: 'john@company.com',
    })
    fixture.detectChanges()

    expect(component.isActive()).toBe(true)

    fixture.componentRef.setInput('user', {
      id: '1',
      name: 'John Doe',
      email: 'john@external.com',
    })
    fixture.detectChanges()

    expect(component.isActive()).toBe(false)
  })
})
```

### Service Test Example

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { TestBed } from '@angular/core/testing'
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing'
import { UserService } from './user.service'

describe('UserService', () => {
  let service: UserService
  let httpMock: HttpTestingController

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UserService],
    })

    service = TestBed.inject(UserService)
    httpMock = TestBed.inject(HttpTestingController)
  })

  it('should fetch users', () => {
    const mockUsers = [
      { id: '1', name: 'John Doe' },
      { id: '2', name: 'Jane Smith' },
    ]

    service.getUsers().subscribe(users => {
      expect(users).toEqual(mockUsers)
    })

    const req = httpMock.expectOne('/api/users')
    expect(req.request.method).toBe('GET')
    req.flush(mockUsers)
  })
})
```

## Tools to Use

### Claude Code Tools

- `Read`: Read existing Angular files and project structure
- `Write`: Create new Angular components, services, tests
- `Edit`: Modify existing Angular code
- `Bash`: Run Angular CLI commands, Vitest tests
- `Grep`: Search for Angular patterns in codebase
- `Glob`: Find Angular files by pattern

### Angular MCP Server Tools

- `mcp__angular-cli__list_projects`: List Angular projects to get workspacePath
- `mcp__angular-cli__get_best_practices`: Get version-specific best practices (requires workspacePath)
- `mcp__angular-cli__search_documentation`: Search Angular docs with version alignment
- `mcp__angular-cli__find_examples`: Find modern Angular code examples
- `mcp__angular-cli__onpush_zoneless_migration`: Analyze OnPush/Zoneless migration

### Common Commands

```bash
# Generate component
ng generate component features/user-profile

# Generate service
ng generate service services/user

# Run tests with Vitest
npm run test

# Run tests in watch mode
npm run test:watch

# Build project
ng build

# Serve project
ng serve

# Check TypeScript types
npx tsc --noEmit
```

## Workflow

1. **Get Workspace Info**: Call `mcp__angular-cli__list_projects` to get workspacePath
2. **Get Best Practices**: Call `mcp__angular-cli__get_best_practices` with workspacePath for version-specific guidance
3. **Search Examples**: Use `mcp__angular-cli__find_examples` for modern patterns
4. **Write Tests First**: Create Vitest tests defining expected behavior (TDD)
5. **Run Tests**: Verify tests fail appropriately
6. **Implement Code**: Write Angular component/service to pass tests
7. **Use OnPush**: Always set `changeDetection: ChangeDetectionStrategy.OnPush`
8. **Use Signals**: Implement state with `signal()`, `computed()`, `input()`, `output()`
9. **Use New Control Flow**: Use `@if`, `@for`, `@switch` instead of structural directives
10. **Use inject()**: Use `inject()` function for DI instead of constructor
11. **Apply Tailwind**: Use Tailwind utility classes for styling
12. **Run Tests Again**: Verify all tests pass
13. **Type Check**: Run `npx tsc --noEmit` to verify TypeScript types

## Related Skills

- `typescript-core-development`: For TypeScript patterns and types
- `vitest-react-testing`: Similar testing patterns applicable to Angular
- `react-component-development`: Component design principles applicable to Angular

## Reference Documentation

See detailed documentation in references/:

- [Tailwind Patterns](references/tailwind-patterns.md) - Sophisticated minimalist design patterns
- [Vitest Patterns](references/vitest-patterns.md) - Testing patterns and best practices
- [MCP Integration](references/mcp-integration.md) - Angular CLI MCP server integration guide

## Key Reminders

- Standalone components are default, no need to set `standalone: true`
- Always use `ChangeDetectionStrategy.OnPush`
- Use `input()` and `output()` functions, not decorators
- Use `computed()` for derived state, not getters
- Use `update()` or `set()` on signals, never `mutate()`
- Use `@if`, `@for`, `@switch` instead of `*ngIf`, `*ngFor`, `*ngSwitch`
- Use `inject()` instead of constructor injection
- Use `host` object in decorator, not `@HostBinding`/`@HostListener`
- Use `[class]` and `[style]` bindings, not `ngClass`/`ngStyle`
- Prefer Reactive forms over Template-driven forms
- Use `NgOptimizedImage` for all static images
- Always include `track` function in `@for` loops for performance
- Write tests first (TDD), then implementation
- Use Tailwind utility classes for styling
- Always call `list_projects` before other MCP tools to get workspacePath
