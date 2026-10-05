---
name: angular
description: Angular framework patterns, standalone components, Signals, and dependency injection. Use when building Angular apps, components, services, or migrating from NgModules.
---

## angular

### Core Concepts
- Standalone components: default since v15, no NgModules needed
- Signals: signal(), computed(), effect() for reactive state without Zone.js
- Dependency injection: inject() function, @Injectable() providers
- RxJS integration: Observables, async pipe, operators for async workflows
- Directives: structural (*ngIf, *ngFor) and attribute ([ngClass], [ngStyle])

### Common Patterns
- Smart + dumb component separation with @Input/@Output signals
- Lazy loading routes with loadComponent in standalone setup
- Reactive forms with FormBuilder, validators, and valueChanges
- HTTP interceptors for auth headers and error handling
- Content projection with ng-content and multi-slot projection

### Best Practices
- Prefer signals over RxJS for state, keep RxJS for event streams
- Use OnPush change detection with signals for performance
- Leverage inject() rather than constructor injection
- Keep components small, delegate logic to services
- Use Angular CLI for code generation and schematics

### Common Code Patterns
- Standalone component with signal-based state management
- Route guard as injectable function returning Observable/boolean
- Typed reactive form with FormGroup and validation
