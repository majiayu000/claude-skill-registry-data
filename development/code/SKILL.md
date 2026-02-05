---
name: code
description: ALWAYS follow this style when writing Python / JavaScript code
---

- Prefer libraries to writing code. Prefer popular, modern, minimal, fast libraries
- Write readable code. Keep happy path linear and obvious. Write flow first, then fill in code. Name intuitively
- Keep code short
  - Data over code: Structures beat conditionals. Prefer config.{json|yaml|toml|...} if >= 30 lines
  - DRY: Helpers for repeated logic, precompute shared intermediates
  - Early returns fail fast and reduce nesting. Skip defensive fallbacks, existence checks, ... unless essential
  - YAGNI: Skip unused imports, variables, and code
- Change existing code minimally. Retain existing comments. Follow existing style
- Use type hints and docstrings (document contracts and surprises, not mechanics)
- Don't comment readable code. If commenting, only comment non-obvious stuff that'll trip future maintainers: why, why not alternatives, pitfalls, invariants, input/output shape, ...
- When tests exists, or writing new code, add tests first. Keep tests fast
- Replace PII in committed code, tests, docs with similar REALISTIC dummy data
- Show status & progress for long tasks (>5s)
- Make re-runs efficient for long tasks (>1min). Restarting should resume. Log state, cache & flush data and LLM/API/HTTP requests, etc.
- Read latest docs for fast moving packages: GitHub README, `npm view package-name readme`, https://context7.com/$ORG/$REPO/llms.txt, ...

## Python

Prefer `uv run`, `uvx` over `python` or `python3`

Unless `pyproject.toml` is present, add dependencies to script:

```py
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["scipy>=1.10", "httpx"]
# ///
```

Preferred libs:

- `typer` / `click` not `argparse`
- `httpx` not `requests`
- `lxml` not `xml`
- `pandas` not `csv`
- `orjson` over `json` if speed/datetime matters
- `tenacity` for retries
- `pytest`
- `python-dotenv`

Use one of these for exception tracebacks with locals:

```python
from rich.traceback import install; install(show_locals=True)
from loguru import logger; logger.add(sink=lambda m: print(m, end=""), diagnose=True, backtrace=True)
```

## HTML

Prefer modern HTML:

- Loading: loading="lazy", fetchpriority="low", <link rel="preload" as="image">
- Forms: inputmode=, enterkeyhint=, autocomplete=, list=, autocapitalize=, spellcheck=, form=
- UI: popover, popovertarget=, formmethod="dialog", inert, <details name=""> for accordions, <dialog>, <meter>, <progress>, <track>, <data>
- Media: picture srcset=, video preload=, crossorigin=, playsinline=, muted=, autoplay=, loop=, controls=, poster=

Prefer SVG favicons e.g.

```html
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg%20xmlns ... %3C%2Fsvg%3E"/>
```

designed with Unicode and rich typography, e.g.:

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="128">
  <rect fill="#2563eb" width="64" height="64" rx="10"/>
  <text x="32" y="35" text-anchor="middle" dominant-baseline="middle" font-size="40">🌈</text>
</svg>
```

## JavaScript

Preferred JS style:

- Bootstrap. Minimize custom CSS. Prefer declarative data-* patterns
- Hyphenated HTML class/ID names (id="user-id" not id="userId")
- Use modern browser APIs and ESM2022+: Use `?.`, `??`, destructuring, spread, implicit returns (`=>` over `=> { return }`)
- Avoid TypeScript, but enable `// @ts-check`. `.d.ts` is OK for packages
- Loading indicator while awaiting fetch()
- Error handling only at top level. Render errors for user
- Helpers: `const $ = (s, el = document) => el.querySelector(s); $('#id')...`
- Prefer lit-html > .insertAdjacentHTML / .innerHTML >> .createElement + setting attributes
- Prefer vitest + jsdom for unit tests, Playwright for end-to-end tests
- Import maps: `<script type="importmap">{ "imports": { "package-name": "https://cdn.jsdelivr.net/npm/package-name@version" } }</script>`

Preferred libs:

```js
import * as d3 from "d3"; // @7/+esm for visualizations
import hljs from "highlight.js"; // @11/+esm highlight Markdown code; link CDN CSS
import { html, render } from "lit-html"; // @3/+esm for DOM updates
import { unsafeHTML } from "lit-html/directives/unsafe-html.js";
import { marked } from "marked"; // @17/+esm
import { parse } from "partial-json"; // @0.1/+esm parse streamed JSON. `const { x } = parse('{"x":"incomplete')`

import { asyncLLM } from "asyncllm"; // @2 streams LLM responses. `for await (const { content, error } of asyncLLM(baseURL, { method: "POST", body: JSON.stringify({...}), headers: { Authorization: `Bearer ${apiKey}` } }))`
import { bootstrapAlert } from "bootstrap-alert"; // @1 for notifications. `bootstrapAlert({ title: "Success", body: "Toast message", color: "success" })`
import { geminiConfig, openaiConfig } from "bootstrap-llm-provider"; // @1 LLM provider modal. `const { baseUrl, apiKey, models } = await openaiConfig()`
import saveform from "saveform"; // @1 to persist form data. `saveform("#form-to-persist")`
```

Debug front-end apps with Playwright (prefer CDP on localhost:9222) using .evaluate(); view screenshot images, console logs.

## Tmux

Use tmux outside the sandbox for interactive REPLs/TUIs, long running commands: servers, services, sub-agents: codex/claude/...

```bash
tmux new-session -d -s $SESSION 'uv run --with pandas,httpx,lxml python -iqu'
tmux pipe-pane -t $SESSION -o "cat >> /tmp/$LOG"
tmux send-keys -t $SESSION 'print(1 + 2)' C-m
cat /tmp/$LOG
tmux capture-pane -p -t $SESSION -S -5
```
