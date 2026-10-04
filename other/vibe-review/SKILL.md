---
name: vibe-review
description: >
  Evidence-based code review skill — mandatory gate after every phase completes.
  Triggers on "review:" prefix, "review the code", "code review", "audit the codebase",
  "check code quality", "review phase N", "is the code ready", "quality check".
  Mandatory gate: Phase N cannot proceed to Phase N+1 until review passes with 0 P0 and 0 P1.
  Final phase review blocks deploy on the same bar (0 P0, 0 P1).
  Acts as Senior Engineer, Architect, and Code Quality Auditor.
  Gracefully handles missing ARCHITECTURE.md — reviews against PLAN.md patterns instead.
  Automated checks adapt to project stack (not npm-only).
  Every finding backed by file path and line number. No vague feedback.
---

# Vibe Review Skill

Mandatory quality gate after every phase.
Acts as **Senior Engineer, Architect, and Code Quality Auditor**.
Evidence-based. Every finding backed by file path and line number.

**Never writes feature or source code.** Review is read-only on the codebase; the only
files it writes are its own artifacts — the report in `vibe/reviews/`, `backlog.md`, the
gate lines and RFX tasks in `vibe/TASKS.md`, and `vibe/.gates.json`.

**Never fix what you find — not even a one-line P1.** Every P0/P1 becomes an `RFX-NNN`
task under the phase's gate line, and the gate is recorded with the counts you found
(so it is `open`). The fix happens in the build's fix loop (vibe-mode
`AUTONOMOUS_EXECUTION_BLOCK.md`), and a fresh review then decides whether the gate
passes. Fixing inside the review and marking the gate passed skips the evidence the
gate exists to produce: the fix is never reviewed by anyone but its author.

---

## The O'Reilly principle this enforces

Issues caught at Phase 1: cheap — fix once, never propagates.
Issues caught at Phase 3: expensive — retrofit across every feature.
Issues caught at deploy: very expensive — production risk.

Without a review gate, bad patterns from Phase 1 get copied into every feature.
Architecture drifts silently. Duplication builds. Quality degrades.

---

## The reviewer's stance — falsify, don't bless

A review is not a request for approval. Do not ask "is this code good?" — that
question is answered "yes" by default and finds nothing. Ask the opposite, of
every change under review:

> **"Prove this is unsafe, incorrect, or unnecessarily complex."**

You are trying to *break* the change, not confirm it. For each significant unit,
actively attempt to construct:

- **An input that makes it wrong** — an edge case, empty/null, boundary, unicode,
  concurrency, an unexpected ordering — that produces a wrong result or a crash.
- **A failure it does not handle** — the network call that times out, the promise
  that rejects, the file that is missing, the permission that is denied.
- **A simpler version that does the same job** — if you can write it in fewer
  moving parts, the current form is unnecessarily complex (a real P2/P1).
- **A security hole** — untrusted input reaching a sink, a secret in scope, a
  missing authz check, an injection path.

A finding is only worth reporting if you can state the concrete scenario that
triggers it (inputs/state → wrong output/crash). "This looks fragile" is not a
finding; "with an empty `items` array this throws at line 42" is. This falsifying
stance is what a *second-opinion* reviewer must adopt above all — its value is in
disagreeing with the first pass, not echoing it.

If, after genuinely trying, you cannot break a unit, say so plainly and move on —
an honest "I could not find a way to make this fail" is a real result. Do not
manufacture findings to look thorough.

---

## When this skill runs

**Mandatory — phase gates:**
```
Phase 1 complete → review: phase 1 → gate passed? → Phase 2 begins
Phase 2 complete → review: phase 2 → gate passed? → Phase 3 begins
Final phase      → review: final  → gate passed? → deploy unlocked
```

**On demand:**
```
review: phase 2 invoice management
review: audit the Supabase integration
review: full codebase before new team member
```

**Gate rules:**
- **P0 AND P1 → block progression.** Both must be zero for a phase gate to pass; fix
  them (rework tasks) before the next phase begins. A P1 is never deferred past the
  phase that introduced it — "0 open P0/P1" is the bar at *every* phase gate, not only
  the final one.
- P2 / P3 → logged to backlog.md, carried to the final cleanup pass (do not block).
- Final phase: 0 P0 AND 0 P1 (same bar, plus P2/P3 addressed or explicitly accepted).
- Gate passes **only** at 0 open P0 and 0 open P1 → next phase begins.

---

## Documents this skill reads

Read in this order. Note if any are missing.

1. `vibe/ARCHITECTURE.md` — primary reference for drift detection
2. `vibe/CODEBASE.md` — exact file paths as-built
3. `vibe/SPEC.md` — acceptance criteria to verify against
4. `vibe/DECISIONS.md` — past spec/scope decisions, context for why things are as they are
5. `vibe/IMPLEMENTATION_LOG.md` *(if exists)* — implementation decisions (why-this-approach / why-this-library); the "why" behind the code
6. `vibe/PLAN.md` — phase scope, what was meant to be built
7. `vibe/TASKS.md` — what tasks completed this phase
8. `vibe/reviews/` — all previous review files for carryover tracking
9. `BRIEF.md` *(if exists)* — original intent and core value
10. `CLAUDE.md` — boundaries and conventions

**If vibe/ARCHITECTURE.md does not exist:**
> Flag this as a finding in the report: "ARCHITECTURE.md not found — no explicit architecture
> decisions documented. Pattern compliance reviewed against PLAN.md and CODEBASE.md instead."
> Use PLAN.md folder structure, tech stack, and conventions as the reference baseline.
> Recommend running `architect:` to formalise decisions. This is a P1 finding.

---

## Step 0A — Concept boundary pre-screening (graph-assisted)

**Check for dependency graph before reading any source files:**
```bash
ls vibe/graph/CONCEPT_GRAPH.json 2>/dev/null && echo "GRAPH EXISTS" || echo "NO GRAPH"
```

**If graph exists — run boundary pre-screening:**

Read `vibe/graph/DEPENDENCY_GRAPH.json` and check for cross-concept imports
that violate ARCHITECTURE.md patterns:

```python
import json

dep_g = json.load(open('vibe/graph/DEPENDENCY_GRAPH.json'))
arch_violations = []

for file_path, node in dep_g.items():
    file_concept = node.get('concept', 'foundation')
    for imported in node.get('imports', []):
        imported_node = dep_g.get(imported, {})
        imported_concept = imported_node.get('concept', 'foundation')

        if file_concept != imported_concept and imported_concept != 'foundation':
            # Frontend component importing backend/agent directly → DIP violation
            if node.get('type') == 'component' and imported_node.get('type') in ['agent', 'service', 'model']:
                arch_violations.append({'file': file_path, 'imports': imported,
                    'issue': 'Frontend directly imports backend — DIP violation', 'severity': 'P1'})
            # Agent calling another agent directly (bypasses orchestrator)
            elif node.get('type') == 'agent' and imported_node.get('type') == 'agent':
                if 'base_agent' not in imported:
                    arch_violations.append({'file': file_path, 'imports': imported,
                        'issue': 'Agent directly imports agent — bypasses orchestrator', 'severity': 'P1'})

for v in arch_violations:
    print(f"{v['severity']}: {v['file']} → {v['imports']} ({v['issue']})")
```

**Flagged files** → deep review (read source, check thoroughly)
**Clean files** → standard review (check naming, size, test coverage only)

This pre-screening surfaces most P1 architectural findings before reading
a single source file. On a clean codebase: 0 violations, shallower reads.
On a drifting codebase: violations surface immediately, guide where to look.

**If no graph exists — proceed with standard full read:**
No pre-screening available. Read all files in the phase as normal.

---

## Step 0 — Run automated checks first

> **Prefer first-party review tools when available.** If the session has the
> `/code-review` and/or `/security-review` commands, run them here — they are
> deeper and produce structured findings. Fold their output into this review's
> P0-P3 findings (map their severities onto ours) rather than re-deriving
> everything by hand. The stack commands below still run (tests/lint/typecheck/
> audit are ground truth); the manual Steps 3-8 then focus on what the tools
> don't cover (architecture drift vs ARCHITECTURE.md, spec alignment). Treat the
> hand-rolled grep checks as the fallback when those tools aren't available.

Run these before reading any code. Adapt to the project stack from CODEBASE.md section 2.

**Node / npm projects:**
```bash
npm test              # Failures are P0
npx eslint . --quiet  # Errors are P0, warnings are P2
npx tsc --noEmit      # TypeScript errors are P0
npm audit             # High/critical = P0, moderate = P1
```

**Python projects:**
```bash
pytest                # Failures are P0
ruff check .          # Errors are P0
mypy .                # Type errors are P0
pip-audit             # Critical vulnerabilities are P0
```

**Flutter / Dart projects:**
```bash
flutter test          # Failures are P0
flutter analyze       # Errors are P0
dart pub audit        # Critical vulnerabilities are P0
```

**No test runner configured:**
Flag as P1: "No automated test runner configured. Tests exist but cannot be run automatically."

Include full tool output in the review report.
If a check fails with P0-level findings: document output, do not stop — continue full review.
Machines verify first, agent verifies second.

---

## Step 1 — Establish review scope

**Scoping rule:** If this phase modified more than 30 files, review feature by feature.
Generate a sub-report per feature, then synthesise into one phase report.
Do not attempt to review 30+ files in a single pass — quality degrades.

**Review focus by phase:**

Phase 1 — Foundation integrity:
Is this a solid base? Patterns, abstractions, folder structure, TypeScript setup, shared utilities.

Phase 2+ — Incremental delta + integration:
What this phase added + does it integrate cleanly? Cross-phase consistency. Emerging duplication.

Final phase — Full production readiness:
Everything. Performance, security, accessibility, error handling, bundle size. Strictest gate.

---

## Step 2 — Carryover check

Read all `vibe/reviews/phase-N-review.md` files. Read `vibe/reviews/backlog.md`.

**If no previous reviews exist** (this is Phase 1):
State: "No previous reviews — this is the first review. No carryover to check."
Skip carryover section in the report.

**If previous reviews exist:**
For each previously logged issue, check current state:
```
✅ P1-001 — [Issue] — RESOLVED
⚠️ P1-002 — [Issue] — STILL PRESENT — escalating to P0 (appeared in 2+ reviews)
❌ P1-003 — [Issue] — NOT ADDRESSED — remains P1
```

Escalation rule: unresolved P0 from previous phase → highest priority.
P1 appearing unresolved across 2+ phase reviews → escalate to P0.
P2 appearing unresolved across 3+ phase reviews → escalate to P1.

---

## Step 3 — Architecture drift detection

> 🧠 **Effort:** drift detection and the SOLID/security judgment in Steps 3-7 are
> the highest-value reasoning in a review — run the review at high/xhigh effort
> with adaptive thinking. For the final-gate review, consider claude-opus-5.

**Most important section. Check ARCHITECTURE.md (or PLAN.md if no ARCHITECTURE.md) first.**

For each documented decision, check the actual code.

Drift format:
```
🔴 ARCHITECTURE DRIFT — [Section violated]
   Decision: "[exact quote from ARCHITECTURE.md or PLAN.md]"
   Found: [file path] line [N]
          [exact violation]
   Decision origin: [architect: session / D-ID / PLAN.md]
   Impact: [what breaks or degrades]
   Fix: [specific action]
```

Check:
- Folder structure — all new files in correct folder?
- Naming conventions — files, components, hooks, utilities match exactly?
- State management — correct layer for each type of state?
- Data fetching — all calls going through the abstraction layer?
- Component patterns — functional, one per file, props typed?
- TypeScript — strict mode, no any, all params typed?
- Error handling — following the documented strategy?
- Testing — co-located files, names describe behaviour?

Any violation = P0. Architecture drift that propagates is expensive.

**Undocumented significant decisions (P2).** While reading the code, watch for choices that
clearly cleared the "meaningful" bar — a new library/dependency added, a non-obvious pattern,
a data-model or API-shape decision, or a deliberate deviation from ARCHITECTURE.md — that are
**not** recorded in `vibe/IMPLEMENTATION_LOG.md` (nor DECISIONS.md/ARCHITECTURE.md). Flag each
as a P2 finding: name the choice, the file, and why it warranted a log entry. This keeps the
"why" from silently rotting out of the record. Do not flag routine implementation — only
decisions that a future reader would need the reason for. (If IMPLEMENTATION_LOG.md is absent
entirely on a project past Phase 1, that itself is one P2 finding, not one per decision.)

---

## Step 4 — SOLID principles review

Read each source file created or modified this phase. Every violation cites file path and line.

**SRP:** Each component/hook/service has one reason to change.
- >500 lines → P1. >1000 lines → P0 CRITICAL.
- Component handling both UI AND business logic → extract hook.

**OCP:** New features added without modifying existing working code?
- Conditional chains replacing polymorphism? Flag.

**LSP:** Components/functions behave consistently across implementations?
- Hook return shapes consistent — all returning `{ data, loading, error }`?

**ISP:** Props interfaces not forcing unused props?
- Props interface >10 props (especially optional) → P1.

**DIP:** High-level components depend on abstractions, not concrete implementations?
- Direct DB client import in component → P0 CRITICAL
- Direct localStorage in component → P1

---

## Step 5 — Platform-specific review

Read `references/PLATFORM_CHECKS.md`. Apply the section matching this project's stack
(from CODEBASE.md section 2).

Platforms covered: React Web · React Native · Node/Express · Supabase · Security (universal)

---

## Step 6 — Code quality analysis

**Component size audit:** Log every component exceeding thresholds.
**Duplication analysis:** Patterns repeated across 3+ files → extract.
**TypeScript quality:** Count `any` usages — each is P0.
**Test quality:** Names describe behaviour, not implementation. AAA structure present.

---

**Performance-tagged findings (handoff to vibe-perf):** when a finding is a
performance concern (N+1 queries, unbounded lists, missing memoisation, oversized
bundles, sequential calls that could parallelise), tag it `category: performance`
in the report's structured findings and note it. This is what `vibe-perf` Entry B
triggers on — after review, if any `performance` P1/P2 findings exist, suggest
running `perf:` to audit and fix them properly. Do not attempt deep perf fixes
inside review.

---

## Step 7 — Security review

**Universal — all projects, all phases:**
```bash
# Include npm audit / pip-audit output from Step 0
```
- [ ] Hardcoded secrets, tokens, API keys → P0 CRITICAL
- [ ] `.env` in `.gitignore` → P0 if missing
- [ ] User input rendered without sanitisation (XSS) → P0
- [ ] Auth checks before protected content → P0 if missing
- [ ] Sensitive data not logged → P1
- [ ] Input validation at API boundary → P1 if missing
- [ ] Dependency vulnerabilities: high/critical = P0, moderate = P1

**Final phase review only (additional checks):**
- [ ] CORS not configured as `*` in production → P1
- [ ] Security headers (Helmet or equivalent) → P1
- [ ] Rate limiting on public endpoints → P1
- [ ] HTTPS enforced in production config
- [ ] Content Security Policy (CSP) headers set
- [ ] Session management correct
- [ ] Zero high/critical dependency vulnerabilities (must be zero before deploy)

---

## Step 8 — Testing review

- Tests present for all business logic? (missing → P1)
- Test names describe behaviour? (implementation names → P2)
- AAA structure? (missing → P2)
- Edge cases and error states covered for critical paths? (missing → P1)
- Coverage estimate >70% on business logic? (below → P1)

**Runtime evidence, not assertion (for UI / runnable changes).** Code review reads
the source; it does not prove the thing runs. Where the change touches something
observable — a screen, an endpoint, a CLI path — confirm it against the running
software, not just the diff: boot it, exercise the primary flow, and check for
console/stderr errors. A screen that renders blank, a route that 500s, or a
console error is a P0/P1 with the observed symptom as its evidence — "opened
/checkout, button click throws `undefined is not a function` in console" beats any
amount of reading. If you cannot run it in this environment, say the check was not
performed rather than implying the code was verified.

---

## Step 9 — Generate the review report

Read `references/REVIEW_REPORT.md` for the full template.

Save to `vibe/reviews/phase-[N]-review.md`.

**Quality score formula:**
- Start at 10.0
- Subtract 1.0 per P0 finding
- Subtract 0.5 per P1 finding
- Subtract 0.2 per P2 finding
- Subtract 0.1 per P3 finding
- Subtract 0.5 additional per architecture drift violation

**Evidence standard — non-negotiable:**
Every P0 and P1 must have file path + line number + specific actionable recommendation.
"Some components are too complex" — rejected, no file path.
If a finding cannot be backed by evidence — it does not go in the report.

**The machine-readable findings block is MANDATORY, not optional.** Every report must
contain the ` ```json ` structured-findings block from `references/REVIEW_REPORT.md`
(one object per finding: `id`, `severity`, `file`, `line`, `issue`, `fix`) — a prose
summary or a markdown table alone is not enough. Tooling (the gate, the panel's
findings/fix UI) parses that block; without it the findings are invisible and can't be
fixed, and the gate can't count them. A human-readable table may accompany it, never
replace it.

---

## Step 10 — Update vibe/TASKS.md

Edit the gate line **in place** under its own heading (`## Phase [N] gate`, or
`## Final gate` for `review: final`). Never add a second gate section. If the heading is
missing (older or retrofit file), add it at the end of that phase's block. See the
update rules in vibe-new-app `references/TASKS_MD.md`.

**P0 or P1 issues found — mark blocked and insert fix tasks under the gate line:**
```
## Phase [N] gate
🔴 review: phase [N] — blocked [date] · [N] P0 + [M] P1 open
   [ ] RFX-001 · [P0/P1 fix — plain English]
                 File: [path] · Issue: [one line]
   → Full report: vibe/reviews/phase-[N]-review.md
```

**Zero P0 and zero P1 — mark passed:**
```
## Phase [N] gate
✅ review: phase [N] — passed [date] · 0 P0, 0 P1 (P2/P3 to backlog)
```

On a re-review, replace the 🔴 line with the new result and leave completed `[x]`
RFX tasks beneath it as history.

---

## Step 11 — Update vibe/reviews/backlog.md

Add all P1/P2/P3 findings. Use the format in `references/REVIEW_REPORT.md`.

---

## Step 11.5 — Record the gate state (enforcement)

Read `references/GATES.md`. Write the outcome to `vibe/.gates.json` so phase
advancement and the deploy gate can *check* this review rather than trust memory —
this is what makes the gate hold in manual mode. Merge into the existing file; never
drop other phases' entries.

```bash
# Set these from the review you just completed:
#   PHASE = the phase reviewed ("1", "2", … or "final")
#   P0 / P1 = the P0 / P1 finding counts from this review
PHASE="[phase]"; P0=[p0 count]; P1=[p1 count]
python3 - "$PHASE" "$P0" "$P1" << 'PY'
import json, sys, pathlib, datetime
phase, p0, p1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
p = pathlib.Path("vibe/.gates.json")
g = json.loads(p.read_text()) if p.exists() and p.read_text().strip() else {"phases": {}}
g.setdefault("phases", {})
# One bar at every gate (phase and final): passed only at 0 P0 AND 0 P1.
status = "passed" if (p0 == 0 and p1 == 0) else "open"
entry = {"review": status, "p0": p0, "p1": p1,
         "date": datetime.date.today().isoformat(),
         "report": f"vibe/reviews/phase-{phase}-review.md"}
if phase == "final":
    g["final"] = entry
else:
    g["phases"][phase] = entry
p.write_text(json.dumps(g, indent=2) + "\n")
print(f"gate recorded: phase {phase} → {status} (P0={p0}, P1={p1})")
PY
```

If P0 > 0 **or** P1 > 0, the phase gate is **open** — the generated CLAUDE.md's
advancement rule blocks the next phase from starting until a re-review passes.

---

## Step 12 — Update vibe/ARCHITECTURE.md (if gaps found)

If review reveals a pattern being used that isn't documented:
- Add to the relevant section with `> 📝 [date] · Added during phase-[N] review`
- Log in DECISIONS.md if it changes something previously decided

---

## Step 13 — Signal done and generate hooks

**Read execution mode:**
```bash
grep "VIBE_MODE" CLAUDE.md 2>/dev/null | cut -d= -f2 | tr -d ' '
```

**Standard output (both modes):**
```
## Phase [N] Review Complete

📊 Score: [X/10] — Grade [A-F]
🏗️  Architecture drift: [N issues / none]
🔴 P0 issues: [N — fix tasks in TASKS.md / none]
🔶 P1 issues: [N — fix tasks in TASKS.md / none]
📋 Report: vibe/reviews/phase-[N]-review.md
```

**If `manual` or not set — standard gate message:**
```
Gate decision:
[✅ PASS — Phase [N+1] may begin. Say "next" to continue.]
[🔴 BLOCKED — complete RFX tasks in TASKS.md first, then say "next".]
```

**If `autonomous` — structured signal for calling skill:**

On PASS (0 P0 and 0 P1):
```
REVIEW_RESULT: PASS
P0: 0 | P1: 0 | P2: [N]
AUTONOMOUS: Phase [N] gate passed.
```
Return control to the calling skill. It decides what happens next (see
vibe-mode's AUTONOMOUS_EXECUTION_BLOCK — by default the phase ends here).

On FAIL (any P0 or P1):
```
REVIEW_RESULT: FAIL
P0: [N] | P1: [N] | P2: [N]
AUTONOMOUS: PAUSED — [N] P0 + [M] P1 issue(s) block the gate.

[List each P0/P1 with file path, line, and specific fix]

Fix the above, then say "resume" to continue autonomous execution.
```
Return this signal to the calling skill — do not wait here. The autonomous execution
block (vibe-mode `references/AUTONOMOUS_EXECUTION_BLOCK.md`) owns what happens next: it
runs the RFX fix tasks and re-runs this review, up to 2 cycles, and records a stop in
`vibe/.run_state.json` if the gate still won't clear. When review is run on its own
(not from that block), print the list above and stop; on "resume", re-run this review.

---

## Step 14 — Generate .claude/settings.json hooks (Phase 1 review only)

After the very first phase review (Phase 1), check if `.claude/settings.json`
has a PostToolUse lint hook. If not — offer to add it. (In autonomous mode, don't ask
and don't change `.claude/settings.json`: note "lint hook not installed — offer on the
next interactive review" in the review report and move on. Editing the agent's own
settings is a decision for a person.)

> "Phase 1 review complete. One quick setup: adding a lint+typecheck hook
> will catch TypeScript errors and ESLint violations as soon as they're
> introduced rather than at the next phase gate. Want me to add it? (y/n)"

If yes — **merge** the hook into `.claude/settings.json` (never overwrite it).
`.claude/settings.json` may already hold `permissions`, `env`, or other hooks
(e.g. a `PreToolUse` hook written by `vibe-doctor`). A `cat > … <<EOF` overwrite
would wipe all of that. Read-merge-write instead, and no-op if an equivalent
lint hook is already present:

```bash
# Pick the lint command for the stack (see per-stack variants below):
LINT_CMD='npm run lint --silent 2>&1 | tail -10 || true'

mkdir -p .claude
python3 - "$LINT_CMD" << 'PY'
import json, sys, pathlib
lint_cmd = sys.argv[1]
p = pathlib.Path(".claude/settings.json")
cfg = {}
if p.exists() and p.read_text().strip():
    try:
        cfg = json.loads(p.read_text())          # preserve existing config
    except json.JSONDecodeError:
        print("settings.json is not valid JSON — leaving it untouched"); sys.exit(0)
hooks = cfg.setdefault("hooks", {})
post = hooks.setdefault("PostToolUse", [])
# Skip if any PostToolUse hook already runs a lint/typecheck command.
already = any(
    "lint" in h.get("command", "") or "tsc" in h.get("command", "") or "ruff" in h.get("command", "")
    for entry in post for h in entry.get("hooks", [])
)
if not already:
    post.append({"matcher": "Edit|Write",
                 "hooks": [{"type": "command", "command": lint_cmd}]})
    p.write_text(json.dumps(cfg, indent=2) + "\n")
    print("Lint hook merged into .claude/settings.json")
else:
    print("A lint/typecheck PostToolUse hook already exists — no change")
PY
```

Set `LINT_CMD` per stack — Python: `ruff check . 2>&1 | tail -10 || true`;
TypeScript with typecheck: `npm run lint --silent 2>&1 | tail -5; npx tsc --noEmit 2>&1 | tail -5 || true`.

> Prefer the `update-config` skill if it is available in the session — it owns
> `settings.json` edits and merges hooks safely. Use the inline merge above only
> as a fallback.

Tell the user:
> "Hook added to .claude/settings.json. From now on, lint runs automatically
> after every file edit. ESLint errors surface immediately — no more discovering
> them at phase gate review."

If the merge reported that a lint/typecheck hook already exists — skip silently.
If the user says no — skip and note they can add it manually later.

---

## Always-flag anti-patterns

**P0 — Critical:**
1. Direct DB client import in component (DIP violation)
2. Component >1000 lines (SRP violation CRITICAL)
3. `any` type anywhere (TypeScript violation)
4. Hardcoded secrets/tokens/API keys (security CRITICAL)
5. Auth check missing on protected route/endpoint (security CRITICAL)
6. Architecture drift from ARCHITECTURE.md (or PLAN.md if no ARCHITECTURE.md)
7. npm/pip audit high/critical vulnerability
8. TypeScript compilation errors
9. All tests failing (if test runner exists)

**P1 — Fix before deploy:**
9. Component >500 lines (SRP violation)
10. Direct storage/localStorage without abstraction (DIP)
11. Missing error boundaries on data-fetching components
12. Hooks managing multiple unrelated concerns
13. Props interface >10 props (ISP violation)
14. console.log in production code
15. Test names describing implementation not behaviour
16. Missing tests for business logic
17. ARCHITECTURE.md not present (recommend running architect:)

---

## Pre-submission checklist

- [ ] Automated checks run — output included in report
- [ ] Every P0 and P1 has file path and line number
- [ ] Drift checked against ARCHITECTURE.md (or PLAN.md if missing) — not generic rules
- [ ] Carryover from previous reviews addressed (or stated as first review)
- [ ] Quality score calculated using the formula — not estimated
- [ ] Strengths acknowledged with file references
- [ ] RFX tasks in TASKS.md for all P0 issues
- [ ] P1/P2/P3 logged to vibe/reviews/backlog.md
- [ ] Gate decision stated clearly
- [ ] No section TBD or skipped
- [ ] Report saved to vibe/reviews/phase-[N]-review.md
