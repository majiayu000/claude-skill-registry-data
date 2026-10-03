---
name: nuxt-ui-tools-file-preview
description: Use this skill when previewing files with nuxt-ui-tools as a package consumer. Covers mounting UiFilePreviewProvider, opening one file or a gallery with useFilePreview() or useNuxtApp().$filePreview, file descriptors (URL, File/Blob, or a function that returns a signed URL), options (index, mode, gallery, loop, pdf page, callbacks), the returned handle, the built-in renderers (image, video, audio, PDF, text/JSON, CSV, Markdown, Office and archive fallbacks), renditions, download and custom header actions, the markdown render hook, custom renderers with defineFilePreviewRenderer and UiFilePreviewTools, theming tokens, and how the upload field uses the preview.
---

# nuxt-ui-tools File Preview

One call opens any file in an overlay with a renderer made for its kind. Media opens in a modal,
documents in a right drawer, and phones get fullscreen. Renderers load on first use, so an app only
downloads the code for the kinds it actually shows.

## Mount the provider once

The module creates one API for the whole app. Mount the provider next to the form provider; it
renders the previews:

```vue
<template>
  <UApp>
    <UiToolsProvider :locale="uiToolsLocale">
      <UiFormProvider>
        <UiFilePreviewProvider :markdown="renderMarkdown">
          <NuxtPage />
        </UiFilePreviewProvider>
      </UiFormProvider>
    </UiToolsProvider>
  </UApp>
</template>
```

The component prefix follows the module `prefix` option (`Ui` by default).

`markdown` is optional. It receives the file text and must return sanitized HTML (or a promise of
it). Without it, Markdown files show their source.

## Open files

Components use `useFilePreview()`. Code outside setup, such as entity actions or stores, uses
`useNuxtApp().$filePreview`:

```ts
export function previewAccountFile(account: { id: string; name: string }, file: 'kbis' | 'logo') {
  const { $filePreview } = useNuxtApp()
  return $filePreview.open({
    name: `${file.toUpperCase()} — ${account.name}.pdf`,
    src: `/v1/accounts/${account.id}/files/${file}`,
  })
}
```

`open()` accepts one input or an array (a gallery). Each input is a URL string, a `File` or `Blob`,
or a descriptor:

```ts
const preview = $filePreview.open(
  contract.files.map((file) => ({
    id: file.id,
    name: file.label,
    mime: file.mimeType,
    size: file.size,
    updatedAt: file.createdAt,
    // Runs only when this file is shown, and again when the user presses Retry.
    src: () => $api.contracts.fileUrl({ params: { fileId: file.id } }).then((res) => res.url),
    download: () => downloadContractFile(file),
    actions: [{ icon: 'i-lucide-folder-open', label: 'Open in registry', to: registryPath(file) }],
  })),
  { index: 2 },
)

preview.next()
await preview.closed
```

### Descriptor fields

| Field                 | Meaning                                                                                                                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `src`                 | URL, `File`/`Blob`, or `() => MaybePromise<string \| Blob>`. Functions resolve once per file and again on Retry.                                                               |
| `name`                | Display name. Defaults to `File.name`, then the last URL segment.                                                                                                              |
| `mime`                | Wins over the extension to pick a renderer.                                                                                                                                    |
| `kind`                | Forces a renderer (`'image'`, `'pdf'`, …, or a custom kind).                                                                                                                   |
| `size`, `updatedAt`   | Shown in the meta line and the details panel. `File` inputs fill them.                                                                                                         |
| `thumbnail`, `poster` | Gallery strip image; video poster or audio cover.                                                                                                                              |
| `rendition`           | A preview made by your server for files browsers cannot render (DOCX → PDF, HEIC → JPEG). The preview shows it with a "Converted preview" notice; download keeps the original. |
| `details`             | Extra `{ label, value }` rows in the details panel.                                                                                                                            |
| `download`            | `false` hides it, a string downloads that URL, a function replaces the download. Default: the resolved source under `name`.                                                    |
| `actions`             | Extra header buttons: `{ label, icon?, to?, onSelect? }`. External `to` opens a new tab; internal `to` closes the preview and navigates.                                       |
| `tracks`              | Video captions: `{ src, srcLang, label, kind?, default? }`.                                                                                                                    |

Text values (`label`, `value`) accept a getter such as `() => t('files.uploadedBy')` so they follow
the language.

### Options

| Option                               | Meaning                                                                                                                                                       |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `index`                              | File shown first.                                                                                                                                             |
| `mode`                               | `'modal' \| 'drawer' \| 'fullscreen'` or a responsive value like `'fullscreen md:drawer'`. Responsive values start at `sm`, so the first value covers phones. |
| `id`                                 | Opening the same id again updates that preview instead of stacking another.                                                                                   |
| `gallery`                            | `'strip'` (default, thumbnails) or `'counter'`. Phones always show the counter.                                                                               |
| `loop`                               | Wraps from the last file to the first.                                                                                                                        |
| `pdf.page`                           | Page PDFs open at.                                                                                                                                            |
| `onChange(file, index)`, `onClose()` | Callbacks.                                                                                                                                                    |

Without `mode`, each file's renderer suggests a container and the largest wins, so a gallery keeps
one container while navigating: images and video use `fullscreen md:modal`, documents
`fullscreen md:drawer`. A single audio file or fallback card uses a narrow modal.

### Handle

`open()` returns right away: `{ id, index (readonly ref), next(), previous(), goTo(i), update(input), close(), closed }`.
`closed` resolves once the overlay has left the screen. The API also has `close(id?)` (top-most
preview when omitted), `closeAll()`, `isOpen(id?)`, `instances`, and `mounted` (a provider is
rendering).

## Built-in renderers

| Kind                         | Matches                                        | Rendering                                                                                                                                                                           |
| ---------------------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `image`                      | `image/*`, png jpg webp gif avif svg heic…     | Fits without upscaling; wheel/pinch/double-click zoom, drag to pan, rotate. Transparent formats sit on a checkerboard. SVG renders through `<img>`, so its scripts never run.       |
| `video`                      | `video/*`, mp4 webm mov…                       | `<video>` with custom controls (play, seek, volume, speed, captions, picture-in-picture, fullscreen).                                                                               |
| `audio`                      | `audio/*`, mp3 m4a wav…                        | Card with cover and the same controls.                                                                                                                                              |
| `pdf`                        | `application/pdf`                              | The browser's own viewer in an iframe (`#view=FitH`). Blob sources are re-typed as PDF. When `navigator.pdfViewerEnabled` is `false` (Android), it shows Open and Download instead. |
| `text`                       | `text/*`, json, xml, yaml, log, code files     | Line numbers, wrap, copy. JSON is formatted and tinted.                                                                                                                             |
| `csv`                        | `text/csv`, csv, tsv                           | Table with sticky header, row numbers, right-aligned numbers. Detects `;`, `,`, tab, and `\|`, and strips the BOM. Shows the first 1,000 rows.                                      |
| `markdown`                   | md, `text/markdown`                            | Your `markdown` hook's HTML with a Preview/Source switch, or the source.                                                                                                            |
| `office`, `archive`, `other` | doc(x) xls(x) ppt(x) odt…, zip…, anything else | A card with the facts and Download. Pass a `rendition` to preview Office files.                                                                                                     |

Text, CSV, and Markdown read at most 512 KB (`FILE_PREVIEW_TEXT_LIMIT`) and say when a file was cut.
They read `Blob` sources directly; for URLs they use `fetch`, so the URL must be readable from the
page (same origin, or CORS allowing your origin). Images, video, audio, and PDFs use elements that
follow redirects without CORS.

Errors show a reason and the right action: Retry when `src` is a function (an expired signed link),
Download when the browser cannot decode the format.

Keys: `←` `→` `Home` `End` navigate, `Esc` closes, `+` `−` `0` `R` zoom, fit, and rotate images,
`Space` `K` `M` `F` control media.

## Custom renderers

Register a renderer in a plugin. Registering a built-in kind replaces it (for example, a pdf.js
renderer for phones):

```ts
// app/plugins/file-preview.ts
export default defineNuxtPlugin(() => {
  useNuxtApp().$filePreview.register(
    defineFilePreviewRenderer({
      kind: 'email',
      icon: 'i-lucide-mail',
      label: () => 'Email',
      match: ({ mime, extension }) => mime === 'message/rfc822' || extension === 'eml',
      component: () => import('~/components/previews/EmailPreview.vue'),
      mode: 'fullscreen md:drawer',
    }),
  )
})
```

The component receives `{ file, url, blob, container }` and emits `ready(details?)` once content is
on screen and `error({ reason, message? })` when it cannot render. Put toolbar buttons in
`<UiFilePreviewTools>`; they appear in the header, or in the bottom bar on phones. Use
`useFilePreviewText(props)` to read text with the size limit, and `onFilePreviewKey(keys, handler)`
for shortcuts.

```vue
<script setup lang="ts">
import type { FilePreviewRendererEmits, FilePreviewRendererProps } from '#ui-tools/file-preview'
import { useFilePreviewText } from '#ui-tools/file-preview'

const props = defineProps<FilePreviewRendererProps>()
const emit = defineEmits<FilePreviewRendererEmits>()
const content = useFilePreviewText(props)

watch(content.status, (status) => {
  if (status === 'ready') emit('ready')
  if (status === 'error') emit('error', { reason: 'source', message: content.error.value?.message })
})
</script>
```

## Upload fields

When a provider is mounted, the upload field's open action previews the field's files as a
gallery, starting at the clicked one. Files uploaded in the current session preview from the
browser's copy with no request; stored files use the `url` their `resolve()` returns. A custom
`upload.open` still wins, and without a provider the field keeps opening a new tab.

## Theming

Override these CSS variables: `--nut-fp-veil` (overlay), `--nut-fp-stage` (image and loading
background), `--nut-fp-document` (behind PDFs), `--nut-fp-checker-a` / `--nut-fp-checker-b`,
and `--nut-fp-token-key|string|number|literal` (JSON tint). Strings live in the `filePreview`
section of the package locales (`en`, `fr`).
