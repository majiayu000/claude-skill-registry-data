---
name: pb-offer
description: >-
  Draft a client offer with line items priced only from your price list, and
  send it only after your GO. Use for "write an offer", "quote for this
  client", "draft a quote", "price this job".
category: bdb-core
kind: playbook
trigger: ["write an offer", "quote for this client", "draft a quote"]
inputs: [client_brief, price_list]
requires:
  skills: [bdb-eventagency-skill, copywriting]
  agents: []
  mcps: []
  store: []
go_points: [send offer]
outputs: ["offer.md", "run-log.md"]
verify: "every unit price exists in the price list; total recomputed from line items matches"
difficulty: beginner
est_time: 10-20 min
---

# Client offer
What you get: a client offer with line items, priced only from your price list.

## Inputs
- A client brief — a text or document file
- A price list file — item and unit price per line
- A save folder — asked once; default `./pb-offer-<date>/`

## Steps
1. Ask once — save folder, client brief, price list; also the VAT rate and the offer validity → `run-log.md` — the files are readable
2. bdb-eventagency-skill (section "2. Client & Project Intake") — brief → scope and line items; an item with no price in the list is marked `no price`, never priced by guess
3. Write `offer.md`: items, quantity, unit price, line total, net total, VAT at the rate you gave, gross total, validity — every unit price exists in the price list; the net total recomputed from the line items matches
4. copywriting — brief and `offer.md` → the cover text at the top of `offer.md`; no claims beyond the brief
5. Show `offer.md` in full and apply your edits until you approve — approval logged
6. [GO] Send the offer through a connector you name, or send it yourself — show the recipient (name + address, `?` blocks sending until you fill it) and the full text first. The run stops here until the human types GO. The GO covers exactly the recipient and message shown and nothing else; a different or added recipient needs a fresh GO. The go-gate hook does not guard sending: this [GO] is the only guard.

Run log: `run-log.md` in the save folder. One line per step as it completes (`N. done|skipped|failed — file — check result`), and `WAITING FOR GO: <step>` at the gate. Anything other than the literal GO (case-insensitive) is not a GO. If a check fails, stop, write the failure into the log and tell the user.
