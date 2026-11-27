---
name: evidence-boundary-discipline
description: >-
  Revise a knowledge page, company profile, monitoring delta or delivery table without overstating
  cited sources. When a source describes a plan, is silent or conflicts with another entry, align
  tense to the dateline, match provenance labels and cite factual paragraphs without inferring
  absence. Not for official-document-verification.
metadata:
  revision: "6"
  areas: "work-management"
  targets: "runtime-agnostic"
  summary: "state only what a dated source supports: tense to dateline, provenance-label parity, absence never escalates"
  summary_zh: "只陈述有日期的来源所能支持的事实：时态对齐日期、来源标签全链路一致、缺失不升级为不存在"
  kind: "entry"
---

# Evidence boundaries for claims built from reported sources

## When to Use

- Writing or revising a knowledge page, monitor delta, entity/concept section, or delivery table whose
  claims rest on news reports, press releases, partial legal text, or sources read in an earlier round.
- A reviewer returned a page or candidate with "this overstates what the source says".
- For the mechanics of a rejected-candidate round (versioned patches, immutability, numstat reporting),
  pair this with the project's own revision-candidate procedure.

The rule underneath everything here: a page states what a named source said at a dated moment, and never
what the world is like now unless a later artifact was actually read.

## 1. Fix the tense to the dateline

A source writing `will be developed in the coming weeks` records a plan as of that report. Days later it does
not license "still not formed", "not public yet", or "no draft exists". Write:

> The report of <date> records a pre-session drafting plan (the original uses the future tense); as of this
> cutoff no text was obtained and the current completion/public state is unknown.

A negative that was true when the source wrote it ("no checkable text before the session") is a statement
about that moment, not a standing property of the artifact.

## 2. Hold one provenance label across all surfaces

| Surface | Carries |
|---|---|
| page body (bullet, table row) | fact / report / judgment / unknown |
| delivery or evidence table | same label, plus re-read-this-round vs attributed |
| runtime receipt / log | run summary only, never a research conclusion |

If the delivery table says a source was not re-read this round, the page cannot call the item `fact` with no
locator. Preferred fix: keep the Fact and tag the boundary in place — `fact; carried from the first run's
in-page citation; not re-verified this round; attributed this round`. Deleting previously verified facts is
not required; silently upgrading an unrechecked item to Fact is the defect.

Labels are the project's vocabulary (`EVIDENCE_ATTRIBUTION_LABEL`, `EVIDENCE_RECHECK_LABEL`); the parity
rule is universal even when the words differ.

## 3. Every new factual paragraph carries its own citation

- Full clickable URL, version/date, locator (section, paragraph, figure, line), short verbatim quote.
- A wikilink to a sister page, a media name, or a bare domain is not a citation; the backlink supplements.
- Sections appended to a concept or entity page are read standalone. Give them the same citation set even
  when the sibling query page already holds the full ledger.

## 4. Absence never escalates

| Observed | Allowed | Forbidden |
|---|---|---|
| searched this version, nothing found | "not found in the version read on <date>" | "does not exist", "no channel" |
| visible actions happened in forum A | "this round's visible action was in A" | "there is no pathway in B" |
| no text obtained yet | "not obtained this round; status unknown" | "unobservable until <event>" |
| field not queried, access blocked, or zero records searched | "not queried; value unknown" | `0`, "none", "never came up" |
| only a search snippet or preview read | "preview shows the <date> entry; latest state unread" | "current status is …", "no reply was sent" |
| item in an earlier export missing from a newer one, with no closing record | "absent from the <date> export; outcome not recorded" | "completed", "won", "retired" |

The last three rows adapt [knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)
(Apache-2.0) `small-business/shared/absent-is-not-zero.md` and the `sales/` skill rules.

A monitoring window closes on its stated end date or an explicit retirement decision, never early because the
evidence looks thin. When a later artifact might exist, say what you searched and when, not what cannot exist.

## 5. Read the definition before mapping an observation onto it

- A sub-criterion requiring sustained multi-year output, durable instruments, or shaped great-power conduct
  is neither satisfied nor refuted by a single announcement.
- An actor class defined as "moderate-material-weight, non-great-power" does not require the usual cohort;
  "the author is not the group this page normally covers" is therefore not a counterexample.
- A method label (`codification`, `implementation`, `pilot`) does not prove equivalence with, or independence
  from, the prior arrangement. Name the level (bill section vs proposed code subsection) and say what was not
  compared.

## 6. Self-check before delivering

Run the checks with the project's own retired-qualifier list and page set:

```bash
# every banned qualifier the reviewer retired, including softened variants
grep -n -f "${EVIDENCE_QUALIFIER_FILE:?set the retired-qualifier list}" <candidate pages>

# each appended section must show its own external source
grep -c "https://" <appended-section-range>

# label parity: rows marked attributed in the receipt must appear tagged on the page
grep -n "${EVIDENCE_ATTRIBUTION_LABEL:-attributed}\|${EVIDENCE_RECHECK_LABEL:-not re-read}" <page>
```

The qualifier file is content, not a hard-coded policy: when a reviewer retires a new phrase, append it
there so the next round's grep catches the softened variant too.

Report as separate lines what was read this round, what is attributed from an earlier round, and what could
not be obtained from this client/path/date. Reviewers accept the latter two when labelled and reject a flat
list that hides which is which.

## Configuration

| Key | Env | Default |
|---|---|---|
| `page_glob` | `EVIDENCE_PAGE_GLOB` | none — the pages named by the delivery table |
| `receipt_path` | `EVIDENCE_RECEIPT_PATH` | none — the project's delivery/evidence table |
| `qualifier_file` | `EVIDENCE_QUALIFIER_FILE` | none — must be supplied per project |
| `attribution_label` | `EVIDENCE_ATTRIBUTION_LABEL` | `attributed` |
| `recheck_label` | `EVIDENCE_RECHECK_LABEL` | `not re-read` |
| `qualifier_pattern` | `EVIDENCE_QUALIFIER_PATTERN` | none — prefer the file; a pattern is the fallback |

Resolution order and the config-file path are defined in
[references/configuration.md](references/configuration.md);
this skill does not restate them.

## Pitfalls

- Restating an older future-tense plan as present status; the invented observation is what gets rejected.
- Marking a claim Fact on the page while the delivery table calls it attributed.
- Appending an observation whose only citation is a sister-page wikilink and a media name.
- Treating one event as satisfying or refuting a sub-criterion that requires sustained output or a named actor class.
- Letting a run summary in a log or receipt carry a research conclusion that later rounds then inherit.
- Quoting the reviewer's rejected formulation inside a "not established" list without marking it as withdrawn,
  so a later grep cannot tell assertion from retrieval.
