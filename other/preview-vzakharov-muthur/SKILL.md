---
description: "STUB — not yet hydrated for this project. Render a visual change and actually look at it, instead of judging appearance by reading code. Hydrate this file against the project's UI stack and dev-server setup before invoking it."
---

> ⚠️ **STUB.** This skill has no working procedure yet. Before it can be
> invoked, fill in: how to mount a component or page in isolation, how to boot
> the app without real credentials, how to drive a browser and capture images,
> and where the captures go. Delete this banner once you have. If the project
> has no visual surface, delete the skill instead.

## What this skill is for

Looking at a visual change with your own eyes before claiming it works.

The failure mode this exists to prevent is specific and common: reasoning about
appearance by reading the code that produces it. Spacing, overflow, contrast,
and how something reflows at a narrow width are not reliably derivable from
source — they have to be rendered and observed.

## Concerns that hold regardless of stack

Each is something a hydrated version must handle.

### Isolation

Mount the thing under test on a scratch route or story that doesn't require
navigating the real app to reach it. Reaching a deep UI state through six clicks
makes the check expensive enough that it gets skipped.

### Boot without secrets

The preview has to come up against placeholder config — stub credentials,
fixture data, whatever it takes. A preview that needs production keys is one
nobody runs. Say plainly which parts are faked, so an observation about them
isn't mistaken for an observation about the real thing.

### Several widths

Capture at more than one viewport. Most layout defects are width-dependent, and
a single desktop screenshot is exactly the evidence that misses them. Pick the
breakpoints the project actually claims to support.

### Every colour scheme the app serves

When the change is a colour, one scheme's screenshot is half the evidence: a
value that reads correctly against a dark surface can be invisible against a
light one. Don't expect the VM's OS preference to get you there — an app that
picks its scheme from an explicit attribute or storage key, with one hardcoded
default, serves that default no matter what the machine prefers. A hydrated
version takes the scheme as an argument, seeds it before the first paint so
nothing is captured mid-transition, and puts it in the filename so one scheme's
shots don't overwrite the other's.

### Keep artifacts out of the merge

Screenshots are for the operator now, not for the repo forever. Put them under
gitignored `tmp/`, or under `docs/remove-before-merging/` when they need to ride
the branch for review — `/finalize` sweeps that tree before the PR goes ready.
Never leave image files to land on the trunk.

### Report what you saw, not what you rendered

"Captured 3 screenshots" is not a finding. Say what the images show and whether
it matches what was intended, and surface the ones that don't.

## Related

`/qa-checklist` classifies some verification steps as `manual-only` precisely
because they need a human's eye on pixels; a hydrated `/preview` is what lets
you close some of that gap yourself.
