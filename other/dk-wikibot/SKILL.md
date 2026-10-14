---
name: dk-wikibot
description: Fetch, search, and extract information from Wikipedia, Wikidata, or any MediaWiki-based wiki using pywikibot. Use when the user asks to scrape Wikipedia articles or infoboxes, iterate over Wikipedia categories, query Wikidata entities and claims (structured facts), look up award winners, historical lists, or biographical data from Wikimedia projects. Also triggers on phrases like "use the wikibot skill", "look up on Wikipedia", or "query Wikidata". Does not handle live web searches, non-Wikimedia sites, or tasks requiring a logged-in Wikipedia account.
compatibility: "Requires Python 3.8+, pywikibot, mwparserfromhell (uv add pywikibot mwparserfromhell). Read-only tasks require no credentials."
license: Apache-2.0
disable-model-invocation: true
metadata:
  author: dushyantkhosla
  version: "1.0"
  opencode/autoinvoke: false
---

# Pywikibot Skill

Pywikibot wraps the MediaWiki API. For **read-only** tasks (the common case), no credentials are
needed — set `PYWIKIBOT_NO_USER_CONFIG=1`.

Always write a standalone Python script and execute it via `bash_tool`. Do not import pywikibot
interactively — it makes blocking network calls and must run as a script.

## Setup

```bash
uv add pywikibot mwparserfromhell
export PYWIKIBOT_NO_USER_CONFIG=1
```

Every script must start with:

```python
import os; os.environ['PYWIKIBOT_NO_USER_CONFIG'] = '1'
import pywikibot
```

---

## Step-by-step instructions

### 1. Fetch a Wikipedia article

```python
import os; os.environ['PYWIKIBOT_NO_USER_CONFIG'] = '1'
import pywikibot

site = pywikibot.Site('en', 'wikipedia')
page = pywikibot.Page(site, 'Grammy Award for Best Rock Song')
print(page.text[:3000])  # raw wikitext — inspect this first before parsing
```

Always inspect `page.text` before writing any parser. Wikitext structure varies per article.

### 2. Parse wikitext

```python
import mwparserfromhell
wikicode = mwparserfromhell.parse(page.text)
templates = wikicode.filter_templates()  # e.g. {{won}}, {{nom}}, {{infobox}}
```

Alternatively, use regex directly on `page.text`:

```python
import re
year_sections = re.split(r'\n==\s*(\d{4})\s*==\n', page.text)
links = re.findall(r'\[\[([^\|\]]+)(?:\|[^\]]+)?\]\]', block)
```

### 3. Iterate a Wikipedia category

```python
import os; os.environ['PYWIKIBOT_NO_USER_CONFIG'] = '1'
import pywikibot

site = pywikibot.Site('en', 'wikipedia')
cat = pywikibot.Category(site, 'Category:Grammy Award for Best Rock Song')
for page in cat.articles(total=50):
    print(page.title())
```

Use `cat.subcategories()` for subcats, `cat.members()` for everything.

### 4. Query Wikidata via SPARQL

Best for clean structured data (winners, dates, relationships). Find the QID for any entity at
https://www.wikidata.org/wiki/Special:Search first, then use it in the query.

```python
import os; os.environ['PYWIKIBOT_NO_USER_CONFIG'] = '1'
from pywikibot.data import sparql

QUERY = """
SELECT ?year ?songLabel ?artistLabel WHERE {
  ?award wdt:P31 wd:Q1377714 .       # instance of Grammy Award for Best Rock Song
  ?award wdt:P585 ?date .
  BIND(YEAR(?date) AS ?year)
  FILTER(?year >= 2010)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY ?year
"""
results = sparql.SparqlQuery().select(QUERY)
for row in results:
    print(row)
```

### 5. Fetch a Wikidata item directly

```python
import os; os.environ['PYWIKIBOT_NO_USER_CONFIG'] = '1'
import pywikibot

site = pywikibot.Site('en', 'wikipedia')
page = pywikibot.Page(site, 'Douglas Adams')
item = pywikibot.ItemPage.fromPage(page)
item.get()
print(item.labels.get('en'))
print(item.claims)  # dict of property_id -> list of Claims
```

---

## Decision guide

| Task | Approach |
|------|----------|
| Award winner lists, formatted tables | Wikipedia `page.text` + wikitext parsing |
| Clean structured facts (dates, IDs, relationships) | Wikidata SPARQL or `ItemPage` |
| Category membership | `Category.articles()` |
| Multiple entities at once | Wikidata SPARQL (most efficient) |

---

## Examples

### Find all Grammy Best Rock Song winners since 2010

```python
import os; os.environ['PYWIKIBOT_NO_USER_CONFIG'] = '1'
import re, pywikibot

site = pywikibot.Site('en', 'wikipedia')
page = pywikibot.Page(site, 'Grammy Award for Best Rock Song')
text = page.text

# Inspect first — then adapt the pattern to what you see
print(text[:2000])

# Split by year section headers
sections = re.split(r'\n==\s*(\d{4})\s*==\n', text)
# sections alternates: [preamble, year, content, year, content, ...]

results = []
for i in range(1, len(sections) - 1, 2):
    year = int(sections[i])
    if year < 2010:
        continue
    content = sections[i + 1]
    won_blocks = re.findall(r'\{\{won\}\}.*?\n\|-', content, re.DOTALL)
    for block in won_blocks:
        links = re.findall(r'\[\[([^\|\]]+)(?:\|[^\]]+)?\]\]', block)
        if links:
            results.append({'year': year, 'song': links[0], 'artist': links[1] if len(links) > 1 else ''})

for r in results:
    print(f"{r['year']}: {r['song']} — {r['artist']}")
```

---

## Common edge cases

- **`NoPageError`**: page doesn't exist — check spelling or follow a redirect.
- **`IsRedirectPageError`**: follow with `page.getRedirectTarget()`.
- **Template name varies**: the winner template may be `{{won}}`, `{{winner}}`, `{{yes}}`, etc. Always check `page.text` first.
- **SPARQL timeouts**: add `LIMIT 100` or tighten filters.
- **Rate limits**: pywikibot has built-in throttling; don't add manual `sleep()`.

## LLM-based extraction (PydanticAI + LMStudio)

For pages with messy, inconsistent, or deeply nested wikitext, skip regex/template parsing entirely
and pass `page.text` directly to a local LLM. The LLM handles wikitext syntax natively and returns
a validated Pydantic model. This is the most agent-native approach.

**See the `free-models-pydantic-ai` skill for full setup and usage patterns.** The pattern here is:

1. Fetch `page.text` via pywikibot as usual
2. Truncate to fit context window (8000 chars is a safe default for most local models)
3. Pass to a PydanticAI agent with a structured `output_type` matching your desired schema
4. Get back a validated Pydantic model — no regex, no template parsing

**When to use this over regex/mwparserfromhell:**

- Page structure is inconsistent across years
- Templates are non-standard or undocumented
- You need to extract prose context alongside structured fields
- Rapid prototyping — skip the wikitext archaeology

**Caveats:**

- Local models may hallucinate values — validate against known data if accuracy is critical
- Slower and heavier than SPARQL or regex for well-structured pages; use those first

---

See [references/api.md](references/api.md) for a full API reference of commonly used classes and methods.
