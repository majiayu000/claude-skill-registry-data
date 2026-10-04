---
name: attempt-audit
category: tooling
description: >-
  Find absence-assertions that carry no attempt-record — code that returns the
  same empty value whether the work RAN and found nothing or was SKIPPED
  entirely, so the caller cannot tell the two apart. Detects the concrete
  syntactic shape: a boolean parameter gates real work, and the function falls
  through to an empty sentinel that records nothing. Zero config, one command,
  plain-language findings; reports what it could not parse rather than letting a
  clean run and an empty run look identical. USE WHEN a check "passed" and you
  are not sure it ran, a manifest reports "no results / no findings / no speech",
  a gate went green after a rename, a test suite is suspiciously fast, or before
  trusting any tool that emits a negative verdict. NOT FOR general linting, dead
  code, or type errors — it answers exactly one question.
---

# attempt-audit — an absence with no attempt-record is not evidence

## The one command

```bash
python3 scripts/attempt_audit.py            # audits the current directory
python3 scripts/attempt_audit.py <path>     # a file or a directory
python3 scripts/attempt_audit.py --json     # machine-readable
```

No config file. No flags to memorise. No path required. That is the whole interface.

## What it looks for

One shape, precisely:

```python
def load_transcript(info, allow_whisper, outdir):
    if allow_whisper:                          # a switch gating real work
        cues = _whisper_faster(...) or _whisper_cli(...)
        if cues:
            return join_deoverlap(cues), cues  # the computed result
    return "", []                              # the SAME value when skipped
```

A caller receiving `("", [])` cannot distinguish *"ASR ran, the clip was silent"*
from *"ASR was never invoked."* In the case that produced this tool, that
ambiguity became a confident `frames-mandatory` verdict with an empty
`degradations` list, on a clip carrying 282 words of speech.

The detector requires **all** of:

1. a top-level `if` whose test is a **bare truthiness check on a parameter** —
   `if flag:` or `if not flag:`. Nothing compound: a test like
   `if a is not None and sha256(f) == expected` is a computation over data, and
   naming one of its operands produces a false sentence;
2. the guard's **body** does real work — a call, an assignment, a loop. A body
   that immediately returns a constant is a validation branch: every guard ran
   and nothing was skipped;
3. the guard contains a `return` of a computed value;
4. the guard is the **last statement before** the fall-through. Work in between
   means the function tried an *alternative* rather than skipping;
5. the function falls through to `return <empty sentinel>` — `None`, `""`, `[]`,
   `{}`, or a tuple of those. **Not `0` or `False`**: `return 0` from a command
   handler is process success, and `False` is an answer, not an absence;
6. nothing on the skipped path records the skip.

Every one of these narrows the detector. That is deliberate — see *Recall* below.

## What it deliberately does not flag

Requirement 2 is what keeps it honest. Without it the detector flags every
validation chain, which is a different and correct shape:

```python
def failure_reason(frames_raw, kept, sheet):
    if frames_raw <= 0:
        return "no frames could be extracted"   # returns immediately — no work
    ...
    return None                                 # every guard RAN; None is true
```

Also not flagged: search loops (`for … if match: return i` / `return None` —
searched and not found is not the same as never searched), guards on the subject
being examined (`if isinstance(entry, dict):`), guards whose only call lives in
the test (`if len(text) < 5: return True`), guards followed by an alternative
path, and any function that records its skip.

Recording the skip is the fix, so recording it removes the finding.

## Reading the output

```
scripts/video_ingest.py:967  load_transcript()
  Returns ('', []) when `allow_whisper` is false — the same value it
  returns when the work ran and found nothing. A caller cannot tell
  "never attempted" from "attempted, and empty".
  Guard at line 963 is skippable and records nothing.
  Fix: return a distinct value, or record the skip in the same object.
```

Exit codes: **0** clean · **1** findings · **2** something could not be read — nothing to scan, a bad path, an unparseable file, or a directory it could not enter. **0 never means every file was seen:** directories in `SKIP_DIRS` and dot-directories are skipped by design, named in the output and in the JSON `skipped_dirs`, and do not change the exit code.

## It does not commit the defect it audits

A tool that printed "nothing found" identically whether it read 400 files or 0
would be exactly the failure it looks for. So:

- **Scanning nothing is not clean.** Zero files scanned prints *"Scanned 0 files
  — nothing was audited. This is NOT a clean result"* and exits **2**, distinct
  from the exit **0** of a real clean run.
- **Unreadable files are named.** Anything it cannot parse is listed as *"these
  were NOT audited"* with the reason, never silently dropped.
- **Skipped directories are counted and named.** `SKIP_DIRS` and dot-directories
  are reported, not swallowed, and `os.walk` runs with an `onerror` handler so a
  permission-denied subtree is named rather than vanishing.
- **Exit 0 requires that nothing was unreadable.** If a file could not be parsed
  or a directory could not be entered, the run exits **2** — reporting success
  over a tree it failed to read would be this tool's own defect. Deliberately
  skipped directories (`SKIP_DIRS`, dot-dirs) are a different case: they are
  named in the output, but they do **not** move the exit code, so a defect inside
  `build/` or `.github/` yields exit 0 with a "Skipped 1 director(ies)" line.
  Read the output, not only the status.
- **A clean run states its own limit.** It prints *"this shape was not found —
  which is not the same as every absence being evidenced."* The tool finds one
  syntactic shape; it does not certify your absences.

## Two fixes, in order of strength

1. **Make the confusion unrepresentable** — the empty value stops being able to
   mean two things:
   ```python
   transcript: Measured(int) | Unattempted(reason)
   ```
2. **Record the skip** in the same object the verdict travels in:
   ```python
   degradations.append("ASR disabled (--whisper not passed); unattempted, not empty")
   ```

Fix 2 alone leaves the confusion representable; anyone who later reads only the
value re-enters the trap. Fix 1 is the durable one.

## Scope, stated plainly

Python only. One syntactic shape. It will not find an absence-without-attempt
expressed through a class attribute, a global, a database column, or a network
response — those are the same defect and this tool is blind to them. It is a
tripwire on the most common form, not a proof of anything.

## Recall — what it misses, named

This is a **tripwire for one spelling**, not a survey. It is tuned for precision
because a noisy tripwire gets muted. Shapes carrying the same defect that it does
**not** find, all confirmed by adversarial review:

- **the early-return spelling** — `if not flag: return "", []` followed by the
  work. Structurally invisible: rule 3 wants the computed return *inside* the
  guard. This is the largest known gap;
- **a switch that is not a parameter** — a module-level constant, or `self.allow`
  on a method;
- **a switch read indirectly** — `kwargs.get("enabled")`, a dispatch table, a
  ternary or `and`-short-circuit instead of an `if`;
- **a guard nested inside `try:` / `for:` / `while:`** — only the function's top
  level is examined;
- **an accumulator return** — `out = []; if flag: out = work(); return out`;
- **`else: return "", []`** rather than a fall-through;
- **anything outside a Python `if`** — a class attribute, a database column, an
  HTTP response;
- **one innocuous statement between the guard and the sentinel.** Rule 4 wants
  them adjacent, so `print("done")` before the fall-through, an intermediate
  `empty = []; return "", empty`, or simply another guard sitting after the
  switch all hide a genuine finding. Rule 4 buys precision and costs real
  recall — that trade is deliberate, and this is its price;
- **a skipped path containing a name that merely looks like a record.**
  `_records_a_skip` substring-matches hints such as `log`, `note`, `err` over
  every identifier on that path, so a local called `catalogue_count` or
  `dialog` silences a true finding. It also under-suppresses: a function that
  records its skip *before* the guard is still reported.

A clean run means *this shape was not found in the files it read*. It is not a
statement about your absences.

## Validation

```bash
python3 -m pytest tests/test_attempt_audit.py -q   # unit tests
./tests/mutation_proof.sh                          # arms + a breakage sentinel
```

`mutation_proof.sh` removes one behaviour per arm and names the test that must go
red. Two things make its verdicts mean something:

- **a per-arm sanity probe** — the mutated script must still audit a clean file
  correctly. Red from a mutant that cannot run is breakage, not evidence;
- **arm 0, a sentinel** — a totally broken script (`sys.exit(3)`) must be
  *rejected as invalid*, not counted as a kill. An earlier version ran one global
  control before any mutation and called that pairing; replacing the whole script
  with `sys.exit(3)` scored every arm KILLED.

The negative tests assert an empty finding list, which is a one-bit check; the
positive and dogfood tests assert the function, the guard name and the returned
value. Where a one-bit assertion is load-bearing, the mutation arm is what gives
it teeth.

**Dogfood gate:** `test_dogfood_catches_the_reference_case` runs the auditor over
the real `~/broomva/scripts/video_ingest.py` and requires it to flag
`load_transcript` naming `allow_whisper`. If that stops holding, the skill is
broken regardless of the unit tests.

## Related

- **BRO-2142** — the fix in `video_ingest.py` this tool generalises
- **BRO-2190** — the skillify tier model; this is the worked **Tier D** example
- `research/entities/pattern/default-off-channel-reads-as-absent-signal.md`
- `research/entities/concept/carrier-state-failure.md` — the symptom class
