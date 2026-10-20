---
name: fespalier-images
description: "Responsive CDN images in a fespalier app with fespalier_image (since 0.9.0) — ResponsiveImage (the width bucket from the box and the device pixel ratio, aspectRatio, the latch, placeholders and errors), imageCdnProvider in startup(), the URL builders (imgproxy and EmgR, Cloudinary, imgix, Thumbor, a template, a srcset), signing without a key in the app, precaching behind a RouteLink, hero flights, the web and CORS, caching, FakeImages in tests and image spans. Load before showing a network image, configuring an image CDN, signing image URLs, or when an image flickers, loads twice, is blurry or fails on the web."
---

# fespalier-images

> **Verified against fespalier `589cf391` (2026-10-08), release v0.13.0.**
> These skills ship in the fespalier repository, and CI checks them against its code
> on every change. Version-sensitive claims say the release they became true in; if
> your app pins another fespalier, trust that release's code over this page. See
> [Versions](https://github.com/fespalier/fespalier/blob/main/skills/README.md#versions).

**Since 0.9.0.** `package:fespalier_image` shows a network image at the size its layout needs: a
`ResponsiveImage` measures its box, multiplies by the device pixel ratio, rounds **up to one of a few widths**
(a bucket) and asks the app's image CDN for that one. The CDN, and the URL it writes, is the app's choice:
imgproxy and EmgR, Cloudinary, imgix, Thumbor, a URL template, or a srcset the backend already signed. It adds
no file kind, no `fespalier:` key and no `fsp` command, and `app.g.dart` is the same bytes: an app that does
not depend on it has none of it.

## Install

```yaml
# pubspec.yaml: the same url and the same ref as fespalier, or pub refuses to resolve
dependencies:
  fespalier:
    git:
      url: https://github.com/fespalier/fespalier
      path: packages/fespalier
      ref: <the tag of your fespalier>
  fespalier_image:
    git:
      url: https://github.com/fespalier/fespalier
      path: packages/fespalier_image
      ref: <the same tag>
```

(A fragment, not a sample: pub resolves the pair only at a release tag. Write `ref: v…` with a real tag in an
app, but never in these pages, where `cli/tests/versions.rs` would read it as fespalier's own version.)
Dart 3.9 and Flutter 3.35 or newer; no plugin; nothing in `pubspec.yaml`'s `fespalier:` section.

## The shape of it

```dart
// lib/images.dart
import 'package:fespalier_image/fespalier_image.dart';

/// Product photos from an EmgR on this computer, unsigned (development): a production app has its backend
/// sign them (see references/signing.md).
const shopImages = ImageCdn(
  builder: ImgproxyUrlBuilder.emgr(
    baseUrl: 'http://localhost:13001',
    sourceBase: 'https://images.example.com/',
  ),
);
```

```dart
// lib/app/startup.dart
import 'package:fespalier/startup.dart';
import 'package:fespalier_image/fespalier_image.dart';
import 'package:my_app/images.dart';

Future<List<Override>> startup() async => [imageCdnProvider.overrideWithValue(shopImages)];
```

```dart
// lib/app/page.dart
import 'package:fespalier_image/fespalier_image.dart';
import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) => const Scaffold(
    body: Center(child: ResponsiveImage('products/3.jpg', width: 160, aspectRatio: 1)),
  );
}
```

`imageCdnProvider` holds an `ImageCdn`: the `builder`, the `buckets` (Next.js 16's `32 … 3840`), the `format`
(`webp`), the `quality`, `maxPixelRatio` (3), a `providerFactory` (a disk cache goes here), `webHtmlElementStrategy` (`never`) and the defaults
of the placeholder, the error view and the fade. Every argument of `ResponsiveImage` overrides the CDN's for
that image. Without an override the provider holds `const ImageCdn()`, which is **no CDN**: a source is a URL,
fetched as it is. A nested `ProviderScope` can override it for a subtree.

The width needed is `(logical × min(devicePixelRatio, maxPixelRatio) − 0.5).ceil()`, then the smallest bucket
at least that wide (the largest when none is): 40 points at 3× is 120 pixels, bucket **128**; 160 points at 3×
is 480, bucket **640**. `references/builders.md` has every builder's URL, `references/signing.md` the key
question, and `references/integration.md` precache, heroes, the web, caching, testing and telemetry.

## The golden rules

1. **Never a key in the app.** `fespalier_image` has no parameter for a signing key or a salt and ships no
   HMAC code, on purpose: a key in a binary, in `main.dart.js` or in a `--dart-define` is public, and turns
   the resizer into an open proxy. The backend returns signed URLs (a srcset, `SrcsetUrlBuilder`), or the
   server runs unsigned with source and option allowlists and presets only, or a `signer:` looks signatures
   up. Never write an HMAC into `signer:`. ([`references/signing.md`](references/signing.md).)
2. **Give the shape with `aspectRatio`** (a design constant: 1, 4/3, 16/9), or a `width` and a `height`. The
   server then crops, and the CDN caches one URL per bucket. Without it the request is width-only and `fit`
   crops on the device. A ratio measured from the box would make a URL per pixel of padding.
3. **Precache at the page's size, with a shared constant.** In the link, `onPreload: (context) => ResponsiveImage.precache(context, p.image, width: pagePhotoSize, aspectRatio: 1)`: the page then has its image in its first frame. Buckets absorb a few points of padding; a constant that both sides use makes the two URLs equal. (`onPreload` is since 0.9.0; without a link, call `precache` before `route.go(context)`. [`references/integration.md`](references/integration.md).)
4. **`route.imageHero(name, child: ResponsiveImage(...))` for a hero**, on both pages (or
   `Heroes(shuttle: ResponsiveImage.flightShuttle)` in `transition.dart`). Without the flight shuttle
   Flutter's default measures the image at every size of the flight.
5. **`FakeImages` in every test that shows an image**, in `pumpRouter(overrides:)` and in
   `test/routes/setup.dart`'s `overrides(pattern)`. Without it the test goes through flutter_test's fake
   `HttpClient` (400s and a warning) and, with no CDN, prints the "not a URL" message.
6. **Name a format.** `ImageFormat.webp` is the default and Flutter decodes it everywhere. `ImageFormat.auto`
   lets the CDN choose from an `Accept` header Flutter cannot steer, so it can answer an AVIF the platform
   does not decode.

## The traps

- **An unconfigured app fetches `products/3.jpg` as a URL**, fails as a network error, and prints once in a debug build: `fespalier_image: "products/3.jpg" is not a URL and no image CDN is configured, so it is fetched as it is. Override imageCdnProvider in startup() (docs/responsive-images.md, "Images").` The fix is the `startup()` override.
- **It chooses once and only grows.** An animated box (`AnimatedSize`, a hero) asks for one width; a smaller
  box never asks again (a change of the view's size or of the device pixel ratio also grows it). For a box that really should get a sharper image as it grows, `growWithBox: true`.
  "It loads twice" is a box that grew with `growWithBox`, or a precache at another width than the page
  (a different bucket: say it with one constant).
- **While a variant loads it shows the widest loaded one of the same picture**, not the placeholder: a
  thumbnail on screen stands in for the large image. That is "loaded" in Flutter's `ImageCache`, so it needs a
  provider whose key is available synchronously (`NetworkImage`'s is).
- **`LayoutBuilder` and intrinsics.** Without a `width` the widget measures with a `LayoutBuilder`, which
  throws inside `IntrinsicHeight` and `IntrinsicWidth`: give it a `width`.
- **CORS on the web.** CanvasKit and skwasm fetch the bytes with XHR: the image server must send
  `Access-Control-Allow-Origin` on the image **and on a redirect's target** (EmgR redirects to its
  `CDN_BASE_URL`). A blank image on the web and fine elsewhere is this.
- **EmgR is not imgproxy.** An unsigned URL says `unsigned` (and the server needs `ALLOW_UNSIGNED_REQUESTS`),
  `g:` is grayscale and gravity is `gr:`, a plain source ends in `.png` and not `@png`. `ImgproxyUrlBuilder.emgr`
  has them right; the plain constructor is imgproxy's.
- **A `403` from EmgR** is `unsigned` against a server that has not allowed it, or a signature over another
  path than the URL's (the signer gets the path after the signature, leading `/` included).
- **Telemetry never has the URL.** Image spans (since 0.9.0) carry the builder's name, the width, whether a
  precache started the load and the HTTP status of a failure, never the URL, the source or a signature. A sink
  that switches exhaustively over `TelemetryOp` needs an `image` case.
- **No disk cache** off the web by default: `dart:io` has no HTTP cache, so a restart downloads again.
  `providerFactory` takes `CachedNetworkImageProvider.new` (the app adds the dependency).

## What it does not do

No wrapping of `cached_network_image`, `extended_image` or a CDN's SDK (plug one in through
`providerFactory`); no signing key and no HMAC; no imgproxy source encryption (`enc/`), no Cloudinary token
authentication; no typed gravity or focal point (the CDNs disagree: use `extra:`); no blurhash or low-quality
placeholder (`placeholder:` can show one an app already has); no asynchronous signer in the widget (a signing
endpoint belongs in `data.dart`); no `fsp` lint for a raw `Image.network` and no generated precache.

## Where the code is

`packages/fespalier_image/`: `lib/src/responsive_image.dart` (the widget, `precache`, the flight shuttle),
`cdn.dart` (`ImageCdn`, `imageCdnProvider`), `buckets.dart`, `request.dart`, `builder.dart` and
`builders/` (one file per CDN), `variants.dart` (the loaded-variant registry), `warnings.dart` (the debug-only "not a URL" message and the reported builder errors), `heroes.dart`
(`imageHero`), `telemetry.dart` (the image span), and `lib/testing.dart` (`FakeImages`). The tests pin each
builder's URL against the providers' published examples (`test/builders_test.dart`, `signing_test.dart`).
`examples/shop` shows the product photos through EmgR, with a precache behind each row's link and an image
hero.
