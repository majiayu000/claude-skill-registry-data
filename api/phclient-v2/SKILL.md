---
name: phclient-v2
description: Use when reading, calling, or debugging shared/thetadata.py (ThetaDataController) — the potatohedge PHClient v2 REST client every suite routes through — especially when a call raises PHRequestValidationError, "v2 payload is None", a 404/502 that looks wrong, or when adding/changing an entry in _PATH_ALIASES/_PARAM_ALIASES.
---

# PHClient v2 (ThetaData proxy client)

## THE FIVE-SECOND LIE (measured 2026-09-19 — read this before blaming the vendor)

**For years the answer to "why did that pull fail?" was "rate limits / transient
proxy 502s / the vendor can't serve that range". For a large class of failures
that was WRONG. It was `httpx`'s default timeout, on our side, five seconds.**

`PHClient` builds `httpx.Client(follow_redirects=...)` with **no timeout**, so it
inherits httpx's 5.0s default, and `ClientConfig` exposes no way to change it.
Anything denser or slower than ~5s died and got filed as vendor flakiness.

Measured live on SPY one-minute history (`market.stock_ohlc`):

| span | httpx default (5.0s) | timeout raised to 120s |
|---|---|---|
| 7d  | OK | OK |
| 10d | **PHTimeoutError at 5.0s** | **OK — 3,519 rows in 0.3s** |
| 14d | **PHTimeoutError at 5.0s** | **OK — 3,909 rows in 0.3s** |
| 21d | **PHTimeoutError at 5.0s** | **OK — 5,862 rows in 0.3s** |
| 25d | **PHTimeoutError at 5.0s** | **OK — 7,425 rows in 0.5s** |
| 30d+ | PHTimeoutError | PHAPIError (real vendor ceiling) |

Same requests. Same proxy. The only change was our own client timeout. Several
of these then returned in **0.3 seconds** — they were never slow, they were
never rate-limited, and the data was there the whole time.

**Fixed:** `shared/thetadata.py::_apply_http_timeout` sets the timeout on every
thread-local `PHClient` (`THETADATA_HTTP_TIMEOUT_S`, default **120**).

### The diagnostic that settles it in one look

**Check the elapsed time.** A failure at *almost exactly 5.0s* is the old
client default, not the vendor. A real vendor refusal either comes back fast
(instant `PHAPIError` = `LARGE_REQUEST` rejected) or after a genuinely long
wait. If something times out at 5.0s on the dot, the request was fine.

### What is STILL real — do not overcorrect

- **The `LARGE_REQUEST` ceiling exists.** 30 days of one-minute data returns
  `PHAPIError` no matter how long you wait. Dense routes must still chunk:
  **21 days** for one-minute (`hist_stock_ohlc`), 28 for EOD-density routes.
  One minute is ~390 rows a session against EOD's one, so an EOD-safe span is
  nowhere near safe on a minute route.
- **Concurrency still bites.** Concurrent `PHClient` callers really do time
  each other out; serialise, sleep 0.3–0.5s, never fan out.
- Genuine 502s on options bulk routes under load are still real rate limits.

**The rule: prove it with the clock before you call something a rate limit.**


`shared/thetadata.py::ThetaDataController` is a **legacy-path shim over the real `potatohedge`
v2 SDK** (`potatohedge.client_v2.PHClient`), not a hand-rolled REST client anymore (that was true
pre-2026-08-18). Every one of `ThetaDataController`'s ~28 public methods builds an old-style
`/api/theta/...` path + flat params dict, which `_translate_path`/`_rewrite_params` convert into a
v2 namespaced call (`client.options.bulk_snapshot_option_open_interest(**kwargs)` etc) via
`_PATH_ALIASES` (path pattern → namespace/method/defaults) and `_PARAM_ALIASES` (legacy param
name → v2 param name). Full vendor docs (method catalog, REST endpoint catalog, migration guide)
are mirrored at `docs/phclient_v2/vendor_docs/`; the migration/bug-fix session log is
`docs/phclient_v2/WIKI.md` — read that before assuming something here is stale.

## Key architectural facts

- **Namespaced methods, not flat.** `client.options.*`, `client.market.*`, `client.dealer.*`.
- **Capability-scoped credentials** — `ClientConfig.credentials` is a dict keyed by capability
  string (`options.bulk.read`, `dealer.read`, ...), each with its own `Credential`. No blanket `"*"`.
- **`caller_id="zinko"` is mandatory** on every request (`PH-Caller-Id` header).
- Responses are `ResponseEnvelope`s — unwrap via `.data`. `shared/thetadata.py`'s `_V2Response`
  wraps this: `.json()` raises `TypeError("v2 payload is None")` when `env.data` is `None` (server
  genuinely returned no data, or every retry attempt in `_get_with_retry` was exhausted).
- **Dates are `YYYYMMDD`**, strikes are integer-thousandths of a dollar (190000 = $190.00),
  intervals in ms. `exp` is typed as an **integer** in the v2 schema even though this codebase
  always builds/passes it as a string (`"20261117"`) — the SDK coerces this fine, not a bug.
- **`use_csv` matters and defaults to `True` server-side** on most `/api/theta/*` routes, meaning
  "list of lists" (`[headers_row, data_row, ...]`), not raw CSV text. `_parse_rows`/`_rows_from_any`
  already handle this shape (the "legacy ThetaData list-of-lists" branch) — don't assume you need
  to force `use_csv=False` unless a specific method's `_PATH_ALIASES` entry already does so
  (`get_dealer_positioning` and the catch-all fallback in `_translate_path` do).
- **`retry_policy` is per-endpoint** (`"unsafe"` on bulk snapshot routes) and the vendor's own
  `PHClientError.retryable` flag is **not trustworthy** — live 502s come back with
  `retryable=False` even though a bare retry seconds later succeeds. `_get_with_retry` retries on
  `e.retryable OR e.status in _RETRY_STATUSES` (`404, 502, 503, 504`) for exactly this reason —
  if you ever "simplify" that OR to just `e.retryable`, you silently stop retrying real transient
  failures (this happened once already, see WIKI.md bug #5).

## Known-fixed bugs — don't reintroduce these

1. `list_expirations` — `available_expirations` rows are dicts (`{'expiration': '2026-08-14'}`),
   not strings. Extract `.expiration`, normalize `YYYY-MM-DD` → `YYYYMMDD`.
2. `list_strikes` — single-expiration `options_chain` returns a chain-summary dict with strikes
   nested under `data['chain']`, not a flat contract list.
3. `options_chain` needs `exp`→`expiration` and `root`→`ticker` renamed — it's the ONE namespace
   method that doesn't use the `exp`/`root` convention every other method uses. Special-cased in
   `_translate_path`, not in the generic `_PARAM_ALIASES` table.
4. **Double-passthrough key collisions** — a param can't be both (a) in `_PARAM_ALIASES` as an
   alias target AND (b) in `_rewrite_params`'s literal-passthrough set, or both the old and new key
   name reach the SDK call and it 422s with `PHRequestValidationError: request arguments do not
   match the generated signature`. This is exactly what broke `ivl`/`interval` for 100% of
   hist-greeks calls before the fix — when adding a new alias, grep the passthrough set in
   `_rewrite_params` for the same target name first.
5. `PHClient` is built **per-thread** (`threading.local()` in `ThetaDataController.__init__`), not
   shared, because the suites fan out concurrent hist calls across a `ThreadPoolExecutor`
   (`option_bulk_hist_greeks`/`option_bulk_hist_oi`/`_enumerate_contracts`) and nothing in the SDK's
   docs promises thread-safety for concurrent request-building.

## "v2 payload is None" — what it actually means

Not a wiring bug by itself. It's `_get_with_retry` exhausting its retries and the last response's
`.data` still being `None` — i.e. a real transient outage or genuinely-empty snapshot (common on
thin/micro-cap tickers), not "wrong endpoint/params". See `rate-limit-options` for the
acquisition-discipline side of this (backoff, one-ticker-at-a-time, don't impute zeros). Before
assuming a mapping bug, check `_PATH_ALIASES`/`_PARAM_ALIASES` for the specific method against
`docs/phclient_v2/vendor_docs/CLIENT_REFERENCE.md`, then check whether the *caller* (e.g.
`orchestrator.py`'s max-pain fallback, or a Vol_Suite required-file validation check) is treating
this failure mode as gracefully as it treats a plain 404 — a validation cascade from one failed
step (e.g. dealer positioning) silently disabling an unrelated feature (e.g. GARCH/fair-vol context
threading) has happened before and doesn't announce itself as a v2-client bug.

## Where to look before changing anything

- `shared/thetadata.py`: `_PATH_ALIASES` (~line 127), `_PARAM_ALIASES` (~line 196),
  `_translate_path`/`_rewrite_params` (~line 319), `_get_with_retry` (~line 514), `_parse_rows`/
  `_rows_from_any` (~line 553).
- `docs/phclient_v2/vendor_docs/CLIENT_REFERENCE.md` — full generated method catalog (namespace +
  method name, canonical).
- `docs/phclient_v2/vendor_docs/API_REFERENCE.md` — full generated REST endpoint catalog (path,
  params, schema types — this is where you'll find the `exp: integer` / `use_csv` details above).
- `.venv/Lib/site-packages/potatohedge/_generated/descriptors.py` — the actual installed SDK's
  machine-readable endpoint contracts (path, params, `retry_policy`, `auth_capability`); more
  authoritative than the mirrored docs if the two ever disagree, since it's what's really running.
