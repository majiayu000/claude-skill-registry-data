---
name: embedded-image-studio
description: Use whenever a form needs to accept ONE image and produce permanent public URLs for one or more platform-specific sizes (OG image, social posts, avatars, logos, favicons, app icons). Replaces every legacy image-URL input, single-size uploader, and base64-data-URL flow. Triggers when you see a manual `<input type="url">` for an image, a single-size uploader, or anywhere a `dataUrl` could leak into a clipboard or a saved record.
---

# Embedded Image Studio — Skill

Drop the `<EmbeddedImageStudio>` component into any form that needs an image. The user drops a file → cropper opens → all caller-requested sizes generate → variants upload as **public** to Cloud Files → host receives **permanent Cloudflare CDN URLs**.

This is the **only** approved pattern for image inputs going forward. It is forbidden to:

- Save base64 `data:` URLs in any record (chat clipboard, DB column, redux slice).
- Use `<input type="url">` to capture an image URL when an embedded studio could capture it from a real file upload.
- Upload images with `visibility: "private"` for fields meant to be embedded in HTML, OG meta tags, emails, or anywhere else a paste might appear.
- Generate variants client-side with `canvas.toDataURL()` and ship them as URLs.
- Hand-roll a "drop → resize → upload" pipeline. There is one pipeline; use it.

---

## Three intake paths — all built in

The user has three ways to give us an image. The component surfaces them up-front so we never push the user out of our system to find what they already have.

| Path | When to use | What happens |
|---|---|---|
| **Drop / Browse** | Brand-new image | Crop dialog → Sharp generates every preset → uploads as PUBLIC → CDN URLs returned |
| **Paste URL** | The user already has a public URL elsewhere | The URL is used **as-is**. No re-upload, no resize. `onSaved` fires immediately with that URL as `primary`. |
| **From library** | The user already saved this image to Cloud Files | Opens `useFilePicker` → user picks a file → its permanent CDN `publicUrl` (or a 1h signed URL for private files) is used as-is. `onSaved` fires immediately. |

Drop is the "I want all the sizes" path. The other two are "I already have what I need" paths — they emit `result.primary.publicUrl` straight away so the host form gets populated with one click. **Never push a user out of the system to find an image they already have.**

---

## The pattern at a glance

```tsx
import { EmbeddedImageStudio } from "@/features/image-studio/components/EmbeddedImageStudio";

<EmbeddedImageStudio
  // Which preset sizes to auto-generate. From features/image-studio/presets.ts.
  presetIds={["og-image", "fb-post", "tw-card-large", "ig-square"]}
  // Which one's URL the host actually cares about — the result's `primary` URL.
  primaryPresetId="og-image"
  // Folder segment under Images/Generated/. One per host feature.
  rootFolderSegment="html-pages"
  // Recommended: pass a meaningful default (page title, app name, person's name).
  defaultFilenameBase={page.title || "page-social-image"}
  // Show the existing public URL with a Replace CTA when the field is already set.
  initialUrl={page.ogImage || null}
  disabled={!user}
  label="Social Share Image"
  onSaved={(result) => {
    // result.primary.publicUrl is a permanent Cloudflare CDN URL.
    if (result.primary?.publicUrl) {
      setOgImage(result.primary.publicUrl);
    }
    // result.byPreset has every preset's CDN URL — store them too if useful.
  }}
  onCleared={() => setOgImage("")}
/>
```

### What the user sees

1. **Drop zone** (or "Replace" button if `initialUrl` was set).
2. **InitialCropWindow** opens automatically (a floating WindowPanel) with aspect-ratio chips, panning, and resize handles.
3. **Source preview + filename input** — the user can rename the slug; the slug becomes the per-source subfolder AND every variant's filename.
4. **"Generate & save"** button — one click runs Sharp + cloud upload.
5. **Variant grid** — every requested preset shows preview, dimensions, file size, compression %, and a permanent CDN URL with a Copy button.
6. **`onSaved` fires** with `result.primary.publicUrl` ready to drop into the host's state.

### Where the bytes go

```
Cloud Files
└── Images/
    └── Generated/
        └── <rootFolderSegment>/                 ← e.g. html-pages
            └── <filenameBase>/                  ← e.g. how-to-bake-bread
                ├── how-to-bake-bread-og-image.webp
                ├── how-to-bake-bread-fb-post.webp
                ├── how-to-bake-bread-tw-card-large.webp
                └── how-to-bake-bread-ig-square.webp
```

Every file is `visibility: "public"` → API returns `public_url` → the result is a `https://cdn.aidream.com/.../...?v=<checksum>` URL that:

- Never expires.
- Cache-busts automatically when content changes (the checksum suffix flips).
- Is served from Cloudflare's CDN, not a presigned S3 URL.

---

## Picking the right `presetIds`

Read [presets.ts](presets.ts) for the full catalog (60+ across 10 categories). The right set depends on the host feature.

| Host feature | Suggested `presetIds` | `primaryPresetId` |
|---|---|---|
| HTML pages / blog SEO | `["og-image", "fb-post", "tw-card-large", "ig-square"]` | `"og-image"` |
| Agent app cover / preview | `["agent-app-cover", "fb-post", "ig-square"]` | `"agent-app-cover"` |
| Avatar / profile picture | `["avatar-xl", "avatar-lg", "avatar-md", "avatar-sm", "avatar-xs"]` | `"avatar-md"` |
| Org logo | `["logo-xl", "logo-md", "logo-favicon"]` | `"logo-md"` |
| Favicon set | `["favicon-32", "favicon-192", "apple-touch-icon", "android-chrome-192", "android-chrome-512"]` | `"favicon-192"` |
| Podcast cover art | `["podcast-cover", "ig-square", "fb-post"]` | `"podcast-cover"` |
| Single OG-only field | `["og-image"]` | `"og-image"` |

If a preset you need doesn't exist, add it to `PRESET_CATEGORIES` in [presets.ts](presets.ts) — don't pass arbitrary dimensions inline.

---

## When the host has a richer surface

If the host feature wants different filenames per record (e.g. per-page title), pass `defaultFilenameBase` from that record. It's used as the per-source subfolder AND as the prefix for every variant filename.

```tsx
// Bad — every page's variants land in /image-studio/social-image/
defaultFilenameBase="social-image"

// Good — every page gets its own folder, slugged from the title
defaultFilenameBase={page.title}
```

When the user later AI-describes the image (or types a new name), the variants are regenerated under the new slug.

---

## Replacing existing image inputs

### Step-by-step migration recipe

1. **Identify the field.** Search for `<input type="url">` near the word "image", or `useState<string>` whose default is an image URL.
2. **Identify the presets.** Match the field's purpose to the table above.
3. **Identify a meaningful filename source.** Title, name, slug, agent name, etc.
4. **Replace the input** with `<EmbeddedImageStudio>` exactly as shown above.
5. **Remove any `dataUrl`/`base64` plumbing.** The component never returns one.
6. **Verify** by uploading an image: the URL the host stores should start with `https://cdn.` and contain `?v=`.

### Anti-patterns to delete on sight

```tsx
// ❌ Plain URL input
<input type="url" value={ogImage} onChange={(e) => setOgImage(e.target.value)} />

// ❌ Single-size uploader that returns a dataUrl
<ImageAssetUploader onComplete={(r) => setOgImage(r.dataUrl)} />

// ❌ Saving a data: URL into Redux/DB
dispatch(updateMetadata({ ogImage: canvas.toDataURL() }));

// ❌ Manual `uploadFile` + `getSignedUrl` chains for a public image
const f = await uploadFile(...); const s = await getSignedUrl(f.id);
setUrl(s); // ← signed URL expires, breaks shares
```

---

## What the component handles for you

- **Drop / paste / browse** — multi-source intake (file picker, drag-drop, paste-from-clipboard).
- **EXIF rotation** — Sharp auto-rotates so portrait phone shots aren't sideways.
- **Crop dialog** — full freeform + aspect-ratio chips, with rule-of-thirds guides.
- **Per-source subfolder** — variants for one image stay grouped, never jumbled.
- **Filename gate** — auto-named files surface a banner before mass generation.
- **Public-by-default** — `visibility: "public"` so the API returns a CDN URL.
- **Per-variant copy buttons** — every result has a "Copy CDN" action. We never copy a data URL once the variant is saved.
- **Replace flow** — clicking Replace clears state and re-opens the drop zone.
- **`onSaved` callback** — host receives `result.primary.publicUrl` to fold back into its state.

---

## Forbidden in callers

- Don't read `variant.dataUrl` for anything user-facing once `savedAt` is set.
- Don't bypass `onSaved` to manually fish URLs out of the cloud-files slice.
- Don't override `visibility: "private"` unless the field is genuinely never going to be embedded anywhere (rare — usually the answer is public).
- Don't render the `<EmbeddedImageStudio>` inside a tight grid cell. It needs ~400px of width.
- Don't reuse the same `rootFolderSegment` across unrelated features. Use the host feature's slug.

---

## Reference implementation

[`SavePageTab.tsx`](../../features/html-pages/components/tabs/SavePageTab.tsx) — the canonical example. Copy the pattern:

```tsx
<EmbeddedImageStudio
  presetIds={["og-image", "fb-post", "tw-card-large", "ig-square"]}
  primaryPresetId="og-image"
  rootFolderSegment="html-pages"
  defaultFilenameBase={state.metadata.title?.trim() || "page-social-image"}
  initialUrl={state.metadata.ogImage || null}
  disabled={!user}
  label="Social Share Image"
  onSaved={(result) => {
    if (result.primary?.publicUrl) {
      actions.setMetadataField("ogImage", result.primary.publicUrl);
    }
  }}
  onCleared={() => actions.setMetadataField("ogImage", "")}
/>
```

---

## Files of record

- [`components/EmbeddedImageStudio.tsx`](components/EmbeddedImageStudio.tsx) — the component itself.
- [`hooks/useImageStudio.ts`](hooks/useImageStudio.ts) — the underlying state machine.
- [`presets.ts`](presets.ts) — the preset catalog (add new presets here, never inline).
- [`components/InitialCropWindow.tsx`](components/InitialCropWindow.tsx) — the crop step (floating window; the older Dialog wrapper was removed in 2026-05).
- [`../files/SKILL.md`](../files/SKILL.md) — the cloud-files contract this component honors.

## Change log

- **2026-05-04** — Three-way intake (Drop / Paste URL / From library). URL paste and library pick emit `onSaved` immediately with the chosen URL as `primary` — no forced pipeline. Stops pushing users out of the system when they already have what they need. Also fixed a closure-staleness bug in `saveAll` where variants saved right after `generate()` had no `publicUrl` because the function read from a frozen `files` reference; now reads through `filesRef.current`.
- **2026-05-03** — Initial skill. Defines `EmbeddedImageStudio` as the canonical image-input component for every form. SavePageTab is the reference implementation.
