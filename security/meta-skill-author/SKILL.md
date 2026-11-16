---
name: meta-skill-author
description: Use when creating a skill or reviewing its format. Defines the catalogue frontmatter and its real length limits, the two-layer principle/binding anatomy, the five-question portability gate, section order, skill shapes, naming, rule ownership, and which plugin a skill belongs to.
---

# Meta — Skill Author

A skill is **narrow**: it covers one artifact, or one set of artifacts that always arrive together.
Skills are read as reference knowledge; the job is to show how the right file gets written. Uniformity
matters more than expressiveness — a reader who has applied one skill should be able to apply any other.

This catalogue is distributed on the Claude Code marketplace, so a skill is written for someone whose
stack is not yours: state the obligation mechanism-free, then bind it to exactly one concrete stack.

This skill produces one new `SKILL.md`; editing other skills is an audit task.

**Read the sibling `CONVENTIONS.md` in this skill's own directory before writing anything.** It carries
the catalogue's shared placeholder vocabulary (`Foo`, `Bar`, `myapp`, `myschema` and the names derived
from them), the banned vocabulary, the index of what each existing skill covers, the six-plugin
packaging layout, the four skill shapes, and what is deliberately out of scope. Only this file is
loaded automatically; the sibling is not, so open it rather than working from this summary of it.

## When to use vs. neighbours

- Adding a brand-new skill → this skill.
- Editing an existing skill to fix a rule or a template → not this skill; edit the file directly.
- Sweeping cross-references after a rename → not this skill; that is an audit task.
- Deciding which plugin a skill ships in → the packaging table in the sibling `CONVENTIONS.md`.
- Documenting a process rather than an artifact → still this skill; the format adapts (no `Template(s)`
  section, every other section still applies).

## File location

```
skills/<skill-name>/SKILL.md
```

The directory name **is** the skill name. One `SKILL.md` per directory, plus sibling files when needed
(this skill's `CONVENTIONS.md`). A body past ~500 lines takes sibling topic files, and `SKILL.md`
becomes navigation — only when it genuinely does not fit, because only `SKILL.md` is preloaded and a
sibling is reached by an explicit instruction to read it.

## Frontmatter

Two fields are required. Two more are valid, documented and used deliberately. No other field;
information that would need one goes in the body.

```yaml
---
name: <skill-name>
description: Use when <trigger>. <What it owns, second.>
paths: <optional — activation globs>
user-invocable: false   # optional — only where a command drives the skill
---
```

- **`name`** — the skill's name. Keep it identical to the directory name.
- **`description`** — what the skill covers and when to apply it. This is what gets matched to decide
  whether to load the skill, and it is read first, so it carries the trigger.
- **`paths`** — a valid, documented Claude Code field carrying glob patterns that limit when a skill
  auto-activates. Optional, and not restricted to test skills. It **narrows** auto-activation, so a
  too-tight glob makes a skill unfindable in a project whose layout differs slightly. Glob the layer
  directory (`**/domain/**`, `**/tests/**`), never a file name, and prefix with `**/` so the skill
  still fires inside a workspace member. A **universal** skill carries no `paths` at all — it binds
  anywhere, and a glob would suppress it — and neither does a skill that must fire on a greenfield
  project, where the directories it would match do not exist yet (`architecture-choice` is the case).
- **`user-invocable: false`** — hides the skill from the `/` menu; it still loads automatically and
  through the Skill tool. Set only on a skill a command walks the person through — showing a draft,
  taking corrections — where invoked by hand the skill would do the work without them. A gate the
  person must pass is still a rule of the skill, never of the command alone: the skill loads without
  the command. `delivery-spec`, driven by `/pyhouse-delivery:spec`, is the case. A skill whose command
  only walks its decision, with nothing the skill alone would skip, stays in the menu.

`allowed-tools`, `metadata`, `license` and `compatibility` are valid and unused here. Deliberately
**not** used: `disable-model-invocation: true` (blocks automatic loading *and* preloading — hand
invocation only), and `when_to_use` — Claude Code only appends it to `description`, under the same
cap and listing budget, so trigger phrasings beyond the first sentence go at the end of `description`
instead.

### Length

- **`description` truncates at 1,536 characters** in the skill listing. That is the ceiling; a
  description is as long as its triggers and routing need, and no shorter cap applies.
- **The listing has a total budget, a share of the context window** (1% by default,
  `skillListingBudgetFraction`). Past it, the least-invoked skills' descriptions are dropped and only
  their names kept. This catalogue's descriptions come to ~38,700 characters, ~760 a skill, enough to
  pass it. Every character added to one skill's listing is weighed against another skill's description
  being dropped.
- Truncation is from the end, so **the trigger leads**. A description that does not fit is rewritten as
  complete sentences to fit, never cut mid-sentence.

### Description rules

- **Open with `Use when …` — the single opening formula.** Put the trigger first and what the skill owns
  second. The first clause decides whether the skill is loaded, so it carries the trigger: what artifact,
  what situation.
- **Never a bare `: ` inside an unquoted description.** A colon-plus-space breaks the YAML parse and
  the skill loads with empty metadata: `/name` still works, it just never fires on its own. Use an
  em dash.
- **Carry the negative routing that separates this skill from its nearest sibling, and only that.**
  A skill that never fires never reaches its own `When to use vs. neighbours`, so the one or two
  "not X — that is `<other-skill>`" clauses a dispatcher needs belong here. The *rest* of the
  neighbour map stays in the body: a `description` that carries all of it is spending length where
  it buys the least.
- One paragraph, no bullets, no line breaks. It should read as a sentence.
- No application-specific names (no `Material`, no `Order`). Use the placeholder vocabulary from the
  sibling `CONVENTIONS.md`.

### Publishing caveat

Claude Code ignores unknown frontmatter keys. **claude.ai and the Skills API** accept only `name`,
`description`, `license`, `compatibility`, `metadata` and `allowed-tools` and **fail hard** on anything
else, so `paths` and `user-invocable` are stripped before publishing there. Marketplace distribution
— this catalogue's channel — is unaffected.

## Body — the canonical sections

Every skill has these sections, in this order, with these exact headings — templates have one
allowance, stated in rule 1. Four sections are required (`Template(s)` only where the skill has
something to copy — see the universal rules); three (`Other bindings`, `Inlined typing /
import rules`, `Package wiring`) are optional, included only when load-bearing.

```markdown
# <Title> — usually `<Prefix> — <Concept>` or `<Concept>` alone

<One short opening paragraph: what the skill covers and its hardest boundary.>

## When to use vs. neighbours

<One line per genuine neighbour, as many as the skill has: "X → `skill-name`." Goal: a reader who
misclassified the work sees its real home immediately. This is also where the negative routing lives
that the description deliberately leaves out.>

## Template(s)

<One or more literal file templates with placeholder names, from the sibling CONVENTIONS.md — the
entire file for a house artifact, the house skeleton around one minimal call for an integration
(rule 4). The heading NAMES THE STACK the template binds. When the skill covers several kinds of
genuinely different shape (standalone vs UoW-managed repository, list vs cursor pagination), give one
template per kind under `### <kind>` subheadings. A second vendor for the same kind is not a kind.>

## Other bindings

<Optional. 1–3 bullets per named alternative, each saying what changes and what does not. Never a
second full template.>

## Rules

<Numbered list of the obligations specific to this artifact, stated mechanism-free. Don't restate
cross-cutting rules (typing, imports, packaging) — reference the cross-cutting skill instead. Each rule
is one short paragraph or one bold-led bullet, and states one obligation once — two rules saying the
same thing are one rule. There is no numeric limit; past ~20 entries, review checks whether the skill
holds two concerns and should split, or move part to a sibling file.>

## Inlined typing / import rules

<Optional but common. A 3–6 bullet slice of the cross-cutting rules most load-bearing for THIS
artifact, so the reader need not pull the full cross-cutting skill when only a few rules apply.>

## Package wiring

<Optional. When the artifact requires updating an `__init__.py` re-export, point to
`python-packaging` in one line. Do not restate the rules.>

## Hard stops

<Bullet list of "asked for X → stop, use `<other-skill>` (or fix the request)". One line each, and
only for a wrong turn taken before any rule applies (rule 7). These are how a reader self-detects "I'm
in the wrong skill".>
```

## The two layers — principle and binding

One skill serves several stacks by keeping two layers apart.

**Layer 1 — the principle.** What the reader is obliged to achieve. It survives a change of library,
driver or framework. It lives in `## Rules`.

**Layer 2 — the binding.** One concrete stack, shown in full, so the reader has something to copy. It
lives in `## Template(s)`, and alternatives are *named* in `## Other bindings` without being written
out.

### `## Rules` states obligations, not mechanisms

The test for every rule: **would it survive swapping the library?**

- Survives: "Translate the driver's integrity error into a catalogue exception at the repository
  boundary."
- Does not: "Catch `IntegrityError`."

A rule may *name* a library as an example of the obligation — "…`IntegrityError` under SQLAlchemy" — but
the obligation must be legible with the example removed. A rule that collapses into nothing when the
library name is deleted belongs in the template, not in `## Rules`.

### `## Template(s)` headings name their stack

`## Template — SQLAlchemy Core`, not `## Template`. `## Template — FastAPI router`, not `## Template`.
A reader must know in one glance which binding they are looking at, because the binding they are looking
at may not be theirs. A bare `## Template(s)` is only correct where the template binds no stack at all —
stdlib-only code, or a directory layout.

### `## Other bindings` names alternatives without writing them

- **1–3 bullets per alternative**, each saying **what changes and what does not**. "Under the ORM,
  mapped classes replace the table objects and the session replaces the connection; the repository
  protocol, the exception translation and the transaction ownership rule are unchanged."
- **Never a second full template.** Two full templates in one skill is what makes a skill
  unmaintainable — every rule change then has to land twice, and one copy rots.
- If an alternative genuinely needs its own templates, **it is a sibling skill, not a bullet.**
- Omit the section when the skill has no real alternative. An empty `## Other bindings` is noise.

### `## When to use vs. neighbours` has no bullet cap

**One line per genuine neighbour, as many as the skill has.** There is no 3–5 limit; any such cap is
withdrawn. **Dropping a real routing edge to hit a count is a defect**, not tidiness — a reader who
lands in the wrong skill and finds no route out does the work in the wrong place.

## The portability gate

A skill ships to projects the author has never seen, so it is written against five questions and
re-read against them before every edit. The swap test above answers question 3 only — a skill can pass
it while saturated with one project's directory roles and workload assumptions. Whatever a question
flags is replaced with a placeholder or deleted before the skill ships.

1. **Provenance** — does anything name or imply one particular application: its domain, services,
   tables, queues, env prefixes, role names, or vocabulary invented for it?
2. **Repository shape** — does it assume a layout beyond the one artifact it describes — a monorepo, a
   workspace, sibling packages, a shared library — or carry `paths` globs matching one project's
   directory names?
3. **Technology** — is any library, framework, vendor or protocol required rather than illustrated?
   Would every rule and every hard stop still fire if it were swapped?
4. **Workload** — does it assume what the program is: that it has a database, an HTTP surface, a
   scheduler, a queue, a long-running process, more than one deployable?
5. **Residue** — strip everything the first four flag. Is there a rule left that a reader could
   actually violate, and is it the rule the skill claims to own?

### Hedging is not placeholdering

The failure these questions catch is a **disclaimer standing in for a placeholder**. "One app's
model", "rename these to suit", "illustrative only" above a concrete example lets the example
survive, and readers copy examples, not disclaimers. The proof case in this catalogue was one skill
pair carrying two source projects' role ladders and tenant names at once, each labelled "one app's
model" — when two projects each donate a ladder and both get a disclaimer, the disclaimer is doing a
placeholder's work. **The fix for a hedge is a placeholder or a deletion, never a better hedge.**

## Rules

1. **Match the section order exactly — with one allowance for templates, and one for Reference
   bodies.** Section headings are how a reader decides what to read, so renaming or reordering breaks
   navigation. `## Template(s)` is canonical and names the stack it binds (see above); the template
   allowance touches that section alone and takes two forms.
   **Grouped by topic** — a skill covering **several artifacts** may use topical `##` sections with the
   templates as `###` subheadings, on one condition: **the heading names the artifact** (`## The Table`,
   `## The container`), never a discussion (`## Notes`, `## Background`) — an artifact name answers
   "is this the section I need?" as well as `Template(s)` does.
   **Singular or named** — a heading carrying **one** template may name its form and stack
   (`## Template — SQLAlchemy Core`, `## Skeleton — router file`); several forms of one artifact go
   either under `## Template(s)` as `### <kind>` or each under its own name.
   **Reference bodies** produce no file, so they may use topical `##` headings that name *the subject
   matter* (`## Naming a protocol`), never a discussion label; the required sections keep their exact
   headings and relative order around them.
   Every other section keeps its heading and place, and a Reference skill still omits the template
   section. These allowances rest on evidence of success — skills in these forms were loaded and
   applied, and no template went unfound. If a template is ever missed because of a topical, singular
   or named heading, that form is withdrawn and `## Template(s)` becomes the only heading.
2. **State the obligation, then bind it once.** `## Rules` is mechanism-free; `## Template(s)` carries
   exactly one stack; `## Other bindings` names the rest in bullets. A skill that teaches two stacks in
   full is two skills, or one skill and a sibling.
3. **Keep the body concise.** A loaded body stays in context for the rest of the session, so every line
   is a recurring cost: state what to do rather than narrating how or why, and split into sibling topic
   files past ~500 lines.
4. **Templates are literal, not prose — and they are copied, not read.** Show the entire file for a
   house artifact; for an integration with a vendor, show the house skeleton around one minimal call
   (rule 15). Every line lands in the reader's project verbatim — directory and class names,
   constants, version floors and comments alike — so a comment in a template is one that is true in the
   reader's file; the API a version floor relies on qualifies, because it stays true there. Why the
   template itself looks this way (why this example, why a driver raises what it raises) goes in prose
   or `## Rules`, never in a `#` line. Use the placeholders rule 8 names, and read the sibling
   `CONVENTIONS.md` for the full set rather than guessing at it.
5. **One artifact kind per skill, or one set that always arrives together.** Two unrelated artifact
   types means two skills. Producing 2–3 tightly-coupled files (command + handler; protocol + adapter)
   is fine, and so is one skill covering several artifacts a single change always adds at once.
6. **Cross-cutting rules are referenced, not restated.** Point to the owner in the table below rather
   than copying its rules; an inlined slice of 3–6 load-bearing bullets is the one exception.
7. **A hard stop catches a wrong turn no rule in this skill governs.** It exists only for an action
   taken before any rule applies — the request itself, the choice of skill, whether to write at all —
   stated as that action. The remedy decides it, not the phrasing: a stop whose remedy is another
   skill, or writing nothing, stays; one whose remedy writes something in this skill differently is
   deleted however it is worded — declining and writing it otherwise here counts as the latter — its
   better wording moving into the rule first. Every plausible wrong-skill case is one, with a
   redirect. A hard stop keeps its *reason*; softening "X → stop, use `Y`" into advice deletes the
   rule.
8. **Use placeholder vocabulary.** `Foo` for the primary aggregate, `Bar` for the secondary, `Baz` for a
   third held by a different kind of store, `Qux` for an external system the service calls, `myapp` for
   a distribution's own root package, `myschema` for a library several distributions share, `myrepo`
   for the repository root, `myframework` for a framework a rule is about wrapping. Never name a real
   aggregate, role, tenant, bucket or service from the application at hand. The banned vocabulary is
   in the sibling `CONVENTIONS.md`.
9. **No author-side notes in the body.** Lines like "do not duplicate these rules here" address the
   author, not the reader, and they cost context on every load. Put them in the commit message.
10. **A skill must not know what invokes it.** No mention of who calls it, what it reports back, or what
    inputs some caller must supply — those belong to layers outside the skill. The purity test: would a
    new developer read this as onboarding documentation? If they would trip over a line, that line is a
    leaked layer — cut it.
11. **Names carry their style.** Anything bound to a style carries that style's prefix. An unprefixed
    name means "applies in any style".

```
<universal>              naming, coupling, python-style, ...
meta-<artifact>          meta-skill-author
hex-<artifact>           hex-domain-model, hex-application, ...
hex-restapi-<artifact>   hex-restapi-endpoint, ...
hex-test-<artifact>      hex-test-application-handler, ...
flat-<artifact>          flat-entrypoint, flat-persistence, ...
flat-test-<artifact>     flat-test-entrypoint, ...
delivery-<artifact>      delivery-spec
```

`flat-layered` keeps its name — it is the style anchor, not an artifact skill.

12. **Run a template's imports before the skill ships.** A reader pastes a template, so every symbol it
    names has to exist in the library version the template binds — import them and see the names
    resolve. Nothing else catches this: the checks confirm a skill parses and that the skills it names
    exist, never that the code inside it runs. A symbol that does not exist is not a typo, it is a
    template nobody ran.
13. **An empirical claim names what was measured, or it comes out.** "Measured", "in practice", "this
    has been hit" are what make a rule credible, so a rule using them states the observation a reader
    could repeat — what was run, against what, and what came back. Otherwise drop the evidence
    language and let the rule stand as the obligation it is. A fabricated measurement is worse than no
    evidence: it is what stops the next reader checking.
14. **A rule a defect paid for travels verbatim.** When such a rule is moved, merged or reworded
    across skills, copy the sentence rather than restate it. What carries it is one distinctive phrase
    or code pattern, the part a plausibly-wrong rewrite would never reproduce by accident; a paraphrase
    keeps the topic and drops exactly that, so the rule survives as a heading and stops changing
    anyone's behaviour. If the wording around it has to change, keep that phrase intact inside the new
    wording.
15. **House pattern, not vendor manual.** Strip every call to the vendor's API from a template. If a
    house pattern remains — injection, error translation at the boundary, transaction ownership, the
    shape of the file — show it once, on the most common binding, around a minimal call. If nothing
    remains, the template is the vendor's documentation, which the reader already has; it does not
    belong in the catalogue. An error-code map, a canonicaliser or a client wrapper that restates the
    SDK fails this test. A template shows each kind of artifact at most once; a second vendor for the
    same kind is `## Other bindings` bullets, and `### <kind>` subheadings separate different shapes,
    never different vendors (rule 2).
16. **A skeleton carries only lines most services of its family have.** A reader copies every line of
    it, so a variant is either one line marked with the condition that earns it, or one sentence of
    prose — never an unmarked line.

## Ownership — reference, never restate

A rule lives in exactly one skill. Every other skill points at it.

| Rule | Owner |
|---|---|
| What anything is called, incl. the `I` prefix on protocols | `naming` |
| Typing, comments, type suppressions | `python-style` |
| Logging — the event, who logs an error, where it is configured | `python-logging` |
| The interpreter floor, and the three settings that name it | `python-style` |
| One class per module, `__all__`, `__init__.py` re-exports, imports | `python-packaging` |
| Settings from the environment | `python-settings` |
| The image a runnable program ships in — its stages, its user, its build context, its stop signal | `python-container-image` |
| Lint, type-check and test-runner configuration, the src layout, dependency declarations and floors, where any other hand-written version comes from | `python-toolchain` |
| The error catalogue and boundary translation | `exception-catalog` |
| A unit delivered at least once — when it is acknowledged or returned, bounded redelivery and the dead letter, a redelivery changing nothing, a third party's signature checked over the raw body, what a relay of a recorded effect owes | `at-least-once-delivery` |
| A command-line interface — the thin command, the exit-code map, the command line as a published surface, its in-process test | `python-cli` |
| Store-generic data access — which rules bind given the store, transaction ownership, where a driver error is translated (the translation itself is `exception-catalog`'s), constraint and table names, row mapping, stored types, conflicts, ordering and deduplication, paged reads, migrations as a deploy step, data-access code logging nothing | `persistence` |
| What the version promises, and the change that moves it | `python-versioning` |
| Where a boundary goes, split vs merge | `coupling` |
| Testing constitution | `test-principles` |
| Choosing between the hex and flat families | `architecture-choice` |

**Every owner in this table is a universal skill**, so every rule it assigns is present in a
`pyhouse-universal`-only install. A rule only one family has is owned inside that family and does not
get a row — transport authentication is `hex-restapi-auth`'s, in the `pyhouse-hex` plugin — because a
row is a requirement, and a universal file may name a family skill only as an example.

**Before replacing a restatement with a reference, open the owner and confirm the rule is there.** A
pointer to a rule the owner never stated is a deletion both files hide, each reading as if it exists.

An inlined slice of 3–6 bullets under `## Inlined typing / import rules` is the one allowed exception,
and only when those bullets are load-bearing for the artifact at hand.

## Skill shapes (a navigational aid, not a requirement)

Every skill falls into one of four shapes. The section format is universal — a shape adds no canonical
section; shapes signal which sections will be load-bearing rather than ceremonial. Identify the shape
before writing, so the content matches skills already in the same shape. What each shape emphasises,
with the skills already in it, is under `## Skill shapes` in the sibling `CONVENTIONS.md`.

### Picking a shape

| Question | If yes |
|---|---|
| Does it create a brand-new file each time? | **Producer** |
| Does it only extend a file that already exists? | **Modifier** |
| Does it produce a fixed set of files, once per project? | **Bootstrap** |
| Does it produce no file at all — just rules others follow? | **Reference** |

A skill that fits no shape cleanly probably mixes concerns; split it.

## Universal rules, whatever the shape

- No `## Revision` footer and no author history block — that is author metadata paid for on every load.
  Use git history.
- No section describing what the skill returns or who invokes it (rule 10).
- Hard stops use the canonical phrasing: "X → stop, use `<other-skill>`" or "X → stop, <action>".
- A reference skill omits `Template(s)`, `Other bindings` and `Package wiring`; everything else keeps
  all four required sections, under the allowances of rule 1, except that a skill with nothing to copy
  omits `Template(s)` (below).
- **A template earns its place by being copied.** It shows a file, or a block of text, that most
  projects using the skill would take as written — a command block only when a project runs it once,
  as written, such as a bootstrap. Commands repeated per change or per release, a walkthrough or a
  demonstration of the mechanism behind a rule are not a template: they become a sentence of prose
  beside the rule, the commands inline and whole, with any flag that keeps them from prompting, or
  nothing. A skill left with nothing to copy omits `## Template(s)`, as a reference or process skill
  does.
- A universal (unprefixed) skill may name a `hex-*` or `flat-*` skill as an example, but may not
  *require* one — the `pyhouse-universal` plugin must be installable alone. See the packaging table in
  the sibling `CONVENTIONS.md`.

## Common pitfalls

- **Two skills wearing one name.** A description that reads "apply when X *or* Y" is two skills. Split.
- **A description that does not disambiguate.** "Apply when working with foos" is too vague. Compare
  "Apply when adding or modifying a repository adapter for an aggregate on a relational store", which
  excludes the other foo-touching work by construction.
- **A description carrying the whole neighbour map.** Keep the one or two clauses that separate it
  from its nearest sibling; move the rest to `When to use vs. neighbours`, where a reader who is
  already in the wrong skill will see them.
- **A rule that names a mechanism instead of an obligation.** "Catch `IntegrityError`" is a template
  line wearing a rule's clothes. Restate it as what must be achieved.
- **Templates that document the rule instead of showing the file.** More comments than code means the
  rule is being explained. Move the explanation to `Rules` and tighten the template — every comment
  left behind ships into the reader's files (rule 4).
- **A template that is the vendor's manual.** SDK error-code tables, input canonicalisers, client
  setup the vendor documents — nothing house-shaped is left once the vendor calls go (rule 15).
- **A rule above, broken in passing.** A description that does not open with its trigger, a second
  full template, a `## Template` heading naming no stack, a hard stop softened into advice ("think
  carefully before X"), a leaked layer (rule 10) — each is stated once above and fails the same way here.

## After writing the file

The catalogue has two indexes — the one in the sibling `CONVENTIONS.md` and the catalogue index at
`skills/README.md`. A skill's coverage is stated once, in its own frontmatter; both indexes restate
it, and no generator derives them yet, so they are kept in step by hand in the same change as the
skill.

1. **Add the skill to both indexes.** In `CONVENTIONS.md`, one disambiguating line under its family —
   written to agree with the skill's `description` and body, not copied from either. In
   `skills/README.md`, one row in its family's table.
2. **Update every count the skill changes** — the family heading in both indexes, the total at the
   top of each, the plugin's row in the packaging table, the plugin table and the prose total in the
   repository's top-level `README.md`, and the counts in the repository's `CLAUDE.md`. Counts are the
   first thing to go stale.
3. Confirm which plugin the skill ships in, using the packaging table in `CONVENTIONS.md` — the prefix
   decides it.

## Hard stops

- Asked for a skill whose whole content is rules an existing skill already states, or whose description
  overlaps an existing one's by more than half → stop; that is an edit to the existing skill.
- About to write a skill from supplied material that leaves nothing once question 5 strips the
  project-bound part → stop, there is no skill here — the material was a case study, not a subject.
