---
name: uri-path-validation-normalization
description: Use when code decides whether a request URI or a configured file path is allowed — extension allow-lists, directory allow-lists, edge/CDN request handlers, service workers, or a gate that asserts a specific file is covered. Triggers on percent-encoded input (`%2E`, `%2F`), dot segments, and any `endsWith`/`includes` check standing in for an identity test.
---

# URI and Path Validation Normalization

## Profile keys consumed

- `architecture.source_root`

The exact-path rules below apply to files under `architecture.source_root`
and to the repository's own gate manifests. This skill introduces no build or
test command of its own; anything it asks you to re-run goes through the
profile's `make` target map, skipping with a recorded note when a key maps to
`null`.

## Overview

Validate the form the downstream consumer will act on, not the form that arrived. An allow-list
applied to an encoded URI, or an identity test written as a suffix match, passes exactly the input
it was meant to stop.

## When to use

- Writing or reviewing a request handler that maps a URI onto an object key or a file path.
- Building an extension, directory, or filename allow-list.
- A gate that must confirm a configured value points at one specific repository file.
- Reviewing a security finding about encoding bypass or path traversal.
- Not for: routing inside the application, where the router owns the path.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate
  CI target): partial — no edge handler; the exact-path rule applies to gates that pin a file, such
  as the entries in `config/gate-thresholds.manifest.json` and the spec paths in
  `tests/e2e/route-coverage.tsv`.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — the CDN routing
  script, the CDN security-headers script, and `public/sw.js` are the edge layer, and a production
  guardrail gate pins the Jest coverage entry for them by exact path.
- **Component-library shape** (Storybook-first, no bootable app, published package): no — it ships
  a component library, with no request handler or edge layer.

## Core pattern

An extension check that reads the encoded URI sees `js` in `/images/%2Eenv.js` and admits it; the
origin then percent-decodes the path to derive the object key and serves `/images/.env.js`. `%2F` is
worse: it moves where the last segment even begins, so `/images/a%2F.env.js` resolves to
`images/a/.env.js`.

There are two correct answers, and which one applies depends on whether decoding can fail safely.

- **Decode, then validate** — when a decode failure can be routed to a rejection. Malformed input
  (`%zz`) makes the decoder throw, so the throw must land on the deny path, never on
  catch-and-continue.
- **Reject the encoded family outright** — when a throw inside the handler is caught by an outer
  frame that fails **open**, decoding is not safe to attempt. Refuse any URI containing `%`, and
  prove separately that no shipped asset name needs one.

```js
// Reject before the allow-list tables ever see the URI: a dot segment satisfies
// the directory and extension tests while resolving somewhere else entirely,
// a percent escape hides the leading dot from the dotfile check, and a backslash
// is a segment separator to the normalizers downstream but not to split('/').
function isUnsafeUri(uri) {
  if (uri.indexOf('%') !== -1 || uri.indexOf('\\') !== -1) {
    return true;
  }
  var parts = uri.split(/[/\\]/);
  for (var i = 0; i < parts.length; i++) {
    if (parts[i] === '.' || parts[i] === '..') {
      return true;
    }
  }
  return false;
}
```

Splitting on `/` alone is the same defect as reading the encoded URI: `/images/..\..\secret` has no
dot segment at a slash boundary and no `%`, so it passes a slash-only gate, and a proxy, IIS origin
or CDN handler that treats `\` as a separator then resolves it upward. Split on both separators and
refuse the backslash outright — no shipped asset name needs one, so the two together leave no
spelling of the traversal that reaches the allow-list tables.

The extension reader itself must also treat a dotfile as extensionless: with `lastDot <= 0` covering
"no dot at all" and a leading-dot test covering every dotfile, `/images/.env.js` never reports `js`.

## Identity, not resemblance

A check that a configured path names one specific file is an equality test against the exact
accepted spellings — the repository-relative path and its root-prefixed form. A suffix or substring
test admits a traversal (`../../other/scripts/handler.js`), a negation that excludes the file from
collection (`!<rootDir>/scripts/handler.js`), and a longer sibling (`handler.js.map`).

Compare the extracted string values. Building a pattern out of a path and escaping only the dot
leaves every other metacharacter — the backslash above all — unescaped, which is the incomplete
escaping defect static analysis flags.

## Common mistakes

- Validating the encoded URI and letting the origin decode it — decode first, or refuse escapes.
- Catching a decoder throw and continuing — the malformed input then bypasses the check entirely.
- `endsWith` or `includes` where identity is meant — compare for equality against each accepted
  spelling.
- Forgetting that a dotfile can carry a second dot — the leading-dot test, not the last one,
  decides.
- Assuming no dot segments arrive because the router normalises them — an edge handler is given the
  raw URI.
- Splitting on `/` only, so a backslash-separated traversal has no segment to test — split on both
  separators and refuse `\` alongside `%`.
