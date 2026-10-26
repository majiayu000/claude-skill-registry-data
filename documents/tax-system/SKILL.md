---
name: tax-system
description: Use when a German investment-tax question arises — explains the authority order and how to use the 2026 tax guide PDF.
---

# Tax System (reference)

## Authority order

When a tax question comes up, consult sources **in this order**:

1. **`docs/INDEX.md` + project docs (`docs/*`)** — check what this project has
   already documented/decided first.
2. **BMF circulars / official ELSTER forms** — this is the actual source of
   truth in German tax law. Line numbers, rates, and loss-bucket rules must
   trace back here.
3. **`2026+TaxGuide.pdf`** at `/mnt/c/Users/Kostan/Downloads/2026+TaxGuide.pdf`
   — plain-language clarification **only**. Never treat it as authoritative,
   and never accept a line number, rate (e.g. Basiszins, Teilfreistellung %),
   or loss-bucket rule from it without verifying against the BMF/ELSTER source.

## PDF caveat

- Reading the PDF requires `poppler-utils` (for `pdftotext`), which is **not
  currently installed** on this WSL host. One-time fix:
  `sudo apt-get install poppler-utils`. Until then, the Read tool will fail on
  this file — don't assume it succeeded without checking.

## Hard rule

- Never assert a line number, rate, or loss-bucket rule sourced only from the
  PDF. Always cite (or go verify) the corresponding BMF circular or official
  form before treating it as correct.

## Cross-links

- See [[ibkr-tax]] for broker-statement-to-form mapping (Interactive
  Brokers / Freedom Finance specifics).

---
Source: docs/superpowers/specs/2026-07-21-agent-team-and-skills-design.md §3, §4.2
