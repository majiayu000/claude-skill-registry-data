---
name: block-print-system
description: "Printing and PDF export for AI response blocks and messages via @ai-matrx/print. Use when adding a print button or BlockPrinter to a render block, wiring PrintOptionsDialog/usePrintOptions, captureBlockElement, or useDomCapturePrint, or when a print window shows no images or a print fails silently."
---

# Block Print System

Three-tier architecture for printing AI response messages, plus the reusable
printing core that other surfaces build on. **The core lives in
the `@ai-matrx/print` npm package** (extracted 2026-08-29; source `aidream/apps/shared/print`) — chat-specific tiers live with the conversation feature.

## Architecture Overview

```
Tier 1 — Quick Print (prose only)
  printMarkdownContent() → regex → HTML window
  File: packages/chat/src/conversation/utils/markdown-print.ts
  Limitation: ignores all custom blocks

Tier 2 — Full Message (DOM screenshot)
  useDomCapturePrint → html2canvas + jsPDF
  File: packages/chat/src/conversation/hooks/useDomCapturePrint.ts
  Hook returns: { captureRef, isCapturing, progress, captureAsPDF, error }
  isCapturing must be wired to the menu item (disabled state + label change)

Tier 3 — Per-Block (best quality, block owns its output)
  Print button in each block's header → either HTML template printer or DOM capture
  Dialog + hook: @ai-matrx/print/react (PrintOptionsDialog, usePrintOptions)
```

## The BlockPrinter Interface

Source of truth: `@ai-matrx/print/core` (BlockPrinter, PrintVariant, PrintSetting, PrintSettings)

```typescript
interface BlockPrinter {
    label: string;
    variants: PrintVariant[];
    settings?: PrintSetting[];
    print: (data: unknown, variantId?: string, settings?: PrintSettings) => void | Promise<void>;
}

interface PrintVariant { id: string; label: string; description?: string; }

// PrintSetting is a discriminated union of FOUR control types (all support
// appliesTo?: string[] — which variantIds the setting shows for):
//   { type: "boolean"; id; label; description?; defaultValue }
//   { type: "range";   id; label; fromId; toId; defaultFrom; defaultTo; min?;
//     fromPlaceholder?; toPlaceholder? }   // two number inputs; writes TWO
//     settings-map keys (fromId/toId); 0 = "no bound" by convention
//   { type: "number";  id; label; defaultValue; min?; max? }  // single numeric input
//   { type: "select";  id; label; options: {value,label}[]; defaultValue }
//     // compact segmented one-of-N row

type PrintSettings = Record<string, boolean | string | number>;
```

If `variants.length === 0` AND `settings.length === 0`, `usePrintOptions` calls `print(data)` immediately with no dialog. Otherwise the `PrintOptionsDialog` opens first (Dialog on desktop, Drawer on mobile).

## Existing Printers

| Block / surface | Strategy | File |
|---|---|---|
| FlashcardsBlock | HTML template | `@ai-matrx/print/flashcards` (flashcardsPrinter) |
| MultipleChoiceQuiz | HTML template | `components/mardown-display/blocks/quiz/quiz-printer.ts` |
| MathProblemBlock | HTML template | `components/mardown-display/blocks/math/math-printer.ts` |
| DiagramBlock | HTML template | `components/mardown-display/blocks/diagram/diagram-printer.ts` |
| PD rating report | HTML template | `features/legal/wc/pd-ratings/print/pd-report-printer.ts` |
| Performance review report | HTML template | `features/employee-performance-reviews/review-report.ts` |
| **QR label sheets** | HTML template (registry-driven grid) | `@ai-matrx/print/labels` (qrLabelsPrinter) — Avery + roll stock QR labels; template registry, calibration page, LabelSheetPreview (in /react) + jsPDF lane |
| Various display blocks | DOM capture | inline in component via `@ai-matrx/print/pdf` (captureBlockElement) |

## Adding an HTML Template Printer

1. Create `<block-name>-printer.ts` alongside the component file.
2. Import `buildPrintDocument, openPrintWindow, escapeHtml, type BlockPrinter, type PrintSettings` from `@ai-matrx/print/core`.
3. Define `variants` and optional `settings` arrays.
4. In `print(data, variantId = "default", settings?)`:
   - Cast and guard: `if (!typed?.items?.length) { openPrintWindow(buildPrintDocument("<p>No data.</p>", ...), "fallback"); return; }`
   - Call `escapeHtml()` on every user string.
   - Read settings as: `const show = (settings?.showX ?? false) as boolean`.
5. In the component: call `usePrintOptions(printer, data)` (from `@ai-matrx/print/react`), wire `triggerPrint` to a `<Printer>` button, render `<PrintOptionsDialog>` outside (not inside) the block wrapper.

Full examples in the package source (`aidream/apps/shared/print/src/`): `flashcards.ts` (variants + boolean settings + fit-text auto-shrink), `labels.ts` (all four setting types, inch-exact `@page` geometry, data-URI images).

## Adding a DOM Capture Block

Required pattern — copy exactly:

```typescript
const blockContentRef = useRef<HTMLDivElement>(null);
const [isPrinting, setIsPrinting] = useState(false);

const handlePrint = useCallback(async () => {
    if (!blockContentRef.current || isPrinting) return;
    setIsPrinting(true);
    try {
        const { captureBlockElement } = await import('@ai-matrx/print/pdf');
        await captureBlockElement(blockContentRef.current, 'filename', 'landscape'); // or 'portrait'
    } catch (err) {
        console.error('[BlockName] Print failed:', err);
    } finally {
        setIsPrinting(false);
    }
}, [isPrinting]);
```

Key rules:
- `captureBlockElement` signature: `(element, filename, orientation?: "landscape" | "portrait")` — default is `"landscape"`
- Always `await` it — missing await means errors are invisible silent rejections
- Attach `ref` to the **content container**, not the whole block shell or a stats summary
- `disabled={isPrinting}` on the button; show `"Saving…"` label while active
- If the block has fullscreen mode, add a print button in the fullscreen header too — the regular toolbar is hidden

## Wiring Tier 2 `isCapturing`

In the assistant-message component:

```typescript
const { captureRef, isCapturing, captureAsPDF } = useDomCapturePrint();
```

Pass `isCapturing` to the message options menu as a prop. The menu item should be `disabled` and show `"Generating PDF…"` while true.

## Key Utilities

All in `@ai-matrx/print` (`/core`, `/pdf`, `/markdown`, `/react`). Since 0.3.0 the markdown converter and the print stylesheet ship IN the package — there is no host seam, and re-adding one is the defect this repo already made three times:

- `buildPrintDocument(bodyHtml, title?, extraStyles?)` → complete `<!DOCTYPE html>` string
- `openPrintWindow(htmlDoc, filename?)` → popup window; falls back to `.html` download if popup blocked. **The window is a fresh unauthenticated document — inline every image as a data URI, never fetch.**
- `printHtmlContent(bodyHtml, title?, extraStyles?)` → shorthand combo
- `markdownToPdfBlob(markdown)` (`/pdf`) → styled multi-page PDF Blob, no arguments beyond the markdown
- `markdownToHtml` / `getMarkdownStylesheet` / `printMarkdown` (`/markdown`) → the shipped converter, the two default stylesheets ("document" and "article"), and the one-call print window. Brand it with `tokens`; never fork the sheet.
- `captureBlockElement(el, filename, orientation?)` → delegates to `captureToPDF` with scale:2
- Fixed-geometry sheets (`@page { size: …; margin: 0 }`, inch-exact cells, screen-only "100% scale, no margins" banner, FIT_TEXT auto-shrink): patterns in the package's `flashcards.ts` (Avery 5388) and, generalized to a template registry, `labels.ts`

## Common Bugs to Watch For

1. **Missing `await` on `captureBlockElement`** — errors silently swallowed
2. **`ref` on wrong element** — attach to content, not stats/header/outer shell
3. **Print button absent in fullscreen** — must add to fullscreen header explicitly
4. **Missing `settings` param in `print()`** — use `settings?.key ?? defaultValue` pattern
5. **`isCapturing` not wired** — users get no feedback during Tier 2 PDF generation
6. **Fetched images in a print window** — the window has no auth; only data URIs render
