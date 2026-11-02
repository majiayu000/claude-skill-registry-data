---
name: interactive-notebook-demo
description: |-
  Use when authoring or reviewing a hands-on demo, tour, or walkthrough notebook (`#%%` percent-format or Jupyter) that demonstrates a feature, library, or API and doubles as semi-interactive documentation. Triggers: "write a demo notebook", "build a feature demo", "demo this library/API", "a notebook to walk through X", "interactive docs for this feature". Not for production/analysis notebooks or pure asyncio event-loop mechanics (see python-notebooks-async).
---

# Interactive Notebook Demo

## Overview

A demo notebook does two jobs at once, and must do both:

- **Orient** — it doubles as semi-interactive documentation for a feature.
  Read top to bottom, it should leave the reader understanding the motivating problem, the design, the mechanism, and the data flow — the narrative layer over the code.
- **Interact** — a reader can run one operation, read the **real** output, edit a literal, and re-run, building hands-on understanding by poking at it.
  The cells are the examples; git holds the original, so they can change anything and revert.

The orientation is _what_ to teach; the interaction is _how_ to teach it.
A notebook that interacts beautifully but explains nothing is a toy; one that explains but only runs as opaque blocks is a slideshow.
Clear both bars.

Two failure modes make a notebook _performative_ (a script that happens to have cell markers) rather than interactive:

1. **Wrapper functions.**
   Grouping operations into `async def demo_function(...)` and calling them as opaque blocks.
   The reader can only run the whole block; they cannot step into a single call and tweak it.
2. **Terse labels.**
   Printing `f"created {name}"` instead of showing the evidence — the object the call returned, the before/after, the read-back.
   The reader has to take the markdown's word for it.

This skill is the bar a demo notebook must clear.
It is language-agnostic in principle; examples use Python because most demo APIs are.
For asyncio event-loop ownership (top-level `await`, kernel-owns-the-loop), defer to `python-notebooks-async`.

## When to Use

- Writing a `#%%` / percent-format or `.ipynb` notebook that demonstrates a library, API, or service so a maintainer can experiment with what was built.
- Reviewing a demo notebook that "looks like a script," wraps steps in functions, or prints labels instead of proving effects.
- Converting a working script into a genuinely interactive walkthrough.

### When Not to Use

- Production pipelines, ETL, or analysis notebooks where reusable logic _should_ live in functions/modules — extract to `.py` and test it.
- Pure asyncio mechanics (`RuntimeError: event loop already running`, `asyncio.run()` in a cell) — see `python-notebooks-async`.
- One-shot throwaway exploration no one else will read.

## Invocation Notice

- Tell the user when this skill is running: `interactive-notebook-demo`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## What the demo must orient the reader to

A reader should come away understanding the feature, not just a list of callable methods.
Convey each of these through the prose and the evidence — never by labeling a cell with the lens name (see _Write it, don't announce it_, below):

- **The motivating problem.**
  What pain drove this and who it's for — the job it's hired to do.
  A reader who knows why it exists reads every later cell with the right frame; open with it and keep each section anchored to it.
- **The design.**
  The core components, how they layer, and the non-goals — what it deliberately doesn't do.
  Sequence the notebook to mirror this shape (see narrative arc, below) so the structure itself teaches the architecture.
- **The mechanism.**
  What actually happens under the hood for a representative operation — make the invisible visible.
  Don't just create a record and print "ok"; surface the value the system computed so the reader sees the rule fire.
- **The data flow.**
  What moves where, especially across boundaries — input → which layer → storage → response; what crosses a trust or process boundary and what deliberately stays behind.
  Trace one representative path end to end.

Pull these through as well — they are usually the difference between a tour and real orientation:

- **Vocabulary.**
  Define each domain term on first use.
  A newcomer drowns in unexplained nouns; one sentence where the term first appears is the cheapest, highest-leverage orientation you can give.
- **Guarantees and invariants.**
  Make the system's promises observable — a rejected stale write, an unauthorized call refused, a retried write that stays idempotent.
  This is where _prove-with-data_ earns its keep: don't assert the guarantee, demonstrate it.
- **Failure modes.**
  Show how the system says no — its errors made tangible (the error-demo cells).
  The shape of failure orients as much as the happy path.
- **Pointers into the code.**
  Close each section with the real source, spec, or test behind it, so the documentation links back to what it describes rather than dead-ending.
  This is what keeps the demo anchored to the code it documents.

## Core principles (the bar)

1. **One claim per cell.**
   Each cell demonstrates one idea, and its output stands on its own.
   Usually that's one call; group calls only when the claim needs them together (a setup→read pair, a before/after), never to save space.
   No `main()`, no multi-call wrapper functions (one exception below).
2. **Idempotent cells, or marked.**
   Aim for cells a reader can re-run any number of times with the same outcome, so re-running one never desyncs the others (whether or not they've been run).
   Reads, lookups, and set-to-a-fixed-value calls are naturally idempotent — leave them unmarked.
   When the underlying operation can't be — it bumps a version, appends, increments, or has an external side effect — that's fine, but **mark the cell** with a short, consistent note (`# not idempotent: re-running adds a revision`).
   Marking is an expectation, not a judgment call: an _unmarked_ cell is then a trustworthy promise that re-running it is safe.
   The reset for accumulated drift is the whole-notebook contract — **Restart→Run-All must pass.**
   Keep the reader's knob in plain view, not buried in `setup()`.
3. **Markdown teaches before each cell.**
   Precede each code cell with a `# %% [markdown]` cell of 2–4 sentences explaining what it demonstrates and why it matters — teach, don't label.
   This prose carries the orientation: tie the operation to the motivating problem, surface the mechanism or invariant it shows, define any new term.
4. **Write it, don't announce it.**
   Make relevance evident in the writing; never prepend a meta-label.
   No `**Why this exists:**`, `**What you'll learn:**`, or `**Story:**` prefixes — the first sentence already carries the point.
   Give each section a heading that states its claim ("## Edits version — they don't overwrite"), not a bare noun ("## Editing"), so the headings read as the story and the notebook is navigable.
   See `antislop-writing`.
5. **Prove the effect with real data.**
   Every claim the markdown makes must be visible in the cell's output — show the evidence, not a summary:
   - Dump the whole object the call returned when its shape is instructive (e.g. `print(result.model_dump_json(indent=2))` for a pydantic model), not one cherry-picked field — but skip dumps so large they bury the point.
   - Show before and after for a mutation, side by side — the values, never a bare `True`/`False`.
   - For an invariant, `assert` it with the values in the message (`assert rb == expected, (rb, expected)`): the claim is visible _and_ a wrong value fails the kernel run instead of quietly printing `False`.
   - Read the record back after a write and print what came back, to prove it landed.
6. **Interactive-first.**
   Top-level `await` in cells (the kernel owns the loop).
   No `if __name__ == "__main__"` script guard — straight-line `python file.py` is _not_ a supported mode.
   Make cleanup its own clearly-marked final cell the reader runs when done.
7. **kwargs everywhere.** `client.update(record_id=rid, data=payload, expected_revision=3)` — explicit names aid comprehension and survive signature drift.
   **Verify against the real signatures**; naive guesses drift (a parameter you'd call `path` is really `path_prefix`, `version` is really `target_version`).
   Read the source before you write the call.
8. **try/except only where the error is the point.**
   Keep it for cells whose purpose is to show a failure (a version conflict, an authorization denial, a validation error).
   Delete defensive `try/except Exception` around calls that just work — let the reader see the real call and its real result.

## Structure

- **Narrative arc, not an API index.**
  Order sections as a story that mirrors the design: open with the motivating problem, build from primitives to composed behavior, happy path before edge cases, and let the failure and guarantee cells land _after_ the reader has seen the thing work.
  The sequence should teach the architecture; never sort cells alphabetically by method name.
- **Header cell.**
  Lead with the motivating problem and the mental model (the core nouns and how they relate), then the run mechanics: supported environments (VS Code Interactive / Jupyter), that the kernel handles top-level `await`, that the reader can edit any input and re-run to explore (git holds the original), the re-run convention (unmarked cells are safe to re-run; `# not idempotent` cells mutate each run, and Restart→Run-All resets), and any optional dependency the later cells need.
- **Setup may stay a function.**
  Connection or bootstrap boilerplate the reader doesn't need to inspect granularly can remain an `async def setup(...)`, invoked in its own cell that unpacks into notebook-scope variables.
  Everything _after_ setup is flattened to one cell per claim.
- **Close each section with where it lives.**
  A short pointer to the real source, spec, or test behind the section, linking the documentation to the code it describes — written as a sentence, not a `**Where this lives:**` label.
- **Zero-infrastructure default.**
  The primary notebook should run with no external services (local or in-memory backends) under a self-cleaning temp dir, so a reader can run it immediately.

## Infrastructure-dependent notebooks (remote backends)

For a notebook that needs a database, object store, or other services:

- **Probe-first.**
  The first cell is a connectivity probe.
  On failure it prints actionable guidance (how to start the stack, which ports) with **no traceback**, and makes clear the later cells need the stack.
  Subsequent cells may assume the connection succeeded.
- **Coexist with the test stack.**
  Ship a demo `docker-compose.yaml` on non-conflicting host ports so the demo and test stacks run side by side; document the ports/DSNs in the file header.
- **Graceful skip, never a wall of red.**
  Absent services → one clear message, not a stack trace.
- **README + gitignore.**
  A short `README.md` (how to open in VS Code/Jupyter, how to start the stack, a port table) and a `.gitignore` for demo artifacts (local DB files, data/temp dirs).

## Validate the real artifact — don't fool yourself

The committed `.py` percent-file **is** the artifact.
Its top-level `await`s are the part most likely to break interactively — so they are exactly what you must execute.

- **Do not validate an async-wrapped copy.**
  Wrapping the cells in `async def main(): ...; asyncio.run(main())` for a quick `python` run is a trap: it exercises a _different_ program and leaves the real top-level-await artifact unverified. (This is the mistake to catch in review.)
- **Run the actual `#%%` file through a live kernel** via jupytext + ipykernel, then assert zero unexecuted cells and zero error outputs.
  Never commit the generated `.ipynb`.
- Exact headless commands, sandbox `JUPYTER_*` redirects, and the ruff per-file-ignores notebooks need (`F704` top-level await, `E402`, `B018`, `D`, `S`) are in `references/headless-validation.md`.
- Clean up any scratch files; leave nothing behind.

## Common mistakes (review checklist)

- **Wrapper-per-topic functions** — a whole topic behind one `await demo_topic(...)` block instead of cell-per-claim.
- **Labels instead of evidence** — `print("done")`, or a bare `True`/`False`, rather than the returned object, the before/after, the read-back.
- **Non-idempotent cell, unmarked** — re-running mutates state (version bump, append) with no marker, so the reader can't tell it's unsafe to hammer.
- **Meta-labels and flat headings** — `**Why this exists:**` / `**Story:**` prefixes, or bare-noun headings that don't state a point.
- **Operations without orientation** — correct cells that never convey why, what they prove, or where the code lives.
- **Method-index ordering** — sections sorted by API surface, not told as a story.
- **Unexplained vocabulary** — domain nouns used before they're defined.
- **Defensive try/except** — swallowing errors around calls that work, hiding real behavior.
- **Positional args from memory** — guessed names that drift from the real signature.
- **Validating a stand-in** — an async-wrapped copy or `python file.py` path; neither runs the real artifact through a kernel.
- **Committing the `.ipynb`** — the `#%%` `.py` is the source of truth; the executed notebook is a byproduct.

## References

- `references/headless-validation.md` — run the real `#%%` file through a live kernel, sandbox env setup, ruff per-file-ignores, gitignore/README checklist.
- `references/cell-patterns.md` — copy-paste cell skeletons: header, section opener, point-into-the-code closer, markdown-then-operation pairing, prove-with-data idioms, the error-demo cell, the connectivity probe, and cleanup.
- `references/notebooks-async.md` — event-loop ownership, top-level `await`, and background-task patterns for demos with async cells (shared from `python-notebooks-async`).
