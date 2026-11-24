---
name: delegate-to-mcp-server
description: 'Sync the Senzing Bootcamp plugin with the live Senzing MCP server by finding Senzing facts the SBCP still holds that the server now serves itself, and filing GitHub issues to delegate them to a runtime call. Use when the maintainer wants to sync with the MCP server, retire redundant or stale Senzing content, check what the server now covers, or reduce the plugin''s Senzing-fact maintenance surface. Files GitHub issues in this repository — never edits the plugin, never writes under specs/. Maintainer tool — not part of the bootcamper experience.'
argument-hint: "[area or category to bound this run to] (omit to take the full re-check list) [--draft <run-dir> | --file <run-dir>]"
---

# Delegate to the Senzing MCP server

This is a **maintainer** tool for developing the Senzing Bootcamp Claude Plugin
(SBCP). It compares the Senzing facts the SBCP **holds** against what the live
Senzing MCP server **now serves**, and files **GitHub issues** proposing that the
plugin stop holding what the server can answer at runtime.

The premise: the SBCP guides a Bootcamper through Senzing; the MCP server is the
authority on Senzing (INV-080). When a fact was written into the plugin the server
may not have had it — so the plugin filled the gap, correctly. The server ships
independently and gets smarter, and that same text becomes redundant, then stale,
then wrong. Nothing in the plugin notices: a cached fact reads exactly as
authoritative on the day it goes out of date. This skill is the periodic sweep that
notices.

**The goal is a smaller maintenance surface, not a smaller plugin.** Every fact the
SBCP stops owning is a fact that can never again go stale here. That is the whole
return, and it is why a deletion that makes the bootcamp *worse* is a net loss even
when the server can technically answer the question.

## What this skill is not

Three neighbors overlap; keeping them distinct keeps all four useful.

| Skill | Asks |
|---|---|
| `dry-run` phase 1 | Do the plugin's MCP **calls** work? (right tool, required params, enum values) |
| `auto-test` | Has the server **drifted** under the calls the plugin already makes? |
| `feedback-to-issues` | What did a **bootcamper** hit, and is it still true? |
| **this skill** | What does the plugin still **own** that the server now owns? |

`dry-run` spot-checks two adjacent patterns ("a figure hardcoded that the server says
to look up", "an invariant asserting a server limitation"). This skill is the
systematic version of both, and it is the only one of the four that reads the plugin's
*content* as a maintenance liability rather than as a set of instructions to test.

## Scope and guardrails

- ⛔ **Write nothing under `specs/`.** It holds live records only (INV-307): the table in
  `specs/README.md` is the list of the files that belong there, and the frozen archive of the
  spec files is in the repository `specs/README.md` names. This skill's only writes
  are **GitHub issues** and its own ledger, `specs/mcp-coverage.jsonl` — a **named live
  exception** to the freeze, recorded in INV-307 and in the table in `specs/README.md`.
  ⚠️ **It is NOT exempt for being `.jsonl`.** That was the reason given here until #142, and
  it rested on the `specs/*.md` glob the freeze guard used until #257 — *a scope-narrowing that
  happens to produce correct behavior, which INV-308 says must not be relied on*, as
  `invariant_manifest.py` says of its own artifact. Widening the guard would have silently
  revoked an exception nobody had recorded; #257 widened it to every file in `specs/` only
  after #142 had named the exception.
- **Never modify plugin code, hooks, scripts or skills.** Filing the issues is the
  deliverable; implementing them is the job of `/implement-github-issue` *(user level)*.
- ⛔ **(INV-314) Filing is outward-facing and immediate. Show the maintainer every title and body and
  get an explicit yes first** (Step 7), or one yes for the whole list shown in one message
  (INV-314, 2026-10-13 note), under the conditions in
  `.claude/skills/feedback-to-issues/drafts.py` → "The batch yes". An issue is visible to anyone
  watching the repository the moment it is created; it can be edited or closed, never un-filed, and its
  notifications have already gone out. This is the same gate Step 8 applies to
  `submit_feedback`, for the same reason, except that there each message takes its own yes.
- **"The server can answer it" is not by itself a reason to delete anything.** It is
  the entry ticket to Step 6, where delegation has to earn its place. A large fraction
  of legitimate findings end in *keep* — record those too, or the next run re-litigates
  them.
- **Re-ask the server this session, for every fact.** Never carry a Senzing fact from
  the plugin, from a spec, from the ledger, or from training data into a recommendation
  (INV-080). The ledger records what was true at a version; it is not a source.
- **Delegation done badly is worse than duplication.** A paragraph replaced by "ask the
  MCP server" — with no tool, no parameters, and no statement of what to extract — is a
  regression, not a cleanup. Every `delegate` issue names the call.
- **Never propose deleting or renumbering an invariant.** `specs/INVARIANTS.md` is
  append-only; a superseded invariant is *marked* superseded (see Step 5, verdict
  `retire-workaround`).
- **Deduplicate against the tracker and the ledger before filing.** ⛔ **Search closed
  issues too** — re-filing something decided against wastes the decision, and a closed
  issue often records *why*. Where an item is already filed, reference or update that
  issue rather than opening a second one.
- **Respect the invariants.** Every generated issue references `@INVARIANTS.md`. A
  delegation that would break cross-platform behavior, language-agnosticism, or an
  offline guarantee is not a valid recommendation.

## Step 1: Record both of the server's versions, and what it now covers

**Do this first, before looking at anything; it is not optional.** Every ledger comparison
is against these two axes, and a run that skips them cannot tell an expired decision from a
current one.

The server moves on **two independent axes**, and a sweep that tracks only one will
skip exactly the rows the other changed. Get both:

```text
get_capabilities()                          → server_info.server_version   e.g. 1.32.2
search_docs(query='entity specification')   → metadata.index_built         e.g. 2026-07-29 11:11 UTC
```

- **`server_version`** versions the MCP server software — its tools and their schemas.
- **`index_built`** versions the **documentation corpus** those tools answer from
  (`search_docs` returns it in `metadata`, alongside `documents_indexed`).

Senzing can rebuild the index — new content, corrected content — and ship no server
release. `search_docs` then starts answering differently while `server_version` sits
still, so any query issued for `index_built` also serves as a live check that the corpus
is reachable. Record both; every verdict is stamped with both.

Neither is the Senzing SDK version. `get_capabilities` reports `senzing_version` as the
string `"current"`, not a number — the server does not pin a Senzing product version, so
"verified against 1.32.2" never means "holds for engine version X" (INV-169).

Also take from `get_capabilities`:

- **The coverage manifest** — tool list, coverage areas, `suggested_workflows`. A
  coverage area that is new since the last run is the highest-yield place to look,
  because it is precisely where the plugin was most likely filling a gap.
- **`llm_instructions.common_confabulations`** — the server's own list of what it
  expects to be got wrong. Any plugin text near one of these is worth reading closely.

Compare against the ledger's most recent stamps:

```bash
python3 .claude/skills/delegate-to-mcp-server/coverage_ledger.py summary
```

If **both** axes are unchanged since the last run, say so up front. The run is then
limited to sites never examined at all — a server that has moved on neither axis cannot
have started serving anything new, and re-asking it produces the same answers at the
cost of a lot of calls.

## Step 2: Build this run's re-check list

Four sources, in priority order. Take them all; they overlap and the overlap is cheap.

**The argument bounds the run.** With no argument, build the list from all four sources and
bound the inventory at Step 3, as item 4 says. With an argument naming an area or category,
take that as the bound, and say so in the Step 10 report, so the next run knows what was left.

1. **Ledger rows stamped with a different server version or docs index** — decisions
   that may have expired (any difference on either axis, not only a newer one: a
   rollback re-opens them too):

   ```bash
   python3 .claude/skills/delegate-to-mcp-server/coverage_ledger.py \
     stale --server <version> --index "<index_built>"
   ```

   Pass both. With `--index` omitted the index axis goes unchecked, and the command
   says so on every path rather than reporting a clean bill (INV-163) — but a partial
   result relayed as a clean one is how a re-indexed corpus gets skipped.

   `keep-server-lacks-it` rows are the most valuable re-checks in the whole run: each
   one is a gap the plugin is paying to fill, and the server closing it is exactly what
   this skill exists to catch.

2. **New coverage areas** from Step 1's manifest, mapped to the plugin text that covers
   the same ground.

3. **Plugin text changed since the last run**, which has never been examined:

   ```bash
   git log --since=<last run date> --name-only --pretty=format: -- source/ | sort -u
   ```

4. **The un-ledgered surface** — everything Step 3 finds that has no ledger row yet. On
   a first run this is the entire inventory; bound it (Step 3) rather than trying to
   finish it in one pass.

## Step 3: Inventory the Senzing-fact surface

Run the inventory helper, which greps the categories below and prints `file:line` hits
grouped by category:

```bash
python3 .claude/skills/delegate-to-mcp-server/coverage_ledger.py inventory
```

It is a **lead generator, not a verdict** — regex cannot tell a cached authority from a
worked illustration. Read every hit before classifying it.

| Category | What it looks like | Owning tool |
|---|---|---|
| Attribute / mapping rules | `NAME_ORG`, `RECORD_TYPE`, feature tables | `search_docs(category='data_mapping')` |
| SDK method shapes | signatures, argument types, per-binding names | `get_sdk_reference(topic='parameters', language=…)` |
| Engine flags | `SZ_*` literals, "applies to" claims, flag families | `get_sdk_reference(topic='flags')` |
| Response shapes | field names inside a returned document | `get_sdk_reference(topic='response_schemas')` |
| Error codes | `SENZ####`, symptom→cause text | `explain_error_code` |
| Install / config | package names, env vars, paths, platform commands | `sdk_guide(topic='install' \| 'configure')` |
| Export / reporting / graph | SQL, export flags, data-mart schema | `reporting_guide(topic=…)` |
| Scaffold code | inlined snippets the plugin ships | `generate_scaffold` |
| Sample data | dataset names, sources, record shapes | `get_sample_data` |
| **Invariants asserting a server limitation** | `specs/INVARIANTS.md` prose about what the server cannot do | whichever tool owns the claim |

The last row is the highest-risk category in the repo and is easy to skip because it is
not in `source/`. An invariant that says the server *cannot* do something is pinned by
tests, cited by specs, and shapes future work — so when the server gains the ability,
the false premise is load-bearing in a way ordinary stale prose never is. Sweep
`specs/INVARIANTS.md` on every run.

## Step 4: Ask the server whether it owns the fact

For each site, call the tool that **owns** the fact — not `search_docs` for everything.
A flag's `applies_to` is authoritative under `topic='flags'`; prose that mentions the
flag is not.

Ask two questions, and record both answers:

1. **Does the server answer this at all?** — coverage.
2. **Does it answer it the same way the plugin does?** — agreement.

Quote what came back rather than paraphrasing it, so a later reader can tell the
server's words from yours. Where the server cannot reach a fact — a field name below
the shape `response_schemas` documents, a value only a live engine returns — that is
`keep-server-lacks-it` with the reason recorded, never a laundered MCP citation
(INV-080/INV-149).

## Step 5: Classify each site

Exactly one verdict per site. The ledger accepts these six and nothing else.

| Verdict | Means | Produces |
|---|---|---|
| `delegate` | Server answers it, and Step 6 says a runtime call is an improvement | An issue |
| `contradicted` | Server's current answer differs from the plugin's | An issue — **urgent** |
| `retire-workaround` | Plugin mitigates a server defect that no longer reproduces | An issue |
| `keep-server-lacks-it` | Asked; the server has no answer | Ledger row (+ optional Step 8) |
| `keep-by-design` | Server answers it, but Step 6 says delegating would regress | Ledger row, with the named reason |
| `not-a-senzing-fact` | Bootcamp pedagogy, ordering, wording, plugin mechanics | Nothing — out of scope |

Three of these need care:

**`contradicted` is a defect, not a cleanup.** The plugin is shipping a wrong Senzing
fact today. File it at high priority and do not batch it with tidy-ups. Before filing,
apply INV-169: most apparent contradictions are two different conditions, not a
disagreement. If the plugin's claim holds under a flag set, binding, SDK version or
platform the server's generic answer does not cover, that is `keep-by-design` with the
conditions recorded — flattening the two into one absolute is a mistake this repo has
had to retract twice.

**`retire-workaround` usually touches an invariant.** Workarounds here are pinned:
INV-160 (a `find_examples` retrieval returning empty `content` alongside a non-zero
`content_length` is a failed retrieval) and INV-173 (a validation gate that cannot
represent a legitimate input) both encode server behavior. When such behavior is
fixed:

- **Never delete or renumber the invariant.** Per `INVARIANTS.md`'s own rules, propose
  appending a superseding note — "(superseded by INV-NNN)" or a dated "no longer
  reproduces as of server X" clause — and a *new* invariant if the rule genuinely
  changed meaning.
- **Name the tests that pin it.** They will fail, and the issue must say which and what
  they should assert instead.
- **Prove the fix, don't infer it.** One passing call is not proof a defect is gone —
  reproduce the original failing conditions as closely as the environment allows, and
  where it cannot be reproduced at all, say so and leave the workaround in place. A
  workaround removed on a false all-clear fails in front of a Bootcamper.

**`keep-by-design` must name its reason.** An unreasoned keep is indistinguishable from
"nobody looked", and the next run will look again.

## Step 6: Test whether delegation is actually an improvement

Only for sites the server covers. **All six must pass** before the verdict is
`delegate`; the first failure decides `keep-by-design` and names the reason.

1. **Can the call be made there?** Some steps run with no network guarantee, and the
   plugin has deliberate offline paths. A fact needed inside one cannot be delegated.
2. **Does the answer arrive usable?** If the step would have to re-teach, filter or
   reinterpret a long generic response to get the sentence it needs, the plugin is
   adding value, not duplicating.
3. **Is the plugin's version narrower on purpose?** A generic server note that the
   Bootcamp has already *measured* for this installation must stay suppressed in favor
   of the measured value (INV-150). Delegating re-introduces the noise.
4. **Does an invariant require the text at that step?** INV-183 requires a step that
   generates an artifact to name every governing rule *at that step*, not one file away.
   Where an invariant mandates local presence, the duplication is the requirement.
5. **What happens when the call fails?** Delegation makes the step depend on the call.
   INV-125 requires the fallback to preserve the primary path's quality gates — the issue
   must say what the fallback is, or there is no delegation.
6. **Does it cost the Bootcamper a visible turn for nothing?** Agent-side apparatus is
   free; a round-trip the Bootcamper waits through to be told something the flow could
   have stated is friction (INV-012).

One pattern deserves recognizing rather than deleting, because it already does the right
thing. `module-05-data-quality-mapping/phase1-quality-assessment.md` inlines a table of
which features apply to `PERSON` vs `ORGANIZATION`, and labels it: verified against a
named server version on a named date, explicitly **partial**, and followed by "re-read
it for the source you are assessing rather than trusting this table — it is an
illustration of *how the specification marks type*, not a substitute for asking". That
is a worked illustration of a method, not a cached authority. Deleting it would remove
teaching and keep nothing. The correct handling is `keep-by-design` plus re-verification
of the dated claim — and where a site holds a cached authority, this is the shape to
convert it *into* when full delegation fails Step 6.

## Step 7: File the issues

One issue per coherent change, using `issue-template.md` in this skill's directory.
Group sites that share one fix; keep unrelated ones apart.

⛔ **(INV-314) Show the maintainer every title and body, and get a yes, or
one yes for the whole list shown in one message (INV-314, 2026-10-13 note), under the conditions
in `.claude/skills/feedback-to-issues/drafts.py` → "The batch yes", before filing.**
Then, for each approved item:

```bash
gh issue create --title "<title>" --body-file <file>
```

⛔ **(INV-319) Never pass `--repo`, and never file anywhere but here.** This is the parent repository;
parent-to-child change travels by **parity**, from a tagged release, so the parent never
files into a child at all. A flag naming another repository is a violation of that rule,
not a convenience: whatever the finding, never pass `--repo`.

⛔ **(INV-318) Never apply the `unattended-ok` label to an issue this run files.** A sync that
labels its own findings lets `/unattended-issue-loop` *(user level)* retire plugin content with
nobody choosing to. Choosing what runs unattended is the maintainer's decision alone.

**Record each issue number as you go** — Step 9's ledger rows and Step 10's report both
need it.

⛔ **(INV-368) With `--draft <run-dir>`, this run files nothing, fixes nothing and sends nothing, and writes
nothing outside `<run-dir>`.** Each issue, Step 8 message and Step 9 row becomes a
[`drafts.py`](../feedback-to-issues/drafts.py) `add` record instead, carrying its row's `record`
arguments as `--after` and `--after-struck`, and the run ends with `drafts.py list`. `--draft` is
the release cycle's interface (#573), and the caller records unresolved drafts (INV-317). **With
`--file <run-dir>`**, file what `drafts.py file-plan` prints, after a yes for each record or one yes
for the whole list shown in one message (INV-314, 2026-10-13 note), under the conditions in
`.claude/skills/feedback-to-issues/drafts.py` → "The batch yes"; an upstream draft is never sent
by `--file` and keeps its own yes. Both stages, the manifest and its statuses are stated once in `drafts.py` (INV-300).

Rules beyond the template:

- **Name the call that replaces the text** — tool, parameters, and what to extract from
  the response. This is the whole deliverable of a `delegate` issue.
- **Quote both sides.** What the plugin says now, and what the server returned, with the
  tool, parameters, version and date.
- **Say what stays.** Delegation rarely removes a whole section: the step still needs
  its orientation sentence and its "what to do with the answer". An issue that reads as
  "delete lines 40-60" will be implemented that way.
- **Name the tests that will fail.** Plugin content is pinned by tests across `tests/`;
  an issue that removes text without saying which assertion goes with it will be reverted
  by a red suite.
- **Give the acceptance criteria a re-verification clause** — the implementer re-asks
  the server before changing code (`/implement-github-issue` *(user level)*, INV-080), and the criterion should
  say what answer they must get for the change to remain correct.
- ⛔ **Any absence claim carries `owner-checked:` (INV-213).** Where a finding rests on the
  server *lacking* something — a `keep-server-lacks-it` verdict, "returns no X", "does not
  cover" — the `MCP evidence` line MUST also name the route that would **carry** that fact
  and what it returned. ⚠️ **This binds harder here than anywhere else in the repository**,
  because this skill's entire subject is what the server does and does not cover: an absence
  concluded from the wrong route becomes an instruction deleted from the plugin and from four
  child ports. The tools you asked and found empty are true statements about *those tools*
  and no evidence for the negative. Enforced by `tests/test_spec_absence_claims_name_their_owner.py`.

## Step 8: Send the gaps upstream

The `keep-server-lacks-it` rows are, collectively, a list of things Senzing's MCP server
could serve and does not. Reporting them is how the server gets smarter, which is the
only thing that shrinks this plugin's maintenance surface for good — so this step is
part of the job, not an afterthought.

Follow `feedback-to-issues` Step 8's rules exactly, with one difference: these are
coverage gaps, so the category is usually `feature` rather than `bug`.

- Draft it as something Senzing can act on without context from this repo: what was
  asked, which tool and parameters, what came back, and what was needed instead.
- Strip everything identifying. Describe data shape, never data. No paths, hostnames,
  employer, or dataset contents.
- **(INV-314) Show the maintainer the exact message and get an explicit yes before sending.**
  Then `submit_feedback(category='feature', message='<approved text>')`.
- ⛔ Never send under `category='license_request'` (INV-135).
- Record the outcome on the ledger row so the next run does not re-file it.

## Step 9: Record every verdict in the ledger

**Every site examined gets a row — including the keeps.** A run that records only the
sites it filed throws away most of its work, and the next run pays for it again.

```bash
python3 .claude/skills/delegate-to-mcp-server/coverage_ledger.py record \
  --key <stable-slug> \
  --where <path/to/file.md> \
  --claim "<one line: what the SBCP asserts or holds here>" \
  --verdict <delegate|contradicted|retire-workaround|keep-server-lacks-it|keep-by-design|not-a-senzing-fact> \
  --reason "<required for keep-by-design; the Step 6 test that failed>" \
  --server <version> \
  --index "<index_built>" \
  --tool "<the call that established it>" \
  --issue <the number filed in Step 7, e.g. 142>
```

With `--file <run-dir>`, run `record` once per line `drafts.py after` prints.

The ledger is `specs/mcp-coverage.jsonl`, append-only and read last-wins, so a verdict
is revised by appending a new row with the same key — never by editing history.

⚠️ **29 historical rows carry a `spec` field instead of `issue`**, from the runs before this
skill filed issues (#114). They are read and displayed unchanged: rewriting them would edit
history, which this ledger's whole shape forbids. A row carries one or the other, never both. The key
is a **stable slug describing the claim**, not a path: files move and line numbers
churn, and a decision keyed to a location is lost the moment the file is reorganized.

**Record `--index` even though it is optional.** A verdict with no index provenance
cannot be proved current against a later re-index, so it expires on the next check that
supplies one — the work is redone rather than lost, but it is still redone.

## Step 10: Report

State **both** stamps — server version and docs `index_built` — and which of them moved
since the last run. "1.32.2, unchanged" and "1.32.2, corpus re-indexed since the last
sweep" call for completely different amounts of trust in the previous run's keeps. Then
a table:

| Site | Category | Server says | Verdict | Action |
|---|---|---|---|---|
| `<key>` | flags | `applies_to: [...]` — same as the plugin | `delegate` | Filed → #<n> |
| `<key>` | error codes | now documents SENZ#### | `retire-workaround` | Filed → #<n> (INV-### superseded) |
| `<key>` | response shapes | no coverage below the top-level shape | `keep-server-lacks-it` | Ledger only; upstream `feature` sent |
| `<key>` | mapping | answers it, but needed offline at that step | `keep-by-design` | Ledger only |

Then, in this order:

1. **Anything `contradicted`, first and separately.** The plugin is shipping a wrong
   Senzing fact right now; it should not arrive at the bottom of a cleanup report.
2. The issues filed, as `#<n>` with their titles.
3. **What the server started covering since the last run** — the headline result of a
   periodic run, and invisible unless stated.
4. **What is still uncovered**, and which of those went upstream.
5. **Coverage of the sweep itself**: how much of the inventory was examined and what was
   left, so a partial run is never mistaken for a clean bill of health. Name any site whose
   owning tool could not be reached: a gap disclosed is a finding, and a gap skipped silently
   is a false clean bill of health.

Do not implement the issues. Offer `/implement-github-issue` *(user level)* as the next step.
