---
name: state-implementation
description: Implement NgRx store with actions and reducers, build selectors, create effects for async operations, configure entity adapters, and integrate HTTP APIs with state management.
sasmp_version: "1.3.0"
bonded_agent: 06-state-management
bond_type: PRIMARY_BOND
---

# State Implementation Skill

## Quick Start

### Simple Service-Based State
```typescript
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class UserStore {
  private usersSubject = new BehaviorSubject<User[]>([]);
  users$ = this.usersSubject.asObservable();

  constructor(private http: HttpClient) {}

  loadUsers() {
    this.http.get<User[]>('/api/users').subscribe(
      users => this.usersSubject.next(users)
    );
  }

  addUser(user: User) {
    this.http.post<User>('/api/users', user).subscribe(
      newUser => {
        const current = this.usersSubject.value;
        this.usersSubject.next([...current, newUser]);
      }
    );
  }
}

// Usage
export class UserListComponent {
  users$ = this.userStore.users$;

  constructor(private userStore: UserStore) {}
}
```

### NgRx Basics
```typescript
// 1. Define actions
export const loadUsers = createAction('[User] Load Users');
export const loadUsersSuccess = createAction(
  '[User] Load Users Success',
  props<{ users: User[] }>()
);
export const loadUsersError = createAction(
  '[User] Load Users Error',
  props<{ error: string }>()
);

// 2. Create reducer
const initialState: UserState = { users: [], loading: false };

export const userReducer = createReducer(
  initialState,
  on(loadUsers, state => ({ ...state, loading: true })),
  on(loadUsersSuccess, (state, { users }) => ({
    ...state,
    users,
    loading: false
  })),
  on(loadUsersError, (state, { error }) => ({
    ...state,
    error,
    loading: false
  }))
);

// 3. Create effect
@Injectable()
export class UserEffects {
  loadUsers$ = createEffect(() =>
    this.actions$.pipe(
      ofType(loadUsers),
      switchMap(() =>
        this.userService.getUsers().pipe(
          map(users => loadUsersSuccess({ users })),
          catchError(error => of(loadUsersError({ error })))
        )
      )
    )
  );

  constructor(
    private actions$: Actions,
    private userService: UserService
  ) {}
}

// 4. Use in component
@Component({...})
export class UserListComponent {
  users$ = this.store.select(selectUsers);
  loading$ = this.store.select(selectLoading);

  constructor(private store: Store) {
    this.store.dispatch(loadUsers());
  }
}
```

## NgRx Core Concepts

### Store
```typescript
// Dispatch action
this.store.dispatch(loadUsers());

// Select state
this.store.select(selectUsers).subscribe(users => {
  console.log(users);
});

// Select with observable
this.users$ = this.store.select(selectUsers);

// Multiple selects
this.store.select(selectUsers, selectLoading).subscribe(([users, loading]) => {
  // ...
});
```

### Selectors
```typescript
// Feature selector
export const selectUserState = createFeatureSelector<UserState>('users');

// Select from feature
export const selectUsers = createSelector(
  selectUserState,
  state => state.users
);

// Selector composition
export const selectActiveUsers = createSelector(
  selectUsers,
  users => users.filter(u => u.active)
);

// Memoized selector
export const selectUserById = (id: number) => createSelector(
  selectUsers,
  users => users.find(u => u.id === id)
);

// With props
export const selectUsersByRole = createSelector(
  selectUsers,
  (users: User[], { role }: { role: string }) =>
    users.filter(u => u.role === role)
);

// Usage with props
this.store.select(selectUsersByRole, { role: 'admin' });
```

### Effects
```typescript
// Side effect - HTTP call
@Injectable()
export class UserEffects {
  loadUsers$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UserActions.loadUsers),
      switchMap(() =>
        this.userService.getUsers().pipe(
          map(users => UserActions.loadUsersSuccess({ users })),
          catchError(error => of(UserActions.loadUsersError({ error })))
        )
      )
    )
  );

  // Non-dispatching effect
  logActions$ = createEffect(
    () => this.actions$.pipe(
      tap(action => console.log(action))
    ),
    { dispatch: false }
  );

  constructor(
    private actions$: Actions,
    private userService: UserService
  ) {}
}
```

## Entity Adapter

### Setup
```typescript
export interface User {
  id: number;
  name: string;
  email: string;
}

export const adapter = createEntityAdapter<User>({
  selectId: (user: User) => user.id,
  sortComparer: (a: User, b: User) => a.name.localeCompare(b.name)
});

export interface UserState extends EntityState<User> {
  loading: boolean;
  error: string | null;
}

const initialState = adapter.getInitialState({
  loading: false,
  error: null
});
```

### Reducer with Adapter
```typescript
export const userReducer = createReducer(
  initialState,
  on(loadUsers, state => ({ ...state, loading: true })),
  on(loadUsersSuccess, (state, { users }) =>
    adapter.setAll(users, { ...state, loading: false })
  ),
  on(addUserSuccess, (state, { user }) =>
    adapter.addOne(user, state)
  ),
  on(updateUserSuccess, (state, { user }) =>
    adapter.updateOne({ id: user.id, changes: user }, state)
  ),
  on(deleteUserSuccess, (state, { id }) =>
    adapter.removeOne(id, state)
  )
);

// Export selectors
export const {
  selectIds,
  selectEntities,
  selectAll,
  selectTotal
} = adapter.getSelectors(selectUserState);
```

## Facade Pattern

```typescript
@Injectable()
export class UserFacade {
  users$ = this.store.select(selectAllUsers);
  loading$ = this.store.select(selectUsersLoading);
  error$ = this.store.select(selectUsersError);

  constructor(private store: Store) {}

  loadUsers() {
    this.store.dispatch(loadUsers());
  }

  addUser(user: User) {
    this.store.dispatch(addUser({ user }));
  }

  updateUser(id: number, changes: Partial<User>) {
    this.store.dispatch(updateUser({ id, changes }));
  }

  deleteUser(id: number) {
    this.store.dispatch(deleteUser({ id }));
  }
}

// Component usage simplified
@Component({...})
export class UserListComponent {
  users$ = this.userFacade.users$;
  loading$ = this.userFacade.loading$;

  constructor(private userFacade: UserFacade) {
    this.userFacade.loadUsers();
  }
}
```

## Angular Signals

```typescript
import { signal, computed, effect } from '@angular/core';

// Create signal
const count = signal(0);

// Read value
console.log(count()); // 0

// Update value
count.set(1);
count.update(c => c + 1);

// Computed value
const doubled = computed(() => count() * 2);

// Effect
effect(() => {
  console.log(`Count is ${count()}`);
  console.log(`Doubled is ${doubled()}`);
});

// Signal-based state
@Component({...})
export class CounterComponent {
  count = signal(0);
  doubled = computed(() => this.count() * 2);

  increment() {
    this.count.update(c => c + 1);
  }
}
```

## HTTP Integration

### HttpClient with Interceptor
```typescript
@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = this.authService.getToken();
    const authReq = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
    return next.handle(authReq);
  }
}

// Register
@NgModule({
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ]
})
export class AppModule { }
```

### Caching Strategy
```typescript
@Injectable()
export class CachingService {
  private cache = new Map<string, any>();

  get<T>(key: string, request: Observable<T>, ttl: number = 3600000): Observable<T> {
    if (this.cache.has(key)) {
      return of(this.cache.get(key));
    }

    return request.pipe(
      tap(data => {
        this.cache.set(key, data);
        setTimeout(() => this.cache.delete(key), ttl);
      })
    );
  }
}

// Usage
getUsers() {
  return this.caching.get(
    'users',
    this.http.get<User[]>('/api/users'),
    5 * 60 * 1000 // 5 minutes
  );
}
```

## Testing State

```typescript
describe('User Store', () => {
  let store: MockStore;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [StoreModule.forRoot({ users: userReducer })]
    });
    store = TestBed.inject(Store) as MockStore;
  });

  it('should load users', () => {
    const action = loadUsers();
    const completion = loadUsersSuccess({ users: mockUsers });

    const effect$ = new UserEffects(
      hot('a', { a: action }),
      mockUserService
    ).loadUsers$;

    const result = cold('b', { b: completion });
    expect(effect$).toBeObservable(result);
  });

  it('should select users', (done) => {
    store.setState({ users: { users: mockUsers } });
    store.select(selectUsers).subscribe(users => {
      expect(users).toEqual(mockUsers);
      done();
    });
  });
});
```

## Best Practices

1. **Normalize State**: Flat structure, avoid nesting
2. **Single Responsibility**: Each reducer handles one feature
3. **Use Facades**: Simplify component-store interaction
4. **Memoize Selectors**: Prevent unnecessary recalculations
5. **Handle Errors**: Always include error states
6. **Lazy Load Stores**: Register feature stores when needed
7. **Time-Travel Debugging**: Use Redux DevTools

## Advanced Patterns

### Composition Pattern
```typescript
// Combine multiple stores
@Injectable()
export class AppFacade {
  users$ = this.userFacade.users$;
  products$ = this.productFacade.products$;
  cart$ = this.cartFacade.cart$;

  constructor(
    private userFacade: UserFacade,
    private productFacade: ProductFacade,
    private cartFacade: CartFacade
  ) {}
}
```

### Feature Flags
```typescript
export const selectFeatureFlags = createFeatureSelector<FeatureFlags>('features');
export const selectFeatureEnabled = (feature: string) => createSelector(
  selectFeatureFlags,
  flags => flags[feature]?.enabled ?? false
);

// Component
<div *ngIf="featureEnabled$ | async">New Feature</div>
```

## Resources

- [NgRx Documentation](https://ngrx.io/)
- [Entity Adapter](https://ngrx.io/guide/entity)
- [DevTools](https://github.com/reduxjs/redux-devtools-extension)
