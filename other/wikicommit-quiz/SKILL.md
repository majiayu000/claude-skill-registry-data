---
name: wikicommit-quiz
description: Generate a quiz from the wiki's own pages, at an adjustable difficulty. Use this when someone wants to test or review what the wiki covers, asks to be quizzed, wants practice questions or flashcards on a topic the wiki holds, or wants to check how much of a subject they have retained — even if they do not use the word "quiz".
---

# wikicommit-quiz

A `wikicommit-ask`-derived skill that generates a difficulty-adjustable quiz from the content of `.wikicommit/entity/` and outputs it into the conversation. When `--topic` is given, gathering related pages is delegated to the shared script `.wikicommit/scripts/search_index.py` (the same call `wikicommit-search` uses). It never writes to the filesystem.

## Usage

```
/wikicommit-quiz [--topic <keyword>] [--lang <lang>] [--difficulty=easy|medium|hard]
```

- `--topic <keyword>`: if given, generate the quiz from pages related to that keyword (if omitted, sample randomly from the whole wiki)
- `--lang <lang>`: restrict the `--topic` search to pages in the given language (ISO 639-1), which turns off its fan-out across languages but not the translation of `<topic>` into `<lang>` (optional; ignored without `--topic`, since that branch has no query to translate)
- `--difficulty`: one of `easy` / `medium` / `hard` (default `medium`)

**The quiz itself is written in the language of `<topic>`, or in `primary_lang` when `--topic` is omitted** — questions, options, explanations and the score summary alike. Do not let the language of a grounding page decide this: with cross-lingual search the grounding set can span several languages, and a quiz that switches language question by question is unusable. (Same rule `wikicommit-ask` applies to its answers.)

## Processing Flow

### Step 1: Gather Target Pages

Branches depending on whether `--topic` is given.

#### With `--topic`

**First determine which languages to search.** If `--lang <lang>` was given, the list is just `[<lang>]` — the user narrowed the search deliberately, so do not detect a language or add others; `--lang` doubles as the opt-out for the fan-out across languages. It does *not* switch off the translation step below: when `<lang>` is not the language `<topic>` is written in, the keyword groups are still rendered into `<lang>` before being searched, because one language's words cannot match another language's pages (`--topic 認証フロー --lang en` has to look for `Authentication Flow`). Otherwise read `.wikicommit/config.yml` for `translation.primary_lang` and `translation.targets` (if the file doesn't exist, display an error, guide the user to run `/wikicommit-init`, and stop), have the LLM determine the language of `<topic>`, and build the list — the language of `<topic>`, then `primary_lang`, then each language in `targets`, then any remaining language directory that actually exists under `.wikicommit/entity/` (its immediate subdirectories, excluding `assets/`) — **deduplicating repeats**. That last group matters because every query carries a `--lang`, so the search covers a closed set of languages: `/wikicommit-translate <page> --lang en` writes `.wikicommit/entity/en/` whatever `targets` says, and those pages would otherwise be unreachable. Configured languages come first so they win the dedup priority below. Without the fan-out the search only reaches pages that share the topic's own wording: `認証フロー` never matches a page titled `Authentication Flow`.

Then split `<topic>` into the distinct keywords it names, and **expand each into a group of alternative wordings**. FTS5 matches literal text, so a topic phrased differently from the wiki's own wording — the user types `子ども手当`, the pages say `児童手当` — yields no pages to build a quiz from even though the wiki covers the subject. Each keyword plus its expansions becomes one `--expand` group. This is an internal step — the quiz itself never mentions it.

**Expansion rules.** trigram search matches *substrings*, so inflected forms and longer compounds containing the term (`エンジニア` → `ソフトウェアエンジニア`) are already reached for free; spending expansion slots there only adds noise. Expand only where the vocabulary genuinely differs:

- **Expand**: synonyms (`児童手当` / `子ども手当`), hypernyms and general terms (`Claude Code` / `AIコーディングツール`), abbreviation–full-form pairs (`LLM` / `大規模言語モデル`), cross-language equivalents (`vibe coding` / `バイブコーディング`), orthographic variants (`サーバ` / `サーバー`).
- **Do not expand**: inflected forms and word endings, compounds already reachable as a substring, or merely related terms whose meaning sits somewhere else (a term that "gets discussed alongside" the original is not a synonym).
- **Limits**: at most 2–3 expansions per original term, and roughly 5 expanded terms across the whole search. Left unbounded this widens without end.
- **Never produce an expansion shorter than 3 characters** — the trigram tokenizer cannot form a token from it, so it can never match.

Render every keyword group in each of the target languages: the language of `<topic>` uses the terms as-is, any other language gets each term translated individually (the LLM translates on the fly — no dedicated translation API or library). Do not translate `<topic>` as one sentence.

Then run **one query per language, sequentially — never in parallel**: `search_index.py query` rebuilds the index whenever it is missing or stale, so concurrent calls after a wiki change would each rebuild it — the swap is atomic, so nothing breaks, but the work is done once per language instead of once (the same reason `wikicommit-synthesize` gives for its own per-language loop). Pass one `--expand` per keyword group, using that language's rendering, each group's terms joined by `|`. Use `--limit 10` per language regardless of how many languages there are (the merge below trims back to 10). Splitting the budget across languages would shrink the candidate pool on a fully translated wiki, where each language returns the same pages and dedup collapses them to one set:

```bash
python .wikicommit/scripts/search_index.py query \
  --expand "$(cat <<'EOF'
<keyword 1 in this language>|<expansion>|<expansion>
EOF
)" \
  --expand "$(cat <<'EOF'
<keyword 2 in this language>|<expansion>
EOF
)" --lang <lang> --limit 10
```

Terms inside a group are OR-ed and the groups are AND-ed, which is why the expansions have to be grouped rather than appended to a single query string: FTS5 AND-s adjacent phrases, so appending a synonym would demand that a page contain every wording at once and would drop the very page the expansion was meant to reach.

Pass every term through a quote-delimited heredoc, not a plain double-quote embedding — `--topic` is free-form user text with no upstream validation, the expansions and translations are LLM output derived from it, and a plain `"<term>"` embedding would let shell metacharacters (`` ` ``, `$(...)`) in it be evaluated by the shell when this command line is assembled, regardless of the downstream script.

On exit code `1` (failure, with an `ERROR:` line printed), display that error message as-is to the user and stop (e.g. SQLite doesn't support trigram, or `.wikicommit/entity/` doesn't exist). Stop on the first such failure instead of trying the remaining languages — the cause is the environment, not the query.

Collect the `MATCH:` lines (`path` / `title` / `type` / `lang` / `review_status`) from every language, then **merge them into one list**: hits sharing the same `type` and `slug` — `type` from the `MATCH:` line, `slug` being the `<path>`'s file name without `.md` — are the same page in different languages, so keep exactly one — priority "language of `<topic>`" > `primary_lang` > the order the language appears in `targets` — and then keep the top 10 by the per-language bm25 order (a naive cross-language score comparison, the same approximation `wikicommit-ask` documents). **Deduplicating is not cosmetic here**: two language versions of one page would ground two questions about the same fact, so the same item would be asked twice in a quiz that is only 3–5 questions long. Merge even when a page's languages disagree in detail — pick the priority language's version and ignore the other, rather than treating the discrepancy as extra material.

If no hits remain after merging, display "No pages related to \"<topic>\" were found" and stop. A `WARNING: expand group ... has no term of at least 3 character(s)` or `WARNING: no usable --expand term remains` line means a keyword could not match in that language for structural reasons rather than because the wiki lacks the topic; say so, naming the language, instead of reporting a bare "no pages found".

#### Without `--topic`

1. Read `.wikicommit/config.yml` and get `translation.primary_lang`. If `.wikicommit/config.yml` doesn't exist, display an error, guide the user to run `/wikicommit-init`, and stop.
2. Scan `.wikicommit/entity/<primary_lang>/**/*.md` and build a list excluding `index.md` and pages with `status: removed`.
3. Randomly sample 5–10 pages from the list (not scripted, since this isn't deterministic — the agent performs the random selection).
4. If fewer than 5 target pages exist, proceed with however many exist. If there are zero, display "No pages available to generate a quiz from" and stop.

### Step 2: Fetch Page Content

Read each page gathered in step 1 in full and add its body (excluding frontmatter) to the LLM's context.

### Step 3: Generate the Quiz

Write everything in the quiz language fixed in the Usage section above (the language of `<topic>`, or `primary_lang` when `--topic` was omitted) — not in the language of whichever page a given question is grounded in.

Vary the question format based on `--difficulty`. **Do not include claims in the quiz or explanations that aren't in the gathered body content** (hallucination prevention).

- `easy`: one Q&A per page, asking about the `title` and basic facts of a single page. One question per page.
- `medium`: multiple-choice (4 options) questions spanning connections across multiple pages. Build incorrect options from within the gathered body content as well.
- `hard`: free-response questions about relationships and chronology between pages connected via WikiLink. If no WikiLink (`[[Type/slug]]`) is found among the gathered pages, switch to questions about chronology within a gathered page (dates, the order of events).

Aim for around 3–5 questions depending on the number of gathered pages (`easy` is one question per page, but if there are more than 5 gathered pages, narrow it down to a representative 5). Prepare the full question/answer/source set up front, but do not reveal it yet — questions are presented one at a time (Step 4).

### Step 4: Present One Question at a Time

This is a self-test: the user must not see the correct answer before answering. Output only the current question — never the answer or the grounding page path — then wait for the user's response before continuing.

```
Q1. <question text>
(medium only)
  A. ...
  B. ...
  C. ...
  D. ...
```

Never write to a file.

### Step 5: Interactive Grading and Progression

When the user answers the current question, grade it and reveal, for the first time, whether it's correct, an explanation (quoting the relevant part of the grounding page), and the grounding page path. If the grounding page is in a different language from the quiz, translate the quoted passage into the quiz language and show the page's own path unchanged, so the quote stays readable while the citation still points at the real file. If incorrect, also show the correct answer.

```
✅ Correct! (or ❌ Incorrect. Correct answer: <correct answer>)
<explanation quoting the relevant part of the grounding page>
Source: .wikicommit/entity/ja/Person/yamada-taro.md
```

Then present the next question (back to Step 4's format) until all prepared questions have been asked. After the last question, show a final score summary (e.g. `3/5 correct`) and end.

## Notes

- Never write to the filesystem (including `.wikicommit/exports/`), and never commit or create a PR against `main` or any branch
- Do not write to `.wikicommit/schema/`
- Do not include claims in the quiz or explanations that aren't in a gathered page's body content (hallucination prevention; see step 3)
- This skill itself has no side effects. However, when `--topic` is given, the `search_index.py` call automatically rebuilds the index file (`.wikicommit/.cache/search_index.sqlite3`, not tracked by Git) when it doesn't exist or no longer matches the pages (a page added, edited or removed since it was built — it then prints a `NOTE:` line)
