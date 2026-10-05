---
name: padosoft-knowhow-harvest
description: >-
  Use this skill to turn what other repositories have learned into skills — a periodic harvest of their
  lessons files, rule folders, internal skills, decision records and security docs, deciding for each
  finding whether it updates an existing skill, becomes a new one, or is deliberately left alone. Also when
  the user says "check the repos for new rules", "harvest the know-how", "what changed since last time",
  asks how to keep the catalogue current, wants to know whether something was already considered, or asks what to do with the local
  rules a skill now duplicates. It
  covers the work order, the judgement that turns a finding into a rule, the promotion criterion, and the
  ledger that stops the same material being mined twice. Do not use it to write a single skill from scratch
  (padosoft-skill-creator) or to audit an existing one.
license: MIT
compatibility: >-
  Requires the repository's `harvest.py` (in its `scripts/` folder) and read access to the source repositories. The
  sources and the ledger live in gitignored files, because a list of the repositories you run is metadata
  about your business.
metadata:
  version: 0.2.0
  author: Padosoft
  summary: Harvest the rule, leave the story, and record what you decided so nobody mines it twice.
  profiles: core
  scope: global
  repository: https://github.com/padosoft/skills
  keywords: harvest, lessons, rules, catalogue, maintenance, promotion, ledger, know-how, periodic
---

# Know-how harvest

Every repository you run accumulates hard-won rules — in a lessons file, a rules folder, decision records,
an internal skill. They stay there, benefiting one project. This is the loop that moves them into the shared
catalogue **without** re-reading everything every time, and without losing the record of what was decided.

**The rule: harvest the rule, leave the story, and write down what you decided — including the rejections,
because an undocumented rejection is re-mined every six months.**

---

## 0. Setup, once

```bash
cp .harvest-sources.example.json .harvest-sources.json   # then fill in your paths
```

Both that file and `.harvest-ledger.json` are gitignored on purpose: **a list of the repositories you run is
metadata about your business**, and this repository is public. If more than one person harvests, keep them
in a private companion repository or a secret rather than committing them here.

## 1. The work order

```bash
make harvest                 # or: python3 scripts/harvest.py scan
python3 scripts/harvest.py scan --id monolith       # one source
python3 scripts/harvest.py scan --json              # to drive another tool
```

It prints four groups, and the current catalogue to match against:

| Group | What it means |
|---|---|
| **New** | never considered — the bulk on a first run, a trickle afterwards |
| **Changed** | reconsider; the work order says what you decided last time |
| **Gone** | the source file is gone — check whether a skill still rests on it |
| **Unreadable** | too large to read in one pass. Split it or exclude it **deliberately** |

The problems section is part of the output, not a warning: a source path that no longer resolves is a
finding. A harvest that silently skips a repository reports a clean catalogue — see
**`padosoft-evidence-boundaries`**.

**The scan never writes to the ledger.** A session that dies half way must not leave everything marked as
processed.

## 2. Read for the rule, not for the change

For each finding, open the file — for a changed one, the **added** material is what matters. Then ask, in
this order:

1. **Is it a rule, or is it a note?** A rule states what goes wrong and what prevents it. A dated progress
   entry, a local path, a vendor version, a review comment is a note: it was true for that repository on
   that day and carries nothing.
2. **Would the agent get it wrong without it?** If the model already does the right thing unprompted, the
   rule adds context and not quality. That is the filter that keeps the catalogue small enough to be read.
3. **Is it project-specific, or a class of defect?** *A named table must be registered in the resolver* is
   specific; *a resolver that returns its input unchanged makes an incomplete registration
   indistinguishable from a no-op* is the class. Harvest the class.

Most findings fail one of the three. That is normal, and saying so explicitly is the point of the ledger.

## 3. The four outcomes

| Outcome | When | What you do |
|---|---|---|
| **Extend an existing skill** | the class already has a home | add the section; bump the version; say which skill in the ledger |
| **Create a new skill** | a coherent domain nothing covers | **`padosoft-skill-creator`**, then register it in a package |
| **Promote to global** | see §4 | move to `core`, state the boundaries in the description |
| **Reject** | a note, already covered, too specific, or the agent gets it right anyway | record it **with the reason** |

Default to extending. A new skill that overlaps an existing one makes both trigger worse, and the
description is what pays the price.

## 4. Promotion is decided by independent convergence

A rule belongs in `core` when **stacks that share no line of code arrived at it on their own**. Not when it
feels important, not when it appears in the biggest repository — when two or three unrelated sources
produce it independently.

```bash
python3 scripts/harvest.py status     # shows how many sources feed each skill
```

That count is the evidence. There is no cap: if four sources converge on a fifth rule, it gets promoted.
And a global skill's description must state its boundaries, because it loads into every session — the repo's
own tests enforce that.

## 5. Strip the provenance, always

The source repositories are private; this one is not. Everything in
**`padosoft-skill-creator` §2** applies, and the gate runs before the commit:

```bash
make privacy
```

No dates, no customer or brand names, no people, no real tables, hosts or identifiers, no error messages
copied verbatim, no ticket or change numbers. **Keep the rule, drop the story** — and where a lesson only
makes sense with its story, the class of defect underneath it usually makes sense on its own.

## 6. Record every decision

```bash
python3 scripts/harvest.py record "monolith|docs/LESSON.md" covered --skill padosoft-query-performance
python3 scripts/harvest.py record "api|.claude/rules/rule-x.md" rejected --note "product-specific: names its own tables"
python3 scripts/harvest.py record "mobile|.claude/skills/y/SKILL.md" pending --note "good, needs a second source before promoting"
```

`covered` requires a skill and `rejected` requires a reason — enforced, because a bare "done" is what makes
the next harvest re-read the same four hundred lines. `pending` is a legitimate state: a rule worth having
that is waiting for a second independent source.

## 7. Close the loop

`make catalog && make all`, update the changelog, commit, tag, release. Then state the numbers: sources
scanned, findings, what was extended, what was created, what was rejected and why. A harvest that produced
nothing is a valid outcome **and it is still recorded**, so the next one starts from the right place.

## 8. After the harvest: the source and the skill are two layers, not two copies

This is the part that decides whether the whole loop is worth running. You harvested a rule **out of** a
repository, and now you install the package **into** that same repository. Without a further step you have
the rule twice: the agent loads both, they cost context, and the day the skill improves they disagree.

They are not duplicates. They are two layers:

| Layer | Holds | Lives in |
|---|---|---|
| **The skill** | the class of defect — what goes wrong, why, what prevents it | the package, one copy for every project |
| **The local rule** | the binding — what that class means *here*: the table, the helper, the path, the documented exception | the repository |

So the step after installing is to **thin the source, not delete it**. A four-hundred-line rule becomes
twenty lines that name the skill and keep only what is true about this repository.

```bash
python3 scripts/harvest.py adopt --id <source>     # exactly which files, and into which skill
```

```markdown
<!-- .claude/rules/rule-database-design.md, after adoption -->
# Database design — local binding

The general rule is **`padosoft-database-design`** (installed with the `data` profile).
This file only records what is specific to this repository.

- Index naming here is `idx_<abbrev>_<col>_<col>`.
- The partition key helper is `App\Support\PartitionKey`.
- Migration guards go through `App\Support\SchemaGuard`, not inline checks.
- **Documented deviation:** the archive tables keep a redundant single-column index,
  because the reporting tool cannot use a composite prefix. Revisit when it is replaced.
```

Delete it outright only when nothing project-specific is left. Keep the full local copy only in a repository
that cannot install the package at all — and write down that this is why.

### Precedence, so a disagreement is never silent

**The skill is the default. The local file may narrow it, add to it, or override it — and an override
carries a written reason.** A local rule that contradicts a skill without saying so is a bug in one of the
two: either the project is a genuine exception (say so, in the binding) or the skill is wrong (fix the
skill, for everybody).

### Starting a new project

Install the profiles and **write no local rules at all**. The rules folder starts empty and grows only with
bindings — a local file appears the first time this project needs to say something the general rule cannot
know. That is also the honest test of whether you needed it.

### Adopting in a project that already has rules

Once, per repository, in this order:

1. **Install** the profiles it needs.
2. **Take the adoption list** above. For every file the ledger says is covered: thin it to its binding.
3. **Leave what is not covered.** Those are candidates for the next harvest, not debt.
4. **Resolve the contradictions explicitly.** A local rule that says the opposite of a skill is the most
   valuable thing the adoption finds: one of the two is out of date, and until now nobody knew which.
5. **Thin the derived instruction files too** — the copies for the other agents. Thinning one and not the
   others is how you create the disagreement that
   **`padosoft-agent-instructions-sync`** exists to prevent.

Do it repository by repository, not all at once. Each one takes an hour and removes a source of drift
permanently.

---

## Gotchas

- **The biggest file is usually the poorest.** A long lessons journal is mostly environment notes and review
  chatter; the density is in the rule folders and the decision records.
- **A rule with an identifier that nothing enforces means the control exists today and nothing protects it
  tomorrow.** Worth harvesting, and worth saying so.
- **Two sources with the same rule word-for-word are one source.** Shared ancestry is not convergence; check
  whether one was copied from the other before counting it twice.
- **The interesting material is often outside the rules folder** — a security directory, decision records,
  a runbook. Adjust the globs per source once, rather than assuming the default found everything.
- **A deleted source file does not mean the rule is wrong.** It means nothing in that repository defends it
  any more, which is itself worth knowing.
- **Re-running the scan after the work but before recording** shows the same findings. That is correct, and
  it is the reason `record` exists as a separate step.

## Checklist

- [ ] Sources file current; every path resolves (problems section empty)
- [ ] Work order read in full, including the *gone* group
- [ ] Each finding judged: rule or note · would the agent get it wrong · class or instance
- [ ] Extending preferred over creating; overlap with existing descriptions checked
- [ ] Promotions justified by independent convergence, counted rather than felt
- [ ] Provenance gate green before committing
- [ ] Every finding recorded — covered with its skill, rejected with its reason, pending with what it waits for
- [ ] Catalogue rebuilt, checks green, changelog written, release tagged
- [ ] Adoption: every source file now covered by a skill thinned to its binding, derived instruction files included

## Final report

```
Harvest <date> — sources <n> · files read <n> · findings <n>
Extended: <skill> ← <source|file> (<what the rule is>)
Created:  <skill> ← <sources>
Promoted: <skill> — converging sources: <n> (<which>)
Rejected: <n> — <the categories, with an example each>
Pending:  <n> — waiting for <what>
Provenance gate: clean
Release: <tag>
Adoption pending: <source> — <n> files still holding a full copy
```
