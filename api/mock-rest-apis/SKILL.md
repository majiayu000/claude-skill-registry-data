---
name: mock-rest-apis
description: "Stand up an HTTP endpoint you control instead of a live third-party API, and point the Mendix app at it — Prism from an OpenAPI contract, a constant swap, or a forward proxy. Use when building or debugging a REST integration without the real API, forcing a 404/500 through an error handler, or running offline or in CI."
---

# Mock REST APIs Skill

Use this skill when a REST integration needs an endpoint you control instead of a
live third-party API — while building it, while reproducing a bug, or while
verifying the app in a browser or a test run.

Developing against the real API means network, rate limits, credentials, and a
payload that can change under you. None of that is where Mendix integration
defects live: those are in the mapping, the entity types, the error handler, and
the BSON. A mock removes the variables that are not the bug.

## When to Use This Skill

- Building a REST client or `REST CALL` microflow before (or without) real credentials
- Reproducing a payload-shaped bug **deterministically** — a shape small enough to read, that behaves the same on every run
- Exercising error paths: 404, 500, a timeout, a 401 from missing auth
- Verifying the app (`test-app`) or running a suite (`test-microflows`) offline or in CI
- Redirecting the outbound calls of an app whose model you must not edit

## Two separate problems

Almost every wasted hour here comes from conflating them:

| Problem | Answer |
|---|---|
| **Something must answer the request** | A mock server: Prism (from a contract), WireMock, mitmproxy |
| **The app must send the request there** | A constant, a `BaseUrl`, or a forward proxy — see below |

A mock server is **not** an interceptor. Prism serves one contract at one port
and answers only clients that address it. Asking it to "catch all calls the app
already makes" is a category error — that is the forward-proxy job, further down.

## 1. Point the app at the mock

Three routes, cheapest first. Pick by how the URL is built.

### The URL is built in the microflow — use a constant, change nothing per run

A `REST CALL` URL is an **expression**, so it can be assembled from a constant
(`@Module.Constant` is Mendix's constant reference — `$Name` is a *variable*):

```sql
mdl 1;
create constant MyModule.ApiBaseUrl ( Type: String, DefaultValue: 'https://api.example.com/v1' );

create microflow MyModule.CallApi() returns string
begin
  $response = call rest service get @MyModule.ApiBaseUrl + '/rates'
    header Accept = 'application/json'
    returns string;
  return $response;
end;
```

Then swap the endpoint per run, with no model change and nothing committed:

```bash
# this run only — never written to the project
mxcli run --local -p app.mpr --constant MyModule.ApiBaseUrl=http://127.0.0.1:4020

# a test suite against the mock (--constant needs --local)
mxcli test tests/ -p app.mpr --local --constant MyModule.ApiBaseUrl=http://127.0.0.1:4020

# machine-local default, gitignored: every run picks it up
mxcli constant set MyModule.ApiBaseUrl http://127.0.0.1:4020 -p app.mpr

# flip it on an app that is already running
mxcli constant set MyModule.ApiBaseUrl http://127.0.0.1:4020 -p app.mpr --apply
```

`constant set` refuses a name the project does not define, so a typo cannot
silently apply to nothing. `mxcli constant list -p app.mpr` shows the winning
value for every constant **and which layer set it** — read it first whenever a
run does not use the endpoint you expected.

### The call goes through a REST client document — rewrite `BaseUrl`

A REST client document's `BaseUrl` is a **literal**; it cannot reference a
constant. Point it at the mock by re-running the create, which is a one-line diff:

```sql
mdl 1;
create or modify consumed rest service MyModule.RatesAPI (
  OpenAPI: 'specs/rates.json',
  BaseUrl: 'http://127.0.0.1:4020'
);
```

`BaseUrl` also overrides `servers[0].url` at import time, so one contract can be
imported against the mock and later re-pointed at production.

### You cannot edit the model at all — use a forward proxy

See §3. This is the most work and the last resort.

## 2. Prism: serve an OpenAPI contract as a mock

```bash
npm install -g @stoplight/prism-cli      # ~15s
prism mock specs/rates.json --port 4020  # serves the contract's `example` values
```

Everything below cost real time to find out and is not on Prism's front page:

- **Prism mounts paths at the root** and ignores any base path in
  `servers[0].url`. Address it as `http://127.0.0.1:4020`, not
  `http://127.0.0.1:4020/v1` — otherwise every path 404s while the server looks
  perfectly healthy.
- **Make `servers[0].url` absolute in the contract you import.** mxcli's OpenAPI
  import only accepts an `http://` or `https://` URL as `BaseUrl`; a relative one
  (`/api/v3`) is skipped with the warning *"server URL … is relative and cannot
  be used as BaseUrl; set BaseUrl explicitly in CREATE CONSUMED REST SERVICE"*, and a
  client with no `BaseUrl` fails at call time, not at import time.
- **`Prefer: code=404`** on the request forces any status the contract documents.
  This is the only practical way to drive a Mendix error handler through a real
  HTTP response rather than by hand-editing the model.
- **`prism mock -d`** returns schema-generated random data instead of the
  `example` values. Run the suite both ways: a mapping that quietly depends on
  one fixed payload passes under `example` and fails under `-d`.
- **Prism enforces the contract's `security`**, so a call with no `Authorization`
  header gets a real 401. Useful — but know the ceiling before you design around
  it: a REST client document's header value may be a literal, a `$Variable`, or a
  literal **prefix** plus a variable (`'Bearer ' + $Token`), and nothing else. A
  token that must be computed per call belongs in a `REST CALL` expression, not
  in the document.
- **Cut a subset; never point Prism at a vendor's full contract.** The official
  Microsoft Graph spec is 41 MB of YAML: it downloads in seconds and Prism was
  still printing "Starting Prism…" when killed at a 300-second cap. Importing it
  would also generate thousands of operations into the module.

A contract small enough to read is the point. Hand-cut one path with one
`example` per response code you care about, and keep it in the project under
`specs/` next to the `.mpr` — the same relative path the `OpenAPI:` clause takes.

## 3. Forward proxy: when the model cannot change

For an app whose model you must not touch, redirect the JVM instead. The Mendix
runtime honours the standard Java proxy properties, and `mxcli run --local`
passes your environment through to the runtime JVM — including `JAVA_TOOL_OPTIONS`,
which mxcli **appends** to rather than replaces, so an exported value survives
even alongside `--trace`. No model change, nothing committed:

```bash
export JAVA_TOOL_OPTIONS="-Dhttp.proxyHost=127.0.0.1 -Dhttp.proxyPort=8080"
mxcli run --local -p app.mpr
```

Two things to know before committing to this route:

- **HTTPS is the real work.** The proxy must present a certificate the JVM
  trusts. WireMock 3.13.2 on Java 21 cannot generate a usable one; use mitmproxy
  (which ships a CA you install into the JVM truststore) or supply your own
  keystore. Plain `http://` targets need none of this — one more reason to have
  the mock on loopback HTTP.
- **Loopback is not proxied.** `127.0.0.1` sits in the runtime's
  `http.nonProxyHosts`, so app→mock traffic on loopback works *inside* a proxied
  container without any exemption of your own. It also means a proxy on
  `127.0.0.1` will not intercept loopback calls — that is not a bug to hunt.

For **consumed OData** services specifically there is a fourth route that needs
no JVM flags: `System.ConsumedODataConfiguration` carries `ProxyConfiguration`,
`ProxyHost` and `ProxyPort` as data (see `system-module`), so the proxy can be
set per service at runtime.

## Verify the mock before blaming Mendix

Always prove the endpoint from the shell first. A Mendix error message cannot
distinguish "the mock is not running" from "the mapping is wrong".

```bash
curl -sS -i http://127.0.0.1:4020/rates          # 200 + the example payload?
curl -sS -i -H 'Prefer: code=404' http://127.0.0.1:4020/rates
```

Then, and only then, run the microflow and check the payload actually reached it
(`mxcli oql`, or the runtime log under `mxcli run --local`).

## Failure modes, symptoms first

| Symptom | Cause | Fix |
|---|---|---|
| Every path 404s, server looks fine | The client address includes the contract's base path | Address Prism at the root: `http://127.0.0.1:4020` |
| Import produced a client with no `BaseUrl` | `servers[0].url` is relative — mxcli warned and skipped it | Make it absolute, or pass `BaseUrl:` explicitly |
| Prism never finishes starting | Vendor contract is tens of MB | Cut the paths you need into a small contract |
| Mock returns 401 | The contract declares `security`; the call sent no credentials | Add the header, or drop `security` from your cut contract |
| Calls still reach the real API | Proxy properties not applied, or the target is loopback (never proxied) | Check the JVM args; prefer the constant route over a proxy |
| Endpoint swapped but the app disagrees | An override on a different layer wins | `mxcli constant list -p app.mpr` — it names the layer |
| Works with `example` values, fails in CI | The mapping depends on one fixed payload | Run `prism mock -d` locally and fix the mapping |

## Related Skills

- `rest-client` — the three ways to call a REST API; where the contract goes once you have one
- `rest-call-from-json` — JSON structure → entities → import mapping → `REST CALL`
- `test-app` — browser verification; a REST app's prerequisite is a reachable endpoint
- `test-microflows` — running a suite; `--constant` points it at the mock
- `run-local` — `mxcli run --local`, the warm loop the mock plugs into
