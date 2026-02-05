---
name: dev-browser-nix
description: Use dev-browser for browser automation on NixOS. Invoke when user asks to test UI, automate browser interactions, take screenshots, or verify web app behavior.
---

# Dev-Browser on NixOS

This skill wraps the dev-browser plugin with NixOS-specific setup.

## Prerequisites

The project flake.nix must include:
```nix
packages = with pkgs; [
  nodejs_22
  playwright-driver.browsers
];

shellHook = ''
  export PLAYWRIGHT_BROWSERS_PATH=${pkgs.playwright-driver.browsers}
  export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
'';
```

## Chromium Version Symlink

Playwright in dev-browser may expect a different chromium version than nixpkgs provides. Create a symlink:

```bash
mkdir -p ~/.cache/playwright-nix/chromium-1200
ln -sf /nix/store/*/playwright-browsers/chromium-*/chrome-linux ~/.cache/playwright-nix/chromium-1200/chrome-linux64
```

Then use `PLAYWRIGHT_BROWSERS_PATH=~/.cache/playwright-nix` when starting the server.

## Starting the Server

```bash
eval "$(direnv export bash)" && \
cd ~/.claude/plugins/cache/dev-browser-marketplace/dev-browser/*/skills/dev-browser && \
PLAYWRIGHT_BROWSERS_PATH=~/.cache/playwright-nix HEADLESS=false \
npx tsx scripts/start-server.ts &
```

Wait for "Ready" message before running scripts.

## Running Scripts

Always run from the dev-browser skills directory with direnv loaded:

```bash
eval "$(direnv export bash)" && \
cd ~/.claude/plugins/cache/dev-browser-marketplace/dev-browser/*/skills/dev-browser && \
npx tsx <<'EOF'
import { connect, waitForPageLoad } from "@/client.js";

const client = await connect();
const page = await client.page("mypage");

// Your automation here
await page.goto("http://localhost:5173");
await waitForPageLoad(page);
await page.screenshot({ path: "tmp/screenshot.png" });

await client.disconnect();
EOF
```

## Common Patterns

### Handling Results Overlay
Sessions in etude end quickly and show a results overlay that blocks clicks:
```typescript
// Dismiss overlay before interacting
await page.evaluate(() => {
  document.querySelectorAll('[class*="overlay"]').forEach(el => el.remove());
});
```

### Capturing Console Logs
```typescript
const logs = [];
page.on('console', msg => {
  if (msg.text().includes('DEBUG')) logs.push(msg.text());
});
```

### Checking Element Colors (for note coloring verification)
```typescript
const colors = await page.evaluate(() => {
  const notes = document.querySelectorAll('.note use');
  return Array.from(notes).map(use => ({
    id: use.closest('.note')?.id,
    fill: getComputedStyle(use).fill
  }));
});
```

### Starting Fresh
When state is polluted, navigate from home:
```typescript
await page.goto('http://localhost:5173/');
await waitForPageLoad(page);
await page.click('text=C Major Scale');
await page.waitForTimeout(2000);
```

## Troubleshooting

### "npx: command not found"
Ensure nodejs is in flake and direnv is loaded:
```bash
eval "$(direnv export bash)"
which npx  # Should show nix store path
```

### "chromium-XXXX not found"
Create symlink from available version to expected version in ~/.cache/playwright-nix/

### Overlay blocking clicks
The error `<div class="_overlay_...">…</div> intercepts pointer events` means a modal is open. Dismiss it with Escape or remove via evaluate.

### HMR not updating code
Restart vite dev server:
```bash
pkill -f vite
cd packages/client && bun run dev &
```

### Session ends too quickly
The playhead runs fast on short pieces. For testing note coloring, capture console logs to verify the coloring code runs, rather than relying on visual screenshots.
