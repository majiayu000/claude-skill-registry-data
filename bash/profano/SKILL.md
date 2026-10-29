---
name: profano
repo: remorses/profano
description: >
  CLI tool to analyze V8 .cpuprofile files and Chrome Performance traces and
  print top functions by self-time or total-time in the terminal. ALWAYS load
  this skill when CPU profiling JavaScript or TypeScript programs (Node, Vitest,
  Bun, Chrome DevTools exports, Cloudflare Workers startup or request CPU).
  It shows how to generate .cpuprofile files and how to inspect them from the
  terminal without opening Chrome DevTools.
---

# profano

`profano` reads V8 `.cpuprofile` files and Chrome Performance traces (`Trace-*.json`) and prints the heaviest functions as a table sorted by self-time or total (inclusive) time.

Every time you use profano, you MUST fetch the latest README and read it in full:

```bash
curl -s https://raw.githubusercontent.com/remorses/profano/main/README.md  # NEVER pipe to head/tail, read in full
```

The README covers generating `.cpuprofile` files (Node, Vitest, Bun, **Cloudflare Workers** startup and request, Chrome Performance traces, browser pages via playwriter, React component profiling), all CLI options, and how to read the output columns.

Chrome Performance **Save profile** writes a trace JSON. Pass it to `profano Trace.json` directly. Do not convert it first.

## Cloudflare Workers

A Worker needs **two** profiles. Startup is `wrangler check startup`. A request is `wrangler dev --inspector-port 9230` plus `profano workers request <url>`. `wrangler tail` `cpuTime` is only a total. Never paste a one-off CDP script; use the CLI command.

Do **not** copy `dist/` to a temp folder unless `wrangler check startup` errors about two wrangler configs with different base paths. That copy is an exception, not the default.

Trust the **function mix** in a local profile. Do not treat local milliseconds as Cloudflare CPU.
