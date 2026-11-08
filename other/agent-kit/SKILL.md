---
name: agent-kit
description: The portable rules layer of the agent — laws, rules, hooks and checks shipped by the package and adjusted by the tree through overrides. Load when a file with the rt-kit header is edited, the package is upgraded or the layout audit refuses. The shape of a new skill — write-a-skill.
---
<!-- rt-kit v0.34.0 · skills/agent-kit.md · 25f93b27d3bb · правится надстройкой, не здесь -->

# The portable rules layer

Laws, rules, patterns, hooks, checks and roles are shipped by the package; the tree takes them
by layout and adjusts them with overrides. A laid-out file carries a header and is not edited —
either the package or the override is edited.

**Cold part:** `pitfalls.md` next to it — pitfalls, traps already stepped on. Loaded on demand,
not together with the skill.

## When to use

- The file you are about to edit carries the header
  `rt-kit v<version> · <resource> · <checksum> · правится надстройкой, не здесь`.
- The package was updated, or `sync --check` refused in the push gate.
- Your own behaviour has to be added on top of the package one: a guard, the gate map, the
  set of checks.
- The package is installed into a tree whose hooks and checks are already its own.

## Where what is set up

| What you change                                   | Where the edit goes                                     |
| ------------------------------------------------- | ------------------------------------------------------- |
| which rule the gate demands for which file        | `.claude/rt-kit/gate-map.sh` — your own `skill_for`     |
| ports, addresses, linters, branch form, inventory | `.claude/rt-kit/project.sh` — your own `rt_*`           |
| paths and identifiers the checks live by          | `.claude/rt-kit/checks.json`                            |
| which uniformity signs the tree takes             | `checks.json`, keys `reuse.bundles` and `reuse.signals` |
| a section of a laid-out text                      | `.claude/rt-kit/overrides/<resource identifier>`        |
| what to take and what to drop                     | `.claude/rt-kit.json`, keys `only` and `skip`           |
| which roles are called by hand, not mandatorily   | `.claude/rt-kit.json`, key `rolesOff`                   |
| what the tree has: storage, admin, packages       | `.claude/rt-kit.json`, key `has`                        |
| the mechanism itself — guard, check, rule text    | the resource in the package                             |

An override redeclares the function and may call the default by the same name with the
`_default` suffix. Text merges by `## ` sections: a matching heading replaces, a new one is
appended, an empty one lifts the package section.

A ready-made sample for every row of this table is the skill `agent-kit-extend`: how the edit
itself looks, what checks it and how it ends if put in the wrong place.

## Order

The layout puts everything or nothing: a refusal on even one file writes nothing — half a
layout is worse than a whole one. Either the override here or the resource itself is edited —
and that is the work of the tree where the package lives as sources; nothing is said about it
here.

**A file whose body matches the package is never a refusal.** The header alone diverged from the
body — the layout puts it again and says the header went stale. The word "edited by hand" stays
for a file whose body differs, and it sends the reader looking for an edit that is there.

**A layout is an edit of the tree, not a service call:** it rewrites hundreds of tracked files at
once, so the work is set up before `sync`, by the same rules as any other.

**The package version bump and the layout go in one change.** The layout audit stands in the
push gate: an edition bumped without a layout turns the main branch red and locks the whole tree.

**The layout puts the hook declaration together with the hook itself.** A hook is called by an
entry in the agent settings, and one laid out without it is indistinguishable from the outside
from a working one. The layout appends an entry for every event missing from the settings and
reports it. The edit only adds: entries are neither rewritten nor removed, and settings that
cannot be parsed as JSON the package does not touch — it prints a ready-made piece to enter by
hand.

**An entry is written only for the dispatcher that lies on disk.** A tree that did not take it
used to get settings calling a file that is not there — and such settings look working from the
outside. The layout holds no list of what the tree removed, so a hand-removed entry comes back on
the next layout: it is removed together with the dispatcher, not on its own.

**This is held by the edit-location guard, not by memory.** It refuses an edit of a file with the
layout header at the minute of the edit and names the address: the source, if the tree holds
it, otherwise the override. The copy is edited not only by hand: the tree formatter rewrites a
laid-out file its own way, and the layout reads that exactly as a hand edit. Removing the copy
the guard lets through — a removed file the layout puts anew.

**An override is edited by section, not put in full.** Sections are added to it by different
branches and different sessions, and put in full it carries away all that this edit did not
touch. This is held by the second guard — it refuses a write over a non-empty override and names
the size of what would be wiped. Appending at the end and editing in place pass.

## Commands

```bash
npx agent-kit doctor        # what is laid out, what lags, what lies from a dropped resource
npx agent-kit doctor --since <path>  # the same, plus what a new edition added into a replaced section
npx agent-kit sync          # lay out
npx agent-kit sync --check  # write nothing, refuse on a divergence
npx agent-kit stats         # what was used, what never, what people stumbled on
npx agent-kit enroll --code <code>  # enrol the tree in the intake and put its token
npx agent-kit propose       # send the cargo to the intake: the digest, proposals and analyses
npx agent-kit fate          # the fate of one's own records and the overrides that are due to be lifted
npx agent-kit adopt [files] # hand the package your own file lying on its path
```

Adoption sets the former content aside next to it, marked `.before-rt-kit`, and frees the path
for the layout; without names all foreign files are handed over at once.

Some commands of the layer are run by the agent, not by the program: `/feedback` puts a remark
about the rules as a block into the proposals file, `/skill-curator` reviews a closed task,
`/next-session` closes the session.

There are no commands for editing the package itself here: they are called where its resources
lie.

## Version bump

A matching heading replaces the package section in full, and everything the package added to such
a section in a new version vanishes silently: the layout matches, the headings match, and the
statements are gone. The heading audit catches a renamed section, not an extended one — the loss
has no other witnesses.

So the bump takes three steps, and the first goes before the installation.

1. **A snapshot of the former edition of the resources.** The installation wipes it without a
   trace, and there is nothing to compare with afterwards.

    ```bash
    cp -r node_modules/@rt-tools/agent-kit/assets /tmp/agent-kit-assets-<former version>
    ```

2. **Installation and layout.** The usual way. The layout puts the edition that is
   **installed**, not the one the tree declared: the installed one is left over from a
   neighbouring branch and lands in full, silently, with the same successful exit. A mismatch of
   the exact number the layout refuses by itself; the fix is to install dependencies and repeat
   the call.
3. **An audit of the replaced sections against the snapshot.** Which sections are replaced is
   named by `doctor` — with the line "замещено надстройками разделов" and a list of
   "resource · heading". Each is read in the snapshot and in the new edition: what the package
   added is added to the override by hand.

The snapshot is given to the state review as an argument — `agent-kit doctor --since <path to the
snapshot>` — and it names the articles the new edition added inside a replaced section: the
resource, the heading and the opening of the article. Without the argument the review is as
before.

For every named section the articles are compared, not the headings: the heading is exactly
what matched, that is what replaced the section. A ready-made pair of commands is in the cold
part next to it.

Then the decision is the usual one: the section the override was started for stays replaced,
and the section whose reason left with the fixed edition is lifted.

## What the package ships and what stays with the tree

The package is installed by foreign trees, and it ships them only what they carry out. A
resource that has no subject in a foreign tree, or nobody there to call it, is never a package
resource — it lives as the tree's own resource where the subject exists.

The sign is not an appraisal but two questions to the resource:

| Question                                          | "No" means                                       |
| ------------------------------------------------- | ------------------------------------------------ |
| Does the consumer have what the resource speaks of? | no subject: nothing to fill the companion with |
| Does the consumer have someone to call it?        | no executor: the command does not run there      |

"No" to even one — the resource stays with the tree that writes the package.

**The list of dropped resources does not close the boundary.** A line in `skip` says "I do not
need this" and lifts the layout at home; the resource stays in the package and keeps going to
everyone else. It is removed from the package itself, not from your own layout.

**The tree's own rule is declared on a par with the package one:** the same shape, the same law
above, a companion next to it and its own branch in the gate map. The reader must not see that
it is younger.

What must be true at that is written as an agreement in the tree that writes the package: the
check that holds the boundary lives there too. A foreign tree has no business judging the
package resources, so the check does not go here.

## Feedback upwards

The rules layer is edited not from memory but by how it was used. This is held by three things.

**Observations** are written by the guards themselves — into `.claude/rt-kit/observations/`, a
file per day. A line holds the package resource name, the kind of event, the kind of edit, the
version and a session sign; no tree paths and no tree name are there. Switched off by the key
`"observe": false` in the config.

**The digest** is `agent-kit stats`. Its most valuable line is not "what was used" but **what is
laid out and never loaded**: a rule nobody opened gives itself away by nothing.

**The cost** is `agent-kit cost`. The digest says what was used; the cost — what it cost: the
weight of entering work, the weight of one rule and the weight of the whole layer. Counted is
not the file but what the session receives. The number is comparable only with one taken by the
same command.

**Proposals** come by two roads: the review of a closed task — by the `/skill-curator` command —
brings them in a batch, and a remark made in the middle of work is put by the agent itself with
the `/feedback` command. Both write into one file of the day and in one form; neither goes to
the network — the send carries them away.

**The wording of a record is judged by the send, not only by the guard on an edit.** The guard
stands on a `.md` of the tree, and a record leaves by a command — that is, past it. The send calls
the wording check laid out in the tree on the text of every record: one with findings does not
leave and is named by its file, its line and the first finding, while the rest of the batch goes.
A refused record stays lying on the disk with the mark «отбито» and leaves after the fix. A tree
that laid out no such check sends as before and says so by a line: silence about it would read as
a check that found nothing.

**The text of a record is written by the role `cargo-writer`, and it writes no files.** The
record is read by a person who knows neither this task nor this tree, while it is written by a
session thinking in the words of the rules layer. The role writes into the ready-made shape —
its own shape gets the block refused by the quote — and hands the text back: putting it on the
disk belongs to whoever answers for the send.

Every record carries four lines: **place** — where the edit goes in the resource, **reason** —
what went wrong without it, **closest** — the exact quote of the resource line this is closest
to, and **what it closes** — which overrides of the tree are lifted when the edit arrives as a
package edition.

The third line is the only one the machine checks: the quote is searched for in the resource,
and one not found refuses the block. There is nothing close at all — write exactly that: «нет».
A refused block stays lying with the mark «отбито» and the reason: it is visible that the review
took place and why it did not become an edit.

The fourth is written because the proposal goes outside while the override stays lying here:
without it, it replaces an already fixed section forever. There is nothing to lift — write
exactly that; the fourth line is never empty.

The same link is put on the override itself — as a markup comment in its section:

    <!-- rt-proposed: rules/task-flow.md · «the article in full, as in the proposal» · 2026-09-03 -->

Nobody opens the proposal records on the day of the update: nothing points to them. The mark is
invisible in the assembled text, survives the merge by headings and is read by the machine: the
layout lists the sections whose article already exists in the new edition. A person lifts them —
something else may have been added to the section. A section without a mark counts as permanent.

Every proposal gets an address: «пакет», «компаньон» or «дерево». They are dumped into a file in
`.claude/rt-kit/proposals/` (the form is the template `proposal.md`), and `agent-kit propose`
carries to the intake those addressed to the package, together with the digest and the incident
analyses. A tree address in the digest or in the proposal text refuses the send in full.

The intake is a closed service: the digest speaks of the team's working habits, and in an open
work queue that is laid out for all to see. The intake address is declared by the key `intake`
in the tree config, the token by the key `token`, and it lies outside the tree.

Both values come from the intake owner and are not invented by the consumer: the address they
name, the token they issue as a one-off invitation code — the code enrols the tree in the intake
and puts the token into the file of the key `token`. Before the invitation the send refuses by
design, not by misconfiguration.

**The fate of its own records the tree asks by `agent-kit fate`.** The command reads the intake by
the token — the same one the cargo goes under — and prints every record with its state, what it was
fixed by and the version of the release. Under a record stands the override the mark of its section
ties to it: it is lifted now when the article already lies in the laid-out edition, and it waits for
an installation when the fix came out and has not reached this tree. A mark the intake gave no
record for is named apart. The command lifts nothing itself: the mark holds one article, and the
section may have been written into since.

**The tree sign is computed by the sender, not by a person.** It is derived from the repository
address, and the intake record is created by exactly it: a tree enrolled under its own word the
intake does not recognise. What would go and under which sign is printed by the dry run.

**The mark of a send is a trace for a person, not a store of state.** A clean tree after a send
means the whole cargo already lay in the intake, not that the send did not work.

They are reviewed where the editable resources lie and all consumers are visible at once — and
what arrives here is the intake's reply about how many records landed.

**The proposal file name is not named in tree texts.** It gives a reader of a foreign tree
nothing, and a link to a directory on the author's machine leads nowhere and turns the path check
red. Repository text says whom the proposal was sent to and what it is about; the package
resource may be named.

A proposal does not straighten the work. It lies as text, is read by eye and does not come into
the context by itself. It counts as closed only once it has entered a package resource: until
then it is not referred to as a current requirement and the hole is not counted closed.

**The owner's word about a proposal — "send it", "file it", "write a proposal" and any other form
of the same — is carried out by a send in the same turn.** A dry run does not count as a send: it
shows what would be sent and leaves no trace outside. The marks the send leaves in the tree land
as a second commit in the same branch. This is checked by the proposal guard at the end of the
turn.

## Installation where everything is already your own

1. `init`, then `skip` on everything the tree holds itself; an empty layout is a lawful start.
2. A snapshot of what the tree's checks say, before a single edit: it is the measure.
3. Resource by resource: bring the package edition up to the local one, move the subject matter
   into an override, lift the drop, lay out, run the scenarios and compare with the snapshot.
4. The package does not write a layout over your own: a file without a header is foreign to
   it. It is handed over with the `adopt` command — the former content lands next to it, marked
   `.before-rt-kit`.
5. A resource whose local edition is richer than the package one in substance is not taken into
   the layout. The sign is an article that the package edition lacks and cannot have: it follows
   from the tree's subject. It goes into `skip`, and a proposal to remove it from the package
   goes upwards.
6. Your own scenarios of a handed-over file are rewritten for the package behaviour or removed:
   fixing the package edition in place is not allowed, its address is the package source or the
   override.

## Tree traits

Some package rules are true only where there is a storage, an admin or an application. The tree
lists what it has by the key `has`; a resource names the trait it needs by a prefix in its name —
`observability.needs-app.md` — and to a tree that did not name such a trait it is not put at
all: neither itself nor the draft of its companion.

```json
{ "has": ["packages", "app"] }
```

- **Silence does not answer a requirement.** A tree with an empty `has` gets not one marked
  resource: put at a guess, it comes back as an empty companion with nothing to fill it.
- **A requirement is not a kind.** A kind is chosen once; a tree has several traits at once.

## Disabled role

A role with a guard next to it is not called at the executor's discretion: the guard holds the
work until the role has had its say. A tree it gets in the way of names it by the key `rolesOff`
— by the role file name.

```json
{ "rolesOff": ["strict-teacher"] }
```

- **What is switched off is the mandatory call, not the role.** The role file stays laid out, and
  it can be called by hand at any minute. The list is read by the guards themselves — through a
  helper lying next to them.
- **It differs from dropping by the `skip` key in that it removes nothing.** A drop does not put
  the role file at all: there is nobody left to call, and the guard next to it stays and keeps
  refusing. Here it is the other way round — the role is in place, the guard is silent.
