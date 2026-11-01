---
name: flutter-test-to-jest
description: Port flutter_test files (unit `test()` and widget `testWidgets()`) from the poc_vedaxl test/ folder to Jest + @testing-library/react-native v14 in the workspace that owns the code, with fixtures, fake repositories and fake services. Use it when porting or writing parity tests for a ported Dart file, when asked to "port the tests for X", "convert <name>_test.dart", or to check test parity; also when a ported RN test needs pumpVida-style setup, 360px/French variants, timers or fake HTTP. Remember RNTL v14 `render` is async.
---

# flutter_test → Jest + RNTL v14

**The one rule that bites:** in `@testing-library/react-native` v14, `render` returns a promise. Always `await render(...)` (and
`await renderVida(...)`). A missing `await` gives empty queries and act() warnings.

## Where the test goes

Find the Dart test file in `docs/migration/TRACEABILITY.md` §e; it lists the Jest target(s). The rule (from `CLAUDE.md`):
`test/<x>_test.dart` → `<workspace>/__tests__/<x camelCase>.test.ts(x)` in the workspace that owns the code. Mixed files are split:

| Dart test content | Target |
|---|---|
| `fromJson` / fixture parsing, repository requests over HTTP, `ApiException` handling | `packages/api/__tests__/<x>.test.ts` |
| Pure rules (checkout maths, bid validation, countdowns, route mapping, reward-wheel landing, `PhotoRules`, `MemberState` logic, validators) | `packages/core/__tests__/<x>.test.ts` |
| ARB / translation / plural tests | `packages/i18n/__tests__/<x>.test.ts` |
| UI kit widgets | `packages/ui/__tests__/<x>.test.tsx` |
| Screens, stores, services, navigation (`testWidgets`, `ChangeNotifier` state) | `apps/mobile/__tests__/<x>.test.tsx` |

Start the file with `// Ported from: test/<x>_test.dart`. Keep **the same `group` and test names** (`describe` / `test`), in the same order,
so the Dart and Jest results can be compared one-to-one. If a case can't be ported (layout overflow, Hero), keep it as
`test.skip('<same name>', …)` with a one-line reason; don't silently drop it.

## Procedure

1. Read the Dart test file, its helpers (`helpers.dart`, `cart_fakes.dart`, `account_v3_helpers.dart`) and the fixtures it loads.
2. Count `test(` / `testWidgets(` (`grep -cE "^\s*(test|testWidgets)\(" file`) so you can check you ported them all.
3. Port the fakes first (see below), then the tests group by group.
4. Run `npm test -w <workspace> -- <file>`; fix the code under test if the behaviour differs from Dart (the Dart test is the spec).
5. Update the §e row: status `tested` when every case passes (or is skipped with a reason); note counts if the file was split.

## Translating the pieces

API details and finder tables: [references/flutter-test-api.md](references/flutter-test-api.md). The essentials:

```dart
testWidgets('empty orders show the shop button', (tester) async {
  await pumpVida(tester, AccountSource(apis: fakeApis(orders: []), child: const OrdersPage()), state: signedIn());
  await tester.pumpAndSettle();
  expect(find.text('Start shopping'), findsOneWidget);
  await tester.tap(find.text('Start shopping'));
  expect(AppNav.tab.value, 1);
});
```
```tsx
// Ported from: test/orders_v2_test.dart
test('empty orders show the shop button', async () => {
  await renderVida(<OrdersPage />, { repositories: fakeApis({ orders: [] }), member: signedIn() });
  expect(await screen.findByText('Start shopping')).toBeOnTheScreen();
  fireEvent.press(screen.getByText('Start shopping'));
  expect(navigationSpy.lastRoute()).toBe('products');
});
```

- **Copy text assertions as they are** (English by default). They check the copy, and the same i18n keys give the same strings.
- **`pumpVida` → `renderVida`** in `apps/mobile/__tests__/helpers/renderVida.tsx`: wraps the real providers (QueryClient with
  `retry: false` and `gcTime: Infinity`, i18n initialised with the real JSON in the requested locale, `VidaOverlayProvider`, the navigation
  container, the repositories context with fakes, initial store state). Reset Zustand stores between tests (`store.setState(initial, true)`
  in `beforeEach`), like the Dart tests create a fresh `MemberState(ticking: false)`.
- **`pump()` / `pumpAndSettle()`** → `await screen.findBy…`, `await waitFor(() => …)`, or `await act(async () => {})`.
  With timers (countdowns, 10 s polling, 3.4 s splash, toasts): `jest.useFakeTimers()` and `await act(() => jest.advanceTimersByTimeAsync(ms))`.
- **`tester.view.physicalSize = Size(990, 2340)` + `devicePixelRatio 2.75`** (= 360 dp wide): mock `useWindowDimensions` to
  `{ width: 360, height: 851 }`. `expect(tester.takeException(), isNull)` (no overflow) can't be checked in RN: assert that the screen renders
  and the long French strings are present.
- **Locales:** `renderVida(ui, { locale: 'fr' })`; for i18n package tests call `initI18n('fr')`.

## Fakes and fixtures

- **HTTP-level** (repository tests): `fakeFetch()` + `fixture()` from `packages/api/__tests__/helpers.ts`; build `new ApiClient({ baseUrl,
  fetch, getIdToken })` and assert `calls[i].url / method / headers / body`. Dart `MockClient` handlers become the `reply` callback.
- **Repository-level** (screen tests): Dart fakes subclass the repository (`class _FakeCart extends CartRepository`). In TS, create an
  object typed as the repository (`Pick<CartRepository, 'cart' | 'addItem'>` or a class extending it with `super(dummyClient)`), returning
  parsed fixtures; record calls in arrays the test asserts on. Put shared fakes in `apps/mobile/__tests__/helpers/` (`cartFakes.ts`,
  `accountFakes.ts`), mirroring `cart_fakes.dart` and `account_v3_helpers.dart`.
- **Services** (push, live auction updates, photo upload, auth): pass fakes through the same injection points as Dart
  (`AuctionLiveUpdates`, `PhotoUploadService`, `AdminAccess({ readClaim, currentUid })`, `PushTokenSync({ account, tokens })`), not module
  mocks. Native modules are already mocked globally in `apps/mobile/jest.setup.js` (gesture handler, AsyncStorage); add new global mocks
  there only for modules every test needs.
- **Fixtures** are in `packages/api/__tests__/fixtures/*.json` (36 files, byte-for-byte copies). Never edit them; if a test needs a
  variant, derive it in the test (`{ ...fixture('v3_cart'), lines: [] }`).
- **Streams** (`StreamController` for Firestore / `received` pushes): a tiny emitter in the test (`const emit = (v) => listeners.forEach(l => l(v))`),
  wrapped in `act()`.

## Done when

- [ ] Every Dart `test`/`testWidgets` has a Jest `test` with the same name (or `test.skip` with a reason); counts match the §e row.
- [ ] `await render` everywhere; no act() warnings; fake timers restored (`afterEach(() => jest.useRealTimers())`).
- [ ] Tests pass with `npm test -w <workspace>`; the §e row is updated.
