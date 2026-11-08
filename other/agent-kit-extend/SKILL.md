---
name: agent-kit-extend
description: Ready-made examples of how a tree adds its own on top of the rules package. Load when the package text says something that is not true here, the gate demands the wrong rule or a guard judges by the wrong paths. Layout and settings — skill agent-kit; the shape of a new skill — write-a-skill.
---
<!-- rt-kit v0.34.0 · skills/agent-kit-extend.md · 9a289cb25603 · правится надстройкой, не здесь -->

# How to add your own on top of the package

The skill `agent-kit` names **where** each kind of edit is set up. Here is **how** the edit
itself looks, on ready-made samples, and what checks each of them.

One rule is shared by all five: a laid-out file is not edited in place. It carries the header
`rt-kit v… · <resource> · <checksum>`, an edit in it is lost on the next layout and until then
looks applied, and `sync` refuses such a file instead of overwriting it silently.

## When to use

- The package text says something that is not true here: the names, paths and techniques of
  this tree.
- The gate demands the wrong rule for a file — or stays silent where there is a rule.
- A guard judges by the wrong paths: foreign roots, its own set of checks, its own branch form.
- Something of your own is started — a uniformity sign, a check, a law with a rule — which the
  package does not ship.

## Text: an override merges by section

The file goes to `overrides/<resource identifier>` — the path repeats the resource one to one:
`rules/testing.md` is overridden by the file `rules/testing.md`.

```markdown
## Pitfalls of this tree

- **The tree snapshot is edited by the same commit as the declaration.** Otherwise the
  installation at a neighbour installs something other than what stands here.
```

| Heading in the override | What happens                    |
| ----------------------- | ------------------------------- |
| the package has it      | the section is replaced in full |
| the package lacks it    | appended at the end             |
| has it, but the body is empty | the package section is lifted |

**Replacement is in full, and that is the main pitfall.** Your own item, added under the package
heading `## Pitfalls`, carries away all package items of this section at once, and the loss is
visible by nothing: the file looks assembled. That is why the heading in the sample above is your
own. The package heading is taken only when the package text is wrong here and really has to be
lifted.

**A heading standing inside a sample does not count as a section.** The parser skips everything
lying inside a code fence: a document sample with headings of its own would tear the resource
into pieces. So an override named by such a heading replaces nothing — it falls into the line
"the package lacks it" and is appended as a new section at the end. The edit looks as if it
worked: the file is assembled, `sync --check` is green, and the needed paragraph stayed as it was.

It is reached by the heading of the section it lies inside — and that section is replaced in
full, together with the sample:

````bash
# which headings the resource really has — samples inside a fence do not get here
awk '/^```/ { fence = !fence } !fence && /^## / { print }' <resource file>
````

Checked by the layout: `sync`, then `sync --check` — and by eye over the laid-out file, whether
the package sections are in place.

A resource is dropped in full not here but by the `skip` list in the config: an override edits
the text, `skip` cancels the file.

## Nothing checks a gate map override

The package scenarios run its default and do not touch the tree's branches: the override has no
tests of its own, and no place for them either. The map decides which rule is loaded under each
edit, that is, what the session is guided by in its work, and it is held by a run by hand and by
the memory of whoever edited it.

A miss in it is silent: a wrong branch does not refuse but quietly returns the wrong rule — it
is noticed only by the volume loaded and by the fact that the loaded text held no answer. So an
edit of the map ends with a call of the gate on three paths: the one the edit was made for, a
neighbouring one that the edit should not have touched, and a file that has no rule at all.

## Gate: your own branch decides before the default

The gate asks `skill_for` — it prints the rule name or stays silent. Silence means "there is no
rule for this", and the edit passes.

```bash
skill_for() {
    kind="$1"; target="$2"; written="$3"

    case "$kind" in
        edit)
            case "$target" in
                # The specific is always before the general: a story file is not a component file.
                *.stories.ts) printf '%s\n' 'showcase'; return 0 ;;
            esac
            ;;
    esac

    # Everything else is handled by the package default — otherwise it is lost in full.
    command -v skill_for_default >/dev/null 2>&1 && skill_for_default "$kind" "$target" "$written"

    return 0
}
```

Two things here are mandatory. **The order of branches:** the first match wins, and a general
branch placed above a specific one eats it silently. **The call of the default:** having
redeclared the function without calling `_default`, the tree is left without all package
branches at once — and it looks like "the gate stopped demanding rules".

Checked by the gate scenarios from the package suite: they run the map without laying anything
out.

## Guard: the profile answers for names and commands

The profile functions are declared by the same technique — what to run before a push, which
document goes as a pair, what lints a file, what counts as application code here, which branch
form is lawful.

```bash
# Which document must go in the same commit. Prints a path sample or stays silent.
rt_docs_pair_for() {
    case "$1" in
        *.spec.ts) return 0 ;;
        libs/kit/src/*/*.component.ts) printf '%s' "${1%/*}/CONTEXT\.md" ;;
    esac
}
```

A **sample** is printed, not a path: the guard checks the commit content against it. The default
is called the same way — `rt_docs_pair_for_default "$@"` — wherever your own rule did not cover
the case.

The path comes from the tree root. A substring sign like `*/projects/*` also matches a foreign
directory outside the repository — that is how a write to the home directory was refused by a
plan requirement that did not apply to it.

## Signs and checks: data, not code

A uniformity sign is data. The tree names the package bundles whose ready-made it takes, and
adds its own by a file; a matching key replaces the package one.

```json
{
    "sourceRoots": ["apps", "libs"],
    "reuse": { "bundles": ["kit"], "signals": "tools/signals/own.json" }
}
```

An object merges key by key: having named one key of a section, the tree does not lose the
neighbouring ones. **A list, on the contrary, is replaced in full**, and that is a pitfall:
having named `sourceRoots`, the tree gets exactly what it named, not the package roots plus its
own. "Add to the list" and "remove from the list" are indistinguishable in this notation, so a
list is always written in full.

A bundle is declared by what the tree **consumes**. A tree in which the kit is written, not
called, having declared its bundle, gets advice to call the kit on the files of the kit itself:
the sign is right, but pointed the wrong way.

A tree that both writes and calls the ready-made does not have to choose between noise and
silence: the sign has a reverse path sample — `exceptNamed` — and by it the source folders of
the ready-made are taken out, not the bundle as a whole. Inside the bundle, bypassing the
ready-made is caught after that as at a consumer, and the folder where that ready-made is written
gets no sign. The sample is read the same way by the sweeping check and by the guard on an edit.

## Your own law and rule

The package ships a rules layer but does not forbid your own. A law of the tree lies next to the
package ones, the rule under it — in the skills directory, and the link goes through the
frontmatter: a rule has `law:` with the law name, a pattern has `rule:` with the rule name. A
name nothing answers to refuses the consistency audit.

A statement of the rule gets a line in the companion `implementation.md` — a binding to a file
and a symbol. A statement that found no place in the code is not put into the checked section:
its place is in "Pitfalls" as prose.

Checked by the spec audit — before the push.

## Common misses

- **An in-place edit instead of an override.** A laid-out file is recognised by the header, not
  by the directory: the layout lands in the same `tools/` and `.claude/` where your own lies.
- **Your own item added to a package heading** — the package items of this section left silently.
- **The override is named by a heading that stands inside a sample.** It can replace nothing —
  the resource has no such section — and goes as a new section to the end. It is visible by eye
  in the laid-out file: two identical headings, one inside a sample fence, the other as the last
  section; the layout is green at that, because there is no divergence from the package.
- **The function is redeclared without a call of `_default`** — together with your own case all
  package ones are lost.
- **A general branch of the map stands above a specific one** — the specific one never runs.
- **A pattern replacement in a shell file** — `case` loses its `esac`, and the guard with a
  syntax error answers with a non-zero code, that is, "the edit is refused". After the edit —
  `bash -n`.
- **An edit of a package resource without a build.** The launch line reads the built output, not
  the sources: the order is always one — edit, build, `sync`.
- **The formatter edits the resource on commit, and the layout falls behind after the fact.**
  The laid-out matched at the minute it was laid out, and the resource changed after: the
  formatter rewrites a sample with a fence inside a sample to a longer fence, the resource
  checksum changes, and `sync --check` turns red already on the next step. The way around: run
  the formatter on the edited resource, then `sync`, then commit — or lay out again and add to
  the same commit.
