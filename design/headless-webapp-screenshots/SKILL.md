---
name: headless-webapp-screenshots
description: Capture clean, deterministic screenshots of a JavaScript web app without installing a browser automation framework. Use when needing product screenshots of an SPA for a README, portfolio, or design review, especially when the app shows onboarding modals, seedable demo data, animations, or needs mobile and desktop viewports. Not for native or mobile apps, video capture, or installing a browser automation framework.
version: 1.0.0
---

# Headless Webapp Screenshots

Plain `chrome --headless --screenshot` fails on real apps: onboarding modals block the view, empty states look broken, and entry animations freeze the capture mid-fade. This skill captures final-state screenshots using only the Chrome/Edge already installed on the machine.

## Method

1. **Build a local harness page** next to the app (copy `assets/shot-harness-template.html`). It loads the app's real CSS/JS but first runs an inline script that seeds `localStorage` with demo state: `onboarded: true`, realistic records, logs. Seeding must run *before* the app's scripts, so the app boots straight into the target state with no modal.
2. **Add a `shot=1` query param** in the harness that injects CSS killing all animations and transitions. Without this, headless captures freeze fade-ins at partial opacity.
3. **Add view/theme params** (`?view=stats&theme=dark`) that call the app's own view-switch API after boot, so every screen is reachable without clicking.
4. **Capture** with `scripts/capture.ps1` (Windows) or the equivalent command:

```
chrome --headless=new --disable-gpu --hide-scrollbars \
  --user-data-dir=<temp dir> --virtual-time-budget=8000 \
  --window-size=1440,900 --screenshot=out.png "file:///.../harness.html?shot=1&view=today"
```

- `--virtual-time-budget` fast-forwards timers and async work before the capture; raise it when the view triggers async flows (e.g. mock API calls) that must finish first.
- Mobile shots: `--window-size=390,844 --force-device-scale-factor=2` for retina-crisp output.
- Always open the produced PNG and check it before using it.

## Pitfalls

- Semi-transparent, washed-out captures mean animations were frozen mid-run: the `shot=1` style is missing or injected too late. Inject it in `<head>` before other stylesheets.
- An empty or modal-covered capture means the seed did not land: confirm the storage key matches exactly what the app reads, and that the seed script runs before app init.
- `file://` pages share one localStorage origin in Chrome; give each capture run its own `--user-data-dir` to avoid state leaking between shots.
- Keep the harness out of the deployed site and out of the public repo if it contains demo data.

## Before / After

Before, a plain capture of a real SPA looks broken:

```
chrome --headless --screenshot=shot.png --window-size=1440,900 http://localhost:5173
# 结果：新手引导弹窗挡住整个界面，列表是空的，入场动画卡在半透明
```

After, the harness boots the app straight into its final state:

```
chrome --headless=new --disable-gpu --hide-scrollbars \
  --user-data-dir=<temp dir> --virtual-time-budget=8000 \
  --window-size=1440,900 --screenshot=stats.png \
  "file:///.../harness.html?shot=1&view=stats&theme=dark"
# 结果：演示数据已注入、动画被禁用、直接进入目标视图
```

Same machine, same Chrome, no Puppeteer and no Playwright installed.
