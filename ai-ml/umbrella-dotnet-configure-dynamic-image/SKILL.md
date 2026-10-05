---
name: umbrella-dotnet-configure-dynamic-image
description: 'Configure, repair, or audit Umbrella Dynamic Image in ASP.NET Core, Blazor, or Razor applications. Use for analyzer and generator installation, server-only catalogs, external Razor source roots, URL fingerprinting, URL/version-token propagation, middleware mappings, cache policies, generated-variant validation, UWDI001-UWDI005 diagnostics, or end-to-end image and browser-cache verification.'
---

# Configure Dynamic Image

## Purpose

Configure and verify Dynamic Image as one cross-project contract: source discovery, generated catalogs, runtime validation, URL fingerprinting, and HTTP caching must agree.

Before acting, read:

- `.ai-shared\bundles\umbrella\analyzer-compatibility.md`
- `.claude\skills\umbrella-dotnet-configure-dynamic-image\references\dynamic-image-contract.md`

## Workflow

### 1. Discover the application topology

Identify:

- the executable Server project and every Client, Shared, model-factory, or MVC project containing Dynamic Image source;
- all `UmbrellaDynamicImage`, `UmbrellaFileImagePreviewUpload`, `dynamic-image`, `UmbrellaDynamicImageSource`, and `dynamic-source` usages, and for nested sources the element each is declared inside;
- all `FocalPointX`/`FocalPointY` and `focal-point-x`/`focal-point-y` bindings;
- every `EnableFocalPointSelection` usage and whether its value is a literal;
- the service registration and `UseUmbrellaDynamicImage` middleware call;
- every file-provider mapping and its data sensitivity;
- existing analyzer/generator package references and central package-version policy;
- existing `*Url`/`*VersionToken` properties and `GetVersionedWebFilePathAsync` calls.

Do not infer catalog completeness from a clean build. Compare every active Razor usage with generated variants.

### 2. Establish build-time ownership

- Install `Umbrella.WebUtilities.DynamicImage.Analyzers` directly, with `PrivateAssets="all"`, in every project containing checked models, assignments, or Razor.
- Install `Umbrella.Generators.DynamicImage` only in the Server project, with `PrivateAssets="all"`.
- Set `UmbrellaDynamicImageEnableUrlFingerprinting` explicitly in participating projects when fingerprinting is enabled across compilations.
- Give the Server local Razor a non-empty catalog name and configure named external source roots for Client or MVC Razor.
- Ensure one physical Razor file has exactly one catalog owner. Keep catalog names case-insensitively unique.
- Never add the generator to a browser Client merely to discover Client Razor; use a Server external source root.

### 3. Configure runtime behavior

- Assign `EnableUrlFingerprinting` as a literal `true` or `false` in the real registration callback.
- Register the generated named catalogs, or the aggregate catalog, before enabling validation.
- Configure each file mapping independently. Use `Public` only for CDN-shareable content, `Private` for user-specific browser-cacheable content, and `NoStore` for temporary or sensitive files.
- Use long max-age values only with URL fingerprinting. Keep unversioned/stale redirects non-cacheable.
- Keep validation enabled unless the application has an explicit reason not to constrain transforms.
- Place `UseUmbrellaDynamicImage` where requests reach it before terminal endpoint/fallback handling.
- Supply focal coordinates as a pair of normalized values from 0 through 1 and only with `Crop`, which crops from the image center when no focal point is supplied; invalid UI combinations fail before a Dynamic Image URL is rendered.
- ASP.NET Core validation requires image-bound approval for explicit coordinate pairs. Resolve `DynamicImageDescriptor` with `IDynamicImageDescriptorFactory` from trusted server metadata and bind `Image`, or propagate `FocalPointApproval`. Ordinary images and implicit center crops need no keys. Persist signing keys in server secrets, share them across instances, and never expose an unrestricted signing endpoint.
- Enable interactive preview selection only with a literal `EnableFocalPointSelection="true"`. The picker renders the complete image with `ScaleDown`, reports pointer or keyboard changes atomically, and clears to a null coordinate pair.

### 4. Preserve the URL/token contract

- Add nullable matching `*VersionToken` properties for Dynamic Image model URLs.
- Obtain the pair through `GetVersionedWebFilePathAsync`; do not manufacture tokens independently.
- Assign URL and token together in object initialization, mapping, post-save enrichment, and client-side copying.
- Treat a missing stored source as a recoverable state on administrative manage surfaces: keep the admin URL/token pair nullable, allow the form to load with both values null, and let the administrator upload a replacement. User-facing surfaces may remain strict when that is the application's explicit policy.
- On update, tolerate an unresolved pre-existing image when no replacement was requested. When a replacement was requested, fail if the newly promoted file still cannot be resolved; create operations remain strict.
- Use asynchronous Mapperly interfaces when enrichment performs file-provider I/O.
- Resolve collection items concurrently when lookups are independent and the collection is bounded; preserve result ordering.
- Pass the token to model-bound `UmbrellaDynamicImage` and `UmbrellaFileImagePreviewUpload` usages.
- Keep variant-shaping Razor inputs literal. Enum members are valid when type-qualified or when an effective simple or fully qualified `@using static` imports the matching enum type; constants, model expressions, and mixed strings are not catalog-discoverable.
- Focal coordinates are runtime inputs, may be model expressions, and do not participate in generated variant identity or UWDI004.
- `EnableFocalPointSelection` is variant-shaping. A literal `true` adds `ScaleDown` selector variants alongside the preview's configured crop variants; a runtime binding reports UWDI004.

### 5. Validate the complete contract

Build all participating projects with analyzers enabled, then:

1. Confirm UWDI001-UWDI005 are absent for legitimate code; add a regression before changing an analyzer for a suspected defect.
2. Inspect the generated named and aggregate catalog source and reconcile it with every active Razor usage.
3. Confirm generated catalog types exist in the Server assembly and do not ship in browser boot assets.
4. Request canonical fingerprinted fallback, WebP, and configured AVIF URLs; when focal cropping is used, confirm every URL preserves the same `fpx`/`fpy` pair and returns its explicit format without `Vary: Accept`.
5. For an interactive image preview, confirm the selector uses uncropped `ScaleDown` URLs and the adjacent canvas updates without focal-crop HTTP requests. Clearing emits a null pair. Save returns a fresh descriptor; catalogs retain the configured crop and selector variants.
6. Confirm changed dimensions, resize modes, and unregistered explicit formats return `404`.
7. Confirm ordinary missing/stale fingerprints redirect with `Cache-Control: no-store`; invalid or stale signed focal requests return `404` before cache/conditional responses. Check UWDI006 for missing approval propagation in authored Razor.
8. Confirm mapping-specific cache headers, ETag/Last-Modified validators, and explicit conditional `304` responses.
9. Change a disposable source file and verify its token and canonical URL change before removing the probe.

Temporary probes and assets must remain uncommitted and be removed before the final build.

## Completion

Report package placement, catalog ownership, mapping cache policies, generated-catalog reconciliation, analyzer results, and HTTP/browser evidence. If the request was audit-only, make no changes.
