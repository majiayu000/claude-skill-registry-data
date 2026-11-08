---
name: seed-dataroom
description: >-
  Data Room Builder. Assembles the data room investors ask for and tells you
  what is missing. Lays out the nine standard folders (01 Company, 02 Pitch
  deck, 03 Financials, 04 Market, 05 Product, 06 Team, 07 Legal, 08 Cap table,
  09 Customers), checks the files against a 25-item checklist (present,
  missing, or stale by the date in the file name or its last change), writes
  seed/dataroom/INDEX.md describing every file, and lists what to share before
  a term sheet and what only after one. Flags what must never be in a data
  room: passwords, keys, ID documents, raw customer lists. It never uploads or
  shares anything. Use when the user says "build my data room", "what goes in
  a data room", "what am I missing for diligence", "the investor asked for
  the data room", "what can I share now", "make an index of my documents", or
  after a /seed-closer call goes well or /seed-terms reads a term sheet.
argument-hint: "[init | check | index | share-list]"
---

# seed-dataroom

The Data Room Builder gets the documents in order before an investor asks
for them, so the answer to "can you send the data room?" is a link the same
day, not a week of digging. It sets up the standard folders, checks what is
there against the list investors work through, warns when a file is too old
to send (a cap table from last quarter, metrics from June), and writes an
index so the investor can find everything. It also keeps the sequence
straight: the deck and the model go out after a first meeting; the cap table,
contracts and bank statements wait for a signed term sheet.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/dataroom.py" init                        # the nine folders in seed/dataroom/
python3 "${CLAUDE_SKILL_DIR}/dataroom.py" check --today 2026-10-26    # present / missing / stale
python3 "${CLAUDE_SKILL_DIR}/dataroom.py" check --stage before        # only what goes out before a term sheet
python3 "${CLAUDE_SKILL_DIR}/dataroom.py" index                       # writes seed/dataroom/INDEX.md
python3 "${CLAUDE_SKILL_DIR}/dataroom.py" share-list --stage before   # what to send now, and what waits
```

Every command takes `--dir` (default `./seed`) and `--today`; `check` and
`share-list` take `--json`.

## What it reads and writes

| file | what |
| --- | --- |
| `seed/dataroom/01 Company/` ... `09 Customers/` | the folders `init` creates; the user (or Claude, on request) puts files in them |
| `seed/config.json` | the startup's name, for the index title (optional) |
| `seed/dataroom/INDEX.md` | written by `index`: every file, what it is, its date, size, and when to share it |

## The checklist

| folder | before a term sheet | after a signed term sheet |
| --- | --- | --- |
| 01 Company | one-pager (90 days), business plan (90) | |
| 02 Pitch deck | the deck as a PDF (90) | |
| 03 Financials | the 36-month model (60), use of funds (90) | historical P&L and balance sheet (45), bank statements (45) |
| 04 Market | market sizing (180), competitor analysis (90) | |
| 05 Product | a demo (90), traction and KPIs (45), roadmap (120) | |
| 06 Team | founder bios (365) | org chart and hiring plan (180), IP assignments |
| 07 Legal | | incorporation and bylaws, board consents, IP, material contracts |
| 08 Cap table | | the cap table (30), signed SAFEs and notes, the option plan |
| 09 Customers | testimonials and reviews (180) | references (180), waitlist, pilots and LOIs as counts (90) |

The number is how many days old a file can be before it is stale. A file
matches an item when its name has one of the item's keywords ("deck",
"cap table", "model" ...) and it sits in that item's folder. Its date is the
date in the name (`Cap table 2026-10-01.xlsx`, `Metrics 2026-10.pdf`) when
there is one, else the day it was last changed, read in UTC so the
computer's time zone never moves it.

## Rules

- Files that look like a password, a key or token, a personal ID document,
  or a raw customer list are flagged "DO NOT SHARE" and left out of the index.
  Share counts of customers, never their names and emails.
- Files outside the nine folders are listed as loose; files the checklist
  does not know are listed as "other" (they still go in the index).
- Nothing is shared by this skill. The user picks the tool (Google Drive,
  Dropbox, DocSend, Notion) and who gets the link. Prefer one view-only link
  per investor; ask for an NDA before the "after" folders.

## Steps

1. `dataroom.py init`. Tell the user what goes in each folder.
2. Fill it from the pack: /seed-deck's `seed/deck.html` printed to PDF into
   02 Pitch deck, /seed-plan's `seed/plan.md` into 01 Company, /seed-model's
   export into 03 Financials, /seed-market and /seed-scout's results into 04
   Market. The rest (legal, bank, cap table) comes from the user; ask, never
   invent a document.
3. `dataroom.py check`. Read back what is missing and what is stale, most
   urgent first (the stage the user is at). Remove anything flagged DO NOT
   SHARE before going further.
4. `dataroom.py index` once the "before" items are in.
5. `dataroom.py share-list --stage before` when an investor asks after a
   first call; `--stage after` once a term sheet is signed (/seed-terms).
   The user shares the link themselves.

## Example: the reel

Leashly (fictional) after the Northlight call on Thursday, Nov 5. The room
has the one-pager, the business plan, the 10-slide deck, the model, the use
of funds for the $1.5M seed, the market sizing (APPA's $158B and 71M dog
homes) and the Rover / Wag! competitor analysis. `check --stage before`
shows 9 of 12 items present, the traction metrics from June stale (147 days,
limit 45), and the roadmap and testimonials missing. A stray `customer list
export.csv` is flagged DO NOT SHARE. Fix those three, run `index`, and the
deck-to-demo half of the room is ready to send to Maya the same day; the cap
table (86 days old, limit 30) gets refreshed before any term sheet.

## What it never does

- Never uploads, shares or emails a file, and never opens one's contents.
- Never creates a document to fill a gap: a missing item stays missing until
  the user provides it.
- Never promises that a complete data room gets a deal closed.
