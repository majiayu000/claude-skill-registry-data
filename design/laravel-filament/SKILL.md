---
name: laravel-filament
description: "Use when writing, reviewing or upgrading Filament code (panels, resources, forms and schemas, tables, actions, relation managers, widgets) in a Laravel app: find the installed major first, apply the version-independent rules, and verify every signature against that version's documentation instead of writing it from memory."
---

# laravel-filament

Step 6 of the pipeline (`WORKFLOW.md`). Filament's API changes between majors, so the same snippet is right
on one and wrong on the next. The discipline of this block is the order: **version first, then rules, then a
signature read from that version's documentation**. It deliberately carries no per-version syntax: that
would be a copy of documentation that goes stale with the next release.

**Special status.** New block, 🟡, "base to confront with the first real change": never run on real work in
house. The version and policy facts below were re-read in Filament's own 5.x documentation on 2026-10-20;
re-read before relying on one (`skills/source-freshness`).

## When
A file under a Filament panel's resources, pages, widgets or relation managers; a question about a Filament
component; an upgrade of the package.

## Steps
1. **Detect the installed major before writing anything.** Read the resolved version (`composer show
   filament/filament`, or the application's `about` output, or the lock file), the constraint only tells the
   intended range. If Filament is absent, ask which major is wanted. If the version cannot be determined, ask:
   never guess.
2. **Read the matching documentation for that major** (`filamentphp.com/docs/<major>.x`) before using a
   namespace, a class or a method signature. Verified here: a path valid on one major can 404 on another.
   State the detected version at the top of the answer, and label code with it.
3. **Know where the real break is.** As of the 2026-10-20 reading, the 5.x documentation presents v5 as the
   v4 line moved to Livewire 4: the upgrade guide lists PHP 8.2+, Laravel 11.28+, Livewire 4.0+, Tailwind CSS
   4.0+ (the installation page lists Tailwind 4.1+ and no Livewire line: take the stricter figure), upgraded by
   the vendor's upgrade package and a version-named script, followed by a manual review of what it changed. Third-party plugins may lag a major and are removed from the constraint until they catch up. The
   operator runs the upgrade commands themselves (`CONVENTIONS.md`: a block installs nothing).
4. **Authorisation is a policy, not a hidden button.** Filament observes the model's registered policy:
   `viewAny` governs the resource's visibility in navigation, `create`, `view`, `update` and `delete` the
   matching operations, and bulk actions use the `*Any` variants (`deleteAny`, `forceDeleteAny`,
   `restoreAny`) unless per-record authorisation is switched on (`authorizeIndividualRecords()` on the bulk
   action). Two traps the documentation states: `viewAny` hides the resource but does **not** filter which
   records the table lists (that is step 5), and a missing policy or method means the operation is allowed
   unless a gate `before` callback denies it, so turn on the strict authorisation mode to surface a missing
   policy (custom actions and inline editable columns still need their own check). Write the policy for every
   resource and test the denied paths (`skills/laravel-permissions-not-roles`: check permissions, not role names).
5. **The base query is the one place to shape reads.** Every query of a resource starts from its Eloquent
   query method: put tenant or visibility constraints and eager loading there, and prefer counts over loading
   a collection for a badge (`skills/laravel-no-queries-in-loops`). That query feeds the list table, the record
   pages and the global search. Removing a global scope there (`withoutGlobalScopes()`) is a decision to be
   named in review, never a convenience (own guidance).
6. **Editing is bounded by the form, but exposure is not.** Per the documentation only attributes with a form
   field are editable, and it calls the browser exposure of attributes "not an issue with mass assignment", so
   mass assignment is not the risk it points at. Model attributes are exposed to the
   browser's component state unless hidden: add secrets and binary, geometry, point and blob columns to
   `$hidden` (documented: otherwise the page can fail to load with a blank screen and nothing in the log;
   expose the value through an accessor if it is needed). On the edit and view pages an attribute can also be
   removed from the browser state in `mutateFormDataBeforeFill()`.
7. **Server-side validation lives in the schema.** Field rules are real validation; nothing from client state
   is trusted.
8. **Keep a resource declarative.** It reads as configuration. Logic goes to the model, an action class or a
   service (`skills/laravel-no-fat-models`, `skills/laravel-conventions` §1). Prefer a relation manager to a
   hand-built nested form for one-to-many and many-to-many editing.
9. **Test panels as Livewire components.** Pages, relation managers and widgets are tested through Livewire's
   test helpers (the documentation shows Pest with its Livewire plugin and says to swap in `Livewire::test()`
   for PHPUnit); resources, schema components and actions are non-Livewire classes tested by calling their
   methods. Authorisation and authentication in tests are not covered by that page: write them explicitly.
10. **Match the ecosystem versions.** Each major pins Laravel, Livewire, Tailwind and PHP ranges; a mismatch on the Livewire or
    Tailwind major is the first thing to check when a panel does not render.

## Output / checkpoint
The answer or diff names the detected major, every Filament signature in it was read from that major's
documentation, and each resource has a policy with a denied-path test. Checked at `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. Never copy a snippet from another major, a blog or a model's memory without
the check in step 2. An upgrade is run in a branch with the vendor's automated script first and the manual list
second, never by hand-editing a hundred files.

## Origin
Version-detection discipline and the stable principles rewritten from the `laravel-filament` skill of
`majdghithan/agent-skills` (MIT per the repository metadata, read 2026-10-20). Its per-version syntax references
are left out on purpose. Facts re-read from Filament's own 5.x documentation on 2026-10-20 (the framework
repository itself is MIT, LICENSE read): the upgrade guide (new requirements, automated upgrade script, plugin
caveat), the installation page (requirements), the resources overview (Authorization and Policies, Eloquent Query
and Global Scopes, Model Attribute Exposure, Binary and Non-UTF-8 Columns, Mass Assignment) and the testing
overview (Livewire helpers, Pest or PHPUnit, which classes are Livewire components). The public skill advises
guarding mass assignment; the documentation does not, so step 6 follows the documentation. Still unsourced
reasoning of ours: step 5's "name a removed scope in review", steps 7 (field rules as the only trusted
validation) and 8 (declarative resource; relation manager preferred to a nested form: the overview does not
compare them) and 10. Mechanisms only, rewritten in our words.

Independent verification 2026-10-21: 14 checked, 14 matched, 0 corrected, 0 unverified (read against the 5.x branch; a 6.x documentation branch also exists at this date with PHP 8.3+ and Laravel 12.0+, no 6.x release tag).
