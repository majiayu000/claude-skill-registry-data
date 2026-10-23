---
name: postman-collections
description: "Repairs Postman and Newman runs in CI - a reporter that never writes the HTML file the pipeline expects, a nightly job that fires requests as fast as it can until a partner API rate-limits it, or a report with one row per request when the collection asserts a dozen things between them. Authors Postman collections (requests, tests, variables, environments), runs them headless via the Newman CLI, configures reporters (cli / json / junit / html) for CI artifact upload, and drives data-driven runs from JSON / CSV iteration files. Use when HTTP API tests are authored in Postman and need to run, pace themselves, and report correctly in CI."
---

# postman-collections

## Overview

**Newman** is Postman's official CLI for running collections headlessly in CI
([newman-readme][readme]). The shape is two-step: author the collection in the
Postman app (or import an OpenAPI spec), save it as `collection.json`, then run
`newman run collection.json` in CI and emit JUnit / JSON for gating.

[readme]: https://github.com/postmanlabs/newman

This skill covers the headless Newman side. GUI authoring inside Postman is out
of scope; its reference is [learning.postman.com](https://learning.postman.com/).

## When to use

- The repo contains `*.postman_collection.json` (or the team
  exports collections to `collections/`).
- API testing is the team's primary integration-testing layer and
  the team is already in the Postman ecosystem.
- A CI workflow needs `newman run` with structured reporter output
  for PR gating.

If the team uses TypeScript / JavaScript and prefers code-first
authoring, evaluate
`tavern-testing` (YAML) or
`karate-testing` (Karate DSL) before
adopting Postman/Newman - those keep tests next to source code rather
than in a separate JSON artifact.

## Install

```bash
npm install -g newman
```

(Per [newman-readme][readme].)

For per-project install (preferred for CI determinism):

```bash
npm install --save-dev newman
```

For the HTML reporter (external, separate install):

```bash
npm install --save-dev newman-reporter-htmlextra
```

## Running

The canonical invocation ([newman-readme][readme]):

```bash
newman run <collection-file-source> [options]
```

`<collection-file-source>` can be:

- A local file path: `./collections/orders.postman_collection.json`.
- A Postman Cloud URL: `https://api.getpostman.com/collections/...`.
- A public-link URL exported from Postman.

### Key flags

The flags you reach for first: `-e/--environment`, `-r/--reporters`
(`cli,json,junit,html`), `--reporter-junit-export <path>`, `--bail
[folder|failure]`, and `--timeout-request <ms>`. The full flag table (per
[newman-readme][readme]) is in
[references/newman-reference.md](references/newman-reference.md).

### Worked example

```bash
newman run examples/sample-collection.json \
  -e environment.json \
  -d data.csv \
  -r cli,json,junit \
  --timeout-request 5000 \
  --reporter-junit-export results.xml \
  --reporter-json-export results.json \
  --bail folder
```

(Adapted from [newman-readme][readme].)

## Reporters

The four built-in / canonical reporters per [newman-readme][readme]:

| Reporter | Purpose                                                          |
|----------|------------------------------------------------------------------|
| `cli`    | Terminal output; enabled by default.                              |
| `json`   | Full JSON summary of every request and assertion result.          |
| `junit`  | JUnit XML - consumable by GitHub Actions, GitLab, Jenkins.        |
| `html`   | Static HTML report; requires `newman-reporter-htmlextra`.         |

**JUnit is the canonical CI choice** - every major CI platform
ingests JUnit XML, surfaces test counts on the run summary, and lets
the team click through to per-assertion failures.

For richer per-test details (which assertion in which folder failed
with which response), pair `junit` with `json` and upload both as
build artifacts.

## Authoring tests inside the collection

Tests live in each request's **Tests** tab and run in a sandboxed JS
environment with `pm.*` globals:

```javascript
pm.test('status is 200', () => {
  pm.response.to.have.status(200);
});

pm.test('body is JSON with .order_id', () => {
  const json = pm.response.json();
  pm.expect(json).to.have.property('order_id').that.is.a('number');
});

pm.test('saves order_id for next request', () => {
  pm.collectionVariables.set('order_id', pm.response.json().order_id);
});
```

Each `pm.test('...', () => {})` call becomes one entry in the JUnit
XML / JSON output - name them clearly so the CI run summary is
readable.

## CI integration

A GitHub Actions workflow that runs `newman`, exports JUnit + JSON, uploads
both as artifacts, and surfaces results in the run summary - with `if: always()`
on the upload and reporter steps so the reports survive a failing collection -
is in [references/newman-reference.md](references/newman-reference.md).

## Anti-patterns

The common Newman anti-patterns and their fixes - hard-coded URLs and tokens in
the collection JSON, running against production, cascading shared-state
`pm.test` blocks, one giant 200-request collection, and missing `--bail` - are
tabulated in [references/newman-reference.md](references/newman-reference.md).

## Limitations

- **No code-first authoring.** Postman's authoring story is the GUI;
  the JSON file is the artifact. Teams that prefer code-first DSLs
  should evaluate `karate-testing` or
  `tavern-testing`.
- **Sandboxed JS only.** Tests can't import npm packages - the `pm.*`
  sandbox provides chai / lodash / cheerio pre-loaded; for richer
  logic, consider Karate or Tavern.
- **No native parallelism inside one Newman run.** Parallelize across
  CI matrix jobs, not within a single Newman process.

## References

- [newman-readme][readme] - install, `newman run` syntax, flags,
  reporters, example invocation.
- `tavern-testing` - YAML alternative.
- `karate-testing` - DSL alternative.
- `schemathesis-fuzzing` - 
  property-based fuzzing as a complement (not replacement) for
  example-based collections.
