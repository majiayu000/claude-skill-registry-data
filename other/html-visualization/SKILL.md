---
name: html-visualization
description: Build, revise, and evaluate browser-rendered HTML visualizations for concepts, systems, codebases, architectures, workflows, timelines, comparisons, and other relationship-heavy explanations. Use to create or improve an HTML/CSS/JS diagram, process map, interactive explainer, or visual documentation, validating the rendered result with Playwright CLI screenshots.
---

# HTML Visualizations

Build the visualization in code, render it in a real browser, and judge it from screenshots. Prefer pedagogical clarity over marketing polish.

## Plan

- Name the audience and the main questions the visualization must answer. That answer is your stop rule.
- Inspect the source material or code first so the diagram reflects the real implementation.
- Pick the simplest structure that fits the relationships. Identify the content model before adding visual detail.
- Use HTML/CSS for layout; reach for SVG or canvas only when connectors, geometry, or density demand it. Add interaction only when the core explanation can't stand without it.

## Build and render

Prefer a standalone HTML file. Before choosing a browser, inspect the installed
CLI because accepted browser values and installed channels can drift:

```bash
playwright-cli open --help
playwright-cli install-browser --help
```

Start from a value listed by the installed `open --help` (at the pinned review
point: `chrome`, `firefox`, `webkit`, and `msedge`), but treat the error
message as the final authority — a listed value can still fail when its browser
channel is not installed, and an unlisted alias can work (observed: `chromium`
was absent from the help yet accepted, mapping to `chrome-for-testing`, while
`chrome` failed wanting the system Chrome channel). If `open` reports a missing
browser, install the exact bundle named by the error (for example,
`playwright-cli install-browser chrome-for-testing`) and retry with the value
that named it.

Serve the HTML over HTTP because the browser daemon blocks `file://` URLs. Run
this as one shell block so the variables and cleanup trap remain active, after
setting `browser` to the accepted value you selected:

```bash
set -e
viz_dir=/abs/dir/containing/viz
browser=SELECTED_BROWSER
shot_dir="$(mktemp -d -t html-viz-XXXXXX)"
port="$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()')"
python3 -m http.server "$port" --bind 127.0.0.1 --directory "$viz_dir" >/dev/null 2>&1 &
server_pid=$!
trap 'kill "$server_pid" 2>/dev/null' EXIT
url="http://127.0.0.1:$port/viz.html"

curl --retry 5 --retry-connrefused -fsS "$url" -o /dev/null
playwright-cli -s=html-viz open --browser="$browser" "$url"
playwright-cli -s=html-viz resize 1440 900
playwright-cli -s=html-viz screenshot --filename="$shot_dir/viz.png"
echo "$shot_dir/viz.png"
```

View the printed screenshot path. Re-run the block after changes, using the same viewport for comparison.

- Do not assume `chromium` is an accepted alias; use the installed help and
  install guidance as the source of truth.
- Use the named session on every command so concurrent browser sessions cannot interfere.
- Check `playwright-cli console` after load and interactions; a missing `/favicon.ico` is expected noise.
- Use `playwright-cli snapshot` when diagnosing layout or DOM structure.

## Critique and iterate

Check accuracy, reading path, clipping or overlap, legibility, scrolling, contrast, and color-independent meaning. Fix the largest defect and re-screenshot. Stop when the visualization answers the target question with no meaningful defect.

When done, close the browser session and remove the printed screenshot directory. Then report the HTML location, what you verified, and any known limitations.
