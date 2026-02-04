---
name: routing-performance-implementation
description: Configure routing with lazy loading, implement route guards, set up preloading strategies, optimize change detection, analyze bundles, and implement performance optimizations.
sasmp_version: "1.3.0"
bonded_agent: 05-routing-performance
bond_type: PRIMARY_BOND
---

# Routing & Performance Implementation Skill

## Quick Start

### Basic Routing
```typescript
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent, AboutComponent, NotFoundComponent } from './components';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'about', component: AboutComponent },
  { path: '**', component: NotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
```

### Navigation
```typescript
import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  template: `
    <button (click)="goHome()">Home</button>
    <a routerLink="/about">About</a>
    <a routerLink="/users" [queryParams]="{ tab: 'active' }">Users</a>
  `
})
export class NavComponent {
  constructor(private router: Router) {}

  goHome() {
    this.router.navigate(['/']);
  }
}
```

### Route Parameters
```typescript
const routes: Routes = [
  { path: 'users/:id', component: UserDetailComponent },
  { path: 'users/:id/posts/:postId', component: PostDetailComponent }
];

// Component
@Component({...})
export class UserDetailComponent {
  userId!: string;

  constructor(private route: ActivatedRoute) {
    this.route.params.subscribe(params => {
      this.userId = params['id'];
    });
  }
}

// Or with snapshot
ngOnInit() {
  const id = this.route.snapshot.params['id'];
}
```

## Lazy Loading

### Feature Modules with Lazy Loading
```typescript
// app-routing.module.ts
const routes: Routes = [
  { path: '', component: HomeComponent },
  {
    path: 'users',
    loadChildren: () => import('./users/users.module').then(m => m.UsersModule)
  },
  {
    path: 'products',
    loadChildren: () => import('./products/products.module').then(m => m.ProductsModule)
  }
];

// users/users-routing.module.ts
const routes: Routes = [
  { path: '', component: UserListComponent },
  { path: ':id', component: UserDetailComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UsersRoutingModule { }
```

### Lazy Loading with Standalone Components
```typescript
const routes: Routes = [
  {
    path: 'admin',
    loadChildren: () => import('./admin/admin.routes').then(m => m.ADMIN_ROUTES)
  }
];

// admin/admin.routes.ts
export const ADMIN_ROUTES: Routes = [
  { path: '', component: AdminDashboardComponent },
  { path: 'users', component: AdminUsersComponent }
];
```

## Route Guards

### CanActivate Guard
```typescript
import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';
import { map } from 'rxjs/operators';

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean> {
    return this.authService.isAuthenticated$.pipe(
      map(isAuth => {
        if (isAuth) return true;
        this.router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
        return false;
      })
    );
  }
}

// Usage
const routes: Routes = [
  { path: 'admin', component: AdminComponent, canActivate: [AuthGuard] }
];
```

### CanDeactivate Guard
```typescript
export interface CanComponentDeactivate {
  canDeactivate: () => Observable<boolean> | boolean;
}

@Injectable()
export class CanDeactivateGuard implements CanDeactivate<CanComponentDeactivate> {
  canDeactivate(component: CanComponentDeactivate): Observable<boolean> | boolean {
    return component.canDeactivate();
  }
}

// Component
@Component({...})
export class FormComponent implements CanComponentDeactivate {
  form!: FormGroup;

  canDeactivate(): Observable<boolean> | boolean {
    return !this.form.dirty || confirm('Discard changes?');
  }
}

// Usage
{ path: 'form', component: FormComponent, canDeactivate: [CanDeactivateGuard] }
```

### Resolve Guard
```typescript
@Injectable()
export class UserResolver implements Resolve<User> {
  constructor(private userService: UserService) {}

  resolve(route: ActivatedRouteSnapshot): Observable<User> {
    return this.userService.getUser(route.params['id']);
  }
}

// Usage
{
  path: 'users/:id',
  component: UserDetailComponent,
  resolve: { user: UserResolver }
}

// Component receives data
@Component({...})
export class UserDetailComponent {
  user!: User;

  constructor(private route: ActivatedRoute) {
    this.route.data.subscribe(data => {
      this.user = data['user'];
    });
  }
}
```

## Query Parameters

```typescript
// Navigation
this.router.navigate(['/users'], {
  queryParams: {
    page: 1,
    sort: 'name',
    filter: 'active'
  }
});

// Reading
this.route.queryParams.subscribe(params => {
  const page = params['page'];
  const sort = params['sort'];
});

// Template
<a [routerLink]="['/users']" [queryParams]="{ page: 2, sort: 'name' }">
  Next Page
</a>
```

## Fragment (Hash)

```typescript
// Navigation
this.router.navigate(['/docs'], { fragment: 'section1' });

// Reading
this.route.fragment.subscribe(fragment => {
  console.log('Fragment:', fragment);
});

// Template
<a routerLink="/docs" fragment="section1">Section 1</a>
```

## Preloading Strategies

```typescript
// Default: no preloading
RouterModule.forRoot(routes);

// Preload all lazy modules
RouterModule.forRoot(routes, {
  preloadingStrategy: PreloadAllModules
});

// Custom preloading strategy
@Injectable()
export class SelectivePreloadingStrategy implements PreloadingStrategy {
  preload(route: Route, load: () => Observable<any>): Observable<any> {
    if (route.data && route.data['preload']) {
      return load();
    }
    return of(null);
  }
}

// Usage
const routes: Routes = [
  { path: 'users', loadChildren: '...', data: { preload: true } }
];

RouterModule.forRoot(routes, {
  preloadingStrategy: SelectivePreloadingStrategy
})
```

## Route Reuse Strategy

```typescript
@Injectable()
export class CustomRouteReuseStrategy implements RouteReuseStrategy {
  storedRoutes: { [key: string]: RouteData } = {};

  shouldDetach(route: ActivatedRouteSnapshot): boolean {
    return route.data['cache'] === true;
  }

  store(route: ActivatedRouteSnapshot, detachedTree: DetachedRouteHandle): void {
    this.storedRoutes[route.url.join('/')] = { route, handle: detachedTree };
  }

  shouldAttach(route: ActivatedRouteSnapshot): boolean {
    return !!this.storedRoutes[route.url.join('/')];
  }

  retrieve(route: ActivatedRouteSnapshot): DetachedRouteHandle | null {
    return this.storedRoutes[route.url.join('/')]?.handle || null;
  }

  shouldReuseRoute(future: ActivatedRouteSnapshot, current: ActivatedRouteSnapshot): boolean {
    return future.routeConfig === current.routeConfig;
  }
}
```

## Performance Optimization

### Code Splitting
```typescript
// Only load admin module when needed
{
  path: 'admin',
  loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule)
}
```

### Change Detection with Routes
```typescript
@Component({
  selector: 'app-root',
  template: `<router-outlet></router-outlet>`,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AppComponent { }
```

### Scroll Position

```typescript
// Scroll to top on route change
RouterModule.forRoot(routes, {
  scrollPositionRestoration: 'top'
})

// Or custom scroll
export class ScrollToTopComponent implements OnInit {
  constructor(private router: Router) {}

  ngOnInit() {
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe(() => {
      window.scrollTo(0, 0);
    });
  }
}
```

## Advanced Patterns

### Auxiliary Routes
```typescript
// URL: /users/1(admin:admin-panel)
<router-outlet></router-outlet>
<router-outlet name="admin"></router-outlet>

// Navigation
this.router.navigate([
  { outlets: {
    primary: ['users', userId],
    admin: ['admin-panel']
  }}
]);
```

### Child Routes with Components
```typescript
const routes: Routes = [
  {
    path: 'dashboard',
    component: DashboardComponent,
    children: [
      { path: 'stats', component: StatsComponent },
      { path: 'reports', component: ReportsComponent }
    ]
  }
];

// DashboardComponent template
<nav>
  <a routerLink="stats" routerLinkActive="active">Stats</a>
  <a routerLink="reports" routerLinkActive="active">Reports</a>
</nav>
<router-outlet></router-outlet>
```

## Testing Routes

```typescript
describe('Routing', () => {
  let router: Router;
  let location: Location;
  let fixture: ComponentFixture<AppComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppRoutingModule, AppComponent]
    }).compileComponents();

    router = TestBed.inject(Router);
    location = TestBed.inject(Location);
    fixture = TestBed.createComponent(AppComponent);
  });

  it('should navigate to home', fakeAsync(() => {
    router.navigate(['']);
    tick();
    expect(location.path()).toBe('/');
  }));
});
```

## Best Practices

1. **Lazy load features**: Reduce initial bundle size
2. **Use route guards**: Control access and preload data
3. **Implement RouteReuseStrategy**: Cache components when needed
4. **Handle 404s**: Provide meaningful error pages
5. **Query params for filters**: Keep state in URL
6. **Preload strategically**: Balance performance vs initial load
7. **Use fragments for anchors**: Scroll to page sections

## Resources

- [Angular Routing Guide](https://angular.io/guide/router)
- [Route Guards](https://angular.io/guide/router-tutorial-toh)
- [Lazy Loading](https://angular.io/guide/lazy-loading-ngmodules)
