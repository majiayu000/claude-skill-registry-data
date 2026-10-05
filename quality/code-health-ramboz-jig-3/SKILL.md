---
name: code-health
description: >
  Run a static-analysis pass on a project — detect the ecosystem (Python or
  Node), drive its linter (ruff / eslint, plus advisory pyright/complexity/
  prettier and a cross-ecosystem duplication signal) via the `health.py`
  helper, and act on the normalized exit code
  (0 clean / 1 findings / 2 no-linter). Auto-triggers when you say lint this,
  check code health, run the linter, ask is this code clean, ask any lint
  issues, or want a static analysis pass. Tools are resolved on PATH or run
  ephemerally via uvx / pipx / npx — it installs nothing.
  Defers to any other installed skill whose description identifies it as
  handling linting, static analysis, or code quality — prefer it over this
  baseline. Do not use for running tests (use `/jig:tdd-loop`), for
  security review (use `/jig:security-review`), for spec-compliance review
  of a finished slice (use `/jig:independent-review`), or for general PR
  craft review (use `/jig:pr-review`).
user-invocable: true
---

> Spec 060 introduced `code-health` as the **static-analysis sibling of
> `tdd-loop`**, under [ADR-0017](../../docs/decisions/adr-0017-scaffolded-code-health.md)'s
> "detect the language → drive its blessed tools → normalize → degrade
> gracefully" framing. Like `tdd.py`, the deterministic detection +
> subprocess invocation live in `health.py`; this SKILL.md drives the
> judgment layer. If another installed skill's description identifies it as
> handling linting / static analysis / code quality, the Codex skill
> router prefers it — the deferral is **category-based**.

## What this skill does

Detects the project's ecosystem and runs its linter, normalizing the result
so callers can branch deterministically. Ecosystem detection is
**table-driven** — each ecosystem (Python, Node) is a data-structure entry,
so adding a language is an entry, not a control-flow fork. Current scope:
**Python (ruff) + Node (eslint)**, each with **advisory** secondary signals.

- A `.jig/lint-command` override always wins and **bypasses ecosystem
  detection entirely** (honored verbatim — same semantics as `tdd.py`'s
  `.jig/test-command`).
- Otherwise detects the ecosystem by marker files (`pyproject.toml` / `*.py`
  for Python; `package.json` for Node) and resolves its primary linter:
  - **Python** — `ruff` on `PATH` → `uvx ruff` → `pipx run ruff` (ephemeral),
    invoked as `ruff check --output-format=json <dir>`.
  - **Node** — `eslint` on `PATH` → `npx eslint` (ephemeral), invoked as
    `eslint --format json <dir>`.
- Parses the result into a **tight summary** — a findings count + the top
  rule codes, not the raw dump (per spec 057's "tight envelope, not a
  transcript").
- Adds an **advisory** dimension that is *reported, not gating* (it never
  changes the exit code):
  - **Python — complexity:** an advisory ruff probe with
    `--select C901,PLR0911,PLR0912,PLR0913,PLR0915` surfaces a per-function
    complexity signal ("complexity: N function(s) over threshold; top: …").
  - **Python — type checking:** an advisory `pyright --outputjson` probe
    resolves `pyright` on `PATH`, then `uvx pyright`, then `pipx run pyright`.
    Type diagnostics are summarized as a count + representative rules
    ("pyright: N type diagnostic(s); top: …"). If no type-checker resolves,
    it emits `pyright: skipped (no type-checker) …`. Like every advisory
    signal, it is reported, never gating.
  - **Node — formatting:** an advisory `prettier --check` probe surfaces
    files that need formatting ("prettier: N file(s) need formatting").
  - **Cross-ecosystem — duplication:** an advisory probe (run for BOTH
    Python and Node) reports copy/paste duplication. It is **native-first**
    (an explicit extension point for a future per-ecosystem native
    duplication tool — currently empty, since no jig ecosystem ships a
    distinct native detector), falls back to an ephemeral **`npx jscpd`**
    when `npx` is on `PATH` (the Node analogue of `pipx run`, works on any
    language, installs nothing), and otherwise emits
    `duplication: skipped (no detector) — install a duplication tool or Node
    (npx jscpd) to enable`. When it runs, the summary is a tight
    percentage + the top clones as `file:line`
    ("duplication: 4.2% (12 clones); top: foo.py:10, bar.py:88") — never the
    raw jscpd log. Like the other advisory signals it is **reported, never
    gating** (it cannot change the exit code).
- Normalizes the **primary** linter's exit code:
  - `0` — clean (no findings)
  - `1` — findings exist (the linter ran and reported issues)
  - `2` — no linter resolvable, no recognized ecosystem, OR the resolved tool
    failed to start
- Degrades gracefully (AC4), never a stack trace:
  - **no markers** → exit `2` + "no recognized ecosystem (Python/Node) found
    — set .jig/lint-command to run your linter".
  - **one ecosystem, no resolvable linter** → exit `2` + an
    ecosystem-specific recommendation (ruff/pipx for Python; eslint/npx for
    Node).
  - **mixed (2+ ecosystems)** → exit `2` + a recommendation naming the
    detected ecosystems and pointing at `.jig/lint-command` to disambiguate.

It **installs nothing** — `uvx` / `pipx` / `npx` run the tools ephemerally
only if those launchers are already on `PATH`.

## Helper invocations

Two subcommands mirror `tdd.py`: `detect` reports which linter resolves, and
`check` runs it.

### Detect the linter

```bash
python3 "${PLUGIN_ROOT}/skills/code-health/health.py" detect [target]
```

- `target` defaults to `.` when omitted.
- Stdout: the resolved primary linter name across ecosystems (`ruff`,
  `uvx ruff`, `pipx run ruff`, `eslint`, or `npx eslint`).
- Exit `2` with a recommendation on stderr if nothing resolves (no recognized
  ecosystem, no resolvable linter, or a mixed project needing disambiguation).

### Run the lint pass

```bash
python3 "${PLUGIN_ROOT}/skills/code-health/health.py" check [target]
```

- Auto-resolves the ecosystem's linter via the same logic as `detect`.
- Prints a tight summary (count + top rule codes) to stdout, plus any
  **advisory** lines (Python complexity / Python pyright / Node prettier /
  cross-ecosystem duplication) — advisory lines are reported but never
  change the exit code.
- Exit code is normalized off the **primary** linter (`0` clean / `1`
  findings / `2` no-linter) per the table above. Branch on it
  deterministically — exit `1` means inspect the summarized findings; exit
  `2` means the tool couldn't even start, no ecosystem was recognized, or a
  mixed project needs `.jig/lint-command` disambiguation — not "the code is
  clean".

### Override the auto-detection

Create `<target>/.jig/lint-command` with the first non-blank, non-comment
line being the exact command to run. It is honored **verbatim**, takes
priority over all auto-detection, and **bypasses ecosystem detection
entirely** — the same semantics as `tdd.py`'s `.jig/test-command`. Useful for
a project whose linter isn't ruff/eslint (e.g. `flake8 src` or `pylint
mypkg`), or to disambiguate a mixed Python+Node repo. (This is how jig's own
CI is unaffected — jig commits a `.jig/lint-command`.)

## When NOT to use

- **Running tests** — that's `/jig:tdd-loop` (`tdd.py`). Static analysis and
  the test loop are different cadences.
- **Security review** — that's `/jig:security-review`; this skill is about
  lint / style / correctness signals, not vulnerabilities.
- **Spec-compliance review** of a finished slice — `/jig:independent-review`.
- **General PR craft review** — `/jig:pr-review`.
- **Pure-documentation edits** that touch no code.

## Relationship to other skills

`health.py` is the static-analysis sibling of `tdd-loop`'s `tdd.py` — same
detect → drive → normalize → degrade shape, same `.jig/*-command` override
idiom, same `0 / 1 / 2` exit contract. Per [ADR-0002](../../docs/decisions/adr-0002-contracts-stays-deferred.md)
the shared idioms (`_read_text_safe` / `_custom_command_file` /
`_parse_custom_command`) are **inline-mirrored**, not extracted into a
`_common` module — this is only the second helper of its kind, and the two
have independent lifecycles. The deliberate duplication is noted in
`health.py`'s module docstring (exactly as `tdd.py` documents its own
duplication of `scaffold.py`).

## The code-health review pass (slice 060-05)

Beyond the `health.py` runner, jig wires a distinct **code-health review
pass** into the post-implementation flow (alongside compliance / craft /
arch). The layering ([ADR-0017](../../docs/decisions/adr-0017-scaffolded-code-health.md)):
the **spine runs the tool** (`health.py`), and a **read-only `reviewer`
subagent judges its tight summary** — rendering the judgment a static tool
*can't*: is reported duplication within the [ADR-0002](../../docs/decisions/adr-0002-extract-helper-on-third-caller.md)
inline-mirror budget (two callers may mirror; a third triggers an extract)?
is a flagged complex function inherent or fixable? are the lint findings
worth blocking on?

- **The reviewer never runs `health.py`.** It is read-only
  (Read/Glob/Grep, no Bash). The orchestrator / CI runs `health.py`,
  captures the tight summary, and feeds it into the prompt via
  `review.py code-health … --summary-file <path>` (or `--summary-file -`
  to pipe it in — stdin is never read implicitly, bug 017). The reviewer
  judges the summary, never raw logs.
- **The pass is GATED, not always-on.** It runs only when a slice's
  frontmatter declares `code_health_review: true` — exactly mirroring how
  `arch_review: true` gates the arch pass. **Why gated:** ADR-0017 flags
  the per-slice review cost (the spec 055/057 context-cost discipline —
  every pass adds orchestrator turns + a subagent), and recommends gating
  it like arch-review rather than spending it on every slice. The flag
  defaults off, so existing slices are unaffected; a slice author opts in
  when a change is duplication-/complexity-heavy enough to warrant the
  judgment.
- **Evidence + block rule.** The verdict is recorded as
  `docs/specs/NNN-slug/reviews/slice-NN-code-health.md` ([ADR-0014](../../docs/decisions/adr-0014-review-evidence-model.md)
  evidence model). `[blocker]`-tagged findings block the `REVIEWED`
  transition; `[nit]`-tagged findings become reconciliation-log items —
  the same rule as the craft/arch passes. `workflow.py transition`
  requires the `code-health` verdict for `REVIEWED`/`DONE` iff the flag is
  set. Query the flag with
  `workflow.py code-health-review-needed <spec.md> <slice>`.

See `skills/spec-workflow/SKILL.md` § "After implementation" for the full
four-pass orchestration recipe.

## Gotchas

- **A configured `review.code_health_skill` (scaffold.json) is honored only in
  the orchestrated code-health pass, not on interactive `/jig:code-health`.**
  Spec 096-01 / ADR-0040 D1 makes `code_health` one of the three extensible
  categories, so a project can name a richer code-health reviewer in
  `scaffold.json`; that key is read by `review.py` when it builds the
  **code-health pass** prompt for the spec-workflow reviewer subagent (before
  096-01 that builder had no richer dispatch at all). It is **not** consulted on
  this interactive invocation. Config honoring on orchestrator-invoked surfaces
  is a tracked follow-up (ADR-0040 OQ1).
- **Scope is Python (ruff, + advisory complexity and pyright) and Node
  (eslint, + advisory prettier --check), plus a cross-ecosystem advisory
  duplication signal (`npx jscpd`).** The dedicated code-health reviewer pass (slice
  060-05) is now live — see "The code-health review pass" above; the Tier-2
  scaffold-the-floor work (slice 060-06) is **DEFERRED**. An unrecognized
  ecosystem with no `.jig/lint-command` override degrades to a recommendation.
- **Advisory ≠ gating.** The complexity and pyright (Python), prettier
  (Node), and duplication (cross-ecosystem) signals are reported in the
  summary but **never** change the exit code — the exit code is driven solely by the
  primary linter (ruff / eslint). A clean ruff run with complexity or
  type findings still exits `0`.
- **Duplication is honest about being unavailable.** Unlike complexity /
  prettier (which stay silent when their tool isn't present), the duplication
  probe emits `duplication: skipped (no detector) …` when neither a native
  tool nor `npx` is available — so a reader knows the dimension was *not
  measured* rather than *measured clean*. It writes jscpd's JSON report to a
  temp dir outside the project (read back, then removed) so it never pollutes
  your tree, and runs jscpd without `--threshold` so jscpd itself never exits
  non-zero (advisory, not gating).
- **The override path runs no advisory probes** (including duplication) — it
  honors `.jig/lint-command` verbatim without ecosystem detection, so jig's
  own dogfood CI (which sets an override) is unaffected.
- **Mixed repos degrade, they don't guess.** If both `pyproject.toml` (or
  `*.py`) and `package.json` are present, `check` exits `2` and asks you to
  set `.jig/lint-command` to disambiguate — it never picks one for you.
- **Exit `1` vs `2`.** Exit `1` means the linter ran and found issues —
  inspect the summary. Exit `2` means no linter was resolvable, no ecosystem
  was recognized, a mixed project needs disambiguation, or the resolved tool
  failed to start (an environment issue) — don't conflate any of those with
  clean.
- **Ephemeral runs need a network/cache.** `uvx ruff` / `pipx run ruff` /
  `uvx pyright` / `pipx run pyright` / `npx eslint` / `npx prettier` /
  `npx jscpd` fetch the tool on first use. If neither the binary nor a
  launcher is present, the skill recommends (for the primary linter) or
  reports `skipped` (for pyright/duplication) rather than failing opaquely.
- **Tight summary, not the raw dump.** `check` parses the linter's JSON into
  a count + top codes; it does not echo the full tool output. Re-run the
  linter directly when you need every finding's location.
