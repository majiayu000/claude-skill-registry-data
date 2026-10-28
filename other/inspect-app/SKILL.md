---
name: inspect-app
description: Visually check a running app with the Playwright MCP - a local production build or a deployed Vercel preview. Use to verify an app renders, to debug layout or runtime problems, or to review a preview after deploy.
---

# inspect-app

Input: a URL, or an `appName` to run locally. The browser is limited to localhost and
`*.vercel.app`.

1. **Local:** build the app into the fixed preview folder (inside the sandbox):
   `npm run build -w @lab/<kebab-name> -- --outDir ../../.preview --emptyOutDir`.
   Then start the static server as a background command, exactly this text (no `cd`, redirects,
   variables or changes to it):
   `npx serve -s .preview -l tcp://127.0.0.1:5173 -c ../tools/serve.json --no-compression --no-clipboard`
   and check that it is up by opening `http://127.0.0.1:5173` with the Playwright MCP. Do not
   check with `curl` or similar: every sandboxed command has its own loopback, so it never sees
   the server. It must match the user's `excludedCommands` entry exactly; started any other way
   (for example wrapped in `nohup` or `&`) it stays inside the sandbox, where the browser cannot
   reach it. It serves only the built files, so a rebuild into `.preview` is needed to see changes.
   **Deployed:** use the preview URL.
2. Open the page with the Playwright MCP, take a snapshot and a screenshot, and check:
    - it renders real content (not a blank page) and the core interaction works;
    - the console has no errors or warnings that matter, and no failed network requests;
    - the layout holds at a phone width (about 390px) and at desktop width.
      A blocked navigation (for example to another origin) replaces the page with Chrome's error
      page, so navigate back to the app before taking further snapshots or screenshots. Do not pass
      a `filename` to screenshots: bare names land in the repo root. The default output directory
      `.playwright-mcp/` is gitignored.
3. Look at the screenshot yourself and judge basic layout and legibility. Visual taste is the
   user's call; report what you saw, not that it is "good".
4. Stop the server when done (stop the background task, then check with the Playwright MCP that
   `http://127.0.0.1:5173` no longer answers, because `npx` can leave its child process running). Report findings and fix what is yours to fix.
