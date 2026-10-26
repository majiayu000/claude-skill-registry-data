---
name: ibkr-tax
description: Consult when mapping Interactive Brokers (or, less precisely, Freedom Finance) statements to German tax forms — FIFO, FX, withholding, Teilfreistellung, Vorabpauschale.
---

# IBKR Tax Mapping (reference)

## Target forms

Interactive Brokers activity maps onto **Anlage KAP / KAP-INV / SO**, depending
on the instrument (plain securities vs. investment funds vs. private sale
transactions).

## No German tax certificate

- IBKR does **not** issue a German tax certificate (Steuerbescheinigung). All
  figures must be **derived from the Flex XML** statement export rather than
  read off a ready-made German form.

## FX

- Use **ECB reference rates** for currency conversion, applied **consistently**
  across buys, sells, and dividends — don't mix rate sources within one
  computation.

## Cost basis

- Use **FIFO** (first-in-first-out) lot matching, per BMF guidance.

## Fund taxation (§20 InvStG — Teilfreistellung)

Partial exemption rates by fund type:

- Equity funds: 30%
- Mixed funds: 15%
- Real-estate funds: 60%
- Foreign real-estate funds: 80%

## Vorabpauschale (§18 InvStG)

- Advance lump-sum taxation applies annually to fund holdings; compute per
  §18 InvStG, not as an afterthought at sale.

## Dividends & withholding

- Structure dividend income by security / country / withholding tax, and check
  against the relevant DBA (Doppelbesteuerungsabkommen / double-tax treaty) for
  creditable foreign withholding.

## Freedom Finance caveat

- The source material (kapitaltax) covers **Interactive Brokers only** and
  makes no Freedom Finance comparison. The principles above are usable for
  Freedom Finance "but not precisely" — treat any Freedom-specific difference
  as **project knowledge, not from this source**, and verify it against golden
  fixtures before relying on it.

## Cross-links

- See [[tax-system]] for the overall authority order (project docs → BMF/ELSTER
  → PDF) that governs how findings here get verified.

---
Source: kapitaltax.de/en/interactive-brokers-tax-return
