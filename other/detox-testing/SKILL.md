---
name: detox-testing
description: "Authors React Native E2E tests with Detox (Wix) - gray-box architecture (runs in-process with the app), `element(by.id|by.text|by.label)` matchers, `waitFor()` for explicit sync beyond Detox's automatic async tracking, Jest runner. Use when the app is React Native and speed matters. For Flutter use flutter-testing; for black-box cross-platform use appium-testing; for YAML-declarative flows use maestro-flows; for non-RN native use xcuitest-suite or espresso-suite."
---

# detox-testing

[det]: https://wix.github.io/Detox/

Detox's "gray-box" architecture is load-bearing: unlike Appium (black-box,
external server), it runs **in the app's process** (per [detox-docs][det]),
so it "automatically monitors asynchronous operations to eliminate test
flakiness at its core" ([detox-docs][det]) - tracking network calls,
animations, and timers without explicit sync hooks.

## When to use

- The app is React Native (the framework's intended use case).
- Speed matters more than cross-stack reuse (Detox is faster than
  Appium for RN apps).
- The team uses Jest (Detox's default runner; built-in integration).

If the app is native iOS/Android (not RN), use
`xcuitest-suite` or
`espresso-suite`. For
non-RN-specific cross-platform, see
`appium-testing`.

## How to use

1. Install Detox and scaffold with `npx detox init` (Step 1).
2. Add `testID` props to the RN components the tests will target (Step 4).
3. Build the app for the target device configuration with `detox build` (Step 2).
4. Author `e2e/*.test.js` specs using `element(by.id(...))` matchers, actions,
   and assertions (Step 3, [references/element-api.md](references/element-api.md)).
5. Add `waitFor(...).withTimeout(N)` only where Detox's auto-sync misses a
   genuine async condition (Step 5).
6. Run `detox test --configuration <cfg>` and iterate until green (Step 6).
7. Wire build + test into CI as a headless job (Step 7).

## Step 1 - Install

```bash
npm install --save-dev detox
npx detox init   # scaffolds .detoxrc.js + e2e/ directory
```

`.detoxrc.js` configures device + app + runner; the default
template is sensible.

## Step 2 - Build the app for testing

```bash
# Android
detox build --configuration android.emu.debug

# iOS
detox build --configuration ios.sim.debug
```

The build configuration in `.detoxrc.js` references the project's
existing build commands (Gradle / xcodebuild) - Detox doesn't
introduce a new build pipeline.

Verify: `detox build` must finish and emit the app binary before Step 6.
If it fails, fix the underlying native build error (Gradle / xcodebuild) and
re-run - the fix lives in the RN build config, not Detox.

## Step 3 - Author tests with matchers

Match elements with `element(by.id(...))`; prefer `by.id` (the RN `testID`
prop) for stable, translation-proof lookups. The full matcher catalog,
combinators, action verbs, and assertions are in
[references/element-api.md](references/element-api.md).

Example test:

```javascript
describe('Cart flow', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it('adds item to cart', async () => {
    await element(by.id('product-BOOK-001')).tap();
    await element(by.id('add-to-cart-button')).tap();
    await expect(element(by.id('cart-count'))).toHaveText('1');
  });

  it('applies promo code', async () => {
    await element(by.id('promo-input')).typeText('WELCOME10');
    await element(by.id('apply-promo-button')).tap();
    await expect(element(by.id('subtotal'))).toHaveText('$22.49');
  });
});
```

## Step 4 - Production code: set `testID`

In RN production code:

```jsx
<TouchableOpacity testID="add-to-cart-button" onPress={addToCart}>
  <Text>Add to cart</Text>
</TouchableOpacity>

<TextInput testID="promo-input" value={code} onChangeText={setCode} />
```

`testID` is React Native's prop for `accessibilityIdentifier`
(iOS) / `resource-id` (Android). Detox finds elements by it.

## Step 5 - `waitFor` for explicit sync

When Detox's automatic tracking misses something:

```javascript
await waitFor(element(by.id('async-result')))
  .toBeVisible()
  .withTimeout(10000);

await waitFor(element(by.id('progress-bar')))
  .not.toBeVisible()
  .whileElement(by.id('list')).scroll(100, 'down');
```

`waitFor(...).withTimeout(N)` polls the condition for up to N ms.
`whileElement(...)` performs an action (scroll) while waiting - 
useful for "scroll until visible."

## Step 6 - Run

```bash
detox test --configuration android.emu.debug
detox test --configuration ios.sim.debug

# Specific test file
detox test e2e/cart.test.js --configuration ios.sim.debug

# Headless mode
detox test --headless
```

Verify: assert every spec reports green. If one fails, read the Detox error
(element not found / timeout), fix the matcher or add a `waitFor` (Step 5),
and re-run that spec before wiring CI. Detox then runs headless on CI
platforms such as Travis CI, CircleCI, and Jenkins (per [detox-docs][det]).

## Step 7 - CI integration

```yaml
jobs:
  detox-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: npm ci
      - uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 34
          script: |
            detox build --configuration android.emu.debug
            detox test --configuration android.emu.debug --headless

  detox-ios:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v5
      - run: npm ci
      - run: npx pod-install
      - run: |
          detox build --configuration ios.sim.debug
          detox test --configuration ios.sim.debug
```

## Worked example

A React Native store app needs an E2E check that adding a book to the cart
updates the badge count.

1. The product card already renders `<TouchableOpacity testID="product-BOOK-001">`
   and the cart badge renders `<Text testID="cart-count">` (Step 4).
2. Build once: `detox build --configuration ios.sim.debug` (Step 2).
3. Author `e2e/cart.test.js` with the `'adds item to cart'` spec from Step 3.
4. Run `detox test e2e/cart.test.js --configuration ios.sim.debug` (Step 6).
5. Detox launches the simulator, taps the product and the add button, and its
   auto-sync waits for the state update before the assertion runs. The spec
   passes: the badge reads `1`, with no `sleep` anywhere in the test.

## Anti-patterns

| Anti-pattern                                                         | Why it fails                                                              | Fix |
|----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Querying by `by.text` for translatable strings                       | Translation breaks tests.                                                 | Use `by.id` (testID) for stable lookups (Step 3). |
| `await sleep(2000)` between actions                                   | Detox's auto-sync is the point; sleeps mask real flake.                  | `waitFor(...)` for genuine async; trust auto-sync otherwise. |
| Skipping `device.reloadReactNative()` between tests                   | State leaks; tests pollute each other.                                   | `beforeEach` reload (Step 3 example). |
| `by.type('RCTView')` (iOS-specific class)                              | Tests break on Android (different class name).                           | Use `by.id` (cross-platform) or platform-conditional code. |
| Per-test app reinstall                                                | Slow; Detox's reload is faster.                                           | `device.reloadReactNative()` over `device.launchApp()`. |
| Long-press without device wake                                        | Simulator may be in screensaver; tap misses.                              | `device.shake()` / `device.openURL()` to wake. |

## Limitations

- **React Native only.** Native non-RN apps need
  `xcuitest-suite` or
  `appium-testing`.
- **iOS support depends on RN version.** Per [detox-docs][det],
  some iOS features may have caveats per RN version.
- **Test runner choice.** Detox works with any runner; Jest is
  built-in. Mocha / Jasmine require additional config.
- **In-process gray-box trade-off.** Detox knows about the JS
  bridge; native iOS/Android crashes that don't surface to JS may
  be invisible until next interaction.

## References

- [det][det] - Detox overview: gray-box architecture, automatic
  async monitoring, JS test syntax, CI-ready, RN-specific.
- [references/element-api.md](references/element-api.md) - matcher catalog
  (`by.id`, `by.text`, `by.label`, `by.type`, `by.traits`), combinators,
  actions, and assertions.
- `xcuitest-suite`,
  `espresso-suite`,
  `appium-testing`,
  `maestro-flows` - alternatives.
