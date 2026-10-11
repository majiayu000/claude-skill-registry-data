---
name: anthill-shared-css-verify
description: "Use when editing AntHill's shared AntHill.App/wwwroot/app.css, the dashboard renders unstyled or with 0 CSS rules after an edit, or a CSS fix needs proof while the WPF client can't be screenshotted (locked workstation); also when resizing a .flow-svg diagram."
---

# Verifying AntHill shared CSS changes

`src/AntHill.App/wwwroot/app.css` is **one file served to two hosts**, so a rule change lands
in both. Scope deliberately.

- Web dashboard → `AntHill.Web/Components/App.razor`, fingerprinted via `@Assets[...]`
- WPF client → `AntHill.Client/wwwroot/index.html`, plain `_content/AntHill.App/app.css`

## Trap 1: `--no-build` serves a 0-byte stylesheet

After editing `app.css`, starting the dashboard with `dotnet run --no-build` can serve a
**stale fingerprinted asset with content-length 0 and 0 CSS rules** (e.g. `app.3typwxqhjs.css`).
The page renders near-unstyled and looks exactly like a CSS regression you just caused.

Always rebuild Web after touching `app.css`:

```bash
dotnet build src/AntHill.Web/AntHill.Web.csproj -c Debug --nologo
```

Confirm the sheet actually loaded before trusting any measurement:

```js
for (const s of document.styleSheets)
  if (s.href?.includes('AntHill.App/app')) console.log(s.cssRules.length); // expect ~800+, not 0
```

## Trap 2: build "failures" that are file locks

A running `AntHill.Web`, `AntHill.Client` or Visual Studio holds `AntHill.App.dll` /
`AntHill.Client.exe`. You get `MSB3026`/`MSB3027`/`MSB3021` and a non-zero exit **with no
`error CS` lines**. That is a lock, not a compile error, and not a test result: the suite never
ran. For reading build and test failure shapes in general, see `dotnet-test-verdict-capture`.

```bash
# distinguish
... 2>&1 | grep -E "error CS" || echo "no compile errors - lock only"
```

MSBuild names the holder and its PID. If you started it, stop it (`hub stop web`, or
`Stop-Process -Id <pid>`), build, then restart it. If it is the user's dashboard or Visual
Studio, do not kill it: state which suites were skipped and argue from the changed file set
(client-only changes cannot affect `AntHill.Web.Tests`).

## Verifying layout without a client screenshot

The WPF client can't be screenshotted while the workstation is locked (capture returns the lock
screen). The dashboard serves the *same stylesheet*, so verify rule mechanics there, and say
plainly that it proves computed rules, not the client's appearance.

Give the dashboard a throwaway database. It reads `ConnectionStrings:AssetLibrary` (unset, that
is the compose `db` on 5432) and migrates on startup:

```bash
docker run -d --name nb-pg -p 5437:5432 -e POSTGRES_USER=anthill \
  -e POSTGRES_PASSWORD=smoke -e POSTGRES_DB=anthill_nb postgres:18.3
# the dashboard process must inherit this: export it in the same call that starts
# the dashboard, or pass it in hub start's env={...}. Unset, it silently uses 5432.
export ConnectionStrings__AssetLibrary="Host=localhost;Port=5437;Database=anthill_nb;Username=anthill;Password=smoke"
```

Measure at the user's real window width (check it first; a maximized studio monitor is often
~2560 CSS px, not the screenshot's pixel size):

```js
const tab = await browser.open({ url: "http://localhost:5252/settings",
                                 viewport: { width: 2560, height: 1300 } });
await tab.evaluate(`(() => {
  const body = document.querySelector('.detail-body');
  return { maxWidth: getComputedStyle(body).maxWidth,
           actual: Math.round(body.getBoundingClientRect().width) };
})()`);
```

To see a state the dev dashboard cannot reach, **inject the component's markup** with its real
classes under the real stylesheet. The bell hides for `unattributed`, so a signed-out dev
dashboard never renders it:

```js
host.innerHTML = `<details class="bell-menu" open>...`;  // real classes, real stylesheet
await tab.screenshot({ path: "_diag/probe.png" });       // _diag/ is gitignored
```

Injection proves styling only. Pair it with a bUnit test for the component's own contract.
For row grids (a synthetic row, the live `getComputedStyle` pitfall), see
`anthill-row-grid-track-overflow`.

When done, stop the dashboard process as well as the container: a stray `AntHill.Web` left on
5252 breaks `AntHill.Client.Tests` (see `anthill-test-environment`).

## Diagrams are bounded on purpose

`.flow-svg` is capped (`max-width`) and centred. The figures are drawn in their own SVG units,
so stretching one across a wide panel scales every label with it (13px text arriving ~32px).
Nothing overlaps or clips, so no test sees it. To make a diagram feel tighter, **lower the cap**,
never remove it. A figure that needs a different size gets its own class and cap
(`.flow-svg-rail`), not a change to the shared class.

## Finish

Rebuild Client and Web, run both suites (`AntHill.Client.Tests`, `AntHill.Web.Tests`), and state
explicitly whether a real visual check happened or only computed-rule verification.
`AntHill.Layout.Tests` measures real layout (Playwright against a running dashboard). It needs
Docker, plus a one-time `tests/AntHill.Layout.Tests/bin/Debug/net10.0/playwright.ps1 install chromium`
after its first build.
