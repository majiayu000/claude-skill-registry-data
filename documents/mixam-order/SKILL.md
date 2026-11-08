---
name: mixam-order
description: Prepare a print order at Mixam (mixam.com) — binding by page count, the PUR spine formula with paper calipers, press-ready PDF specs, multi-file upload naming, and the inner-cover "Artwork missing" trap. Use for "print-ready PDF for Mixam", "spine width", "perfect bound / PUR / saddle-stitch", "is this too many pages for a magazine", "inner covers say artwork missing", "how do I name the upload files", or checking a Mixam cart against the files.
---

# Mixam: preparing a print order

**Ordering spends money, so a person places the order.** The agent builds the files, gives the
exact cart settings, and checks a screenshot of the cart against the files.

## Binding: choose it by page count

| Binding | Pages | Use it when |
|---|---|---|
| Saddle-stitch (staples) | at most **96**, a multiple of 4; the cover counts in the total | Magazine thickness |
| **Perfect bound (PUR)** | 32+ inside pages, a multiple of 4; the cover is a separate file | Past 96 pp. Still reads as a thick magazine, with a flat spine for type |
| Wire-O, hardcover | offered | Wire-O reads as a notebook |

Decide the binding before laying out: it changes the file set and the page arithmetic.

## PUR spine formula

`spine = floor(pages / 2 × caliper, to 0.01 in) + 0.01 in`, where pages = inside pages only.

- **Calipers** (inches per leaf, from Mixam's calculator data, read 2026-10):
  Satin 70 lb Text 0.0035, 80 lb Text 0.004, 100 lb Text 0.005. Cover weight doesn't change the
  spine on the standard US plants.
- Fitted against 14 live quotes: 112 pp on 80 lb Text → 0.23 in; 152 pp → 0.31 in (confirmed in
  a cart).
- **Some plants quote wider.** Express, and Best Value on 130 lb Cover, quote 0.03–0.10 in
  wider. **Always read the spine width off the cart** and rebuild the cover if it differs.
- Put spine text only when the spine is ≥ 0.25 in; keep it 0.08 in clear of each fold.

## Files

- **Format:** trim size + 0.125 in bleed on every edge, TrimBox and BleedBox set. sRGB is fine
  (Mixam converts). No crop marks.
- **PUR cover:** **one** page holding the outer spread, back | spine | front. Width =
  2 × trim + spine (8.5 × 11 trim at 152 pp → 17.31 × 11.00 in before bleed).
  Mixam may warn that it's wider than letter; that's expected.
- **Several files in one upload:** Mixam orders them by the **number in the file name**
  (`1-cover.pdf`, `2-interior.pdf`). The words `front`, `back`, `rear`, `last` and `inner` are
  also understood.
- **Cover printed on both sides is the cart default.** "Full-color printing (front and back)"
  means Mixam expects **inner front** and **inner back** cover artwork; otherwise the proof
  shows "Artwork missing" on both. Either supply `inner-front.pdf` and `inner-back.pdf` (one
  trim+bleed page each, uploaded with the **⋯** button on each inner-cover slot), or set the
  cover to print on the outside only.
- Using the inner covers (e.g. contents inside the front, a closing page inside the back) moves
  pages out of the body. The body must stay a multiple of 4 and the spine changes with it:
  **plan the inner covers before the final build**, not after.

## Saddle-stitch settings that worked

Custom trim (e.g. 8.375 × 10.875 in — enter the trim, never trim plus bleed), Coated Satin,
100 lb inside pages.

## Checking a cart screenshot

Check every line against the files: size and orientation; binding; inside page count; text
paper and weight; **spine width = the cover file's spine**; cover paper, lamination, and
whether the inside covers print. Then report the price per copy at each quantity offered —
quantity breaks are steep at short runs.
