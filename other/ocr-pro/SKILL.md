---
name: ocr-pro
description: Optical character recognition pipelines — engine choice, preprocessing, and accuracy — use when extracting text from images or scans.
category: document-processing
---

## Overview

OCR turns images of text — scans, photos, screenshots — into machine-readable
text. Accuracy depends less on the engine than on input quality and post-
processing. This skill covers choosing an OCR approach, preprocessing images
for maximum accuracy, and validating results.

## When to use

- Digitizing scanned documents, PDFs-as-images, or paper archives
- Extracting text from photos (receipts, signs, whiteboards, IDs)
- Choosing between local OCR engines and cloud vision APIs
- Improving accuracy on difficult inputs (handwriting, low contrast, skew)
- Building validation for OCR output in a pipeline

## Core concepts

**Garbage in, garbage out — preprocessing is half the job.** Denoise, deskew,
increase contrast, and upscale small text (300 DPI equivalent is the rule of
thumb) before OCR. A 30-second preprocessing pass often beats switching engines.

**Engine choice is a trade-off.** Local engines (Tesseract and its successors)
are free, private, and good for clean printed text. Cloud vision APIs handle
handwriting, complex layouts, and poor photos better but cost money and send
data off-site. Neural/document-AI services add layout understanding (tables,
forms, key-value pairs) — worth it for invoices and forms.

**Layout analysis precedes recognition.** Good OCR segments the page into
blocks, lines, and words first. Multi-column pages, tables, and mixed
orientations need layout-aware processing — naive line-by-line OCR interleaves
columns.

**Confidence scores are signal.** Engines report per-word/per-character
confidence. Use it: route low-confidence segments to human review, and never
let sub-threshold numbers flow into financial or legal records unchecked.

**Language and domain tuning.** Set the expected language(s); add custom
dictionaries or patterns for domain vocabulary (product codes, medical terms).
Constraining the character set (digits only for amounts) dramatically cuts
character-confusion errors (0/O, 1/l/I).

## Practical workflow

1. **Assess the input:** scan quality, language(s), layout complexity,
   handwriting presence — this determines engine and preprocessing.
2. **Build the preprocessing chain:** grayscale → denoise → deskew →
   contrast/threshold → upscale to ~300 DPI; inspect intermediate outputs on
   samples.
3. **Run OCR with the right config:** page segmentation mode matched to layout
   (single block vs sparse text vs single line), language packs installed,
   character whitelist where applicable.
4. **Post-process:** spell/domain correction, regex validation of structured
   fields (dates, amounts, IDs), and format normalization.
5. **Validate with ground truth:** hand-transcribe a sample set, measure
   character/word error rates, and set an acceptance threshold before
   production.
6. **Design the human-in-the-loop path:** low-confidence items queue for
   review; corrections feed back into dictionaries or fine-tuning data.

## Common pitfalls

- **Skipping preprocessing** and blaming the engine — most accuracy problems
  are input problems.
- **Trusting OCR numbers blindly** in financial/legal contexts — always
  validate with checksums, totals, or human review above a risk threshold.
- **Wrong segmentation mode** — the single most common Tesseract misconfiguration;
  match it to the actual layout.
- **Ignoring rotation/skew** — even 2–3 degrees of skew degrades accuracy
  measurably; deskew first.
- **Sending sensitive documents to cloud OCR** without considering data
  residency and privacy obligations — PII in images is still PII.
- **No handling for multi-page documents** — page ordering, headers/footers
  repeated per page, and tables spanning pages all need explicit logic.
