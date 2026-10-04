---
name: code-review
description: Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".
---

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating issue / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings.

The issue tracker should have been provided to you — run `/setup-matt-pocock-skills` if `docs/agents/issue-tracker.md` is missing.

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point — a commit SHA, branch name, tag, `main`, `HEAD~5`, etc. If they didn't specify one, ask for it.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here — not inside two parallel sub-agents.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.) — fetch via the workflow in `docs/agents/issue-tracker.md`.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

### 3. Identify the standards sources

Anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below — a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation — and, like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name** — a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code** — the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy** — a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps** — the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery** — one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change** — one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality** — abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man** — a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest** — a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 4. Spawn both sub-agents in parallel

**Standards sub-agent prompt** — include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3, **plus the smell baseline from step 3** pasted in full — the sub-agent has no other access to it.
- The brief: "Report — per file/hunk where relevant — (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk. Distinguish hard violations from judgement calls — documented-standard breaches can be hard, but baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Under 400 words."

**Spec sub-agent prompt** — include:

- The diff command and commit list.
- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned. Do **not** merge or rerank findings — the two axes are deliberately separate (see _Why two axes_).

End with a one-line summary: total findings per axis, and the worst issue _within each axis_ (if any). Don't pick a single winner across axes — that's the reranking the separation exists to prevent.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.

---

## 6. PREFLIGHT — VERIFY BEFORE YOU SPAWN

The two sub-agents are expensive and their prompts are long. Everything that can fail cheaply must fail
**here**, not inside a sub-agent that has already burned a context.

```bash
REPO="$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "NOT A GIT REPO - stop"; exit 1; }
FIXED="${1:?usage: review-since <fixed-point>}"
echo "repo        : $REPO"
# 1. the fixed point must resolve to exactly one commit
git rev-parse --verify --quiet "$FIXED^{commit}" >/dev/null \
  || { echo "BAD REF: '$FIXED' does not resolve to a commit - stop, ask the user"; exit 1; }
echo "fixed point : $(git rev-parse --short "$FIXED^{commit}")"
echo "head        : $(git rev-parse --short HEAD)"
# 2. the diff must be non-empty, and captured ONCE, with the three-dot form
git diff "$FIXED"...HEAD > .review.diff || { echo "DIFF FAILED - stop"; exit 1; }
LINES=$(wc -l < .review.diff); FILES=$(git diff --name-only "$FIXED"...HEAD | wc -l)
echo "diff        : $LINES lines across $FILES files"
[ "$FILES" -eq 0 ] && { echo "EMPTY DIFF - stop, the fixed point may be HEAD itself"; exit 1; }
# 3. the merge-base, which is what the three-dot form actually compares against
echo "merge-base  : $(git merge-base "$FIXED" HEAD | cut -c1-12)"
# 4. the commit list, captured for both prompts
git log "$FIXED"..HEAD --oneline > .review.commits
echo "commits     : $(wc -l < .review.commits)"
cat .review.commits
# 5. and the mechanical checks, which must NOT reach a sub-agent:
#    anything a tool already enforces is out of scope for both axes
git diff "$FIXED"...HEAD --name-only > .review.files
echo
echo "PREFLIGHT RESULT: $( [ -s .review.diff ] && echo READY || echo STOP )"
```

**Every failure that is cheap to detect must be detected here.** A bad ref discovered inside a parallel
sub-agent wastes both contexts and produces two confident reports about nothing.

## 7. THE SPEC GATE — DECIDE THE AXIS COUNT

The Spec axis cannot run without a spec. Decide that **before** spawning, and record the decision, because
a silently-skipped axis reads in the final report exactly like an axis that passed.

```bash
# the spec, in the documented order of preference
SPEC=""
# 1. an issue reference in the commit messages
REFS=$(grep -oiE '(closes|fixes|resolves|refs|see) +[#!][0-9]+|#[0-9]+|![0-9]+' .review.commits | tr -d '\n' | tr -s ' ')
echo "issue refs in commits: ${REFS:-<none>}"
# 2. a path the user supplied
[ -n "$2" ] && [ -e "$2" ] && SPEC="$2"
# 3. a spec file matching the branch or the feature
BR="$(git rev-parse --abbrev-ref HEAD)"
if [ -z "$SPEC" ]; then
  SPEC=$(ls -1 docs/*.md specs/*.md .scratch/*.md 2>/dev/null | grep -i -e "$BR" -e "$(basename "$BR")" | head -1)
fi
echo "spec        : ${SPEC:-<NOT FOUND>}"
if [ -z "$SPEC" ] && [ -z "$REFS" ]; then
  echo
  echo "SPEC GATE: no spec and no issue reference found."
  echo "  ASK THE USER for the spec path. If they say there is none:"
  echo "  - run the STANDARDS axis ONLY"
  echo "  - the final report MUST state 'Spec axis: not run - no spec available'"
  echo "  - an absent Spec section and a passing Spec axis must never look the same"
  exit 2
fi
echo "SPEC GATE: $( [ -n "$SPEC" ] && echo "local spec found" || echo "issue reference - fetch via docs/agents/issue-tracker.md" )"
```

**A skipped axis and a passed axis must be distinguishable in the output.** This is the failure mode that
makes a two-axis review silently useless, and the gate is the remedy.

## 8. EXECUTION PRIMITIVES

Both axes are proven by **a finding that cites a concrete line of the diff and a concrete rule or spec
line, with the mechanical checks excluded**. Every block ends at a quoted, located finding.

### 8.1 The diff bundle, which both sub-agents receive

```bash
# build ONE bundle and hand the same bytes to both sub-agents, so they review the same change
python3 - <<'PY'
import subprocess, os, json
def sh(*a): return subprocess.run(a, capture_output=True, text=True).stdout

FIXED = open(".review.fixed").read().strip() if os.path.exists(".review.fixed") else "HEAD~1"
files = [f for f in sh("git","diff","--name-only",f"{FIXED}...HEAD").splitlines() if f]
print("=== COMMITS ===")
print(sh("git","log",f"{FIXED}..HEAD","--oneline").strip() or "<none>")
print()
print("=== FILES CHANGED ===")
for f in files: print(" ", f)
print()
print("=== PER-FILE SUMMARY (the size of each hunk set) ===")
stat = sh("git","diff","--stat",f"{FIXED}...HEAD")
print(stat)
# the diff itself, chunked to a budget so a huge change does not silently truncate
full = sh("git","diff",f"{FIXED}...HEAD")
BUDGET = 60000
print()
print(f"=== DIFF ({len(full)} chars) ===")
if len(full) > BUDGET:
    print(f"[TRUNCATED to {BUDGET} chars - the review must state this, and the axis briefs get the")
    print(" file list plus this chunked view, never a silent truncation]")
    print(full[:BUDGET])
else:
    print(full)
open(".review.bundle.md","w").write(full)
PY
wc -c .review.bundle.md
echo "-> hand .review.bundle.md to BOTH sub-agents, plus each axis's own extra input"
```

**One bundle, two consumers.** If the two axes see different bytes they will disagree about the facts, and
the aggregation step cannot reconcile that.

### 8.2 The mechanical checks, which are excluded from both axes

```bash
# tooling already enforces these. Reviewing them by hand duplicates the tool and dilutes the report.
echo "=== run the repo's own tooling FIRST, and record its output ==="
for CMD in "npm run lint" "npm run typecheck" "npx tsc --noEmit" "cargo clippy" "gofmt -l ." \
           "ruff check ." "mypy ." "eslint ." "rubocop" "shellcheck" "$( [ -f Makefile ] && echo 'make lint' )"; do
  [ -z "$CMD" ] && continue
  if command -v "${CMD%% *}" >/dev/null 2>&1; then
    printf '%-24s ' "$CMD"
    OUT=$(eval "$CMD" 2>&1 | tail -5)
    echo "$([ -n "$OUT" ] && echo "see below" || echo "clean")"
    [ -n "$OUT" ] && echo "$OUT" | sed 's/^/    /'
  fi
done
echo
echo "TOOLING OUTPUT GOES IN AN APPENDIX, NOT IN EITHER AXIS."
echo "Both axis briefs carry: 'Skip anything tooling already enforces.'"
echo
echo "the list of what is EXCLUDED because tooling enforces it:"
for R in "formatting and whitespace" "import ordering" "unused variables and imports" \
         "type errors" "linter rule violations" "test failures" "lockfile drift" \
         "generated-file divergence" "spelling in code identifiers"; do
  echo "  - $R"
done
```

**Tooling output is an appendix, not a finding.** Both axis briefs must carry the exclusion, or the two
reports become a worse linter output.

### 8.3 The Standards axis, with the smell baseline pasted in

```python
# the Standards brief, assembled programmatically so the baseline is never forgotten
import os
SMELLS = [
 "Mysterious Name", "Duplicated Code", "Feature Envy", "Data Clumps", "Primitive Obsession",
 "Repeated Switches", "Shotgun Surgery", "Divergent Change", "Speculative Generality",
 "Message Chains", "Middle Man", "Refused Bequest",
]
standards_files = []
for c in ["CODING_STANDARDS.md","CONTRIBUTING.md","STYLE.md","docs/standards.md",
          "docs/architecture.md","AGENTS.md","CLAUDE.md"]:
    if os.path.exists(c): standards_files.append(c)

brief = f"""You are the STANDARDS axis of a two-axis code review. Do not review the spec.

INPUT
- The diff bundle at .review.bundle.md (the ONLY change under review).
- The repo's documented standards, read from: {standards_files or 'NONE FOUND - use the baseline only'}.
- The repo standard OVERRIDES the baseline below.

THE SMELL BASELINE (Fowler, _Refactoring_ ch.3) - all {len(SMELLS)} apply:
{chr(10).join('  - ' + s for s in SMELLS)}

REPORT, per file/hunk where relevant:
(a) every place the diff violates a DOCUMENTED standard - cite the standard (file + the rule);
(b) any baseline smell you spot - name it and quote the hunk.

RULES
- Documented-standard breaches may be HARD violations. Baseline smells are ALWAYS judgement calls:
  label them "possible Feature Envy", never "violates".
- SKIP anything tooling already enforces: formatting, import order, unused vars/imports, type errors,
  lint rules, test failures, lockfile drift, generated-file divergence.
- Never invent a standard. If you cannot cite a file and a rule, it is a baseline smell, not a
  standard breach.
- If the diff is truncated in the bundle, say so and scope your report to what you received.

Under 400 words."""
open(".review.standards.brief.md","w").write(brief)
print(brief[:900]); print("...")
print()
print("standards sources found:", standards_files or "NONE")
```

**The baseline is pasted in full, every time.** A sub-agent has no other access to it, and a forgotten smell
list produces a report that reviews only the documented standards.

### 8.4 The Spec axis, with the requirement table

```python
# the Spec brief: every requirement becomes a row, and every row gets a verdict with a quoted line
import os
spec_path = os.environ.get("SPEC_PATH", "")
spec_text = open(spec_path).read() if spec_path and os.path.exists(spec_path) else ""
brief = f"""You are the SPEC axis of a two-axis code review. Do not review the code's style.

INPUT
- The diff bundle at .review.bundle.md (the ONLY change under review).
- The spec: {spec_path or 'see the contents below'}.

THE SPEC
{spec_text[:20000] if spec_text else '<fetch via docs/agents/issue-tracker.md and paste here>'}

FIRST, extract every requirement into a table:
| # | requirement (quote the spec line) | asked-for behaviour |

THEN, for every requirement, give one verdict:
| # | verdict | evidence (quote the diff hunk, or 'no hunk found') |
    verdict is one of: MET / PARTIAL / MISSING / WRONG / SCOPE-CREEP-ADJACENT

FINALLY, report these three lists explicitly:
(a) requirements the spec asked for that are MISSING or PARTIAL;
(b) behaviour in the diff that was NOT asked for (scope creep);
(c) requirements that look implemented but where the implementation looks WRONG.

RULES
- Quote the spec line for every finding. A finding with no quoted spec line is not a finding.
- Quote the diff hunk for every verdict. "MISSING" must be backed by a search, not by a guess.
- If the spec is absent or unreadable, output exactly: "no spec available" and stop.

Under 400 words."""
open(".review.spec.brief.md","w").write(brief)
print(brief[:700]); print("...")
```

**The requirement table is the discipline.** A verdict without a quoted diff hunk is a guess, and "MISSING"
must be backed by an actual search of the change.

### 8.5 The aggregation, which must not rerank

```python
# aggregate the two reports WITHOUT merging them. The separation is the point of the skill.
import os, re
standards = open(".review.standards.out.md").read() if os.path.exists(".review.standards.out.md") else ""
spec      = open(".review.spec.out.md").read()      if os.path.exists(".review.spec.out.md")      else ""
spec_ran  = bool(spec.strip()) and "no spec available" not in spec.lower()

def count(t):
    # findings are the bolded smell names or the table rows - count what is actually enumerated
    return len(re.findall(r'(?m)^\| *(?:possible )?[A-Z]', t)) + len(re.findall(r'\*\*[A-Z][^*]{3,40}\*\*', t))

out = []
out.append("## Standards")
out.append(standards.strip() or "<the Standards sub-agent returned nothing - report this, do not invent>")
out.append("")
out.append("## Spec")
out.append(spec.strip() if spec_ran else "**Spec axis: NOT RUN — no spec available.**")
out.append("")
out.append("## Summary")
out.append(f"- Standards: {count(standards)} findings")
out.append(f"- Spec: {'%d findings' % count(spec) if spec_ran else 'not run (no spec available)'}")
worst = re.search(r'(?im)^\*{0,2}worst\*{0,2}[:\s]+(.+)$', standards)
out.append(f"- Worst on Standards: {worst.group(1).strip() if worst else '<none stated>'}")
if spec_ran:
    w2 = re.search(r'(?im)^\*{0,2}worst\*{0,2}[:\s]+(.+)$', spec)
    out.append(f"- Worst on Spec: {w2.group(1).strip() if w2 else '<none stated>'}")
out.append("- **Deliberately no single winner across axes** — one axis must never mask the other.")
open(".review.report.md","w").write("\n".join(out))
print("\n".join(out))
print()
print("RULES for this step:")
for r in ["present both axes VERBATIM or lightly cleaned - do NOT merge them",
          "do NOT rerank findings across axes",
          "a skipped Spec axis MUST be labelled 'not run', never left as an empty section",
          "state the totals per axis, and the worst issue WITHIN each axis",
          "if a sub-agent returned nothing, say so - never fill the gap yourself"]:
    print("  -", r)
```

**The two axes are published side by side, never merged.** A skipped axis is labelled `not run` — an empty
section and a passing axis must never look the same.

### 8.6 The end-to-end harness

```bash
python3 - <<'PY'
import subprocess, os, re
def sh(*a): return subprocess.run(a, capture_output=True, text=True).stdout.strip()

print("=== STEP 1: PREFLIGHT ===")
fixed = os.environ.get("FIXED", "HEAD~1")
ok = sh("git","rev-parse","--verify","--quiet",f"{fixed}^{{commit}}")
print("  fixed point resolves:", bool(ok), ok[:12] or "(BAD REF - STOP)")
files = [f for f in sh("git","diff","--name-only",f"{fixed}...HEAD").splitlines() if f]
print("  files changed       :", len(files))
print("  empty diff          :", "YES - STOP" if not files else "no")

print()
print("=== STEP 2: SPEC GATE ===")
commits = sh("git","log",f"{fixed}..HEAD","--oneline")
refs = re.findall(r'(?:closes|fixes|refs|see) +[#!]\d+|#\d+|!\d+', commits, re.I)
spec = os.environ.get("SPEC_PATH","")
print("  issue refs in commits:", refs or "<none>")
print("  spec path supplied   :", spec or "<none>")
print("  spec gate            :", "Spec axis RUNS" if (refs or spec) else
      "ASK USER; if none, run STANDARDS ONLY and label the Spec axis 'not run'")

print()
print("=== STEP 3: MECHANICAL CHECKS (appendix, excluded from both axes) ===")
for c in ["npm run lint","npx tsc --noEmit","ruff check .","cargo clippy"]:
    if os.path.exists("package.json") and c.startswith(("npm","npx")): print("  would run:", c)
    elif os.path.exists("pyproject.toml") and c.startswith("ruff"):   print("  would run:", c)
    elif os.path.exists("Cargo.toml") and c.startswith("cargo"):      print("  would run:", c)
print("  -> their output belongs in an APPENDIX, and both briefs say 'skip what tooling enforces'")

print()
print("=== STEP 4: THE TWO AXES (parallel) ===")
print("  Standards brief:", os.path.exists(".review.standards.brief.md"))
print("  Spec brief     :", os.path.exists(".review.spec.brief.md"))
print("  both receive   : .review.bundle.md (the SAME bytes)")

print()
print("=== STEP 5: AGGREGATION ===")
print("  ## Standards ; ## Spec ; ## Summary - published side by side, NEVER merged")
print("  a skipped axis is labelled 'not run', never left empty")
print()
print("REPORT = quoted diff hunks + cited rules/spec lines, per axis, with the totals stated separately.")
print("         Tooling output stays in the appendix. No cross-axis winner.")
PY
```

**Preflight, the spec gate, the mechanical exclusion, two parallel axes, and an unmerged aggregation.**
This is the whole skill in one runnable sequence.

---

## 9. CONFIRMING THE FINDING
A code review's output is **an argument about a specific line**, and the line is only half of it — the
other half is the **reachability** that makes the line matter. This table is the gate.

| Step | Question | What it proves |
|---|---|---|
| 1 | Is the **exact file and line** cited, quoted, and still present in the reviewed revision? | a claim against a moving tree is unreviewable |
| 2 | Is the **input that reaches it** identified, with the path from an entry point? | a flaw with no reachable input is a style note |
| 3 | Is there a **guard elsewhere** that already prevents it, and was it checked? | the commonest false positive is a check three call-frames up |
| 4 | Was the **control** run: the same code with the fix applied, behaving correctly? | the difference attributable to the line is the finding |
| 5 | Is the **review revision pinned** (a commit, not a branch name)? | a branch moves and the finding evaporates |
| 6 | Is the mechanism named, not the symptom: which invariant the code violates? | "unsafe" is not reviewable; "the length is checked before, not after, the copy" is |
| 7 | Is the impact stated at the step **demonstrated by reading**, not by assuming an exploit? | a code review does not demonstrate execution |

**A quoted line at a pinned revision, a reachable input path, a checked-for guard, and a fixed-code
control.** "This looks vulnerable" is a hypothesis; the reachability argument is the finding.

---

---

## 10. EVIDENCE STANDARD — REVIEW ARTEFACTS

| Item | Why |
|---|---|
| The **fixed point**, resolved to a commit SHA | the review is only defined against a pinned point |
| The **diff command**, in the three-dot form, and the **merge-base** | the three-dot form compares against the merge-base, and the reviewer must know which |
| The **file list and the commit list** | scopes both axes to the same change |
| The **spec path or issue reference**, or an explicit "none" | decides whether the Spec axis ran |
| The **standards files found**, by path | a standard breach must cite a file and a rule |
| The **tooling output**, in an appendix, with the commands run | shows what was excluded and why |
| Every finding **with its quoted hunk or quoted spec line** | a finding without a quote is not a finding |
| The **hard/possible distinction** on every Standards finding | documented breaches may be hard; smells are always judgement calls |
| The **totals per axis**, and the worst issue within each | the summary the skill promises |
| An explicit note if **either sub-agent returned nothing** | never fill the gap; report it |

Report the **findings and the boundary**: "the review is of `git diff v2.4.0...HEAD`, whose merge-base is
`a91f3c2`, across 7 commits and 14 files. The Standards axis cites `CONTRIBUTING.md` rule 'no direct
database access from handlers' for the breach in `handlers/orders.py`, and raises three judgement calls
under the baseline - possible Duplicated Code across `orders.py` and `refunds.py`, possible Primitive
Obsession on the `status` string, and possible Speculative Generality on the unused `dry_run` parameter.
The Spec axis extracted 9 requirements from `docs/specs/orders-v2.md`; 6 are MET, 2 PARTIAL, and 1
MISSING with no matching hunk found after searching the full diff for the `idempotency_key` field the spec
requires in the POST body. Both axes reported 4 and 3 findings respectively, and no cross-axis winner is
stated. The tooling appendix shows `ruff check .` clean and `mypy .` reporting 2 errors, which are
excluded from both axes by design", never "the code review found some issues".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| A **formatting, import-order, or lint** difference | tooling enforces it; it belongs in the appendix |
| A **type error or a failing test** | tooling enforces it |
| A **lockfile or generated-file** divergence | tooling enforces it |
| A smell reported as a **hard violation** | baseline smells are always judgement calls; label them "possible" |
| A finding with **no quoted hunk** | not a finding |
| A Spec finding with **no quoted spec line** | not a finding |
| A "**MISSING**" verdict with no search of the diff | a guess; back it with a search or drop it |
| A finding **outside the diff** | the review is scoped to the change, not the whole repository |
| A finding on a **file the diff did not touch** | out of scope |
| A finding **a documented repo standard endorses** | the repo overrides the baseline; suppress it |
| A **passed Spec axis** and a **skipped Spec axis** that look identical | an unlabelled skip is the worst outcome this skill can produce |

**A quoted hunk or spec line, inside the diff, with the mechanical layer excluded.** Unquoted findings and
an unlabelled skipped axis are what make a two-axis review unusable.

---

## 11. REMEDIATION REFERENCE — REVIEW PROCESS HARDENING

1. **Pin the fixed point to a resolved commit SHA and record the merge-base you actually compared against** - an unresolved ref or a silently empty diff invalidates the entire review.
2. **Run every cheap check before spawning a sub-agent, and never let a sub-agent discover a bad ref or an empty diff** - an early failure inside a parallel agent wastes both contexts.
3. **Decide the axis count explicitly: if there is no spec, run Standards alone and label the Spec axis "not run"** - a silently skipped axis is indistinguishable from a passing one.
4. **Hand both axes the identical diff bytes, from one bundle, and state any truncation in the briefs** - two axes reasoning about different bytes cannot be reconciled.
5. **Paste the smell baseline into the Standards brief every time, because the sub-agent has no other access to it** - a forgotten baseline degrades the axis to a linter.
6. **Carry the "skip what tooling enforces" exclusion into both briefs, and put the tooling output in an appendix** - otherwise the review duplicates the tooling and dilutes the findings.
7. **Require a quoted hunk for every Standards finding and a quoted spec line for every Spec finding** - the quote is what separates a finding from an opinion.
8. **Label every baseline smell as "possible" and reserve hard violations for documented-standard breaches** - the distinction is what makes the report actionable rather than noisy.
9. **Publish the two axes side by side and never rerank across them** - the separation exists so one axis cannot mask the other.
10. **State the totals per axis and the worst issue within each, and state nothing across axes** - the cross-axis ranking is the specific outcome the design prevents.
11. **Report a sub-agent that returned nothing as having returned nothing** - filling the gap yourself converts a failed review into a confident fiction.

---

## 12. RELATED SIBLINGS - LOAD TOGETHER

- [review-changes](../implement/SKILL.md) - the implementation flow this review closes
- [to-spec](../to-spec/SKILL.md) - the spec source the Spec axis consumes
- [to-tickets](../to-tickets/SKILL.md) - the originating issue the spec is derived from
- [diagnosing-bugs](../diagnosing-bugs/SKILL.md) - the sibling flow when the review finds a defect
- [writing-for-agents](../writing-for-agents/SKILL.md) - the brief-writing discipline both axis prompts need
