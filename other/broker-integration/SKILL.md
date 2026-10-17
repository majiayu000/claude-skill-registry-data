---
name: broker-integration
description: Add a broker to OpenAlgo Desktop or change an existing Rust broker adapter under src-tauri/src/brokers/. Use when porting a broker from the web's broker/<name>/ Python, wiring its sign-in (OAuth redirect, direct login with TOTP, Noren or XTS family member, bespoke), master contract, books, quotes, depth, history, margin, GTT or streaming feeds, when a broker is missing from Select Broker or Broker Configuration, or when debugging broker symbol, exchange, status or order-field mapping, a forged-callback refusal, or a token that reaches a log.
---

# Broker integration (Rust)

The broker's only job is translation: the broker's shapes in, OpenAlgo's
common symbol, order, book and streaming formats out. Business logic lives in
`src-tauri/src/services/`, never in an adapter. Analyzer mode short-circuits
to the sandbox engine before any broker call, so "it works in analyzer mode"
proves nothing about an adapter.

The web's skill is the companion for broker *behaviour* (rate limits, history
windows, order-type emulation, quirks per broker). Its references are in the
read-only web checkout at `openalgo/.claude/skills/broker-integration/references/`
(`cross-broker-reference.md`, `auth-and-login.md`, `master-contract.md`,
`streaming.md`, `order-updates.md`, `history-data.md`, `rate-limiting.md`,
`order-type-emulation.md`, `hardening-and-verification.md`). This skill is the
desktop's *mechanics*: where each piece goes in Rust and how it is tested.

## 1. Pick the family first

| Family | Shape in this repo | Members | Copy |
| --- | --- | --- | --- |
| Noren / Finvasia | `families::noren::NorenBroker` holding a `&'static NorenConfig` (hosts, `Dialect`, `Login`, master files, `TickRule`, `IndexNaming`, `MppScope`, `FundsM2m`, ...) plus `NorenHooks` fn pointers. A member dir is one `mod.rs` with `pub static CONFIG`, `pub static HOOKS` and `pub fn broker(symbols) -> NorenBroker`. | shoonya, flattrade, tradesmart, zebu | `brokers/shoonya/mod.rs` |
| Symphony XTS | `families::xts::XtsBroker` holding a `&'static XtsConfig` (`XtsLogin`, paths, `master_segments`, `stream_mode_codes`, `binary_decoder`, `XtsHooks`). Member dir is one `mod.rs` with `CONFIG` and `pub fn broker`. | fivepaisaxts, jainamxts, compositedge, rmoney, ibulls, wisdom, iifl | `brokers/fivepaisaxts/mod.rs` |
| OAuth redirect | Own module | zerodha, upstox, fyers, dhan, groww, arrow, paytm, aliceblue, definedge, pocketful, hdfcsky, hdfcsecurities | `brokers/zerodha/` |
| Direct login + TOTP | Own module | angel, kotak, mstock, motilal, samco, tradejini, fivepaisa, nubra, indmoney, firstock | `brokers/angel/` |
| Bespoke | Own module | iiflcapital (REST + MQTT via the relay), deltaexchange (HMAC, `CRYPTO`, leverage) | as named |

The family is the code shape. How the trader actually signs in is decided per
broker by `catalog::auth_type` and `login_kind`, and does not follow the
table: Groww (TOTP or a pasted access token) and Definedge (OTP) sign in through the
in-app form, while the Noren members, compositedge, rmoney and iiflcapital
redirect. Check the catalogue, not the family, before wiring the login.

A white-label of Noren or XTS is a new `CONFIG` constant, not new code. Look
for `/NorenWClientTP/` or `/interactive/user/session` in its API docs before
deciding it is bespoke. If a config field cannot express a difference, add a
hook to `NorenHooks` / `XtsHooks` rather than forking the family.

A standalone module follows the existing layout (see `brokers/angel/` or
`brokers/kotak/`): `mod.rs` (the adapter struct and `impl Broker`), `auth.rs`,
`orders.rs`, `data.rs`, `funds.rs`, `mapping.rs`, `master_contract.rs`,
`streaming.rs`, optional `gtt.rs`, and `tests.rs` behind `#[cfg(test)]`. The
adapter takes a `SymbolResolver` in `new(symbols)` and keeps a clone of
`common::http::client()`; give it a `with_base_url(..)` (and
`with_feed_urls(..)` when it streams) constructor so tests can point it at a
local fake.

## 2. The `Broker` trait (`src-tauri/src/brokers/mod.rs`)

Required: `id`, `name` (the display name the UI shows), `logo`, `login_kind`
(`types::LoginKind::{Redirect, DirectTotp, TwoStep, AccessToken,
ApiKeySecret}`), `supported_exchanges` (the web `plugin.json` list, a promise
you must test), `capabilities` (`types::Capabilities`: `history`,
`multiquotes_batch`, `margin`, `gtt`, `streaming`, `order_feed`,
`depth_levels`), `timeframe_map`, `authenticate`, `place_order`,
`modify_order`, `cancel_order`, `get_order_book`, `get_trade_book`,
`get_positions`, `get_holdings`, `get_funds`, `get_quote`,
`get_market_depth`, `get_history`, `download_master_contract`.

Defaults you override only when the broker differs:

| Method | Default | Override when |
| --- | --- | --- |
| `begin_login(&creds)` | `Ok(None)`: the catalogue's authorize URL applies | the authorize address needs a broker call first (Dhan's consent). Called by `BrokerAuthService::start_oauth`. |
| `restore_session(&creds)` | nothing | per-login state the stored token does not carry must be rebuilt on resume after a restart (Kotak's UCC). Never sets password, TOTP or codes. Called from `broker_auth_service.rs` resume. |
| `on_logout()` | nothing | the adapter runs anything itself (an order poller, cached session state). Called by `BrokerRuntime::teardown` on logout, at the 03:00 IST boundary and at shutdown. Must be idempotent. |
| `create_feed(&auth)` | `Unsupported("streaming")` | the broker has a market-data socket. Returns `Box<dyn BrokerFeed>`. |
| `create_order_feed(&auth)` | `Unsupported("order_feed")` | order updates come from a socket (`OrderFeed::Socket`) or a poller you own (`OrderFeed::Stream(mpsc::Receiver)`, see `common::order_poll`). Leave unsupported when the market feed already carries them (Kite). |
| `create_depth_feed(&auth, levels)` | `Unsupported("depth_feed")` | a separate socket serves books deeper than 5 (Fyers 50, Dhan 20). `BrokerRuntime` asks for each `depth_levels` entry above 5. |
| `feed_depth_levels(exchange)` | `capabilities().depth_levels` | depth differs by exchange. The feed bridge uses it to answer 8765 subscribers. |
| `get_holdings_with_totals(&auth)` | holdings, `totals: None` (the service computes them) | the broker reports its own portfolio totals (Angel's `totalholding`). Used by `account_service`. |
| `get_multiquotes` | one `get_quote` per key | the broker has a batch endpoint; also set `multiquotes_batch`. Options tools ask for 180+ symbols. |
| `cancel_all_orders`, `close_all_positions`, `get_open_position` | built from the books | the broker has a native call. `close_all_positions` needs `symbols()` to return your resolver. |
| `calculate_margin`, GTT methods | `Unsupported` | the broker supports them; set the capability. Basket margin: never sum legs when a basket endpoint exists. |
| `place_order_exact`, `leverage_config`, `broker_type`, `set_leverage` | whole units, `IN_stock` | crypto only (deltaexchange). |
| `as_any` | `None` | a sign-in helper needs the concrete type (Definedge OTP, Samco IP check). |

`BrokerCredentials` and `AuthResponse` have redacted `Debug`. `AuthToken`
holds a `Secret`; read it with `expose()` only where the request is built.

## 3. Registration and the catalogue

1. `brokers/mod.rs`: `pub mod <name>;` and one line in `BrokerRegistry::new()`
   (`Arc::new(<name>::XBroker::new(symbols.clone()))` or
   `Arc::new(<name>::broker(symbols.clone()))` for a family member). Update
   the sorted id list in the `registry_shares_one_symbol_master` test.
2. `brokers/catalog.rs`:
   - `ALL_BROKERS` (web directory order) feeds `valid_brokers` in
     `GET /api/broker/credentials`.
   - `auth_type`: `OAuth` (browser redirect to `/<broker>/callback`) or
     `Form` (in-app form posted to `/<broker>/callback`).
   - `authorize_url_string`: the authorize URL with the server-generated
     `state`. Return `None` when `begin_login` builds it.
   - `extract_code`: which callback parameter carries the code. Spell it
     exactly (Zerodha `request_token`, Fyers `auth_code` and never `code`).
   - `callback_carries_state`: `false` only when the broker's redirect drops
     `state`. Such a callback is matched to the newest pending sign-in of that
     broker from the same browser session (single use, 3 minutes) and must be
     bound to an account.
   - `configured_account` and `CLIENT_ID_BROKERS`: the account a sign-in
     must come back for. Dhan and the Noren family take `client_id:::key` or
     a client id; Arrow, HDFC Sky, HDFC Securities and AliceBlue take the
     Client ID entered on Broker Configuration. A state-less broker with no known
     account is refused, so a state-less broker must name its account here.
   - `login_binding` / `callback_binding` (Dhan's `consentAppId`),
     `posts_callback` (XTS `session=` form POST: compositedge, rmoney),
     `pasted_token` (tradesmart), `login_fields` and `credential_slot` (the
     in-app form fields and which `BrokerCredentials` slot each fills).
3. The redirect URL stays byte-identical to the web:
   `http://127.0.0.1:5000/<broker>/callback` (`ServerConfig::redirect_url_for`).

## 4. Symbols: every book returns OpenAlgo symbols

Orders, trades, positions and holdings must carry OpenAlgo `symbol` and
`exchange`, never the broker's trading symbol, or smart orders and
close-position silently mismatch. Resolve through `SymbolResolver`
(`common/symbols.rs`): `oa_symbol(brsymbol, exchange)`,
`oa_symbol_or_raw(..)`, `br_symbol(symbol, exchange)`, `token(..)`,
`brexchange(..)`, `by_token(exchange, token)`, `by_brsymbol(..)`,
`by_symbol(..)`. Map statuses to the web's lowercase strings (`complete`,
`open`, `trigger pending`, `cancelled`, `rejected`; `brokers::lower_status`
for the rest) and constants through `common::mapping` (`Exchange`,
`Product`, `PriceType`, `Action`, `OrderStatus`, `Validity`). Requests reach
you as `ResolvedOrder` / `ResolvedModify`, already resolved against the
master.

## 5. Master contract

`download_master_contract` returns `Vec<SymbolData>` (`SymbolData` is
`common::symbols::SymToken`). Fill every web `SymToken` column: `symbol`,
`brsymbol`, `name`, `exchange`, `brexchange`, `token`, `expiry` as `DD-MMM-YY`
uppercase (empty when it never expires), `strike`, `lot_size`
(`lotsize`), `instrument_type` (`instrumenttype`), `tick_size`. Dropping one
breaks expiry pickers and option chains. Helpers in
`common/master_contract.rs`: `format_expiry`, `parse_broker_expiry`,
`normalise_expiry`, `format_strike`, `future_symbol`, `option_symbol`,
`split_csv_line`, `CsvHeader` (read columns by header name, not position).
Downloads use `http::DOWNLOAD_TIMEOUT`. Crypto per-row extras go through
`download_master` / `MasterContract`.

`services/master_contract_service.rs` decides when to download
(`should_download`, the broker's `cutoff`), stores rows in the `symtoken`
table (`db/sqlite/symbol.rs`), loads them into the shared resolver and emits
the web's Socket.IO events. Ground truth for symbol formats is the web's
`symtoken` for the same broker, or the web docs
`docs/prompt/symbol-format.md`.

## 6. Streaming

Implement `common::streaming::BrokerFeed`: `broker`, `prepare` (async work
before each connect: authorize call, socket token; `PrepareError::AuthFailed`
stops the manager), `ws_request`, `on_connected` / `on_authenticated` /
`awaits_auth_ack`, `subscribe_frames`, `unsubscribe_frames`,
`mode_change_frames`, `parse` (frame to `FeedEvent::{Tick, Depth,
OrderUpdate, AuthOk, AuthFailed, Heartbeat, Reply}`), `heartbeat`,
`supported_depth_levels`, `is_auth_failure`.

The feed is driven by `websocket::WebSocketManager`
(`src-tauri/src/websocket/manager.rs`): one owned supervisor task, connect
timeout, close-before-reconnect, capped exponential backoff with jitter, stall
timeout, re-subscribe on reconnect, reference-counted subscriptions, bounded
command channel and a bounded broadcast (`TICK_CHANNEL_CAP`) whose slow
receivers see `Lagged`. You write no reconnect loop. `services/broker_runtime.rs`
starts the market feed, the depth feed and the order feed on login and tears
all of them down (one `JoinSet`, three managers) on logout.

A transport that is not a broker WebSocket (IIFL Capital's MQTT) or an
upstream session that must be relayed (Nubra's order socket) goes through the
loopback relay, `common/relay.rs`: implement `Upstream::open` and `Session`,
start it with `RelayHandle::start` / `ensure_started`, and point
`ws_request` at `RelayHandle::url()` (`ws://127.0.0.1:<port>/<secret>`).
Readiness and refusals reach `parse` as control frames (`relay::control`).
The relay owns one listener and one session, aborted with the handle.

Ticks carry OpenAlgo symbols, epoch-millisecond timestamps, and
`NormalizedTick::derive_change` for change and percent. The 8765 contract
(modes 1/2/3, depth 5/20/30/50) is checked by `tests/it/feed_conformance.rs`.

## 7. Secrets and redaction

- One HTTP client: `common::http::client()` (timeouts built in). Never
  `reqwest::Client::new()` in an adapter.
- Every request, socket and transport error that may be logged or returned
  goes through `common::redact`: `http(e)` (a `reqwest` error without its
  URL), `ws(e)` / `ws_error_kind(&e)` (a socket error by kind only),
  `redact(AppError)`, and `url_safe_error(&e)` / `url_safe(text)` for log
  lines (keeps scheme, host, path; drops userinfo, query, fragment). Brokers
  that put a key or token on a URL (Kite's ticker, HDFC, mStock) leak through
  `reqwest`'s `Display` otherwise.
- `lib.rs::log_filter` pins `tungstenite` at info because it traces the
  handshake URL; do not lower it.
- Trader-facing messages come from `AppError::client_message`; the detail
  goes to the log once, at the boundary.

## 8. Tests to write (in the same commit)

Fixtures: `src-tauri/tests/fixtures/brokers/<broker>/` (recorded broker
payloads: `order_book.json`, `positions.json`, `holdings.json`,
`quote.json`, `master.json` or `instruments.csv`, `errors.json`, ...). Use
`<APIKEY>`, `<USER_ID>`, `<EMAIL>`; fake JWTs end in `.sig`, `.signature` or
`.c2ln` (the gitleaks allowlist in `.github/gitleaks.toml`). Never a real
account id or token.

1. **Mapping unit tests** in `src/brokers/<broker>/tests.rs`, loading
   fixtures with `include_str!(concat!("../../../tests/fixtures/brokers/<broker>/", $name))`
   (see `brokers/zerodha/tests.rs`): master rows by header name, every book
   to OpenAlgo symbols and statuses, order payloads equal to what the web
   sends, quotes and depth, history candles (epoch seconds, oldest first),
   funds, margin, error mapping to trader-facing text. Where the web
   recorded the same instrument, compare against `tests/fixtures/web/rest/`
   (`web_fixture` in the Zerodha tests).
2. **HTTP round trip** in `src-tauri/tests/it/` against a local axum fake on
   an ephemeral port (`with_base_url`): headers, request bodies and the mapped
   answers for auth, orders, books, funds, quotes, depth, history, margin,
   GTT. Model: `tests/it/broker_angel_http.rs`; batch modules in
   `tests/it/brokers_noren.rs`, `brokers_xts.rs`, `brokers_oauth_batch/`,
   `brokers_direct_batch_a/`, `brokers_direct_batch_b/`. A new file is a new
   `mod` line in `tests/it/main.rs`.
3. **Secrets never leak.** Model: `tests/it/brokers_direct_batch_b/secrets.rs`.
   Drive every auth, REST and socket error path with sentinel credentials
   (`const S: &str = "SENTINELq7Zx"`, a digit sentinel for TOTP/PIN), against
   a closed port (transport errors carry the URL) and a fake that refuses
   everything. Capture tracing at TRACE with a `fmt()` subscriber writing to
   a buffer (`tracing::subscriber::set_default`), assert the capture is not
   empty (else the check is vacuous) and that the sentinel appears nowhere:
   logs, `Display`, `Debug`, `client_message`. For a single error helper, the
   precondition pattern in `brokers/hdfcsky/tests.rs`
   (`transport_errors_lose_their_url_before_logging`): assert the raw error
   does carry the secret, then that the redacted one does not.
4. **Feed parsing** of recorded frames (`parse` to `FeedEvent`, binary
   offsets, subscribe frames), and for a feed with its own task a hygiene
   test like `tests/it/broker_groww_hygiene.rs` or
   `broker_upstox_feed_hygiene.rs` (tasks and descriptors back to baseline).
5. **Sign-in refuses forgeries.** When the broker's callback is state-less,
   uses a client id, posts its callback or takes a pasted token, add its
   cases to `server::tests::every_way_to_create_a_broker_session_refuses_a_forged_attempt`
   (`src-tauri/src/server/tests.rs`; the broker joins `family_harness`) and
   update the table in `docs/security/known-residuals.md`. Run:
   `cargo test --lib every_way_to_create_a_broker_session`.
6. `cargo test --lib catalog` for `extract_code` / `authorize_url` /
   `configured_account` cases.

Run (from `src-tauri/`, with the shared target dir):

```bash
export CARGO_TARGET_DIR=/Users/openalgo/openalgo-desktop/openalgo-desktop/src-tauri/target
cargo test --locked --lib brokers::<broker>
cargo test --locked --test it broker_<broker>      # or the batch module name
cargo clippy --all-targets --locked -- -D warnings
(cd .. && python3 scripts/ci/code_health.py)        # CLAUDE.md, Code health
```

A new broker is new code, so it meets the Code health limits in full: an
adapter over 1,000 lines splits into `auth.rs`, `orders.rs`, `streaming.rs`
and `mapping.rs` the way the existing brokers do, and a shared shape belongs
in its family's generic code, not in a copy.

## 9. Frontend touchpoints

- `src-tauri/src/brokers/setup_guide.rs`: the broker's entry on the Broker
  Configuration page (`src/pages/BrokerConfig.tsx`, served by
  `GET /api/broker/list`): the display name, the keys it needs labelled the
  way the broker names them (API key, secret, the client id for
  `catalog::CLIENT_ID_BROKERS`, the market-data pair for XTS), a hint per
  key, the sign-in banner and the redirect URL hint. Its table test
  (`every_broker_has_help_consistent_with_its_sign_in`) checks the entry
  against the catalogue; a new broker needs an entry and nothing in TS.
- Select Broker (`src/pages/BrokerSelect.tsx`) starts each sign-in the way
  the server reports it: `sign_in` (`catalog::sign_in`) on
  `GET /api/broker/list`. `redirect` goes to `GET /<broker>/initiate-oauth`
  (the server builds the URL and records `state`; the page never sees the
  API key), `form` to `GET /<broker>/callback` (which opens the in-app login
  card, sending Definedge's and Nubra's OTP first), `saved_keys`
  (`catalog::SAVED_KEY_BROKERS`: the keys are all the adapter needs) signs in
  with one CSRF-checked `POST /<broker>/callback` and no fields; a `GET` of
  that callback signs in nothing. A failed redirect sign-in comes back to
  `/broker?error=..&broker=<id>` and shows on that card.
  `server::tests::sign_in` drives every catalogue broker this way.
- `src/pages/BrokerTOTP.tsx` carries the web's per-broker form copy for
  direct-login brokers; keep it close to the web's
  `frontend/src/pages/BrokerTOTP.tsx` and make its field names match
  `catalog::login_fields` / `credential_slot`.
- `Broker::logo` returns `/logos/<broker>.svg` by convention, but no logo
  files ship in `public/` today; do not add one without the others.

## 10. Porting from the web's `broker/<name>/`

| Web Python | Desktop Rust |
| --- | --- |
| `plugin.json` | `id`, `name`, `logo`, `supported_exchanges`, `broker_type`, `leverage_config` |
| `api/auth_api.py` `authenticate_broker` | `auth.rs`, `Broker::authenticate`; callback params in `catalog.rs` |
| `api/order_api.py` | `orders.rs`: place, modify, cancel, books, `cancel_all_orders`, `close_all_positions`, `get_open_position` |
| `mapping/transform_data.py` | request payload builders and enum maps in `mapping.rs` / `orders.rs` |
| `mapping/order_data.py` | book mappers in `mapping.rs` (OpenAlgo symbols, lowercase statuses) |
| `api/data.py` `BrokerData` | `data.rs`: quote, multiquotes, depth, history, `timeframe_map` |
| `api/funds.py` | `funds.rs` |
| `api/margin_api.py`, `api/gtt_api.py` | `calculate_margin`, GTT methods |
| `database/master_contract_db.py` | `master_contract.rs` |
| `streaming/*_adapter.py`, `*_websocket.py` | `streaming.rs` (`BrokerFeed`); no thread, no ZMQ, no reconnect loop |
| `utils.httpx_client`, `utils.logging` filter | `common::http::client()`, `common::redact` |
| `utils.mpp_slab` | `common::mpp` (`protected_price`, `round_to_tick`) |
| per-broker `test/test_<broker>_*.py` | Rust unit and `tests/it` cases with the same inputs and expectations |

Read the web code and its tests for behaviour, then reproduce shapes, not web
bugs (`tests/fixtures/web/INDEX.md` lists the observed defects). Never edit
the web checkout.

## Checklist

- [ ] Family chosen; family member = config + hooks only
- [ ] `Broker` impl: required methods, capabilities honest, `supported_exchanges` = web `plugin.json`
- [ ] Session hooks where needed: `begin_login`, `restore_session`, `on_logout` (idempotent, stops pollers)
- [ ] Registered in `BrokerRegistry::new()` and the registry test id list
- [ ] `catalog.rs`: `ALL_BROKERS`, `auth_type`, authorize URL, `extract_code`, state carriage, `configured_account` / `CLIENT_ID_BROKERS`, form fields
- [ ] Every book returns OpenAlgo symbols and web status strings
- [ ] Master contract fills every `SymToken` column, expiry `DD-MMM-YY`
- [ ] Feeds via `BrokerFeed` on the shared manager (relay only for non-WebSocket transports); depth and order feeds as the broker offers
- [ ] Shared HTTP client; every error through `common::redact`; nothing secret in logs
- [ ] Fixtures under `src-tauri/tests/fixtures/brokers/<broker>/` with placeholders
- [ ] Unit mapping tests, HTTP round trip, secrets test (non-vacuous), feed parsing, forged-sign-in cases
- [ ] `catalog::sign_in` right for the broker (the broker page follows it), a `setup_guide.rs` entry, `BrokerTOTP.tsx` copy
- [ ] `fd-audit` skill run on the change; `verify` skill before claiming a control holds
- [ ] fmt, clippy `-D warnings`, the full `cargo test --locked` green
