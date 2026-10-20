---
name: fespalier-cratestack
description: "Wiring a CrateStack backend into a fespalier app with fespalier_cratestack (since 0.10.0) — the generate-dart client, the two seams the app writes (a CrateStackTransport over the generated RPC adapter, an error reader with CrateStackFailure.fromEnvelope), the startup() overrides, the Dio with CrateStackCancelInterceptor, CrateStackPortalInterceptor and fespalier_dio's WriteGuard, ref.cancellable in data.dart, actions as intents with withCrateStackFieldErrors, the server's idempotency contract (keys namespaced by a verified principal) and the answer table, one retry layer, where the embedded SQLite mode fits, and the package's debug messages. Load before connecting a CrateStack client to data.dart or action.dart, configuring its Dio, or when a CrateStack call runs twice, is cancelled with another page, or an override error names crateStackTransport."
---

# fespalier-cratestack

> **Verified against fespalier `589cf391` (2026-10-08), release v0.13.0.**
> These skills ship in the fespalier repository, and CI checks them against its code
> on every change. Version-sensitive claims say the release they became true in; if
> your app pins another fespalier, trust that release's code over this page. See
> [Versions](https://github.com/fespalier/fespalier/blob/main/skills/README.md#versions).

**Since 0.10.0.** `package:fespalier_cratestack` puts a [CrateStack](https://cratestack.dev) client behind
`data.dart` and `action.dart` and makes it work offline. The ideas (reads that say how current they are, intents, owned
rows, sync) are [`fespalier-offline`](../fespalier-offline/SKILL.md) and the API is its; this skill is the **wiring**.

- **No `fsp` change**: no file kind, key or command, and the same `app.g.dart`. You write `data.dart` and `action.dart`
  as always and call the package inside them. It has **no `fespalier_adapter.dart`**, so `adapters:` cannot list it:
  it goes in `startup()`.
- **No CrateStack package dependency.** It never imports CrateStack's Dart runtime (`cratestack_cbor` pins
  `flutter_rust_bridge` exactly, which would be yours to resolve): your generated client reaches it through **two small
  seams you write once**, a transport and an error reader.
- **No timers, no listeners.** The one periodic trigger is a signal your app fires from its own timer.
- **CrateStack is pre-1.0.** The package was written against its `generate-dart` client and its documented behaviour;
  where something is an assumption, this skill says so.

## Install

```yaml
# pubspec.yaml: the same url and the same ref for all three, or pub refuses to resolve
dependencies:
  fespalier:
    git:
      url: https://github.com/fespalier/fespalier
      path: packages/fespalier
      ref: <the tag of your fespalier>
  fespalier_dio:
    git:
      url: https://github.com/fespalier/fespalier
      path: packages/fespalier_dio
      ref: <the same tag>
  fespalier_cratestack:
    git:
      url: https://github.com/fespalier/fespalier
      path: packages/fespalier_cratestack
      ref: <the same tag>
```

(A fragment: pub resolves them only at a release tag that contains the packages, 0.10.0 or later; never write `ref: v…`
in these pages, where `cli/tests/versions.rs` reads it as fespalier's own version. The package's
[install block](https://github.com/fespalier/fespalier/blob/main/packages/fespalier_cratestack/README.md#install) is the
one release-please keeps current.) Dart 3.9, Flutter 3.35.

| Library                                                  | For                                | What is in it                                                                                                                  |
| -------------------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `package:fespalier_cratestack/fespalier_cratestack.dart` | everything that is not Dio or Hive | the transport seam, errors, `Served` and `ref.serve`, `LocalStore`, `ReadCache`, intents, owned rows, `SyncEngine`, `autoSync` |
| `package:fespalier_cratestack/dio.dart`                  | Dio                                | `ref.cancellable`, `CrateStackCancelInterceptor`, `CrateStackPortalInterceptor`, `DioFailures`                                 |
| `package:fespalier_cratestack/hive.dart`                 | a durable store                    | `HiveLocalStore`, a hive_ce box that never evicts                                                                              |
| `package:fespalier_cratestack/testing.dart`              | tests                              | `FakeCrateStackTransport`, `FakeRowServer`, `ManualSyncTicker`, `crateStackTestOverrides`                                      |

## 1. Generate the client

```sh
cratestack generate-dart --schema schema.cstack --out packages/shop_client --library-name shop_client \
  --preset riverpod --run-build-runner
```

Commit the output as a path dependency of the app and gate it in CI with `cratestack generate-dart ... --check`, so a
schema change cannot leave it stale. **Use the RPC transport**: every procedure takes a per-call options object that
carries the idempotency key, and RPC errors are typed (`CratestackRpcException`: status, code, message). REST works for
reads and for a `RestCall` intent, but REST has no typed error, so the classification has only the HTTP status to go on.

## 2. The two seams

The generated types (`CratestackRpcAdapter`, `CratestackRpcCallOptions`, `CratestackRpcException`) live in **your**
generated package, which is why the package cannot ship these. Verbatim from the docs, as fragments (they cannot compile
without that package):

```dart
final class GeneratedTransport implements CrateStackTransport {
  GeneratedTransport(this.adapter);
  final CratestackRpcAdapter adapter;

  @override
  Future<Object?> send(CrateStackCall call, {String? idempotencyKey}) => switch (call) {
    RpcCall(:final opId, :final input) => adapter.call(
      opId,
      input,
      options: CratestackRpcCallOptions(idempotencyKey: idempotencyKey),
    ),
    RestCall() => throw UnsupportedError('this app uses the RPC transport'),
  };
}

CrateStackFailure? readShopError(Object e) => e is CratestackRpcException
    ? CrateStackFailure.fromEnvelope(status: e.status, code: e.code, message: e.message, details: e.details)
    : null;
```

The same shape, built here against an **app-side stand-in** for the adapter's call so the `switch (call)` is checked:

```dart
// lib/shop_transport.dart
import 'package:fespalier_cratestack/fespalier_cratestack.dart';

/// A stand-in for the generated adapter's call: your CratestackRpcAdapter.call has this shape, with its options object.
typedef RpcCaller = Future<Object?> Function(String opId, Object? input, {String? idempotencyKey});

final class ShopTransport implements CrateStackTransport {
  ShopTransport(this._call);

  final RpcCaller _call;

  @override
  Future<Object?> send(CrateStackCall call, {String? idempotencyKey}) => switch (call) {
    RpcCall(:final opId, :final input) => _call(opId, input, idempotencyKey: idempotencyKey),
    RestCall() => throw UnsupportedError('this app uses the RPC transport'),
  };
}
```

`CrateStackErrors([readShopError, DioFailures.read])` runs the readers in order, **the app's reader first** (a
`CrateStackFailure` passes through as itself; anything unknown is `null` and is rethrown unchanged by whoever asked).
`CrateStackFailure.fromEnvelope` applies the status and code table (`fespalier-offline`,
[`fespalier-offline`](../fespalier-offline/SKILL.md) (its `intents.md` page)).

## 3. `startup()`, the Dio and the root layout

The full, compiled wiring is [`references/wiring.md`](references/wiring.md). The overrides, in short:

- `shopAdapterProvider` (your generated client's provider) on a Dio you configure, `crateStackTransport` over it, and
  `crateStackErrors` with `[readShopError, DioFailures.read]`;
- `crateStackScope.overrideWith((ref) => ref.watch(authUserId))` (whose data it is: `fespalier_auth`) and
  `localStore.overrideWithValue(await HiveLocalStore.open(directory: ...))` (where queued work lives);
- optionally `readCache` on the storage your `dataCache` already uses, `reconnectSignal.overrideWith(ConnectivitySignal.new)`
  and `syncTicker.overrideWith(<your ticker>)`.

**The Dio**, with the guard last because it goes first:

```dart
// lib/dio.dart
import 'package:dio/dio.dart';
import 'package:fespalier/fespalier.dart';
import 'package:fespalier_cratestack/dio.dart';
import 'package:fespalier_dio/fespalier_dio.dart';

final dio = Provider<Dio>((ref) {
  final dio = Dio(BaseOptions(baseUrl: 'https://api.example.com'))
    ..interceptors.addAll(const [CrateStackCancelInterceptor(), CrateStackPortalInterceptor()]);
  WriteGuard.install(dio); // last: it goes first (fespalier_dio)
  ref.onDispose(dio.close);
  return dio;
});
```

```yaml
# pubspec.yaml dependencies
  dio: ^5.7.0
```

- **`CrateStackCancelInterceptor`** is what makes a page that went away stop its requests (section 4).
- **`CrateStackPortalInterceptor`** rejects a `text/html` response as an error that `DioFailures.read` reads as
  **offline**: Dio does not throw on a `200`, so without it a captive portal's page reaches the generated client, which
  cannot decode it, and no reader knows what it threw.
- **`WriteGuard`** keeps a retrier from sending a write twice. The generated RPC reads are **POSTs**, so it counts them
  as writes and a Dio retry policy never repeats them. That is what you want (section 6).
- The root `layout.dart` does `ref.watch(autoSync)` once (a sample is in `fespalier-offline`), and a sign-out calls
  `ref.read(crateStackAccount).clear()` **before** the session ends (`fespalier-guards`,
  [`auth-package.md`](../fespalier-guards/SKILL.md) (its `auth-package.md` page)).

## 4. Reads: `data.dart` with `ref.cancellable`

```dart
// lib/shop_client.dart
import 'package:fespalier/fespalier.dart';
import 'package:my_app/dio.dart';

/// A STAND-IN for your generated package (shop_client): its client has these shapes, over the Dio of dio.dart.
class Order {
  const Order(this.id, this.status, this.version);

  factory Order.fromMap(Map<String, Object?> map) =>
      Order(map['id']! as int, map['status']! as String, map['version']! as int);

  final int id;
  final String status;
  final int version;

  Map<String, Object?> toMap() => {'id': id, 'status': status, 'version': version};
}

class ShopClient {
  const ShopClient(this.models);

  final ShopModels models;
}

class ShopModels {
  const ShopModels(this.order);

  final OrderModel order;
}

class OrderModel {
  const OrderModel();

  Future<List<Order>> list() async => const [];
}

final shopClientProvider = Provider<ShopClient>((ref) {
  ref.watch(dio); // the generated client is built over this Dio
  return const ShopClient(ShopModels(OrderModel()));
});
```

```dart
// lib/app/orders/data.dart
import 'dart:async';

import 'package:fespalier/fespalier.dart';
import 'package:fespalier_cratestack/dio.dart';
import 'package:fespalier_cratestack/fespalier_cratestack.dart';
import 'package:my_app/shop_client.dart';

/// Loaded again when a minute old and the app resumes or the network comes back.
const freshness = Freshness(staleTime: Duration(minutes: 1), refetchOnResume: true, refetchOnReconnect: true);

final _codec = ServedCodec<List<Order>>(
  toJson: (orders) => [for (final o in orders) o.toMap()],
  fromJson: (json) => [for (final m in json! as List<Object?>) Order.fromMap(m! as Map<String, Object?>)],
);

/// The server's orders; offline, the last ones this account loaded here (Served says which, and when).
FutureOr<Served<List<Order>>> data(Ref ref) => ref.serve(
  key: 'orders',
  codec: _codec,
  empty: () => const [],
  fetch: () {
    final client = ref.watch(shopClientProvider); // BEFORE cancellable: watch and read other providers first
    return ref.cancellable(() => client.models.order.list()); // the body is only the client call
  },
);
```

```dart
// lib/app/orders/page.dart
import 'package:fespalier_cratestack/fespalier_cratestack.dart';
import 'package:flutter/material.dart';
import 'package:my_app/shop_client.dart';

class OrdersPage extends StatelessWidget {
  const OrdersPage(this.orders, {super.key});

  final Served<List<Order>> orders; // spelled exactly as data() returns it

  @override
  Widget build(BuildContext context) => Column(
    children: [
      if (orders.source == ServedFrom.local) const Text('Offline copy'),
      for (final o in orders.value) Text('Order ${o.id}: ${o.status}'),
    ],
  );
}
```

- **`ref.cancellable` stops the request with the provider.** The generated options carry no cancel token, so the token
  travels in a **zone value** that `CrateStackCancelInterceptor` picks up. Call it **before the first `await`**. The body
  must be **only the client call**: a provider built _inside_ it runs in the same zone, so its own requests would take
  this provider's token and be cancelled with it (the symptom: another page's request is cancelled).
- **`freshness` decides _when_ a read runs again, `serve` _where_ the answer comes from.** Do not combine `serve` with
  `dataCache`.
- **The default `invalidates` of an action reloads `data` after any outcome**, `Queued` included. That is harmless: the
  read stays as the server says, and the "cancelling" overlay comes from `pendingIntents`.
- To read a generated provider with **no offline fallback**, select it as fespalier says
  (`ProviderListenable<AsyncValue<Order>> data(Ref ref, {required int id}) => orderProvider(id)`).

## 5. Actions are intents

```dart
// lib/app/orders/action.dart
import 'package:fespalier/fespalier.dart';
import 'package:fespalier_cratestack/fespalier_cratestack.dart';
import 'package:my_app/shop_client.dart';

typedef CancelInput = ({int orderId, int expectedVersion});

/// Cancelling is the server's decision: queued offline, sent with an idempotency key, decided once.
/// It never claims the order is cancelled before the server says so.
Future<IntentOutcome<Order>> cancel(Ref ref, {required CancelInput input}) => ref
    .read(intentQueue)
    .submit(
      // Your generated args: CancelOrderArgs(id: ..., expectedVersion: ...).toWire()
      RpcCall('cancelOrder', {'id': input.orderId, 'expectedVersion': input.expectedVersion}),
      subject: 'order:${input.orderId}',
      touches: const {'orders'},
      decode: (output) => Order.fromMap(output! as Map<String, Object?>),
    )
    .withCrateStackFieldErrors(ref);
```

`submit` returns `Accepted` or `Queued`; a refusal on the spot is thrown and nothing is kept; the call must be
JSON-native; a subject is ordered (`fespalier-offline`, [`fespalier-offline`](../fespalier-offline/SKILL.md) (its `intents.md` page)).
`withCrateStackFieldErrors(ref, fieldName: ...)` turns a `422` `VALIDATION_ERROR` into `FieldErrors`; the shape of
`details` is an **assumption** (CrateStack documents the message, not a structure).

## 6. Retries: one layer

Riverpod's data retry is the **one** retry layer for reads. A Dio retrier on top multiplies it (the two retry layers
multiply, `fespalier-data`, [`http.md`](../fespalier-data/SKILL.md) (its `http.md` page)), and generated RPC reads are POSTs that
`WriteGuard` refuses to repeat anyway. An intent has its own, slower retry: the next sync. Nothing here sleeps or backs
off with a timer.

## 7. Golden rules

- **The server must namespace idempotency keys by a verified principal.** The key is stored per namespace: the verified
  principal, else a hash of the `Authorization` header, else the peer address. With the `Authorization` fallback **a
  token refresh between two attempts changes the namespace**, so the replay of a call whose answer was lost is a new
  request and runs the call a second time. `fespalier_auth` refreshes lazily and a `401` keeps the same key, so this
  does happen. Configure the server's idempotency layer for the verified principal (the docs call it the first choice
  since CrateStack 0.14.0), and **do not queue a call whose double run matters against a server that cannot**. Details
  in [`references/server-contract.md`](references/server-contract.md).
- **`crateStackScope` must be the signed-in account**, and the sign-out wipe runs first (`fespalier-offline`).
- **Only intents and the row sync use `crateStackTransport`**; online reads keep using the generated client directly.
- **`HiveLocalStore.open` needs a directory off the web**, a folder the system does not empty (the application support
  directory, not a cache directory).

## A transport that signs each attempt

When the server verifies a signature on every request, the signing goes **inside `CrateStackTransport.send`**, once per
attempt, and nowhere earlier. An intent stores the call as JSON and sends it from the store on every attempt, so each
attempt must be a new message (a fresh issue time and nonce, or the server's replay check refuses the second one) over the
same payload under the same `Idempotency-Key` (which a signature can bind). `examples/cose` is the worked case: a
COSE_Sign1 transport with a device key from `fespalier_sign_keypair`, a Rust CrateStack server that checks it, and an
end-to-end test that starts the server's binary.

- **An unsigned `401` is `CrateStackUnauthenticated`**: the intent stays pending under the same key. Do not turn it into a
  retry inside the transport.
- **Only a sealed answer is the server's word.** An unsigned answer is believed for the refusals the envelope layer makes
  before the handler runs, by status alone and with its body ignored: `401` is `Unauthenticated`, `400`, `413`, `415` and
  `426` are `Refused` (code `HTTP_<status>`). **Every other unsigned answer is `CrateStackOffline`, same key**: a `5xx` would
  otherwise move the intent to the next key (the layer answers an unsigned `500` after the handler ran when it cannot seal),
  and a `409` or a `4xx` with a code chosen by whoever is on the path would drop it.
- **A sealed answer that does not open is `CrateStackOffline`, never `CrateStackUnavailable`.** The write may have landed;
  `Unavailable` moves the intent to the next key and risks a second write.
- **A read is still `ref.serve`**: only `CrateStackOffline` serves the copy, and a `401` is the answer.
- The key is registered by a plain call before the first signed one (a request signed by an unknown key is a `401`). The
  transport's `beforeSigned` hook runs before **every** signed call (the example's registrar makes the registration happen
  once, and `onUnauthenticated` forgets it after an unsigned `401`); whatever the hook throws is `CrateStackOffline`, same
  key, because the call was never sent.
- A server must answer the refusals it makes from the headers (a content type, a contract selector) as answers: read the
  body first, or the connection is closed with it unread and the client sometimes sees the reset before the answer (a
  `426` as `Offline`). `examples/cose/server` does, and its README says how it was measured.
- The server's `IdempotencyLayer` goes **inside** the envelope layer: it then hashes the plain CBOR (the same on every
  attempt, whatever the signature) and takes the verified device as its principal, and the replay is sealed anew.

This is not the "signed intents" below: a proof stored with a queued call, tied to the moment it was made.

## Messages and symptoms

The package's debug messages and what each one means are catalogued in
[`fespalier-troubleshooting`](../fespalier-troubleshooting/SKILL.md) (its `diagnostics-cratestack.md` page); the main ones:
`UnimplementedError: fespalier_cratestack: override crateStackTransport ...` (an intent or sync ran with no transport:
override it in `startup()`), `StateError: fespalier_cratestack: crateStackScope is null ...` (a `submit` or `OwnedRows`
call while signed out), `CrateStackNoLocalData` in `error.dart` (a single-row read with no answer and nothing stored), a
queued intent that never sends (no trigger runs: watch `autoSync`), and a call that ran twice after a token refresh (the
namespace rule above).

## Not built

Signed intents, paging helpers beyond `RowSync`'s cursor loop, sync telemetry spans (a data read through `serve` and an
action that calls `submit` already run inside fespalier's data and action spans; a sync span is planned as a custom op
(`TelemetryOp.custom`, since 0.11.0, named `fespalier.cratestack.sync`; no new `TelemetryOp` value, so no exhaustive sink breaks), and nothing from an intent, a row, a subject or a server message would ever be sent), and a background
isolate.

## References

| Need                                                                                                  | Page                                                             |
| ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| The whole `startup()`, the Dio, the root layout, sign-out, `path_provider`, the web                   | [`references/wiring.md`](references/wiring.md)                   |
| What the server's idempotency layer guarantees, the answer table, what `RowSync`'s procedures must do | [`references/server-contract.md`](references/server-contract.md) |
| Where CrateStack's embedded SQLite mode fits and where it does not                                    | [`references/embedded-mode.md`](references/embedded-mode.md)     |
| Reads, intents, owned rows, sync, testing                                                             | [`fespalier-offline`](../fespalier-offline/SKILL.md)             |
| A transport that signs every request and a server that checks it, end to end                          | [`examples/cose`](../../examples/cose/README.md)                 |
| What a call costs in bytes as JSON, CBOR and `COSE_Sign1` CBOR, counted in process (no socket)        | [`examples/wire-sizes`](../../examples/wire-sizes/README.md)     |

## Where the code is

`packages/fespalier_cratestack/lib/`: `fespalier_cratestack.dart`, `dio.dart` (`src/dio/cancel.dart`, `portal.dart`,
`failures.dart`), `hive.dart`, `testing.dart`, and `src/transport.dart` (`CrateStackTransport`, `RpcCall`, `RestCall`,
`crateStackTransport`). The guide is
[`docs/cratestack.md`](https://github.com/fespalier/fespalier/blob/main/docs/cratestack.md).

`examples/offline` (in the fespalier repository) is the wiring without a CrateStack server to start: `lib/wiring.dart`
overrides the transport, the error reader (`lib/errors.dart`), `crateStackScope` and the `RowSync`, over a demo server
in process that plays the part of the generated client.
