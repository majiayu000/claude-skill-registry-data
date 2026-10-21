---
name: facts-check
description: >
  Read-only consistency check of any live site, on any stack. FACTS: one approved facts
  list (value, source, owner); scripts/facts_check.py reports every figure on the
  sitemap's pages that differs from it (text, titles, descriptions, alt texts,
  structured data, llms.txt) and retired phrases (old names, taglines, claims) still in use. POSITIONING: rules map page paths (/en/business/*) to an
  audience and the term each page owns; it lists pages that lost the term in title,
  meta description or H1/intro, as the starter's positioning test does. AI answer
  engines quote whatever figure and wording they find. Stdlib Python; runs weekly beside
  the AI check, in-house. Trigger phrases: "facts check", "check our figures", "do our
  pages contradict each other", "claims register", "is the old name still on the
  site", "positioning check of the live site", "do our pages still carry their terms".
---

# Facts check: one list of approved facts, every page compared with it

Two checks in one run, both read-only, both from the same reading of the live pages:
**facts** (every figure against the approved list, steps 1 to 4 below) and
**positioning** (every page against the term it owns, see "The positioning check").
Either can be used alone.

A site that has grown for years says the same thing in many places: the client count on
the home page, in the about page, in a press page, in the meta description and in the
structured data. They drift. One page says 500 clients and another 700, and an AI
assistant that reads both may quote either, or neither. People rarely notice, because
nobody reads 400 pages side by side. A script does.

The skill has two halves. **People decide what is true**: the facts list, with a source
and an owner for every value. **The script compares**: it reads the live pages and
reports every number that names a fact and differs from the list. It never edits a page
and never decides which of two figures is right.

## When to run

- First, once, to see how far a grown site has drifted. Expect findings.
- Then weekly, beside the AI check (`search-console-insights`, `geo_check.py`): the AI
  check shows what assistants believe, this check shows what the site says.
- After any change to a fact (a new client count, a new product name): update the list
  first, then run, and the report lists every page still on the old value.
- Before a launch or a campaign that quotes figures.

## Step 1: the facts list

The script is this skill's `scripts/facts_check.py`. In the commands below, the name in
braces stands for the folder this SKILL.md is in: Claude Code fills it in; with another
assistant, put that folder's path in its place. Run the commands in the folder where the
facts list and the reports should live. On a site with an `analytics/` folder kept off GitHub
(in the site folder, for each file you will write, `git check-ignore -q --no-index analytics/<file>` succeeds and `git ls-files -- analytics/<file>` succeeds and prints nothing), put the reports there so drift shows over time:
`mkdir -p analytics/<date>_facts-check`, then `--out analytics/<date>_facts-check/facts-report.md
--json analytics/<date>_facts-check/facts-report.json --history analytics/facts-history.csv`.

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/facts_check.py" --init facts.json
```

writes a starter file. Fill it **with the owner**, never from the pages themselves:
copying today's figures off the site would approve whichever one happened to be read
first. Each fact:

| Field | Meaning |
|---|---|
| `id`, `label` | A short key, and the name the report shows |
| `value` | The approved number, written as a number: `27000`, not `"27,000+"` |
| `unit` | `""` (plain numbers, default) or `"%"` (only percentages are tied to it) |
| `terms` | Words that follow the number when a page states the fact: `["client", "customer", "Kunden"]`. A term matches every word that starts with it, so `client` covers `clients` |
| `whole_words` | `true` makes the fact's terms match whole words only, so `Kunde` no longer matches `Kundenservice` (then list `Kunde` and `Kunden`). Default `false` |
| `before` | Phrases that come right before the number: `["NPS of", "founded in"]` |
| `window` | How many words after the number to look for a term (default 4, 1 to 12) |
| `also_accept` | Other numbers that are true too, e.g. a rounded `100` for `120` ("100+ clients") |
| `retired` | Known old values. They are reported as OUTDATED rather than MISMATCH |
| `source`, `owner`, `checked` | Where the value comes from, who vouches for it, when it was last confirmed. The report prints the source next to each finding |

Top level: `site` (the address), optionally `sitemap` (otherwise robots.txt, then
`/sitemap.xml`, `/sitemap-index.xml`, `/sitemap_index.xml`), optionally `pages` (a fixed
list instead of the sitemap), `extra_urls` (pages you do not own: a directory listing, a
review profile, a press article; reported as "not your site") and `retired_phrases`
(`{"text": "Old Name GmbH", "note": "renamed in 2024"}`).

Language: write `terms` and `before` in every language the site uses. Numbers are read
in English and German notation alike (`27,000`, `27.000`, `27k`, `2,5 Mio.`,
`1.5 million`, and `27 000` with a no-break or thin space). A plain space does not group
thousands, or "our 5 120 clients" would read as 5120. A minus sign counts: "NPS of -5" is
minus five, so it differs from an approved 5 (if your pages write a drop that way, such as
"-30%", list -30 in `also_accept`). A hyphen in "5-10", "2024-10-09" or "+/-3%" is no sign.

Structured data counts too: a number in the JSON-LD is read with its property name after
it, so `"numberOfEmployees": {"value": 500}` reads as "500 number of employees" and the
term `employee` ties it.

## Step 2: run it

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/facts_check.py" facts.json \
    --out facts-report.md --json facts-report.json --history facts-history.csv
```

- `--only /en/` checks one section first (useful on a large site, and for a first look).
- `--max-pages` (default 1000), `--delay` (default 0.5 seconds between requests),
  `--timeout`. A sitemap index is followed through at most 200 sitemap files; if it lists
  more, the report says how many were left unread.
- robots.txt is respected. One that answers with a server error, or not at all, keeps the
  site out, as the robots convention says; the report gives that reason. `--ignore-robots`
  reads disallowed pages too: only on a site the owner runs, never on someone else's.
  A page that redirects to an address robots.txt disallows is not followed there: the report
  lists it as skipped, with the address it led to. The script reads robots.txt as RFC 9309 does,
  with its own code and not Python's parser, which reads the same file differently from one
  version to the next: the longest rule that matches wins and an `Allow` wins a tie, `*` and
  `$` work, `%2F` is not a `/`, and a group that names `facts-check` shuts out the group of `*`.
  Sitemaps and robots.txt themselves are read wherever they redirect. Only http and https addresses are read: a sitemap entry or a redirect
  to file: or ftp: is never followed. An address with letters beyond ASCII (`/über-uns`, as many CMS sitemaps list it) is
  requested as a browser requests it (`/%C3%BCber-uns`). A sitemap entry that is not a web address (or is longer than 8,000 bytes) is left out and
  the report says how many; an entry in your own page list that is not one is listed as not read.
- The site's `/llms.txt`, written for AI assistants, is read too when it exists (not with
  `--only` or a fixed `pages` list). Pages over 5 MB are read up to 5 MB, and the report
  says so.

Exit code: **0** every tied number matches, **1** at least one finding, **2** the run
could not start or read no page of the site (a bad facts file, no sitemap found). A
run that read nothing is never reported as clean.

## Step 3: read the report with the owner

The report opens with one line of counts and a table per fact, then:

- **Mismatches**: a number tied to the fact that is neither approved nor known-old.
  Either the page is wrong, or the list is (a new figure nobody entered). Ask; do not
  guess which.
- **Outdated values**: a known old value still on a page. Usually a straight fix.
- **Retired phrases still in use**.
- **Facts no page names**: either no page states them, or the `terms` do not match how
  the pages phrase it. Look at one page that should name it and widen the terms.
- **Not checked**: pages that answered with an error, were skipped by robots.txt, or were
  not HTML (a PDF).

Each finding carries the page, where on the page and the sentence around the number,
with the number in bold, so the editor can find it. The places read are the page text,
the title, the meta description, the social description, the share title (`og:title`,
`twitter:title`, site name, author), image alt texts, the structured data and `llms.txt`.
Retired phrases are also searched in link addresses (links, canonical, `og:url`), so an old
domain is found; figures are not, since numbers in addresses state nothing. The report
prints each fact's source, owner and last-confirmed date next to its findings.

A false tie (a number that is not about the fact) means the rules were too loose: shorten
`window`, make a term more specific, or move it to `before`. Fix the list; never ignore a
finding without saying so in the report you hand over.

On a large site, most false ties come from three places:

- **Rows of figures** ("27,000+ talents 35+ languages 70+ countries in the talent pool"):
  give each figure in the row a fact of its own. The term that comes first after a number
  decides which fact it belongs to, so a countries fact keeps 70 away from the talent pool
  (two terms that start at the same word tie both facts; another fact's `before` phrase
  right before the number claims it too).
- **German compounds**: a term matches every word that starts with it, so `Kunde` also
  matches `Kundenservice`. Set `whole_words` and list the forms you mean.
- **Blog posts** use the same words in passing ("300 agents in a contact center", "45 euros
  per agent hour"). Prefer terms only the fact uses ("vetted", "freelance", "talents") and
  a window of 2, and check the blog with `--only` once before the weekly run.

## Step 4: fix, then keep it fixed

The script edits nothing. Fixes go through the site's own process: in a CMS as drafts
for the editors, in a repository as a pull request. After the fixes, run again: the
counts in `facts-history.csv` should fall to zero and stay there.

To run it weekly: a cron line or a systemd timer on Linux, launchd on macOS, or a
scheduled CI job, e.g.

```cron
0 6 * * 1  cd /path/to/workdir && python3 /path/to/facts_check.py facts.json --out facts-report.md --history facts-history.csv
```

Keep `facts.json` under version control next to the site or the team's docs: a change
to an approved fact is then reviewed like any other change.

## The positioning check

The same idea for words. The positioning skill (`website-positioning`) works out what a
site offers, for whom and in which category, and names the term each page owns. On a site
built with the starter, `tests/positioning.spec.ts` fails the build when a page loses its
term. This check applies the same rule to any live site, from its published pages, so a
corporate site on any CMS gets it too.

Add a `positioning` block to the facts file (the facts list can then stay empty):

```json
"positioning": {
  "rules": [
    {"pages": "/", "audience": "buyers", "term": "customer service outsourcing"},
    {"pages": ["/en/careers", "/en/careers/*"], "audience": "applicants", "term": "remote customer service jobs"},
    {"pages": "/en/business/*", "audience": "buyers",
     "title": [["CX outsourcing", "customer service outsourcing"]], "h1": ["outsourcing"]}
  ],
  "exempt": ["/privacy", "/imprint", "/en/legal/*"]
}
```

- **`pages`**: an address path, or a list of them. `*` matches the rest of the path, so
  `/en/business/*` covers every page below `/en/business/` (but not that page itself:
  list both, as for careers above). `/about/`, `/about.html` and `/about/index.html` all
  read as `/about`. **The first matching rule wins**, so put specific rules first.
- **`audience`**: a name for the group the page speaks to (buyers, applicants,
  investors). The report counts pages per audience. A large company usually has one
  positioning per audience: what that group would use instead, what you offer it, why
  it should believe you. The company itself (name, category, facts) stays the same for
  all of them.
- **`term`**: the shorthand. The phrase must appear in the `<title>`, the meta
  description, and the `<h1>` or the intro paragraph (so the heading can stay human).
- **Or per surface**: `title`, `desc`, `h1`, `body`, each a list of clauses that must
  all match. A clause is a phrase, or a list of phrases of which any one is enough. Use
  it where a page's surfaces legitimately differ. `body` checks the whole page text.
- **`exempt`**: legal and utility pages that own no term. Every other page with no rule
  is listed under "Pages with no positioning rule": a warning, not a finding.

Matching ignores case. The intro is the first `<p>` of `<main>` (else of `<article>`, else
of the page), as in the starter's test. A page that lost its term is a finding (exit 1, and
the `positioning_lost` column of the history file); the report names each surface and the
phrase it needs. Whether the page or the term changes is the team's call.

Where the rules come from: the positioning work (`website-positioning`, run once per
audience on a large site), written down in `POSITIONING.md` or the team's docs. On a
starter site, copy the `POSITIONING` map of `tests/positioning.spec.ts`: each key becomes
`pages`, the rest stays as it is.

## What it does not do

- **It does not run JavaScript.** Text a page adds only in the browser is not seen, and
  a count-up that renders 0 before its script runs is ignored rather than reported. For
  a site that renders everything in the browser, the report will say most facts are
  named nowhere.
- **It ties numbers by nearby words, not by meaning.** "We answer 30,000 agent calls a
  day" next to the term `agent` is tied to an agent count. The rules are kept narrow by
  default: terms after the number, a short window, a comma or full stop ends the search,
  a zero is ignored unless the fact is 0, and so is a plain year right after "in", "since",
  "seit", "founded", a date ("March 2026", "September 4th, 2026", "4. Sept. 2026"), © and
  the like unless the fact is itself a year (a four-digit count such as "über 2000 Kunden"
  is still read). Every
  finding shows its sentence, so a person decides.
- **It checks numbers and exact phrases**, not paraphrased claims ("market leader").
  Retire such claims as phrases, or leave them to the content review.
- **It reads pages, not PDFs or images.** A figure in a picture is invisible to it, and
  to most AI assistants too.
- **It does not decide what is true.** The facts list does, and people keep the list.

## Related

- `search-console-insights`: the weekly AI check (`geo_check.py`). Its branded
  question, read for accuracy, shows which wrong figure has already spread to the
  assistants.
- `business-listings-setup`: checks that profile links resolve; this check's
  `extra_urls` reads what those profiles say.
- `ai-seo`, `schema-markup`: how to state facts so assistants can quote them.
- `website-positioning`: the same idea for words: one approved positioning term per
  page, held by a test on sites built with the starter.
