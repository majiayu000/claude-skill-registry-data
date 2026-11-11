---
name: website-new-page
description: >
  Add a page to a site, or rewrite one, so it is worth reading and findable before it is built.
  Writes one page document (a brief, then the full draft), has a fresh pair of eyes judge it for
  the reader, for search and AI answers, and for originality, takes the owner's go on the exact
  sentences, builds, then checks the build kept the approved text. It calls the checks other
  skills own (website-seo-geo, ai-seo, seo-audit, copywriting, search-console-insights,
  website-review) and does not repeat them. Use for a new page, a new article, a page rewrite,
  or "is this page any good". Trigger phrases: "add a page", "new page", "write a page about",
  "new article", "rewrite this page", "this page feels thin", "what should this page rank for",
  "review the draft before we build it", "move this page from the old site".
---

# New page

A page can be accurate and still thin: it answers no search, has no FAQ, says nothing the top
results do not. A review of the finished code cannot see that; it checks that the page is built
right, not that it is the right page. This skill moves the judgment in front of the build, where
a change costs a sentence and not a round of code review.

**What you produce:** one page document, `docs/pages/<slug>.md` unless the site keeps such files
elsewhere. It has two parts: a brief of one page at most, then the full draft copy. Start from
`${CLAUDE_SKILL_DIR}/templates/page-document.md`.

## The steps

**1. Intake.** Ask the owner these five questions, unless the request already answers them:

1. Who reads the page?
2. What do they type into a search box, or ask an AI?
3. What should they do after reading?
4. What can we say that others cannot (proof, our own experience, a point of view)?
5. For each document, link or note they hand over: is it a **source**, or **ideas only**?

Ideas-only input may suggest questions to research. It never backs a claim, a citation or a
link, unless the owner reclassifies it after you have read the source itself.

**2. Research.** Read the top results for the main query and ask an AI the same question. Save
what they cover and what they miss in a research file (`docs/pages/<slug>-research.md`), with the
address of every source you read. Read each source at the source, not through a summary. Where
the site has Search Console data and the `search-console-insights` skill is installed, that skill
shows what the page's neighbours already rank for; otherwise skip this.

**3. Write the page document.** The brief fills its fields in plain words: the page type (an
article that answers a question, a home page, a product or service page, a contact or legal
page: the review judges depth and FAQ by it), reader, main query and
two or three related ones, title, H1 and description led by the search words, the one original
angle, the outline with what each section must teach, the graphics, four to six FAQ questions
that each add something the body does not, the inputs with their labels, a claims table, an
outbound-links table, and "what we will not say". Every proof point must be one the reader can
open or understand without access: no internal ticket, pull request or repository names on a
public page. Then write the draft copy in full, to that outline. Drafting is cheap; reviewing
copy after it is built is not.

Call the other skills for their own questions, and do not restate their rules here:

| The brief asks | Ask |
|---|---|
| Title and description length, schema, `llms.txt` | `website-seo-geo` |
| Will an AI answer quote this page? | `ai-seo` |
| Does the page match the search intent? | `seo-audit` |
| Is the copy clear and in the owner's voice? | `copywriting` |
| What does the site already rank for? | `search-console-insights`, where it is installed |

**4. Content review.** One reviewer reads the page document and the research file with the prompt
in `${CLAUDE_SKILL_DIR}/references/content-review.md`. It asks three things: does the page answer
its reader (including graphics and proof the reader can check), is it findable (search, AI
answers, who wrote it and why they know), and is it original next to the top results? The answer
is a ranked list of BUG, RISK and NIT findings.

- **Who reviews is the owner's choice. The default is your own AI**, started fresh: a subagent
  that did not write the page or, where yours cannot start one, a new conversation with the
  three texts pasted in. That needs no second AI provider. A second reviewer is the owner's
  call, as `website-review` says for all site work. If the owner has the `independent-review`
  skill working, `independent_review.sh <page document> --content --evidence <research file>`
  sends the same prompt to its seats.
- Two rounds at most. Fix each finding, or list it for the owner to accept or reject in the go.
  A fix that changes the meaning of a sentence gets one more read.

**5. The owner's go.** Show the owner the reviewed document and a short note of the findings still
open, each with your recommendation. Their go covers the exact sentences, not an outline. Write
"approved by the owner on <date>" at the top of the page document.

**6. Build** the page and everything the site wants around it: the route, `llms.txt`, the share
card, an inbound link from a page that already ranks, and the schema (`FAQPage` where there is a
FAQ). Tests should check that contract, the sentences the site marks as locked (its
`AGENTS.md` or `CLAUDE.md` says which), and the claims-table rows the owner signed off. They need
not pin all of the body copy: the next step watches it.

**7. Check the build kept the text.** After the site builds, run:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/check_page_text.py" docs/pages/<slug>.md dist/<slug>.html \
  --title-suffix " | Site name" --skip nav,footer,aside,.byline
```

It compares the draft with the built page's title, description, FAQ schema and every sentence in
its `<main>` (the whole body if there is none), after folding whitespace, HTML entities and
typographic quotes. Dashes and every other character are compared as written. Exit
0 means the build kept the text. Exit 1 lists every changed sentence: put that list in the PR for
the owner to read, as it is. Components that add their own text (a byline, a button) are named
with `--skip`, as tags or `.classes`; if the check names a sentence the owner did not approve,
that is the finding. Exit 2 means the check could not read its input.

**8. Review the code** with the site's usual review (`website-review`, or `independent-review`'s
diff gate where the owner has chosen it). By now the copy has been judged, so this round checks
the build.

## Moving a page from an old site

Use this when the intake names an old address: the page exists on WordPress, Contao, Wix,
Squarespace or another tool, and the new page replaces it. A page like that already has an
address, links pointing at it and searches it ranks for. A rewrite can drop the one section
people came for, or change the address without a redirect, and the ranking is gone before anyone
notices. Everything above applies. These steps change, and one is added:

**1. Intake** also asks for the old address, written as Search Console lists it (closing slash
included), whether the old site had Search Console and under which property, and the planned
go-live date. The old and the new address may sit in different properties. If the new address is on
another domain, the old host has to forward each old address itself: the new site's redirect file
cannot answer for it. This mode does not set that up; the page document and the go say who does.

**2. Research** starts from the old page.

- *Search Console.* With the `search-console-insights` skill, run its `gsc_query.py` with
  `--site <property> --page <old address> --days 90 --no-csv` for the queries, clicks, impressions
  and position, and copy its query table (up to 100 queries; it says when it cut some) into the research file under **Old page, Search
  Console**. Once the old site is gone, give the 90 days as `--start` and `--end` instead, ending
  the day before go-live. Without Search Console, say so in the research file: the owner names the
  queries and sections that matter, and the four-week check below is skipped, with that reason
  written in the page document.
- *The old page.* Save its HTML before the site changes (the owner's saved copy, or a download of
  the live page). The research file gets a section **Old page** from that file: every heading with
  its text, and every download, form and embed with its target (the file's address, the form's
  action, the embed's source). The reviewer reads the research file, so this section is how the
  old page reaches it.

**3. The page document** gets two more fields. The **address decision**: keep the address, or name
the new path. The **section table**: one row for each section of the old page, by its old heading,
marked *kept*, *rewritten*, *merged into* another section, or *dropped* with the reason. Downloads,
forms and embedded media are rows too, each with its target from the "Old page" section, so one
that disappears without changing the visible text is still listed. A download that moves gets a
redirect like a page.

**4. Content review.** The prompt for a moved page carries one more question (in
`${CLAUDE_SKILL_DIR}/references/content-review.md`): does the section table account for every section
of the saved old page, and does the draft still answer each query that earned the old page clicks?

**5. The go** lists every dropped section by its old heading and every dropped query by name, each
with its reason, and the owner's go covers them by name. Put the two four-week windows (step 9) and
their dates into the note.

**6. Build** writes the redirect when the address changes. With the `wordpress-inspector` skill's
`make_redirects.py`, run from a folder beside the saved site, not in the site's repository: a text
file with the old address on one line, `--draft moves.csv`, then fill in the new path and run
`make_redirects.py old.txt moves.csv --site <new site> --out redirects.txt`. It writes a line for
the address and one for its closing-slash twin. Add those lines to the site's `public/_redirects`
yourself, without the two `#` header lines (they say the file is regenerated).
Read the script's counts and exit code first. The script refuses to write over a file it did not write. After
go-live, run that skill's `check_move.py old.txt <new site> --moves moves.csv` and read its report.

**9. The four-week check.** The page document records two fixed windows of 28 days. *Before* ends
the day before go-live and is pulled on the old address. *After* starts the day after go-live and is
pulled on the new address. Pull each with `gsc_query.py --site <property> --page <address> --start <day> --end <day>
--by-date --no-csv --pages-csv <window>-pages.csv`, so a rerun reads the same days and the report says whether the window is
complete: the property's own rows by date must reach its last day. Until it says so, judge nothing and pull again a few days later; three days after
the end is when to try first, not proof. If it still says "Not complete" a week after the end, say
so in the note to the owner and judge by hand in the Performance report. For `<window>` use `before`, `after` and, for the old
address's own after window, `old-after`, so no pull writes over another's file. Run this at the date the page document and the go note
name; the owner runs it, nothing is scheduled. Where the page moved to a new address, the old address's own
*after* window is never judged on its own: after a working redirect its numbers fall by design. Its
clicks still count in the page total below.

A *main query* has at least 10 clicks in the before window. It is a finding when the after window
shows less than half those clicks, or when its row is missing from the new address's query table and
`gsc_query.py --query "<query>"` with the same dates shows the new address gone from the pages that
serve it. Search Console hides rare queries, so a missing row is never read as zero: where the owner
cannot see the query in the Performance report either, write "unknown". A complete after
window with no rows for the new address at all is a finding too, never a reason to wait.

The *page total* is the page's own row in each window's pages file. Search Console leaves rare
queries out of the query rows, so this row often counts many more clicks than they add up to.
Before, the old address's row; after, the new address's row. Where the page moved to a new
address, add the old address's row for the same days (from the old address's property if it is
another one); a kept address is one row, counted once. Fold the spellings as under "More than ten
pages". A page with at least 10 clicks before is a finding when its after total is less than half
of them. On a small site this is often the only rule that can fire: its pages seldom have a query
with 10 clicks. Where two rows were added, leave the total's position blank: positions do not add.

Give the owner a table that starts with the page total, then every query the before report lists
with at least 1 click, largest first, with clicks, impressions and position for both windows. Mark
each row, the page total too, *main* (10 or more clicks before) or *for information*. A row for
information is never a finding, whatever its numbers: at a few clicks a month a fall can be chance.
It is there so the owner sees what moved, and the note says so. Where its query has no row in the
after report, write "not in the table", not 0; a main query's missing row follows the rule above.
If either report says "Showing 100 of N queries", the note says how many were left out. Give the
findings below the table. They go to the owner, not into an automatic rewrite.

**More than ten pages.** Sort the pages before the full mode runs. Start from the full address list
(`wp_inventory.py`'s `urls.csv`, or the sitemap for another tool) and join the clicks and impressions
of every page over 90 days: `gsc_query.py --pages-csv pages.csv` writes them. Search Console lists
the same page under several spellings (scheme, www, closing slash): fold only the spellings the old
site itself sends to one address, add those up before joining, keep the rest as separate rows, and
list every row of `pages.csv` that matches no address. An address with no row returned no
impressions in those 90 days; that is not proof of zero, and the triage deletes nothing. Every address lands in one group:

- **Move with care:** the pages that together bring 80% of the clicks. They get the full mode.
- **Let go?** Pages with no clicks and no impressions, listed for the owner. Only the owner decides,
  and checks Search Console's Links report for any that others link to.
- **Carry over:** every other address, with text and address kept, title and description checked,
  and no content review.

Without Search Console the owner names the "move with care" pages, the rest carry over and nothing is
proposed to let go. The 80% line is a judgment, not a measurement; the owner can move a page between
groups.

`check_page_text.py` does not find dropped text: a rewrite changes most sentences, so it would list
the whole page. The section table, checked by the reviewer against the saved old page, does that job.

## Rules that keep the process short

- **Judge the page before building it.** A copy change after the build costs a code review.
- **Words in tests are for the sentences that must not change.** Not for every paragraph.
- **The research file is evidence, not decoration.** A review that has no research file cannot
  say a page is thin, and says so.
- **The reviewer returns findings, not orders.** The owner decides.

## Done means

- The page document says "approved by the owner" with a date, and its draft is the text on the page.
- `check_page_text.py` exits 0, or its list of changed sentences is in the PR and the owner has read it.
- The site's own checks and review are green.
- You say plainly what you did not check: whether the page ranks, which only time shows.
