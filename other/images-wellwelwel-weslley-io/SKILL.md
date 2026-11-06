---
name: images
description: Responsive image generation and audit through a deterministic hook. It encodes every declared master into AVIF and WebP at the widths devices actually render, detects drift between masters and their generated variants, and pairs with the Picture component so pages serve the smallest fitting source. Use when adding, changing, or auditing raster images.
user-invocable: true
metadata:
  author: Weslley Araújo
  version: '1.0.0'
---

# Responsive images

This skill owns how raster images reach the browser. Masters stay the only edited files, and everything a device downloads is derived from them by the hook: modern formats at a ladder of widths, a catalog the Picture component reads to build its sources, and a lock that ties the generated set to the exact master bytes that produced it.

## Generate, never hand-export

Every derived image comes from the hook, so the whole set is reproducible from the masters and the manifest alone. A claim that an image is optimized is a verdict printed by the hook, not an impression from a file listing. When a master or the recipe that encoded it changes, the lock stops matching and the drift is a failing check, never a silent regression.

## When to use it

Reach for it when a raster image enters the project, when a master is edited or replaced, when a page ships more image bytes than its layout can display, and as a gate before releasing a change that touches images. Vector files are out of scope, since they already scale.

## How it works

The manifest declares each master, the widths its usages need, and whether its group encodes lossless. A build encodes every declared master into AVIF and WebP at those widths, writes the variants beside the master named by width, content stamp, and format, refreshes the catalog that maps each public path to its ladder, stamp, and intrinsic size, and records the master's hash and encode recipe in the lock. The stamp derives from the master bytes and the recipe, so any change also changes every variant URL, no cache can keep serving old bytes, and the build removes the variants a previous recipe produced. Verify replays that contract read-only and fails on any divergence. Scan inventories every raster under the static assets, heaviest first, and marks the ones the manifest does not cover.

On the page, the Picture component looks the image up in the catalog. A covered image renders as a picture element offering AVIF and WebP ladders with the master as fallback. An uncovered image renders as a plain img, so adopting it is never a breaking change.

## Conventions

- Widths come from the rendered size multiplied by the device pixel ratios worth serving, never from the master's own size. Small flat art lists those products exactly, so the browser picks a one-to-one source and never resamples what the hook already resized once.
- Photographic and soft content compresses lossy at the default qualities. Flat-color art (logos, icons, badges with text) declares lossless in its group, since hard edges are exactly where lossy artifacts live.
- The ladder never upscales: a width above the master clamps to the master, and the srcset only declares real pixels.
- The caller passes a sizes attribute describing the slot the layout gives the image, since only the call site knows it.
- The layout owns the rendered size through its own styles, on both axes or one axis plus a CSS aspect ratio. The component writes no dimension attributes, because a height hint sets a used height that defeats a CSS aspect ratio, and the catalog records each master's intrinsic size instead.
- Images below the fold or outside the first viewport load lazily, and only the likely largest contentful paint carries a high fetch priority.
- Generated variants, the catalog, and the lock are committed, so a build is reproducible without re-encoding and a stale set fails verification anywhere.

## Dependencies

The hook needs `sharp`. Check it with `npm ls sharp` and install it as a development dependency with the package manager the root lockfile points to when it is missing.

## Running it

The hook lives in the project, at `tools/images.ts`, and is exposed as npm scripts:

```sh
npm run images:scan
npm run images:build
npm run images:verify
```

| Flag         | Purpose                                                        |
| ------------ | -------------------------------------------------------------- |
| `--manifest` | Manifest to read, `tools/images.json` by default               |
| `--dir`      | Directory `scan` walks, the static assets directory by default |

## Verdicts

| Command  | Verdicts                                                                                  |
| -------- | ----------------------------------------------------------------------------------------- |
| `build`  | `built` when variants were encoded, `fresh` when the lock already matched                 |
| `verify` | `ok`, `stale` on hash mismatch, `missing` on absent files, `orphan` for lock leftovers    |
| `scan`   | `managed` when the manifest covers the file, `unmanaged` when it does not, heaviest first |

`verify` exits non-zero on anything but `ok`, and `build` and `scan` exit non-zero only on failure, so both gates fit CI unchanged.
