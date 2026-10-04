---
name: direct-verify
description: Verify an existing Direct composition, including strict activation, deterministic settlement, semantic scenario behavior, coverage truthfulness, cleanup, and exclusion from production output. Use when asked to test, audit, validate, review, or report the proof boundary of a Direct workbench or frontend verification run.
---

# Direct verification

## Discover the declared contract

1. Read applicable `AGENTS.md` files, package scripts, Direct definition, world parser, deterministic adapters, session construction, browser installation, verifier, and production-boundary policy.
2. If a Direct page is running, read and parse
   `window.__direct.manifest` first. Use it to list every scenario and coverage
   entry, then compare it with the authored definition when source is
   available.
3. Map each `fixture`, `mixed`, and `direct` claim to the evidence required to close it.
4. Identify the production adapter, service, host, operating system, or device behavior replaced by each deterministic port.
5. Inspect each command before treating it as evidence. A script named `verify` may build and scan boundaries without driving a browser.

Do not infer a stronger proof mode from a passing screenshot or fixture interaction.

## Run deterministic checks

Run the repository's narrow Direct typecheck, unit tests, property tests, and Direct build when those commands exist. Report a missing property suite or browser verifier as `not present`; do not synthesize evidence. Prefer an existing isolated verifier or temporary output directory so builds do not dirty the source tree.

Verify that tests cover malformed worlds, explicit activation failures, adapter failures, cancellation, cleanup, and exact-script drain behavior when applicable.

When a browser verifier exists, drive stable scenario URLs and interact in
product terms. Read only the canonical `window.__direct` bridge. Parse the
complete manifest and every probe; bind `manifest.coverage` to the authored
definition with `parseDefinitionCoverageSnapshot`. Do not accept compatibility
or product-specific globals as equivalent evidence.

The manifest is driver-neutral. With agent-browser, read one synchronous
bridge sample:

```sh
agent-browser --json eval "(() => { const bridge = window.__direct; return { bridgeSchema: bridge?.schema, manifest: bridge?.manifest, probe: typeof bridge?.snapshot === 'function' ? bridge.snapshot() : undefined }; })()"
```

The JSON command envelope stores that sample at `data.result`; parse the
result, not the envelope, as the Direct contract. With Playwright MCP, call
`browser_evaluate` with the same page function:

```json
{
  "function": "() => { const bridge = window.__direct; return { bridgeSchema: bridge?.schema, manifest: bridge?.manifest, probe: typeof bridge?.snapshot === 'function' ? bridge.snapshot() : undefined }; }"
}
```

No Direct-specific browser plugin or MCP server is required. Add
`manifest.queries.scenario` to the product's known Direct entry URL, navigate,
and reacquire the complete sample because navigation replaces the document.
The published scenario `route` is the product route under review, not
necessarily the wrapper workbench's entry path.

After every scenario navigation, require:

- `bridgeSchema` equals `direct.browser-bridge/v2`;
- `manifest.active.source` equals the requested activation source;
- `manifest.active.scenario` equals the requested scenario;
- `manifest.active.route` equals the expected product route; and
- the parsed manifest's `active.selectionHash` binds that public selection to
  its activation hash; and
- the parsed probe activation hash equals
  `manifest.active.activationHash`.

Retain the complete initial manifest and probe with each result. After product
interactions, atomically sample the bridge again and require unchanged public
catalog metadata, coverage, catalog hash, full active selection, and probe
activation identity. Bind every sampled `manifest.coverage` to the authored
definition.

## Join the probe

Wait until the same generation, revision, activity totals, and pending counters
remain quiet for the verifier's bounded settle interval. A quiet probe requires
zero current activity and zero pending counters. One successful
`wait --fn "window.__direct?.snapshot().isQuiescent === true"` observes only a
single quiet sample; it does not prove stability. Parse another probe after the
settle interval and compare the complete quiet state.

After each interaction:

1. Join quiescence again.
2. Reject relevant nonzero violation counters.
3. Reject page errors, unexpected console errors, unmapped or failed network calls, malformed transport values, leaked activity, and required script steps left unused.
4. Assert the route, visible semantics, accessibility state, and product result required by the scenario.

Never replace the probe join with a fixed sleep. Treat remaining work as a diagnostic unless the declared claim requires it to drain.

Definition activation, parser tests, and adapter unit tests do not close a claim about the real rendered interface. Such a claim requires the declared semantic and accessibility assertions against that interface.

## Verify production exclusion

Build the real production graph independently. Run its emitted-boundary scanner across every declared production surface. Require at least one executable bundle and reject package names, wire schemas, reserved query keys, fixtures, workbench strings, and browser bridge globals.

When a bundler selects platform variants, require a paired source map for every executable and every production platform. Positively match the declared shared behavior, native composition, and production-adapter modules in each map; reject Direct and web-fixture paths. Verify the inverse selection for the fixture graph. A clean marker scan proves only absence of those markers in those files, and a clean unrelated bundle proves nothing. Source selection still does not prove native linkage, service behavior, runtime loading, or device behavior.

## Classify the evidence

Report every coverage entry as one of:

- `verified` when every fixture scenario and direct gate required by the claim's declared mode ran through the named behavior and passed its claim-specific assertions;
- `fixture-verified` when every declared fixture scenario for a mixed claim passed while its direct half remains open;
- `partial` when some required evidence passed;
- `not-exercised` when the run produced no evidence for the claim; or
- `direct-required` when deterministic evidence cannot close the claim.

A browser-only run keeps a direct claim `direct-required` and can report at most `fixture-verified` for a mixed claim. A wider run may report a mixed or direct claim as `verified` after every named direct behavior is exercised. Note supporting unit or structural evidence separately when it does not close the direct gate.

Use `classifyCoverageEvidence` from `@hraness/direct/testing`. Pass only scenario IDs whose claim-specific assertions succeeded, and set direct evidence to verified only for a current passing direct gate. Do not hand-roll a looser status promotion.

Include `HEAD` plus dirty or clean working-tree status, commands, scenario
results, catalog hash, activation hashes, final probes, production surfaces
scanned, retained artifacts, and exact failures. Treat the catalog hash as a
drift fingerprint, not a security digest or deployed-bundle identity. Report
absent property tests, browser probes, or artifacts as `not present` or `not
observed`. State skipped direct gates once. Do not use credentials, contact
live services, or expand into device testing unless the user placed those
systems in scope.
