---
name: feedback-to-issues
description: 'Analyze a Senzing Bootcamp plugin feedback file and file it as GitHub issues in this repository, re-verifying every Senzing fact against the live Senzing MCP server first and reporting confirmed server-side defects upstream via submit_feedback. Use when the maintainer wants to process SENZING_BOOTCAMP_FEEDBACK.md, triage bootcamper feedback, or turn collected feedback into issues. Maintainer tool — not part of the bootcamper experience.'
argument-hint: "[path to feedback file] [--draft <run-dir> | --file <run-dir>]"
---

# Feedback → Issues

This is a **maintainer** tool for developing the Senzing Bootcamp Claude Plugin
(SBCP). It reads a feedback file collected during bootcamps, analyzes and triages
each item against the codebase, the **live Senzing MCP server** and the issues already
filed, and **files one or more GitHub issues in this repository**. It does **not**
implement the fixes — it turns raw feedback into actionable, deduplicated issues a
developer (or a follow-up session) can act on.

⛔ **It files in its own repository and nowhere else.** In child repos cross-repo routing
is owned exclusively by `/escalate-to-parent` *(children only)*; in this repo — the parent —
parent-to-child change travels by **parity**, so the parent never files into children at all.
⚠️ A `--repo` argument to `gh issue create`, or any other way of naming a repository, is a
violation of this rule rather than a convenience.

⛔ **It never writes into `specs/`.** That directory is a **read-only archive** as of the
2026-09-15 cutover (INV-307). Read it for historical context — a spec often records why the
plugin reads as it does — but nothing new lands there.

**Feedback is a snapshot; the server is not.** Every entry records how Senzing and
its MCP server behaved on the day it was written, and the server is released
independently of this plugin. So triage always re-asks the server before writing
(Step 5): a defect may already be fixed, a claim may have been wrong all along, or
the server may now contradict guidance the plugin still ships. Where the current
server is itself the defect, the finding goes back to Senzing (Step 8).

It is unrelated to the bootcamper-facing `/bootcamp-feedback` flow, which only
*captures* feedback. This skill *consumes* that captured feedback.

## Scope and guardrails

- ⛔ **Write no files except under `feedback/`.** Never modify plugin code, hooks, scripts or skills, and ⛔ **never write into `specs/`** — it is a read-only archive (INV-307). Filing issues is the deliverable; implementing them is a separate, later step. Exactly four actions have effects outside this session: **creating GitHub issues in this repository** (Step 7), appending to `feedback/PROCESSED.jsonl` and moving the processed file into `feedback/` (Step 9), renaming a duplicate candidate in place (Step 3), and the upstream notification in Step 8 — an MCP call, not a file write, and gated on the maintainer's explicit yes. **Never edit the content of a feedback file**, archived or not; the archive is a record.
- **Never process the same entry twice.** Identity is per entry and content-addressed (Step 3). A file whose entries are all in the ledger is a duplicate: rename it, report it, write nothing. A file with some new entries is triaged for those entries only.
- **Never invent feedback.** Every issue must trace to a real entry in the feedback file. If an entry is too vague to file, mark it *needs clarification* rather than guessing.
- **Re-verify every Senzing fact against the live MCP server before filing (Step 5).** Feedback is a snapshot of how the server behaved on the day it was filed, and the server ships independently of this plugin — so an issue written from the report alone can encode a defect that is already fixed, or miss that the server now contradicts the plugin. Never carry a Senzing fact from a feedback entry into an issue without re-asking the server (INV-080). ⚠️ **An issue is harder to correct than a spec was**: it is visible to anyone watching the repository the moment it is filed, so the re-check happens *before* `gh issue create`, never after.
- ⛔ **Asserting the server LACKS something requires naming the route that owns the fact.** Where an issue's diagnosis rests on absence — "returns no X", "does not cover", "no MCP tool answers this" — the `MCP re-check` line MUST also carry `owner-checked: <the route that would CARRY this fact> — <what it returned>` (**INV-213**; see `issue-template.md`). The tools you asked and found empty are true statements about *those tools* and no evidence for the negative (**INV-194**): "`sdk_guide(topic='load', record_count=100)` returns no license limit" is correct and worthless as support for "Senzing has no record limit", because the limit lives in `sdk_guide(topic='load', record_count=<above the limit>)`, whose `compatibility_notes` state it only when the count exceeds the limit. INV-213 is that reasoning carried into the issue format, and it matters more here than in shipped prose because an issue is the *input* to implementation — an absence concluded from the wrong route has already become an invariant plus a guard enforcing it, with the offline suite certifying both. Exempt: `n/a (no Senzing fact)`. Enforced by `tests/test_spec_absence_claims_name_their_owner.py`.
- **Deduplicate against two different things.** `feedback/PROCESSED.jsonl` catches the **same entry arriving again** in a later feedback file — per-entry and content-addressed (Step 3), and the primary check. ⚠️ It does **not** catch two *different* entries describing the same defect, so search the issue tracker before filing (Step 4). Where an item is already filed, **reference or update that issue rather than opening a second one**, and record it as already-tracked.
- **Respect the invariants.** Every generated issue references `specs/INVARIANTS.md` and must not propose anything that violates it (cross-platform Linux/macOS/Windows, language-agnostic, production-ready, consistent/coherent/complete). If feedback conflicts with an invariant, say so in the issue instead of silently overriding it.

## Step 1: Locate and read the feedback file

Resolve the feedback file in this order:

1. An explicit path the maintainer gave (argument or message).
2. `SENZING_BOOTCAMP_FEEDBACK.md` at the repo root.
3. `docs/feedback/SENZING_BOOTCAMP_FEEDBACK.md` (a bootcamper project's file, if copied into the repo).

⛔ **`feedback/` is the archive, never a candidate.** Files under `feedback/` have already
been processed (Step 9), and `*_DUPLICATE.md` files have already been rejected. Never resolve
a candidate to either, even when the maintainer's argument points at one — say what it is and
ask for the file they meant.

If more than one candidate exists and none was named, ask which to use. If none is
found, say so and stop — there is nothing to analyze.

Read the whole file.

## Step 2: Parse the feedback into discrete items

Feedback is usually a series of `## Improvement: <title>` blocks with subsections
(**What happened**, **Why it matters**, **Suggested fix**, **Context when
reported**), plus **Date**, **Module**, **Priority**, and **Source** lines. The context
block's **AI assistant** line names the assistant the bootcamper ran (Claude, GitHub Copilot,
Kiro, ChatGPT or Gemini) and is read in Step 6. An entry written before 2026-11-14 has no such
line; it came from the Claude plugin unless the file name says otherwise. Handle
free-form prose too — bootcampers do not always follow the template.

For each item, extract: `title`, `symptom` (what happened, with any verbatim
error/output), `impact` (why it matters), `suggested_fix`, `priority`, `module`,
`date`, and `source`. Skip the file's header/placeholder sections (e.g. an empty
"Your Feedback" heading with no content).

**`Source:` — who noticed it.** Two values (absent means `bootcamper-reported`):

- **`bootcamper-reported`** — a human hit this and said so. It is real, felt
  friction: someone's experience was degraded enough that they stopped to report
  it. Weight impact accordingly.
- **`self-observed (assistant retrospective)`** — the graduation retrospective
  filed it. These skew toward the defect class a bootcamper *cannot* report:
  silently-wrong output, undocumented environment gotchas, tools behaving
  differently than documented. A bootcamper never files "the field name was wrong
  so the section rendered empty," because on screen that looks like no data.

Do **not** treat self-observed items as lower priority by default — they are
often more severe precisely because nobody would otherwise catch them. Do use the
distinction when an issue's `## Problem` needs to say who experienced what: attribute
bootcamper-reported items to the bootcamper's experience, and self-observed ones to
what the assistant hit, without implying a user complained. Record the value in the
issue's `## Source` block so the provenance survives into implementation.

## Step 3: Check whether these entries have already been processed

Feedback files arrive from **multiple bootcampers at multiple times**, and the file is
gitignored at the repo root, so the same content reaches this skill more than once. The
realistic collision is **not** the identical file twice — it is a file that *overlaps* a
previous one, because a bootcamper's project accumulates entries during a run and a later
copy carries the earlier entries **plus** new ones.

So identity is **per entry**, not per file, and it is content-addressed: an entry's id is
`sha256` of its normalized text. Whole-file comparison gets the overlap case wrong in both
directions — a byte-compare calls the file new and re-files everything, and a whole-file
duplicate verdict would discard the genuinely new entries.

Run the bundled helper (it lives beside this skill; the hashing and normalization live in
code so a later run cannot drift and silently re-process everything):

```bash
python3 .claude/skills/feedback-to-issues/feedback_ledger.py check <candidate.md>
```

It prints every entry with its id and status, and exits **0** when some entries are new,
**3** when every entry has already been processed, **1** on bad input. Act on the verdict:

- **NEW** (no entry seen before) → triage the whole file. Continue to Step 4.
- **PARTIAL** (some entries seen) → **triage only the new entries.** Do not re-analyze or
  re-file the known ones; name them in the Step 10 report with the issue each previously
  produced, so the maintainer can see what was skipped and why. Continue to Step 4.
- **DUPLICATE** (every entry seen) → **stop. File no issues.** Run
  `feedback_ledger.py commit <candidate.md>`, which renames the file in place to
  `SENZING_BOOTCAMP_FEEDBACK_<unixtime>_DUPLICATE.md` — the unixtime of the archive
  it duplicates — and leaves the ledger untouched. Then tell the maintainer plainly: this
  file is a duplicate, nothing was processed, here is the archive it duplicates and the
  issues those entries already produced. Skip to Step 10 and report only that.

Why normalization is part of the identity, not a nicety: a file re-saved on Windows can
gain a UTF-8 BOM or CRLF line endings, and PowerShell can double-encode it outright — all
of which change the bytes while the content is the same (see `ground-rules.md` → "Windows
and PowerShell"). The helper strips the BOM, normalizes newlines, right-strips lines and
collapses blank runs before hashing, so "same feedback, different bytes" is still a
duplicate. It does **not** touch case or interior wording: a reworded entry is a new entry,
which is the correct call — the maintainer should see a revised report.

The ledger is `feedback/PROCESSED.jsonl`, append-only, one JSON object per processed entry:
`entry_id`, `title`, `archive`, `archive_unixtime`, `processed` date, and `disposition`.
The disposition is what makes it worth keeping — it records **which issue each entry
produced**, or `already-tracked`, or `needs-clarification`, so an entry that legitimately
produced no issue is never re-triaged forever.

## Step 4: Load triage context (do this before writing anything)

- **Read `specs/INVARIANTS.md`.** This is the ruleset every issue must respect. ⚠️ It is **live and still written to**, unlike the rest of `specs/`.
- **List the open issues** — `gh issue list --state open --limit 100` — and record each title and the problem it covers, so you can deduplicate against work already tracked. ⛔ **Check closed issues too** for anything you are about to file (`gh issue list --state closed --search <terms>`): re-filing something decided against wastes the decision, and a closed issue often records *why*.
- **Read `specs/` as history, never as a backlog.** It is a read-only archive (INV-307), and every spec in it is implemented or declined. A spec often explains why the plugin reads as it does, which is worth reading before proposing to change it — but nothing there is open work, and nothing new goes there. `specs/DECLINED.md` is the one to check before re-proposing something: it records the argument *against* a change that the spec itself argues *for*.

## Step 5: Re-verify every Senzing fact against the live MCP server

**Do this before analyzing, and before writing anything.** The Senzing MCP server is
versioned and released independently of this plugin, so an entry filed weeks or months
ago describes a server that may no longer behave that way. Three outcomes are all
common, and each changes what gets filed:

- **Still reproduces** → the item stands, and the issue carries a current citation instead of
  a stale field report.
- **Fixed upstream** → do **not** file an issue proposing a plugin workaround for a
  defect the server no longer has. Record it as resolved-upstream in the triage table
  and, if the plugin carries a workaround added for it, file the *removal* instead.
- **The server now contradicts the plugin** → the plugin is the thing that is wrong, and
  the issue's subject changes from "the server is broken" to "our guidance is stale".

Record the server version first — `get_capabilities` returns `server_info.server_version`
— so every claim you write can be dated and attributed. Then, for each item touching
Senzing behavior, re-ask the tool that owns the fact:

| The entry claims something about… | Re-ask |
|---|---|
| an SDK method, its arguments, or its response shape | `get_sdk_reference(topic='parameters' \| 'response_schemas', filter='<method>', language='<binding>')` |
| a flag, what it applies to, or what it returns | `get_sdk_reference(topic='flags', filter='<FLAG_NAME>')` |
| an attribute or mapping rule | `search_docs(query='…', category='data_mapping')` |
| an error code or its symptom | `explain_error_code('<SENZnnnn>')` |
| export, reporting, evaluation or graph behavior | `reporting_guide(topic='…')` |
| install, configuration or platform paths | `sdk_guide(topic='install' \| 'configure', platform='…')` |
| an example file or repository | `find_examples(...)` |

Rules for this step:

- **Ask the tool that owns the fact, not `search_docs` for everything.** A flag's
  `applies_to` is authoritative in `topic='flags'`; prose found by search is not.
- **Quote what the server returned** into the issue, rather than paraphrasing it. A future
  reader must be able to tell your claim from the server's.
- **A single field observation does not outrank the server, and the server does not
  outrank a reproducible observation.** When they disagree, say so plainly and record
  both with their conditions — flag set, SDK version, binding, platform (INV-169). Most
  "contradictions" turn out to be two different conditions, and an issue that flattens
  them into one absolute is the defect this repo has already had to retract twice.
- **Where the server cannot reach** (a field name below the shape `response_schemas`
  documents, a value only a live engine returns), say that explicitly and mark the fact
  as observation-only with its version and date — never launder it into an MCP-sourced
  claim (INV-080/INV-149).
- **If the network is unavailable**, do not guess and do not fall back to training data:
  file the issue with the fact marked "unverified — MCP unreachable at triage time" and
  say so in the report, so it can be re-checked before implementation.

## Step 6: Analyze each item (go beyond the feedback text)

For every parsed item:

1. **Classify** it: bug / false-positive, UX or wording, missing feature, invariant gap, documentation, or unclear.
   Then decide **which assistants it affects**, because the bootcamp is one source built for five:
   - **Every assistant:** the defect is in `source/` text or a bundled script that no marker varies.
     Reproduce it by reading the source, not one package. This is the default: text outside a
     host marker is the same everywhere.
   - **One assistant:** the defect is in that assistant's profile, fragments or files under
     `hosts/<assistant>/`, in the hook adapter's handling of its payloads, or in how the assistant
     itself behaves. Say which, and check `python3 -m tools.bootcamp_build check` still passes
     after the fix.
   - **Unknown:** the entry names no assistant and the evidence does not settle it. Say so.
   Put the verdict in the issue's Source section, and label the issue `assistant:<id>`
   (`assistant:claude`, `assistant:copilot`, `assistant:kiro`, `assistant:chatgpt`,
   `assistant:gemini`) only when it affects that one assistant. ⛔ A report from one assistant is
   not evidence the defect is limited to it: most are not.
2. **Confirm the root cause in the codebase**, don't just restate the report. Open the code the feedback implicates — `source/hooks/`, `scripts/`, `skills/`, `commands/` — and verify what actually causes the symptom. Cite `file:line`. If you cannot confirm it, label the root cause "Unverified — needs investigation" rather than asserting one.
3. **Reconcile the code against what Step 5 returned.** Where the plugin's text or code states a Senzing fact the server now answers differently, the plugin is the defect — even when the entry blamed the server, and even when the plugin's claim was correct when written. Check both directions: text the server contradicts, *and* a workaround the plugin still carries for a defect the server has since fixed.
4. **Decide the routing** — `plugin`, `mcp-server`, `both`, `host` or `unclear`, the same five verdicts the bootcamper-facing flow records (`feedback.md` Step 2b) — from what Step 5 established, not from what the entry guessed. An entry may be routed `mcp-server` and still need a plugin issue (our reference should record the confirmed shape), and one routed `plugin` may turn out to be a server defect worth reporting upstream (Step 8). ⛔ **`host` has no upstream channel and MUST NOT be sent** — `submit_feedback` reaches Senzing, which does not ship the Claude Code harness, so Step 8 is skipped for it entirely. A `host` entry may still need a **plugin** issue for the part the bootcamp does own: what it says when the bootcamper raises it, and how it recovers a question the host displaced.
5. **Deduplicate** against the issues listed in Step 4. Mark the item `already-tracked → #<n>` when covered, whether that issue is open or closed — a closed one means the question was decided, so re-filing needs a reason that answers the decision.
6. **Group**: merge items that share one root cause or one fix into a single issue; keep unrelated items in separate issues. The number of issues per run is whatever the analysis warrants — one, several, or (if everything is already tracked or too vague) none.

## Step 7: File the issue(s)

For each item that warrants one, file **one GitHub issue in this repository**, using
`issue-template.md` (in this skill's directory) as the body.

⛔ **(INV-314) Show the maintainer the title and body, and get a yes, before filing. Or get one
yes for the whole list shown in one message (INV-314, 2026-10-13 note), under the conditions in
`.claude/skills/feedback-to-issues/drafts.py` → "The batch yes".** Filing is
**outward-facing and immediate** — the issue is visible to anyone watching the repository
the moment it is created, and it carries the Bootcamper's report into a public record.
An issue can be edited or closed afterwards, but it cannot be un-filed, and its
notifications have already gone out. ⚠️ This is the same gate Step 8 applies to
`submit_feedback`, for the same reason, except that there each message takes its own yes.

```bash
gh issue create --title "<title>" --body-file <file>
```

⛔ **(INV-319) Never pass `--repo`, and never file anywhere but here.** In child repos cross-repo
routing is owned exclusively by `/escalate-to-parent` *(children only)*; this is the parent,
where parent-to-child change travels by **parity**, so the parent never files into children
at all. A flag naming another repository is a violation of that rule, not a convenience.

⛔ **(INV-318) Never apply the `unattended-ok` label to an issue this run files.** A triage that
labels the issues it files lets `/unattended-issue-loop` *(user level)* work them with nobody
between the report and the work. Choosing what runs unattended is the maintainer's decision alone.

⛔ **(INV-368) With `--draft <run-dir>`, this run files nothing, fixes nothing and sends nothing, and writes
nothing outside `<run-dir>`.** Each issue, Step 8 message and Step 9 disposition becomes a
[`drafts.py`](drafts.py) `add` record instead, the candidate stays where it is, and the run ends
with `drafts.py list`. `--draft` is the release cycle's interface (#573), and the caller records
unresolved drafts (INV-317). **With `--file <run-dir>`**, file what `drafts.py file-plan` prints,
after a yes for each record or one yes for the whole list shown in one message (INV-314,
2026-10-13 note), under the conditions in `.claude/skills/feedback-to-issues/drafts.py` →
"The batch yes"; an upstream draft is never sent by `--file` and keeps its own yes. Both
stages, the manifest and its statuses are stated once in `drafts.py` (INV-300).

Rules for the issue itself:

- **Write the title as the defect, not the symptom** — the shape the existing issues use, e.g. *"`/retrofit-from-public` should file issues, not apply changes directly"* rather than *"retrofit is wrong"*. It is what a reader scans in a list of thirty.
- **Ground it in code.** Root cause cites real `file:line`; affected files list real paths. Where you could not confirm it, write "Unverified — needs investigation" rather than asserting a cause.
- **Ground every Senzing fact in Step 5's result, with its provenance.** Name the tool and parameters that established it, the server version and the date — e.g. "`get_sdk_reference(topic='flags', filter='SZ_ENTITY_INCLUDE_RECORD_JSON_DATA')` reports `applies_to: ["get_record"]` (server 1.32.1, verified 2026-07-28)". Where the entry and the server disagree, state both and which governs. Where the fact is observation-only, mark it so.
- ⛔ **Carry the `owner-checked:` clause on any absence claim** (INV-213). See the guardrails above: the tools you asked and found empty are evidence about those tools, never about the negative.
- **Say when the current server changed the report.** If re-verification narrowed, widened, redirected or canceled what the entry asked for, put that in the issue rather than silently filing the corrected version — the next reader needs to know the report and the issue differ, and why.
- **Make acceptance criteria observable and testable**, and include a criterion that the change holds on Linux, macOS and Windows and stays language-agnostic (the invariants). For a fact only a live engine can confirm, say so in the criterion rather than writing one that cannot be run.
- **Link the source**: name the feedback file, the entry title, its date, module and priority.
- **Record the issue number** as you go — Step 9's ledger entries and Step 10's triage table both need it.

⚠️ **A minor item is still an issue, or it is nothing.** There is no lightweight backlog to
route it to: `specs/todo.md` served that purpose and is frozen with the rest of the archive
(INV-307). So either it is worth an issue — small ones are cheap and closeable — or it is
recorded in the triage table as *not filed*, with the reason. ⛔ **Do not invent a third
destination.**

## Step 8: Notify Senzing when the defect is theirs

An item belongs upstream when Step 5 confirms the **current** server is what is wrong —
a wrong or unobtainable documented path, a flag whose `applies_to` contradicts the
schema, a missing response shape, guidance that produces code the SDK rejects. A plugin
an issue and an upstream report are not alternatives: file both when the plugin also needs to
record the confirmed behavior.

1. **Check the entry's `Upstream:` field first, and classify it by the table below.** The
   bootcamper-facing feedback flow may already have sent it (`submitted YYYY-MM-DD`), in which
   case do not re-file the same finding. A **follow-up** is worth sending only when you now have
   something the first submission lacked — that it still reproduces on a newer server
   version, or a confirmed field name/shape they can act on. Say in the message that it
   is a follow-up.

   ⛔ (INV-281, INV-300) **This is the canonical statement of both closed `Upstream:` sets and
   the mapping between them.** The **entry field** (a bootcamper's feedback entry) is the first
   column of the mapping; the **issue field** (a filed issue's `Upstream:` line) is the second
   table. Every other site that enumerates a field states that field's full set, nothing
   missing and nothing extra, and every value written into a field is a member of its set.
   `tests/test_blocked_submission_has_a_vocabulary_value.py` parses both tables and holds
   every site to them.

   | Entry value | Report still owed? | Issue value once the maintainer is asked | Issue value when no maintainer is asked |
   |---|---|---|---|
   | `not applicable` | no | `not applicable` | same |
   | `submitted YYYY-MM-DD` | no | `already sent <date> (per the entry)` | same |
   | `offered, declined` | no | `declined by the bootcamper (per the entry)` | same |
   | `offer pending` | **yes** | `sent <date> via submit_feedback (<category>, anonymous)`, `declined by the maintainer`, or `submission failed: <reason>` if the maintainer's send errors | `not yet sent — needs maintainer approval` |
   | `submission blocked: <reason>` | **yes** | as above | `submission blocked: <reason>` (keeps the record of consent) |
   | `submission failed: <reason>` | **yes** (a retry can succeed) | as above | `submission failed: <reason>` |
   | *(no entry: a finding an unattended run drafts in its handoff, filing no issue)* | **yes** | as above | `not yet sent — needs maintainer approval` |

   | Issue value | Report still owed? |
   |---|---|
   | `not applicable` | no |
   | `already sent <date> (per the entry)` | no |
   | `declined by the bootcamper (per the entry)` | no |
   | `sent <date> via submit_feedback (<category>, anonymous)` | no |
   | `declined by the maintainer` | no |
   | `submission failed: <reason>` | **yes** |
   | `submission blocked: <reason>` | **yes** |
   | `not yet sent — needs maintainer approval` | **yes** |

   `offer pending` itself is never written on an issue (#167): the issue side has its own
   pending value.

   ⛔ (INV-281) **`submission blocked: <reason>` is an outcome where the report is STILL OWED,
   and it must not be triaged like a decline.** It means the answer was **yes** and the
   session could not send on it — a `/dry-run`, which never sends on an in-character
   answer. Nobody declined anything, so the finding still needs forwarding: draft the
   message and put it to the maintainer. ⚠️ `offered, declined` and `declined by the
   maintainer` are values that end the obligation; `submission blocked:` is a value
   that keeps it. Reading the first where the second was meant is how a consented report
   stops being anyone's job.

   ⛔ (INV-281) **`offer pending` is STILL OWED too, and is handled the same way.** The entry was
   saved before its upstream question was answered, and the bootcamp never came back to answer it.
   Nobody declined anything: draft the message and put it to the maintainer, exactly as for
   `submission blocked:`. `submission failed: <reason>` is still owed as well: a retry can
   succeed.
2. **Draft the message as a technical bug report Senzing can act on without context from
   this repo:** the tool and parameters called, what came back, what was expected, the
   contradiction (quote both sides), the server version and SDK version, and the impact
   in one line. Include a minimal reproduction.
3. **(INV-321) Strip everything identifying.** No bootcamper name, employer, email, file paths from
   their machine, host names, dataset contents, or record values — the MCP server's own
   notice forbids sending PII, and submissions are anonymous, so nothing in the message
   can be followed up with you. Describe data shape, never data.
4. **(INV-314) Show the maintainer the exact message and get an explicit yes before sending.** This
   is required by `submit_feedback` itself and is the only outward-facing action this
   skill takes; a decline costs nothing and the issue still stands. Then call
   `submit_feedback(category='bug', message='<the approved text>')` — `category='feature'`
   for a coverage gap that is a request rather than a defect.
5. **Record what happened** in the triage report and on the issue's `Upstream:` line, as an
   issue-field value from item 1's table: `sent <date> via submit_feedback (<category>, anonymous)`,
   `declined by the maintainer`, `submission failed: <reason>` when the send errors, or
   `already sent <date> (per the entry)` when the entry was already sent. Note that the
   submission is anonymous, so no reply is possible — if the finding needs a conversation, it needs a channel other than this tool.

⛔ **Never send under `category='license_request'`.** That path takes personal details and
is for evaluation licenses only; a defect report there is both wrong and a PII leak
(INV-135).

## Step 9: Archive the processed file and record its entries

**Do this only after the issues are filed** (Step 7) and any upstream submission is
settled (Step 8). If a run aborts before that, the candidate must still be exactly where it
was — an archived input with no issues to show for it is the one outcome worse than
re-processing.

```bash
python3 .claude/skills/feedback-to-issues/feedback_ledger.py commit <candidate.md> \
  --disposition "<entry title>=#<issue number>" \
  --disposition "<entry title>=already-tracked" \
  --disposition "<entry title>=needs-clarification"
```

With `--file <run-dir>`, the dispositions are the lines `drafts.py after` prints.

This moves the file to `feedback/SENZING_BOOTCAMP_FEEDBACK_<unixtime>.md` and
appends one ledger line per **newly processed** entry. Entries this file carried that were
already in the ledger are not re-recorded, and are reported as skipped.

- **Pass a `--disposition` for every entry you triaged.** Without it the ledger records
  `unrecorded`, the helper warns, and the ledger loses the thing that makes it useful — the
  link from an entry to the issue it produced. Use the entry's title exactly as the `check`
  output printed it.
- **The archived file stays on this machine; only the ledger is committed.** This repository is
  public, and a feedback file carries bootcamper text: usernames, workstation details, dataset
  names. `.gitignore` keeps `feedback/SENZING_BOOTCAMP_FEEDBACK_*.md` out of git, so the raw
  report is kept locally for reference and `feedback/PROCESSED.jsonl` is the durable record of
  what was processed. ⛔ Never force-add an archived file, and never quote more of an entry in
  an issue than the defect needs.
- **Never edit an archived file or a ledger line.** Both are the record of what was
  processed. The ledger is append-only and read **last-wins**, so a disposition recorded as
  `unrecorded` (or recorded wrongly) is corrected by *appending*:
  `feedback_ledger.py annotate <entry_id> "<disposition>"`. A correction to the *analysis* is a
  new issue, never a rewritten entry.
- **Quote a title exactly, or address the entry by id.** A `--disposition` key is matched
  against the title as `check` printed it; titles containing `=` (e.g.
  `sdk_guide(topic='configure') …`) are why the key is split on the **last** `=`, and why the
  `entry_id` is accepted as a key. If the helper warns `unrecorded`, fix it with `annotate`
  rather than leaving the ledger without the entry-to-issue link.

## Step 10: Report the triage

Present a compact table so the maintainer sees every item's disposition, including
what the live server said about it:

| Feedback item | Classification | MCP re-check | Action |
|---|---|---|---|
| <title> | <bug/UX/feature/…> | still reproduces | New issue → #<n> |
| <title> | <…> | server now contradicts the plugin | New issue → #<n> (subject redirected) |
| <title> | <…> | fixed upstream | Not filed — resolved on server <version> |
| <title> | <…> | n/a (no Senzing fact) | Already tracked → #<n> |
| <title> | unclear | not checked | Needs clarification |

State the server version every re-check ran against, once, above the table.

**Name what was skipped as already-processed, and where the file went.** A PARTIAL run must
list the known entries with the issue each previously produced — otherwise the maintainer
cannot tell "we triaged 2 of 6" from "the file only had 2". Then give the archive path and
the ledger line count from Step 9. For a DUPLICATE run this is the entire report: nothing
was processed, here is the `_DUPLICATE` filename, here is the archive it duplicates, and
here are the issues those entries already produced.

Then list the issues created (as `#<n>` references, which GitHub renders as links), note
anything routed to `todo.md` or left for clarification, report each upstream
submission's outcome as its issue-field value (Step 8.1's table), and offer next steps
(e.g. "I can implement #<n> next with /implement-github-issue" *(user level)* or "want me to open the questions
for the unclear items?"). Do not start implementing unless asked.

**Call out anything the re-check changed.** If the current server narrowed, redirected or
canceled what an entry asked for, say so in the report as well as in the issue — that is
the highest-value output of a triage run, and it is invisible if it only lives in a file
the maintainer has not opened yet.
