---
name: wikicommit-search
description: Search the wiki's pages by keyword, expanding synonyms and searching each configured language. Use this whenever someone asks what the wiki says about something, wants to find a page, asks whether a topic is already covered, or asks which pages mention a term — even if they do not say "search". In a repository with a .wikicommit/ directory, prefer this over grep — it ranks results, handles CJK without word breaks, expands synonyms and abbreviations, and finds the same page written in another language.
---

# wikicommit-search

A keyword-search skill that performs FTS5 trigram full-text search over `.wikicommit/entity/`. All index-building and query logic is delegated to the shared script `.wikicommit/scripts/search_index.py`; this skill is responsible for building the queries, merging per-language results, and formatting them for display.

## Usage

```
/wikicommit-search <query> [--lang <lang>] [--no-expand]
```

- `<query>`: search keywords (multiple words separated by spaces are allowed)
- `--lang <lang>`: restrict to pages in the given language (ISO 639-1) (optional). This turns off Step 0's fan-out across languages — but not Step 0.5's rendering into `<lang>`; see both
- `--no-expand`: skip Step 0.5's synonym expansion and search the query words themselves (optional). Independent of `--lang`: it suppresses invented synonyms, not other languages

The two flags are separate axes and can be combined. `--lang` narrows *which languages are searched*; `--no-expand` narrows *which words are searched for*.

## Processing Flow

### Step 0: Determine Target Languages

**If `--lang <lang>` was given, the language list is just `[<lang>]` — skip the rest of this step.** Do not detect the query's language and do not add any other language: the user narrowed the search deliberately, and this Skill should not widen it back. `--lang` is therefore how a user opts out of the fan-out across languages.

What it does *not* turn off is Step 0.5's rendering: when `<lang>` is not the language `<query>` is written in, the concepts are still translated into `<lang>` before being searched. Searching one language's words inside another language's pages returns nothing by construction, so skipping the translation here would make `--lang` a guaranteed-empty search rather than a narrower one (`/wikicommit-search 認証フロー --lang en` has to look for `Authentication Flow`). Step 3's "Also searched" line reports those translations as usual.

Otherwise, search every language, translating the query into each — a query written in one language reaches pages written in another only when a proper noun or Latin-script term happens to be shared (`認証フロー` never matches a page titled `Authentication Flow`):

1. Read `.wikicommit/config.yml` and get `translation.primary_lang` and `translation.targets`. If `.wikicommit/config.yml` doesn't exist, display an error, guide the user to run `/wikicommit-init`, and stop.
2. Have the LLM determine the language of `<query>`.
3. List the language directories that actually exist under `.wikicommit/entity/` (its immediate subdirectories, excluding `assets/`).
4. Build the list of languages to search, in this order, **deduplicating any repeated language**: the language of `<query>`, then `primary_lang`, then each language in `targets`, then any remaining directory from step 3.

   Step 3 exists because every query carries a `--lang`, so the search covers a closed set of languages: a wiki can hold pages in a language `config.yml` never mentions (`/wikicommit-translate <page> --lang en` writes `.wikicommit/entity/en/` whatever `targets` says), and without step 3 those pages would be unreachable. Configured languages come first so that they win the dedup priority in Step 2.3.

### Step 0.5: Extract, Expand and Translate Keywords

FTS5 matches literal text, so a search finds nothing when the wiki writes the same idea in different words than the user typed — the user asks for `子ども手当`, the page says `児童手当`, and the result is zero hits even though the wiki covers the topic. Expanding the query with the LLM's own vocabulary knowledge closes that gap.

1. Split `<query>` into the distinct **concepts** it is asking about (usually one per word or phrase; a multi-word proper noun is one concept). Do this even under `--no-expand` and even for a single-language run: `search_index.py` splits a positional query on whitespace and treats each piece as a phrase, so a full sentence in a language without whitespace word boundaries (`ja`, `zh`) becomes one verbatim phrase that structurally cannot match page body text.
2. Unless `--no-expand` was given, produce for each concept the original term plus its expansions under the rules below.
3. For each language from Step 0, render every concept in that language: the language of `<query>` uses the terms as-is, and any other language gets each term translated individually (the LLM translates on the fly — no dedicated translation API or library). Do not translate `<query>` as one sentence and pass that. One concept becomes one `--expand` group **per language**.

Do not add expansions to the query string instead of grouping them. FTS5 AND-s adjacent phrases, so an appended synonym makes the search *narrower* — pages would have to contain every wording at once, and the hit that motivated the expansion disappears. Only the `--expand` grouping OR-s them.

**Expansion rules.** trigram search matches *substrings*, so inflected forms and longer compounds containing the term (`エンジニア` → `ソフトウェアエンジニア`) are already reached for free; spending expansion slots there only adds noise. Expand only where the vocabulary genuinely differs:

- **Expand**: synonyms (`児童手当` / `子ども手当`), hypernyms and general terms (`Claude Code` / `AIコーディングツール`), abbreviation–full-form pairs (`LLM` / `大規模言語モデル`), cross-language equivalents (`vibe coding` / `バイブコーディング`), orthographic variants (`サーバ` / `サーバー`).
- **Do not expand**: inflected forms and word endings, compounds already reachable as a substring, or merely related terms whose meaning sits somewhere else (a term that "gets discussed alongside" the original is not a synonym).
- **Limits**: at most 2–3 expansions per original term, and roughly 5 expanded terms across the whole search. Left unbounded this widens without end.
- **Never produce an expansion shorter than 3 characters** — the trigram tokenizer cannot form a token from it, so it can never match.

### Step 1: Run the Query, Once Per Language

Run one query per language from Step 0, always passing that language as `--lang`. **Run them sequentially, one language at a time — never in parallel**: `search_index.py query` rebuilds the index whenever it is missing or stale, so concurrent calls after a wiki change would each rebuild it — the swap is atomic, so nothing breaks, but the work is done once per language instead of once (the same reason `wikicommit-synthesize` gives for its own per-language loop).

**`--limit`**: always `--limit 10`, per language, regardless of how many languages are in the list. Step 2.3 merges and trims to 10. Splitting the budget across languages (5 each, as `wikicommit-ask` does for its grounding set) would *shrink* the result list on the wikis this feature is for: in a fully translated two-language wiki, both queries return the same ten pages in different languages, dedup collapses them to one set, and the user ends up with five results where a single unfiltered `--limit 10` query used to give ten. `wikicommit-ask` splits because every extra hit costs LLM context; this Skill only prints lines, so the local index is free to return more.

With expansion (the default), pass one `--expand` per concept, using that language's rendering from Step 0.5, each group's terms joined by `|`:

```bash
python .wikicommit/scripts/search_index.py query \
  --expand "$(cat <<'EOF'
<concept 1 term in this language>|<expansion>|<expansion>
EOF
)" \
  --expand "$(cat <<'EOF'
<concept 2 term in this language>|<expansion>
EOF
)" --lang <lang> --limit 10
```

With `--no-expand`, use the positional form instead, with that language's rendering of the concepts joined by spaces (for the query's own language that is the query's own words):

```bash
python .wikicommit/scripts/search_index.py query "$(cat <<'EOF'
<concepts in this language, space-separated>
EOF
)" --lang <lang> --limit 10
```

Pass every search term through a quote-delimited heredoc, not a plain double-quote embedding — `<query>` is free-form user text with no upstream validation, expansions and translations are LLM output derived from it, and command substitution (`` ` ``, `$(...)`) is evaluated by the shell at the point this command line is assembled regardless of which program the resulting argument is ultimately handed to; scoping the downstream program to a local read-only script does not by itself contain that.

Never pass both forms at once — the script rejects that combination rather than guessing which semantics you meant.

On exit code `1` (failure, with an `ERROR:` line printed), display that error message as-is to the user and stop (e.g. SQLite doesn't support trigram, or `.wikicommit/entity/` doesn't exist). Stop on the first such failure rather than continuing with the remaining languages — the cause is the environment, not the query, so the next language would fail the same way.

### Step 2: Parse the Output

Parse each language's stdout separately, keeping track of which language each line came from:

- `MATCH: <path> | title=<title> | type=<type> | lang=<lang> | review_status=<review_status>` line → information for one hit
- The indented line immediately after (`  <snippet>`) → that hit's snippet
- `SUMMARY: query=<what was searched>, hits=<N>` line → *that language's* hit count, not the number Step 3 reports (Step 2.3 computes that one). With `--no-expand` the value is the raw query in double quotes (`query="児童手当"`); with expansion it is the FTS5 expression actually run (`query=("子ども手当" OR "児童手当") AND ("手続き")`), which reflects any term the script dropped and is what Step 3 shows the user
- `WARNING:` line(s), zero or more — `search_index.py` detects terms too short for the trigram tokenizer to ever match. Four forms, which mean different things:
  - `WARNING: query term "<term>" has <N> character(s); ... cannot match anything` → `--no-expand` path; that term kills the whole search. Collect these to explain an unexpected `hits=0` in Step 3
  - `WARNING: expand term "<term>" ... so it was dropped — its group still matches via: <terms>` → the concept survives through a longer synonym. **Do not surface this to the user**: nothing is wrong, and the expansion did exactly what it is for
  - `WARNING: expand group "<a>|<b>" has no term of at least 3 character(s); ... no longer narrows the search` → that entire concept was dropped, so the results are broader than asked for. Surface this in Step 3 — in **both** the `hits=0` and the `hits` >= 1 branch, since results that silently answer a narrower question than the user asked are exactly what this warning exists to flag
  - `WARNING: no usable --expand term remains; ... cannot match anything` → every concept was dropped, so the search ran with no terms and `hits=0` is guaranteed regardless of what the wiki contains. Surface this in Step 3 instead of the per-group message, whose "no longer narrows the search" wording is the opposite of what happened here

Record the language alongside every warning you keep. A short-term warning usually applies to *one* language's rendering of a concept — a translation can land under three characters where the original did not — and reporting it without saying which language would suggest the whole search was broken when only one leg of it was.

### Step 2.3: Merge Results Across Languages

Skip this step if only one language was searched; its hits are the result list as-is.

1. Combine every language's hits into a single list.
2. **Collapse language variants of the same page into one hit.** Two or more hits that share the same `type` and `slug` are the same page in different languages (linked via `translated_from`). Neither field is printed as such: `type` comes from the `MATCH:` line, and the `slug` is the `<path>`'s file name with `.md` removed (`.wikicommit/entity/ja/DefinedTerm/auth-flow.md` → `auth-flow`). Keep exactly one, by this priority: the language of `<query>` > `primary_lang` > the order the language appears in `targets`. Remember which languages the suppressed variants were in — Step 3 shows them, so that a hit's other-language versions are visible instead of silently disappearing.
3. Sort the surviving hits roughly by the bm25 order `search_index.py` returned (already ranked within each language) and keep the top 10. A naive cross-language score comparison is accepted as an approximation here: corpus size and trigram distribution differ per language, so a strict comparison isn't available. This is the same approximation `wikicommit-ask` documents.

The merged count is what Step 3 reports as `<hits>` — not the sum of the per-language `hits=` values, which double-counts translated pages.

### Step 2.5: Look Up Each Hit's `sources`

For each merged hit's `<path>` (skip this step entirely if there are no hits left after Step 2.3), read the page and extract its frontmatter. `search_index.py`'s own index doesn't carry `sources` — it isn't full-text-searchable structured data, so extending the FTS5 schema for it isn't worth it when each hit's `path` is already in hand. Format a `sources` line per hit:

- Ordinary page with a non-empty `sources` list: format each entry and join with `, `:
  - `type: path` → the `path` value as-is (e.g., `raw/paper-2024.pdf`)
  - `type: url` / `type: wikicommit` → the `url` value with a leading `https://` or `http://` stripped (e.g., `simonwillison.net/2025/May/1/not-vibe-coding/` — full URLs would dominate the result listing's width; the scheme carries no information the reader needs to recognize the source)
  - `type: manual` → `manual (author: <author>)`
- Translation page (`translated_from` present; these have no `sources` of their own): read the parent page at `translated_from` and format *its* `sources` the same way as above, prefixed with `translated from <translated_from>: ` — this is more informative than a bare "this is a translation" note, and the parent page's `sources` are exactly what a reader chasing provenance actually wants. If the parent page itself is missing (already a `check_translation_status.py` `MISSING_SOURCE` case elsewhere), fall back to `translated from <translated_from> (parent page not found)`.
- Synthesized page (`derived_from` present; these also have no `sources` of their own): format as `derived from: <path1>, <path2>, ...` using each entry's `path`.
- Anything else with an empty or missing `sources` (a malformed page that isn't a translation/synthesis/index page — `index.md` pages don't reach this step at all, since `search_index.py`'s `build` already excludes them from the index): `sources: (none)`.

### Step 3: Display Results

`<hits>` throughout this step is the merged count from Step 2.3.

If there are no hits:

```
No matching pages
```

If any surfaceable `WARNING:` line was parsed in Step 2 (the `query term`, `expand group` and `no usable --expand term` forms, not the `expand term` one), append a supplementary note naming the offending term(s) **and the language whose query produced them** (translate the explanation into the query's language if it isn't English). Naming the language matters once more than one is searched: a term can be long enough in the original and too short once translated, and "no matching pages" would otherwise look like a gap in the wiki rather than a query that structurally could not match in that language:

```
No matching pages

⚠️ The query term(s) "<term1>" (en), "<term2>" (ja) are shorter than 3 characters. Trigram search can't match terms under 3 characters — try a more specific term (e.g. 児童手当 instead of 児童).
```

Display this and stop.

If `<hits>` is 1 or more, number the hits 1, 2, 3, ... in merged order and format them, appending the `sources` line from Step 2.5. Append `⚠️ Unreviewed` at the end of the line for any hit with `review_status: pending` (omit it for `reviewed`). **If Step 2.3 suppressed other-language versions of a hit, append `(also in: <lang>, ...)`** so the reader can see the page exists in those languages too — collapsing the duplicates keeps the list readable, but hiding that they existed would make the wiki look thinner than it is.

**If an `expand group` warning was parsed in Step 2, say so here too**, on a line under the header, naming the dropped concept. These results answer a *broader* question than the user asked — one of their concepts is not constraining the search at all, so pages unrelated to it are in the list — and that is invisible from the hits themselves. Reporting it only when `hits=0` would leave the more common case (some other concept still matches, so results do come back) silently wrong:

```
⚠️ The concept "<a>|<b>" was dropped: every wording is shorter than 3 characters, which trigram search can never match. The results below are not narrowed by it.
```

**Say which words were actually searched** — list, on a line under the header, every term that is not one of the user's own words: the expansions Step 0.5 added and the translations it produced for the other languages. A person reading these results is entitled to know that a word they never typed is why a hit is here; silently searching for something else and presenting the results as theirs is the wrong default for a Skill whose whole output is read by a human (`wikicommit-ask` makes the opposite call because there the search is an internal step and the answer carries its own grounding notes). Omit the line only when nothing was in fact added — `--no-expand` together with a single language that is the query's own (under `--lang <other-lang>` the translations still have to be listed) — and omit any term the Step 2 warnings say was dropped — it did not contribute:

```
Search results: "<query>" (<hits> hits)
Also searched: 子ども手当 (ja), child allowance, child benefit (en)

1. <title> (<type>, <lang>) ⚠️ Unreviewed
   <path>
   <snippet>
   sources: simonwillison.net/2025/May/1/not-vibe-coding/, arxiv.org/html/2510.17842v1

2. <title> (<type>, <lang>) (also in: en)
   <path>
   <snippet>
   sources: translated from .wikicommit/entity/ja/DefinedTerm/vibe-coding.md: raw/paper-2024.pdf
```

## Notes

- Do not commit or create a PR against `main` or any branch
- Do not write to `.wikicommit/schema/`
- This skill itself has no side effects. However, `search_index.py` automatically rebuilds the index file (`.wikicommit/.cache/search_index.sqlite3`, not tracked by Git) when it doesn't exist or no longer matches the pages (a page added, edited or removed since it was built — it then prints a `NOTE:` line)
