---
name: python-versioning
description: Use when deciding what version a Python distribution declares and what changes it — a first release, a breaking change, a deprecation, a pre-release, a tag, or the note a consumer reads before upgrading. Owns whether the number is a compatibility promise at all or only a label, the single place it is declared, which change forces which bump, what 0.y.z deliberately withholds, and the canonical form a published version must already be in before a build tool rewrites it silently. What a package root re-exports is `python-packaging`'s, retiring a published identifier is `naming`'s, and choosing a version floor for a dependency this project consumes is the inverse concern and belongs to `python-toolchain`.
---

# Python Versioning — what the number promises, and what changes it

The version a distribution declares, the change that moves it, and the tag and note that make it
reachable. **The number is a claim about compatibility**, so this skill is about the claim first and
the digits second. What the compatible surface actually consists of is `python-packaging`'s; this
skill owns what happens to the number when that surface changes.

**Precondition — something chooses which version to install.** Which rules bind follows from who
reads the number, not from how the project is built:

| Does anything… | If no, these do not apply |
|---|---|
| depend on this by a version range, or install it from an index | rules 6, 7, 8, 9 — no one can be broken by a bump nobody reads |
| have a declared public surface | rules 6, 7, 8 — there is no promise for a change to break |
| publish to an index that refuses re-uploads | rule 11 — a mistake is corrected in place, not outlived |
| ship its members as separate artifacts | rule 13 — one artifact, one number |

**Rules 1, 2, 3, 4, 5, 10, 12, 14 and 15 hold for any distribution at all**, including one deployed
from a commit and installed by nothing. A service that is built from `main` and run in a container has
no consumer choosing a version, so its number is a **label** rather than a promise — it still has to be
single-sourced, canonical and tagged, so a running artifact can be traced back to a tree, and that is
all. Wherever a number moves at all, three limits hold with it, whichever rows above lift rules 6
and 8: it never moves because time passed or because the release was a lot of work; a break never
takes a smaller segment because the right one looks alarming, which only moves the breakage to a
consumer who had no reason to test for it; and a fix never ships as a post-release, which sorts after
the release it names and exists to correct that release's notes.

**A version nobody depends on is a label, not a promise.** Leaving it at `0.1.0` while nothing
installs it by range is accurate, not neglect. What is not accurate is `0.y.z` after something started
depending on it.

## When to use vs. neighbours

- What the compatible surface consists of — what a library root re-exports, and the fact that a
  distributable package's root *is* its public API → `python-packaging`. This skill says which bump a
  change to that surface forces; it does not define the surface. A CLI tool's command line is
  `python-cli`'s (rule 5).
- Retiring a published identifier — a name that escaped the codebase and became an external contract
  is added alongside and retired deliberately, never renamed in place → `naming`. This skill adds that
  the retirement lands in a major, and the deprecation in a minor before it.
- An error `code` that clients and dashboards key on → `exception-catalog` owns its stability; the
  release that retires one is this skill's.
- Choosing a version floor or a pin for a dependency this project **consumes** → `python-toolchain`,
  the inverse concern. A floor states a known breaking boundary in someone else's history; this skill
  is about producing your own. Where a distributed package raises a floor its consumers resolve
  against, the release that carries it is still weighed here.
- A repository holding several distributions — the member split, in-repository dependency edges, tooling
  settled once → `python-workspace`. It governs members; which number each member carries is here.
- Database schema evolution and the migration chain → `persistence` for the rules, and for the files
  the architecture family's data-access skill or the project's own layout. A migration is versioned by
  its own chain, not by the distribution's number.
- A library, an SDK or any distributed package has no architecture family — `architecture-choice`
  names that shape as one this catalogue does not cover, and says the universal skills still bind in
  full. This is one of them, and it binds hardest there: a distributed package is the case where the
  number has readers.

## Template — static declaration, canonical PEP 440

The version is a literal in `pyproject.toml`, changed only in the commit that cuts a release — once
per release, however many changes since the last tag earned it. A commit that is not a release leaves
it alone; bumping as each change lands carries the number past anything that was released.

```toml
[project]
name = "myapp"
version = "0.1.0"
```

Three integer components, no `v`, no hyphen, no plus sign. The pre-release ladder, when one is cut,
is exactly three phases and no others — `1.5.0a1`, `1.5.0b1`, `1.5.0rc1`, then `1.5.0`.

The release is an annotated tag on the release commit, spelled `v0.1.0` (rule 5) —
`git tag -a v0.1.0 -m "myapp 0.1.0"`.

Where the program reports its version — a `--version` flag, a health endpoint — it reads the installed
distribution's metadata (`importlib.metadata.version`, given the **distribution** name, which need not
equal the import package's) rather than a second literal, when asked and never at import
(`python-packaging` rule 8).

## Other bindings

- **The backend reads the number from source** (`dynamic = ["version"]` plus a backend setting
  pointing at a module attribute). The declaration moves into Python and the static `version` key must
  be removed — declaring both is an error every conforming backend raises. Single-sourcing, canonical
  form, the bump rules and the tag are unchanged; what you give up is that the authoritative number is
  no longer readable without running the build.
- **The tag is the declaration** (`setuptools-scm`, `hatch-vcs`). The tag becomes the source of truth,
  so the number and the history cannot drift, and every build between tags is a development version.
  Two settings stop being optional: the local-version segment has to be suppressed for anything
  published, because an index will refuse a version carrying one, and a fallback has to be set or a
  build without repository metadata fails outright. The bump decision, the promise and the note are
  unchanged — only where the number is stored moves.
- **A date-based scheme** (`YYYY.MM.DD`, as several large Python projects use). Rules 6, 7 and 8 lapse
  entirely, because the segments no longer encode compatibility; rule 14 becomes the whole of the
  contract, and it has to be stated loudly, since a reader's default assumption is that the first
  segment means something it does not.

## Rules

1. **Say what the number is a claim about, where a consumer will look.** A version means nothing until
   the surface it refers to is declared; an undeclared surface makes every bump below unfalsifiable.
   `python-packaging` owns what that surface is for a distributable package.

2. **One declaration is the source of truth.** Where the number necessarily appears twice — a
   packaging declaration and a module attribute — one derives from the other, or a test asserts they
   are equal. Two hand-maintained copies drift, and the stale one is the one a reader trusts.

3. **A published version string is already in its canonical form.** Do not rely on a normalizer you
   cannot see run: a non-canonical string is either rewritten silently into something else or rejected
   outright, and which of the two you get depends on the string. The rewrite is the dangerous case,
   because nothing is reported.

4. **Three integer components, always, and nothing else in the release segment.** A two-component
   number compares equal to its three-component form but produces a different artifact filename, so
   both can exist and no resolver can tell them apart. Nothing in the toolchain enforces the arity;
   this rule is the enforcement. No hyphen and no plus sign: a plus marks a locally patched rebuild,
   changes ordering and is refused by public indexes, and identifying a build — a commit hash, a build
   number, a branch — is the tag's and the artifact metadata's job, never the version's.

5. **The `v` belongs on the tag and nowhere else.** In a version field it is ignored and stripped, so
   it is a character that survives review and not the build. A repository whose tags already run
   without it keeps that spelling; one series never mixes the two.

6. **A change that can break a consumer who used only the declared surface is a major** — from
   `1.0.0` on; below it, rule 9 says what it bumps. That includes removing or renaming a name in it,
   changing what a call returns, reordering or retyping its parameters, changing a default that a call
   omitting it depends on, and changing which exception a documented failure raises. Whether the
   consumer *deserved* to depend on it is not the test; whether the surface declared it is. The segment
   follows what changed to the declared surface, within the limits stated under the precondition.

7. **Adding to the surface without changing what is there is a minor, and so is deprecating.** A
   deprecation is a release event of its own: it ships in a minor, at least one release before the
   removal it announces, so a consumer has a version they can move to before the one that breaks them.

8. **A fix that changes no declared behaviour is a patch.** A fix that changes declared behaviour is
   not a patch however small the diff, and a security fix that must break the surface is the deliberate
   exception — take it, and say so in the note rather than pretending the bump was compatible.

9. **`0.y.z` withholds the promise, deliberately, so below `1.0.0` a break bumps the minor.** Anything
   may change at any time there, and that is a legitimate state to ship in while nothing depends on
   you. It stops being legitimate the moment something does. A break moves `0.4.2` to `0.5.0`, as an
   addition does, and a fix moves the patch; no break carries the number to `1.0.0`. Reaching `1.0.0`
   is the act of making the promise — a decision for whoever makes it, never the consequence of one
   breaking change, and not a milestone earned by maturity. `0.y.z` kept while consumers are told the
   surface is stable is neither state: make the promise or withdraw the claim.

10. **A released version is immutable, and so is its tag.** A correction is the next number — never a
    re-upload with corrected contents, never a tag moved to another commit. Where an index refuses to let
    a filename be reused even after deletion, this stops being a convention and becomes the only
    available behaviour — the number is spent whether or not the artifact was right.

11. **Withdraw a bad release rather than replacing it.** The mechanism that marks a release as one
    installers should skip exists for this; deleting it instead breaks every consumer who pinned it
    and frees nothing, because the name cannot be reused.

12. **A pre-release is one of the three phases, and it is invisible by default.** Alpha, beta and
    release candidate are the only pre-release kinds a Python version can express. Ordinary installs
    exclude them unless asked, so publishing one and seeing no uptake is the mechanism working.

13. **Members of one repository version independently.** Lockstep is correct only where a single
    artifact ships them all. A shared library several distributions depend on carries its own number,
    and bumping it is a release its consumers choose to take — which is the whole reason it has one.
    A tag names exactly one released thing, in rule 5's spelling: one `<member>-v<version>` tag per
    member where members are released separately, and one `v<version>` naming an aggregate number where
    one artifact ships every member. That aggregate moves whenever a member does, because its tag is never reused — by a minor
    if any member moved by a minor or a major, by a patch if every member that moved only patched.

14. **State where the scheme deviates, loudly.** Strict compatibility-encoding is not the Python norm,
    and a project that bends it — a minor that may carry a narrow break, a date-based scheme, a `0.y.z`
    kept deliberately — owes its consumers that sentence where they will read it before upgrading, not
    in a commit message.

15. **The release note is written for the consumer deciding whether to upgrade** — what changed to the
    declared surface, what a break asks of them, what is deprecated — never generated from the commit
    log, which records how the work was done and does not answer that question.

## Hard stops

- Asked which version of a dependency this project should require → stop, use `python-toolchain`; a
  floor states a known breaking boundary in someone else's history.
- Asked what a package root may re-export, or what belongs to the public surface → stop, use
  `python-packaging`.
- Asked to rename a published identifier in place → stop, use `naming`; this skill covers the release
  that retires it, not the rename.
- Asked how several distributions share one repository root → stop, use `python-workspace`.
