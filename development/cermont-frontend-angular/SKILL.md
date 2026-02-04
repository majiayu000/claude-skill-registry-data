---
name: cermont.frontend.angular
description: |
  Angular standalone components, RxJS patterns, and reactive forms for frontend development.
  Use when: Building Angular components, services, guards, interceptors, or working with RxJS observables.
triggers:
  - Angular
  - RxJS
  - standalone
  - OnPush
  - interceptors
  - guards
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
role: secondary
scope: frontend
---

<!-- Cermont Project Fit -->
## Project Fit

| Attribute | Value |
|-----------|-------|
| **Applies to** | frontend |
| **Requires** | Angular, pnpm |
| **Not for this repo** | React, Vue |
| **Status** | Secondary (use `angular-best-practices` as primary) |

### Guardrails

**Does NOT do:**
- Install dependencies without user approval
- Modify pnpm-lock.yaml directly

**Safety Checklist:**
```bash
pnpm --filter @cermont/frontend lint
pnpm --filter @cermont/frontend test
# Rollback: git restore -SW .
```
<!-- End Project Fit -->

## Quick Start

### Standalone Component

```typescript
@Component({
  selector: 'app-player-list',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './player-list.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayerListComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();
  players$ = new BehaviorSubject<Player[]>([]);

  constructor(private playerService: PlayerService) {}

  ngOnInit(): void {
    this.playerService.list().pipe(
      takeUntil(this.destroy$),
      map(page => page.content)
    ).subscribe(players => this.players$.next(players));
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

### Service with State Management

```typescript
@Injectable({ providedIn: 'root' })
export class WalletService implements OnDestroy {
  private balance$ = new BehaviorSubject<PlayerBalance | null>(null);
  private destroy$ = new Subject<void>();

  getBalance(): Observable<PlayerBalance | null> {
    return this.balance$.asObservable();
  }

  refreshBalance(playerId: number): void {
    this.http.get<PlayerBalance>(`${this.apiUrl}/${playerId}/balance`).pipe(
      takeUntil(this.destroy$),
      catchError(error => {
        console.error('Balance fetch failed:', error);
        return of(null);
      })
    ).subscribe(balance => this.balance$.next(balance));
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Standalone | All new components | `standalone: true` in decorator |
| Cleanup | Every subscription | `takeUntil(this.destroy$)` |
| State | Service-level state | `BehaviorSubject<T>` |
| Performance | List rendering | `trackBy` + `OnPush` |
| Forms | All user input | Reactive forms with `FormGroup` |

## Common Patterns

### HTTP with Error Handling

**When:** Any API call

```typescript
this.http.post<Resource>(this.apiUrl, request).pipe(
  catchError(error => {
    console.error('Create failed:', error);
    return throwError(() => error);
  })
);
```

### Form with Validation

**When:** User data entry

```typescript
this.form = this.fb.group({
  email: ['', [Validators.required, Validators.email]],
  amount: [null, [Validators.required, Validators.min(0)]]
});
```

## See Also

- [hooks](references/hooks.md) - Lifecycle hooks and cleanup patterns
- [components](references/components.md) - Component structure and standalone patterns
- [data-fetching](references/data-fetching.md) - HTTP services and caching
- [state](references/state.md) - BehaviorSubject and state management
- [forms](references/forms.md) - Reactive forms and validation
- [performance](references/performance.md) - OnPush, trackBy, and optimization

## Related Skills

- See the **typescript** skill for type definitions and interfaces
- See the **spring-boot** skill for backend API patterns
- See the **playwright** skill for E2E testing
- See the **frontend-design** skill for CSS and UI patterns