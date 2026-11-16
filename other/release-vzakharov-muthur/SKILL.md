---
description: "STUB — not yet hydrated for this project. Cut a release: bump the version, collect the notes, open the release PR, and arm or ship the deploy. Hydrate this file against the project's actual versioning and deploy setup before invoking it."
---

> ⚠️ **STUB.** This skill has no working procedure yet. Before it can be
> invoked, fill in: the version scheme and where the version lives, the
> branch/PR shape a release takes, what merging a release actually does, which
> gate must be green first, and the commands for each. Delete this banner once
> you have.

## What this skill is for

Taking the accumulated work on the trunk and turning it into a named, shippable
version — one that a human can point at afterwards and say what was in it. It's
the routine that makes "we released" a repeatable act rather than an improvised
one.

## Concerns that hold regardless of stack

These are what a hydrated version has to answer. They're stated as questions
because the answers are project-specific, but every project has an answer, and
leaving one implicit is how release procedures rot.

### Version scheme

Semver, date-based, or a running integer — and where the number lives (a
manifest, a tag, a file the build reads). If release branches share a prefix
(`release/*`), treat that prefix as **reserved**: nothing else may create a
branch under it, or the release automation fires on ordinary work.

### Notes per version

Each release gets its own notes file or section, written for someone who wasn't
in the room. Decide where it lives and whether it's assembled from commits or
written by hand — assembled-from-commits only works if commit subjects are
disciplined enough to read as notes.

### Arm vs. ship

Does merging the release _arm_ a deploy (someone still presses a button) or
_ship_ it (the merge is the deploy)? This single fact changes what the skill
owes the operator: an arming release ends with "here's what to press"; a
shipping release ends with verification that the thing is live.

### Tag or no tag

If deploys are driven by tags, the tag is the release and creating it is the
act. If they're driven by branch merges, a tag is optional bookkeeping — decide,
rather than half-doing both.

### The gate

Name the one check that must be green before a release is armed, and make the
skill refuse to proceed without it. "The usual checks passed at some point" is
not a gate.

### Who owns the bump

Whether the agent bumps the version or the operator does. If the agent does, say
what stops two concurrent releases from claiming the same number.

## Related

Once hydrated, `/squash-message` already accommodates a release: its Step 3
exempts a release body from the three-paragraph cap, expecting a paragraph per
product area instead. `/hotfix` is the sibling procedure for when the trunk
isn't safe to ship from.
