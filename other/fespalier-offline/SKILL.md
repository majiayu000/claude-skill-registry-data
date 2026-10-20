---
name: fespalier-offline
description: "Offline-first fespalier apps (since 0.10.0, the pure-Dart core of fespalier_cratestack) — deciding what a write is (a row the user owns, merged field by field; a decision only the server makes, queued as an intent; or online-only), reads through ref.serve with Served (network or local, fetchedAt, stale, neverFetched) and the networkFirst, cacheFirst, localOnly and serverOnly policies, the IntentQueue (submit, Accepted or Queued, idempotency keys, per-subject order, pendingIntents for a waiting banner), OwnedRows with a hybrid logical clock and RowSync, SyncEngine and autoSync with the start, resume, reconnect and tick triggers, LocalStore and ReadCache, the sign-out wipe, and testing offline. Load before making a screen or a write work without a network, adding sync, an offline banner or a pending-changes indicator, or when a queued change never sends, sends twice or shows success too early."
---

# fespalier-offline

> **Verified against fespalier `589cf391` (2026-10-08), release v0.13.0.**
> These skills ship in the fespalier repository, and CI checks them against its code
> on every change. Version-sensitive claims say the release they became true in; if
> your app pins another fespalier, trust that release's code over this page. See
> [Versions](https://github.com/fespalier/fespalier/blob/main/skills/README.md#versions).

**Since 0.10.0.** An app that keeps working without a network: what is read from the device, what is written locally,
and what must wait for the server. The code is `package:fespalier_cratestack/fespalier_cratestack.dart`, and **its
core is pure Dart that does not depend on CrateStack**: the only backend seam is `CrateStackTransport`, which sends a
`RpcCall` or a `RestCall`. Wiring a CrateStack client into it is
[`fespalier-cratestack`](../fespalier-cratestack/SKILL.md). It adds no file kind, no `fespalier:` key and no `fsp`
command, and `app.g.dart` is the same bytes; an app that does not depend on it has none of it. The install block is
that skill's.

## Decide first: what is this write?

|                 | Rows a user **owns**                   | **Decisions** only the server makes                                    |
| --------------- | -------------------------------------- | ---------------------------------------------------------------------- |
| Examples        | a note, a draft, a to-do, a setting    | cancel an order, accept an invitation, transfer a balance              |
| Written         | on the device at once, offline or not  | as an **intent**: saved, sent, and decided by the server               |
| Conflicts       | merged field by field, nobody is asked | the server answers, the person resolves a conflict                     |
| The page shows  | the new value immediately              | "will send when back online", never a success the server has not given |
| In this package | `OwnedRows`, `RowSync`                 | `IntentQueue`                                                          |

A third kind is **online-only, on purpose**: a one-time code, a stock reservation, anything that has to be answered
now. Do not queue it; a call that fails when there is no network is a feature.

## Reads: `ref.serve` and `Served`

The sample is one small app: a domain type, a client, a read, a page and a write. (`shopClient` stands for whatever
reaches your server, a generated CrateStack client included.)

```dart
// lib/shop.dart
import 'package:fespalier/fespalier.dart';

class Order {
  const Order(this.id, this.status, this.version);

  factory Order.fromMap(Map<String, Object?> map) =>
      Order(map['id']! as int, map['status']! as String, map['version']! as int);

  final int id;
  final String status;
  final int version;

  Map<String, Object?> toMap() => {'id': id, 'status': status, 'version': version};
}

abstract class ShopClient {
  Future<List<Order>> orders();
}

final shopClient = Provider<ShopClient>((ref) => throw UnimplementedError('override shopClient in startup()'));
```

```dart
// lib/app/orders/data.dart
import 'dart:async';

import 'package:fespalier/fespalier.dart';
import 'package:fespalier_cratestack/fespalier_cratestack.dart';
import 'package:my_app/shop.dart';

final _codec = ServedCodec<List<Order>>(
  toJson: (orders) => [for (final o in orders) o.toMap()],
  fromJson: (json) => [for (final m in json! as List<Object?>) Order.fromMap(m! as Map<String, Object?>)],
);

/// The server's orders; offline, the last ones this account loaded here (Served says which, and when).
FutureOr<Served<List<Order>>> data(Ref ref) => ref.serve(
  key: 'orders',
  codec: _codec,
  empty: () => const [],
  maxAge: const Duration(hours: 1), // drives Served.stale; null: never stale
  fetch: () => ref.read(shopClient).orders(),
);
```

```dart
// lib/app/orders/page.dart
import 'package:fespalier/fespalier.dart';
import 'package:fespalier_cratestack/fespalier_cratestack.dart';
import 'package:flutter/material.dart';
import 'package:my_app/app.g.dart';
import 'package:my_app/shop.dart';

class OrdersPage extends ConsumerWidget {
  // Spelled exactly as data() returns it: fsp matches by type, syntactically.
  const OrdersPage(this.orders, {super.key});

  final Served<List<Order>> orders;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final cancel = OrdersRoute.useCancel(ref);
    final waiting = ref.watch(pendingIntents(null)).value ?? const [];
    return Column(
      children: [
        if (orders.source == ServedFrom.local)
          Text(orders.neverFetched ? 'Offline: not loaded on this phone yet' : 'Offline copy, as of ${orders.fetchedAt}'),
        if (waiting.isNotEmpty) Text('${waiting.length} changes waiting to send'),
        for (final o in orders.value)
          ListTile(
            title: Text('Order ${o.id}: ${o.status}'),
            subtitle: waiting.any((i) => i.subject == 'order:${o.id}') ? const Text('Cancelling, will send when back online') : null,
            trailing: TextButton(
              onPressed: cancel.isPending ? null : () => cancel.call((orderId: o.id, expectedVersion: o.version)),
              child: const Text('Cancel'),
            ),
          ),
      ],
    );
  }
}
```

| Policy                   | Looks first at                                      | Use it for                                        |
| ------------------------ | --------------------------------------------------- | ------------------------------------------------- |
| `networkFirst` (default) | the server, then the device on a connection failure | anything others can change                        |
| `cacheFirst`             | the device, then the server if there is nothing     | data that does not change once saved              |
| `localOnly`              | the device only: the copy an earlier read saved     | data only ever read here (`fetch:` is not needed) |
| `serverOnly`             | the server only; offline is an error, never a guess | what must be current                              |

The rules that keep it honest:

- **Only `CrateStackOffline` falls back.** A refusal (`403`) is the answer and goes to `error.dart` (on a first load): last week's copy
  of something you may no longer see would be a leak. An error no reader in `crateStackErrors` knows is rethrown too. That holds on a route with a `freshness` too (since 0.13.1): `CrateStackRefused` is a `DataRefusal`, so `keepDataOnError` keeps the page for an offline reload but shows `error.dart` instead of the old copy for any refusal (every `4xx` but 401 and 409). Before 0.13.1 the old copy stayed on screen: watch `reconnectSignal` in `data.dart` instead of declaring `freshness` there.
- **An empty list offline is an answer**: `neverFetched` is true, so the page can say "not loaded on this phone yet".
  A **single row** with nothing saved is `CrateStackNoLocalData`, shown by `error.dart` with a retry; pass `empty:` for
  a list only.
- **Every answer is per account.** The scope (`crateStackScope`) is part of every key, so one account's copy never
  reaches another; while nobody is signed in nothing is read or saved.
- **A gateway or a captive portal counts as offline**: an HTML page where JSON was expected, or any `5xx` with no
  CrateStack envelope (since 0.16.0 a bare `500` too: whoever answered may have done so after the commit; before
  0.16.0 only `502`, `503`, `504` and `511`). A `5xx` in the envelope does not (the server did answer). With Dio add
  `CrateStackPortalInterceptor` (`fespalier-cratestack`).
- **`Freshness` says _when_ a read runs again; `serve` says _where_ its answer comes from. Never combine `serve` with
  `dataCache`**: `serve` keeps its own copy, per account.
- Show the time, not the word "stale": `Offline copy, as of 10:42`. `stale` only follows the `maxAge` you pass.

## Writes that are decisions: intents

```dart
// lib/app/orders/action.dart
import 'package:fespalier/fespalier.dart';
import 'package:fespalier_cratestack/fespalier_cratestack.dart';
import 'package:my_app/shop.dart';

typedef CancelInput = ({int orderId, int expectedVersion});

/// Cancelling is the server's decision: queued offline, sent with an idempotency key, decided once.
/// It never claims the order is cancelled before the server says so.
Future<IntentOutcome<Order>> cancel(Ref ref, {required CancelInput input}) => ref.read(intentQueue).submit(
  RpcCall('cancelOrder', {'id': input.orderId, 'expectedVersion': input.expectedVersion}),
  subject: 'order:${input.orderId}',
  touches: const {'orders'},
  decode: (output) => Order.fromMap(output! as Map<String, Object?>),
);
```

`submit` saves the call, sends it once, and returns `Accepted(value)` (the server said yes) or `Queued(intent)` (no
answer: the next sync sends it again); switch over it, there are two cases:

```dart
// a fragment: what the page does with the outcome
switch (out) {
  Accepted(:final value) => showSnack('Order ${value.id} cancelled'),
  Queued() => showSnack('Saved. It will be sent when you are back online'),
}
```

- **Never fake success.** `Accepted` only when the server said yes. The "cancelling..." overlay on a row comes from
  `pendingIntents(subject)` (a `FutureProvider.autoDispose.family<List<Intent>, String?>`: `null` for all), not from
  pretending the order is already cancelled.
- **A stored call.** It is encoded once, saved **before** it is sent, then sent from the saved text every time:
  every attempt is byte-identical, which a server's idempotency check compares. The key is `<id>#<attempt>`; a stored
  failure (a `5xx` in CrateStack's envelope) moves to the next attempt, everything else keeps the key, a bare `5xx`
  included (since 0.16.0).
- **Never expiring**, and **ordered per subject**: an intent waits behind an undecided earlier one with the same
  `subject`, a `submit` behind one is saved and `Queued` **without being sent**. Other subjects do not wait.
- **JSON-native only** (maps, lists, strings, numbers, booleans, `null`): a `DateTime` throws before anything is saved
  and bytes would silently become a list. Convert them to text.
- **A refusal on the spot is thrown and nothing is kept** (the person is on the screen that asked); an error no reader
  knows is kept as `Queued`, because it may have landed. Add a reader to `crateStackErrors` to turn it into a
  decision. `references/intents.md` has the answer table and the statuses.
- **A signed-out `submit` is a `StateError`.** Calls that must work signed out (a sign-in) stay out of the queue.

## Rows the device owns

```dart
// a fragment: a note edited offline
final rows = ref.read(ownedRows);
await rows.edit('notes', 'n1', {'title': 'Groceries', 'body': 'Milk'}); // stamped, saved, dirty
await rows.remove('notes', 'n1'); // a tombstone (deletedAt), a field like any other

// A page reads them locally: synchronous with a synchronous store, so on the first frame.
FutureOr<List<OwnedRow>> data(Ref ref) {
  ref.watch(crateStackRevision('notes')); // an edit or a sync rebuilds the read
  if (ref.watch(crateStackScope) == null) return const []; // signed out: empty, not an error
  return ref.watch(ownedRows).list('notes');
}
```

Each field carries its own hybrid-logical-clock stamp, so two devices that edit different fields both keep their edit
and the same field goes to the greater stamp, on both. `references/owned-rows-and-sync.md` has the merge rules,
`RowSync` (two procedures **you** add to the schema: CrateStack has no sync protocol) and a sample.

## Sync and the triggers

`ref.watch(autoSync)` **once, in the root `layout.dart`**, runs `syncRunner.sync(...)` on four triggers: **start**,
**resume** (`appResumeSignal`), **reconnect** (`reconnectSignal`, which does nothing until `startup()` overrides it with
`ConnectivitySignal.new` from `fespalier_connectivity`) and the app's **tick**. The tick is a signal the package never
fires itself, because it starts no timer: the app owns it.

```dart
// lib/foreground_ticker.dart
import 'dart:async';

import 'package:fespalier/fespalier.dart';

/// Ticks every five minutes while the root layout shows (autoDispose, watched only by autoSync).
class ForegroundTicker extends RefetchSignal {
  @override
  int build() {
    final timer = Timer.periodic(const Duration(minutes: 5), (_) => fire());
    ref.onDispose(timer.cancel);
    return 0;
  }
}
```

```dart
// lib/app/layout.dart
import 'package:fespalier/fespalier.dart';
import 'package:fespalier_cratestack/fespalier_cratestack.dart';
import 'package:flutter/material.dart';

class RootLayout extends ConsumerWidget {
  const RootLayout({super.key, required this.child});

  final Widget child;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final sync = ref.watch(autoSync); // keeps the sync alive; sync.isSyncing and sync.last can drive a banner
    return Column(
      children: [
        if (sync.isSyncing) const LinearProgressIndicator(),
        Expanded(child: child),
      ],
    );
  }
}
```

```dart
// lib/app/startup.dart
import 'package:fespalier/fespalier.dart' show reconnectSignal;
import 'package:fespalier/startup.dart';
import 'package:fespalier_connectivity/fespalier_connectivity.dart';
import 'package:fespalier_cratestack/fespalier_cratestack.dart';
import 'package:my_app/foreground_ticker.dart';

Future<List<Override>> startup() async => [
  reconnectSignal.overrideWith(ConnectivitySignal.new), // fespalier_connectivity
  syncTicker.overrideWith(ForegroundTicker.new), // the app's own timer
];
```

- A sync does **push the dirty rows, pull each collection, then drain the intents**, in that order (an intent may name
  a row made offline). The drain runs even if the push failed and stops at the first sign of no network.
- **Single flight** (a sync that starts while another runs joins it) and a **`minInterval` of 10 seconds**: a signal
  within it of the last sync that reached the server does nothing unless the last found no network or work was queued
  since. A manual sync and the first one at start always run. **A sync never throws**: its `SyncReport` has `failure`,
  `pushed`, `pulled`, `rolledBack` and the drain's `DrainReport`.
- **Save locally, then sync best-effort**: an action edits the row, calls `engine.sync(SyncReason.manual)` and ignores
  the failure. **Push before a server decision that names a local row**: `await ref.read(syncEngine).push()` throws when
  it fails, where `sync` does not, so you do not send a decision about a row the server has never seen. The report of a sync an action starts does not reach `autoSync`'s state, so its `rolledBack` is not shown by a banner on `autoSync` alone: keep it yourself (`examples/offline`'s `lastSync` notifier).

## Golden rules and traps

- **The sign-out wipe.** `ref.read(crateStackAccount).clear()` removes the account's intents, rows, cursors and cached
  reads, and **must run before `signOut()`**: sending one account's intent under another's session is worse than
  losing it. `fespalier_auth`'s sign-out flips synchronously, so `crateStackScope` is already null afterwards and a
  late `clear()` does nothing: then pass the account you left, `clear(scope: leavingId)`.
- **`LocalStore` is not a `fespalier_storage` storage.** Those evict the entries written longest ago; an intent never
  expires and an unpushed row is the only copy of an edit. `HiveLocalStore` (`package:fespalier_cratestack/hive.dart`)
  never evicts; `InMemoryLocalStore` is the default, **and loses every queued intent at exit**. `ReadCache.storage(...)`
  may sit on a budgeted storage, with its key list in the `LocalStore` (`index:`).
- **`Intent` is also Flutter's `Intent`.** A file that imports `package:flutter/material.dart` and this package and names
  `Intent` gets `ambiguous_import`: `import 'package:flutter/material.dart' hide Intent;`.
- **Nothing the server said is stored or reported**: a refusal keeps its wire code only, never its message or `details`
  (they may quote values).
- **No timers, no background isolate.** Sync runs while the app is open; a `testWidgets` that ends with a timer pending
  is your own ticker.
- **Not built:** signed intents (a queued call cannot carry a proof tied to the moment it was made: keep those calls
  online-only; a `CrateStackTransport` that seals each attempt when `send` runs is another thing and works, see
  `examples/cose`), paging helpers beyond `RowSync`'s cursor loop, a background sync, sync telemetry spans. On the web use
  `InMemoryLocalStore` (nothing outlives the tab) or `HiveLocalStore` on IndexedDB.

## References

| Need                                                                                      | Page                                                                                                        |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `serve`'s parameters, `ReadCache`, `Served`, the portal and gateway rules                 | [`references/reads.md`](references/reads.md)                                                                |
| The answer table, statuses, `discard`, `drain`, field errors, the sign-out wipe           | [`references/intents.md`](references/intents.md)                                                            |
| The clock, per-field merge, writing a `RowSync`, `SyncEngine` and the triggers            | [`references/owned-rows-and-sync.md`](references/owned-rows-and-sync.md)                                    |
| `FakeCrateStackTransport`, `FakeRowServer`, `ManualSyncTicker`, `crateStackTestOverrides` | [`references/testing.md`](references/testing.md)                                                            |
| Wiring a CrateStack client, Dio, the server's idempotency contract                        | [`fespalier-cratestack`](../fespalier-cratestack/SKILL.md)                                                  |
| A signed transport under intents and `ref.serve`, with a server to run it against         | [`examples/cose`](../../examples/cose/README.md)                                                            |
| A message from the package                                                                | [`fespalier-troubleshooting`](../fespalier-troubleshooting/SKILL.md) (its `diagnostics-cratestack.md` page) |

## Where the code is

`packages/fespalier_cratestack/lib/src/`: `served.dart`, `read_cache.dart`, `intent_queue.dart`, `intent.dart`,
`owned_rows.dart`, `lww.dart`, `hlc.dart`, `row_sync.dart`, `sync_engine.dart`, `auto_sync.dart`, `local_store.dart`,
`scope.dart`, `errors.dart`, `transport.dart`; `test/intents_test.dart` pins the answer table and
`test/no_timers_test.dart` greps `lib/` for timers. The guide is
[`docs/offline-first.md`](https://github.com/fespalier/fespalier/blob/main/docs/offline-first.md).

`examples/offline` (in the fespalier repository) is a running app of the sample above: an orders list read with
`ref.serve`, a cancel as an intent, notes as owned rows with a `RowSync`, `autoSync` in the root layout with the app's
own ticker, the sign-out wipe and a switch that plays the network, all on an in-process demo server. Its
`test/support.dart` is `references/testing.md` applied to a whole app.
