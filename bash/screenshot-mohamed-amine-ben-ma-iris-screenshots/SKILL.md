---
name: screenshot
description: Capture screenshots of live websites with the iris CLI — full page, single CSS element, desktop/iPhone/iPad presets, dark mode, concurrent batch, JSON output. Use when the user asks to screenshot or capture a website or local dev server, visually verify a rendered page, check responsive or dark-mode rendering, or needs a visual reference for a task.
license: MIT
compatibility: Requires iris + a Chrome-family browser (Chrome, Chromium, Edge, Brave). Both auto-installed by scripts/install.sh (network needed; Linux may need sudo for system libs).
allowed-tools:
  - Bash(bash scripts/doctor.sh)
  - Bash(bash scripts/install.sh)
  - Bash(iris:*)
  - Read
---

# Screenshot — website camera powered by iris

`iris` renders a page in a real Chrome via the DevTools Protocol, waits for
fonts, images, entrance animations (and lazy-loaded content on `--full`), then
captures a trustworthy image at retina `@2x` by default. It is a camera, not a
driver: it captures, it does not click, type, or script-scroll.

## Preflight (once per session, before the first capture)

Paths like `scripts/` and `references/` below are relative to THIS skill's
directory — run them from there, or prefix them with the skill's absolute path.

```bash
bash scripts/doctor.sh
```

- Exits 0 and prints the resolved Chrome path only when a smoke capture succeeded.
- If anything is missing, run `bash scripts/install.sh` and re-run doctor.
- If `$CHROME` is not set in your environment, add `--chrome <path printed by doctor>`
  to iris invocations (or export CHROME for the session).
- If `iris` is not on your PATH, use the absolute path doctor printed.

## Choosing a command

| Goal | Command |
|---|---|
| Desktop shot (1440×900 @2x) | `iris <url>` |
| Full page height | `iris --full <url>` |
| Full page, dark mode | `iris --full --dark <url>` |
| One element (first CSS match, auto-scroll, tight framing) | `iris --selector '#hero' --padding 24 <url>` |
| iPhone (390×844 @3x, mobile UA) | `iris -s iphone <url>` |
| iPad (1024×1366 @2x) | `iris -s ipad <url>` |
| Custom viewport | `iris -s 1280x800 <url>` |
| Local dev server | `iris http://localhost:3000 -o shots/home.png` (bare localhost uses HTTP automatically) |
| Wait for an element before capturing | `iris --wait-for 'h1' <url>` |
| Concurrent batch | `iris -o shots/ a.com b.com c.com` or `cat urls.txt \| iris - -o shots/` |
| Machine-readable results | add `--json` (one JSON object per capture on stdout) |

## Conventions

- Save captures to `shots/` in the working directory unless the user specifies a path.
- Single URL → `-o file.png`; multiple URLs → `-o dir/` (filenames derive from the URL, collisions get `-2`, `-3` suffixes).
- Use `--json` for batches and verify each result; exit code 1 if any URL failed.
- Pages taller than ~16k px at @2x fall back to @1x automatically — check the JSON `scale` field and mention it if it happens.
- Formats: `png` (default), `jpg`, `webp` — picked by the `-o` extension or `--format`.

## Limitations (do not fight these)

- `--selector` captures the FIRST matching element in document order only. It conflicts with `--full`; `--padding` requires `--selector`.
- Cross-origin iframe content is not captured.
- No interaction (clicks, typing, scripted scroll). For interactive checks, use a browser automation tool instead.

## References (read only when needed)

- `references/flags.md` — complete flag reference, presets, JSON schema, tuning tips.
- `references/mcp-setup.md` — register `iris mcp` so the agent gets a `capture` tool (stdio MCP server built into the same binary).
- `references/troubleshooting.md` — failure modes and fixes (missing browser, headless libs, timeouts, batch failures, MCP tool not appearing).

## MCP (optional)

If the user wants iris available as an agent tool rather than just a CLI, read
`references/mcp-setup.md` and register the server
(`command: iris, args: ["mcp"]`).
