---
name: spec-driven-domain
kind: pattern
rule: spec-driven
description: Pattern of rule spec-driven. Load when creating or editing a domain spec in docs/specs — the mandatory sections, the scenario form, binding a rule to code, the order of work from spec to code. Not for creating a law, a rule or a pattern — that is pattern spec-driven-rule.
---
<!-- rt-kit v0.34.0 · patterns/spec-driven-domain.md · 851d6319feaf · правится надстройкой, не здесь -->

# Domain spec

Pattern of the rule `spec-driven`. What must be true — the law
`docs/constitution/project-documentation.md`.

## When to use

- A new domain or a feature in `proposed/` is created.
- A `.proto` is edited — the specs of the touched domains go in the same branch.
- A divergence between a spec and the code was noticed.

## Layout

```
docs/specs/<domain>/
    spec.md              — how the domain works
    implementation.md    — the table "rule → file:symbol"
    scenarios.md         — scenarios SC-<PREFIX>-<NUMBER>
    <subdomain>/         — its own spec.md, implementation.md and scenarios.md
    proposed/<feature>/  — only what does not exist yet
```

The template is `docs/specs/_template/spec.md`, the index with prefixes is `docs/specs/README.md`.

A subdomain is asked the same as a domain: the same mandatory sections, the same companion next
to it, the same link between scenarios and tests. A domain with half its subdomains described and
half created as empty directories is never green.

Work that touched a domain and its subdomain writes two product agreements, not one. A subdomain
has a scenario prefix of its own, and the audit gives no spec a second prefix: the scenarios of
such work part into two numberings — one per spec they will merge into. The plan names both, and
they merge apart, each into its own spec.

The place of an agreement is chosen by the length of the spec it will merge into, at the moment it
is written. The domain spec plus the agreement's rules is measured against the tree's size limit;
one that would cross it is written from the start as the agreement of a new subdomain, with its
own scenario prefix. Measured only at the merge, the overrun moves a finished agreement to a new
place and a new prefix, together with the test titles that carry its numbers.

## Mandatory sections

`## Зачем` · `## Терминология` with the subsection `### Как это называется в интерфейсе` ·
`## Правила` · `## Что не входит` · `## Контракт` with the subsection `### Коды отказов` ·
`## Данные` · `## Экраны и состояния` · `## Сквозные требования` with four subsections
`### Локали`, `### SEO`, `### Мобильная раскладка`, `### Мультиобъектность` · `## Решения` ·
`## Открытые вопросы` · `## История изменений`.

The heading text is checked verbatim. "Not applicable" is a legitimate answer, a missing section
is not.

`## Решения` is a temporary place. A decision lives in it until the layer it belongs to is found;
the found layer takes it as an item, and nothing stays in the spec. A section that has grown reads
as a sign of a rule not yet created, not as a trait of a complex domain: splitting such a spec by
lines is useless, because what splits in it is not the description of the domain but the unwritten
rule.

**The heading of a decisions-section entry is not a date.** A date says when the decision was
made, while the section answers "why so and not otherwise": a decision cannot be selected or
found by date, yet an entry named by one reads as archive and stays in the spec forever. An entry
starts with the decision itself.

**A statement standing in another section of the same spec is not created as a second rule
item.** The structure of a record lives in the data section, the order of calls in the contract
section, the reason the domain exists in the `## Зачем` section: all three say what the rule would
say. The second copy diverges from the first silently, and there is nothing to notice it by — the
audit knows a rule item against an anchor, and nobody compares two statements about one thing.
The decision at that point leaves the decisions section whole: the place where the requirement
lives is found.

The header carries the status, the revision date, the scenario prefix, the dependencies on other
domains, the `**Законы:**` line — the laws the domain applies — and the `**Процедуры:**` line —
the lib roots whose procedures the domain serves.

```markdown
**Зависимости:** `catalog` (booking request contents), `availability` (date occupancy)
**Законы:** `access`, `locales`, `lists`
**Процедуры:** `libs/api/<domain>`
```

A law named anywhere in the spec text must stand in this line: the link is checked both ways.

## A rule and its binding

A rule is worded so that it can be broken, and starts with a bold phrase:

```markdown
- **One maximum discount is applied.** Adding discounts up gives a price below cost.
```

The binding lives in `implementation.md` next to it, and the key of the link is the rule text
itself:

```markdown
| Rule                             | Where it is carried out                                            |
| -------------------------------- | ------------------------------------------------------------------ |
| One maximum discount is applied. | `libs/api/<domain>/util/src/lib/quote.calculator.ts:calculateQuote` |
```

A rule that found no place in code is an intention: its place is "Open questions" as
`Q-<law letter>-<number>`, not a formal anchor.

## Scenario

```markdown
### SC-BK-19 — confirmation for occupied dates is refused

Given the property has a confirmed booking on overlapping dates
When the owner confirms the booking request
Then the refusal is shown to the owner as occupied dates, not as a database error
```

**"Then" names one outcome.** A wording through "either … or" describes two structures at once,
and the scenario gives no way to learn which one works: it is green under either. A fork is
described by two scenarios with different "Given" — then a change of behaviour fails exactly the
one that stopped being true, instead of passing silently.

The identifier is put at the start of the test title, followed by a dash. A scenario without a
test is marked `Не покрыто: <reason>`, a scenario with an incomplete test — `Покрытие: частичное
— <what is missing>`.

A scenario that cannot be checked by anything at all is not created. The "not covered" mark says
"there is no test yet" and promises one will appear; where no check exists, there is no promise,
and the marked scenario hangs in the suite forever, reads as debt and makes every next reader
find out anew whether it is time to close it. The rule the scenario was meant for stays a rule:
it is held by the line in the companion and the entry in the change history, and that is enough.

The number in the identifier lives like this:

| What happened             | What is done with the number                                                                                |
| ------------------------- | ----------------------------------------------------------------------------------------------------------- |
| a scenario was added      | the next free one is taken — the largest issued **across all branches** plus one, not a gap in the middle   |
| the promise changed       | the number stays, the test title is edited by the same commit                                               |
| a scenario was deleted    | the number stays empty and is not given to a new scenario; the test is deleted with the scenario            |
| the numbers looked worth compacting | they are not renumbered: only the number ties them to the tests, and the run stays green under both edits |

The number is written the same way as its neighbours' in the same file: the audit looks for it by
a pattern, and a number written differently matches neither in the spec nor in the test title.

**A free number is looked for across all branches, not in the main one alone.** Neighbouring work
keeps its numbers on disk and has not reached main yet: six numbers were issued twice this way,
and the work whose agreement was not merged had to move. The number is the only thing tying a
scenario to its test, and issued a second time it leaves the old reference looking right and
leading elsewhere.

This is asked by a tree command, if the tree created one: it reads scenario headings across all
branches — local and remote — and prints the first free number past the largest taken. The
command's name is given by the rule's companion.

## Order of work

1. A task is created by scenarios: what will become true when the work is finished.
2. The domain spec (or `proposed/<feature>/`) is edited **before** the code.
3. The code is written to the scenarios, and the tests are named by their identifiers.
4. `npm run check:specs` — before the push.
5. Acceptance goes by the scenarios, not by a retelling of the edit.

Between steps 2 and 3 `npm run check:specs` is red by design, not by mistake. A scenario without a
test it only lists, but a rule without a binding and a contract row without a procedure it refuses,
and their bindings name code that is not written yet. So a stage that edits the spec names as its
readiness sign the refusal list itself — only the new rules unbound, only the new scenarios under
"no test" — and not exit 0. Exit 0 is the sign of the stage that writes the bound code.

A rule promising a result a person sees is confirmed on the running application, not by
inference from the call graph. Reading confirms headings, the link to bindings and the shape of
data; a rule with nothing to confirm it on leaves as an open question and is not written as a
statement.

## Common misses

- A second table under the contract section: the audit reads every table there as the list of
  procedures, and a set of refusal codes standing next to them comes back as that many
  discrepancies at once — thirty-six on a spec that was right. Under the contract stands the table
  of procedures alone; a set of codes goes into the data section.
- A grown domain is split into new domains instead of subdomains: a new domain has to be entered
  in the index, audited against the code separately and explained as to why it is not a subdomain
  of its neighbour — while a subdomain stays in its domain and inherits its contract. A
  neighbouring domain is created only when the subject lives as an entity of its own. The
  boundary is drawn by the owner: a split rewrites the numbers in all the domain's test titles,
  and it cannot be put back by the same move.
- A count of rules or scenarios in the domain index: it is recomputed at every edit of any spec,
  and a year later most such numbers silently describe the spec of the day before yesterday. The
  index holds the domain, the prefix and one line of "what it is about".
- `tasks.md` in a spec: steps are a session artefact; their place is the branch or the PR
  description.
- A field table copied from the contract: the source is `libs/common/proto/proto/<area>/v1/`,
  and only one of the two compiles.
- Columns and indexes in a spec: they are in `prisma/schema.prisma`, and the spec keeps the rule
  the constraint expresses.
- The place where a rule is carried out inside the rule text: it changes at the first
  refactoring, and `implementation.md` exists for it.
- A `Не покрыто` mark with an existing test is a refusal: the debt was closed, and the mark was
  not removed.
- The `Не покрыто` mark is read verbatim and from the start of the line. Any word between it and
  the colon — `Не покрыто, и прогоном не покрывается вовсе: …` — and the scenario counts as not
  marked at all, and the reason the mark was written for never reaches the PR.
- A law named in the text but forgotten in the `**Законы:**` line: then the law gives no way to
  learn which domains stand on it.
- A `.proto` edit without the specs of the touched domains: `docs-guard` refuses such a commit.
- **A rule inferred from the call graph errs silently.** It reads as confidently as a measured
  one, and the binding audit lets it through — the symbol is in place, it just describes the wrong
  thing. Two rules of one spec turned out inverted: the link went not between the stores but
  through the component listening to them — and both nearly became a task for a defect that does
  not exist.

- **A grown domain splits into subdomains, not into new domains.** A new domain would have to be
  entered in the index, audited against the code separately and explained as to why it is not a
  subdomain of its neighbour; a subdomain stays in its domain and inherits its contract. A
  neighbouring domain is created only when the subject lives as an entity of its own.
- **The largest issued number is looked for across the whole domain by a command, not by eye at
  the tail of the file.** Numbers in the scenarios file are out of order: edits inserted them next
  to their neighbours by meaning, and the last line does not show the maximum. Six new numbers out
  of eleven landed on taken ones — the spec audit caught it, not reading, and the test titles had
  to be rewritten along the way.
- **The boundary between domains is drawn by the owner, not by the author of the next edit.** The
  author sees their edit, not what the subject will grow into: a domain created along the way
  turns out a month later to be half of its neighbour, and parting them means parting the scenario
  numbers too.
- **A changed or removed scenario is edited in the live spec, not restated in `proposed/`.** The
  spec audit refuses a second heading with a taken number. A changed promise or a removed
  scenario goes into the domain's `scenarios.md` by the commit that changes the code and the test
  title; the agreement names such scenarios by number in prose.
