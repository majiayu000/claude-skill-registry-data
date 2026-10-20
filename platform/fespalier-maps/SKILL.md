---
name: fespalier-maps
description: "A place picked on a map in a fespalier app with fespalier_maps (since 0.13.0) — a PinPicker body for a page you write (the pin fixed at the centre, the map moving under it), the Geocoder you implement (recipes for Nominatim, Photon and your own backend), the position source over geolocator, MapLibreSurface over maplibre_gl, a name shown as a guess and never as fact, forward search in a field docked at the bottom, a PickedPlace returned through push<PickedPlace>, the fespalier.maps telemetry that never carries a place, and FakeMapSurface, FakeGeocoder and FakePositionSource in tests; and offline MapLibre region packs — RegionPackRequest and its tile estimate, the tilePacks notifier (start, pause, resume within the session, remove, refresh, storage) with a PackStatus per key, MapLibreOfflineTiles over the offline database, a download that does not resume across an app restart, and FakeOfflineTiles; and resumable file packs — FilePackRequest (a PMTiles archive, a URL, a destination path, a size and a sha256), the filePacks notifier (start, pause, resume, remove, refresh, storage) over the packHttpClient the app provides, HTTP Range and If-Range resume after a restart, a partial file moved into place only when checked, pmtilesSourceUrl for a style's source, and FakePackFiles. Load before adding a place or address picker, a map, geolocation, a geocoder, downloaded offline map regions or an offline PMTiles file, or when a picker shows no pin, never asks for the position, confirms nothing, a pack stays Interrupted after a restart, a file download restarts from zero, a pack fails with hashMismatch or rejected, or a test cannot render the map."
---

# fespalier-maps

> **Verified against fespalier `589cf391` (2026-10-08), release v0.13.0.**
> These skills ship in the fespalier repository, and CI checks them against its code
> on every change. Version-sensitive claims say the release they became true in; if
> your app pins another fespalier, trust that release's code over this page. See
> [Versions](https://github.com/fespalier/fespalier/blob/main/skills/README.md#versions).

**Since 0.13.0.** `package:fespalier_maps` is a pin picker that returns a place: the pin is fixed at the centre and the
map moves under it, a search field you place at the bottom finds places, the geocoder's name for the point under the pin
is shown as a **guess**, and confirming pops a `PickedPlace` (the **point is the truth**, the label a courtesy) to the
page that did `await PickPlaceRoute().push<PickedPlace>(context)`. It adds no file kind, no `fespalier:` key and no `fsp`
command, and `app.g.dart` is the same bytes. It cannot add a route (`fsp` scans your `lib/app/`): **you write
`lib/app/pick-place/page.dart`**, whose body is `PinPicker`. A release that predates 0.13.0 has no such package.

## Install

```yaml
# pubspec.yaml: the same url and the same ref as fespalier, or pub refuses to resolve
dependencies:
  fespalier:
    git:
      url: https://github.com/fespalier/fespalier
      path: packages/fespalier
      ref: <the tag of your fespalier>
  fespalier_maps:
    git:
      url: https://github.com/fespalier/fespalier
      path: packages/fespalier_maps
      ref: <the same tag>
```

(A fragment: pub resolves the pair only at a release tag that contains the package, 0.13.0 or later. Write `ref: v…`
with a real tag in an app, but never in these pages, where `cli/tests/versions.rs` would read it as fespalier's own
version. The package's own
[install block](https://github.com/fespalier/fespalier/blob/main/packages/fespalier_maps/README.md#install) is the one
release-please keeps current.) The package brings `maplibre_gl` (`>=0.27.1 <0.28.0`) and `geolocator`
(`>=14.0.0 <15.0.0`), which are platform plugins: the location permission strings (`NSLocationWhenInUseUsageDescription`
in `Info.plist`, `ACCESS_FINE_LOCATION` and `ACCESS_COARSE_LOCATION` in the manifest) and a map **style** you may use are
the app's. Nothing in CI draws a map or builds Android with `maplibre_gl`: a device run is the check.

## The shape of it

Three libraries, so an app links only what it uses, and one rule: **the page is yours, the three widgets in it are yours,
the geocoder is yours.**

| You import                                   | For                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `package:fespalier_maps/fespalier_maps.dart` | `PinPicker`, `PinPickerModel`, `GeoPoint`, `PlaceGuess`, `PickedPlace`, `MapCamera`, `MapBinding`, the seams `Geocoder`, `PositionSource` (`PositionFix`: `Fixed`, `ServiceOff`, `Denied`, `Unavailable`) and `MapSurface`, `tileCount`, `MapsTelemetry`, and the offline packs: `RegionPackRequest`, `tilePacks`, `tilePackStatus`, `TilePacks`, `PackStatus`, `StorageUse`, `OfflineTiles` (provider `offlineTiles`), and the file packs: `FilePackRequest`, `filePacks`, `filePackStatus`, `FilePacks`, `packHttpClient`, `packFileStore`, `PackFileStore`, `pmtilesSourceUrl` |
| `package:fespalier_maps/maplibre.dart`       | `MapLibreSurface` and `MapLibreOfflineTiles`, the one file that imports `maplibre_gl`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `package:fespalier_maps/geolocator.dart`     | `GeolocatorPositionSource`, the one file that imports `geolocator`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `package:fespalier_maps/testing.dart`        | `FakeMapSurface` (`FakeMapMount`, `attachOnMount: false` for a map that exists late), `FakeGeocoder`, `FakePositionSource`, `FakeOfflineTiles`, `FakePackFiles`                                                                                                                                                                                                                                                                                                                                                                                                                   |

The page, the push, the three widgets and a test that runs the whole round trip on fakes are compiled in
[`references/pin-picker.md`](references/pin-picker.md). A geocoder is [`references/geocoders.md`](references/geocoders.md).

## Golden rules

- **A name is a guess.** A geocoder answers with the nearest thing it knows. Show `PinGuess.guess` with its caveat ("Best
  guess"), store `PickedPlace.point`, and never ask the user to type a place that a pin can give. `PickedPlace.guess` is
  null when the geocoder was still asking, knows nothing there or failed: handle null.
- **`PinPicker` is a body.** Put it where the thumb is, as the whole `Scaffold` body (so the keyboard lifts the search
  field with it). The picker lays out your three builders at its bottom edge: `guess`, then `searchField` (with its
  results), then `confirm`. The `confirm` callback is **null** until the pin has a point and the map is at rest: pass it
  straight to a button's `onPressed`.
- **A `MapLibreSurface` is configuration** with value equality (a `const`, a top-level `final`, or one built in `build`),
  shared freely, also by a picker pushed over a picker. Each map it builds belongs to its picker's `MapBinding`: a move made
  for one picker reaches only its map. A new `map:` never makes a new picker: a theme switch (another style) updates the map in place and keeps the pin, guess and position; a surface of another type replaces the map, which opens where the pin is. A new geocoder or locale in a rebuild is fine: the picker keeps its
  model.
- **Nothing opens over the page**: no dialog, no sheet, no menu, no snack bar (the permission prompt is the platform's own).
  A refusal is a value, `PinGuess.fix` (`Denied`, `ServiceOff`, `Unavailable`): render a hint, not an error page.
- **Search is submitted, not typed per keystroke.** `PinSearch.submit` goes on the keyboard's search action. Public
  geocoders forbid search-as-you-type, and the package has no debounce timer. Reverse geocoding asks at most one request at
  a time (the newest rest waits), but the rate limit and the cache are the geocoder's: see `geocoders.md`.
- **The geocoder throws on failure and the picker never shows its text.** `PinSearch.failed` and `PinGuess.failed` are
  flags.

## Traps

- **The pin has no point at first, on purpose.** Until a fix lands, a result is picked or the person moves the map,
  `PinGuess.center` is null and `confirm` is null: the map's first rest, on the whole world, is not a choice. A picker that
  "never enables confirm" is usually one whose position source answered `Denied` or `ServiceOff` and whose person has not
  moved the map; render `PinGuess.fix` to say so.
- **An `initial:` camera turns the position off.** With `initial:` (editing a saved place) the picker starts there and the
  position source is asked only when the person taps "use my location" (`PinSearch.useMyLocation`).
- **The fix moves the map once, when it arrives**, unless the person panned (and came to rest) or picked a result first:
  then their choice stands and the fix is dropped. A rest within about a kilometre of where the map started is taken for the
  map's own (iOS reports a move for any region change) and does not count. "Use my location" always moves the map, even over
  a pan made after tapping it. Not checked on a device: a map's own movement that ends somewhere else (a zoom clamp).
- **Confirming on a page opened with `go` or a link pops nothing** (there is nowhere to go back to) and does not throw; pass
  `onPicked:` for that case.
- **A picked result is not re-geocoded.** `pick` shows the result's label as the guess and the map's rest at that point
  asks the geocoder nothing; a nudge of more than about a metre does.
- **The map's callbacks are the only source of the centre.** A `MapSurface` of your own must key its map by the
  `MapBinding` it is given, call `binding.attach(mover)` when the map exists (and `binding.detach()` when it goes), and
  forward the camera to `binding.move()` when it starts moving and `binding.idle(center)` when it stops; the picker never
  reads the camera itself.
- **The map is a platform view and cannot render in a widget test.** `MapLibreSurface` and `GeolocatorPositionSource` in a
  test reach a platform channel and fail; use the fakes. The default style is MapLibre's **demo** style: use your own tiles
  and their attribution.
- **`GeoBounds` does not check its corners**; a `tileCount` of a rectangle whose south is north of its north is zero rows.
  A `GeoPoint` out of range fails an `assert` in debug only.
- **Telemetry never has a place.** `fespalier.maps.geocode`, `.locate` and `.pick` carry constants and a boolean; if you add
  your own span, keep the coordinate, the label and the query out of it too.

## Offline region packs

`TilePacks` (provider `tilePacks`) downloads MapLibre regions: `start(RegionPackRequest)`, `pause`, `resume`, `remove`,
`refresh`, `storage`; the state is a `PackStatus` per key and `ref.watch(tilePackStatus(key))` reads one. Override
`offlineTiles` once with `MapLibreOfflineTiles()` (no default: reading it unset throws a `StateError` that says so). The
page, the wiring and a test are compiled in [`references/offline-packs.md`](references/offline-packs.md).

- **A MapLibre download does not resume across an app restart.** Pause and resume continue the same download while the app
  stays alive. After a restart `refresh()` finds the region `Interrupted`, and `resume` starts the same definition **again**
  (MapLibre replaces the old region when that download begins; whether stored resources are reused: not checked on a
  device). Say so in the UI ("Download again", not "Resume"). The [file packs](#file-packs-pmtiles) are the resumable kind.
- **Call `refresh()` once** (a packs page opening, or startup): nothing is read before, so a pack from an earlier session is
  `Absent` until then.
- **Progress is provider state**, written from MapLibre's callback: no stream to listen to, no timer. `Downloading` has a
  fraction, **resource** counts (tiles, glyphs, sprites; not tiles) and bytes.
- **`estimatedTiles` is tiles, not bytes**, and `isValid` is false for an antimeridian rectangle or zoom above 22: such a
  `start` ends `Failed(invalidRegion)` without reaching MapLibre.
- **Per-pack bytes overlap** (shared glyphs and edge tiles are counted in each pack) and `StorageUse.onDisk` is the file,
  which also holds the ambient cache: do not add the rows up. `onDisk` is the file `getOfflineDatabasePath` names (null on
  the web).
- **`pause` and `resume` never throw**; `remove` throws only when the database refuses (and the pack is then `Failed`).
  A failure is a `PackFailure` value, never platform text. The web has no offline regions: `Failed(unsupported)`.
- **Telemetry**: `fespalier.maps.download` (`kind=region`; `complete`, `failed` or `cancelled`), never the key, the rectangle
  or the style.
- **One definition is one region** (`maplibre_gl` 0.27): a download deletes the region that already has the same style,
  rectangle and zoom range, at its start (on iOS the new one takes the old id). A re-download that fails has lost the
  pack, and two keys with one definition are refused (`Failed(duplicateRegion)`): give each pack its own rectangle.
- **`refresh()` keeps the complete region of a key** whatever the ids and deletes the others.

## File packs (PMTiles)

`FilePacks` (provider `filePacks`) downloads **one file** over HTTP and, unlike a region, **resumes after the app was closed**:
bytes go to `<destination>.part`, and the next attempt sends `Range: bytes=<size>-` (with `If-Range` and the `ETag` it kept in
`<destination>.part.etag`). The file is renamed to `destination` only when it has the `bytes` and `sha256` of the
`FilePackRequest`, so **a file at the destination is whole and checked**. Wiring, a page, the style and a test are compiled in
[`references/file-packs.md`](references/file-packs.md).

- **`packHttpClient` has no default**: override it with the app's `http.Client` (never closed by the package). `destination` is a
  **path** the app chose (no `path_provider` dependency); `packFileStore` is `dart:io` unless a test gives `FakePackFiles`. The
  web ends `Failed(unsupported)` before any request.
- **Disk is the state of record: `refresh([requests])`** once when the page opens. A file at the destination is `Complete`, a
  `.part` file is `Interrupted(bytes:, progress:)`, and `resume` goes on from the last byte (say "Resume"). The notifier
  can find a pack only through its request; `remove` and `resume` of an earlier session's pack need that `refresh` first.
- **`start` and `resume` complete when the transfer stops**, not when it begins: `unawaited` them in a handler. `pause` aborts the
  request and keeps the partial file (so does `remove`: a stalled connection holds neither, if the app's client honours `http.Abortable`: `IOClient` does, a wrapper such as `RetryClient` must forward `abortTrigger`); they never throw for a failed transfer.
  Without `packHttpClient` the throw is a `ProviderException`.
- **A server that ignores `Range`** answers 200: the transfer restarts from byte 0 (never appended). A 206 with another
  validator than the stored one restarts too, and a partial file with no stored validator and no `sha256` starts from 0. A 416 to a partial file
  restarts once; any other status (404, 403, 5xx) is `Failed(rejected)` with the partial file kept.
- **Failures are values**: `network` (partial file kept, `resume` continues), `rejected`, `sizeMismatch` and `hashMismatch` (the
  partial file is **deleted**), `storage`, `invalidRequest` (two keys with one destination too) and `unsupported`.
- **The newer-archive trap**: a file already at the destination is `Complete` with no request, so a new archive needs a new
  URL and destination, or `remove` first.
- **Drawing**: a style source `{"type": "vector", "url": pmtilesSourceUrl(path)}` (`pmtiles://file:///...`), in the style JSON of
  `MapLibreSurface(styleString:)`. `maplibre_gl` 0.27.1 lists PMTiles sources on Android, iOS and the web; that a local
  `pmtiles://file://` archive draws was **not checked on a device**. An archive holds tiles only: `glyphs` and `sprite` must be
  offline too.
- **Telemetry**: `fespalier.maps.download` with `kind=file`, one operation across pause and resume; never the key, URL, path,
  hash or headers. **No timer or listener**: the body is read with `await for`. `StorageUse.onDisk` of file packs is the sum
  of the files, and the rows add up (unlike regions).

## What it does not do

Markers, routes and overlays, clustering, search-as-you-type, a geocoder of its own, a retry policy with backoff (it
would need a timer: the app calls `resume`), a download that goes on while the app is closed, a key or a secret of any kind, and a web-specific surface (`maplibre_gl` has a web implementation; nothing
here has run on it). It starts no timer and adds no listener of its own.

## References

| Need                                                                                                    | Page                                                             |
| ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| The page, the push, the guess card and search field, the permission states, the test                    | [`references/pin-picker.md`](references/pin-picker.md)           |
| Offline region packs: the request, `tilePacks`, the page, storage, the restart rule, `FakeOfflineTiles` | [`references/offline-packs.md`](references/offline-packs.md)     |
| File packs: the request, the client, resume over Range, integrity, the style source, `FakePackFiles`    | [`references/file-packs.md`](references/file-packs.md)           |
| `Geocoder`: Nominatim (and its usage policy), Photon, your own backend, the locale, failures            | [`references/geocoders.md`](references/geocoders.md)             |
| A page or a navigation question                                                                         | [`fespalier-routing`](../fespalier-routing/SKILL.md)             |
| `pumpRouter` and the traps that hang a test                                                             | [`fespalier-testing`](../fespalier-testing/SKILL.md)             |
| Where telemetry goes and what a sink may carry                                                          | [`fespalier-observability`](../fespalier-observability/SKILL.md) |

## Where the code is

`packages/fespalier_maps/lib/src/`: `geo.dart` (the values), `ports.dart` (`Geocoder`, `PositionFix`, `PositionSource`,
`MapSurface`), `pin_model.dart` (`PinPickerModel`, `PinSearch`, `PinGuess`: the whole behaviour, with no widget),
`pin_picker.dart` (the widget), `telemetry.dart` (`MapsTelemetry`), `tiles.dart` (`tileCount`), `offline/` (`request.dart`,
`status.dart`, `port.dart`, `tile_packs.dart`, `fake.dart`), `files/` (`request.dart`, `store.dart`,
`transfer_adapter.dart` (the store seen as `fespalier_download`'s `TransferFiles`), `file_packs.dart`, `fake.dart`); `lib/maplibre.dart`,
`lib/geolocator.dart`, `lib/testing.dart`; `test/no_timers_test.dart` greps `lib/` for timers, listeners and for anything
that opens a dialog, and `test/telemetry_test.dart` pins the names. The guide is
[`docs/maps.md`](https://github.com/fespalier/fespalier/blob/main/docs/maps.md).

`examples/maps` is the running version (since 0.13.0): `PinPicker` returning a `PickedPlace` to the page that pushed it, a fixed in-app gazetteer as the `Geocoder` (no network), `GeolocatorPositionSource`, and one region pack with progress, pause, resume and delete. Read `test/pick_place_test.dart` for the round trip and the late fix that does not override a pan, and `test/offline_test.dart` for the pack on `FakeOfflineTiles`. A map does not draw in `flutter test`; its README says how to run it on a device.
