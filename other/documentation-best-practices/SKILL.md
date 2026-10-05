---
name: documentation-best-practices
description: "Almost all bad documentation is well-intentioned writing in which two or more"
---

# Documentation Best Practices (Verbose)

## Core Patterns

### The Four Kinds, and Why Mixing Them Ruins Docs

Almost all bad documentation is well-intentioned writing in which two or more
purposes have been welded into one page. The reader arrives with one need and is
served three, so the page fails all three. The Diátaxis framework names the split
along two axes: is the reader *learning* or *working*, and does the content serve
*practice* or *understanding*?

| | Practical | Theoretical |
|---|---|---|
| **Learning** | Tutorial | Explanation |
| **Working** | How-to guide | Reference |

Each kind has a different author contract.

**Tutorial — a lesson, for someone with no context.** The reader's goal is not to
accomplish their own task; it is to gain confidence that the thing works and that
they can operate it. Therefore: one path, no choices, sample data you supply,
every command written out, guaranteed to succeed. Do not explain the
architecture; do not mention alternatives; do not say "you could also".

```
✅ Tutorial: "Build your first pipeline"

   You'll build a pipeline that reads three sample CSVs and writes a
   summary table. Takes about ten minutes.

   1. Install:            pip install acme-pipelines
   2. Get the sample data: acme fetch-samples ./data
   3. Create pipeline.py:  [complete file, not a fragment]
   4. Run it:              acme run pipeline.py
   5. You should see:      [exact expected output]

   You now have a working pipeline. To schedule it, see
   "Schedule a pipeline". To understand why pipelines are immutable,
   see "Pipeline immutability".
```

**How-to guide — steps for one real goal, for a competent reader.** They already
have a system, they have a specific problem, and they want it solved. Assume
competence, name the goal in the title as a task, and do not teach.

```
✅ How-to: "Retry a failed pipeline run"

   Prerequisites: a run in FAILED state, and `runs:write` on the project.

   1. Find the run id:   acme runs list --status failed
   2. Inspect the cause: acme runs logs <run-id> --tail 50
   3. Retry from the failed step:
        acme runs retry <run-id> --from-failed
      Or retry the whole run: acme runs retry <run-id>

   If the failure was a transient upstream timeout, --from-failed is
   safe. If a step wrote partial output, retry the whole run — steps
   are not individually idempotent unless declared so.
```

**Reference — dry, complete, structured, boring on purpose.** The reader knows
what they are looking for and needs to find it in seconds. Consistency of
structure matters more than prose quality; every entry looks like every other
entry. Reference should be generated wherever possible.

```
✅ Reference

   Pipeline.run(inputs, *, timeout=300, retries=3, on_failure="abort")

   inputs     Mapping[str, Path]   Named input datasets. Keys must match
                                   the pipeline's declared inputs.
   timeout    int, default 300     Per-step timeout in seconds.
   retries    int, default 3       Retries per step. 0 disables.
   on_failure "abort" | "continue" | "skip_dependents", default "abort"

   Returns    RunResult
   Raises     InputMismatchError   inputs keys don't match the declaration
              StepTimeout          a step exceeded timeout after retries
              PipelineLocked       another run holds the pipeline lock
```

**Explanation — prose about why, for a reader who is curious rather than
blocked.** This is where design rationale, trade-offs, historical constraints,
and comparisons belong. It is the only one of the four that may ramble a little,
and the only one that should discuss alternatives that were rejected.

```
✅ Explanation: "Why pipelines are immutable"

   A pipeline object cannot be modified after construction. This is
   inconvenient — you cannot tweak a step and re-run in a notebook —
   and we chose it deliberately.

   Early versions allowed mutation. Two failure modes dominated support
   load: a pipeline mutated by one thread mid-run produced results that
   matched no version of the code, and re-runs of "the same" pipeline
   were not reproducible, which broke every audit we tried to do.

   The cost is notebook ergonomics. `Pipeline.replace(step=...)` returns
   a new pipeline and covers most of that gap...
```

**The canonical failure** is a page called "Getting started" that opens as a
tutorial, pauses in the middle to explain the execution model, and closes with a
table of all forty configuration options. The learner loses the thread at the
explanation. The person who came to look up a config option cannot find the table
and does not know it is there. The person who wanted to understand the model gets
three paragraphs where they needed a page. Splitting it into four pages costs an
afternoon and every one of them then works.

When you cannot decide which kind a page is, that is a strong signal that it is
two pages.

### Docs as Code

Documentation that lives anywhere other than the repository drifts, because
nothing forces it to move when the code moves. A wiki is a fresh snapshot of
whatever was true when someone last cared.

The operating rules:

- **Docs in the repo**, in the same directory tree, in a plain text format under
  version control.
- **Same PR as the change.** If a PR alters a public interface, a CLI flag, an
  environment variable, or an operational procedure, the doc change is part of
  that PR. Not a follow-up ticket — follow-up doc tickets have a completion rate
  close to zero.
- **Same reviewer.** The reviewer who checks the code checks the doc. A separate
  docs reviewer who does not know the change cannot verify accuracy, only prose.
- **CI enforces what it can**: build the docs, run the samples, check the links,
  fail on a broken reference.
- **Ownership by CODEOWNERS**, so a doc page has a team the same way code does.

The reviewable question for a doc change is not "is this well written" but "is
this true, and is it the right kind of page".

### Fighting Rot: Generate or Test Everything That Tracks Code

Documentation decays at exactly the rate the code changes, and the decay is
invisible — nothing fails, readers just quietly get wrong answers. The
countermeasure is not discipline. It is removing the human from the parts that
can be derived.

| Content | How to keep it true |
|---|---|
| API reference | Generate from docstrings, type hints, or an OpenAPI schema emitted by the server |
| Code samples | Live in the test suite: doctest, or extracted from the docs and executed in CI |
| CLI usage and flags | Generate from the parser definition; fail CI if the checked-in output differs |
| Config keys and env vars | Generate from the settings schema |
| Error catalogues | Generate from the error classes |
| Architecture diagrams | Diagram-as-code in the repo (see `architecture-documentation`) |
| Links | Link checker in CI |
| Screenshots | Automate, or avoid — describe the action rather than picture it |

A hand-maintained parameter table is wrong within two releases and nobody notices
until a user files a bug against your docs. A code sample that nothing executes
has roughly a coin-flip chance of running.

What remains after generation is precisely what humans are good at and machines
are not: the how-to guides, the explanations, and the first-five-minutes path.
That is a much smaller corpus, which is the second benefit — you can actually
maintain it.

**Give every hand-written page an owner and a review date.** A page with neither
is a page nobody will ever delete, and stale documentation is worse than none:
it is confidently wrong, and it costs the reader more than absence would.

**Delete aggressively.** If nobody has read a page in a year and nobody owns it,
deleting it is a net improvement in the corpus. Version control means deletion is
not destruction.

### The README

The README's one job is to let a stranger decide, in under a minute, whether this
project solves their problem — and if it does, to get them running. Everything
else belongs on another page.

```
✅ Structure that works

# acme-pipelines

Declarative data pipelines for Python, with reproducible runs.       <- 1 line

For teams running scheduled batch jobs who need every run to be           <- why
auditable and re-runnable. Pipelines are immutable and content-
addressed, so re-running a run reproduces it exactly.

## Install                                                            <- 1 block
    pip install acme-pipelines

## Quick example                                                <- real, runnable
    from acme import Pipeline, step
    ...
    Run complete: 3 steps, 12,431 rows, 4.2s              <- actual output shown

## Docs
- Tutorial: build your first pipeline
- How-to guides
- API reference
- Why pipelines are immutable

## Contributing · Licence
```

What does **not** go in a README: the architecture, every configuration flag,
the changelog, a feature comparison matrix, a roadmap, badges in three rows, a
long acknowledgements section above the code. All of those push the first code
block below the fold, and a README where you cannot see code without scrolling
has failed for the reader who was evaluating you in a minute.

The example must be real and must run. A README example that has drifted is the
single most damaging stale doc in a project, because it is the first thing anyone
tries.

### The First Five Minutes

The install-to-first-success path deserves more attention than any other page,
because it is the only one where a reader will abandon your project entirely
rather than ask for help.

Test it properly: sit with someone who has never used the project, on a clean
machine, and watch without helping. Write down every point where they stop. That
list — the undocumented prerequisite, the API key you assumed they had, the
command that needs sudo on their OS, the step where "obviously" was doing all the
work — is your highest-value backlog, and it is invisible to anyone who already
knows the system.

Properties of a first-five-minutes path that survives:

- **Verbatim executable.** Copy-paste from the top, in order, with no edits.
- **Zero choices.** Not "install with pip, or poetry, or from source" — pick one,
  put the others in a how-to. Every choice is a place to stall.
- **Sample data supplied.** Requiring the reader to bring their own data before
  the first success guarantees failures you cannot debug.
- **Expected output shown at each step**, so a reader can tell whether they are
  on track without knowing what correct looks like.
- **Run in CI on a clean image.** Otherwise it breaks silently, and it will.
- **Ends at something visibly working,** and points at the next three pages.

### When Not to Write Documentation

Documentation is sometimes the wrong fix, and reaching for it can entrench the
problem it papers over. A page explaining a confusing thing must be maintained
forever and is read by perhaps half the people who hit the confusion.

Before writing, check whether the need disappears with a change to the thing:

```
❌ Doc page: "The third and fourth positional arguments to process()
   control validation and retry behaviour. Pass True, False to validate
   without retrying."

✅ Change the API:
   process(data, *, validate=True, retry=False)
   The call site now reads process(data, validate=True, retry=False)
   and the page is unnecessary.
```

```
❌ FAQ entry: "Why do I get 'Error: invalid configuration'? This usually
   means the region field is missing, or set to a region where the
   service isn't available."

✅ Change the error message:
   "Config error: 'region' is required. Available regions: us-east-1,
    eu-west-1. See config.yaml line 12."
```

```
❌ Doc page: "Remember to call cleanup() after using the client, or
   connections will leak."

✅ Make the client a context manager so the correct thing is the
   default thing, and leaking requires effort.
```

The general rule: prefer, in order, **removing the confusion** (better names,
better defaults, fewer options), then **moving the explanation to where the
confusion happens** (error messages, type signatures, docstrings, `--help`), and
only then **writing a page**. A page is the option with the worst discovery rate
and the highest maintenance cost.

Two corollaries. A frequently asked question is a product defect report, not a
demand for an FAQ entry — the FAQ is where teams file the bugs they have decided
not to fix. And a runbook full of manual steps is a script waiting to be written;
document the script's behaviour instead. For incident-specific write-ups see
`incident-timeline-creation`; for system structure and decision records see
`architecture-documentation`.

## Common Anti-Patterns

❌ **One page that teaches, instructs, and enumerates** — the learner loses the
thread, the looker-up cannot find the table.
✅ Four kinds, four pages, cross-linked. If you cannot name the kind, it is two
pages.

❌ **Tutorials offering choices** — "install with pip, poetry, or from source",
"you could also configure X here".
✅ One opinionated path in the tutorial; alternatives go in how-tos.

❌ **How-to guides that teach** — three paragraphs of concept before step 1.
✅ Prerequisites, then steps. The reader is competent and blocked.

❌ **Prose reference** — narrative paragraphs where the reader needs a scannable
structure.
✅ Uniform entries, generated from the source of truth.

❌ **Hand-maintained parameter tables** next to a generator that could emit them.
✅ Generate from docstrings, type hints, or the schema.

❌ **Untested code samples** — roughly a coin flip whether they still run.
✅ Samples live in the test suite or are extracted and executed in CI.

❌ **Docs in a separate wiki, changed in a separate PR** — drift within a
quarter, because nothing couples them to the code.
✅ Same repo, same PR, same reviewer, CI-enforced.

❌ **"See the code for details" in reference docs** — an admission that the page
should not exist.
✅ Either document it or generate it. A pointer to source is not reference.

❌ **A README with badges, architecture, and a feature matrix above the first
code block.**
✅ One-line what, why, install, smallest real example with output, links out.

❌ **Getting-started guides that fail on a clean machine** — undocumented
prerequisites invisible to everyone who already has them.
✅ Watch a newcomer run it on a fresh environment; re-run it in CI.

❌ **Pages with no owner and no review date** — nobody can tell stale from
current, and nobody feels able to delete.
✅ Owner and review date on every hand-written page; delete unread, unowned ones.

❌ **Documenting around a confusing API** — the page must be maintained forever
and reaches half the affected users.
✅ Fix the signature, the default, or the error message. Then the page is
unnecessary.

❌ **Growing an FAQ** — a list of defects the team has decided not to fix.
✅ Treat repeat questions as product bugs; fix the source of the confusion.

❌ **Screenshots of a UI that changes** — stale within a release and expensive to
regenerate.
✅ Describe the action and the control's label; automate captures if you must
have them.

## Documentation Checklist

- [ ] Every page is exactly one of tutorial, how-to, reference, explanation
- [ ] Pages that mix kinds have been split and cross-linked
- [ ] Tutorial offers no choices and supplies its own sample data
- [ ] Tutorial's expected output is shown at each step
- [ ] How-to titles name a task the reader actually has
- [ ] How-to guides state prerequisites and skip the teaching
- [ ] Reference is generated from docstrings, types, or schema
- [ ] No reference entry says "see the code for details"
- [ ] Explanations cover rejected alternatives and the trade-offs taken
- [ ] Every code sample is executed by CI
- [ ] CLI help, config keys, and env vars are generated, not transcribed
- [ ] Link checker runs in CI
- [ ] Docs live in the repo and change in the same PR as the code
- [ ] Interface or procedure changes cannot merge without their doc change
- [ ] Same reviewer reviews code and docs
- [ ] Every hand-written page has an owner and a review date
- [ ] Unowned, unread pages deleted rather than left to mislead
- [ ] README leads with one line on what and who, then why
- [ ] README's first code block is above the fold
- [ ] README example is real, runnable, and shows its output
- [ ] Architecture, changelog, and full config are linked, not inlined
- [ ] Install-to-first-success path tested on a clean machine by a newcomer
- [ ] That path runs verbatim, with no edits, and is exercised in CI
- [ ] Before writing a page, checked whether a rename or default removes the need
- [ ] Confusing states explained in the error message, not only in docs
- [ ] Repeat questions treated as product defects rather than FAQ entries
- [ ] Manual runbook steps replaced by scripts where they repeat
