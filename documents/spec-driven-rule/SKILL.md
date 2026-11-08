---
name: spec-driven-rule
kind: pattern
rule: spec-driven
description: Pattern of rule spec-driven. Load when creating or editing a law in docs/constitution, a rule or a pattern in .claude/skills — ready-made headers, the section set of each layer, the binding table, the sign that a rule is due for splitting. Not for a domain spec — that is pattern spec-driven-domain.
---
<!-- rt-kit v0.34.0 · patterns/spec-driven-rule.md · 27e8998650f1 · правится надстройкой, не здесь -->

# Law, rule and pattern

Pattern of the rule `spec-driven`. What must be true — the law
`docs/constitution/project-documentation.md`.

## When to use

- A rule has to be repeated in two more places — time to create a law.
- A rule is created under a law that already exists.
- Ready-made code in a rule has grown — time to move it out into a pattern.

## Law

`docs/constitution/<law>.md`. Knows nothing of the project: no paths, no file names, no
bindings. The sign of a law: an attempt to put the rule into a domain spec forces repeating the
same thing in two more.

The layer is chosen by one question: does the article stay true in an application with no
payments, no translation locales and no second owning entity. It stays — the law lives in the
root; it does not — this is an application law, and it goes to
`docs/constitution/application/<law>.md`. A law name is one for both layers: neither `law:` in
the rule header nor `**Законы:**` in the spec header names the layer, and two laws with one name
would part a rule from its law.

Sections: `## Зачем` (without a heading, as the intro paragraph) · `## Articles` ·
`## Open questions`. Only "Articles" is mandatory — that is what the check audits. "Open
questions" is created when there is a question and erased with the last one closed: a closed
question is removed from the law, not turned into an empty section.

There is no date in a law either: one law out of seventeen had one, the rest never did, and read
as an expiry it ages a correct text nobody touched, because there was nothing to touch. A law
holds neither a history of edits nor arguments for why something was once chosen so. History is
held by version control, and an argument with a rejected alternative is a trait of the work, not
of the product: its place is the "Pitfalls" of the rule under this law, where file paths are
allowed too. A statement that cannot be written as "always true" does not become an article at
all.

```markdown
# The delivery law

How an edit reaches the running application. …

## Articles

- **The image of the commit being rolled out is what gets rolled out.** The default "latest"
  falls behind the main branch, and the application silently returns to the previous version
  while it keeps answering.
```

The `## Open questions` section is created when there is a question and erased with the last
one closed. A question is named `Q-<law letter>-<number>`, says what the decision would change
and carries its creation date; the number is not reused after closing.

Code behaviour is not a law: "the store answers with a boolean", "the method is called `save`" —
neither a guest nor the owner sees this. The boundary is simple: a law describes what is visible
from outside the application. The exception is an article about code structure that the machine
audits: anchors are read only under `docs/specs/` and `docs/constitution/`.

## Rule

`.claude/skills/<rule>/SKILL.md`. Binds a law to this project; there can be several per law.

```markdown
---
name: git-workflow
kind: rule
law: delivery
description: Rule under the delivery law. Load for … Ready-made code — in patterns …
---
```

Under the header stands the line requiring neighbouring resources — those without which the
rule's articles are not carried out:

```markdown
**Requires:** `hooks/<guard>.sh`, `checks/<check>.mjs`
```

Resources are named by package names, not by tree paths. No line — the rule requires nothing;
it is never empty. Deriving a requirement from a phrase in the text is not allowed: not
everything is laid out at the consumer, and a text saying "a guard refuses the edit" lies in a
tree where there is no guard.

The line is read as a list of resource identifiers, so prose in it turns into requirements that
do not exist: "requires the launch command and the tree token" the layout splits into two names
and prints both as unanswered — in its output such lines cannot be told from a real shortage. A
requirement is declared by a resource identifier or not declared at all.

Sections: `## What it is called here` · `## Where it lives` · `## Flow` ·
`## How the law applies here` · `## What of the law is not here` · `## Patterns` · `## Pitfalls`.

Only `## How the law applies here` is audited: each of its items starts with a bold phrase,
and each bold phrase has a line in `implementation.md` next to it.

```markdown
| Article                                                       | Where it is carried out             |
| ------------------------------------------------------------- | ----------------------------------- |
| Images are rolled out by commit sha, not by the "latest" tag. | `docker-compose.prod.yml:IMAGE_TAG` |
```

A statement that found no place in code is not put into this section: it goes as prose to
"Pitfalls" or as a question `Q-<law letter>-<number>` to the law.

## Pattern

`.claude/skills/<rule>-<what>/SKILL.md`. At least one per rule.

```markdown
---
name: git-workflow-commit
kind: pattern
rule: git-workflow
description: Pattern of rule git-workflow. Load for … Not for … — that is pattern …
---
```

Sections: `## When to use` · ready-made code · `## Common misses`. A pattern has no binding:
there is nothing to check ready-made code against but itself. Its set of sections is checked all
the same — the suite of the package that ships the texts refuses a pattern without `## When to
use` and without the section of misses. A consumer tree does not see that refusal; the tree with
the package sources sees it in the set before a push.

## How the article itself is written

**An argument at an article names the structure on which it is true.** An argument ages with
what caused it: the ban on writing into someone else's settings stood on JSON merging silently
losing what did not match — and was true while the piece was a map of two dozen declarations.
A dispatcher came, the piece became one line per event, the argument stopped being true, yet
it stood for two more editions and read as a current ban. The named structure is what shows,
at the next edit, that the argument is due for rereading.

**A requirement for a step stands in the section that leads that step.** What is written below
is read after the step: the section about the remaining step was required before too, and the
samples stood ready — but the requirement itself lay below the description of opening the PR.
The reader got to the opening, opened the PR and had not yet seen the requirement; it looks like
forgetfulness, not like the order of the text.

**An article about the uncheckable names which tool exactly does not catch it.** "There is
nothing to check it by machine" ages with what was used for checking: the work queue audit does
not read the PR body — and that was written down as "nobody reads it", although the delivery
guard parses the same command line and judges the title by it. The named tool gives the next
edit a point to count from.

## Description: three hundred characters and one question

The description of a rule and a pattern goes whole into the system prompt of every session —
every session pays for it, whatever it works on. It answers one question: load this or not.

| In the description                                     | Not in the description              |
| ------------------------------------------------------ | ----------------------------------- |
| which law the rule is under                            | a retelling of its articles         |
| when to load — by edit paths or by the subject name    | a list of sections                  |
| for a pattern — when not to load, naming the neighbour | an argument for why the rule exists |
| pattern names at a rule                                | their content                       |

The descriptions check counts the length: it names those over the limit by name, with the
character count. A description that would otherwise stop being found by its subject is left
longer than the limit — and then the name of the rule or pattern goes into the accepted-debt
list with a reason, so that a silent overrun and a deliberate one do not look the same.

## Order

1. The article is written into the law — without paths or file names.
2. The rule declares the law in its header and names the same thing in this tree's terms.
3. Every statement of the rule gets a line in `implementation.md`; the anchor is checked by
   opening the file, not from memory.
4. Ready-made code leaves for a pattern, and the rule refers to it.
5. `npm run check:specs` — before the push.

## Compressing an article: a live sample

The shape is in the rule next to it; here is one real article before and after, with numbers.
Taken from the rule on checking a component: 1110 characters, of which the statement is 90.

**Before.** The statement, the mechanism, two cases from the measurement, a rejected cure, the
consequence in the reference:

```markdown
- **A shot beyond the window touches the page under the shutter, and the cure is not a loop but
  the window.** A frame of a whole page wider or taller than the window the browser takes by
  swapping the window for the duration of the frame: the page gets a `resize`, and everything
  computed from the window size shifts right in the frame. The measurement caught this twice in
  one task — the photo viewer strip lost its scroll, and the frame got the first snapshot of the
  set instead of the last; the page height drifted by two pixels. Whether the shift lands in the
  raster is decided by a race, so the same story turns red or not… A loop until two frames in a
  row match is no cure here but a fixing of the breakage: the shift is stable… The cure is the
  reverse order — the window is widened to the page **before** the frame…
```

**After — 517 characters, the same decision:**

```markdown
- **A shot beyond the window touches the page under the shutter, and the cure is not a loop but
  the window.** A frame wider or taller than the window the browser takes by swapping the window:
  the page gets a `resize`, and everything computed from the window size shifts right in the
  frame. A loop until two frames match is no cure here but a fixing of the breakage — the shift
  is stable. The window is widened to the page **before** the frame, the render is waited for to
  settle, and an ordinary frame is taken; in the reference `100vh` and `100vw` count from the
  widened window. Pitfalls — in the cold part.
```

**Where the rest went — 593 characters in `pitfalls.md`:** which story exactly turned red, how
many times, by how many pixels the height drifted, why a different story looked guilty each time
and why this reads as floating layout. Not one edit decision stands on this: it is needed by
whoever reviews a red snapshot — and loads at that moment.

**What stayed at the article:** the whole statement, the mechanism in one phrase, the rejected
cure (without it the next session creates the same loop again) and the consequence in the
reference — it changes how a story is written.

## Common misses

- The check of the requirement "the step is done" is placed on the call of the step itself. A
  guard bound to the call catches the shape of what was done and does not see what was not done
  at all: leaving a draft that never was gives it not a single event. Such a requirement is
  checked at the end of the turn — there it shows what did not happen during the turn.
- The binding names one place where the statement is carried out, while several sides carry it
  out. The audit looks for the presence of a line, not the completeness of the list: the
  agreement promised declaring several events, the binding led to the settings assembly, and the
  dispatcher read one — and both sides stayed silent. An article whose statement is carried out
  in several places names them all.
- The list named by the tree lies in the companion, and the general argument in the rule itself.
  The general argument always reaches the context, the list only when it was read, and it loses
  the minute the decision is made from memory. Whenever a rule requires "the list is named by the
  tree", it also requires that the list be read before the general words — and says so directly.

- A law named a project file — the check refuses. Paths belong in the rule.
- A sidecar with a binding lies next to the law: it binds the law to this project, and a green
  check will confirm that, because the structure matches what the check itself expects.
- The anchor leads to a dead symbol: declared and found nowhere else. That is how five rules on
  entity editing turned out bound to a mechanism no screen calls.
- The statement was reworded and the binding line was not touched: the link goes by text, and
  the check stops finding it.
- An empty binding is refused by the spec audit, and its verdict must be verbatim: accepted are
  `Не исполняется`, `Не применимо`, `Не проверяется`. A phrase in one's own words — "held by
  text", "checked by eye" — does not count as a verdict, and this is learned from the audit's
  refusal.
- A binding line was appended to the end of the companion instead of inserted into the table.
  More sections follow the table there — "What checks it", "What else to know when reading the
  code" — and a line appended at the end does not make the table at all: the statement reads as
  unbound, and the spec audit is silent about it, because it looks for the line in the table.
  The line's place is the same as its statement's in the rule: the order of both sides is kept
  the same, otherwise the statement and its binding stop being found by one another.
- A binding line came out as one sentence of sixty words. The statement ends at its full stop
  inside the bold, and everything after it — the dash, the anchor, the dash and the explanation —
  is one more sentence to the wording check. The explanation after the anchor is written in
  sentences of its own: the line stays one, the long sentence goes.
- The `description` does not say when **not** to load the pattern — the neighbouring pattern of
  the same rule becomes indistinguishable.
- A block of ready-made code was accepted by its look, not by checking against the declaration.
  The call in the sample repeats the name, number and order of the live function's parameters: a
  two-parameter call looked plausible exactly until the four-parameter declaration was opened
  next to it. The same pass checks the shape of the code — a sample declaring fields unlike the
  tree declares them teaches breaking the language rule, and the rule that forbids it will not
  know.
