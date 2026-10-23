---
name: wikicommit-translate
description: Translate wiki pages into the target languages configured in .wikicommit/config.yml, either one named page or every untranslated or stale page, writing the results locally with no Git operations. Use this when someone asks to translate the wiki or to bring its translations up to date, including inside an unattended run. It writes pages into the repository, so do not use it to translate a sentence, a snippet or a file that is not a wiki page, and do not use it to answer a question about a page written in another language — wikicommit-ask and wikicommit-search already search every configured language.
---

# wikicommit-translate

Interactive translation Skill. Per-page processing is identical to the unattended Phase 4 pipeline — inject the source page's full text plus `DefinedTerm/` glossary terms and the source→target term table built from them, generate a translation, check it against the source page with a review subagent (recorded under `.wikicommit/review/` as `translate-check`), and attach `translated_from` / `source_commit` / `translated_at` / `translated_by` / `translated_with`. The only difference is *who* calls it and *when*: this Skill is invoked by a human, writes locally, and performs no Git operations. Run `/wikicommit-merge` afterward to commit and open a PR.

## Usage

```
/wikicommit-translate <page> [--lang <target>]   # translate a single page
/wikicommit-translate                            # batch mode: process all untranslated/stale (page, target) pairs
```

`<page>` must be a source page (a page without `translated_from`) — e.g. `.wikicommit/entity/ja/Person/yamada-taro.md`. If the given page itself has `translated_from` (i.e. it is already a translation), stop and tell the user to run this on the original page instead.

## Processing Flow — the workflow engine holds the order

The order of this Skill's steps is kept by `.wikicommit/scripts/skill_workflow.py`, not by you. It returns **one step at a time**, checks on disk that the step was really done before moving on, and keeps its place in this run's record — so after a compaction or a new session you pick up exactly where the run stopped instead of re-deciding which pairs are already translated, reviewed and written back.

**Start the run**, passing each argument this Skill was invoked with as its own `--arg` (add `--non-interactive` when no person can answer questions in this run — a subagent, a scheduled or unattended run; the workflow engine then answers the five-pair question itself with "first five"):

```bash
python .wikicommit/scripts/skill_workflow.py start --workflow workflow.yaml \
    --model "<the model ID this runtime reports for you>" --arg="<each argument, one --arg each>"
```

Write each argument with `=` — `--arg=<page> --arg=--lang --arg=<target>` — because a value starting with `--` given after a space is read as an option of its own and the run does not start. `workflow.yaml` is in this Skill's directory — the one holding this `SKILL.md`, which the runtime names when it loads the Skill — not in the repository root, because the Skills may be installed under `.claude/skills/` or `.agents/skills/`. Commands still run from the repository root, so spell the path out from there.

Then **loop**:

1. Read the JSON it printed. **Keep the `run` path** — every later call names it.
2. If `notes` is present, report every line of it to the user.
3. If `step` is `null`, the run is over — `finished` (say `finished_because` if present, e.g. "Nothing to translate"), or halted (say `halted_reason`). Stop.

   The first step is a check the workflow engine runs itself, **at the start of the run, before anything is translated**: if `.wikicommit/config.yml` does not exist it halts and you tell the user to run `/wikicommit-init` first; if `.wikicommit/review-rules.md` does not exist it halts and you tell the user to run `/wikicommit-init --no-overwrite`. Every page this run writes goes through the `translate-check` review, and that review follows those rules; without them it degrades to a bare re-read while still writing a record that a review happened, and finding out at the first review would throw that translation away. The same check halts when the named page is itself a translation (has `translated_from` — tell the user to run this on the original page instead) and when there is no target language ("No target language. Pass `--lang <lang>`, or set `targets` in `config.yml`.", fixed English — it is read by the operator, not by readers of the wiki). Without a page, it also halts when `--lang` names a language not in `targets` that has no translations yet: `check_translation_status.py` reports `UNTRANSLATED` only for the configured targets (and `STALE` only for translations that exist), so batch mode could never find anything — tell the user to name a page or add the language to `targets`.
4. If `blocked` is true, the completion check for this step has failed repeatedly: stop and report the last `reason` to the user. Do not work around a check.
5. A `human` step: ask the user `ask`, offering `choices`, and pass the answer back with the `then` command.
6. An `agent` step: **read the file named in `instructions` now and follow it**. When it is done, run the `then` command with one of the `outcomes`, `--token` set to the `pass_token` in the instructions file's frontmatter, and the `--reason`, `--page` or `--count` that step's instructions ask for. If the response has `when_nobody_can_answer`, that is the rule for any question the step would ask.
7. `done` prints the next step in the same form. If it prints `"accepted": false`, the step is **not** complete: read `reason`, fix what it names, and run `done` again. It never skips ahead, and it refuses a step other than the current one.

`skill_workflow.py next <run>` prints the current step again without changing anything — use it whenever you are unsure where the run is, and **always** after a compaction or when resuming in a new session (`skill_workflow.py status` lists the runs still open). The pairs and their order are in the run record's `workflow.lists`, and each finished pair is in its `workflow.log`; read them from there, not from memory. A run whose session is gone for good is closed with `skill_workflow.py abandon <run> --reason "<why>"`, which only a person should decide.

**Why it works this way.** Each pair ends in three writes — the translation, its `source_commit` write-back and its review record — and a long batch done from memory is exactly where the last of them goes missing. The workflow engine checks all three on disk before it moves to the next pair, and `/wikicommit-merge` refuses a change carrying files that a still-open run touched.

The steps (the table is here as well as in the workflow engine's answers so the pointers survive a compaction):

| Step | Kind | Read | What it does |
|---|---|---|---|
| `preflight` | script | — | the checks above |
| `collect` | script | — | lists the `(source page, target language)` pairs, each written `<source page> -> <lang>`; none → the run finishes with "Nothing to translate" |
| `batch-cap` | human | — | batch mode only, when there are more than 5 pairs; a non-interactive run takes the first 5 |
| `select` | script | — | applies that answer |
| `translate` (per pair) | agent | `references/translate-page.md` | Step 4: translate, review (`translate-check`), record, write |
| `rebuild-index` | script | — | `rebuild_index.py`, once for the whole run |
| `report` | agent | `references/completion-report.md` | close the run and report, listing every discarded pair |

**Which pairs `collect` lists.** With a page argument (single-page mode), one pair per target: `--lang <target>` if given, otherwise every `translation.targets` entry, skipping the page's own language. Without one (batch mode), every `UNTRANSLATED` and `STALE` pair `check_translation_status.py` reports — for a `STALE` line the pair is the translation's `translated_from` and `lang`, and with `--lang <target>` only that language's pairs — with **every `DefinedTerm` pair first**, then ascending by the reported path. Translating prose before its glossary is settled is backwards: `DefinedTerm` is the most-referenced type in a wiki, and plain path order would put it wherever `DefinedTerm/` happens to sort, often after the pages that cite it. Step 4's term table is re-read from disk for each pair, so later pairs see the target-language terms this run has already settled — and because the list is `DefinedTerm`-first, answering "first five" settles the glossary within this run instead of deferring it behind unrelated pages. A non-interactive run never reads the absence of an answer as "all": the deferred pairs change nothing on disk, so the next run reports them again.

Single-page mode has no work list to reorder, so it cannot settle the glossary first — it uses whatever target-language `DefinedTerm` pages already exist. Translating a wiki's `DefinedTerm` pages before its other pages is therefore worth doing by hand here, or by running batch mode instead.

If `.wikicommit/scripts/skill_workflow.py` or `_workflow_checks.py` does not exist (`.wikicommit/scripts/` older than this Skill), the run cannot start (the first step halts on the latter): tell the user to run `/wikicommit-update` first.

## Notes

- Do not commit or create a PR against `main` or any branch (that is `wikicommit-merge`'s responsibility)
- Do not write to `.wikicommit/schema/` (read-only)
- No Git operations of any kind — this Skill only reads the working tree (including via `git log` for `source_commit` and `git hash-object` for the rules file) and writes new/updated files under `.wikicommit/entity/` and new review records under `.wikicommit/review/`
