---
name: rxjs-patterns
description: Master RxJS in Angular with observables, operators, subjects, error handling, and reactive patterns for building responsive applications.
---

# RxJS Patterns in Angular

Master reactive programming in Angular with RxJS observables, operators, and best practices.

## Core Patterns

### Observable Creation
```typescript
import { Observable, of, from, interval } from 'rxjs';

// From array
const numbers$ = from([1, 2, 3, 4]);

// From promise
const user$ = from(fetch('/api/user'));

// Interval
const timer$ = interval(1000);
```

### Operators
```typescript
import { map, filter, switchMap, catchError } from 'rxjs/operators';

this.http.get<User[]>('/api/users').pipe(
  map(users => users.filter(u => u.active)),
  catchError(error => of([]))
).subscribe(users => console.log(users));
```

### Service Pattern
```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  private users$ = new BehaviorSubject<User[]>([]);

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>('/api/users').pipe(
      tap(users => this.users$.next(users)),
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    console.error('Error:', error);
    return throwError(() => new Error('Something went wrong'));
  }
}
```

## Best Practices

1. Unsubscribe to prevent memory leaks
2. Use async pipe in templates
3. Handle errors with catchError
4. Use shareReplay for caching
5. Avoid nested subscriptions
6. Use switchMap for HTTP requests

## Resources
- https://rxjs.dev
- https://angular.io/guide/rx-library
