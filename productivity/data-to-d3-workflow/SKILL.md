---
name: data-to-d3-workflow
description: "Complete the data-to-d3 task using one archive-derived monolith with no auxiliary workflow artifact."
---

# data-to-d3 Faithful No-Persistence Monolith

## Monolith Translation Boundary

This monolith serializes the five archived A-stage responsibilities in
source order. It retains the archived task-route clauses, mutations, scope
limits, and scoped checks. The omitted source clauses are exclusively the
persistent carrier protocol: reading or writing an auxiliary file, emitting a
transition command, activating a different stage, and re-entering after
completion. Keep any transient planning only in the current context. Do not
create an auxiliary workflow file.

## Inlined Stage 1: `data-to-d3-entry-selector`

### Select the next task item

The following task-route clauses are copied from the archived entry stage. Choose the applicable next item from them, keep every action within its stated scope, and do not start another completion cycle after all requested outputs pass.

- Start with `output-data`: one standalone source assertion `/root/data/stock-descriptions.csv`; route `target=/root/output/data/`, `allowed scope=Authorize only /root/output/data/ so the copied stock descriptions file and all 50 stock-history CSV files are staged there under the required subdirectory structure.`, `mutation=Copy /root/data/stock-descriptions.csv into /root/output/data/stock-descriptions.csv and copy each manifest-listed /root/data/indiv-stock CSV file into /root/output/data/indiv-stock/ without renaming.`, and local `scoped check=Confirm /root/output/data/ contains the copied stock-descriptions file and all 50 copied stock-history CSV files under indiv-stock/.`.
- If verification of `output-data` fails or is blocked, repeat only `output-data`: one standalone source assertion `/root/data/stock-descriptions.csv`; route `target=/root/output/data/`, `allowed scope=Authorize only /root/output/data/ so the copied stock descriptions file and all 50 stock-history CSV files are staged there under the required subdirectory structure.`, `mutation=Copy /root/data/stock-descriptions.csv into /root/output/data/stock-descriptions.csv and copy each manifest-listed /root/data/indiv-stock CSV file into /root/output/data/indiv-stock/ without renaming.`, and local `scoped check=Confirm /root/output/data/ contains the copied stock-descriptions file and all 50 copied stock-history CSV files under indiv-stock/.`.
- After `output-data` passes, continue with `d3-bundle`: one standalone predecessor assertion `/root/output/data/stock-descriptions.csv`; route `target=/root/output/js/d3.v6.min.js`, `allowed scope=Authorize only /root/output/js/d3.v6.min.js as the offline D3.js v6 runtime required by the stock web app.`, `mutation=Write a local vendored D3.js v6 bundle to /root/output/js/d3.v6.min.js so the page can load D3 force, scale, selection, and CSV APIs offline.`, and local `scoped check=Confirm /root/output/js/d3.v6.min.js is a substantial local D3 v6 bundle with the APIs needed by the stock app.`.
- If verification of `d3-bundle` fails or is blocked, repeat only `d3-bundle`: one standalone source assertion `/root/data/stock-descriptions.csv`; route `target=/root/output/js/d3.v6.min.js`, `allowed scope=Authorize only /root/output/js/d3.v6.min.js as the offline D3.js v6 runtime required by the stock web app.`, `mutation=Write a local vendored D3.js v6 bundle to /root/output/js/d3.v6.min.js so the page can load D3 force, scale, selection, and CSV APIs offline.`, and local `scoped check=Confirm /root/output/js/d3.v6.min.js is a substantial local D3 v6 bundle with the APIs needed by the stock app.`.
- After `d3-bundle` passes, continue with `style-sheet`: one standalone predecessor assertion `/root/output/js/d3.v6.min.js`; route `target=/root/output/css/style.css`, `allowed scope=Authorize only /root/output/css/style.css for the horizontal chart-and-table layout, legend, tooltip, and selection styling.`, `mutation=Write the stylesheet for a side-by-side bubble-chart and table layout, including legend styling, ticker readability, tooltip presentation, and highlighted row or bubble states.`, and local `scoped check=Confirm /root/output/css/style.css defines the side-by-side layout, legend, tooltip, and selected-state styles for the stock dashboard.`.
- If verification of `style-sheet` fails or is blocked, repeat only `style-sheet`: one standalone source assertion `/root/data/stock-descriptions.csv`; route `target=/root/output/css/style.css`, `allowed scope=Authorize only /root/output/css/style.css for the horizontal chart-and-table layout, legend, tooltip, and selection styling.`, `mutation=Write the stylesheet for a side-by-side bubble-chart and table layout, including legend styling, ticker readability, tooltip presentation, and highlighted row or bubble states.`, and local `scoped check=Confirm /root/output/css/style.css defines the side-by-side layout, legend, tooltip, and selected-state styles for the stock dashboard.`.
- After `style-sheet` passes, continue with `visualization-js`: one standalone predecessor assertion `/root/output/css/style.css`; route `target=/root/output/js/visualization.js`, `allowed scope=Authorize only /root/output/js/visualization.js for the D3 bubble chart, sector legend, tooltip behavior, and linked table interactions.`, `mutation=Write the D3 v6 script that loads the copied stock data, builds one clustered bubble chart by sector, sizes nodes by market cap with uniform ETF sizing, labels each node by ticker, suppresses ETF tooltips, renders the stock table, and links bubble and row selection.`, and local `scoped check=Confirm /root/output/js/visualization.js contains the clustered-bubble, ETF guard, tooltip, legend, and linked table-selection logic for the copied stock data.`.
- If verification of `visualization-js` fails or is blocked, repeat only `visualization-js`: one standalone source assertion `/root/data/stock-descriptions.csv`; route `target=/root/output/js/visualization.js`, `allowed scope=Authorize only /root/output/js/visualization.js for the D3 bubble chart, sector legend, tooltip behavior, and linked table interactions.`, `mutation=Write the D3 v6 script that loads the copied stock data, builds one clustered bubble chart by sector, sizes nodes by market cap with uniform ETF sizing, labels each node by ticker, suppresses ETF tooltips, renders the stock table, and links bubble and row selection.`, and local `scoped check=Confirm /root/output/js/visualization.js contains the clustered-bubble, ETF guard, tooltip, legend, and linked table-selection logic for the copied stock data.`.
- After `visualization-js` passes, continue with `index-page`: one standalone predecessor assertion `/root/output/js/visualization.js`; route `target=/root/output/index.html`, `allowed scope=Authorize only /root/output/index.html as the single-page shell that wires the copied data, local D3 bundle, stylesheet, and visualization script together.`, `mutation=Write /root/output/index.html with the side-by-side application shell, the bubble-chart and stock-table containers, the tooltip container, and the local asset references to css/style.css, js/d3.v6.min.js, and js/visualization.js.`, and local `scoped check=Confirm /root/output/index.html loads the local assets and exposes the side-by-side chart, table, and tooltip shell for the stock dashboard.`.
- If verification of `index-page` fails or is blocked, repeat only `index-page`: one standalone source assertion `/root/data/stock-descriptions.csv`; route `target=/root/output/index.html`, `allowed scope=Authorize only /root/output/index.html as the single-page shell that wires the copied data, local D3 bundle, stylesheet, and visualization script together.`, `mutation=Write /root/output/index.html with the side-by-side application shell, the bubble-chart and stock-table containers, the tooltip container, and the local asset references to css/style.css, js/d3.v6.min.js, and js/visualization.js.`, and local `scoped check=Confirm /root/output/index.html loads the local assets and exposes the side-by-side chart, table, and tooltip shell for the stock dashboard.`.

---

## Inlined Stage 2: `data-to-d3-scope-binder`

### Preserve the selected task route

Carry forward only the selected item's target, permitted paths, required action, and scoped check. Do not broaden to another task item or reconstruct a different route.

---

## Inlined Stage 3: `data-to-d3-authorized-continuation`

### Perform the selected task action

Perform exactly the selected route's required action at its stated target. Create or revise only that target and do not broaden to another task item, another output, a global check, or an unrelated helper.

---

## Inlined Stage 4: `data-to-d3-scope-verifier`

### Verify the selected task action

Run exactly the selected route's scoped check against its stated target. Use the result only to decide whether this same item needs repair or the next incomplete task item may be selected; do not broaden verification to other outputs.

---

## Inlined Stage 5: `data-to-d3-catalog-return-gate`

### Decide the next task step

If the scoped check passes, select the next incomplete task item. If it fails or is blocked, return only to that item for repair. Once all user-requested deliverables are complete and appropriately verified, finish normally; do not begin an additional revalidation cycle.

## Completion

Complete any remaining task-native validation and report the task result
truthfully. Do not create auxiliary workflow artifacts or perform a
post-completion re-entry.
