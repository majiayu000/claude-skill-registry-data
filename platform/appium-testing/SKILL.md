---
name: appium-testing
description: "Runs and repairs mobile UI suites driven by Appium - sessions that stop launching after an Appium server upgrade, an iOS or Android half switched off in CI because the simulator or emulator will not boot, unstable waits around one-time codes and other out-of-app steps, and locators that break on every redesign. Covers the WebDriver protocol, driver choice per platform (XCUITest for iOS, UiAutomator2 / Espresso for Android, Mac2 for macOS, Windows for desktop), `desiredCapabilities`, client bindings in JS / Python / Java / Ruby / .NET, and running against simulators, emulators, and device farms. Use when a mobile suite fails, flakes, or only runs on one platform, or when one suite must cover both iOS and Android."
---

# appium-testing

[app]: https://appium.io/docs/en/latest/

The driver model is the load-bearing concept: Appium itself is the
WebDriver protocol; per-platform automation is a **driver** (XCUITest
driver talks to iOS, UiAutomator2 / Espresso to Android, Mac2 to
macOS, Windows to Windows desktop). Client libraries exist for
JavaScript, Python, Java, Ruby, and .NET (per [appium-docs][app]).

## When to use

- A team needs **one** test suite to cover iOS + Android.
- The product is multi-platform (mobile + desktop + TV) and one
  framework should drive all of them.
- Existing Selenium expertise transfers (same WebDriver mental
  model).
- Device-farm integration matters (BrowserStack / Sauce Labs / AWS
  Device Farm all support Appium natively).

If the app is iOS-only, `xcuitest-suite`
is lighter (no external server). For React Native specifically,
`detox-testing` is faster.

## Step 1 - Install Appium server + driver

```bash
npm install -g appium

# Install per-platform drivers:
appium driver install xcuitest         # iOS
appium driver install uiautomator2     # Android
appium driver install espresso         # Android (alternative; gray-box)
appium driver install mac2             # macOS desktop
appium driver install windows          # Windows desktop

# Verify:
appium driver list
```

## Step 2 - Start the server

```bash
appium server -p 4723
```

The default port is 4723; client tests connect to
`http://localhost:4723` (no `/wd/hub` suffix in Appium 2.x).

## Step 3 - Author a test (JavaScript example)

```javascript
import { remote } from 'webdriverio';

const capabilities = {
  platformName: 'Android',
  'appium:automationName': 'UiAutomator2',
  'appium:deviceName': 'Android Emulator',
  'appium:app': '/path/to/app.apk',
};

describe('Cart flow', () => {
  let driver;

  before(async () => {
    driver = await remote({
      hostname: 'localhost',
      port: 4723,
      capabilities,
    });
  });

  after(async () => {
    await driver.deleteSession();
  });

  it('adds an item to cart', async () => {
    const addButton = await driver.$('id=add_to_cart_button');
    await addButton.click();

    const cartCount = await driver.$('id=cart_count');
    const text = await cartCount.getText();
    expect(text).toBe('1');
  });
});
```

The `automationName` capability picks the driver:
`UiAutomator2` (Android), `XCUITest` (iOS), `Espresso` (Android
gray-box), `Mac2`, `Windows`.

## Step 4 - Capabilities catalog

| Capability              | Use                                                  |
|-------------------------|------------------------------------------------------|
| `platformName`          | `iOS` / `Android` / `Mac` / `Windows`                 |
| `appium:automationName`  | Driver name (XCUITest / UiAutomator2 / Espresso etc.) |
| `appium:deviceName`     | Logical device name (Simulator / Emulator / specific) |
| `appium:platformVersion` | OS version (e.g. `14.0`)                             |
| `appium:app`            | Path to .apk / .ipa                                   |
| `appium:bundleId` / `appium:appPackage` | Pre-installed app                    |
| `appium:noReset`        | Don't reinstall app between sessions                  |
| `appium:newCommandTimeout` | Server idle timeout (default 60s)                  |

For device-farm runs, capabilities also include the farm's
authentication tokens / device-pool selection.

## Step 5 - Selector strategies (cross-platform)

```javascript
// By accessibility ID - the most cross-platform
await driver.$('~login-button').click();   // ~ prefix in WebdriverIO

// By id - works for both platforms with platform-prefixed IDs
await driver.$('id=add_to_cart_button');     // Android
await driver.$('id=add-to-cart-button');     // iOS uses accessibility ID

// XPath - works everywhere; brittle (selector-quality anti-pattern)
await driver.$('//XCUIElementTypeButton[@name="Submit"]');

// Image-based locator (Appium-specific) - fallback when no IDs
await driver.findElementByImage('./assets/login-button.png');
```

The cross-platform strategy: production code sets the same
accessibility ID on both iOS (`accessibilityIdentifier`) and
Android (`contentDescription` or `resource-id`). Tests use one
selector for both.

## Step 6 - Run

```bash
# Local with one platform
WDIO_OS=android wdio run wdio.conf.js

# Multi-platform: WebdriverIO multi-capability config
# wdio.conf.js
exports.config = {
    capabilities: [
        { platformName: 'iOS', 'appium:platformVersion': '17.4', ...iosCaps },
        { platformName: 'Android', 'appium:platformVersion': '14', ...androidCaps },
    ],
    runner: 'local',
    services: ['appium'],
};
```

The `services: ['appium']` line auto-starts the Appium server
inside the test runner - no separate server step.

## Step 7 - CI integration

```yaml
# Multi-platform matrix
jobs:
  ui-tests:
    strategy:
      matrix:
        platform: [iOS, Android]
    runs-on: ${{ matrix.platform == 'iOS' && 'macos-15' || 'ubuntu-latest' }}
    steps:
      - uses: actions/checkout@v5

      - if: matrix.platform == 'Android'
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 34
          script: WDIO_OS=android npx wdio run wdio.conf.js

      - if: matrix.platform == 'iOS'
        run: |
          xcrun simctl boot 'iPhone 15'
          WDIO_OS=ios npx wdio run wdio.conf.js
```

## Anti-patterns

| Anti-pattern                                                         | Why it fails                                                              | Fix |
|----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Per-platform separate test code                                       | Defeats Appium's reuse value.                                             | One test, multi-capability config (Step 6). |
| XPath selectors as default                                            | Slowest selector strategy; brittle to UI tree changes.                   | Accessibility IDs first (Step 5). |
| Hard-coded device name (`'iPhone 15'`)                                | Test fails when sim doesn't exist.                                        | Use `genericDevice: true` or generated capabilities. |
| Ignoring `noReset` between tests                                       | App state leaks; flaky.                                                  | `noReset: false` (default) reinstalls per session. |
| One mega-test using `before` for the whole suite                      | Suite-long flake; one tiny issue restarts everything.                    | Per-test `beforeEach` reset; small focused tests. |
| Mixing Appium 1.x and 2.x docs                                        | Server URL / capability format differ; failures cryptic.                 | Pin Appium 2.x; use Appium 2.x docs only. |

## Limitations

- **External server.** Appium's HTTP-protocol design adds latency
  vs in-process frameworks (Espresso, XCUITest) - typical 100-300ms
  per command.
- **Per-driver feature gaps.** Some features are XCUITest-driver
  only or UiAutomator2-driver only; cross-platform tests must
  avoid them.
- **Device-farm cost.** Real devices on cloud farms charge
  per-minute; matrix runs add up.
- **Setup complexity.** Server + drivers + Android SDK + Xcode
  command-line tools = many dependencies. Containerize where
  possible.

## References

- [app][app] - Appium overview: WebDriver protocol, driver
  architecture, supported platforms (iOS, Android, Tizen, browser,
  desktop, TV), client libraries (JS / Python / Java / Ruby /
  .NET).
- `xcuitest-suite`,
  `espresso-suite` - per-platform
  native alternatives.
- `detox-testing`,
  `maestro-flows` - cross-platform
  alternatives with different trade-offs.
- `mobile-device-matrix-toolkit` - orchestrates Appium-driven matrix runs across simulators /
  emulators / farms.
