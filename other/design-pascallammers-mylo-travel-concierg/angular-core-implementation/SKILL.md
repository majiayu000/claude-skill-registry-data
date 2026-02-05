---
name: angular-core-implementation
description: Generate Angular components, services, modules, and directives. Implement dependency injection, lifecycle hooks, data binding, and build production-ready Angular architectures.
sasmp_version: "1.3.0"
bonded_agent: 02-angular-core
bond_type: PRIMARY_BOND
---

# Angular Core Implementation Skill

## Quick Start

### Component Basics
```typescript
import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-user-card',
  template: `
    <div class="card">
      <h2>{{ user.name }}</h2>
      <p>{{ user.email }}</p>
      <button (click)="onDelete()">Delete</button>
    </div>
  `,
  styles: [`
    .card { border: 1px solid #ddd; padding: 16px; }
  `]
})
export class UserCardComponent {
  @Input() user!: User;
  @Output() deleted = new EventEmitter<void>();

  onDelete() {
    this.deleted.emit();
  }
}
```

### Service Creation
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root' // Singleton service
})
export class UserService {
  private apiUrl = '/api/users';

  constructor(private http: HttpClient) {}

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.apiUrl);
  }

  getUser(id: number): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/${id}`);
  }

  createUser(user: User): Observable<User> {
    return this.http.post<User>(this.apiUrl, user);
  }
}
```

### Dependency Injection
```typescript
@Injectable()
export class NotificationService {
  constructor(
    private logger: LoggerService,
    private config: ConfigService
  ) {}

  notify(message: string) {
    this.logger.log(message);
  }
}
```

## Core Concepts

### Lifecycle Hooks
```typescript
export class UserListComponent implements
  OnInit,
  OnChanges,
  OnDestroy
{
  @Input() users: User[] = [];

  ngOnInit() {
    // Initialize component, fetch data
    this.loadUsers();
  }

  ngOnChanges(changes: SimpleChanges) {
    // Respond to input changes
    if (changes['users']) {
      this.onUsersChanged();
    }
  }

  ngOnDestroy() {
    // Cleanup subscriptions, remove listeners
    this.subscription?.unsubscribe();
  }

  private loadUsers() { /* ... */ }
  private onUsersChanged() { /* ... */ }
}
```

**Lifecycle Order:**
1. `ngOnChanges` - When input properties change
2. `ngOnInit` - After first ngOnChanges
3. `ngDoCheck` - Every change detection cycle
4. `ngAfterContentInit` - After content is initialized
5. `ngAfterContentChecked` - After content is checked
6. `ngAfterViewInit` - After view is initialized
7. `ngAfterViewChecked` - After view is checked
8. `ngOnDestroy` - When component is destroyed

### Modules
```typescript
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    UserListComponent,
    UserDetailComponent,
    UserFormComponent
  ],
  imports: [
    CommonModule,
    FormsModule
  ],
  exports: [
    UserListComponent,
    UserDetailComponent
  ]
})
export class UserModule { }
```

### Lazy Loading
```typescript
const routes: Routes = [
  { path: 'users', loadChildren: () =>
      import('./users/users.module').then(m => m.UsersModule)
  }
];
```

## Advanced Patterns

### Content Projection
```typescript
// Parent component
<app-card>
  <div class="header">Card Title</div>
  <div class="content">Card content</div>
</app-card>

// Card component
@Component({
  selector: 'app-card',
  template: `
    <div class="card">
      <ng-content select=".header"></ng-content>
      <ng-content select=".content"></ng-content>
      <ng-content></ng-content>
    </div>
  `
})
export class CardComponent { }
```

### ViewChild and ContentChild
```typescript
@Component({
  selector: 'app-form',
  template: `<app-input #firstInput></app-input>`
})
export class FormComponent implements AfterViewInit {
  @ViewChild('firstInput') firstInput!: InputComponent;

  ngAfterViewInit() {
    this.firstInput.focus();
  }
}
```

### Custom Directive
```typescript
@Directive({
  selector: '[appHighlight]'
})
export class HighlightDirective {
  constructor(private el: ElementRef) {
    this.el.nativeElement.style.backgroundColor = 'yellow';
  }
}

// Usage: <p appHighlight>Highlighted text</p>
```

## Encapsulation

### View Encapsulation Modes
```typescript
@Component({
  selector: 'app-card',
  template: `<div class="card">...</div>`,
  styles: [`.card { color: blue; }`],
  encapsulation: ViewEncapsulation.Emulated // Default
})
export class CardComponent { }
```

- **Emulated** (default): CSS scoped to component
- **None**: Global styles
- **ShadowDom**: Uses browser shadow DOM

## Change Detection

### OnPush Strategy
```typescript
@Component({
  selector: 'app-user',
  template: `<div>{{ user.name }}</div>`,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserComponent {
  @Input() user!: User;

  constructor(private cdr: ChangeDetectorRef) {}

  manualDetection() {
    this.cdr.markForCheck();
  }
}
```

## Provider Patterns

### Multi-Provider
```typescript
@NgModule({
  providers: [
    { provide: VALIDATORS, useValue: emailValidator, multi: true },
    { provide: VALIDATORS, useValue: minLengthValidator, multi: true }
  ]
})
export class ValidatorsModule { }
```

### Factory Pattern
```typescript
@NgModule({
  providers: [
    {
      provide: ConfigService,
      useFactory: (env: EnvironmentService) => {
        return env.production ?
          new ProdConfigService() :
          new DevConfigService();
      },
      deps: [EnvironmentService]
    }
  ]
})
export class AppModule { }
```

## Testing Components
```typescript
describe('UserCardComponent', () => {
  let component: UserCardComponent;
  let fixture: ComponentFixture<UserCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [UserCardComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(UserCardComponent);
    component = fixture.componentInstance;
  });

  it('should emit deleted when delete button clicked', () => {
    spyOn(component.deleted, 'emit');
    component.user = { id: 1, name: 'John', email: 'john@example.com' };
    fixture.detectChanges();

    fixture.debugElement.query(By.css('button')).nativeElement.click();
    expect(component.deleted.emit).toHaveBeenCalled();
  });
});
```

## Performance Optimization

1. **Use OnPush**: Reduces change detection cycles
2. **Unsubscribe**: Prevent memory leaks
3. **TrackBy**: Optimize *ngFor rendering
4. **Lazy Load**: Load modules on demand
5. **Avoid property binding in templates**: Use async pipe

```typescript
// Bad
users: User[] = [];

// Good
users$ = this.userService.getUsers();

<!-- Template -->
<app-user *ngFor="let user of users$ | async; trackBy: trackByUserId">
</app-user>
```

## Best Practices

1. **Smart vs Presentational**: Container components handle logic
2. **One Responsibility**: Each component has a single purpose
3. **Input/Output**: Use @Input/@Output for communication
4. **Services**: Handle business logic and HTTP
5. **DI**: Always use dependency injection
6. **OnDestroy**: Clean up subscriptions

## Resources

- [Angular Documentation](https://angular.io/docs)
- [Angular Best Practices](https://angular.io/guide/styleguide)
- [Component Interaction](https://angular.io/guide/component-interaction)
