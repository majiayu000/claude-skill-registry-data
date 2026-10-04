---
name: node-frontend
description: The vanilla-JS single-page frontend served from public/ by a Node Web Only backend - HTML structure, the Tailwind browser build, self-hosted fonts, the Catppuccin Mocha theme, and the reconnecting WebSocket client. Use when building or changing that page, laying out public/, theming it, choosing which surface a panel or control sits on, or wiring realtime updates. Triggers on public/index.html, public/js/, public/css/, public/vendor/, @font-face, @theme, crust, new WebSocket, reconnect backoff, and Catppuccin. Not for React, Vue, or Svelte, and not for a bundler-driven build.
user-invocable: false
---

# Node Frontend

**One `index.html` under `public/`, styled with the Tailwind browser build and the Catppuccin Mocha palette, plain ES modules, self-hosted fonts, and a WebSocket client that reconnects on its own.**

This is the Go embedded frontend with a different server in front of it. The palette, the layering, the fonts, and the styling rules are the same; only the paths and the realtime client differ.

The backend serves this tree at the site root: `public/index.html` at `/`, `public/css/inter.css` at `/css/inter.css`, `public/fonts/*.woff2` at `/fonts/*.woff2`.

## Layout

```
public/
├── index.html
├── css/
│   ├── inter.css               # @font-face for Inter
│   ├── google-sans.css         # @font-face for Google Sans
│   └── jetbrains-mono.css      # @font-face for JetBrains Mono
├── js/
│   ├── app.js                  # application logic
│   └── ws.js                   # reconnecting WebSocket client
├── fonts/                      # woff2 only
├── icons/
│   └── favicon.png
└── vendor/                     # third-party JS and CSS copied out of node_modules
    ├── tailwind.js             # @tailwindcss/browser
    └── lucide.min.js           # Lucide icons
```

Nothing under `css/`, `fonts/`, or `vendor/` is committed. A Makefile target produces them and the release workflow calls the same target, so the tree in git holds only what a person wrote and a downloaded asset never lands in a diff nobody reviews.

## Rules

No framework and no mandatory bundler. Plain ES modules via `<script type="module">`, the DOM API, `fetch`, and `WebSocket`. A build step exists only for the binary release path and is never required to develop or run the page, which keeps the page a file you can open rather than a target you have to compile.

One `index.html`. Views are shown and hidden client-side, and a second page is added only when something genuinely needs its own URL.

Shared logic lives in `js/app.js` and the socket client in `js/ws.js`. Splitting the transport out means a page that does not need realtime simply does not import it.

Styling is Tailwind utility classes on the element, compiled in the browser by the vendored `@tailwindcss/browser` build. Hand-written CSS is the exception and earns its place only in a case that has no utility form:

- `@font-face` declarations, which live in the downloaded stylesheets under `css/`
- scrollbar pseudo-elements, `::selection`, and other pseudo-elements Tailwind does not reach
- a subtree a third party generates, where the classes are not yours to write, such as rendered Markdown, a Mermaid diagram, or an editor widget
- `@media print` rules
- `@keyframes`

Everything else is a class. A hand-written rule that duplicates a utility is a second place a color or a spacing value can drift, and it is invisible to anyone reading the element.

What remains goes in an inline `<style>` block, never split across the page and a second file. Scattering the same rules across two places is how a color ends up defined twice with different values.

Every form control renders at 16px on a coarse pointer, through `pointer-coarse:text-[16px]` alongside whatever size the design uses. iOS Safari zooms the viewport in when a focused control computes under 16px, and it does not zoom back out on blur.

`text-base` cannot carry it, because the palette defines `--color-base` and Tailwind compiles `text-base` to `color: var(--color-base)` with no font size.

The viewport meta stays `width=device-width, initial-scale=1.0`, since `user-scalable=no` and `maximum-scale=1` suppress the zoom only by taking pinch zoom away from everyone.

The three `@font-face` stylesheets always stay as separate linked files under `css/`, since the asset step regenerates that directory wholesale.

## Fonts

| Font | Role | `font-family` | Source |
|---|---|---|---|
| Inter | body and UI text | `'Inter'` | Google Fonts |
| Google Sans | display headings and branding | `'Google Sans'` | Google Fonts |
| JetBrains Mono | code and monospace | `'JetBrains Mono'` | Google Fonts |

All three are downloaded whether or not a given page uses all three, so the asset step is identical across projects and a later design change needs no build change.

Fonts are woff2, never ttf. woff2 is roughly half the bytes for the same glyphs, and every browser targeted here supports it. All three come from Google Fonts, which already serves woff2, so nothing is converted.

The mono slot takes the plain family by default. The Nerd Font variant is a patched build Google Fonts does not carry, so it is downloaded from the nerd-fonts release as ttf and compressed to woff2, which costs two megabytes and roughly ten seconds against sixty kilobytes and half a second. A page earns that only by actually rendering Nerd Font glyphs, which means a Powerline separator, a file-type icon from the private use area, or terminal output that carries them. An icon that Lucide already has is not a reason.

Switching is a Makefile variable, not a page change. The nerd target writes the same `css/jetbrains-mono.css` under the same `JetBrains Mono` family name, so the HTML is identical either way.

Everything is self-hosted and served from the app's own origin. No runtime CDN, no Google Fonts fetch, no external `<script src>`. A page that fetches a font from a third party leaks every visitor's address and stops rendering correctly offline.

```css
/* public/css/inter.css */
@font-face {
    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-display: swap;
    src: url('/fonts/inter-400.woff2') format('woff2');
}

@font-face {
    font-family: 'Inter';
    font-style: normal;
    font-weight: 600;
    font-display: swap;
    src: url('/fonts/inter-600.woff2') format('woff2');
}
```

`public/css/google-sans.css` and `public/css/jetbrains-mono.css` follow the same shape for the weights the design uses.

`font-display: swap` renders text in a fallback face immediately and swaps when the woff2 arrives, so a slow font never leaves the page blank.

## Layering

The page is grounded on `crust`, the darkest step, and every surface is raised from there. Grounding on `base` instead pushes the whole page one rung up the ramp, leaves the chrome darker than the page it sits on, and costs contrast against every text color.

| Role | Token |
|---|---|
| Page ground, and any chrome flush with it such as a sidebar, header, or rail | `crust` |
| A surface that reads as lifted off the page, such as a card, modal, popover, or dropdown | `mantle` |
| A control sitting on either of those, such as an input, chip, button, or hovered row | `surface0` |
| Borders, dividers, and the hover state of a `surface0` control | `surface1` |
| A well recessed inside a `mantle` panel, such as a code block or an embedded preview | `base` |

Adjacent layers step one rung and no more. `crust` to `mantle` is a contrast ratio of 1.07 and `crust` to `surface0` is 1.49, which separates them without drawing a seam. Skipping a rung reads as two unrelated panels rather than one raised off the other.

Text runs the same way. Body copy takes `subtext0`, headings and the one value a row exists to show take `text`, and metadata takes `overlay1`. Defaulting body copy to `text` makes every word shout and leaves nothing louder for a heading to be.

Structure never borrows from the accent ramp. Borders, dividers, and backgrounds come from the neutral steps, and an accent marks one thing per view: the active item, the primary action, or a state. Two accents competing in one view means neither is signal.

Nothing here names a component. The tokens are assigned by what a surface does, so a layout this skill has never seen still lands on the right step.

## The Page

Catppuccin Mocha is the default for a new frontend in this style, declared once as `--ctp-*` variables on `:root` and mapped into Tailwind's `@theme` so every utility resolves through them. A project that already has a palette keeps it, since re-theming a working app is a design decision rather than a convention. Hardcoding a hex value in a component style is what makes a palette change a search-and-replace.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APP_NAME</title>

    <link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon.png">

    <link rel="stylesheet" href="/css/inter.css">
    <link rel="stylesheet" href="/css/google-sans.css">
    <link rel="stylesheet" href="/css/jetbrains-mono.css">

    <script src="/vendor/lucide.min.js"></script>
    <script src="/vendor/tailwind.js"></script>
    <style>
      /* Catppuccin Mocha */
      :root {
        --ctp-rosewater: #f5e0dc; --ctp-flamingo: #f2cdcd; --ctp-pink: #f5c2e7;
        --ctp-mauve: #cba6f7;     --ctp-red: #f38ba8;      --ctp-maroon: #eba0ac;
        --ctp-peach: #fab387;     --ctp-yellow: #f9e2af;   --ctp-green: #a6e3a1;
        --ctp-teal: #94e2d5;      --ctp-sky: #89dceb;      --ctp-sapphire: #74c7ec;
        --ctp-blue: #89b4fa;      --ctp-lavender: #b4befe; --ctp-text: #cdd6f4;
        --ctp-subtext1: #bac2de;  --ctp-subtext0: #a6adc8; --ctp-overlay2: #9399b2;
        --ctp-overlay1: #7f849c;  --ctp-overlay0: #6c7086; --ctp-surface2: #585b70;
        --ctp-surface1: #45475a;  --ctp-surface0: #313244; --ctp-base: #1e1e2e;
        --ctp-mantle: #181825;    --ctp-crust: #11111b;
      }
    </style>
    <style type="text/tailwindcss">
      @theme {
        --color-rosewater: var(--ctp-rosewater); --color-flamingo: var(--ctp-flamingo);
        --color-pink: var(--ctp-pink);           --color-mauve: var(--ctp-mauve);
        --color-red: var(--ctp-red);             --color-maroon: var(--ctp-maroon);
        --color-peach: var(--ctp-peach);         --color-yellow: var(--ctp-yellow);
        --color-green: var(--ctp-green);         --color-teal: var(--ctp-teal);
        --color-sky: var(--ctp-sky);             --color-sapphire: var(--ctp-sapphire);
        --color-blue: var(--ctp-blue);           --color-lavender: var(--ctp-lavender);
        --color-text: var(--ctp-text);           --color-subtext1: var(--ctp-subtext1);
        --color-subtext0: var(--ctp-subtext0);   --color-overlay2: var(--ctp-overlay2);
        --color-overlay1: var(--ctp-overlay1);   --color-overlay0: var(--ctp-overlay0);
        --color-surface2: var(--ctp-surface2);   --color-surface1: var(--ctp-surface1);
        --color-surface0: var(--ctp-surface0);   --color-base: var(--ctp-base);
        --color-mantle: var(--ctp-mantle);       --color-crust: var(--ctp-crust);

        --font-sans: 'Inter', system-ui, sans-serif;
        --font-display: 'Google Sans', 'Inter', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
      }
    </style>
</head>
<body class="bg-crust text-subtext0 min-h-screen font-sans">
    <header class="flex items-center justify-between px-4 py-3 bg-crust border-b border-surface0">
        <span class="font-display font-semibold text-text">APP_NAME</span>
        <span id="status" class="text-sm text-overlay1">connecting...</span>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-8">
        <h1 class="font-display text-2xl font-bold mb-6 text-text">APP_NAME</h1>
        <div id="app" class="bg-mantle border border-surface0 rounded-xl p-6"></div>
    </main>

    <script type="module" src="/js/app.js"></script>
    <script>lucide.createIcons();</script>
</body>
</html>
```

`@theme` maps each name onto a `--ctp-*` variable rather than a literal hex. The utility resolves the variable at paint time, so redefining the `--ctp-*` set under a selector re-themes the page without a second `@theme` and without touching a single class.

`@import "tailwindcss";` is omitted, because the browser build injects it when no `@import` appears anywhere in the block. Writing one takes over the whole import graph and drops the base styles unless you add it back yourself.

The browser build compiles utility classes in the page at run time. Tailwind documents it as development-only. It is fine for a self-hosted tool or a dashboard, and an app that needs a small payload and no runtime compile moves to a build step emitting a static stylesheet.

## WebSocket Client

The client opens a socket, reconnects with backoff on close, dispatches messages by a `type` field, and queues sends until the socket is open. Queueing rather than throwing means `app.js` can call `send` during startup without waiting for the connection.

Messages are JSON objects with a `type` string; the rest of the object is that type's payload. The server end of the same protocol lives in the backend's `ws.js`.

```javascript
// public/js/ws.js
export function connect(path, options = {}) {
    const { onStatus = () => {}, baseDelay = 500, maxDelay = 15000 } = options;
    const handlers = new Map();
    const queue = [];

    let socket = null;
    let attempts = 0;
    let closed = false;

    function url() {
        const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
        return `${proto}//${location.host}${path}`;
    }

    function backoff() {
        const capped = Math.min(baseDelay * 2 ** attempts, maxDelay);
        return capped / 2 + Math.random() * (capped / 2);
    }

    function open() {
        socket = new WebSocket(url());

        socket.addEventListener('open', () => {
            attempts = 0;
            onStatus(true);
            while (queue.length) socket.send(queue.shift());
        });

        socket.addEventListener('message', (event) => {
            let msg;
            try {
                msg = JSON.parse(event.data);
            } catch {
                return;
            }
            const fns = handlers.get(msg.type);
            if (fns) for (const fn of fns) fn(msg);
        });

        socket.addEventListener('close', () => {
            onStatus(false);
            if (closed) return;
            const delay = backoff();
            attempts += 1;
            setTimeout(open, delay);
        });

        socket.addEventListener('error', () => socket.close());
    }

    open();

    return {
        on(type, handler) {
            const fns = handlers.get(type) ?? [];
            fns.push(handler);
            handlers.set(type, fns);
            return this;
        },
        send(type, payload = {}) {
            const data = JSON.stringify({ type, ...payload });
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.send(data);
            } else {
                queue.push(data);
            }
        },
        close() {
            closed = true;
            if (socket) socket.close();
        },
    };
}
```

The delay is half the capped value plus a random half, so a server restart does not bring every client back in the same millisecond.

`attempts` resets on a successful open, which keeps a long-lived connection from inheriting the backoff of an outage hours earlier.

The `closed` flag distinguishes a deliberate `close()` from a dropped connection, so an intentional teardown does not immediately reconnect.

An `error` event is followed by `close`, so the handler only calls `socket.close()` and lets the close path own the reconnect. Reconnecting from both would open two sockets.

```javascript
// public/js/app.js
import { connect } from '/js/ws.js';

const statusEl = document.getElementById('status');
const appEl = document.getElementById('app');

const socket = connect('/ws', {
    onStatus(online) {
        statusEl.textContent = online ? 'online' : 'reconnecting...';
        statusEl.className = online ? 'text-sm text-green' : 'text-sm text-red';
    },
});

socket.on('update', (msg) => {
    appEl.textContent = JSON.stringify(msg.payload, null, 2);
});

socket.send('subscribe', { channel: 'events' });
```
