---
name: wikicommit-generate
description: Register a source file or URL under .wikicommit/source/ and generate wiki pages from it, process the sources already queued, or rebuild existing pages under the current generation rules with --regenerate. Use this when someone asks to take a source into the wiki, to work through the pending source queue, or to regenerate pages. It writes pages into the repository, so do not use it when someone pastes a link and wants it read, summarized or discussed, and do not use it to answer a question about a source the wiki already holds — wikicommit-ask and wikicommit-search do that without writing.
metadata:
  requires: "wikicommit-init"
---

# wikicommit-generate

> **Paths in this file.** `references/…`, `scripts/…`, `workflow*.yaml` and `../<other-skill>/…` are relative to this Skill's directory — the one holding this `SKILL.md`, which the runtime names when it loads the Skill — not to the repository root, because the Skills may be installed under `.claude/skills/` or `.agents/skills/`. Commands still run from the repository root, so spell the path out from there (`python <this Skill's directory>/scripts/…`). Paths starting with `.wikicommit/` are repository-root paths as before.

Registers a source and generates wiki pages (local writes only) in one run. Performs no Git operations.

## Usage

```
/wikicommit-generate <path|url> [--include <glob>] [--license <id>]   # register a source + generate pages in one run
/wikicommit-generate                                  # process every management file still queued (asks first if more than 5)

/wikicommit-generate --regenerate <page-path>         # rebuild one existing page under the current generation rules
/wikicommit-generate --regenerate --type <Type>       # rebuild every eligible page of that type
/wikicommit-generate --regenerate --all               # rebuild every eligible page (asks first if more than 5)
/wikicommit-generate --regenerate <page> --merge <page> [...]  # merge pages a person decided are the same into the first
```

`--license <id>` records the source's license (free text: an SPDX identifier such as `CC-BY-4.0` where one exists, otherwise a short phrase) on the management file Step 0 creates, so the pages this run writes carry it in `sources[].license`. With `--include`, every newly registered file gets the same value. It is accepted only together with a source argument: the queue run and `--regenerate` register nothing, so there is nowhere to pass it — if it comes without a source or with `--regenerate`, say so and do not start the run.

## Prerequisite Skills (Text Extraction) — see `references/text-extraction-routing.md`

Which tool extracts which file type, and the install command for each, are in
`references/text-extraction-routing.md`. **Pass 1 is the only
reader**, so read it there, when Pass 1 is about to extract its first source. The rule
it opens with holds wherever extraction happens: a missing skill stops the run with an
install command, except for `.pdf` (text-based), `.docx`, `.pptx` and `.xlsx`, which fall
back to the `markitdown` CLI and only stop if `markitdown` itself is absent.

Every `markitdown` invocation in this skill is prefixed with `PYTHONIOENCODING=utf-8`: on
Windows, a Japanese-locale console codepage (`cp932`) can make the `markitdown` subprocess's
stdout encoding disagree with the UTF-8 the rest of the pipeline (redirect target, reading the
file back, hash computation) assumes, corrupting extracted text into mojibake before it ever
reaches Pass 2. The `VAR=value command` prefix is POSIX shell and works unmodified under
both Git Bash and WSL, the shells Skills run under on Windows.

## Processing Flow — the workflow engine holds the order

The order of this Skill's steps is kept by `.wikicommit/scripts/skill_workflow.py`, not by you. It returns **one step at a time**, checks on disk that the step was really done before moving on, and keeps its place in this run's record — so you never need to hold the whole procedure in mind, and after a compaction or a new session you pick up exactly where the run stopped.

Before the first step, read `.wikicommit/config.yml` and obtain `primary_lang`, `theme`, and `generate.max_retries` (default: 2). If `theme` is absent from `config.yml`, treat it as an empty string. An empty `theme` disables the *relevance* judgment described in Pass 2 — no entity is excluded as off-subject. It does not disable Pass 2's other exclusion axis: the entity policy read below is judged independently and can still exclude an entity on a wiki whose `theme` is empty. (A missing `config.yml` is caught by the workflow engine's first step.)

Read `.wikicommit/entity-policy.md` at the same time. It answers a different question from `theme`, on the same entities: `theme` decides **relevance** (has this anything to do with the subject?), the entity policy decides **permissibility** (granted it does, should a page exist for it?). Neither substitutes for the other: a living person at the centre of the subject scores highest on relevance and may still be one this wiki does not want a page about. Hold two things from it for Pass 2c: `wikicommit.exclude_living_persons` (a boolean, default `false`) read from the frontmatter, and the body prose — for the prose, **run `python .wikicommit/scripts/read_policy.py .wikicommit/entity-policy.md` rather than judging the body yourself**. If the file is absent, treat it as the shipped default — the switch off and no prose — and carry on silently. If the file **exists** but cannot be read or its frontmatter does not parse, fall back to that same default but **say so**: print a `WARNING:` naming the file at that moment, and repeat it in the Completion Notice. Do not fail open in silence — one mistyped line in a hand-edited file would otherwise turn the whole policy off with nothing in the run's output to show it. A `POLICY:` line means the prose that follows it is the policy; a `NONE:` line means there is none, exactly as an empty `theme` disables the relevance judgment. The script strips the worked example the file ships with, and every other HTML comment, so what reaches you is what someone wrote — judging that by eye errs one way, because every line of the shipped example argues for excluding something.

**Start the run** (add `--non-interactive` when no person can answer questions in this run — a subagent, a scheduled or unattended run; the workflow engine then answers its own questions with the defaults the workflow defines, and each step it hands you says what to do when nobody can answer):

```bash
python .wikicommit/scripts/skill_workflow.py start --workflow workflow.yaml \
    --model "<the model ID this runtime reports for you>" --arg="<each argument, one --arg each>"
```

Write each argument with `=` (`--arg=--regenerate`): a value starting with `--` given after a space is read as an option of its own and the run does not start. With `--regenerate`, pass `workflow-regenerate.yaml` instead (spell both paths out from the repository root, as the note at the top says).

Then **loop**:

1. Read the JSON it printed. **Keep the `run` path** — every later call names it.
2. If `notes` is present, report every line of it to the user. The version-skew check (`OUTDATED:`, `MISSING:`, `ORPHAN:`, `WARNING:` about `.wikicommit/scripts/`) and the end-of-run scripts speak through it; a skew warning does not stop the run.
3. If `step` is `null`, the run is over — `finished` (say `finished_because` if present), or halted (say `halted_reason`). Stop.
   A run that halts inside its first loop never reaches `ask-deferred`, so before stopping run `python <this Skill's directory>/scripts/workflow_checks.py halted-questions --run <run>` and, if it prints any `ITEM:`, list each source with its `REASON:` line as questions this run set aside and did not ask (it prints nothing when the run had already asked them): they stay queued, and a later run asks them only if it picks those sources again and gets to the end of its loop.
   The first steps are checks the workflow engine runs itself, **at the start of the run, before anything is fetched**: if `.wikicommit/config.yml` does not exist it halts and you tell the user to run `/wikicommit-init` first; if `.wikicommit/review-rules.md` does not exist it halts and you tell the user to run `/wikicommit-init --no-overwrite` to install it. Pass 4 refuses to review without that file, so checking at the start avoids a batch of fetching and generation that could never be reviewed — and a looser review that never read those rules would look completely normal while Pass 4 still wrote a record asserting a review happened. Neither halt touches `failed_pages` or any management file's `status`: it is an installation problem, not a defect in a page.
4. If `blocked` is true, the completion check for this step has failed repeatedly: stop and report the last `reason` to the user. Do not work around a check.
5. A `human` step: ask the user `ask`, offering `choices`, and pass the answer back with the `then` command.
6. An `agent` step: **read the file named in `instructions` now and follow it** for the `item` given (a source management file, or under `--regenerate` a page), reading `also_read` alongside it. When it is done, run the `then` command with one of the `outcomes`, and `--token` set to the `pass_token` in the instructions file's frontmatter. `--add`, `--touched`, `--reason`, `--page` and `--count` are for what that step's instructions and outcome descriptions ask for.
7. `done` prints the next step in the same form. If it prints `"accepted": false`, the step is **not** complete: read `reason`, fix what it names, and run `done` again. It never skips ahead, and it refuses a step other than the current one.

`skill_workflow.py next <run>` prints the current step again without changing anything — use it whenever you are unsure where the run is, and **always** after a compaction or when resuming in a new session (`skill_workflow.py status` lists the runs still open). A run whose session is gone for good is closed with `skill_workflow.py abandon <run> --reason "<why>"`, which only a person should decide: it names the files the run left behind rather than deleting them.

If `.wikicommit/scripts/skill_workflow.py` or `_workflow_checks.py` does not exist (`.wikicommit/scripts/` older than this Skill), the run cannot start (the first step halts on the latter): tell the user to run `/wikicommit-update` first. The same holds when the `preflight` step halts because `.wikicommit/scripts/add_source.py`, `resolve_source_cache_path.py` or `remove_page.py` is missing.

**Why it works this way.** Every failure recorded for this Skill had the same shape: a step at the end of a long flow that did not run, a write-back that did not happen, a result not handed on, or a part improvised because it was written only as prose. The workflow engine takes the order out of memory and checks the result of each step on disk. `/wikicommit-merge` refuses a change carrying files that a still-open run touched, so a run abandoned halfway cannot slip into the default branch.

The steps, and the file each one reads (the table is here as well as in the workflow engine's answers so the pointers survive a compaction):

| Step | Read | When |
|---|---|---|
| `register` | `references/step0-register.md` | only when a source argument is given |
| `pass1-extract` | `references/pass1-extract.md` and `references/text-extraction-routing.md` | per source |
| `pass2b-type` | `references/pass2b-type.md` | per source |
| `pass2c-entities` | `references/pass2c-entities.md` | per source |
| `pass3-generate` | `references/pass3-generate.md` and `references/writing-rules.md` | per source |
| `pass4-review` | `references/pass4-review.md` | per source |
| `reprocess-pass1-extract` … `reprocess-pass4-review` | the same files | per source the person answered about in `ask-deferred` |
| `completion` | `references/completion-notice.md` | once, last |

`preflight`, `freshness`, `collect`, `select`, `collect-questions`, `rebuild-index` and `reconcile` are scripts the workflow engine runs itself; `batch-cap` is the question asked when more than 5 sources are queued. `ask-deferred` is the question asked once every source has been through the passes: guard A's low-density warning and Pass 2b's type candidates never stop the loop — the source is set aside with a `## Deferred Reason` — and this step puts them all to the person at once. It also asks for the type of each entity Pass 2c left `ambiguous: true` (the source was written as `partial` with `ambiguous_entities`, not set aside). The sources answered about go through the passes again in the same run, with the answers handed over in the step's `lists`. In a `--non-interactive` run the answer is `later` and the deferrals stay queued. The whole sequence, with each step's outcomes and completion check, is `workflow.yaml` — read it if a step's answer surprises you.

Each pass file says what it does; the pointers follow, so that each is named at a point of use as well:

- Pass 1 and Pass 2a — **Read `references/pass1-extract.md` now and follow it** when the workflow engine hands you `pass1-extract`. It holds the extraction guards, the caches, and Pass 2a's summary, source-language and source-as-entity judgments.
- Pass 2b — `references/pass2b-type.md`: the two-stage type recall, the deferral and the question asked at the end of the loop, and the narrow write exception that lets this Skill add — never edit — a file under `.wikicommit/schema/`.
- Pass 2c — `references/pass2c-entities.md`: the analysis JSON, the `action` and `exclude_reason` rules, slug derivation, and the `## Summary` / `## Generation Notes` write-back.
- Pass 3 — `references/pass3-generate.md`: the `---FILE:`/`---END FILE---` output contract and the frontmatter rules. The writing rules for the body are in `references/writing-rules.md`, shared with `/wikicommit-synthesize`.
- Pass 4 — `references/pass4-review.md`: the review subagent, the retry loop, `failed_pages`, the review record, and the management file's final status. **It sends you on to one more file**: the review discipline itself is in `.wikicommit/review-rules.md`, shared with `/wikicommit-review` and `/wikicommit-synthesize` and not restated anywhere in this Skill.

### Regeneration Mode (`--regenerate`) — see `references/regenerate.md`

`--regenerate` rebuilds pages that already exist, so that pages generated under older schema templates or older Pass 3 rules can be brought up to the current ones. It is **page-driven, not source-driven**, and it shares Passes 1, 3 and 4 with ordinary generation while using none of Step 0, Pass 2a/2b/2c or the Completion Notice. Start it with `workflow-regenerate.yaml`; the workflow engine hands you `references/regenerate.md` alongside each shared pass file. If that file cannot be read, **stop and say so** rather than attempting a rebuild — it *is* the procedure. With `--merge`, the same mode merges pages recorded as the same concept into one, and the workflow engine hands you `references/merge.md` to take the absorbed pages down.

## Notes

- Do not commit to `main` or any branch
- Do not write to `.wikicommit/schema/`, with one narrow exception: Pass 2b may write a new `.wikicommit/schema/<Type>.md` file for a candidate a person approved in answer to the `ask-deferred` question (a non-interactive run never approves one; it leaves the source deferred) — it only ever adds a file that wasn't already there, never edits or overwrites an existing schema file
- Do not run `gh pr create` or any PR creation commands
- All file writes go directly to the working directory; `git status` will show them as untracked or modified
- For `type: url` / `type: wikicommit` sources, fetch only the registered `source.url`. Do not run additional `markitdown` calls for links discovered within the extracted content — each source page an operator wants ingested must be registered explicitly via `/wikicommit-generate <url>`.
