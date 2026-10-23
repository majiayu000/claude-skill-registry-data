---
name: winappdriver
description: "Authors and runs Windows UI tests against the WinAppDriver UIA surface via both invocation paths - the direct Microsoft W3C-WebDriver service (installing + launching `WinAppDriver.exe` on `127.0.0.1:4723`, `app` / `platformName` / `appArguments` / `appTopLevelWindow` capabilities) and the actively-maintained Appium 2.x wrapper (`appium driver install windows`, `appium:` prefixed capabilities, `windows:` gestures, PowerShell prerun/postrun hooks). Covers UWP / WPF / WinForms / Win32 apps, `AccessibilityId` / `Name` / `ClassName` locators, and Windows-runner CI. Use when driving a native Windows app from a Selenium-style client (C#, Java, Python, Ruby, JS) - directly when no Appium install is wanted, via Appium when the stack already runs Appium for iOS / Android / Mac2; for a C#-only FlaUI client use flaui-tests, and to choose among Windows desktop drivers first use desktop-test-strategy-reference."
metadata:
  keywords: "windows, winappdriver, uia, webdriver, wpf, uwp"
  version: "1.2.17"
---

# winappdriver

## Overview

Per the [WinAppDriver repository][wad]:

[wad]: https://github.com/microsoft/WinAppDriver

> "Windows Application Driver (WinAppDriver) is a service to support
> Selenium-like UI Test Automation on Windows Applications."

WinAppDriver exposes Microsoft UI Automation (UIA) - the Windows
accessibility tree described in
`desktop-test-strategy-reference` - behind a W3C-WebDriver-compatible HTTP endpoint. Per
[wad][wad], it supports four application classes on Windows 10:
"Universal Windows Platform (UWP)", "Windows Forms (WinForms)",
"Windows Presentation Foundation (WPF)", and "Classic Windows (Win32)
apps".

The same UIA surface has **two invocation paths**: talking to the
Microsoft-maintained `WinAppDriver.exe` service directly from a Selenium
client, or going through the Appium ecosystem's actively-maintained Node.js
proxy that sits in front of it and adds gestures, multi-window helpers, and
PowerShell hooks. This skill covers both - the direct path in the sections
below, the Appium path in "Invoking via Appium". Go direct when no Appium
(or Node.js) install is wanted on the test host; go via Appium when the
project already runs Appium for other platforms.

## When to use

- Native Windows desktop app under test - UWP, WPF, WinForms, or
  Win32 ([wad][wad]).
- Selenium-style client already in the project (C# `WindowsDriver<T>`,
  Java `WindowsDriver`, Python `webdriver-windows`).
- Tests must drive system-installed apps (Notepad, Calculator,
  Settings) - `app` capability accepts an executable path or UWP
  application family name ([wadauth][wadauth]).
- Direct-to-`WinAppDriver.exe` is required (no Appium installation
  permitted on the test host).

For Qt-on-Windows out-of-process tests, this is the recommended
driver per
`desktop-test-strategy-reference`;
the Qt application must publish a usable `QAccessible` tree.

## How to use

1. Install WinAppDriver and enable Developer Mode on a Windows 10/11 machine (Install + enable).
2. Launch `WinAppDriver.exe` on the default `127.0.0.1:4723` endpoint (Launch the service).
3. Declare `app` / `platformName` / `appArguments` / `appTopLevelWindow` capabilities for the app under test (Declare session capabilities).
4. Author a Selenium-style test that resolves an element by `AccessibilityId` (UIA `AutomationId`) and drives it end to end (Worked example). The full locator-strategy table, `Inspect.exe` discovery, and attach-to-running-window path live in [references/locators-and-ci.md](references/locators-and-ci.md).
5. Run on a Windows CI runner and parse TRX / JUnit results (feeds `junit-xml-analysis`) - full workflow in [references/locators-and-ci.md](references/locators-and-ci.md).

## Install + enable

Per [wad][wad]:

1. **Windows 10 machine** with the application under test installed.
2. **Enable Developer Mode** - Settings → Update & Security → For
   developers → Developer mode ([wad][wad]).
3. **Administrator privileges** are required to run on a custom
   IP / port ([wad][wad]); default `127.0.0.1:4723` runs as a normal
   user.

Download the latest WinAppDriver installer from the
[releases page][wad] (latest stable per [wad][wad]: v1.2.1, published
2020-11-05) and run it on the test machine. The installer drops
`WinAppDriver.exe` under `C:\Program Files (x86)\Windows Application
Driver\`.

## Launch the service

Per [wad][wad], launch on the default endpoint:

```cmd
:: Default - 127.0.0.1:4723
"C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"
```

The service prints `Press ENTER to exit.` and listens for incoming
W3C-WebDriver session requests. Custom IP / port / URL-prefix bindings
(which require an admin shell) are in
[references/locators-and-ci.md](references/locators-and-ci.md).

## Declare session capabilities

Per the [WinAppDriver authoring guide][wadauth]:

[wadauth]: https://github.com/microsoft/WinAppDriver/blob/master/Docs/AuthoringTestScripts.md

| Capability | Purpose |
|---|---|
| `app` | Application identifier (UWP family name) or full executable path ([wadauth][wadauth]) |
| `appArguments` | Launch arguments string ([wadauth][wadauth]) |
| `appWorkingDir` | Working directory for classic Win32 apps ([wadauth][wadauth]) |
| `appTopLevelWindow` | Hexadecimal handle of an existing window to attach to ([wadauth][wadauth]) |
| `platformName` | Target platform - set to `Windows` |
| `platformVersion` | Platform version string |

Per [wadauth][wadauth], the UWP Application Id appears in the
generated `AppX\vs.appxrecipe` file under the `RegisteredUserModeAppID`
node (example shape:
`c24c8163-548e-4b84-a466-530178fc0580_scyf5npe3hv32!App`).

## Worked example

Drive one element end to end - launch Notepad, locate its editor by
`AccessibilityId`, type into it, and close the session (C# client). The
canonical example from [wadauth][wadauth]:

```csharp
using System;
using OpenQA.Selenium.Appium.Windows;
using OpenQA.Selenium.Remote;

var capabilities = new AppiumOptions();
capabilities.AddAdditionalCapability("app", @"C:\Windows\System32\notepad.exe");
capabilities.AddAdditionalCapability("appArguments", @"MyTestFile.txt");
capabilities.AddAdditionalCapability("appWorkingDir", @"C:\MyTestFolder\");
capabilities.AddAdditionalCapability("platformName", "Windows");

var session = new WindowsDriver<WindowsElement>(
    new Uri("http://127.0.0.1:4723"),
    capabilities);

// Locate by AccessibilityId (the AutomationId attribute)
var editor = session.FindElementByAccessibilityId("15");
editor.SendKeys("Hello from WinAppDriver");

session.Quit();
```

The `AccessibilityId` locator maps to the UIA `AutomationId` property -
the stable locator per the
`desktop-test-strategy-reference`
locator table. The full method-to-attribute mapping and the other
locator strategies are in
[references/locators-and-ci.md](references/locators-and-ci.md).

## Invoking via Appium

Per the [appium-windows-driver repository][awd], "Appium Windows Driver is a
test automation tool for Windows devices and acts as a proxy to Microsoft's
WinAppDriver server." The Node.js driver itself is actively maintained while
the underlying service is described on the
[Appium ecosystem drivers page][appiumdrivers] as "has not been maintained
since 2022" - which is why the wrapper ships a built-in installer to pin a
known-good WinAppDriver version. Same UIA surface, same locator semantics;
what Appium adds: `windows:` gestures (`scroll` / `clickAndDrag` / `keys` /
`launchApp`), multi-window session switching, and `appium:prerun` /
`appium:postrun` PowerShell hooks.

[awd]: https://github.com/appium/appium-windows-driver

Install and launch ([awd][awd]):

```bash
npm install -g appium
appium driver install windows
appium driver run windows install-wad   # pins + installs WinAppDriver.exe
appium --port 4723
```

Session capabilities carry the `appium:` vendor prefix required by
Appium 2.x for non-W3C-standard caps ([awd][awd]):

```json
{
  "platformName": "windows",
  "appium:automationName": "windows",
  "appium:app": "C:\\Windows\\System32\\notepad.exe",
  "appium:appArguments": "MyTestFile.txt"
}
```

`platformName` and `appium:automationName` must both be `windows`
(case-insensitive); `appium:appTopLevelWindow` attaches to an existing
window by hex handle; `appium:prerun` / `appium:postrun` run short,
non-interactive PowerShell around the session ([awd][awd]). Python client:

```python
from appium import webdriver
from appium.options.windows import WindowsOptions
from selenium.webdriver.common.by import By

options = WindowsOptions()
options.platform_name = 'windows'
options.automation_name = 'windows'
options.app = r'C:\Windows\System32\notepad.exe'

driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
editor = driver.find_element(By.NAME, 'Text editor')
editor.send_keys('Hello from Appium Windows')
driver.quit()
```

Appium-path traps: omitting the `appium:` prefix (session rejected); legacy
`automationName: WinAppDriver` (use `windows`); hand-installing a random
WinAppDriver MSI instead of `install-wad` (version mismatch with the proxy);
hard-coding `appTopLevelWindow` (hex handle is per-launch); `windows: scroll`
with positive `deltaY` to scroll down (negative scrolls down). The gestures
API, multi-window flows, PowerShell hook recipes, and the Appium-path CI
workflow are in
[references/gestures-hooks-and-ci.md](references/gestures-hooks-and-ci.md).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Locating by `FindElementByName` for localised apps | Element name changes per language | Use `AccessibilityId` (UIA `AutomationId`) - stable across locales ([wadauth][wadauth]) |
| Hard-coded screen coordinates via `MouseAction` | DPI / window-state / multi-monitor break | Resolve element via accessibility tree; the driver computes hit-test centre |
| Running tests with Developer Mode disabled | Session creation fails with cryptic error | Enable Developer Mode (Install + enable) ([wad][wad]) |
| Custom IP / port without admin privileges | Service refuses to bind to non-default address | Run admin shell or stay on default `127.0.0.1:4723` ([wad][wad]) |
| One mega-session that drives multiple apps | UIA tree gets stale between app switches | One session per app; close + recreate on app change |
| Forgetting `session.Quit()` | Orphaned WinAppDriver child processes accumulate | `try/finally` around session lifecycle |
| Driving Edge / Chrome via WinAppDriver | Browser apps need a real WebDriver (Selenium / Playwright) | Use a browser driver, not WinAppDriver |
| Pixel-image matching for primary assertions | Brittle to font / theme / DPI changes | Accessibility tree first; image matching only for canvas-rendered content (per `desktop-test-strategy-reference`) |

## Limitations

- **WinAppDriver is community-described as unmaintained** since
  ~2022 (per the
  [Appium ecosystem driver page][appiumdrivers] which states the
  upstream "has not been maintained since 2022"). The latest
  official release per [wad][wad] is v1.2.1 (2020-11-05). For new
  projects on actively-maintained tooling, prefer the Appium 2.x
  invocation path above; NovaWindows is referenced on
  [appiumdrivers][appiumdrivers] as "a drop-in replacement for the
  partially unmaintained Windows driver" for new heavy use.

[appiumdrivers]: https://appium.io/docs/en/latest/ecosystem/drivers/

- **Windows-only.** The service runs only on Windows 10/11. No
  cross-OS test sharing without re-authoring against XCTest / AT-SPI.
- **No first-party Linux / macOS analogue.** Per the
  `desktop-test-strategy-reference`
  matrix, each OS has its own driver.
- **No headless mode.** UIA requires an interactive desktop session;
  CI on `windows-latest` works because GitHub-hosted runners are
  interactive, but Windows containers under Session 0 do not.
- **GPU / DirectComposition surfaces** (some WPF + WinUI 3 surfaces
  using DirectX-rendered controls) may not expose themselves to UIA - visible as opaque rectangles in Inspect.exe.
- **App must publish UIA.** Custom-painted Win32 windows that don't
  implement `IRawElementProviderSimple` are uncovered by
  WinAppDriver. Add UIA support or fall back to image matching for
  those specific surfaces.

## References

- WinAppDriver repository (README) - [wad][wad].
- WinAppDriver authoring guide - [wadauth][wadauth].
- Appium ecosystem drivers page (maintenance status note) -
  [appiumdrivers][appiumdrivers].
- appium-windows-driver README - [awd][awd].
- Deep reference (locator-strategy table, `Inspect.exe` discovery,
  custom service bindings, attach-to-running-window, CI wiring):
  [references/locators-and-ci.md](references/locators-and-ci.md).
- Deep reference (Appium `windows:` gestures, multi-window sessions,
  PowerShell hooks, Appium-path CI):
  [references/gestures-hooks-and-ci.md](references/gestures-hooks-and-ci.md).
- Strategic frame:
  `desktop-test-strategy-reference`.
