---
name: wikicommit-synthesize
description: Synthesize a new view page about a topic from existing wiki content, written directly to .wikicommit/view/. Use this only when someone explicitly asks for a new synthesized or overview page in the wiki. It writes a page into the repository, so do not use it to answer a question or to summarize a topic in the conversation — wikicommit-ask does that without writing.
disable-model-invocation: true
metadata:
  requires: "wikicommit-generate"
---

# wikicommit-synthesize

Synthesizes a new **view page** about a given concept or term from the content of `.wikicommit/entity/` itself — the counterpart to `/wikicommit-generate` (which creates pages from external sources): `generate` starts from a source document, `synthesize` starts from existing wiki pages. Gathering related pages uses the same search index as `wikicommit-ask`, but searches only `primary_lang` — the grounding has to be original pages, not translations of them (Step 1). The result is written to `.wikicommit/view/<lang>/<slug>.md` — subject to the quality gate and mergeable via `/wikicommit-merge` like any other page. Besides the shared `search_index.py`, `rebuild_index.py` and, in survey mode, `build_survey_view.py`, its one script of its own is `scripts/workflow_checks.py`, which the workflow engine calls to check each step.

**Why a separate tree**: a view page is grounded in this wiki's own pages (`derived_from`), not in an external document (`sources` + hash), and keeping it out of the type directories is what lets a reader see which is which. A view page carries **no `type:`** either: Schema.org models things, and what a view page holds is a *reading* of several pages, so picking a type would mean inventing one. It has an optional **`kind`** instead — what the page does with several pages at once, not what it is about.

`disable-model-invocation: true` is set because, unlike the read-only `wikicommit-ask`/`wikicommit-quiz` it's derived from, this Skill writes new files under `.wikicommit/`  — the same side-effect class as `wikicommit-generate`/`wikicommit-review`.

## Usage

```
/wikicommit-synthesize <topic>     # write about a topic you already have in mind
/wikicommit-synthesize             # survey the wiki first, and pick a topic out of it
/wikicommit-synthesize [<topic>] --max-grounding <N>   # grounding pages to use at most (default 30)
```

With no `<topic>`, the `survey` step (Step 0) surveys the whole wiki, proposes angles that only
become visible across pages, and hands the one you choose to the `ground` step as `<topic>`.
Everything from there on is identical in both modes.

## Processing Flow — the workflow engine holds the order

The order of this Skill's steps is kept by `.wikicommit/scripts/skill_workflow.py`, not by you. It returns **one step at a time**, checks on disk that the step was really done before moving on, and keeps its place — and the values one step hands to the next (the chosen topic and kind, the grounding pages, the page path) — in this run's record. After a compaction or a new session you pick up exactly where the run stopped instead of re-deciding which pages were chosen and whether the review was recorded.

**Start the run**, passing each argument this Skill was invoked with as its own `--arg` (add `--non-interactive` when no person can answer questions in this run — a subagent, a scheduled or unattended run):

```bash
python .wikicommit/scripts/skill_workflow.py start --workflow workflow.yaml \
    --model "<the model ID this runtime reports for you>" --arg="$(cat <<'EOF'
<the topic, if one was given>
EOF
)" [--arg=--max-grounding --arg=<N>]
```

Write each argument with `=` (`--arg=<value>`): a value starting with `--` given after a space is read as an option of its own and the run does not start. Pass the topic through the quote-delimited heredoc shown — it is free-form text, and a plain `"<topic>"` embedding would let shell metacharacters in it be evaluated; leave that `--arg` out when no topic was given. `workflow.yaml` is in this Skill's directory — the one holding this `SKILL.md`, which the runtime names when it loads the Skill — not in the repository root, because the Skills may be installed under `.claude/skills/` or `.agents/skills/`. Commands still run from the repository root, so spell the path out from there.

Then **loop**:

1. Read the JSON it printed. **Keep the `run` path** — every later call names it.
2. If `notes` is present, report every line of it to the user.
3. If `step` is `null`, the run is over — `finished` (say `finished_because` if present), or halted (say `halted_reason`). Stop.

   The first step is a check the workflow engine runs itself, **at the start of the run, before any search**: if `.wikicommit/config.yml` does not exist it halts and you tell the user to run `/wikicommit-init` first; if `.wikicommit/review-rules.md` does not exist it halts and you tell the user to run `/wikicommit-init --no-overwrite`; if the `wikicommit-generate` Skill is not installed beside this one (Step 5 follows its `../wikicommit-generate/references/writing-rules.md`), it halts and you tell the user to install it. Do not review without the rules and do not fall back to a looser check: without them Step 5.5 degrades to a bare "is this supported" pass while still writing a record that a review happened. Their absence is knowable before anything is searched and does not depend on the topic, so finding out at the review would discard the whole grounding search and body generation that was never going to be reviewable. This is an installation problem, not a defect in any page.
4. If `blocked` is true, the completion check for this step has failed repeatedly: stop and report the last `reason` to the user. Do not work around a check.
5. An `agent` step: **read the file named in `instructions` now and follow it**. When it is done, run the `then` command with one of the `outcomes`, `--token` set to the `pass_token` in the instructions file's frontmatter, and the `--add`, `--reason`, `--page` or `--count` that step's instructions ask for. If the response has `when_nobody_can_answer`, that is the rule for any question the step would ask.
6. `done` prints the next step in the same form. If it prints `"accepted": false`, the step is **not** complete: read `reason`, fix what it names, and run `done` again. It never skips ahead, and it refuses a step other than the current one.

`skill_workflow.py next <run>` prints the current step again without changing anything — use it whenever you are unsure where the run is, and **always** after a compaction or when resuming in a new session (`skill_workflow.py status` lists the runs still open). The values earlier steps added are in the run record's `workflow.lists`, and each finished step is in its `workflow.log`; read them from there, not from memory. A run whose session is gone for good is closed with `skill_workflow.py abandon <run> --reason "<why>"`, which only a person should decide.

**Why it works this way.** The run ends in writes that are easy to lose at the tail of a long synthesis: the page with a `derived_from` that must name exactly the pages read, at their commits, and the review record that says the page was checked. The workflow engine checks both on disk before it moves on, and `/wikicommit-merge` refuses a change carrying files that a still-open run touched.

The steps (the table is here as well as in the workflow engine's answers so the pointers survive a compaction):

| Step | Kind | Read | What it does |
|---|---|---|---|
| `preflight` | script | — | the checks above, and that `--max-grounding` is a positive whole number |
| `survey` | agent | `references/survey.md` | Step 0, only when no topic was given: propose angles, let the person choose; nothing chosen → the run finishes |
| `ground` | agent | `references/ground.md` | Steps 1–4: search `primary_lang`, choose the grounding pages from title, description and headings, read them, warn about unreviewed ones; none → the run finishes |
| `write` | agent | `references/write-page.md` (it sends you on to `../wikicommit-generate/references/writing-rules.md`) | Steps 5–9: synthesize, review (`synthesize-step5.5`), record the verdict, write the view page |
| `rebuild-index` | script | — | Step 10, only when the page was written |
| `report` | agent | `references/completion-report.md` | Step 11: close the run and report |

**Step 10: Update the View Index.** The page just written is not in its language's view index yet, so the workflow engine rebuilds that one index itself in its `rebuild-index` step — do not run this yourself; it is shown so you know what that step does — `rebuild_index.py` with the page's directory:

```bash
python .wikicommit/scripts/rebuild_index.py "$(cat <<'EOF'
.wikicommit/view/<lang>
EOF
)"
```

Given a directory in the view tree, `rebuild_index.py` writes a per-language index listing `[[View/<slug>]]` rather than a per-Type one. It rescans from disk, excludes `status: removed` pages, and is idempotent — an index that is already correct comes out byte-identical. This is a local write only — **do not commit** (`/wikicommit-merge` picks it up with the page). It is not skipped because the page is only one file: a view page has no source of its own (only `derived_from`), so no `/wikicommit-generate` run is scheduled to pick it up, and the page is unlinked at birth, so without its index entry it is reachable only by direct URL.

**Why one directory and not the whole tree**: `/wikicommit-generate` and `/wikicommit-translate` rebuild every index, because over a long multi-source batch, tracking which directories were touched is what gets forgotten at the tail end. That reasoning does not carry here: this Skill writes exactly one page, whose `<lang>` is already determined. Passing it keeps this Skill's stated side effect narrow (it is a conversational Skill, and a tree-wide rebuild can drop unrelated `index.md` diffs into the working tree that the user then has to account for before merging).

If `.wikicommit/scripts/skill_workflow.py` or `_workflow_checks.py` does not exist (`.wikicommit/scripts/` older than this Skill), the run cannot start (the first step halts on the latter): tell the user to run `/wikicommit-update` first.

## Notes

- Do not commit or create a PR against `main` or any branch (that is `wikicommit-merge`'s responsibility)
- Survey mode (Step 0) writes nothing. Its only command is a read-only script, and a run that ends without a topic being chosen leaves the wiki exactly as it was
- Do not write to `.wikicommit/schema/` (read-only)
- Do not include claims in the document that aren't in a grounding page's body content (hallucination prevention; written in Step 5, verified in Step 5.5)
- Do not write a `type:` on a view page, and do not invent a `kind` outside the six in Step 5's table. Both are ERRORs at the quality gate. No kind at all is a valid answer
- The grounding set never includes a page that is itself synthesized (one carrying `derived_from`), so a view page always sits at most one step above ordinary pages (Step 3 item 2). Nor does it include a translation — originals only, found by searching `primary_lang` (Step 1). With the view tree that rule also has a location: **no page under `.wikicommit/view/` is ever grounding material**. View pages stay in the search index — the exclusion is on the grounding set only
- This Skill's side effects are confined to two local writes under `.wikicommit/view/`: the view page itself (Step 9) and its language's `index.md` (Step 10) — besides its review record under `.wikicommit/review/` and its run record. It never writes to `.wikicommit/entity/`. `search_index.py` automatically rebuilds the index file (`.wikicommit/.cache/search_index.sqlite3`, not tracked by Git) when it doesn't exist or no longer matches the pages (a page added, edited or removed since it was built — it then prints a `NOTE:` line)
- A grounding page's own `review_status: pending` **is** surfaced, in the same words `wikicommit-ask` uses (Step 4, repeated in Step 11). It warns and does not block: a wiki fresh out of a generation batch is entirely `pending`, and gating there would disable the Skill exactly when it is most useful
