---
name: app-release-qa
description: >
  Pass/fail structural and install-time checks on released Learn and Deliver CCZs. Use after a
  release, before Connect reads the apps.
disable-model-invocation: false
---

# App Release QA

**Run workspace:** when the dispatch carries a `run_workspace:` block, its values replace the `.env` ones this skill names — `ACE_HQ_DOMAIN` → `run_workspace.hq_domain` — and a partner workspace never falls back to `.env`. Contract: [`skills/_run-workspace.md`](../_run-workspace.md).

Structural + install-time QA on the released CCZ artifacts at the end
of Phase 3. Catches CCZ-marker drops, form-count drift vs. Nova
blueprint, XForm parse errors, and install-time runtime binding
failures at the source. No AVD, no Connect opp dependency — runs
against CommCare HQ's REST API only.

Structural QA partner for `app-release` (no LLM-as-Judge; deterministic
pass/fail on the released artifact). A `validate_app` PASS + a successful
`make_build` / `release_build` is necessary but not sufficient — none of
those verify that the **released CCZ artifact** carries the right
structural markers. For the naming history and the three incident classes
this catches, see reference.md.

## Inputs

The skill QAs any released Learn/Deliver build: this run's, or a live program's after a
re-release (`app-deploy` § Re-uploading to an existing HQ app). Each value is an explicit
argument first; inside `/ace:run` it defaults to the run's artifacts.

| Parameter | Used for | Resolver |
|---|---|---|
| `hq_domain` | the project space the apps released to | explicit `--domain`; default: `run_workspace.hq_domain`, else `ACE_HQ_DOMAIN` env (`connect-ace-prod`) |
| `learn_app_id` / `deliver_app_id` | HQ app ids (Learn + Deliver; either or both) | explicit `--learn-app-id` / `--deliver-app-id`; default: Phase 3 § Step 2 `3-commcare/app-deploy_summary.md` |
| released `build_id` per app | the build to QA | explicit `--learn-build-id` / `--deliver-build-id`; default: Phase 3 § Step 2.7 `3-commcare/app-release_summary.md`; else the app's latest released build (`commcare_list_apps` / the HQ application API) |
| `nova_app_id` per app (optional) | Blueprint structure (modules, forms, fields per form, Connect marker presence) — the canonical structural truth for cross-reference, read live with `get_app({app_id})` | explicit argument; default: the deploy summary's `nova_app_id`. Absent for a non-Nova app: the blueprint cross-checks record `unavailable`, never pass |
| programme rules | Payable-visit rules — whether camera-only photo capture is demanded (the `appearance="acquire"` check in Step 4) — and the stated per-module training durations (the `time_estimate` plausibility check in Step 4) | default: Phase 1 `1-design/idea-to-pdd.md`; outside a run: the program context doc, else `--camera-only=yes|no` (unknown ⇒ record the check `unavailable`) |
| `[FIXED]` instruments (optional) | Step 4.8 question-text + option-set diff (ace#2366) | default: the markdown the PDD cites in Phase 1 `inputs/` (via `inputs-manifest.yaml`); skipped with `not-applicable` when there is none |
| `opportunity_id` + `organization_slug` | Step 4.7 re-release invariants against an EXISTING opportunity | explicit `--opportunity-id` / `--org`; default: run_state `phases.connect-setup.products.connect.opportunity.id` |
| `form_field_rules` | Step 4.7a rule-path check | explicit `--form-field-rules=<json>` (an override); default: read live with `connect_get_verification_flags({organization_slug: <program org>, opportunity_id})` (read-only, ace#3161); else run_state `phases.connect-setup.products.connect.opportunity.verification.form_field_rules`. Only when none of the three resolves is the rule-path check UNEVALUATED, never a pass |
| `externally_written_case_values` (optional) | Step 4 check 3: case-list enum values a DECLARED out-of-form writer sets (e.g. a Phase 10 close-out bulk case update), which pass as `[INFO]` instead of `case-list-enum-drift` (ace#3220) | explicit `--externally-written=<json>` (outside a run: from the program context doc, quoting the PDD); default: the `externally_written_case_values` frontmatter of Phase 3 `3-commcare/pdd-to-deliver-app_summary.md` (written by its Step 4l sub-step 8). Absent ⇒ `[]`: nothing is excused. Never derived here from residual prose |
| `output_folder` | where the result YAML goes | default: the run's `3-commcare/`; outside a run, the program project's Drive folder |

## Existing objects

This skill reads only, but on a live program its verdict is the gate before working FLWs get a
build. **A Step 4.7 `[BLOCKER]` on a live opportunity means do NOT leave that build released.**
A disappeared or added `<deliver id>` breaks payment (the visit errors `Payment unit is not
configured`, and DeliverUnits are shared per app within the holding org, ace#573). A disappeared
Learn module caps every new worker below 100%. Re-release the previous build, or fix and
re-release, and tell the owner which opportunities were exposed and for how long.

## Products

- `3-commcare/app-release-qa_result.yaml` — structural verdict (see § Output schema below). Outside a run, the same file goes into `output_folder`.

No screenshots, no per-app summaries — the structural deltas live in
the verdict YAML.

## Process

### Step 1: Read upstream artifacts

Explicit arguments (§ Inputs) win over every read below. Run-free, only the
HQ ids and build ids are required; each other input that is absent marks its
dependent checks `unavailable` rather than halting.

- Read `3-commcare/app-deploy_summary.md` → extract Learn HQ app id + Deliver HQ app id.
- Read `3-commcare/app-release_summary.md` → extract Learn released build id + Deliver released build id.
- Read both Nova blueprints via `get_app({app_id: <nova_id>})` for cross-reference. (The Nova app ids are referenced in the deploy summary as `nova_app_id`.)
- Read `3-commcare/pdd-to-learn-app_summary.md` + `3-commcare/pdd-to-deliver-app_summary.md` → extract each app's DECLARED module names. This is the only artifact that says what the brief asked for; the Nova blueprint says what was built, and the difference is what Step 4's module-identity check exists to see. A summary that names no modules is not a halt — Step 4 records `declared_structure: unavailable` and relies on the starter-module signature alone.

Inside a run, if any of these inputs are missing, halt with a structured error
naming the missing artifact + the upstream skill that should have
produced it.

### Step 2: Download released CCZs

For each app (Learn, Deliver), call:

```
commcare_download_ccz({
  domain: <ACE_HQ_DOMAIN>,
  app_id: <hq_app_id>,
  build_id: <released_build_id>,
  include_multimedia: false,
})
```

The atom returns the CCZ as base64-encoded zip bytes inside a JSON
envelope. Decode the base64. Verify the resulting bytes start with
the zip magic `PK\x03\x04`. If not, halt with `download-failed`.

### Step 3: Parse zip + suite.xml + form XMLs

For each downloaded CCZ:

1. Read the zip into an in-memory file tree (`readCczTextFiles` in
   `lib/ccz-language-tables.ts`). If a tool needs files on disk, extract into a
   NEW, EMPTY directory per CCZ (`mktemp -d`) — never `unzip -o` into a
   directory an earlier build was extracted into. `unzip -o` deletes nothing,
   so the previous build's files survive and read as this build's: that is how
   ace#2292 reported another opportunity's language tables in a clean CCZ.
2. Read `suite.xml` from the zip root. Parse as XML.
3. For each `<menu>` / `<entry>` in suite.xml, identify the per-form
   XForm path (typically `modules-N/forms-M.xml`).
4. For each form XForm path, read + parse the XForm XML.

If any parse fails (zip malformed, suite.xml missing, XForm XML
malformed), halt with the specific class:
- `cczunzip-failed`
- `suite-xml-missing-or-malformed`
- `xform-parse-failed` (with the form path + the parser error message)

### Step 4: Structural verification per app

For each app, compute:

**Form count.** Count of XForm XMLs in the zip vs. count from Nova
`get_app` blueprint. Mismatch → halt with `form-count-mismatch`
(`expected N, got M`).

**Module identity — the starter module (dimagi-internal/ace#1787).**

> **Form count equality cannot catch this one, and that is not a near miss —
> it is structural.** Until 2026-09-27 Nova's app-creation call seeded every
> new app with a placeholder module: a top-level menu **"Survey"** holding one
> form **"Survey"** holding one text field **`question_1`** labelled "Question 1".
> (`voidcraft-labs/commcare-nova#693` retired that call; `begin_work({new_app})`
> creates no starter. The check stays: apps created before then can still carry
> the seed, and a regression would be invisible to every other gate.)
> That module is present in the released CCZ *and* in the Nova blueprint, so
> the two totals above are **equal on both sides** and the count check passes
> on a dirty app by construction. The Connect-marker checks below are keyed on
> forms that DECLARE `connect.*` blocks, and the starter form declares none,
> so it is invisible there too. **A count is blind to an extra module whose
> count matches; only a name/identity comparison can see it.**
>
> Live on `bednet-check-2-visit/20260828-0629`: the Deliver app reached
> release carrying the seed with every Phase 3 gate green. On a Deliver app
> that is worse than cosmetic — an FLW tapping that menu lands in a dead form
> that writes nothing and is not a payable unit.

Build the released module list (module name → its forms → each form's fields,
from `suite.xml` + the parsed XForms, cross-checked against the `get_app`
blueprint), read the declared module names out of
`3-commcare/pdd-to-<learn|deliver>-app_summary.md`, and **classify with
`auditReleasedModules` from `lib/starter-module.ts`** — a pure function,
unit-tested in `test/lib/starter-module.test.ts`, so the decision is not left
to prose:

```
npx tsx -e "import {auditReleasedModules} from './lib/starter-module.js'; \
  console.log(JSON.stringify(auditReleasedModules({released, declared}), null, 2))"
```

It returns a `CheckOutcome` (`lib/check-outcome.ts`), so **`status: 'unable'`
is not a pass** — narrow on `status` before reading `ok`:

| Outcome | Meaning | Do |
|---|---|---|
| `status: 'unable'` | No module list was built — the check inspected nothing | Halt. This is a caller bug, not a clean app; a released CommCare app always has modules |
| `ok: true` | Ran, found nothing | Continue |
| any finding with `tier: 'blocker'` | The seed survived, or the app carries a module the brief never declared | Halt with **`starter-module-present`**, naming every offending module and form |
| findings, all `tier: 'suspect'` | Named like the seed, content drifted | Record in the verdict and continue |

Four properties of the classifier are deliberate and must not be "simplified"
away:

- **The signature is the seeded FIELD, not the module name.** "No module named
  Survey" is defeated by one rename and false-fails a PDD that legitimately
  specifies a survey module. `question_1` / "Question 1" is a Nova placeholder;
  no PDD-derived brief names a field for its own ordinal. So the BLOCKER tier
  keys on a module holding exactly one form holding exactly one placeholder
  field, and ignores names entirely.
- **A name-only match is `suspect`, not `blocker`.** Module "Survey" → form
  "Survey" with real fields is reported for a human and does not halt. A gate
  that halts a clean run earns its own deletion.
- **A missing declared-module list SKIPS the undeclared half, it does not
  fail it.** The signature check still runs, and the verdict records
  `declared_structure: unavailable` so a clean result cannot hide a comparison
  that never happened.
- **An empty module list is `unable`, never `ok`.** "Found no starter module"
  read off a check that inspected nothing is the blind-gate class this repo has
  paid for four times (ace#1332 → #1538 → #1576 → #1634).

The halt is a BLOCKER, not a `[WARN]`: the whole finding behind ace#1787 is
that every structural gate reported green while a dead menu shipped, and a
non-blocking note reproduces exactly that. Record the classifier's output under
`starter_module` in the per-app verdict block in every branch, including
`unable`.

> **Match Connect markers by NAMESPACE, never by a `<learn:` prefix.**
> Nova emits these markers as **default-namespace** elements — there is
> no `xmlns:learn` declaration anywhere in the CCZ, so a literal
> `grep '<learn:module'` returns **0 on a perfectly clean app** and
> fires a spurious `learn-marker-missing` / `deliver-marker-missing`
> [BLOCKER] on every release. The wire format is:
>
> ```xml
> <module    xmlns="http://commcareconnect.com/data/v1/learn" id="m0_pretest">
> <assessment xmlns="http://commcareconnect.com/data/v1/learn" id="m5_posttest">
> <deliver   xmlns="http://commcareconnect.com/data/v1/learn" id="du_meeting">
> ```
>
> Match on **local name + the `http://commcareconnect.com/data/v1/learn`
> namespace URI**, which is exactly how Connect's own
> `sync_learn_modules_and_deliver_units` matches them. **Preferred:** don't
> re-grep at all — read `projected_connect_state` from
> `commcare_download_ccz`, which already matches by namespace URI and is
> the same projection Connect's sync consumes. See jjackson/ace#680.

**Learn-specific (only for the Learn app):**

- Each Nova form whose blueprint declares `connect.learn_module` MUST
  have a `module` element in the `…/data/v1/learn` namespace in its
  XForm XML (equivalently: a `learn_modules[]` entry in
  `projected_connect_state`).
- Each Nova form whose blueprint declares `connect.assessment` MUST
  have an `assessment` element in that same namespace (equivalently: an
  `assessments[]` entry).
- Per voidcraft-labs/nova-plugin#7 closure (2026-05-22): these wrappers are
  **required** for Connect's HQ→Connect sync to register learn
  modules. Their absence is a structural defect.
- **CARDINALITY, not just presence (dimagi-internal/ace#1131).** Count the
  forms whose blueprint declares `connect.assessment`. **There must be
  exactly one.** Two or more → halt with `learn-assessment-cardinality`,
  naming every form that carries the marker. Connect stores a single
  `passing_score` per `CommCareApp` and `process_assessments` sets
  `passed = score >= passing_score` for **every** submitted form block
  carrying `user_score`, with any-passed semantics on every downstream
  surface — so a second marked form (in practice the baseline pre-test,
  which has the same `user_score` + selects shape as the post-test) lets a
  worker who opened no module be recorded `passed=True`. Zero → halt too:
  a PDD-specified readiness gate with no gating instrument is not
  releasable. This check exists here because it is the only place it can
  live: `app_xml.py` does not extract assessments from the CCZ, so the
  behaviour is submission-time and marker-presence QA is blind to it —
  the blueprint is the only pre-release surface that sees the count.

Mismatch → halt with `learn-marker-missing` (with the form path +
which marker is absent). Before halting, re-check by namespace — a
prefix-grep false negative is the single most likely cause of this
halt firing on a clean build.

**`time_estimate` plausibility-as-hours (dimagi-internal/ace#1077).**
The unit of `connect.learn_module.time_estimate` is **HOURS** — resolved
against Connect source 2026-07-30: the model help_text says "Estimated
hours" (`commcare_connect/opportunity/models.py:297`), the PM dashboard
renders the raw value as `f"{value}hr"`
(`commcare_connect/opportunity/tables.py:1677-1678`), ingest is a
straight `int()` passthrough with no conversion
(`commcare_connect/opportunity/app_xml.py:107-108`), and the FLW-facing
mobile app sums the raw values into "Estimated time: %d hours"
(commcare-android `ConnectJobIntroFragment.kt:64-77`). Nova's tool-schema
description says "Estimated minutes" — stale, filed as
voidcraft-labs/nova-plugin#36 — so an architect that obeyed the schema
description ships a 20-minute module that renders as **"20 hours"** on
every FLW's onboarding screen. Marker *presence* checks cannot see this;
the VALUE must be read.

Run the pure helper over the Learn app:

```ts
import { checkLearnModuleTimeEstimates, formatTimeEstimateReport }
  from '../../lib/time-estimate-check';
const report = checkLearnModuleTimeEstimates(
  projected.learn_modules.map((m) => ({
    moduleId: m.slug,
    timeEstimate: m.time_estimate,
    budgetedMinutes: pddBudgets[m.slug],  // minutes; omit when the PDD is silent
  })),
);
```

`projected` is `projected_connect_state` from `commcare_download_ccz`
(its `learn_modules[].time_estimate` carries the CCZ marker value —
exactly what Connect's sync will store). `pddBudgets` comes from the
PDD: read each module's stated duration in MINUTES from the training
design (e.g. "Modules budgeted 10–20 minutes each"); when the PDD states
no duration for a module, omit the key and the helper falls back to
absolute plausibility bounds. The helper flags, per module:

- `missing` / `non-positive` / `non-integer` — `[BLOCKER]`.
- `minutes-not-hours` — the value tracks the module's MINUTE budget (or
  is an unbudgeted two-digit count): the ace#1077 signature. `[BLOCKER]`.
- `out-of-range` — wrong vs. the budget's hour conversion
  (`max(1, ceil(minutes/60))`): `[BLOCKER]` when >2x expected,
  `[WARN]` otherwise.

`severity: 'blocker'` → halt with `[BLOCKER]`
`learn-module-time-estimate-implausible` (include
`formatTimeEstimateReport(report)`). `[WARN]`-only → record and
continue. Record per-app (Learn only) under `time_estimates` in the
verdict: `pass | { modules_checked, violations: [...] }`.

**Every `learn_module` form reachable by every worker (dimagi-internal/ace#3036).**
Connect computes Learn completion over EVERY `learn_module` in the app. A
marked form behind a display condition the worker fails can never be
finalized, so that worker's Learn tops out below 100% and Deliver never
unlocks. Live on `kaduna-graduation/20261015-1411`: 14 marked modules, 9
gated to `kgrad_role = 'FLW'` and 5 to `'enumerator'`; an FLW finished her 9,
passed the assessment, and Connect read `modules_completed_pct: 64.3` (9/14),
`learn_complete: false`. This skill reported 31/31 green on that build,
because every check above reads the form and only `suite.xml` says who can
open it. Nova compiles a module display condition onto the suite `<menu>`
(`relevant="instance('commcaresession')/session/user/data/<prop> = '…'"`)
and a form display condition onto its `<command>`.

```ts
import { checkLearnModuleDisplayGating, formatLearnModuleDisplayGating }
  from '../../lib/learn-module-display-gating';
const gating = checkLearnModuleDisplayGating({
  suiteXml,                                   // the Learn CCZ's suite.xml (Step 3)
  learnModules: projected.learn_modules.map((m) => ({ slug: m.slug, firstSeenIn: m.first_seen_in })),
});
```

Narrow on `status` first — `unable` (no markers, no menus, or a marker's form
not found in the suite) is NOT a pass; halt and say why. A finding with
`severity: 'blocker'` (the condition reads a user property — role gating) →
halt with `[BLOCKER]` `learn-module-display-gated` (include
`formatLearnModuleDisplayGating(gating)`). `warn` findings (some other
condition) → record and continue. Record under `learn_module_display_gating`
in the Learn verdict block in every branch. Run over the kaduna CCZ above, the
helper reports 14 of 14 marked forms as blockers.

**Deliver-specific (only for the Deliver app):**

- Each Nova form whose blueprint declares `connect.deliver_unit` MUST
  have a `deliver` element in the `…/data/v1/learn` namespace
  (equivalently: a `deliver_units[]` entry in
  `projected_connect_state`).
- Each Nova form whose blueprint declares `connect.task` MUST have a
  `task` element in that same namespace (equivalently: a
  `task_units[]` entry).

Mismatch → halt with `deliver-marker-missing` (with the form path +
which marker is absent). The same namespace re-check applies before
halting.

**Case reachability, case-transaction presence, and case-list enum fidelity
(dimagi-internal/ace#977, #1688).** Three assertions over artifacts this step
already holds — the unzipped CCZ's `suite.xml`, `<lang>/app_strings.txt`, and
the form XMLs. All are pure functions (`lib/commcare-cli-validate.ts` for the
first two, `lib/ccz-enum-fidelity.ts` for the third); no live Nova build, no
device, no Connect.

1. **`findUnreachableCaseLists(suiteXml)` → `case-list-unreachable`.**
   Returns one finding per entry that configures `detail` blocks it can never
   show (a module whose only session datum is `function="uuid()"` pushes no
   entity-selection screen). A caseless survey module (no case type, no case
   datum: every Learn app) is never a finding, even though HQ emits a default
   `mN_case_short` detail for it (dimagi-internal/ace#3167). An empty result
   on a Learn app is the expected pass. **Branch on each finding's `severity` — this check
   is app-wide, not per-module (dimagi-internal/ace#1281):**

   - **`severity: 'blocker'`** → halt with `[BLOCKER]`
     `case-list-unreachable`, naming the command id (`mN-fM`), the
     `caseType`, and the inert `detail` ids. No entry anywhere in the app
     puts a selectable list on screen for that case type, so it is dead
     app-wide — the ace#977 "dead configuration authored to satisfy a
     validator" case, and Jon's 2026-07-28 invariant ("a module that declares
     a case type + case list should have some form that actually opens a
     case") is violated.
   - **`severity: 'info'`** → record `[INFO]` naming the module, its inert
     `detail` ids, and `reachableVia` (the sibling command that DOES render a
     list over the same case type), then **continue — do not halt.** The case
     type is reachable; only this module's copy of the detail is inert.

   **Why `info` and not a blocker: Nova makes the shape unavoidable.** Asked
   to remove the last case-list column from exactly this module (live, on
   spark-facilitator/20260813-2126), Nova refused, verbatim: *"Module … shows
   "community" cases but its Results screen has no visible fields. Every case
   list needs at least one visible Results field so users can tell rows apart
   and pick which case to open. Add or restore an identifying field such as
   "case_name" on Results. Nothing was changed."* Nova REQUIRES ≥1 visible
   Results column on any module declaring a case type, so the inert detail on a
   registration-only module cannot be removed producer-side. Blocking on it
   halted Phase 3 on essentially every ACE Deliver app. Do NOT "fix" an
   `[INFO]` finding by editing the app.

   **When it IS a blocker, remediation points at `pdd-to-deliver-app` Step 4d,
   not at the symptom.** That step calls `add_case_list_columns` on every
   case-CREATE module with an empty `caseListConfig` purely to clear a Nova
   `validate_app` error — so on an app with no followup form at all, ACE
   authors a list over a case type nothing ever opens. The fix is to add the
   followup form behind an entity datum (which is also what makes the case
   type payable), not to paper over the validator.

2. **`hasCaseTransaction(formXml)` → `[BLOCKER]` `case-transaction-missing`.**
   If the Nova blueprint declares ≥1 `caseWrite` / `case_property_on` binding
   on a case type, at least one form must carry a case transaction in the
   `http://commcarehq.org/case/transaction/v2` namespace. Name the case type
   and the count of declared bindings with no writer.

   **This assertion passes today** — a post-#989 released CCZ was verified on
   2026-08-14 to carry `<create>` plus 34 `<update>` properties, one per
   declared binding, no drops. It is a regression preventer, and it exists
   because the alternative — periodically re-grepping a build by hand — is what
   left ace#977 undecidable across three separate investigations for a month.

3. **`checkCczCaseListEnumFidelity({suiteXml, appStrings, forms})` →
   `[BLOCKER]` `case-list-enum-drift` (dimagi-internal/ace#1688).** For every
   id-mapping case-list column whose case property a form `select1` also
   writes, the column's `value → label` map MUST be a **subset** of that
   select's. Pure and structural over artifacts this step already holds — the
   unzipped `suite.xml`, `<lang>/app_strings.txt`, and the form XMLs. No
   device, no live Nova, no Connect.

   ```ts
   import {
     checkCczCaseListEnumFidelity,
     describeCczEnumFidelity,
   } from '../../lib/ccz-enum-fidelity';
   const res = checkCczCaseListEnumFidelity({
     suiteXml,
     appStrings,
     forms,
     // ace#3220 — see "Values set outside the forms" below. [] when undeclared.
     externallyWritten: externally_written_case_values ?? [],
   });
   ```

   Branch on `res.status` — `unable` is **not** a pass (`lib/check-outcome.ts`).
   Record its `reason` in the verdict's `checks[]` and treat the enums as
   UNEVALUATED. On `checked` + `!ok`, halt with `[BLOCKER]`
   `case-list-enum-drift` and emit `describeCczEnumFidelity(res.findings)` —
   one line per drifted value, naming both labels and the authoring form.
   On success record `columnsCompared` / `valuesCompared`, so the memo says
   what was compared rather than only that it passed.

   **Why a BLOCKER and not a warn.** On `spark-facilitator/20260820-0817` the
   `fcap_community` tile rendered `phase` and `current_step_id` through enums
   carrying an ACE-**invented** FCAP taxonomy while the meeting form offered
   Spark's real one, so stored `1` read as `1. Introduction` before the visit
   and `1. Planning` during it — off by one, on the surface the Learn app
   explicitly teaches the worker to read (`m3_start`, and quiz `q9`'s
   scored-correct answer). Both surfaces are well-formed in isolation, which is
   why nothing else catches it: this gate is the only place the two are
   compared. **Remediation points at `pdd-to-deliver-app` Step 4l**, which
   repairs the form's option labels and must also derive the case-list enum
   from that same itemset — not at the enum in front of you.

   **Subset, not equality** — a tile may legitimately label fewer values than
   the form offers (one scoped to a pilot window). Those come back as
   `res.unlabelledInCaseList`: report them, never halt on them. Demanding
   equality would fire on healthy apps, and a gate that cries wolf gets
   skipped. *Enforced:* `test/lib/ccz-enum-fidelity.test.ts` — the negative
   control is the drift above and must FAIL; the positive control is a real
   released CCZ and must pass.

   **The writer is often a hidden `calculate`, not a select** (ace#2188). An
   `entity-state-taxonomy` state (`skills/_app-component-library.md`) is one
   the worker never picks — it is computed from other answers — so pairing
   resolves the case-write bind through to the calculate that determines it and
   recovers the value set from that expression's string literals, unioned
   across every form (on the repro build `declined` is written only by
   Register and `checked` only by Follow-Up, so a per-form compare would
   false-fail both). Such a column is compared on VALUES ONLY: a calculate
   carries no labels, so a wrong LABEL on a calculate-written enum is invisible
   to this gate BY CONSTRUCTION. That is not a hole to paper over here — the
   authority for a state taxonomy's words is the PDD's
   `program_parameters.entity_state_taxonomy`, gated at build time by
   `pdd-to-deliver-app § Step 4l` / `pdd-to-deliver-app-eval §
   entity_state_fidelity`. Where the literals cannot be enumerated (a
   `concat()`, a value copied from a free-text answer) the result stays
   `unable` with a reason naming the expression — record it and treat the
   column as UNEVALUATED. `res.calculateWritten` reports the value set that was
   compared, per property, so the memo can show it.

   **Values set outside the forms are accepted only when DECLARED** (ace#3220).
   Some tile values are written by no form on purpose — connect-fi's Deliver
   app labels `stage = handed_over` "Handed over at close-out", and its PDD's
   build residual reads *"No form sets stage Handed over at close-out; every
   adult still in progress on 28 Feb 2027 needs a bulk case update"* (Phase 10
   closeout, bulk case update on HQ). The CCZ cannot tell that apart from a
   stale enum, so the declaration comes from outside it: the
   `externally_written_case_values` input (§ Inputs), each entry
   `{property, values, writer, source}`. A declared value passes and is listed
   in `res.externallyWritten` — record each as `[INFO]` with
   `describeExternallyWritten(res.externallyWritten)` (it names the writer and
   source), never as a pass-by-silence. Scope is exact: only the named values,
   only on the named property. An undeclared value no form writes still fails
   as `missing-from-form`; an entry missing its `writer` or `source` is refused
   (`res.externalDeclarationProblems`) and excuses nothing; a declared value a
   form also writes, or no tile renders, comes back in
   `res.unusedExternalDeclarations` — report it as a stale declaration. Do not
   add a declaration here to clear a BLOCKER: it is a build record, written at
   `pdd-to-deliver-app § Step 4l` sub-step 8 from a PDD statement, and a value
   with no such statement is the ace#1688 defect this gate exists for.

   **Every writer, or none** (ace#2940). Case writes are read in both shapes —
   bare `/data/case/(create|update)/<prop>` and Nova's
   `/data/__nova_operations/<op>/case/(create|update)/<prop>` — and a column's
   value set is the union of EVERY writer across every form, selects and
   calculates together. If any one writer's values cannot be read, the column
   is `unable`, never compared on the rest: comparing a partial set reports the
   missing writer's values as "never written", a false BLOCKER. Do not discount
   such a finding by hand — if one appears, the writer set is the bug.

**Why `play` cannot substitute for either.** `play verdict: 'skipped'` /
`empty-case-list` only fires when a case-list screen is actually *pushed*.
With no entity datum, `play` walks straight to form entry and returns a clean
`pass`, so the app is verified green while carrying a list no worker can reach.

**An EMPTY `<entity_id/>` / `<entity_name/>` element is NOT a defect —
read the bind** (dimagi-internal/ace#1192). In a correct released CCZ
these render as empty elements, with the value carried by a `calculate`
bind that targets them:

```xml
<deliver xmlns="http://commcareconnect.com/data/v1/learn" id="meeting_record">
  <name>Community meeting record</name>
  <entity_id/>
  <entity_name/>
</deliver>
```

Judging "empty" from element text therefore fires a false `[BLOCKER]`
on every standard ACE Deliver app. The real defect is a marker whose
`calculate` bind is **absent or empty**. Check the bind; never the
element text. This is load-bearing on the case-UPDATE path, where
`pdd-to-deliver-app`'s preload-hidden-field pattern (ace#1180) produces
precisely this shape.

**Field fidelity per form — compare field-ID SETS, not raw counts
(ace#2285).** For each form in the Nova blueprint, collect the set of
field **ids** the blueprint declares, collect the set the released form
XML carries (from `<bind nodeset>` leaf names plus the
`<input>` / `<select1>` / `<select>` / `<upload>` control refs), and
compare the two SETS. The canonical signal is the silent-omission class
("Nova declared `hh_size`, the CCZ has no such node"), and a set
difference names the missing field instead of leaving you a number to
guess at. Halt with `field-count-mismatch` (per form:
`missing from CCZ: [...]`, `unexpected in CCZ: [...]`) only when a
**named** field is absent.

**Do NOT halt on a raw count difference.** The two sides do not share a
counting basis, so a bare `expected N, got M` comparison has no
defensible zero point and it fires on structurally perfect apps.
Measured on `bednet-check-2-visit/20260908-1544`, Learn form "How This
Work Pays", which is 8 Nova `section` containers wrapping 12 labels:

| Basis | Count |
|---|---|
| Nova blueprint (`get_app`) | 20 |
| Literal control + bind elements in the released XForm | 16 |
| Bind-only | 13 |

All three describe the same correct form. A Nova `section` compiles to a
`<group>` carrying **no bind and no input**, and a `label` compiles to a
bind-less body element, so the blueprint legitimately counts rows the
XForm never emits as either. The field-ID set comparison matched 5/5
forms exactly on that same app.

Note the direction: the retired instruction hedged only on count
**inflation** ("false positives on auto-generated binds"), which is the
opposite of what actually happens on a section-using Learn app — the
literal count comes in **under** the blueprint, so the hedge did not
apply and a literal reading halted a clean app. That is the ace#1238
class (a guard predicting a failure that isn't there, deadlocking Phase
3), and section-heavy Learn apps are the *standard* ACE shape, not an
edge case.

This is the third instance of the counting-basis class — hidden leaves
(ace#1789), unlabelled and unrecursed containers
(ace#1807 / ace#2281), and this one. `countNovaVisibleFields` in
`lib/app-release-drift.ts` solves it for `app-release`'s drift check but
is basis-matched to the `--draft-only` form walk, NOT to released-CCZ
XML, so do not reach for it here. Record the counts on every basis you
computed in the verdict as context; just never gate on them.

**Geopoint bind-type fidelity (cross-cutting — Learn + Deliver).**
A `kind: geopoint` field MUST compile to an XForm bind of
`type="geopoint"`. A `type="xsd:string"` bind means the released build
is a stale / downgraded compilation, invisible to every other gate
(`validate_app`, `make_build`, the structural counts above, AND
`commcare-cli play` — the `selected-at(<gps>, 0|1|3)` calcs are
init-guarded, so they don't fire at form-init). For the failure
mechanism + reproducer, see reference.md § Geopoint bind-type fidelity.

Detect it two ways (run both; either firing is a `[BLOCKER]`):

1. **Nova cross-reference (primary).** For each form, call
   `get_form({app_id: <nova_id>, moduleUuid, formUuid})` and collect
   every field whose `kind` is `geopoint`. Nova is **uuid-addressed**
   since 2026-07-31 — no tool accepts `moduleIndex` / `formIndex` (see
   `playbook/integrations/nova-integration.md § The 2026-07-31
   uuid-addressing migration`); read `moduleUuid` / `formUuid` off the
   `get_app({app_id})` blueprint already fetched in Step 1, which prints
   `[uuid …]` on every module, form, and field. Assert the released CCZ's
   form XML has `<bind nodeset="…/<field-id>" type="geopoint">` for each.
2. **CCZ-internal fingerprint (no Nova dependency).** In each form XML,
   find every hidden `calculate` of the shape
   `selected-at(<X>, 0|1|3)` (the lat/lon/accuracy split). The referenced
   node `<X>` is a geopoint by construction; assert `<X>`'s own bind is
   `type="geopoint"`, not `xsd:string`.

Mismatch → halt with `[BLOCKER]` `geopoint-bind-downgrade`
(naming the field path + the observed bind type + "re-build & re-release
the app from the current Nova blueprint, which compiles geopoint
correctly"). Record per-app under `geopoint_binds` in the verdict.

**Camera-only photo capture (`appearance="acquire"`) — PDD-conditional
(dimagi-internal/ace#867).** When the PDD / payable-visit rules /
journeys require live-camera-only photo capture, every image `<upload>`
node in the Deliver form XML MUST carry an `appearance` attribute
containing `acquire`. Contract truth (verified 2026-07-13 against
commcare-android source: `QuestionWidget.ACQUIREFIELD = "acquire"`;
`ImageWidget` hides the CHOOSE IMAGE gallery button when the appearance
hint contains it — and verified live on connect-ace-prod app
`d36493197a2749d49335e02678eed2ff` build v4, where the flip produced
exactly `<upload ref="/data/dwelling_photo" mediatype="image/*"
appearance="acquire">`). A missing attribute when the PDD demands
camera-only means the released app permits gallery uploads — breaking
the verification story and any training material asserting camera-only
(hh-poverty-targeting/20260702-1456 shipped a deck claiming "no gallery
option, on purpose" over a widget showing CHOOSE IMAGE).

Mismatch → halt with `[BLOCKER]` `camera-only-appearance-missing`
(naming the form path + the `<upload>` ref + "apply the camera-only
appearance flip (HQ app builder or Nova) and re-release, then re-run
app-release-qa"). Record per-app under `camera_only_uploads` in the
verdict. When the PDD does NOT demand camera-only capture, skip the
check and record `camera_only_uploads: not-required-by-pdd`.

**Casedb preload on a visible question — always, the Deliver app
(dimagi-internal/ace#2006).** A per-encounter form asks a question because
the answer is specific to THIS encounter. If Nova also emits a casedb
`<setvalue event="xforms-ready">` for that same node, the worker meets the
previous encounter's answer already filled in, and a worker who taps Next
through the form re-files it verbatim — every value internally consistent,
so no constraint fires and nothing warns.

```ts
import { auditCasedbPreloads, formatPreloadAudit }
  from '../../lib/casedb-preload-audit';
const audit = auditCasedbPreloads(formXml, declaredCarryForward);
```

Any violation → halt with `[BLOCKER]` `casedb-preload-on-visible-question`,
emitting `formatPreloadAudit(...)`. Record per-app under `casedb_preloads`.

**This is not hypothetical and it is not rare.** The released Deliver CCZ of
`spark-facilitator/20260828-0703` carries one for **35 of its 36 answerable
questions** — every field except the photo upload, and including
`meeting_conducted` and `meeting_type`, the two fields Connect's payability
predicate reads. That one mechanism is the root cause of FOUR separate
BLOCKERs in that run's deep app-UX verdict, none of which named it: the
case's "last meeting" never advancing (the date preloaded, and
`last_meeting_date` is calculated from it), the geopoint self-certifying,
attendance and participation arriving pre-filled, and a not-held meeting
advancing the case. Three were investigated as independent product defects
and one was investigated three times as a case-write bug that never existed.

Note this check exists because the OPPOSITE was believed and written down:
`pdd-to-deliver-app` carried "a visible case-bound field does NOT emit a
preload either — proven against a compiled CCZ (ace#1232)". That was true
when measured and is false now. The lesson worth keeping is that a refuted
claim is not refuted forever, which is exactly why this is a check against
the artifact rather than a sentence in a skill.

**Count-bound repeat snapshots an unanswered question — always, every form of
both apps (dimagi-internal/ace#2517).** Nova compiles a root `count_bound`
repeat's count into a reserved `__nova_count_<id>` node written by ONE
`<setvalue event="xforms-ready">` and no `calculate` — by design: Nova's
compiler notes say root counts "initialize on `xforms-ready` … They do not
later track answer changes". So a count that reads a question in the same
form is read at form open, while that question is still empty: `jr:count` is
`""`, CommCare renders **zero** instances, and the worker is carried straight
past the repeat. `commcare-cli play` (Step 4.5) cannot see it — it exercises
form init, not a repeat entered after an answer.

```ts
import { auditRepeatCounts, formatRepeatCountAudit }
  from '../../lib/repeat-count-audit';
const audit = auditRepeatCounts(formXml);
```

Any violation → halt with `[BLOCKER]` `dead-repeat-count`, emitting
`formatRepeatCountAudit(audit, formPath)`. Record per-app under
`repeat_counts`. A count with a `calculate`, an `xforms-value-changed`
writer, a `jr-insert` (nested-row) snapshot, or a snapshot of a case
property / session value / constant passes — those are live or legitimate.

**Measured, not hypothetical:** the released Deliver CCZ of
`spark-facilitator/20260926-1413` (HQ app `3b7ec74d9883452a8747796e2f777262`,
build `a556b0725f4d465cbe3377fa51d6e382`) flags **5 of 5** count-bound
repeats across three forms — the meeting activities and independent-project
rows on both meeting records, and Participant Feedback's `participants`, so
every feedback round submitted with no participants. It was found by a
Phase 6 device walk; this gate moves it to Phase 3.

**Grid menu display — always, both apps (dimagi-internal/ace#1009).**
`app-hq-settings` sets `display_style = 'grid'` on every module of both
apps and then declares this skill its downstream backstop. Until ace#1009
that backstop did not exist, so the setting shipped with **zero**
verification — the "applied but never verified" shape that #867 / #971 /
#994 exist to prevent.

**Read it from the raw app doc, NOT from the CCZ and NOT from the REST
API.** Neither intuitive surface can carry the full assertion:

- `suite.xml` only carries `style="grid"` on its `<menu>` elements when
  the app-level `grid_form_menus == 'some'` (HQ's suite generator
  ignores every per-module `display_style` otherwise —
  `suite_xml/sections/menus.py:86-92`). So it reads BARE on exactly the
  half-applied app ace#1082 describes, and even on a fully-gridded app
  it cannot show `use_grid_menus`/`grid_form_menus` themselves —
  corroboration at best, never the authoritative read. (Post-#1082
  correctly-gridded CCZs DO emit `style="grid"`; the pre-#1082 claim
  here that a gridded CCZ "returns nothing" for the substring `grid`
  described builds whose `grid_form_menus` was still `'none'` — see
  dimagi-internal/ace#1246.)
- `GET /api/v0.5/application/<app_id>/` serializes only
  `['case_properties','case_type','forms','name','unique_id']` per
  module. `display_style` is absent, so this surface reads `None` for a
  module that IS grid — a false negative waiting for whoever reaches for
  the obvious API first.

(Cheap secondary signal, optional: because suite.xml is bare *exactly
when* `grid_form_menus != 'some'`, a `style="grid"` absence in the CCZ
already in hand corroborates the half-applied class with no extra HTTP
call — but the raw app doc remains the assertion surface.)

The authoritative surface is the raw app doc, which works against both
the draft app id and a released build id:

```
GET /a/<ACE_HQ_DOMAIN>/apps/source/<released_build_id>/
```

(authenticated with the `~/.ace/connect-session.json` cookie jar, same as
Step 2's download — the endpoint 401s on `ApiKey` auth). For each app,
assert **all three** grid fields (dimagi-internal/ace#1082):

- `use_grid_menus === true` — the app-ROOT menu of modules;
- `grid_form_menus === 'some'` — without it the suite generator ignores
  every per-module `display_style` (HQ
  `suite_xml/sections/menus.py:86-92`), so asserting only the per-module
  half is what let ace#1082 sit unnoticed;
- **every** entry in `modules[]` has `display_style == 'grid'`.

Any miss → halt with `[BLOCKER]` `grid-menu-display-missing` (naming the
app, the field — and for a module miss, the module index + `unique_id` —
plus the observed value and "re-run `app-hq-settings`, re-release, then
re-run app-release-qa"). Record per-app under `grid_menu_display` in the
verdict: `{ use_grid_menus, grid_form_menus, modules_checked,
modules_gridded, non_grid: [...] }`.

(Until ace#1082 the app-level flags were carried here as an INFO-only
caveat — `hh-poverty-targeting/20260728-0705` read `use_grid_menus:
False` on both apps while all 9 module menus were "grid", and
spark-facilitator/20260730-1718 additionally proved `grid_form_menus:
'none'` was rendering those module grids inert. `app-hq-settings` Step 4b
now sets both app-level flags via `commcare_set_app_menu_display`, so all
three fields are asserted as blockers.)

**`entity_id` grain — always, every released Deliver form carrying a
`deliver_unit` (dimagi-internal/ace#1285).** `entity_id` is Connect's dedup and
payment grain, and a wrong one silently UNDER-pays: on
`bednet-check-2-visit/20260814-0357` the released key was
`(FLW username, visit date, consent answer)` against a PDD mandating a
per-household business key, so an FLW who legitimately followed up 5 households
in one day accrued **1** payable unit.

Every existing gate passed it. This skill passed, `pdd-to-deliver-app-eval`
scored 9.2, and the CCZ projection reported `collision_count: 0` — of course it
did; a key that collapses five units into one has no collisions. It surfaced
only in `connect-program-setup-eval`, which runs AFTER Phase 4 has wired a
payment unit around the wrong grain, and Phase 4 cannot repair it: Connect
consumes `entity_id` from the form and has no override.

```ts
import { checkEntityIdGrain } from '../../lib/entity-id-grain';
const report = checkEntityIdGrain(formXml, declaredBusinessKeyNodes, {
  // ace#1441 — REQUIRED whenever the PDD declares a non-payable branch.
  hasNonPayableBranch,        // true when the PDD marks any submission non-payable
  payabilityDiscriminator,    // the field that discriminates (e.g. consent_confirmed)
});
```

Pass the nodes the PDD declares
(`products.pdd.program_parameters.entity_id_components`, else the nodes named
in § Deliver App Specification).

**Pass the payability inputs too, and a disclosed override is a PASS
(ace#1441).** `_app-component-library § payability-scoped-key` REQUIRES the
discriminator inside `entity_id` when a non-payable branch exists, and ace#1434
ruled that requirement wins over a PDD-pinned identity-only grain. A
discriminator is an ANSWER by construction, so without these inputs this
halt-loud gate rejects exactly the key ACE mandates — and any opportunity
declaring a non-payable branch cannot clear Phase 3. Observed on
`bednet-check-2-visit/20260814-2019`, where a correct build disclosing the
override as deviation D-9 tripped `answer-in-grain` + `no-entity-component`
with every other gate green.

With the inputs supplied, the check suppresses those two findings for the ONE
component `resolveEntityIdGrain()` mandates — never for any other answer field,
and never when the residual key is not the declared grain. A build that
deviates from a pinned grain and DISCLOSES it as a named deviation is a pass
here; an undisclosed deviation is still the builder's problem, not this gate's.

Any remaining finding is a `[BLOCKER]` `entity-id-grain`:

- `missing-declared-node` — the key omits a node the PDD names, **neither
  literally nor through the `calculate` of any node it concatenates**
  (ace#1810). A declared component reached through an INTERMEDIATE node is
  present, not missing: whenever the key term needs arithmetic — and a
  per-entity cap like `min(<x>, 3)` always does — Nova computes it in a named
  hidden node and puts that node in the `concat`. Before ace#1810 the plain
  substring test read that as absent and hard-halted Phase 3 on a build that
  obeyed the PDD (`spark-facilitator/20260828-0703`, Deliver build
  `b08533bdf26a48a295a362ff204fb88d`);
- `answer-in-grain` — a worker-chosen answer (consent, eligibility, outcome) is
  inside the dedup grain **and is not the mandated discriminator**. This is the
  ace#969 over-correction: moving a payability predicate INTO the key fixes slot
  consumption and breaks the grain. The mandated discriminator is exempt
  (ace#1441); a SECOND answer field is not;
- `no-entity-component` — fires **even with nothing declared**, because a key of
  worker + date + answers is worker-and-day scoped by construction. On a
  CONDITIONAL key — `if(<predicate>, concat(A), concat(B))`, which is what a
  PDD's non-payable branch needs when the fallback changes the IDENTITY source
  rather than just adding a suffix — this is judged **per branch, and every
  branch must pass** (ace#2417). The finding names which branch failed. The
  `if()` predicate is not a component: it selects a key, it is not part of one.
  `report.components` is the UNION across branches, which is the right list for
  the declared-node test (a declared business key legitimately appears on the
  payable branch only) and the WRONG one for entity identity — read
  `report.components` for display, never re-derive the entity test from it.
  A conditional nested inside a `concat()` is deliberately NOT decomposed: that
  is the released ace#1285 shape, and splitting it would let a clean sub-branch
  launder a worker-and-day-scoped one.

**`report.resolvedThroughIntermediate` is NOT a finding — carry it forward
(ace#1810).** Each entry names a declared component that is in the key only
through an intermediate node. Presence is all this gate can establish: an
intermediate node carrying `min(x, 3)` and one carrying an UNCLAMPED running
index produce a byte-identical composite. Copy the list into the verdict and
into `3-commcare/app-release-qa_*.md` so Phase 4's `connect-opp-setup
§ Archetypes -> longitudinal-visits` reads each entry's own bind and records
whether the PDD's clamp semantics are implemented.

`report.status === 'unable'` (no readable `entity_id`) means the check **did
not run** — NOT a pass. Render it with `formatGrainReport(report)`, record it
in the verdict's `checks[]` with its `reason`, and treat the dedup grain as
UNVERIFIED rather than clean. `report.detail` and `report.ok` are unreachable
on that branch by construction (`lib/check-outcome.ts`); if you expected the
form to set `entity_id`, the extractor is the bug.

**Payable-cap arithmetic — always, every released Deliver form whose
`entity_id` carries a clamped counter OR that computes a `payable_slot`-style
field (dimagi-internal/ace#2148, ace#2649).** The
clamped index GROUPS encounters onto CompletedWork rows; it is not what stops
an over-cap payment. With the `duplicate` flag off — always, on ACE
opportunities — Connect resets a repeat key to `pending` and auto-approves it,
so a repeat is paid again (ace#2512; `playbook/integrations/connect-api.md
§ A repeated entity_id is PAID AGAIN`). The Connect-side stop is the
`payable_slot` field plus the `form_field_rules` row Phase 4 adds on it
(`_app-component-library § payability-scoped-key`). The index arithmetic still
matters — an off-by-one there puts an in-cap and an over-cap encounter on
separate keys and makes the grouping, and every per-entity report built on it,
wrong — so the check below stays. The helper grades BOTH mechanisms and
reports which one carries the cap as `report.mechanism` (`clamped-key` or
`payable-slot`) with the slot itself in `report.payableSlot`; copy both into
the verdict, since the key alone does not bind the cap. **An UNCLAMPED key is
a correct grain** when the slot holds the cap — e.g. `concat(case_id, '-',
step, '-', step_meeting_index, '-', payable_slot)` with `payable_slot =
if(step_meeting_index <= 3, 'yes', 'no')` (`spark-facilitator/20261004-1706`,
whose PDD §14 pinned exactly that). The slot is simulated like the clamp,
because the counter's timing decides what `<= 3` means: over a
`<casedb read> + 1` counter it says `yes` to meetings 1-3; over a bare
`casedb` read it says `yes` to FOUR, the ace#2148 off-by-one in slot form.

The clamp constant and the cap are not the same number, and which way they
differ depends on **when the counter is read**. A `casedb` read is the state
BEFORE this submission, because the case property is written on submit. On
`spark-facilitator/20260906-2233` the per-step cap was 3 and the build shipped
`capped_index = if(payable_count_this_step >= 3, 3, payable_count_this_step)`
over such a read: the 4th meeting reads 3, clamps to 3, and mints an index that
has never existed — Connect creates a CompletedWork for it and pays it. 4 keys
x 7 steps = 28 against a declared `total_cap_per_flw` of 21. `validate_app`,
`compile_app` and `make_build` all passed; the CCZ was structurally perfect and
the app internally consistent with its own wrong key. Only
`pdd-to-deliver-app-eval` re-deriving the arithmetic by hand caught it.

```ts
import { checkPayableCapArithmetic, formatPayableCapReport }
  from '../../lib/payable-cap-arithmetic';
const report = checkPayableCapArithmetic(formXml, {
  // The PDD's per-entity cap, when it declares one. OMIT it and the check
  // reads the app's own `is_payable` guard instead — which is what caught
  // ace#2148, where the guard was right and the key was wrong.
  declaredCap,
});
```

**Do not adjudicate this by comparing the clamp to the cap.** Both correct
constructions are live in ACE and they share no constant: build
`b08533bdf26a48a295a362ff204fb88d` clamps `min(<casedb count> + 1, 3)`
(indices 1..3) and build `0cb63a78fd9949b696876ee7a642b685` clamps
`if(pcts >= 3, 2, pcts)` (indices 0..2). The helper SIMULATES the first
submissions and counts distinct keys; `report.indices` is that trace, and it
belongs in the verdict because it is what a reviewer can check by eye.

Any finding is a `[BLOCKER]` `payable-cap-arithmetic` — name `node`,
`capacity` vs `cap`, the `capSource`, `firstOvercapped`, and the `remedy`
expression, and route the fix to `pdd-to-deliver-app` Step 4j.6. `kind` is
`payable-cap-off-by-one` (the ace#2148 class), `payable-cap-mismatch` (the two
disagree by more than one), `payable-cap-not-expressible` (a cap below 1 is
a payability question, not a dedup one), or `payable-slot-off-by-one` /
`payable-slot-mismatch` (the `payable_slot` field Phase 4's `form_field_rules`
row approves on says `yes` to the wrong number of encounters, or to a set that
is not the first N — a finding even when a clamped key is also present and
correct, because the rule pays what the slot marks).

**The slot's name and shape vary; the helper reads both (ace#2861).** The
library calls the node `payable_slot`, but builds also ship `paid_slot` (after
a PDD's "paid-slot answer"); both are read, and when the Phase 4
`form_field_rules` row names the node, pass it as `slotNode` so any name is
read. A ONCE-ONLY cap (cap 1) is usually a history predicate rather than a
counter — `if(#participant/baseline_done = 'yes', 'no', 'yes')`, or
`if(<payable> and #participant/x_ever != 'yes', 'yes', 'no')` over a flag the
form writes back, or `if(#form/earlier_versions = 0, 'yes', 'no')` over a
casedb count. The helper grades all three as a slot admitting 1
(`report.payableSlot.shape` is `once-only-flag` for the flag form, with
`flagProperty` and `flagWrite`; copy them into the verdict).

`report.status === 'unable'` means the check **did not run** — NOT a pass.
Record it in `checks[]` with its `reason` and treat the cap as UNVERIFIED.
Exactly ONE reason is a `[BLOCKER]` on its own: *no clamped counter in
`entity_id` and no `payable_slot`-style calculate* on a form whose PDD DOES
declare a per-entity cap — the cap is enforced by NEITHER mechanism (raise it
yourself, naming the declared cap). Every other `unable` is a shape or input
the helper could not grade, and is **never mapped to a `[BLOCKER]` by
itself**: trace the slot by hand over the first `cap + 1` payable encounters,
record the trace in the verdict, and block only on what the trace shows. That
covers an unclamped key with a slot present (ace#2649), a slot shape the
helper does not recognise ("… a slot shape this check does not recognise"),
a once-only slot whose flag this form never writes back (check the other
forms — a flag nothing writes IS a missing cap, but that is a finding of the
trace, not of the `unable`), and *the counter never resolves to a casedb
read* — for the clamp, or for the slot — where the timing is undecidable;
never assume one, because a guessed timing is an off-by-one in the other
direction. Blocking on an unrecognised shape halts a correct build: on
`smallholder-seasonal/20261012-1549` 12 of 12 paid forms came back `unable`
while every once-only cap was enforced.

**Scoring arithmetic — always, every Learn form carrying item scores
(dimagi-internal/ace#1035).** CommCare has **no "mark this option correct"
primitive** — Vellum's Assessment Score mug takes a hand-written XPath
(`dimagi/Vellum@8a1ef02` `src/commcareConnect.js:180-198`), and Connect reads
`user_score` straight off the submission
(`commcare_connect/form_receiver/processor.py:230`). Nova's maintainer
confirmed that is the PLATFORM's shape, not a Nova gap (nova#372). So the score
is arithmetic the architect writes, and until this check nothing verified it:
no `-eval` grades it (they grade the app against the PDD, which carries no
per-item score expressions) and the rest of this skill is structural. The
Household Poverty Targeting Learn app spends 36+ hidden fields on scoring
alone; one omitted rollup term produces a plausible score that is quietly
wrong, and a worker's pass/fail against `passing_score` depends on it — a wrong
score gates the wrong people out of PAID WORK.

```ts
import { checkScoringArithmetic, formatScoringReport }
  from '../../lib/scoring-arithmetic';
const report = checkScoringArithmetic(formXml);
```

`report.status === 'unable'` means the check **did not run** — no bind matched
an item-score node. That is NOT a pass: record it in the verdict's `checks[]`
with its `reason` and treat the scoring as UNVERIFIED. **If the form visibly
DOES carry item scores, the `ITEM_SCORE` regex is the bug, not the form** —
that exact failure has now shipped four times (#1332 → #1538 → #1576 →
#1634), most recently sending both Learn scoring forms on
`bednet-check-2-visit/20260825-1310`, gating assessment included, down this
path while the gate reported fine. Any finding is a `[BLOCKER]`
`assessment-scoring-arithmetic`; name
the kind and the nodeset, and route the fix to `pdd-to-learn-app`. The five
mechanical classes: `missing-term` (rollup omits an item), `extra-term`
(rollup names a phantom), `denominator-mismatch` (`* 100 div N` where N is not
the item count), `self-reference-missing` (an item scores a different
question), `unreachable-max` (an item awards 0 on every branch), plus
`no-rollup`. On a form WITHOUT a Connect `<assessment>` block (an ungraded
baseline) the rollup is whatever non-item calculate sums the items — e.g.
`baseline_score` — and gets the same checks; `no-rollup` there means nothing
sums them, never "add a `user_score`", which #1131 forbids on such a form
(dimagi-internal/ace#2958).

It deliberately does NOT judge whether the correct answer is correct — that is
content, and `assessment_rule_coverage` owns it.

**Assessment retry leak — always, every Learn form carrying a score gate
(dimagi-internal/ace#1041).** A fail/retry result label must not restate the
correct answer. Run the pure helper over each form XML:

```ts
import { checkAssessmentRetryLeak, formatRetryLeakReport }
  from '../../lib/assessment-retry-leak';
const report = checkAssessmentRetryLeak(formXml);
```

`report.status === 'unable'` means the check **did not run** — the form carries
no score-gated result labels, so there was nothing to leak into. That is NOT a
pass: record it in the verdict's `checks[]` with its `reason`. If the form DOES
gate a retry message on the score, the recovery matchers are the bug. Any entry
in `report.findings` is a `[BLOCKER]` `assessment-retry-answer-leak`: name the label
nodeset and the leaked option, and route the fix to `pdd-to-learn-app` Step 4c
(replace the retry text with a pointer to the module content).

**`report.info` is `[INFO]`, never a BLOCKER** (ace#2208). It holds hits the
check cannot stand behind as a leak: an answer token of ≤ 4 letters (`No.`,
Tumbuka `Yayi.` — also an ordinary clause-final negator in Bantu-language
layers), or any hit on a form with Connect learn markers but no `<assessment>`
block (`report.gating === 'non-gating'`, a baseline/pre-test Connect never
scores, ace#1131). Record each in the verdict so a reviewer can read it; a
genuine restatement in a pre-test still teaches the answer the gate later
asks, so say so when the text plainly restates one. Matching is per item (a
label is compared only with the answers of the items its own score depends
on) and on Unicode word boundaries.

**`report.blind` is a `[BLOCKER]` too — a blind check is not a clean one.** It
lists fail-branch labels whose text could not be resolved and answer literals
with nothing to match against; `report.ok` is false whenever it is non-empty,
and `formatRetryLeakReport` prints a `BLIND` block. Emit
`assessment-retry-leak-blind` and fix the *form*, not the gate. This exists
because the check reported the benign old `checked: false` on every released CCZ
until 2026-08-14 (#1332): it matched only `<`/`<=` while the compiler emits
`not(score >= N)`, and it read inline `<label>` text while the compiler moves
all label text into `<itext>`. Both are properties of a released CCZ — the only
artifact this skill ever holds.

Why it is a released-CCZ check and not only a build-time one: the live instance
(bednet-spot-check/20260729-0002) happened *because* the brief was hand-composed
at L0 and the `assessment-gate` component paragraph was skipped, so a build-time
assertion inside the producer is exactly the thing that was absent. The correct
answer is recoverable here because ACE's scoring calculates compare the question
against the correct answer's literal value — CommCare has no correct-option
primitive, so that literal is the only answer key that exists.

Effect if missed: the Connect Deliver-unlock gate is decorative. With no attempt
limit, a worker who fails once is shown the answer and passes on attempt 2, while
`user_score >= 80` remains wired and inert — and every structural check passes.

**Constraint locality — always, every form with constraints
(dimagi-internal/ace#980).** A `constraint` must be satisfiable on the
screen where it fires. Run the pure helper over each form XML:

```ts
import { checkConstraintLocality, formatConstraintLocalityReport }
  from '../../lib/constraint-locality';
const report = checkConstraintLocality(formXml);
```

It flags any constraint referencing a question or repeat the user cannot
edit from that screen, resolving hidden calculates transitively (so
indirection can't launder a foreign reference) and allowing the two
legitimate shapes: a self-reference (`.`) and a cardinality gate placed
**immediately** after the repeat it guards — including one spelled
`sum(<repeat>/<flag>) >= N` over a per-row `if(<predicate>, 1, 0)` indicator,
which is the same gate written a different way (ace#2416).

This check is **mechanical on purpose.** The class is 100% detectable
from the binds, and the LLM rubric missed it twice in one form:
`pdd-to-deliver-app-eval` scored `hh-poverty-targeting/20260722-1341`
8.5/10 while it shipped a GPS-accuracy rule on a later yes/no question
(message: "recapture the location", on a screen with no location widget)
and a roster-minimum rule on an unrelated zone question. A domain expert
found both on first read. Judgment is the wrong tool for a property this
crisp — hence a parser, and `lib/constraint-locality.test.ts` pins the
real defective binds as its negative control.

The checker is **screen-aware**, not question-aware: a group carrying
`appearance="field-list"` renders all its questions on ONE scrollable
screen, so a constraint referencing a sibling inside the same field-list
is **local** — the FLW scrolls up and fixes it in place. That is the
shape `skills/_app-component-library.md § data-quality-constraints`
*mandates* (`under_5 <= household_size`), and treating it as a violation
meant a correctly-authored app could not clear this step
(dimagi-internal/ace#1019).

Each violation carries a `severity`:

- `blocker` — the constraint never references the node it is bound to, so
  **no answer the user can give on that screen clears it**. The ace#980
  class: "recapture the location" on a screen with no location widget.
- `warn` — the reference crosses a screen boundary, but the constraint
  also references its own node, so lowering/changing the answer in front
  of the user satisfies it. Annoying, not a dead end.

Severity is decided structurally (does the expression mention its own
nodeset?), never by scanning the message text — validation messages are
free prose written per build, so a phrase list mis-grades any form whose
author phrased it differently (and mis-grades every language-stacked form
built before 2026-08-14 outright).

Each violation also carries a `kind`, because two different defects halt
here and their remedies differ:

- `kind: 'non-local'` — the ace#980 class above.
- `kind: 'dead-repeat-cardinality-gate'` — a **minimum-rows gate bound
  INSIDE the repeat it counts** (dimagi-internal/ace#1560). A constraint on
  a node inside a repeat is evaluated per repeat INSTANCE, so at zero
  repetitions it never evaluates at all — the one input the gate exists to
  reject. This shape satisfies locality *exactly* (a `count()` over your own
  repeat is a same-repeat reference), which is why it needed its own check:
  locality and reachability are different properties. The violation carries
  `deadGate: { repeat, countArg, comparison, minimumRows, fn, indicatorNode? }`.
  `fn` is `'count'` or `'sum'`; `sum` is recognised ONLY over a repeat child
  whose own `calculate` is a `if(<predicate>, 1, 0)` indicator, and
  `indicatorNode` names it (ace#2416). Quote `fn`, not a hard-coded `count(`,
  when you render the offending expression.

  Read `kind` on every violation. A report whose violations you bucket by
  `severity` alone loses the remedy — both kinds are `blocker`, and "move
  the constraint onto the node it is about" is the WRONG instruction for a
  dead gate (it is already on a node it is about).

`severity: 'blocker'` + `kind: 'non-local'` → halt with `[BLOCKER]`
`non-local-constraint` (naming each field, the foreign node, and "move the
constraint onto the node it is about"). `kind:
'dead-repeat-cardinality-gate'` → halt with `[BLOCKER]`
`dead-repeat-cardinality-gate`, naming the field, the repeat, and the
remedy the checker already whitelists: **move the gate to a question
immediately after the repeat**, where it evaluates at zero rows. (Nova
cannot carry it on the repeat container itself — `edit_field` on a repeat
answers `kind "repeat" carries no 'validate' slot`, ace#1560.)
`severity: 'warn'` → emit `[WARN]` `cross-screen-constraint` and continue.
Record per-app under `constraint_locality` in the verdict:
`{ constraints_checked, violations: [...] }` (each violation carrying its
`severity` AND its `kind`). Zero violations records
`constraint_locality: pass`.

**Relevance reachability — always, every form with relevance conditions
(dimagi-internal/ace#996).** The temporal sibling of the check above: a
`relevant` clause must be *decidable by the time the form walks past the
field it gates*. Same module:

```ts
import { checkRelevanceReachability, formatRelevanceReachabilityReport }
  from '../../lib/constraint-locality';
```

It flags any `relevant` referencing a field answered LATER, resolving
calculates transitively so a hidden calculate over a later answer inherits
that answer's position and can't launder it.

**Read the report's REAL fields (dimagi-internal/ace#1539).**
`RelevanceReachabilityReport` is
`{ relevancesChecked: number, violations: RelevanceViolation[] }`, and each
violation carries `whollyUnreachable: boolean`. There is **no** `checked`, no
`unreachable`, and no `partial` field — reaching for those names yields
`undefined` on every form, which renders as "nothing found" and reports a
BLIND PASS on the one check whose whole job is catching a field that can never
display. Derive the two buckets explicitly:

```ts
const wholly  = report.violations.filter((v) => v.whollyUnreachable);
const partial = report.violations.filter((v) => !v.whollyUnreachable);
```

`relevancesChecked === 0` means the form carries no relevance conditions —
"not applicable", NOT a pass, the same rule every other checker here follows.

Two severities:

- `whollyUnreachable: true` — every reference is later, so the field can
  **never** display. `[BLOCKER]`.
- `whollyUnreachable: false` — some clauses resolve in time, others never
  contribute. `[WARN]` — the field shows on some paths and silently not on
  others, which is how `outcome_note` submitted empty on exactly the two
  outcomes it existed to capture.

Record per-app under `relevance_reachability`. Same rationale as constraint
locality: mechanically detectable from bind order, so it is a parser rather
than a rubric line.

**Language tables vs. declared locales — always, every CCZ
(dimagi-internal/ace#2292).** Every `<lang>/app_strings.txt` in the zip must be
declared as a `<locale language="…">` in that CCZ's own `suite.xml`. Build the
file map FROM THE ARCHIVE, in memory, and run the pure helper over it:

```ts
import { auditCczLanguageTables, formatCczLanguageTables, readCczTextFiles }
  from '../../lib/ccz-language-tables';
const files = readCczTextFiles(cczPath);   // in-zip path -> text, no extraction dir
const audit = auditCczLanguageTables({
  suiteXml: files['suite.xml'],
  files,
  appName,        // optional — the app's name from the deploy summary
});
```

**Never feed it a directory you extracted into — that is how ace#2292 was
manufactured.** The issue reported that the released Deliver CCZ for
`bednet-check-2-visit/20260908-1544` (HQ app `a3359eaf446f498a80366e000a677a4a`,
build `171996636b714bb09dee8779e7e83927`) "unzipped to `default/ en/ modules-0/
modules-1/ nya/ tum/`", the last two being spark-facilitator's Chichewa/Tumbuka
tables. Re-downloading that build on 2026-10-16 and listing its ZIP ENTRIES
gave 7 files — `default/` and `en/` app strings, `profile.ccpr`,
`media_suite.xml`, two forms and `suite.xml` — and no `nya/` or `tum/`. The
reproduction (`unzip -o -q deliver.ccz && ls -d */`) had run in a scratch
directory still holding an earlier spark extraction: `unzip -o` overwrites the
files a zip carries and deletes nothing else, so spark's tables survived beside
bednet's fresh `suite.xml`, which is exactly why they looked undeclared. The
captured build is `test/fixtures/ccz/bednet-check-2-visit-20260908-1544-deliver-v7.ccz`,
and `test/lib/ccz-language-tables.test.ts` reproduces the residue mechanism. The
same rule binds Step 3 and every other gate that reads an unzipped tree.

**This is a `[FINDING]`, not a halt.** The device is only ever offered the
locales `suite.xml` declares, so an orphan table is unreachable to a worker and
the English device walk is unaffected. Emit `[FINDING]`
`undeclared-language-table` naming **each orphan language and its
`app.display.name`** (carried as a `foreign-display-name` finding on the same
audit). A `foreign-display-name` on a DECLARED language is `severity: 'signal'`
and does not flip `ok`: a genuinely translated app translates its own name, so
grading that would fire on every correctly multilingual build. `audit.missing`
(declared with no table in the zip) is the INVERSE case, reported and
deliberately not counted as an orphan. Before recording a finding, confirm the
orphan is in the archive (`unzip -l`) — a finding that only exists on disk is a
measurement error, not a residual. Record a real one as a Phase 3 residual and
do not hand-edit the zip.

`audit.status === 'unable'` means the check **did not run** — either the file
map carried no `app_strings.txt` at all, or `suite.xml` yielded zero locale
declarations (every released CCZ declares at least `default`, so zero means the
suite was not read, and reporting "every table is an orphan" on a failed read is
the loudest possible false finding). That is NOT a pass: render it with
`formatCczLanguageTables(audit, '<Learn|Deliver>')`, record it in the verdict's
`checks[]` with its `reason`, and treat the language tables as UNVERIFIED.

Record per-app under `language_tables`.

### Step 4.5: Runtime install validation via `commcare-cli.jar`

Steps 3–4 are **structural** and never bind any XPath expression,
leaving an install-time class uncovered: a CCZ whose XPath references
resolve to nothing at form-init (CommCare rejects it on-device with "A
part of your application is invalid"). `dimagi/commcare-core`'s
`commcare-cli.jar` ships two subcommands; use **both** in series:
`validate` (~2s, parser-class) and `play` (~5–10s, runtime form-init
defects — `XPathTypeMismatchException` from
`FormDef.initAllTriggerables`). For what each mode catches + the bednet
reproducer, see reference.md § Runtime install validation.

**Procedure** — for each app (Learn, Deliver):

1. **`validate` (parser-class pre-screen, fast):**

   ```
   commcare_validate_ccz({
     ccz_path: <local path to the released CCZ on disk>,  // preferred — no 10KB base64 round-trip through model context
     // OR ccz_base64: <if not on disk yet> — exactly one of the two
     mode: "validate",
   })
   ```

2. **`play` (the authoritative install-time gate, slower):**

   ```
   commcare_validate_ccz({
     ccz_path: <same path>,
     mode: "play",
     entry_path: [0, 0],   // first module → first form (default)
   })
   ```

   `entry_path` is the menu position **as displayed**, not the HQ module
   index (ace#2784). Child modules nest inside their parent menu, so on a
   Deliver app with nested child modules the root shows fewer items than
   there are modules. On group-payment-test the root lists `m0 / m3 / m4`
   as `0 / 1 / 2`, so the paid form `m3-f0` is `[1,0]`. Read the root and
   submenus off suite.xml's `<menu>` blocks: a menu with no `root=` is at
   the root, and `root="mN"` places it inside `mN` after that menu's own
   forms. Invoke `play` once per **form** you need covered. Each result
   echoes `command_id`, so check that it names the form you meant.
   **Fire all
   per-form `play` calls in parallel** (one assistant turn, multiple
   `commcare_validate_ccz` tool calls) — they read the same on-disk CCZ
   read-only and differ only by `entry_path`, so there's no ordering
   dependency. Likewise, run the Learn and Deliver `validate`/`play`
   checks concurrently rather than one app fully before the other. Await
   all results, then branch on the worst verdict. (Each call is its own
   short-lived JVM; serial execution just adds ~8s/module of dead wall time.)

   **Role-gated apps (`#user/<field>`, ace#2989).** `play` seeds every
   `session/user/data/<key>` the CCZ reads with an empty string, so a
   `relevant=` on it evaluates instead of throwing. A menu shown only for
   `#user/role = 'FLW'` is therefore hidden by default: pass
   `user_data: {role: 'FLW'}` (and one call per other role value) to walk
   that branch, counting `entry_path` as THAT role sees the menu. Read the
   role values off the `relevant=` attributes in suite.xml. Check
   `command_id` against the form you meant.

3. **Response shape (both modes):**

   ```
   { verdict: 'pass' | 'fail' | 'skipped',   // 'skipped' is play-only
     exit_code: <int>,
     // play-mode only:
     command_id?: 'm3-f0',            // the suite command entry_path resolved to
     skip_reason?: 'empty-case-list' | 'form-entry-not-reached'
                 | 'cli-case-index-unsupported' | 'entry-path-unresolved'
                 | 'cli-fixture-unseeded' | 'cli-user-data-unseeded',
     nav_unresolved?: <why entry_path landed on no command>,
     seeded_case_types?: [...],
     seeded_case_properties?: [{caseType, properties: {prop: literal}}],  // from case-list filters (ace#2286)
     unseeded_case_predicates?: [{datum_id, case_type, predicate, reason}], // with empty-case-list only (ace#2286)
     seeded_fixture_tags?: [...],     // item-list lookup tables seeded empty (ace#2860)
     seeded_user_data?: {key: value}, // custom user data in the restore (ace#2989)
     killed_reason?: 'restart-loop' | 'output-ceiling',  // helper killed a runaway JVM (ace#2988)
     failing_binding?: '/data/du_bednet_visit/deliver',
     unresolved_xpath?: 'instance(commcaresession)/session/data/case_id',
     // both modes:
     parser_message?: 'XPathTypeMismatchException: Calculation Error: …',
     failed_resource?: 'jr://resource/modules-0/forms-0.xml',  // validate only
     stdout: <truncated to 4KB>,
     stderr: <truncated to 4KB>,
     timed_out: <bool>,
     // present only on input errors:
     input_error?: 'jar_not_found' | 'ccz_not_found' | 'ccz_empty' | 'usage',
     input_error_path?: <path>,
   }
   ```

4. **Branch:**

   - **Both modes `verdict: 'pass'`** → record per-app `cli_validate: {validate: pass, play: pass}` and continue.
   - **`input_error: 'jar_not_found'`** (either mode) → emit `[WARN]` `cli-validator-unavailable` with the setup remediation below; continue. Structural Steps 3–4 still authoritative.
   - **`validate verdict: 'fail'`** → halt with `[BLOCKER]` `cli-validate-parser-error` naming `parser_message` + `failed_resource`. Don't bother running `play` — `validate` already proved the CCZ is structurally broken.
   - **`validate: pass` + `play: fail`** → halt with `[BLOCKER]` `cli-form-init-error` naming `failing_binding` + `unresolved_xpath` + `parser_message` (see § Failure modes for the bednet class + fix).
   - **`play verdict: 'skipped'`** → **do NOT halt**, and **never record it as a pass**: form-init was not observed, so the form is UNEVALUATED. Record `cli_validate.play: {verdict: skipped, skip_reason, command_id, seeded_case_types}` so the coverage gap is legible. The reasons are:
     - `empty-case-list` → `[INFO]`. The module's case list rendered zero rows, so the walk died in case-list rendering before form entry. `play` seeds one open case per case type declared in the CCZ's `suite.xml`, plus (ace#2286) one case per case list that filters on a conjunction of `<prop> = '<literal>'` equalities, carrying exactly those properties (echoed as `seeded_case_properties`). So this now only fires when a case-list filter is something else — `or`, `not()`, `!=`, a comparison, `selected()`, a date function, an `index/…` parent join. `unseeded_case_predicates` names each such predicate verbatim with its reason; copy it into the verdict.
     - `cli-case-index-unsupported` → `[INFO]` (ace#2784). Form entry WAS reached, but form-init ran a casedb index query (`case[index/parent = …]`, e.g. a `join()` over a group's member cases, or a `case-choice-attendance` checklist's `casedb` itemset and roster — the case-sourced choice kind Nova shipped in PR #730, closed 2026-10-08 as `voidcraft-labs/commcare-nova#728` and adopted in `playbook/integrations/nova-integration.md § The case choices channel`), and the CLI's in-memory sandbox has no `CaseIndexTable` (`"this.caseIndexTable" is null`). A device has one, so this is the harness's limit, not a defect. Observed on both group-payment-test session forms.
     - `cli-fixture-unseeded` → `[INFO]` (ace#2860). Form-init asked the synthetic restore for a fixture it does not carry (`FixtureInitializationException: Unable to find lookup table`). `play` seeds an empty `item-list:<tag>` fixture root for every `jr://fixture/item-list:<tag>` the CCZ's XML declares (echoed as `seeded_fixture_tags`), so this fires for a fixture kind that seed does not cover — and (ace#2941) when a binding or case-list column reads a ROW column of an empty-seeded table (`Logic references instance(<id>)/… which is not a valid question or value`, every unresolved ref an item-list instance; `unresolved_xpath` names the read). Do not reclassify such a `fail` by hand; the gate does it. A device receives the table on sync, so this is the harness's limit. Before ace#2860 the restore seeded no fixtures and every lookup-backed form graded `fail` → `cli-form-init-error` on a clean build. To check the device side, confirm the table exists on HQ with `commcare_get_lookup_table`.
     - `cli-user-data-unseeded` → `[INFO]` (ace#2989). Something read custom user data (`instance(commcaresession)/session/user/data/<key>`) the restore does not carry — typically a menu `relevant=` thrown from `MenuLoader.menuIsRelevant` while the root menu renders, before any form opens. `play` seeds every key the CCZ's XML names (echoed as `seeded_user_data`), so this fires for a key the scan cannot see. Fires only when EVERY unresolved ref is user data (or an empty-seeded fixture); a real XPath defect in the same stream still fails. HQ sends custom user data on sync, so this is the harness's limit; confirm the field exists on HQ with `commcare_list_user_fields`.
     - `form-entry-not-reached` → `[WARN]`. The walk ended without the CLI printing `Starting form entry` / `Form Start:`. This means the walk is wrong for this app shape (a datum screen it did not answer), so name `entry_path` + `command_id` and file it. Before ace#2784 this case was graded `pass`.
     - `entry-path-unresolved` → `[WARN]`. Your `entry_path` lands on no command, and the CLI was not run. `nav_unresolved` lists what that menu actually shows, so re-issue with the display position.

   **Case seeding (dimagi-internal/ace#1088).** *Most* ACE Deliver apps' payable
   form is a `followup` on a case type — but **not all**: the 2026-08-13
   hh-poverty-targeting build is registration-only, which is exactly the shape
   ace#977's `case-list-unreachable` check exists for. Do not read the sentence
   below as a universal. The restore used to
   seed zero cases — so `play` could not reach any of them and this gate
   had **never once** exercised `initAllTriggerables` on an ACE Deliver
   followup form, while reporting `fail` on clean builds. `play` now
   derives the case types from `suite.xml` and seeds one open case each,
   and derives the menu walk from the same file. A case datum inserts a
   case-list screen, and `detail-confirm` adds a confirmation screen. They
   come BEFORE the form choice when every entry in the menu needs that
   datum, and AFTER it otherwise. The menu tree comes from the `<menu
   root=…>` blocks, not from module indices (ace#2784). Nothing is sent
   after form entry —
   stray keystrokes are typed as *answers*, and a `0` on a date question
   raises `IllegalArgumentException: Invalid cast of data [0] to type
   Date`, which reads as a CCZ defect.

   **What seeding does not cover** — say so rather than implying the gate
   is now complete:
   - Case lists that filter on a case **property** with anything other
     than a conjunction of literal equalities. `[consent_given = 'yes' and
     household_state = 'registered_awaiting_followup']` (the
     `longitudinal-visits` payable list, bednet-check-2-visit/20260908-1544)
     IS seeded — suite.xml states the values a row needs, so they are not
     guessed (ace#2286). `or`, `not()`, `!=`, comparisons, `selected()`,
     dates and `index/…` joins are not: such a list is still empty →
     `skipped`, and `unseeded_case_predicates` names the predicate.
   - Case **search** / registry entries (`<query>` screens) and any datum
     screen other than a plain entity list.
   - Form-init that queries casedb by **index** (parent/child) →
     `skipped`/`cli-case-index-unsupported`. The CLI has no case index
     table. That form's init is not exercised by this gate at all.
   - `relevant=` conditions on menus/commands ARE evaluated by the CLI
     (`MenuLoader.menuIsRelevant`, ace#2989), so a hidden item shifts every
     later display position. The walk mirrors that only for a `relevant=`
     reading custom user data and string literals (`#user/role = 'FLW'`,
     `and`/`or`); any other relevance is assumed true, and `command_id` is
     how you catch a walk that landed elsewhere.
   - The child-menu listing (parent's forms first, then its child menus)
     and the descent into a child menu were observed live on
     group-payment-test (`0 / 2` lists `Register group / Add member /
     Group members / Session records (B)`, then opens the group case
     list). That app's child menus hold case lists, not forms, so walking
     all the way to a FORM inside a child menu has not been observed live. Non-zero form indices on a case-managed menu (`[0,1]` on
     group-payment-test `m0`) were walked live on 2026-10-07 and reach the
     form.

**Operator one-time setup (only when `input_error: 'jar_not_found'` fires):**

```bash
/ace:setup
```

`/ace:setup` auto-downloads the latest tagged `commcare-cli.jar` from
`dimagi/commcare-core` releases and caches it at
`$CLAUDE_PLUGIN_DATA/commcare-cli.jar`. Refresh with `/ace:setup
--force-install`; pin a specific build with `export
ACE_COMMCARE_CLI_JAR=/absolute/path/to/commcare-cli.jar`. Java 17+
required. `/ace:doctor` reports jar presence + cached version.

### Step 4.6: Minimum CommCare version vs the pinned APK (dimagi-internal/ace#1997)

Step 4.5's `validate` + `play` run a **JVM runtime with no
minimum-version gate**, so they cannot see the one property that
decides whether any ACE-provisioned device can open the CCZ at all: the
minimum CommCare version stamped into `profile.ccpr` at the zip root.

```xml
<profile version="10" requiredMajor="2" requiredMinor="64"
         requiredMinimal="0" uniqueid="cb980f9c…" name="… Learn app"/>
```

`requiredMinimal` is the **patch** component — that profile requires
`2.64.0`, not a four-part version. HQ/Nova stamps HQ's *current* release
into it at build time, so it moves whenever HQ ships and nothing in ACE
chooses it. ACE's mobile stack meanwhile **pins** the CommCare APK
(`ACE_CONNECT_APK_VERSION`, else `DEFAULT_APK_VERSION` in
`mcp/mobile/client.ts`) because each APK version needs a calibrated
selector map. When the CCZ's minimum exceeds the pinned APK, CommCare
renders a version-gate screen instead of launching the app and Phase 6's
device walk dies at the Connect→CommCare app-launch handoff — after an
AVD boot, a PersonalID login and a claim, and under the misleading
`claim-START-HANDOFF-WEDGED-issue629` label. Phase 3 is the last point
at which the app can still be rebuilt against a lower target.

Read `profile.ccpr` out of each unzipped CCZ (Step 3 already holds it)
and classify with **`checkCczMinVersion` from `lib/ccz-min-version.ts`**
— a pure function, unit-tested in `test/lib/ccz-min-version.test.ts`, so
the version arithmetic is not left to prose:

```ts
import { checkCczMinVersion } from '../../lib/ccz-min-version';
const res = checkCczMinVersion({
  app: 'learn',                     // or 'deliver'
  profileXml,                       // text of profile.ccpr from the CCZ root
  apkVersion,                       // ACE_CONNECT_APK_VERSION, else DEFAULT_APK_VERSION
  selectorMapVersions,              // versions with a map on disk — see below
  devicePhasePlanned: true,         // false ONLY when this run has no device leg
});
```

It returns a `CheckOutcome` (`lib/check-outcome.ts`), so **`status: 'unable'`
is not a pass** — narrow on `status` before reading anything else. On
`unable` the comparison never ran (unreadable `profile.ccpr`, or a pin that is
not a version triple): emit `res.reason` as a `[WARN]` and record the check as
UNEVALUATED, never as clean.

Resolve the two runtime inputs rather than hardcoding them:

```bash
# the APK Phase 6 will actually run
grep -m1 '^ACE_CONNECT_APK_VERSION=' "${CLAUDE_PLUGIN_DATA}/.env" 2>/dev/null \
  || grep -m1 "DEFAULT_APK_VERSION = " mcp/mobile/client.ts
# versions with a calibrated selector map
ls mcp/mobile/selectors/ | sed -n 's/^connect-\(.*\)\.yaml$/\1/p'
```

**Severity is conditional, and that is the point.** The condition is
true on *every* run today, so a flat `[BLOCKER]` would trade one Phase-6
failure for a Phase-3 failure on every `/ace:run` — earlier and cheaper,
but blocking every run behind a remedy no operator can apply mid-run,
which is how a gate gets switched off. A flat `[WARN]` on an
always-true condition is a line everyone learns to scroll past. So the
severity the helper returns keys on whether a remedy is actually
**reachable**:

| Outcome | State | Do |
|---|---|---|
| `status: 'unable'` | `profile.ccpr` absent/malformed, or the pin is not a version triple | `[WARN]` `ccz-profile-unreadable` / `apk-version-unreadable`, emitting `res.reason`. A check that could not run is never a silent pass |
| `checked`, `severity: 'ok'` | required ≤ pinned | Record and continue |
| `checked`, `severity: 'blocker'` | required > pinned **and** a calibrated selector map already covers the required version | **Halt** `[BLOCKER]` `ccz-min-version-gate`. The remedy is in-run: repin `ACE_CONNECT_APK_VERSION` to `res.satisfyingSelectorMap` |
| `checked`, `severity: 'warn'` | required > pinned, **no** map covers it | `[WARN]` `ccz-min-version-gate`, do NOT halt. The remedy is a new APK plus a live-calibrated selector map — human-owned, out of reach mid-run. Continue, and treat every Phase 6 device result from this run as **unobtained**, not as a pass |
| `checked`, `severity: 'info'` | required > pinned but this run walks no device | `[INFO]`. Nothing breaks here; recorded so the mismatch stays legible |

`res.findings[0].message` already names the CCZ's required version, the
pinned APK version, and the exact consequence; `res.findings[0].remedy`
names the fix. Emit both verbatim into `auto_surfaced_concerns` rather
than paraphrasing — a message that omits either version cannot be acted
on from the log alone. Note `severity: 'info'` still carries
`ok: false`: the mismatch is real, it just breaks nothing on a run with
no device leg.

**Class: static parsing + version comparison, not device truth.** Nothing
here is sent to, or matched against, a device — no selector string, no
tap coordinate, no recipe step order. Both inputs are text Phase 3
already holds. Per CLAUDE.md § *"The trigger is the CLAIM, not the
directory"*, unit tests are complete evidence for this check.

### Step 4.7: Re-release invariants against an existing opportunity (dimagi-internal/ace#2691, #2705)

Two checks, one per app — **4.7a Deliver** and **4.7b Learn** — each run only
when that app is being re-released. Both share the same gate below.

#### 4.7a Deliver

**Runs only on a Deliver RE-release**: when there is an existing
opportunity and the build being QA'd is a newer release of the same HQ app.
The opportunity is an explicit `--opportunity-id` (a live program, or any
opportunity outside this run), or this run's `run_state.yaml`
`phases.connect-setup.products.connect.opportunity.id` (Phase 4
configured an opportunity against an earlier Deliver build). On the first Phase 3 pass
there is no opportunity yet: record `rerelease_invariants: not-applicable
(no opportunity)` and skip.

Run-free, confirm the opportunity is wired to this HQ app before comparing:
`connect_get_opportunity({organization_slug, opportunity_id})`, whose
dashboard half names the `deliver_app` / `learn_app` wiring. A mismatch means
the build is not this opportunity's app. Record `not-applicable (opportunity
not wired to this app)` and name both apps.

Connect matches a forwarded submission by **HQ domain + HQ app id**, picks the
DeliverUnit — and so the payment unit — by the **`<deliver id>` `@id`**, and
evaluates the opportunity's **`form_field_rules`** as JSONPath over the form
JSON by **question path** (commcare-connect `form_receiver/processor.py:78`,
`:605-613`, `:428`, `:395-406`; `opportunity/models.py:1275-1282`). An `@id`
Connect has not seen creates a DeliverUnit with no payment unit, and the
visit errors `Payment unit is not configured` (`processor.py:429-433`). The
form **xmlns is never read** by Connect. A Nova re-upload re-mints every
form's xmlns but keeps the HQ app id, so the invariants a re-release must hold
are the `@id`s and the rule paths — not the xmlns.

1. **Baseline build.** Use the Deliver build Phase 4 configured the
   opportunity against — the Deliver `build_id` in the `app-release_summary.md`
   that preceded Phase 4 (Drive revision history, or the run's
   `phases.commcare-setup` record). If that cannot be determined (always the
   case run-free, unless the caller passes `--baseline-build-id`), use the
   **previously released** build of the same HQ app. Record which one you used.
2. Download the baseline with `commcare_download_ccz({domain, app_id,
   build_id: <baseline>, write_to_path})` and unzip it next to the candidate
   (Step 2/3 already hold the candidate's forms).
3. Resolve `form_field_rules` per § Inputs, in this order:
   1. `--form-field-rules`, when the caller passed it (an override);
   2. otherwise the LIVE rules, from `connect_get_verification_flags({organization_slug:
      <program org>, opportunity_id})`. That atom is read-only and never POSTs (ace#3161). Use
      its `form_field_rules` (each rule's `question_path`, `question_value` and
      `deliver_unit_ids`), and record `rules_source: live` with its `source_path`. The page is
      PM-only, so pass the PROGRAM org, never the holding org. A `verification_page_pm_only`
      error means the wrong org: re-resolve it and do not fall through;
   3. otherwise `phases.connect-setup.products.connect.opportunity.verification.form_field_rules`
      (`rules_source: run_state`).

   A live read that returns `form_field_rules: []` means the opportunity really has no rules;
   the `@id` check still runs. When the live read cannot run (no Connect session, or the
   opportunity is unreachable) and no other source exists, the `@id` check still runs and the
   rule-path check is recorded `unevaluated (no rules source)`. Never pass an empty list as if
   the opportunity had no rules.
4. Classify:

```ts
import { checkDeliverRerelease, formatDeliverRerelease }
  from '../../lib/deliver-rerelease-invariants';
const res = checkDeliverRerelease({
  baseline:  { buildId: baselineBuildId,  forms: baselineForms },   // [{ path, xml }] every modules-*/forms-*.xml
  candidate: { buildId: candidateBuildId, forms: candidateForms },
  rules: formFieldRules,
});
```

| Outcome | Do |
|---|---|
| `status: 'unable'` | `[WARN]` `rerelease-invariants-unable`, emitting `formatDeliverRerelease(res)`. Record as UNEVALUATED — never as a pass |
| `checked`, `blocking: true` | **Halt** `[BLOCKER]` — one entry per blocker finding (`deliver-id-disappeared`, `deliver-id-added`, `rule-path-missing`), message verbatim. Do not let Connect read this build |
| `checked`, `form-xmlns-changed` finding | `[WARN]` `form-xmlns-changed`, message verbatim, do NOT halt. It names the consumers it splits: HQ exports/reports/UCR keyed on xmlns, and connect-labs CCHQ-form pipelines (`cchq_fetcher.py:160-192` fetches only the CURRENT app's xmlns, so pre-release submissions drop out). Connect payment is unaffected, and ACE cannot preserve xmlns across a Nova upload, so a halt would have no in-run remedy |
| `checked`, `ok: true` | Record and continue |

Record under `per_app.deliver.rerelease_invariants`. *Enforced:*
`test/lib/deliver-rerelease-invariants.test.ts` — positive control is the real
v9 → v23 Deliver meeting form of `spark-facilitator/20261004-1706` (same
`@id community_meeting`, same three rule paths, new xmlns → pass + one WARN);
negative controls are a renamed `@id` and a removed rule question (both BLOCK).
Static parsing of two released CCZs — unit tests are complete evidence.

#### 4.7b Learn (dimagi-internal/ace#2705)

**Runs only on a Learn RE-release** against an existing opportunity — same
gate as 4.7a (`--opportunity-id` given, or
`phases.connect-setup.products.connect.opportunity.id` is set, and the Learn
build being QA'd is a newer release of the same HQ app).
Otherwise record `rerelease_invariants: not-applicable (no opportunity)`
under `per_app.learn` and skip.

Connect creates one `LearnModule` row per Learn `<module id>` at opportunity
creation and never deletes one (commcare-connect `opportunity/tasks.py:86-95`);
a submission's module block is matched by **`@id`**, and an unseen `@id`
creates a new row lazily (`form_receiver/processor.py:107-116`). Learn
progress divides by the row count (`opportunity/models.py:385-392`) and Learn
completes only at 100%. So a module `@id` that disappears caps every new-build
worker below 100%, and one that appears drops every worker who already
finished. The assessment is different: `process_assessments`
(`processor.py:208-241`) reads only `user_score` and never the assessment
`@id` — what matters is that an `<assessment>` block still exists.

1. **Baseline build** — the Learn `build_id` Phase 4 configured the
   opportunity against (same sourcing rule as 4.7a step 1), else the
   previously released Learn build. Record which.
2. Download it with `commcare_download_ccz({domain, app_id, build_id:
   <baseline>, write_to_path})` and unzip it next to the candidate.
3. Classify:

```ts
import { checkLearnRerelease, formatLearnRerelease }
  from '../../lib/learn-rerelease-invariants';
const res = checkLearnRerelease({
  baseline:  { buildId: baselineBuildId,  forms: baselineForms },   // [{ path, xml }] every modules-*/forms-*.xml
  candidate: { buildId: candidateBuildId, forms: candidateForms },
});
```

| Outcome | Do |
|---|---|
| `status: 'unable'` | `[WARN]` `rerelease-invariants-unable`, emitting `formatLearnRerelease(res)`. Record as UNEVALUATED — never as a pass |
| `checked`, `blocking: true` | **Halt** `[BLOCKER]` — one entry per blocker finding (`learn-module-id-disappeared`, `learn-module-id-added`, `assessment-disappeared`), message verbatim. Do not let Connect read this build |
| `checked`, `assessment-id-changed` / `form-xmlns-changed` | `[WARN]`, message verbatim, do NOT halt — Connect reads neither |
| `checked`, `ok: true` | Record and continue |

Record under `per_app.learn.rerelease_invariants`. *Enforced:*
`test/lib/learn-rerelease-invariants.test.ts` — positive control is the real
v11 → v12 Learn re-release of `spark-facilitator/20261004-1706`
(connect-ace-prod app `dcd4889a…`, builds `4cafbd1b…` → `6dbbbb2f…`: modules
`m0_pretest`…`m6_payment` and assessment `final_quiz` unchanged → clean pass);
negative controls are a renamed module `@id` and a removed assessment block
(both BLOCK), plus a renamed assessment `@id` and a re-minted xmlns (WARN only).

### Step 4.8: `[FIXED]` instrument verbatim fidelity (dimagi-internal/ace#2366)

**Deliver app only, and only when the PDD marks an instrument `[FIXED]`.**
`pdd-to-deliver-app § Step 4k` diffs the instrument's POINT VALUES against the
source; it cannot see an option that scores 0. On
`poverty-graduation/20260908-0510` the released Deliver app added
"Declined or does not know" to one of the Nigeria PPI's ten questions — a
verbatim-only instrument whose licence permits digitising it only unmodified —
and this skill and `app-release-eval` both passed it. This step reads the
RELEASED form, not the blueprint.

1. Resolve the instrument file exactly as Step 4k did (its `## Build notes`
   record the `file_id`); read it with `drive_read_file` (a markdown table) and
   parse with `parseInstrumentMarkdown`. A published `.xlsx`/`.pdf` source has
   no question-and-option table for this helper — use the `inputs/` markdown
   instrument the PDD cites; if there is none, record `unable` with that reason.
2. Run the check over every Deliver form XML Step 3 parsed:

   ```ts
   import {
     parseInstrumentMarkdown,
     checkFixedInstrumentVerbatim,
   } from '../../lib/fixed-instrument-verbatim';
   const res = checkFixedInstrumentVerbatim({
     instrument: parseInstrumentMarkdown(instrumentMd),
     forms: deliverFormXmls,
     // ONLY where the instrument itself says the question is not asked as-is,
     // quoting it — e.g. the PPI's household-size indicator, derived from a roster.
     exempt,
   });
   ```

| Outcome | Do |
|---|---|
| No `[FIXED]` instrument in the PDD | `fixed_instrument_verbatim: not-applicable` |
| Instrument file unreadable / no question table | `[WARN]` `fixed-instrument-unable`, record the reason — never a pass |
| `ok: true` | Record `matched` + `exempted` and continue |
| any `option-added` / `option-dropped` / `option-order-changed` / `question-text-changed` / `question-not-found` | **Halt** `[BLOCKER]` `fixed-instrument-not-verbatim`, one entry per finding, `message` verbatim. Repair goes back through `pdd-to-deliver-app` (Nova edit → re-release), not a CCZ patch |

Record under `per_app.deliver.fixed_instrument_verbatim`. *Enforced:*
`test/lib/fixed-instrument-verbatim.test.ts` — the instrument fixture is the
real `poverty-graduation` inputs file and the positive control is the released
targeting survey of `poverty-graduation/20260915-1518`; the negative control
re-adds the observed "Declined or does not know" fan option.

### Step 4.9: Every paid form records the followed entity's id (dimagi-internal/ace#2889)

**Deliver app only, and only when the PDD's
`program_parameters.followed_entity_case_type` names a case type.** A paid
form that updates a child case (a crop cycle) can submit nothing that names
the person the programme follows: on `smallholder-seasonal/20261012-1549`
(HQ `6137de98` v23) the paid "Harvest visit" wrote only
`update_crop_cycle/case/@case_id` and a non-crop-only `index/parent`, so no
report could attach a crop-cycle harvest to the woman.
`semantic-registry-author-qa`'s `entity-key` check saw it at Phase 7; this
step stops the build shipping it. The released form XML is the authority.

```ts
import { parseFollowedEntityCaseType, checkFollowedEntityId } from '../../lib/followed-entity-id';
const declared = parseFollowedEntityCaseType(programParameters.followed_entity_case_type);
const res = checkFollowedEntityId({
  caseType: declared.caseType!,
  forms: deliverFormXmls,            // { path: 'modules-N/forms-M.xml', xml } from Step 3
  // ONLY the paid forms pdd-to-deliver-app's summary records under
  // `followed_entity_id.exempt`, each with its reason — never added here.
  exempt,
});
```

| Outcome | Do |
|---|---|
| Row absent, `none (<reason>)`, or archetype neither `longitudinal-visits` nor `multi-stage` | `followed_entity_id: not-applicable` |
| Row present but unparseable | `[WARN]` `followed-entity-unable`, record the parser's `problems` — never a pass |
| `ok: true` | Record `field`, `paid_forms`, `exempted`, and any `warn` findings (field written only under a `relevant`) and continue |
| any `fail` finding | **Halt** `[BLOCKER]` `followed-entity-id-missing`, one entry per form, `detail` verbatim. Repair goes back through `pdd-to-deliver-app` (Nova edit adding the hidden derived field → re-release), not a CCZ patch |

Record under `per_app.deliver.followed_entity_id`. *Enforced:*
`test/lib/followed-entity-id.test.ts` — the negative control is the released
smallholder-seasonal Deliver forms (`test/fixtures/layer1/`); the positive
control is the same Harvest visit with the build rule applied.

### Step 5: Write verdict

Write `3-commcare/app-release-qa_result.yaml`. Shape:

```yaml
skill: app-release-qa
target: <opp>
run_id: <run-id>
ran_at: <ISO-8601>
schema_version: 1
verdict: pass | fail
overall_score: <number>  # 10.0 on pass, 0 on fail
per_app:
  learn:
    hq_app_id: <id>
    build_id: <id>
    form_count_blueprint: <int>
    form_count_ccz: <int>
    form_count_match: true | false
    starter_module:                       # ace#1787 — auditReleasedModules()
      status: checked | unable            # `unable` is NOT a pass
      reason: <str>                       # unable branch only
      ok: true | false                    # checked branch only
      declared_structure: compared | unavailable
      findings:                           # checked branch only
        - kind: starter-module | undeclared-module
          tier: blocker | suspect
          module: <str>
          form: <str>                     # starter-module findings only
          reason: <str>
    learn_module_markers:
      blueprint_count: <int>
      ccz_count: <int>
      match: true | false
    assessment_markers:
      blueprint_count: <int>
      ccz_count: <int>
      match: true | false
    field_fidelity:                       # ace#2285 — SET comparison, not counts
      - form_path: modules-0/forms-0.xml
        basis: field-id-set               # what was actually compared
        match: true | false               # false iff `missing_from_ccz` is non-empty
        missing_from_ccz: [<field-id>, ...]   # the gating signal
        unexpected_in_ccz: [<field-id>, ...]  # recorded; not gating on its own
        counts:                           # CONTEXT ONLY — never gate on these
          blueprint: <int>                # Nova counts sections + labels
          ccz_controls_and_binds: <int>   # reads LOW on section-using forms
          ccz_binds_only: <int>
      - ...
    cli_validate:
      validate:
        verdict: pass | fail | unavailable
        exit_code: <int>
        failed_resource: <descriptor when verdict=fail, optional>
        parser_message: <exception:msg when verdict=fail, optional>
      play:
        verdict: pass | fail | unavailable | skipped
        exit_code: <int>
        entry_path: [0, 0]
        failing_binding: </data/...> # when verdict=fail
        unresolved_xpath: <xpath>    # when verdict=fail
        parser_message: <exception:msg>
    min_commcare_version:                 # ace#1997 — checkCczMinVersion()
      status: checked | unable            # `unable` is NOT a pass
      reason: <str>                       # unable branch only
      required: <str>                     # e.g. "2.64.0", from profile.ccpr
      apk_pinned: <str>                   # ACE_CONNECT_APK_VERSION / DEFAULT_APK_VERSION
      severity: ok | info | warn | blocker # checked branch only
      satisfying_selector_map: <str|null>  # lowest map >= required, if any
      findings:                           # checked + !ok only
        - kind: ccz-min-version-gate
          message: <str>                  # verbatim — names both versions
          remedy: <str>                   # verbatim
    rerelease_invariants:                 # ace#2705 — checkLearnRerelease(); re-release only
      status: checked | unable | not-applicable   # `unable` is NOT a pass
      reason: <str>                       # unable / not-applicable only
      baseline_build_id: <id>
      baseline_source: phase4-configured | previous-release
      blocking: true | false
      module_ids: { baseline: [...], candidate: [...] }
      assessment_ids: { baseline: [...], candidate: [...] }
      xmlns_changes: [{ form, from, to }] # WARN only
      findings: [{ kind, severity, message }]
  deliver:
    hq_app_id: <id>
    build_id: <id>
    form_count_blueprint: <int>
    form_count_ccz: <int>
    form_count_match: true | false
    starter_module:                       # ace#1787 — auditReleasedModules()
      status: checked | unable            # `unable` is NOT a pass
      reason: <str>                       # unable branch only
      ok: true | false                    # checked branch only
      declared_structure: compared | unavailable
      findings:                           # checked branch only
        - kind: starter-module | undeclared-module
          tier: blocker | suspect
          module: <str>
          form: <str>                     # starter-module findings only
          reason: <str>
    deliver_unit_markers:
      blueprint_count: <int>
      ccz_count: <int>
      match: true | false
    task_markers:
      blueprint_count: <int>
      ccz_count: <int>
      match: true | false
    field_fidelity: [...]              # ace#2285 — same SET shape as learn
    cli_validate:
      validate:
        verdict: pass | fail | unavailable
        exit_code: <int>
        failed_resource: <optional>
        parser_message: <optional>
      play:
        verdict: pass | fail | unavailable | skipped
        exit_code: <int>
        entry_path: [0, 0]
        failing_binding: <optional>
        unresolved_xpath: <optional>
        parser_message: <optional>
    min_commcare_version:                 # ace#1997 — same shape as learn, above
      status: checked | unable
      reason: <str>
      required: <str>
      apk_pinned: <str>
      severity: ok | info | warn | blocker
      satisfying_selector_map: <str|null>
      findings: [...]
    rerelease_invariants:                 # ace#2691 — checkDeliverRerelease(); re-release only
      status: checked | unable | not-applicable   # `unable` is NOT a pass
      reason: <str>                       # unable / not-applicable only
      baseline_build_id: <id>
      baseline_source: phase4-configured | previous-release
      blocking: true | false
      deliver_ids: { baseline: [...], candidate: [...] }
      rule_paths_checked: [...]
      xmlns_changes: [{ form, from, to }] # WARN only
      findings: [{ kind, severity, message }]
# Per-app blocks additionally carry (both apps; see Step 4):
#   time_estimates:        pass | { modules_checked, violations: [...] }   # Learn app only
#   camera_only_uploads:   pass | not-required-by-pdd | [<offending upload refs>]
#   geopoint_binds:        pass | [<offending field paths>]
#   casedb_preloads:       pass | [<visible question refs answered from the case>]
#                          # BLOCKER-gated (ace#2006); Deliver app
#   repeat_counts:         pass | { count_bound, violations: [{ repeat, countRef,
#                            workerSources }] }
#                          # BLOCKER-gated (ace#2517); both apps, every form
#   payable_cap_arithmetic: { status: checked|unable, reason, ok, node, timing,
#                            clamp: { threshold, clampedValue }, capacity, cap,
#                            cap_source: declared|is_payable, indices: [...],
#                            findings: [...] }
#                          # BLOCKER-gated (ace#2148); Deliver app. `unable` is
#                          # NOT a pass — record the reason, treat as UNVERIFIED
#   constraint_locality:   pass | { constraints_checked, violations: [...] }
#   relevance_reachability: { relevances_checked, wholly_unreachable: [...], partial: [...] }
#                          # derived from violations[].whollyUnreachable (ace#1539);
#                          # the lib exposes NO checked/unreachable/partial fields
#   grid_menu_display:     { use_grid_menus, grid_form_menus,
#                            modules_checked, modules_gridded, non_grid: [...] }
#                          # all three fields are BLOCKER-gated (ace#1082)
#   fixed_instrument_verbatim: not-applicable | unable | { matched, exempted, findings: [...] }
#                          # BLOCKER-gated (ace#2366); Deliver app, [FIXED] instrument only
#   followed_entity_id:    not-applicable | unable | { field, paid_forms: [...], exempted: [...], findings: [...] }
#                          # BLOCKER-gated (ace#2889); Deliver app, followed_entity_case_type declared
#   language_tables:       pass | unable | { present: [...], declared: [...],
#                            orphans: [...], missing: [...], display_names: {...} }
#                          # FINDING-gated, never a halt (ace#2292) — an orphan
#                          # table is unreachable to a worker, so it is reported
#                          # as a Phase 3 residual, not a release blocker
auto_surfaced_concerns:
  - severity: BLOCKER | WARN | INFO
    message: "..."
blockers: [...]
```

Use `verdict: unavailable` when `commcare_validate_ccz` returned
`input_error: jar_not_found` (the operator hasn't built the jar yet).
Pair with a `[WARN]` `auto_surfaced_concerns` entry pointing at the
Step 4.5 setup block. Use `verdict: fail` only for real install-time
defects.

## Mode behavior

- Auto: write the verdict, halt on first BLOCKER.
- Review: same — this is a structural check with no human-judgment
  step.
- Dry-run: do the downloads + parses, write the verdict, but mark
  status as `dry-run-success` / `dry-run-blocked` instead of
  `pass` / `fail`.

## Failure modes

- `download-failed` — CCHQ returned non-zip bytes or an error. Likely
  a transient CCHQ issue or a wrong build_id. Operator action: verify
  the build_id in `app-release_summary.md` matches the released build.
- `cczunzip-failed` — zip decode failed. Likely a corrupted release.
  Re-run `app-release` to remake + re-release.
- `suite-xml-missing-or-malformed` / `xform-parse-failed` — Nova
  emitted invalid XML. Halt; re-run `pdd-to-{learn,deliver}-app`.
- `form-count-mismatch` — Nova said N forms, CCZ has M. Likely Nova
  partial-persistence on form creation. Re-run the build.
- `starter-module-present` — Nova's canonical starter module (menu
  "Survey" → form "Survey" → one text field `question_1` labelled
  "Question 1") survived to release, or the app carries a module the
  build summary never declared. Form-count equality cannot see this —
  the module is in the blueprint and the CCZ alike — which is why the
  check is identity-based (`lib/starter-module.ts`). Operator action:
  remove the module in Nova, re-run `app-deploy` → `app-hq-settings`
  → `app-release`, then re-run this gate. On a Deliver app treat it as
  blocking: an FLW tapping that menu lands in a dead form that writes
  nothing and is not a payable unit. (ace#1787)
- `cli-validate-parser-error` — `commcare-cli.jar validate` (the
  parser-class pre-screen) surfaced an `XFormParseException` /
  `InvalidStructureException` / `InvalidResourceException` /
  `UnresolvedResourceException`. The CCZ is structurally broken at the
  XML / suite / profile level. Halt loud; root cause is upstream in
  `pdd-to-{learn,deliver}-app` (Nova emitted malformed XML). No need to
  also run `play` — the structural defect is authoritative.
- `cli-form-init-error` — `commcare-cli.jar play` surfaced an
  `XPathTypeMismatchException` / `Calculation Error` /
  `Logic references … which is not a valid question or value` during
  `FormDef.initAllTriggerables`: at least one form's XPath binding can't
  resolve at form-init. **This IS the bednet bug class** (see reference.md
  § Runtime install validation). Verdict YAML's
  `per_app.<app>.cli_validate.play.{failing_binding, unresolved_xpath,
  parser_message}` name the exact defect. The most common cause is a
  `connect.deliver_unit.entity_id` (or `entity_name`) bound to a
  runtime-unresolvable XPath. Halt loud; the operator's fix is usually a
  `pdd-to-{learn,deliver}-app` re-build flipping the
  entity_id substitution per
  `docs/learnings/2026-05-25-entity-id-misdiagnosis.md`.
- `case-list-enum-drift` — an id-mapping case-list column renders a case
  property through a different taxonomy than the form `select1` that writes
  it, so the worker reads one vocabulary off the tile before the visit and
  picks from another during it (dimagi-internal/ace#1688). `[BLOCKER]`: both
  surfaces are well-formed in isolation, and this gate is the only place they
  are compared. Operator fix: re-run `pdd-to-deliver-app` — its Step 4l must
  derive the case-list enum from the SAME itemset it repairs the form's option
  labels from — then re-release and re-run `app-release-qa`. Do not hand-edit
  the enum: an instance fix leaves the next build free to reinvent it.
- `undeclared-language-table` — the CCZ ships a `<lang>/app_strings.txt` that
  its own `suite.xml` never declares as a `<locale language="…">`. `[FINDING]`,
  **not a halt** — the device is only offered declared locales, so the table is
  unreachable to a worker and the run continues. Operator action: FIRST confirm
  the table is in the archive (`unzip -l`, or the file map came from
  `readCczTextFiles`) — the only reported case (dimagi-internal/ace#2292,
  `spark-facilitator` tables "in" `bednet-check-2-visit`'s Deliver CCZ) was
  residue of an earlier extraction in a reused directory, and the build itself
  was clean. If it is real, record the orphan languages and their
  `app.display.name` as a Phase 3 residual and check them against the PDD's
  declared working language. Do not hand-edit the zip.
- `ccz-min-version-gate` — the released CCZ's `profile.ccpr` declares a
  minimum CommCare (`requiredMajor.requiredMinor.requiredMinimal`) ABOVE the
  APK Phase 6 will run, so CommCare shows a version-gate screen instead of
  launching the app and the device walk dies at the Connect→CommCare
  app-launch handoff (dimagi-internal/ace#1997). Step 4.5's `validate` +
  `play` cannot see this — the JVM runtime has no minimum-version gate — so
  this is the only Phase 3 surface where it is observable, and Phase 3 is the
  last point at which the app can be rebuilt against a lower target.
  **Severity is conditional** (Step 4.6): `[BLOCKER]` when a calibrated
  selector map already covers the required version (the remedy is in-run —
  repin `ACE_CONNECT_APK_VERSION`), `[WARN]` when none does (the remedy is a
  new APK plus a live-calibrated selector map, which is human-owned and out of
  reach mid-run; halting there would block every `/ace:run` behind work no
  operator can do, and a gate like that gets switched off). On the WARN branch
  the run continues, but every Phase 6 device result from it is **unobtained**,
  not a pass.
- `deliver-id-disappeared` / `deliver-id-added` / `rule-path-missing` —
  `[BLOCKER]` (Step 4.7, re-release only). The new Deliver build no longer
  carries a `<deliver id>` the existing opportunity was configured on, carries
  one Connect has never seen (its visits error `Payment unit is not
  configured`), or dropped/moved a question a configured `form_field_rules`
  row reads. Operator action: restore the `@id` / question path in Nova and
  re-release, or reconfigure the opportunity in Connect before releasing
  (dimagi-internal/ace#2691).
- `learn-module-id-disappeared` / `learn-module-id-added` /
  `assessment-disappeared` — `[BLOCKER]` (Step 4.7b, Learn re-release only).
  The new Learn build dropped or added a `<module id>` the existing
  opportunity's learn progress is counted against, or no longer carries an
  `<assessment>` block. Operator action: restore the `@id` / assessment block
  in Nova and re-release (dimagi-internal/ace#2705).
- `assessment-id-changed` — `[WARN]` (Step 4.7b). Connect never reads the
  assessment `@id`; only non-Connect consumers keyed on it are affected.
- `form-xmlns-changed` — `[WARN]` (Step 4.7a/4.7b). Nova re-minted form xmlns on
  re-upload. Harmless for Connect; splits HQ exports/UCR and connect-labs
  CCHQ-form pipelines keyed on xmlns. Not a halt — ACE has no remedy.
- `ccz-profile-unreadable` / `apk-version-unreadable` — `[WARN]`. The
  version-gate comparison could not be made: `profile.ccpr` was absent or
  malformed, or `ACE_CONNECT_APK_VERSION` is not a `MAJOR.MINOR.PATCH` triple.
  A check that could not run is recorded as such, never as a pass.
- `cli-validator-unavailable` — `commcare-cli.jar` not on the operator's
  machine (resolved jar path returned `input_error: jar_not_found`). This
  is `[WARN]`, not `[BLOCKER]` — Steps 3–4 still gate structural defects;
  this just means the install-time gate is off. Operator fix: run
  `/ace:setup` (auto-downloads the latest jar from
  `dimagi/commcare-core` releases).
- `learn-module-time-estimate-implausible` — a
  `connect.learn_module.time_estimate` in the released Learn CCZ is not
  plausible **as hours** against the PDD's stated module duration (the
  unit is hours end-to-end in Connect; a raw minute count renders as
  "N hours" on every FLW's onboarding screen — see Step 4 +
  dimagi-internal/ace#1077 + voidcraft-labs/nova-plugin#36). Operator
  fix: re-run `pdd-to-learn-app` (its brief carries the resolved hours
  instruction with source citations), re-release, then re-run
  `app-release-qa`.
- `learn-module-display-gated` — a `connect.learn_module` form in the
  released Learn CCZ sits behind a display condition on a user property, so
  workers who fail it can never complete Learn (Connect counts every marked
  module; ace#3036). Operator fix: rebuild per `pdd-to-learn-app § Step 2a`
  (every marked module visible to every worker; the restructuring choice is
  the `learn-gap-multi-role-learn-completion` decision row), re-release, then
  re-run `app-release-qa`.
- `learn-marker-missing` / `deliver-marker-missing` — released CCZ
  doesn't carry the Connect-marker wrappers Connect's sync requires.
  Halt; investigate Nova-side OR check if any post-build patcher
  (which should be none — `commcare-form-patch` was removed in
  PR #423) is stripping markers.
- `field-count-mismatch` — silent field omission: a field the Nova
  blueprint declares by **id** has no corresponding node in the released
  form XML. Re-run the build (Nova partial-persistence is usually fixed
  on retry). Fires on a named set difference only — never on a raw count
  difference, which has no shared basis between blueprint and CCZ and
  reads LOW on any section-using form (ace#2285; see Step 4 § Field
  fidelity per form).
- `geopoint-bind-downgrade` — a `kind:geopoint` field compiled to an
  XForm bind `type="xsd:string"` instead of `type="geopoint"` in the
  released CCZ (stale / downgraded build; see reference.md § Geopoint
  bind-type fidelity). Operator fix: re-build & re-release the app from
  the **current** Nova blueprint (Nova compiles geopoint correctly
  today), then re-run `app-release-qa` to confirm `type="geopoint"`.
- `camera-only-appearance-missing` — the PDD demands live-camera-only
  photo capture but an image `<upload>` node in the released Deliver
  form XML has no `appearance` containing `acquire`, so the on-device
  widget shows CHOOSE IMAGE (gallery uploads permitted; see Step 4
  + dimagi-internal/ace#867). Operator fix: apply the camera-only
  appearance flip (HQ app builder or Nova), re-release, then re-run
  `app-release-qa` to confirm the attribute is in the released CCZ.
- `grid-menu-display-missing` — the released app's raw doc
  (`/a/<domain>/apps/source/<build_id>/`) fails any of the three grid
  fields: `use_grid_menus != true`, `grid_form_menus != 'some'`, or a
  module with `display_style != 'grid'` — so `app-hq-settings` either
  didn't run, fail-softed, ran a pre-ace#1082 version that only set the
  per-module half, or was applied to a draft that was superseded before
  the release (see Step 4 + dimagi-internal/ace#1009 + #1082). Operator
  fix: re-run `app-hq-settings`, re-release, then re-run
  `app-release-qa`. Do **not** try to confirm this from `suite.xml` or
  `GET /api/v0.5/application/` — suite.xml only carries `style="grid"`
  when `grid_form_menus == 'some'` (bare on the half-applied app, and
  never shows the two app-level flags), and the REST API reads a
  misleading `None` for a correctly-gridded module (ace#1246).
- `non-local-constraint` — a `constraint` in the released form XML
  references a question or repeat the user cannot edit from the screen
  where it fires, so the error is unfixable in place and the FLW must
  navigate backward to a question that gave no sign of a problem (see
  Step 4 + dimagi-internal/ace#980). Operator fix: move the constraint
  onto the node it is actually about — a GPS-accuracy rule onto the
  geopoint itself, a repeat-cardinality rule onto the repeat or a gate
  immediately after it — then re-release and re-run `app-release-qa`.
  Only `severity: 'blocker'` violations halt; questions sharing an
  `appearance="field-list"` group are one screen and are not violations
  at all (ace#1019).
- `dead-repeat-cardinality-gate` — a minimum-rows gate (`count(<repeat>…)
  >= N`, N >= 1) is bound to a node INSIDE the repeat it counts, so it
  never evaluates at zero repetitions: the visit submits with an empty
  repeat and whatever the repeat feeds derives from nothing (see Step 4 +
  dimagi-internal/ace#1560, where an empty roster forfeited the PPI card's
  largest single indicator, 31 points, with nothing on screen to betray
  it). **This one is invisible to a device walk** — the same reason the FLW
  never sees it — so the released binds are the only place it surfaces.
  Operator fix: add a gate question **immediately after the repeat**
  carrying the same rule (the shape this checker already whitelists), and
  drop the inside-the-repeat copy; then re-release and re-run
  `app-release-qa`. Not fixable on the repeat container: Nova answers
  `kind "repeat" carries no 'validate' slot` (ace#1560).
- `dead-repeat-count` — a count-bound repeat's `jr:count` node is written
  only by an `xforms-ready` setvalue that reads a question the worker answers
  in the same form, so the count is empty at form open and the repeat renders
  zero rows on every submission (see Step 4 + dimagi-internal/ace#2517).
  Operator fix is in the Nova blueprint, not HQ: re-run `pdd-to-deliver-app`
  with its `repeat-count-source` rule (a worker-stated count becomes a
  `user_controlled` repeat whose number is derived as `count(<repeat>)`), re-deploy,
  re-release, re-run `app-release-qa`. Do not patch the XForm to add a
  `calculate` on the helper — the next Nova upload overwrites it, and the
  patch has never been validated on a device.
- `cross-screen-constraint` — `[WARN]`, not a halt. A `constraint` reaches
  into another screen, but it also references its own node, so the FLW
  clears it by changing the answer in front of them. Worth tightening
  (move the rule onto the screen that owns both numbers) but it does not
  trap anyone, so it never blocks a release.

## MCP tools used

- ace-connect: `commcare_download_ccz`, `commcare_validate_ccz`
- nova: `get_app` (form/marker counts), `get_form` (per-field `kind` for the geopoint bind-type check)
- ace-gdrive: `drive_read_file`, `drive_create_file`
- CCHQ HTTP probe (no atom yet): authenticated
  `GET /a/<domain>/apps/source/<build_id>/` for the grid menu-display
  check — the only surface that exposes `modules[].display_style` (see
  Step 4). A dedicated app-source atom on `ace-connect` would be the
  natural home (ace#1009 names it as an optional follow-up); until one
  exists this is a raw session-cookie GET.

## Writing the result (shared writer — every `-qa` skill)

Write the result file through the shared writer, never by hand:
collect one outcome per check you evaluated (`{check, type, result: {pass,
detail, auto_fix_hint}}`, or `{check, not_judged: "<why>"}` for a check whose
input does not exist yet) into a local JSON file, then

```bash
node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/qa-result.ts" write \
  --skill <this skill> --target <opp>/<run-id> --capture-path <artifact path> \
  --outcomes <outcomes.json> --out <local result.yaml>
```

and upload that file. It derives `stats` from the outcomes and a result that
evaluated nothing is a FAIL (`aggregateQAResult`, `lib/qa-types.ts`); ACE's own
ace-gdrive write guard turns a `*-qa_result.yaml` in any other shape into an
`INVALID_QA_RESULT` error (`lib/qa-result-write-guard.ts`). A hand-written shape reads on ace-web as
"Passed (0/0 checks)" — `skills/_qa-template.md § QA result YAML contract`.

