---
name: selector-map-heal
description: >
  Internal /ace:run step — Repair the mobile selector map from a live failure dump.
user-invocable: false
---

# Selector-Map Heal

## When to run — and when to stop

Read `atlas-report.yaml` from the run folder and branch on `classification`:

| classification | action |
|---|---|
| `unmapped-surface` | **Run this skill.** The map has no anchor on that screen. |
| `matcher-miss` | **STOP.** The element IS on screen; the recipe reached for it wrongly. Fix the recipe. Do NOT add a selector row. |
| `drift` | **STOP.** An anchor moved. Update the existing row via `selector-map-calibrate`. |
| `mapped` | **STOP.** Nothing to heal; the failure is elsewhere. |
| `superseded` | **STOP.** The dump is from an attempt a later dispatch of the same recipe already replaced — quite possibly a passing one. It is stale forensics, not a coverage gap. |
| `non-app-surface` | **STOP.** Every node on that screen belongs to the home screen or system chrome, so the recipe was not in the app at all. The finding is "the app was not foregrounded", not "the map is missing rows" — never author a selector row for the launcher. |

`superseded` and `non-app-surface` exist because both used to read as
`unmapped-surface` (dimagi-internal/ace#1571): a **green** Deliver leg on
`hh-poverty-targeting/20260819-1435` emitted `needs_tier2: true` off a dump
whose 33/33 nodes were `com.google.android.apps.nexuslauncher`, left behind by
an earlier attempt that a later passing dispatch superseded. An unattended
agent following this table would have opened a heal run against the Android
launcher. Both are now filtered in `lib/atlas-drift.ts`
(`test/lib/atlas-drift.test.ts`), so they should reach you only as an explicit
non-verdict — but if you ever see one, it is a STOP, not a heal.

Adding a row on a `matcher-miss` is the inversion that produced
jjackson/ace#811 and #893 — both shipped a new anchor for a screen whose
anchors were fine.

## Guard 1 — additive only

You may ADD rows. You may **never mutate a row carrying a `Live-verified`
note** — that row records a live-device observation, and overwriting evidence
with a fresh guess is the #893 failure class.

This is enforced mechanically, not on trust: `scripts/check-selector-map-diff.ts`
runs in the pre-commit hook and rejects the commit. Do not try to route around
it — if you believe a `Live-verified` row is genuinely wrong, re-verify on a
device and update its purpose note in the same commit.

**Before adding a row, check whether an existing `Live-verified` row already
describes the same physical element.** If one does, adding a sibling row is
NOT the remedy — the guard only checks that the old row's text is untouched,
not whether a new row quietly supersedes it. Believing a `Live-verified` row
is wrong is out of scope for a heal: re-verifying a live observation needs a
device session and a human's call, which is `selector-map-calibrate`'s job,
not this skill's. Stop and escalate with the dump instead.

**Never re-point an existing recipe reference away from a `Live-verified`
row.** Swapping which key a recipe step resolves against is a mutation of
that row's effect performed at one remove — the mechanical guard diffs the
map file, not the recipe, so it cannot see this. If the leg you're healing
already references a `Live-verified` row and it still fails, that failure is
not `unmapped-surface` — go back to the classification table.

## Guard 2 — green or nothing

Propose rows from the dump, apply them, then **re-run the blocked leg
on-device**.

- Green ⇒ open a PR and arm auto-merge (`gh pr merge <n> --auto --merge`).
- Red after 2 attempts ⇒ **stop and file** an issue with the dump attached
  (see § Filing discipline below).

An "attempt" is a materially different hypothesis about the selector — a
different anchor property, a different resolved node, a different row
entirely. Re-running with the same proposed row unchanged, or after only a
cosmetic edit (renaming the key, rewording `purpose`), does not count as a
new attempt and does not reset the counter.

Never ship an unproven row. Shipping a plausible guess is precisely the class
this skill exists to end, and a red re-run is the only thing that can tell you
your guess was one.

### The green must prove the row

A green re-run only counts as proof if the run actually exercised the new
row. Before opening the PR, confirm and state in the PR body:

- **The recipe under test references the new row's key**, and you name that
  key and the recipe step that resolves it. A green re-run that never
  resolves the new selector proves nothing about it — it proves the recipe
  passed some other way.
- **The PR may add a palette step that uses the new row. It may NOT
  otherwise change recipe control flow** — no swapping a selector match for
  a raw coordinate tap, no changed waits or retries, no removed selector
  references. Those are recipe edits, not map healing, and they can turn a
  red run green without the new row ever being proven.
- **If making the leg pass requires any of those, you are not looking at an
  `unmapped-surface`.** Stop, reclassify, and say so in the run notes — a
  recipe that needs rewriting is a recipe problem, and this skill does not
  fix recipes. Patching the recipe to route around a still-red re-run is the
  same "shipping a plausible guess" this skill exists to end, just reached
  through the front door instead of the map file.

### Filing discipline (red after 2 attempts)

Follow this repo's standing filing discipline exactly — this skill's own
trigger class (#811, #893) is proof duplicate-filing here is a live risk, not
hypothetical:

1. **Search first**: `gh issue list --search "<the failing symbol / surface / classification>" --state open`
   before `gh issue create`. If a match exists, comment on it with this run's
   dump instead of opening a second issue.
2. **Label the blast radius**: `blocks-e2e` if the walk cannot complete
   without this row, `harness` if ACE's own tooling is at fault, or `polish`
   otherwise.
3. **Stamp `Feedback-Ref: <record-slug>/<item-id>`** as a trailer if this run
   was triggered by a human's review comment rather than a routine Phase 6
   walk.

## Guard 3 — never cold-boot over a human's emulator

`mobile_ensure_avd_running` kills and wipes the running emulator. Confirm
before cold-booting over an AVD someone may be driving by hand.

## Provenance

Every new row's `purpose` string names the dump file and the run it came from,
so the next reader checks provenance instead of trusting the note. A row that
cannot say where it came from is a guess wearing a citation.

## Why auto-merge is legitimate here

ACE's standing rule is that selector and recipe changes are validated on a live
device before merge. Here the green re-run in Guard 2 **is** that validation,
performed immediately before the merge. This is the one path where self-heal
and the live-validation rule agree rather than conflict — which is exactly why
the loop closes here and nowhere else.

## Resume

After a successful heal (green re-run + merged PR), report the fork parameters:

```
renderForkInvocation({
  oppSlug: <opp-slug>,
  sourceRunId: <current-run-id>,
  forkAtSkill: <blocking-skill-name>
})
```

This prints a parameter block the operator passes to the `fork-run` skill to
fork the current run at the healed skill boundary. The fork uses `fork_at_skill`
(not `fork_at_phase`) so it resumes from the healed skill onward, validating
the fix without re-running the entire phase unnecessarily.

The operator's decision: fork to validate on a fresh run (with upstream artifacts
copied), or proceed with the current run. ACE never forks itself — forking is the
operator's call based on the risk/cost trade-off. See `skills/fork-run/SKILL.md`
for how to dispatch the fork.

**Do NOT fork.** Print the parameters and stop.
