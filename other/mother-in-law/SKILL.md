---
name: mother-in-law
description: Test a changed user interaction for realistic sequence failures such as double submission, stale responses, navigation, and recovery; use for interaction QA rather than general code review.
---

# Mother-in-law

> And what happens if I click it twice?

Read supplied requirements, interaction code, native tests, existing test support
and applicable project instructions together when practical. Discover missing
paths, not another inventory before known-file reads.
Use controlled responses/clocks, isolated cases, bounded waits, and owned-operation
cleanup—never sleeps or production actions. Preserve user files and scope.

Derive expected states from the product contract, not today's implementation.
Separate final ownership from interval requirements. “Retain while loading” or
“until the latest completes” applies throughout that interval: assert the retained
value after relevant intervening completions while the latest remains pending,
not only at request entry. Printing an observation is not a regression assertion.
If only final ownership is required, leave unspecified intermediate display as
observation; seeing an older response does not require a valid fix to display it.
A regression must reject the fault without rejecting another permitted path.

Choose the requested deliverable; load only its relevant support:

- **Project regression:** extend and run the native test directly, not a disposable
  probe first. Reuse adequate project fixtures and covered cases; skip transport
  and probe references when that support is already present. Only when additional
  Python request-control support is needed, read the [native-test interface](references/native-tests.md)
  and [copiable transport](assets/controlled_fetch.py) together. An installed-helper
  command or saved JSON is not a standalone project regression.

- **Captured observations without a project-test deliverable:** the optional
  [component probe](references/component-probe.md) fits a zero-argument constructor,
  async `run(query, fetch)` and direct payload state. An opt-in mode checks required
  display retention through normal/reversed overlap; repeated identical overlapping
  queries still require project checks. Existing adequate runners take precedence.
  Never change production to fit a helper. Native-project delivery does not need
  this reference.

- **Rendered UI:** read [references/browser.md](references/browser.md).

Return the tested sequence, expected/observed state, tested layer, and complete
bounded command. Stop after the nearest normal and targeted adversarial cases.
Do not add separate evidence files when captured check output already proves them.
Browser unavailability leaves browser QA incomplete. QA does not authorize a fix.
