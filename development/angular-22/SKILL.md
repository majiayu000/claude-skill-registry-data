---
name: angular-22
description: Write, review and migrate Angular 21-22 code (checked against @angular/core 22.2.4) the way the current framework works - zoneless change detection by default, components OnPush by default since v22, signal inputs/outputs/model/queries, computed and linkedSignal instead of effect-driven state, the resource/rxResource/httpResource APIs (params and stream, string statuses, value() throwing in the error state), built-in control flow with track, inject() and @Service, and Vitest-based TestBed tests without fakeAsync. Use when code imports @angular/*, when a view stops updating after removing zone.js or upgrading, when converting @Input/@Output/@ViewChild/*ngIf/*ngFor/ngOnChanges/EventEmitter, when loading data with HttpClient into signals, or when you see Angular 14-19 idioms like zone.run, provideExperimentalZonelessChangeDetection, resource({ request, loader }), ResourceStatus.Loading, fakeAsync or ChangeDetectionStrategy.Default.
license: MIT
---

# Angular 22

Angular 22 (`@angular/core@22.2.4`, `@angular/cli@22.2.5`, November 2026) is two defaults away from
the Angular most examples describe: since v21 applications run **without zone.js**, and since v22
every component without a `changeDetection` setting is **OnPush**. Code written from Angular 14-19
memory still compiles and then silently stops refreshing the screen. Everything below was run
against 22.2.4 with the CLI's Vitest runner.

## 1. Know which Angular you are writing

```sh
npm ls @angular/core @angular/cli typescript
rg -n zone angular.json package.json src/main.ts src/app/app.config.ts
```

| Version | Default that changed | What it means for new code |
| --- | --- | --- |
| 19 | `standalone: true` is the default | Don't write `standalone: true`; list dependencies in `imports`. |
| 20 | `effect`, `linkedSignal`, `toSignal` and the signal component APIs stable; `afterRender` renamed `afterEveryRender`; `*ngIf`/`*ngFor`/`*ngSwitch` deprecated | Resource API renamed (`params`, `stream`), `value()` throws in the error state (section 5). |
| 21 | **zoneless by default**, Vitest is the CLI test runner, signal forms experimental | No `zone.js` polyfill; `provideZoneChangeDetection()` opts back into zones. |
| 22 | **components are OnPush by default** (`ChangeDetectionStrategy.Eager` is the new name for `Default`); `strictTemplates` on by default; `resource`, `rxResource`, `httpResource` and signal forms stable; `@Service()`; `FetchBackend` is the default `HttpBackend` (`withFetch()` deprecated); TypeScript 6.0 required (6.1+ unsupported, so not TS 7) | Mutating state that a template reads no longer repaints it. |

`ng update` to 22 adds `changeDetection: ChangeDetectionStrategy.Eager` to existing components and
`strictTemplates: false` where it was unset, so an upgraded app can look like v21. New components get
neither. Check what the file you are editing actually uses.

## 2. Change detection: what refreshes a view now

Without zone.js nothing patches `setTimeout`, promises, `fetch` or WebSocket callbacks. A view is
refreshed only after one of these notifications:

- a signal read by the template (or by a `computed` it reads) changes;
- a bound template or host listener runs (`(click)`, `host: { '(keydown)': ... }`);
- `ChangeDetectorRef.markForCheck()` (the `async` pipe calls it);
- `ComponentRef.setInput()` (what parents and `fixture.componentRef.setInput` use).

And with OnPush (the v22 default) a component is checked only when it is marked dirty that way or
when an input receives a **new reference**.

| Zone-era habit | Result on 22.2.4 (zoneless) |
| --- | --- |
| `this.status = 'done'` inside `setTimeout`, `.subscribe`, after `await`, in a socket callback | DOM keeps the old value |
| wrapping it in `zone.run(() => ...)` | still stale: `NgZone.run` just calls the function |
| `NgZone.onStable` / `onMicrotaskEmpty` to wait for rendering | never emit; use `afterNextRender` / `afterEveryRender` |
| `provideZoneChangeDetection()` to "fix" it | throws NG0908 "In this configuration Angular requires Zone.js" unless zone.js is loaded |
| `this.items.push(x)` and pass `items` to a child | child (OnPush by default) keeps showing the old list |
| `items.update(a => { a.push(x); return a })` | same array, `Object.is` says unchanged: nothing reading it refreshes |
| `cdr.detectChanges()` after an in-place mutation | refreshes this view; OnPush children with the same array reference still stale |

Fix by making template state reactive, not by forcing change detection:

```ts
@Component({
  selector: 'app-room-status',
  template: `<p>{{ label() }}</p> <app-guest-list [guests]="guests()" />`,
  imports: [GuestList],
})
export class RoomStatus {
  private readonly socket = inject(RoomSocket);
  readonly state = signal<'joining' | 'joined'>('joining');
  readonly guests = signal<readonly Guest[]>([]);
  readonly label = computed(() => (this.state() === 'joined' ? 'In the room' : 'Joining…'));

  constructor() {
    const off = this.socket.listen({
      joined: () => this.state.set('joined'),
      // New array every time: signal consumers and OnPush children see the change.
      guestArrived: (guest) => this.guests.update((list) => [...list, guest]),
    });
    inject(DestroyRef).onDestroy(off);
  }

  async rejoin() {
    this.state.set('joining');
    await this.socket.rejoin(); // after an await nothing is marked dirty for you...
    this.state.set('joined'); // ...but a signal write is a notification
  }
}
```

`markForCheck()` plus immutable updates is also correct, for code you can't convert yet. Keep
`ChangeDetectionStrategy.Eager` only for a component that hosts arbitrary user components; otherwise
delete the marker when you touch the file. More in [the change detection reference](references/change-detection.md).

## 3. Component APIs

```ts
@Component({ selector: 'app-seat-map', templateUrl: './seat-map.html' })
export class SeatMap {
  readonly seats = input.required<Seat[]>();                    // [seats]="..."; read as seats()
  readonly zone = input<'A' | 'B'>('A', { alias: 'section' });   // public name: section
  readonly dense = input(false, { transform: booleanAttribute }); // allows bare <app-seat-map dense>
  readonly maxSeats = input(4, { transform: numberAttribute });   // allows maxSeats="6"
  readonly picked = model<string | null>(null);                  // [(picked)]: input + pickedChange
  readonly hold = output<Seat>();                                // (hold)="..."; this.hold.emit(seat)
  private readonly grid = viewChild.required<ElementRef<HTMLElement>>('grid');
  readonly legendItems = contentChildren(LegendItem);
}
```

- Inputs are read-only signals: call them (`seats()`), in templates too. Only `model()` is writable
  (`picked.set(id)` updates the parent through `[(picked)]`, which also binds to a parent signal).
- Without `booleanAttribute`, a bare `dense` attribute is the string `''`: with strict templates
  (default) the parent fails to compile with TS2322. Keep the transform when converting
  `@Input({ transform: booleanAttribute })`.
- `model('x')` already creates the `xChange` output. Keeping an old `@Output() xChange` next to it is
  a compile error (NG1054).
- Reading a required input or a required query in a field initializer or the constructor is a
  compile error (NG8118). Derive with `computed`, or read in `afterNextRender`, an event or
  `ngOnInit`.
- Queries return signals: `this.grid().nativeElement`. Optional queries are `undefined` until the
  view renders.
- `ngOnChanges` recomputation becomes `computed`; `ngAfterViewInit` focus or measuring becomes
  `afterNextRender` (or stays in `ngAfterViewInit`, reading the query signal).
- Prefer `host: { '[class.dense]': 'dense()', '(keydown)': 'onKey($event)' }` over `@HostBinding` and
  `@HostListener` in new code. Templates may use `protected` members and, since 22.2, `private` ones.

Schematics do most of a conversion: `ng generate @angular/core:signal-input-migration`,
`output-migration`, `signal-queries-migration` (or `signals` for all three), `control-flow-migration`,
`inject-migration`, `self-closing-tags-migration`. Review their output: they keep `@Input` where a
field is written to.

## 4. Derived state: computed, linkedSignal, effect

- `computed(() => ...)` for anything derived. It is lazy, cached and **synchronously** consistent.
- `linkedSignal` for state that resets when its source changes but can also be set by the user:

  ```ts
  readonly sortBy = signal<'date' | 'title'>('date');
  readonly cursor = linkedSignal({ source: this.sortBy, computation: () => 0 }); // back to the top
  next() { this.cursor.update((c) => c + 20); }
  ```

  The short form `linkedSignal(() => options()[0])` resets on every change of what it reads; the
  `{ source, computation: (src, previous) => ... }` form can keep the previous choice when it is
  still valid (pass both generic types when you use `previous`).
- `effect` is for syncing to the outside world (localStorage, a chart library, logging). Effects run
  later, during change detection, so state copied by an effect is stale until then: an effect-based
  "reset page to 1" lets one request go out for the old page first.
  `allowSignalWrites` is deprecated and unnecessary; `untracked()` stops a read from becoming a
  dependency. For DOM work after rendering use `afterRenderEffect`.
- Signals compare with `Object.is`. Always produce new objects or arrays in `set`/`update`; pass
  `{ equal }` only for deliberate structural equality.
- `debounced(source, ms)` (22, **experimental**) returns a resource of the settled value.

## 5. Async data: resource, rxResource, httpResource

| Angular 19 code (fails to compile on 22) | Angular 20+ |
| --- | --- |
| `resource({ request: () => ..., loader: ({ request }) => ... })` | `resource({ params: () => ..., loader: ({ params, abortSignal }) => ... })` |
| `rxResource({ request, loader: ({ request }) => obs$ })` | `rxResource({ params, stream: ({ params }) => obs$ })` |
| `ResourceStatus.Loading`, `.Resolved`, ... | string union: `'idle' 'loading' 'reloading' 'resolved' 'error' 'local'` |
| `res.value()` is `undefined` after an error | `res.value()` **throws** `ResourceValueError` in the error state |

```ts
readonly term = signal('');
readonly results = httpResource<HitPage>(() =>
  this.term() ? { url: '/api/hits', params: { q: this.term(), cursor: this.cursor() } } : undefined,
);
// Guard every read of value(): it throws while results.status() === 'error'.
readonly hits = computed(() => (this.results.hasValue() ? this.results.value().items : []));
```

```html
@if (results.isLoading()) { <p>Loading…</p> }
@else if (results.error()) { <p>Failed.</p> <button (click)="results.reload()">Retry</button> }
@else if (results.hasValue()) { @for (hit of results.value().items; track hit.id) { ... } }
```

- `params` returning `undefined` makes the resource `idle`: no request. Return `undefined`, not
  `{ q: undefined }`.
- A params change aborts the previous load (`abortSignal`; `rxResource` and `httpResource`
  unsubscribe, which cancels the `HttpClient` request). Hand-written `subscribe()` calls do not.
- `'loading'` (params changed) has no value; `'reloading'` (`reload()`) keeps the previous value;
  `set`/`update` make it `'local'`. `isLoading()` covers both loading states.
- A template that reads `value()` anywhere outside a `hasValue()`/`error()` guard, for example a
  results count in a toolbar, crashes the view when the request fails. TestBed rethrows it.
- `httpResource` goes through `HttpClient`, so interceptors apply; `rxResource` wraps an existing
  service method that returns an Observable. Both need `provideHttpClient()`.
- `params: ({ chain }) => chain(userRes)?.teamId` makes one resource wait for another and mirror
  its loading and error states.

Recipes (pagination, optimistic local updates, debounced search, SSR caching with `id`, testing) are
in [the resource reference](references/resources.md).

## 6. RxJS interop

- `toSignal(obs$, { initialValue })` subscribes immediately and must run in an injection context
  (field initializer or constructor); `requireSync: true` for BehaviorSubject-like sources.
- `toObservable(sig)` emits from an effect, so asynchronously; not a replacement for `computed`.
- `takeUntilDestroyed()` in an injection context, or `takeUntilDestroyed(this.destroyRef)` elsewhere.
- `outputFromObservable(obs$)` turns a stream into an output; `outputToObservable(ref)` the reverse.
- Observables still drive `HttpClient`; the signal layer starts where the template reads.

## 7. Templates

- `@if (cond) {} @else if {} @else {}`, `@switch (x) { @case (1) {} @default {} }`.
- `@for (item of items(); track item.id) { } @empty { }`: `track` is mandatory (NG5002). Track a
  stable key, not the object (`track item` re-creates every row when data is refetched) and not
  `$index` when items can be inserted or reordered. `$index`, `$first`, `$last`, `$even`, `$count`
  are available.
- `@let total = cart().total;` declares a template variable.
- `@defer (on viewport; prefetch on idle) { <heavy-chart /> } @placeholder { ... }` lazy-loads.
- Optional chaining in templates returns `undefined` since v22 (it returned `null` before): a
  `=== null` check on `a?.b` no longer matches.
- NgIf, NgFor and NgSwitch are deprecated since v20; NgClass and NgStyle are not, but `[class.x]`
  and `[style.x]` bindings need no import.

## 8. DI, services and HTTP

- `inject(Token)` in field initializers is the idiom; constructor parameters still work.
- `@Service()` (22) is the shorthand for `@Injectable({ providedIn: 'root' })`;
  `@Service({ autoProvided: false })` must be listed in `providers`. `@Injectable` is not deprecated.
- Functional interceptors and guards: `provideHttpClient(withInterceptors([authInterceptor]))` with
  `const authInterceptor: HttpInterceptorFn = (req, next) => next(req.clone({...}))`.
- `HttpClient` uses `fetch` by default in 22. Remove `withFetch()` (deprecated); add `withXhr()`
  only if you need upload progress events.
- Router: `paramsInheritanceStrategy` defaults to `'always'` in 22; `withComponentInputBinding()`
  binds route params to `input()`s.

## 9. Testing (Vitest via `ng test`)

- `ng test` runs Vitest in jsdom through `@angular/build:unit-test`; `--watch=false` for CI. Use
  `vi.fn()`, `vi.spyOn()`, `expect(...)`, not Jasmine spies.
- TestBed is zoneless. Prefer `await fixture.whenStable()` after an action over
  `fixture.detectChanges()`: it waits for the change detection Angular scheduled itself, which is
  what production does.
- Assigning `fixture.componentInstance.x = v` and calling `fixture.detectChanges()` does **not**
  repaint an OnPush (default) component and raises no error. Drive components the way the app does:
  `fixture.componentRef.setInput('name', value)`, DOM events, or the signals they read.
- `fakeAsync`/`tick` need zone.js and throw "zone-testing.js is needed for the fakeAsync() test helper".
  Use `vi.useFakeTimers()`, then `await vi.advanceTimersByTimeAsync(ms)` and `TestBed.tick()` (the
  render scheduler's own timer is faked too), or fake only what you need:
  `vi.useFakeTimers({ toFake: ['setInterval', 'clearInterval'] })`.
- `TestBed.tick()` synchronously runs effects and change detection (`flushEffects` is deprecated).
- **HTTP tests:** a pending `HttpClient` request keeps the app unstable, so `await fixture.whenStable()`
  before you `flush()` hangs until the test times out. Trigger, `TestBed.tick()`,
  `httpTesting.expectOne(...)`, `flush`, then `await fixture.whenStable()`. `req.cancelled` tells
  you whether a superseded request was aborted.

Recipes in [the change detection reference](references/change-detection.md#testing).

## 10. Upgrading to 22

1. Update with the CLI (it contacts the npm registry), keep the lockfile in the same commit, and
   make sure TypeScript is 6.0.x:

   ```sh
   ng update @angular/core@22 @angular/cli@22
   ng test --watch=false
   ```

2. Review what the migrations added (`ChangeDetectionStrategy.Eager`, `strictTemplates: false`,
   `withXhr()`, `$safeNavigationMigration(...)`) and remove each once the code no longer needs it.
3. Zoneless: drop `zone.js` from `polyfills` in both build and test targets and from `package.json`;
   grep for `NgZone`, `onStable`, `onMicrotaskEmpty`, `zone.run`, `fakeAsync`, `waitForAsync`.
4. Make template state signals (or `markForCheck` + immutable updates), then delete `Eager` markers.
5. Full checklist with grep patterns: [the migration reference](references/migration.md).

## 11. Anti-patterns

| Don't | Do |
| --- | --- |
| `zone.run(() => this.x = v)` or `setTimeout(() => cdr.detectChanges())` | `this.x.set(v)` |
| mutate arrays or objects held in signals or passed to inputs | `update(list => [...list, item])` |
| `effect(() => this.page.set(1))` to reset dependent state | `linkedSignal({ source, computation })` |
| `effect(() => this.total.set(...))` | `computed(() => ...)` |
| `{{ res.value()?.count }}` outside a guard | `@if (res.hasValue()) { {{ res.value().count }} }` |
| `resource({ request, loader: ({ request }) })` | `resource({ params, loader: ({ params }) })` |
| manual `subscribe` + `loading`/`error` fields | `rxResource`/`httpResource` |
| `input<boolean>(false)` for a bare attribute | `input(false, { transform: booleanAttribute })` |
| `model()` plus a hand-written `xChange` output | `model()` alone |
| `@for (x of xs(); track x)` / `track $index` on refetched data | `track x.id` |
| `fakeAsync(() => { tick(500) })` | `vi.useFakeTimers()` + `advanceTimersByTimeAsync` |
| `await fixture.whenStable()` with an unflushed HTTP request | flush first, then `whenStable` |
| re-adding zone.js to make a view update | find the missing signal or notification |

## References

- [Change detection, zoneless and testing](references/change-detection.md)
- [resource, rxResource, httpResource recipes](references/resources.md)
- [Migrating Angular 14-21 code to 22](references/migration.md)
- [Sources checked](references/sources.md)
