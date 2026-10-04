---
name: pb-invoice-check
description: >-
  Check invoices and receipts line by line against your offers and list what
  matches, what differs and what has no offer. Nothing is paid or sent. Use
  for "check my invoices", "match invoices to offers", "does this invoice
  match the quote".
category: bdb-core
kind: playbook
trigger: ["check my invoices", "match invoices to offers", "invoice check"]
inputs: [invoices_folder, offers_folder]
requires:
  skills: [pb-offer]
  agents: []
  mcps: []
  store: []
go_points: []
outputs: ["invoices.csv", "check.md", "run-log.md"]
verify: "every PDF in the folder has exactly one row; every total recomputed from its lines"
difficulty: beginner
est_time: 10-20 min
---

# Invoice check
What you get: invoices and receipts sorted and checked line by line against the matching offers.

## Inputs
- An invoices folder with PDFs
- An offers folder — the `offer.md` files from pb-offer
- A save folder — asked once; default `./pb-invoice-check-<date>/`

## Steps
1. Ask once — save folder, invoices folder, offers folder → `run-log.md`; list the PDFs. `pdftotext` is not installed, so you read each PDF with the harness PDF read; a PDF it cannot read becomes a row with status `unread` and the run continues — you may paste its text later
2. Per readable PDF → `invoices.csv`, columns file, vendor, date, number, net, VAT, total, status — a field that is not on the invoice is `?`; every PDF in the folder has exactly one row
3. Match each invoice to an offer by vendor, client and items → matched offer named in `invoices.csv`; no offer found → status `no offer`
4. Write `check.md`: per invoice match / mismatch (which line, how much it differs) / no offer / unread — every total recomputed from its lines; the recomputed value and the printed value are both shown
5. Show `invoices.csv` and `check.md` in full and apply your edits until you approve — approval logged

Nothing is paid or sent, so there is no GO step. The run only reads the two folders and writes into the save folder.

Run log: `run-log.md` in the save folder. One line per step as it completes (`N. done|skipped|failed — file — check result`). If a check fails, stop, write the failure into the log and tell the user.
