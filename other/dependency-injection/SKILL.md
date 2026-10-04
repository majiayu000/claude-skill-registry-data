---
id: angular.dependency-injection
name: Angular Dependency Injection
description: >
  Reviews, designs, and refactors Angular dependency injection for services, providers, injectors, InjectionToken, inject(), testing overrides, standalone apps, NgModules, SSR, lazy loading, and provider scopes.
stack:
  - Angular
  - TypeScript
category: dependency-injection
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - dependency injection
  - Angular DI
  - provider scope
  - InjectionToken
  - inject()
  - NullInjectorError
  - circular dependency
  - service provider
  - TestBed provider override
compatibility:
  angular:
    min: "2"
    conservativeBaseline: "12+"
    injectFunctionFrom: "14"
    standaloneStableFrom: "15"
    activeReference: "19 / 20 / 21"
---

# Angular Dependency Injection

## Purpose

Use this skill to apply Angular Dependency Injection correctly so code stays decoupled, testable, maintainable, and compatible with the target Angular version.

This skill covers service creation, provider scope, injector hierarchy, `InjectionToken`, constructor injection, `inject()`, TestBed overrides, lazy-loaded boundaries, SSR-safe providers, and common DI failures such as `NullInjectorError`, duplicate providers, and circular dependencies.

## When to Use

Use this skill when:

- Creating or refactoring an Angular service.
- Reviewing `providers` in components, directives, modules, routes, bootstrap config, or tests.
- Deciding between constructor injection and `inject()`.
- Introducing configuration values, ports, adapters, or strategy implementations.
- Fixing `NullInjectorError`, circular dependencies, or unexpected duplicate service instances.
- Writing tests that need mocks, spies, local provider overrides, or component-level injected services.
- Designing shared libraries, lazy-loaded features, microfrontends, or SSR-compatible services.
- A component or service manually creates dependencies with `new`.

## When Not to Use

Do not use this skill when:

- The code is AngularJS 1.x; this skill targets Angular 2+.
- The task is about generic TypeScript object construction outside Angular's injector.
- The change is purely about service responsibility boundaries; use `angular.services.single-responsibility-services` first.
- The problem is primarily state ownership; use `angular.state.signals-vs-rxjs` or architecture skills first.

## Inputs Required

Identify these inputs before recommending a DI pattern:

```txt
Angular version
architecture style: standalone, NgModules, or mixed
provider location: root, platform, bootstrap, route, NgModule, component, directive, or test
service lifetime: global singleton, feature scoped, route scoped, component scoped, or per test
runtime target: browser, SSR, library, microfrontend, or worker
testing stack: Jest, Jasmine/Karma, Vitest, or unknown
existing convention: constructor injection, inject(), or mixed
```

Inspect these files when relevant:

```txt
package.json
angular.json
app.config.ts
main.ts
app.module.ts
*.routes.ts
*.module.ts
*.component.ts
*.directive.ts
*.service.ts
*.spec.ts
```

## Version Compatibility

Use version-aware DI guidance:

```txt
Angular 2-5:
  use constructor injection and NgModule providers
  avoid modern standalone and inject() patterns

Angular 6-13:
  prefer @Injectable({ providedIn: 'root' }) for app-wide services
  use constructor injection as the safest default
  use NgModule providers for legacy app-wide or feature scope where required

Angular 14:
  inject() is available in supported injection contexts
  standalone APIs may exist but should not be assumed as the project default
  constructor injection remains the most portable default

Angular 15-18:
  standalone APIs are stable
  providedIn, application providers, route providers, and inject() are valid when project style supports them
  keep legacy compatibility when working inside NgModule-based code

Angular 19-21:
  prefer current Angular DI style when the project is current
  use providedIn, application providers, route providers, standalone providers, and inject() according to scope
  still avoid experimental APIs unless the project opts into them
```

For shared libraries, choose the lowest supported Angular version of the consumers, not the newest version known by the agent.

## Decision Rules

Use this provider scope policy:

```txt
app-wide stateless service -> providedIn: 'root'
app-wide configuration value -> InjectionToken with root provider or application provider
feature orchestration -> route, feature, or facade provider based on lifecycle
component-local state -> component providers
view-only dependency override -> viewProviders when children should not see the provider
legacy module app -> NgModule providers when required by project style
standalone app bootstrap -> ApplicationConfig or bootstrapApplication providers
multi-extension point -> multi provider
test double -> TestBed provider override or fixture injector when component-scoped
```

Use constructor injection when:

```txt
the project targets Angular 2-13
the codebase convention favors constructors
dependencies are part of the explicit class contract
maximum readability and compatibility matter
```

Use `inject()` when:

```txt
the project supports Angular 14+
the code is in a valid injection context
the project convention allows it
the code is a functional guard, resolver, interceptor, factory, token factory, or field initializer
constructor length would add noise without improving clarity
```

Use `InjectionToken` when:

```txt
injecting interfaces, primitives, configuration, strategy functions, adapters, or abstract ports
the runtime token must exist after TypeScript erases types
multiple implementations may be swapped by provider configuration
```

## Execution Workflow

Use this workflow:

```txt
1. Detect Angular version and project style.
2. Identify the dependency lifetime and injector scope.
3. Locate current provider declarations.
4. Detect manual instantiation, duplicate providers, and public mutable state.
5. Select constructor injection, inject(), or token-based injection.
6. Place the provider at the narrowest correct lifecycle scope.
7. Update tests with explicit provider overrides.
8. Explain risks around singleton behavior, SSR, lazy loading, and test isolation.
```

## Do

Use DI instead of manual construction:

```ts
@Component({
  selector: "app-user-panel",
  templateUrl: "./user-panel.component.html",
})
export class UserPanelComponent {
  constructor(private readonly userService: UserService) {}
}
```

Use modern `inject()` only in supported contexts:

```ts
@Injectable({ providedIn: "root" })
export class UserFacade {
  private readonly userApi = inject(UserApiService);
  private readonly userState = inject(UserStateService);
}
```

Use root providers for true app-wide services:

```ts
@Injectable({
  providedIn: "root",
})
export class UserApiService {}
```

Use component providers for isolated component state:

```ts
@Component({
  selector: "app-user-panel",
  templateUrl: "./user-panel.component.html",
  providers: [UserPanelStateService],
})
export class UserPanelComponent {
  private readonly state = inject(UserPanelStateService);
}
```

Use `InjectionToken` for configuration and ports:

```ts
export interface AppConfig {
  apiUrl: string;
}

export const APP_CONFIG = new InjectionToken<AppConfig>("APP_CONFIG");
```

```ts
export const appConfig: ApplicationConfig = {
  providers: [
    {
      provide: APP_CONFIG,
      useValue: {
        apiUrl: "https://api.example.com",
      },
    },
  ],
};
```

Use provider variants intentionally:

```ts
[
  { provide: LoggerPort, useClass: ConsoleLoggerService },
  { provide: API_URL, useValue: "https://api.example.com" },
  { provide: LoggerPort, useExisting: AppLoggerService },
  {
    provide: AuthStrategy,
    useFactory: () => {
      const config = inject(APP_CONFIG);
      return config.useMockAuth
        ? new MockAuthStrategy()
        : new RealAuthStrategy();
    },
  },
];
```

Use multi providers for extension points:

```ts
{
  provide: HTTP_INTERCEPTORS,
  useClass: AuthInterceptor,
  multi: true,
}
```

Mock dependencies explicitly in tests:

```ts
await TestBed.configureTestingModule({
  declarations: [UserComponent],
  providers: [
    {
      provide: UserService,
      useValue: {
        getUsers: jest.fn().mockReturnValue(of([])),
      },
    },
  ],
}).compileComponents();
```

When a provider is declared on the component, get the component-scoped instance:

```ts
const state = fixture.debugElement.injector.get(UserPanelStateService);
```

## Do Not

Avoid manual service construction:

```ts
export class UserComponent {
  private readonly userService = new UserService();
}
```

Avoid placing every service in root:

```ts
@Injectable({ providedIn: "root" })
export class WizardStepStateService {}
```

Avoid public mutable implementation details:

```ts
export class UserStateService {
  usersSubject = new BehaviorSubject<User[]>([]);
}
```

Avoid injecting TypeScript interfaces directly:

```ts
constructor(private readonly config: AppConfig) {}
```

Avoid using `inject()` outside an injection context:

```ts
ngOnInit(): void {
  const userService = inject(UserService);
}
```

Avoid provider placement based only on "where it compiles". Provider location defines lifecycle.

Avoid circular service dependency chains:

```txt
AuthService -> UserService -> PermissionService -> AuthService
```

## Output Format

Use this format when reviewing DI:

```md
## DI Diagnosis

- Angular version:
- Architecture style:
- Provider scope:
- Current issue:

## Recommended Pattern

- ...

## Code Proposal

- Provide the smallest compatible code change.

## Testing Impact

- ...

## Risks

- ...

## Validation Checklist

- ...
```

## Review Checklist

- [ ] No Angular service is instantiated manually with `new`.
- [ ] Provider scope matches the intended lifecycle.
- [ ] App-wide services use `providedIn: 'root'` when appropriate.
- [ ] Component-local state is not accidentally global.
- [ ] Component providers are intentional and tested through the fixture injector when needed.
- [ ] Configuration values and abstract ports use `InjectionToken`.
- [ ] `inject()` is used only in valid injection contexts and compatible Angular versions.
- [ ] Duplicate providers are intentional.
- [ ] Circular dependencies are identified and broken through boundaries, tokens, facades, or extracted services.
- [ ] Tests use explicit mocks, spies, or provider overrides.
- [ ] SSR-sensitive providers avoid direct browser globals without tokens or guards.

## Risks

- Moving a provider can change singleton behavior.
- Adding component providers can create one service instance per component subtree.
- Moving local state to root can leak state between screens.
- Swapping constructor injection to `inject()` can reduce compatibility for legacy projects.
- TestBed overrides may not affect component-level providers unless overridden correctly.
- Factory providers can hide runtime branches that require dedicated tests.
- Circular dependencies often signal poor boundaries, not just DI syntax problems.

## Examples

```txt
Problem:
NullInjectorError for APP_CONFIG.

Likely fix:
Create one exported InjectionToken and provide it once at application, route, module, or test scope.
Do not recreate the token in multiple files.
```

```txt
Problem:
Two components do not share expected state.

Likely cause:
The state service is listed in component providers, creating isolated instances.
Move it to root or a feature provider if shared lifecycle is intended.
```

```txt
Problem:
Unit test mock is ignored.

Likely cause:
The component declares its own provider.
Override the component provider or read the component-scoped service from fixture.debugElement.injector.
```

## Expected Output

1. Detect Angular version and DI architecture style.
2. Identify the intended dependency lifecycle.
3. Recommend the narrowest correct provider scope.
4. Replace manual instantiation with Angular DI.
5. Use `InjectionToken` for runtime-safe configuration and abstract ports.
6. Provide testing guidance for provider overrides and component-scoped services.
7. Explain risks around singleton behavior, lazy loading, SSR, and compatibility.
