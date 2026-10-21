---
name: wordpress-inspector
description: >
  Count what a live WordPress site holds before anyone promises to move it, write the new
  site's redirects, and check them after the move. Read-only toward the site: no login, no
  backup. scripts/wp_inventory.py counts each content type the REST API lists, where the
  sitemap disagrees, page builders and forms, and whether the count is complete.
  scripts/make_redirects.py turns its address list and the owner's decisions into
  public/_redirects lines. scripts/check_move.py asks the new site for each old address and
  names those missing, sent home or not where the decisions say. Stdlib Python. Trigger
  phrases: "how big is this WordPress site", "count the pages", "WordPress migration
  estimate", "what plugins does this site use", "write the redirects", "redirect map for the
  move", "did every page make the move", "check the redirects after the move", "are any old
  addresses broken".
---

# WordPress inspector: count the site before you promise to move it

A move goes wrong at the start, when someone guesses the size of the site. A crawler's copy
looks complete and is not: it misses whatever no page links to and saves error pages under
real page names. This skill asks the site itself, which knows how many records it has.

It reads; it never writes to the site, logs in, or copies its text. Its scripts write their
reports and files on your own computer only.

## When to use it

- Before quoting or planning a move from WordPress to a new site.
- To check a crawler's copy against the truth.
- To learn what a site is built with: page builder, forms, plugins that keep their own data.

Run it only on a site you own or are asked to look at.

## Run it

The three scripts are this skill's `scripts/wp_inventory.py`, `scripts/make_redirects.py` and
`scripts/check_move.py`. In
the commands below, the name in braces stands for the folder this SKILL.md is in: Claude
Code fills it in; with another assistant, put that folder's path in its place. Run the
commands in the folder where the reports should live.

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/wp_inventory.py" https://example.com --out ./inventory
```

It pauses one second between requests and stops after 100, which covers a site of a few
thousand records. If the report says the request limit was reached, run it again with a
higher `--max-requests`. It obeys the site's robots.txt, wildcards included, and asks only
the host you name. A robots.txt that is refused or cannot be read stops the run.

It writes three files into the folder:

- `inventory.md`: the report. Read this first.
- `urls.csv`: one row per address, for a spreadsheet.
- `inventory.json`: the same numbers for a program.

Keep that folder out of any public repository: it lists another party's addresses.

## Read the result with the owner

1. **Is the count complete?** The report's first lines say so. If not, it names each gap.
   Clear the gaps before you estimate. Exit code 0 means complete, 1 incomplete, 2 the run
   could not start. Two kinds of gap name a sitemap address:
   - marked "a usual address, only tried": the script guessed it, because robots.txt names
     no sitemap. If the note says the file was "sent as text/html", open the address in a
     browser: an ordinary web page there means the site keeps no sitemap at that address,
     and this gap is settled. Any other note about such an address (the site refused or
     was busy, the file could not be unpacked, or it was sent as something else) a browser
     does not settle: run the count again later.
   - not marked so: robots.txt or a sitemap index names that file, so the site says a
     sitemap is there and the count lacks its addresses. A web page in its place is an
     error on the site. Have it repaired, or count those pages another way.
2. **Content types.** The count covers the types the site's REST API lists, apart from
   WordPress's own internal ones (menus, templates, patterns, styles, fonts); media is one
   number. Posts and pages are WordPress's own. Any other type comes from a plugin (events,
   speakers, products, jobs): ask who keeps it up to date, and how often it changes, before
   you price it.
3. **"Left as raw shortcode text".** The text the site hands out for such a record holds a
   code such as `[vc_row]` or `[gallery ids="1,2"]` where content should be: a page builder,
   a gallery or another plugin wrote it. This is a sign, not proof. Open two or three of
   these pages in a browser and compare them with their rows in `urls.csv`; where the page
   shows what the text lacks, plan to rebuild it by hand.
4. **Forms and page-builder marks.** These are found by the traces each plugin leaves in the
   text, so a form drawn another way is not counted. Walk the site's menus once to check.
   Each form needs a new home on the new site: ask where its entries should go.
5. **Sitemap addresses no record explains.** A plugin or a listing page stands behind each
   group. Decide for each: keep, redirect, or let go.
6. **Published but not in the sitemap.** Often hidden on purpose. Ask before moving them.

## What it cannot see

Say this to the owner before they rely on the numbers:

- Drafts, private records and anything behind a login. A password-protected record may be
  counted, but its text is not read.
- A content type the site's REST API does not list.
- Content a plugin draws inside a page, such as a directory shown in pop-ups. It counts as
  one page.
- Fields a plugin keeps to itself, such as an event's start time.
- The media files themselves, redirects set inside WordPress, and form entries.

Those need the site's backup or a login. The language of each record is a guess, for German
and English only; treat it as a hint.

## Between the count and the check: write the redirects

Every old address needs a decision: kept at the same address, moved to a new page, or let go.
`make_redirects.py` turns those decisions into lines for the new site's `public/_redirects`,
the file Cloudflare reads its redirects from.

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/make_redirects.py" ./inventory/urls.csv --draft ./inventory/moves.csv
```

This writes `moves.csv`: one row per old page, with an empty `new_address`. Go through it with
the owner and write in each row one of:

- a path on the new site, as the site shows it: `/kontakt` (a Croftweaver site uses no closing
  slash);
- a full address on another host, such as a shop;
- `keep`: same page, same address;
- `let go`: dropped on purpose. Agree these with the owner: they are the record of what was
  given up.

Open the sheet through Excel's Data → From Text/CSV, or in Numbers or Google Sheets, and save it
as CSV UTF-8. Then:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/make_redirects.py" ./inventory/urls.csv ./inventory/moves.csv --site https://example.com --out ../new-site/public/_redirects
```

`--site` is the new site's live address. Keep `moves.csv` in the inventory folder, out of the
site's repository: only `_redirects` goes to the site. The script never overwrites a file
unasked. `--replace` writes over a `_redirects` it wrote before, and never over one written by
hand: merge those lines into the sheet and the address list first.

What it writes, and why. Cloudflare matches the closing slash, the letter case and each
%-escape exactly (measured on two live kit sites), so a moved page gets a line for `/old` and one
for `/old/`, and an address with an escape such as `%c3%bc` gets both cases. A chain (`/a` to
`/b` to `/c`) is written as `/a` to `/c`. No line sends a page to itself.

What it refuses, and lists: an address with a query (`/?p=12`), which `_redirects` cannot
match; a deep page pointed at the home page, which check_move would report as sent home; a new
address it cannot read; a decision for an address the list lacks (add it to `urls.csv` first).
A page with two different decisions, a loop, or more than the 2,000 lines Cloudflare reads
writes nothing at all.

Exit code 0 means the file was written and every address has a decision; 1 that it was written
with findings, undecided pages among them, so a move can go ahead in steps; 2 that nothing was
written.

## After the move: does every old address still lead somewhere?

This is the step where a page nobody rebuilt, or a redirect nobody wrote, goes unnoticed.
`urls.csv` from the count is the list to check against. It holds the records and sitemap
entries the count found; a listing page the sitemap left out is not in it, so add such
addresses to the file by hand if they matter.

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/check_move.py" ./inventory/urls.csv https://preview.example.com --out ./move-check
```

Give it the new site's deployed address, the preview or the live one. A preview server on
your own computer may not apply the host's redirect rules; where it does not, every redirect
reads as missing. Any list of old addresses works in place of `urls.csv`: a text file, one
per line. `/a` and `/a/` are asked separately, since a site can answer the two differently.

Read `move-check.md` with the owner. Each old address ends as one of:

- **kept**: the new site answers at the same address.
- **redirected**: the new site forwards it to another of its pages.
- **off the site**: forwarded to another host, such as a shop. Not followed; the report
  lists each with its target, for you to check.
- **missing**: the new site says "not found". Build the page or write the redirect.
- **sent home**: a deep address forwarded to the home page. A reader who follows an old link
  to it lands on the front page and has to search again, so it counts as a finding. Point
  it at the page that replaced it. The old home address itself (`/`, `/index.php`,
  `/index.html` or `/index.htm`) may go wherever the new home page lives.
- **unreadable**: the new site refused or was busy. Run it again.
- **not as decided** (with `--moves`): the address answers, but not where `moves.csv` sends it.
  A redirect to the wrong page, or the old page still served.

Some pages are dropped on purpose. Write those addresses into a text file, one per line, and
pass it with `--let-go let-go.txt`; they then read **let go**. Agree that list with the owner:
it is the record of what was given up.

With the decisions sheet, the check also asks whether each address ends where the owner decided,
and its `let go` rows need no separate list:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/check_move.py" ./inventory/urls.csv https://preview.example.com --moves ./inventory/moves.csv --site https://example.com
```

`--site` names the live address the decisions may use; it matters when you check a preview.

The report also counts temporary redirects (302, 303, 307), and `move-check.csv` says which.
If the move is for good, make them permanent (301 or 308).

Exit code 0 means every address is accounted for, 1 that there are findings, 2 that the run
could not start (`moves.csv` that cannot be read is one reason). One reason for 2: asked for an address that cannot exist, the new site
did not answer with a plain "not found". Give it a real "not found" page first, or nothing
can be checked.

## What this skill does not do

It does not move anything. It counts before the move, writes the redirects from the owner's
decisions, and checks after it, so that each step rests on numbers.

## Tests

```bash
python3 -m unittest discover -s "${CLAUDE_SKILL_DIR}/scripts/tests"
```

Stub sites on 127.0.0.1, no real requests. In the toolkit's own folder,
`make test-wordpress-inventory` runs the same.
