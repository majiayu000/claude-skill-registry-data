---
name: images
description: Read before an app makes a photo or a PDF page small, crops it or draws on it, to show it, send it to an AI model or put photos into one PDF.
metadata:
  title: "Images"
  subtitle: "Photos and PDF pages, made small"
  about: "Opens photos and the pages of PDFs for the apps that need them smaller, cropped or joined."
  category: Admin
---

Images is for an app that has to look at a photo or a PDF itself: to show a small copy of it, to cut one receipt out
of a photo of several, to send a page to an AI model, or to put photos into one PDF. It has no tools; an app requires
it and calls its functions, which run in that app:

    def requires, do: %{"images" => "to read your receipts"}

    images = OneCore.Call.app(call, "images")
    {:ok, %{data: jpeg, width: w, height: h}} = images.render(file, max: 1600, quality: 85)

- `render(file, options)` opens a photo (JPEG, PNG or WebP, turned upright as its camera recorded) or a page of a PDF
  (`page:`, from 0, drawn with its long side `render:` pixels) and gives a JPEG, `crop: [left, top, right, bottom]` of
  it as fractions from its top left, made smaller to `max:` pixels on its long side (only ever smaller unless
  `enlarge: true`), `quality:` 85, and with `cover:` rectangles, in the same fractions, drawn over in dark grey first.
- `pdf(file)` says each page of a PDF, whether it's typed (shows text) or only a scan.
- `pdf_of(photos)` makes JPEGs into one PDF, a page each.
