---
name: tg-miniapp-ui
description: "Use when building or debugging the interface of a Telegram Mini App: theme colors and dark mode, safe areas and notches, fullscreen, keyboard and viewport height, MainButton and SecondaryButton, BackButton, haptic feedback, performance on weak Android, or a layout bug that shows up only on a real iPhone, Android or Desktop client."
license: MIT
---

# tg-miniapp-ui

Checked against the official docs on 2026-10-30: Bot API 10.3 (latest, August 24, 2026), Mini Apps page, `telegram-web-app.js?64`.

## Not verified live

No client or device was used to write this skill. API facts come from the docs; bug reports come from public trackers. Acceptance on a real iPhone and Android device is still ahead: run the [check](#device-check) below. A browser emulator doesn't catch these bugs.

Client bugs with platform, client, issue number and date: [`client-pitfalls.md`](client-pitfalls.md). Read it before you blame your own CSS.

## Startup

Put `telegram-web-app.js` in `<head>` before other scripts. Call `Telegram.WebApp.ready()` as soon as the essential interface is loaded: it hides the loading placeholder. `expand()` asks for the maximum height; `isExpanded` reports it.

## Theme

Color everything from the theme and repaint on change. There is no separate dark mode API: `colorScheme` is `light` or `dark`, and the palette follows it.

```css
body {
  background: var(--tg-theme-bg-color);
  color: var(--tg-theme-text-color);
}
.hint { color: var(--tg-theme-hint-color); }
.card { background: var(--tg-theme-section-bg-color, var(--tg-theme-secondary-bg-color)); }
```

- `themeParams` fields map to `--tg-theme-*` variables, and every field is optional. Give each a fallback. Fields by version: `secondary_bg_color` 6.1; header, accent, section, subtitle and destructive colors 7.0; `section_separator_color` 7.6; `bottom_bar_bg_color` 7.10.
- Listen to `themeChanged` for logic that reads colors in JS; the CSS variables update on their own.
- `setHeaderColor`, `setBackgroundColor` and `setBottomBarColor` take `#RRGGBB` or keywords. Prefer `setHeaderColor('bg_color')`: a hex header produces light glass buttons on iOS, see [pitfalls](client-pitfalls.md).

## Viewport and keyboard

- `viewportHeight` / `--tg-viewport-height` changes during gestures and animations, and its refresh rate is too low to follow the bottom edge.
- `viewportStableHeight` / `--tg-viewport-stable-height` updates after the app settles. Pin bottom elements to this one.
- `viewportChanged` passes `isStateStable`; run layout work when it is `true`.
- `hideKeyboard()` (9.1) closes the on-screen keyboard.

## Safe areas

Two sets of insets, and fullscreen needs both:

| Set | Covers | CSS variables |
|---|---|---|
| `safeAreaInset` | Notches and system navigation | `--tg-safe-area-inset-{top,bottom,left,right}` |
| `contentSafeAreaInset` | Telegram's own controls | `--tg-content-safe-area-inset-{top,bottom,left,right}` |

```css
.screen {
  padding-top: calc(var(--tg-safe-area-inset-top, 0px) + var(--tg-content-safe-area-inset-top, 0px));
  padding-bottom: var(--tg-safe-area-inset-bottom, 0px);
}
```

Read JS values in `safeAreaChanged` and `contentSafeAreaChanged` handlers. These events and `fullscreenChanged` arrive separately, so inset values read inside `fullscreenChanged` can be stale ([tma.js #704](https://github.com/Telegram-Mini-Apps/tma.js/issues/704), maintainer reply, 2025-04-03).

## Fullscreen

`requestFullscreen()` (8.0) reports through `fullscreenChanged`, and failure through `fullscreenFailed` with `UNSUPPORTED` or `ALREADY_FULLSCREEN`. No list of supporting clients is published, and a practitioner report describes iOS 12.9 sending neither event. So handle the events and also check `isFullscreen` on a timer. The timeout below is a choice, not a documented value.

```js
function enterFullscreen(onResult) {
  const app = Telegram.WebApp;
  if (!app.isVersionAtLeast('8.0')) return onResult(false, 'OLD_CLIENT');

  let timer;
  const finish = (ok, reason) => {
    clearTimeout(timer);
    app.offEvent('fullscreenChanged', changed);
    app.offEvent('fullscreenFailed', failed);
    onResult(ok, reason);
  };
  const changed = () => finish(app.isFullscreen, 'CHANGED');
  const failed = ({ error }) => finish(error === 'ALREADY_FULLSCREEN', error);

  app.onEvent('fullscreenChanged', changed);
  app.onEvent('fullscreenFailed', failed);
  timer = setTimeout(() => finish(app.isFullscreen, 'NO_EVENT'), 1500);
  app.requestFullscreen();
}
```

Design the layout to work without fullscreen. Set `setHeaderColor` even in fullscreen, where the header is transparent: the color picks a contrasting status bar and controls. `lockOrientation()` keeps the current orientation (8.0).

## Bottom buttons

Use `MainButton` and `SecondaryButton` instead of drawing your own bottom bar.

```js
const { MainButton, SecondaryButton } = Telegram.WebApp;
MainButton.setParams({ text: 'Pay', is_visible: true, has_shine_effect: true });
SecondaryButton.setParams({ text: 'Cancel', is_visible: true, position: 'left' });

MainButton.onClick(async () => {
  MainButton.showProgress();          // disabled while running; showProgress(true) leaves it active
  try { await submit(); } finally { MainButton.hideProgress(); }
});
```

- `SecondaryButton` exists since 7.10. `position` is `left` (default), `right`, `top` or `bottom`, and applies only when both buttons are visible.
- `setParams` also takes `color`, `text_color`, `is_active`, and `icon_custom_emoji_id` (9.5).
- `onClick` adds a handler, so a re-render adds another. Remove the old one with `offClick`.
- From the attachment menu the main button stays hidden until the user interacts with the app.

`BackButton` lives in the header: `show()`, `hide()`, `onClick()`. Wire it to your router, and hide it on the root screen.

## Gestures and closing

- `disableVerticalSwipes()` (7.7) only when swipes conflict with your own gestures; the docs recommend keeping them on. Users can still close by swiping the header.
- `enableClosingConfirmation()` (6.2) when closing would lose user input.

## Haptics

`HapticFeedback` (6.1):

| Moment | Call |
|---|---|
| Tap or collision | `impactOccurred('light' \| 'medium' \| 'heavy' \| 'rigid' \| 'soft')` |
| Action result | `notificationOccurred('success' \| 'error' \| 'warning')` |
| Selection moved to another item | `selectionChanged()`; skip it when the user makes or confirms a choice |

## Performance

The docs ask for smooth animation, ideally 60 fps. On Android the User-Agent ends with a performance class; cut animations and effects on `LOW`. iOS has no equivalent.

```js
const match = navigator.userAgent.match(/Telegram-Android\/.*;\s*(LOW|AVERAGE|HIGH)\)/);
const isLowEnd = match?.[1] === 'LOW';
```

## Official design rules

Responsive and mobile-first; interactive elements that mimic native ones; labels on all inputs and images; theme colors tracked live; safe area and content safe area respected. The page gives no spacing numbers or components.

## Device check

Run on a real iPhone and a real Android phone, light and dark theme. The check is done when every line has passed on both.

1. Open from each launch path you ship; the first screen has no blank area and no overlap with Telegram controls.
2. Switch the system theme while the app is open; all colors follow.
3. Enter fullscreen, go to another screen and back, check the top of the page.
4. Focus every text field; the field stays visible and taps still work after the keyboard closes.
5. Press every bottom button; progress shows, and the button recovers after a failure.
6. Android low-end device: animations are cut.

## Sources

- Mini Apps: https://core.telegram.org/bots/webapps · design guidelines https://core.telegram.org/bots/webapps#design-guidelines · events https://core.telegram.org/bots/webapps#events-available-for-mini-apps
- `telegram-web-app.js`: https://telegram.org/js/telegram-web-app.js?64
