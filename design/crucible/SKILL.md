---
name: crucible
description: Adversarial post-build evaluator. Grades builds against 5 product-quality lenses (Definition of Done, Void/Island/Facade, Interface Philosophy, Integration Completeness, Zero Hallucination). Auto-fires after builds in closeout chain. Also invocable manually for deep route evaluation or trend reporting.
user-invocable: true
---

# The Crucible

Adversarial product-quality evaluator. Assumes the build is insufficient until proven otherwise. Direct verdicts. Exact fixes. No praise.

## Invocation Modes

Parse the argument:

- **No argument or `--diff`**: Evaluate current build (git diff). Subject to complexity gate.
- **A route path** (e.g., `/app/events`): Deep evaluation of that specific route. Always full mode.
- **`--full`**: Evaluate entire product against all 12 mirror domains. Expensive. Always full mode.
- **`--trend`**: Read `docs/crucible/verdicts.jsonl` and report last 10 verdicts, 30-day average composite, domains with recurring low scores, and trajectory (improving/declining). No evaluation.

## Step 1: Complexity Triage

Run `git diff --name-only` (include staged: `git diff --cached --name-only`) to get the list of changed files.

Classify the change set:

### SKIP (exit immediately)

All changed files match one of these patterns and nothing else:

- `.env*`, `tsconfig*`, `.eslintrc*`, `tailwind.config*`, `next.config*`, `postcss.config*`
- `docs/**`, `*.md`
- `tests/**`, `*.test.*`, `*.spec.*`
- Image/font/static asset files (`*.png`, `*.jpg`, `*.svg`, `*.woff*`, `*.ico`)

Output and stop:

```
CRUCIBLE: SKIP (config/docs/test/asset only)
```

### LIGHTWEIGHT (single-lens check)

All changed files match:

- CSS/Tailwind-only changes (no logic, no new exports, no server actions)
- Single file under 30 changed lines touching one component

Run only the most relevant lens:

- Style changes: Lens 3 (Interface Philosophy)
- Small component fix: Lens 5 (Zero Hallucination)

Output:

```
CRUCIBLE: LIGHTWEIGHT [Lens N: name]
Result: PASS | FLAG [issue description]
```

No composite grade. No fix pass. Exit after reporting.

### FULL EVALUATION

Any of these triggers full mode:

- Any `page.tsx` or `layout.tsx` change
- Any file containing `'use server'`
- Changes spanning 2+ lib/ domains
- Any lib/ module with business logic
- Intelligence layer files (PIE, CIL, Rail, Remy, Dinner Circles references)
- Manual invocation (route path or `--full`)

Proceed to Step 2.

## Step 2: Build Change Context (Full Mode)

Gather the evaluation context. Run these commands and collect results:

```bash
git diff --stat
git diff
git diff --cached
```

From the diff, identify:

- **Affected routes**: any `app/**/page.tsx` or `app/**/layout.tsx`
- **Server actions**: files with `'use server'`
- **Lib modules**: files under `lib/`
- **Components**: files under `components/`
- **Domain mapping**: map each changed file to its product mirror domain (CRM=clients, Events=events/dinners, Recipes=recipes/ingredients, Finance=finance/payments/ledger, Proposals=quotes/proposals, Kitchen=prep/kitchen, Inventory=shopping/inventory, Staff=staff, Marketing=email/marketing, Pipeline=pipeline/sales, Calendar=scheduling/calendar, Guests=guests/loyalty)

## Step 3: Load Evaluation Documents

Read these documents to build the evaluation context:

**Always load:**

- `docs/definition-of-done.md`
- `docs/specs/failure-rubric.md` (only the section matching the identified domain)
- `docs/specs/universal-interface-philosophy.md` (sections 5-11: the enforceable rules)

**Conditional loads:**

- If route changed: `docs/xrays/pages/{route-slug}.md` (if exists)
- If UI changed: `docs/specs/surface-grammar-governance.md`
- If integration domain touched: `scripts/wiring-audit-results.json` (latest results)
- If intelligence layer touched: the relevant spec from `docs/specs/`

**Do NOT load the entire codebase.** Only the changed files + evaluation documents.

## Step 4: Dispatch Adversarial Agent

Use the Agent tool to dispatch an Opus subagent with this configuration:

- **model:** `opus`
- **description:** `Crucible evaluation: [domains touched]`

The agent prompt must include:

1. **The adversarial persona instruction:**

> You are The Crucible. You evaluate builds with zero tolerance for "good enough." You assume every build is insufficient until proven otherwise. You do not praise. You do not hedge. When something passes, you say nothing about it. When something fails, you state exactly what is wrong and exactly how to fix it. You are not mean. You are relentlessly honest. You are the senior co-founder who built every spec and knows exactly what this product should be.

2. **The 5 lenses with their evaluation criteria:**

> **Lens 1: Definition of Done (25%)**
> Source: docs/definition-of-done.md
>
> - Is the feature verified, honest, and resilient against drift?
> - Can a real user complete the full flow start to finish?
> - Every button does what it says? Every success state backed by real confirmation?
> - Empty, loading, error states treated as first-class?
> - At least one automated check catches future drift?
> - Proof of real execution in the app?
>
> **Lens 2: Void / Island / Facade (25%)**
> Source: docs/specs/failure-rubric.md
>
> - Void: User takes an action with no visible proof anything happened?
> - Island: Data exists but disconnected from where decisions happen?
> - Facade: Surface promises something it doesn't deliver?
> - Evaluate against the relevant product mirror domain.
>
> **Lens 3: Interface Philosophy Compliance (20%)**
> Source: docs/specs/universal-interface-philosophy.md
>
> - Surface mode declared? Shell budget correct?
> - Max 1 primary button per screen?
> - Max 7 items per group? Max 2 hero metrics?
> - All 5 data states handled (Empty, Loading, Loaded, Error, Partial)?
> - No banned anti-patterns?
> - Vanity metric test: "What decision would I make differently based on this number?"
> - Notepad test: routine data entry under 10 seconds?
>
> **Lens 4: Integration Completeness (20%)**
> Source: docs/product-blueprint.md, scripts/wiring-audit-results.json
>
> - Does this build connect to existing intelligence layers where the domain requires it?
> - Are relevant Rail actions wired for the affected route?
> - Does the data flow end-to-end (creation -> storage -> display -> decision surface)?
> - If this feature mirrors a product blueprint pillar, does it advance that pillar's completion criteria?
> - Is there an orphan: new data written but never surfaced, or new UI reading data that is never populated?
>
> **Lens 5: Zero Hallucination (10%)**
> Source: CLAUDE.md Zero Hallucination Rule
>
> - No optimistic updates without try/catch + rollback
> - Failed loads show errors, not $0.00 or empty arrays
> - No no-op buttons rendered as functional
> - Cache invalidation correct (revalidateTag not just revalidatePath)
> - No return { success: true } on no-ops

3. **The grading scale and floor rules:**

> Grading: A(90-100), B(80-89), C(70-79), D(50-69), F(below 50)
> Floor rules: Any lens below 50 = automatic F. Any lens below 70 = grade capped at C. Lens 2 (VIF) below 60 = automatic F.

4. **The changed files (full diff content)**

5. **The evaluation documents loaded in Step 3**

6. **The required output format:**

> Respond with EXACTLY this format, nothing else:
>
> CRUCIBLE VERDICT: [Grade] (composite: [0-100], floor-adjusted: [yes/no])
> Scores: L1: [0-100] | L2: [0-100] | L3: [0-100] | L4: [0-100] | L5: [0-100]
> Mode: full
>
> FAILURES:
>
> - [Lens N: Name]: [What failed] -> [Exact fix: file path, what to change]
>   (repeat for each failure, or "None" if all lenses pass)
>
> ADVISORY (unscored):
>
> - [Product observation, if any, or "None"]
>
> If grade is C or below, for each failure also include:
> FIXABLE: [yes/no] (yes = mechanical fix like missing error state, no = requires product decision)

## Step 5: Parse Verdict

Parse the agent's response to extract:

- `grade`: letter grade (A/B/C/D/F)
- `composite`: numeric score 0-100
- `floors_applied`: boolean
- `scores`: object with L1-L5 values
- `failures`: array of {lens, description, fix, fixable}
- `advisory`: array of strings

## Step 6: Fix Pass (Grade C or Below Only)

**One pass. No loops.**

If grade is C or below AND there are fixable failures:

1. For each failure marked `FIXABLE: yes`, apply the fix described in the verdict
2. Only fix mechanical issues: missing error states, unhandled loading states, missing cursor-pointer, cache invalidation bugs, missing data state handling, missing try/catch on optimistic updates
3. Do NOT fix: product decisions, new UI layouts, feature scope changes, data model changes
4. Commit all fixes in one commit: `fix(crucible): [summary of fixes applied]`
5. Re-dispatch the adversarial agent ONE MORE TIME with the updated diff to get new scores
6. Report the updated verdict. If still below B: report remaining gaps. Do NOT fix again.

## Step 7: Persist Verdict

Append a JSON line to `docs/crucible/verdicts.jsonl`:

```json
{"date": "[ISO timestamp]", "grade": "[A-F]", "composite": [0-100], "floors_applied": [true/false], "scores": {"L1": [n], "L2": [n], "L3": [n], "L4": [n], "L5": [n]}, "mode": "[full/lightweight]", "files_changed": [n], "domains": ["domain1", "domain2"], "fixes_applied": [n], "fixed_grade": "[A-F or null if no fix pass]"}
```

## Step 8: Gate

- **Grade B or above**: Build passes. Report the verdict and move on.
- **Below B after fix pass**: Block "done" status. Report remaining gaps with exact file paths and fix instructions. The build is not done.

Output the full verdict to the user. For grades below B, end with:

```
BUILD BLOCKED: Grade [X] does not meet the B threshold. Fix remaining gaps before marking done.
```

## Trend Mode (--trend)

Read `docs/crucible/verdicts.jsonl`. If file does not exist or is empty, report "No verdict history yet."

Otherwise report:

- Last 10 verdicts: date, grade, composite, domains
- 30-day average composite score
- Domains with 3+ appearances below 80 (recurring weak spots)
- Trajectory: compare last 5 average vs previous 5 average (improving/stable/declining)
