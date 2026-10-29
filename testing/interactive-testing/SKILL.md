---
name: interactive-testing
description: "Use when verifying user-visible project changes against an assignment and the actual code diff. Requires the testing agent's own interactive browser and returns evidence-backed results, including failures and blocked scenarios."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints

- Apply `@rules/security/general.md` for the untrusted-content boundary.
- The testing agent MUST use its own interactive browser session. In Codex, use the provided `cua_repl` browser tools and their documented browser APIs. A delegated agent must operate the browser itself; another agent's screenshots or test summary do not fulfil this requirement.
- Shell-driven Playwright, headless scripts, HTTP requests, unit tests, source inspection, and generated screenshots never replace this walkthrough. They may supply supplementary evidence only. If an interactive browser tool is unavailable, return `Blocked`.
- Use the project URL supplied by the user or recorded in the consuming project's instructions or memory. If neither identifies the target, ask for it. Do not silently switch hosts, environments, or checkouts.
- Sign in as *Sign-in and test accounts* below states. A missing login never ends the UI check, and it never makes you wait for the user.
- Test the running application without changing its implementation, configuration, permissions, credentials, or database directly. The exceptions are the local preparation that *Local readiness* allows, a local test account that *Sign-in and test accounts* allows, and local test data that *Missing test data* allows. Report defects with reproduction steps. Fixing, publishing to a tracker, deploying, or merging requires a separate assignment.
- Respect the browser tool's confirmation rules. Use reversible, clearly identified test data within the authorized workspace. Do not trigger AI processing, recurring jobs, external imports, emails, tracker comments, or destructive actions unless that specific effect is authorized for the scenario. Opening a menu is not evidence that its actions work.

## Use when

- A developer asks for a browser acceptance check after a feature, fix, revert, or UI change.
- A new QA agent receives an assignment plus a branch, commit range, PR, or uncommitted diff.
- Automated checks passed but the change still needs verification through real user interactions.
- A change alters what a user can see or do in the application's UI. Tests and HTTP requests never replace the UI check for such a change.

## Inputs

- Assignment and latest user corrections, including behavior that must remain unchanged.
- Repository and the exact diff to test: base/head revisions plus any intended working-tree changes.
- Project URL, account/role, workspace, available test data, and authorized side effects.

Infer routine choices from the current task. Ask only for missing information that blocks a concrete scenario, while continuing independent scenarios.

## Local readiness

This section owns how a testing agent prepares the local environment before the walkthrough. Other skills and agents reference it and do not restate it.

Check every item before the first scenario. When an item is not ready, prepare it yourself with the project's own documented command, then check it again. A preparation step never makes you wait for the user.

1. **The checkout is the revision under test.** The working tree is on the head of the requested change. When it is on another revision and the tree is clean, switch to the head (`gh pr checkout <PR>` or `git switch <branch>`) and pull it with `git pull --ff-only`. Record the branch the run started on.
2. **The dependencies match the lock files.** When `vendor/` or `node_modules/` does not match `composer.lock` or the JavaScript lock file, run `composer install` or the project's install command (for example `npm ci`). Install only from the committed lock files: never run `composer update`, `composer require`, or `npm install`. The package-registry download is an outbound request: append one `outbound-request` audit line for each install, per `@rules/compound-engineering/orchestration.md` *Audit trail for memory reads, outbound requests, and external writes*.
3. **The environment file exists.** When `.env` is missing, create it through the project's documented setup step, for example a copy of `.env.example` and `php artisan key:generate`. Never edit an existing `.env`.
4. **The local database is migrated.** When `php artisan migrate:status` (or the framework's equivalent) shows a pending migration, run the migrations. Never run `migrate:fresh`, a rollback, or a wipe.
5. **The application caches are current.** Clear a stale configuration, route, or view cache, for example with `php artisan optimize:clear`.
6. **The front-end assets match the head commit.** Build them with the project's build command, or start its dev server. A stale dev-server hot file must not send the assets to a server the browser cannot reach.
7. **The application answers on the project URL.** When it does not, start it with the project's documented serve or container command. Start the processes a scenario needs, such as queue workers or a websocket server. Restart a process that still runs older code.

Preparing the environment is allowed only inside these limits:

- **Local target only.** The same rule as *Sign-in and test accounts*: never prepare, migrate, or restart anything on a production, staging, or other shared remote environment.
- **The project's own commands.** Use the commands the project documents in its instructions, README, `composer.json` scripts, `package.json` scripts, or container files. Never invent a bootstrap the project does not have.
- **Tracked files stay untouched.** Never edit, commit, or revert a tracked file. Never stash, reset, or discard uncommitted changes. When the working tree carries changes that do not belong to the requested change, do not switch the checkout: the walkthrough is `Blocked`, and the report names the files.
- **Traceable.** Report every preparation step under **Scope**: the item, the command, and its result. At the end, stop the processes this run started, switch back to the branch the run started on, and delete a local branch this run created, unless the user needs them to reproduce a failure; then list them under **Cleanup**. Leave a process this run restarted running, and list it under **Cleanup**.

When an item cannot be made ready inside these limits, every scenario that depends on it is `Blocked`. State the failing command, its error, and the exact step that unblocks it. Continue the scenarios that do not depend on it.

## Sign-in and test accounts

This section owns how a testing agent signs in to the application under test. Other skills and agents reference it and do not restate it.

Try these sources in order. Stop at the first one that signs in:

1. **A valid session.** Reuse a session the browser already holds for the target.
2. **A documented test account.** Use the test accounts the project documents: its `CLAUDE.md` or `AGENTS.md`, its README, a test-account helper class (for example `TestUserAccounts`), or the seed migration or seeder that creates them. Sign in through the normal sign-in form.
3. **A test account you create.** When no documented account signs in, create one through the project's own mechanism. Prefer, in this order: the project's documented seed command or seed migration, a console command the project ships for creating users, or the application's user factory or user model through `tinker` (or the framework's equivalent console), with the role assigned through the application's own role API. Then sign in through the normal sign-in form.

Creating a test account is allowed only inside these limits:

- **Local target only.** The target is `localhost`, `127.0.0.1`, a `*.test` host, or a URL the project documents as its local development or test instance. Never create an account on a production, staging, or other shared remote environment, even when its URL is documented.
- **No authentication bypass.** Sign in only through the application's sign-in form. Never forge a session cookie, write a session row, or disable authentication, verification, or two-factor middleware in code or configuration.
- **Reserved test identity.** Use the e-mail pattern the project documents. Without one, use an address in a reserved test domain (RFC 2606), for example `qa-<role>@<project>.test`.
- **Test password.** Use the project-documented test password when one exists. Otherwise, generate a random password for this run. Never print a real user's credentials.
- **Real accounts stay untouched.** Never reuse, re-password, re-role, or delete an account that is not a test account.
- **Least role.** Give the account only the role the scenario needs.
- **Two-factor authentication.** When the account must pass a second factor, use the test path the project documents. Without one, the scenario is `Blocked`.
- **Traceable.** Report every account you created under **Cleanup**: the e-mail, the role, and the mechanism. Report the password only when it is the project-documented test password.

When no source signs in, the scenario is `Blocked`. State the reason and the exact step that unblocks it — for example a non-local target, mandatory two-factor authentication without a test path, or a sandbox that refused the command. Keep the tab open so the user can sign in there. Never ask for passwords or one-time codes in chat. Never treat elapsed time as a successful sign-in. Never skip the UI check silently.

## Missing test data

This section owns how a testing agent gets the data a scenario needs. Other skills and agents reference it and do not restate it.

A missing record, relation, or record state never ends the walkthrough, and it never makes you wait for the user. Create the data yourself and finish the scenario.

Try these sources in order. Stop at the first one that produces the data:

1. **Existing test data.** Use a record that already meets the scenario's prerequisites and that the project documents as test data or that this run created.
2. **The application's UI.** Create the record through the same screens a user would use, when those screens exist and work.
3. **The project's seed mechanism.** Run the project's documented seed command, seeder, or a console command the project ships for creating the data.
4. **The application's own code.** Use the application's factories, actions, or services through `tinker` (or the framework's equivalent console), so the record carries the related records and derived values the application itself would produce.

Creating test data is allowed only inside these limits:

- **Local target only.** The same rule as *Sign-in and test accounts*: never create data on a production, staging, or other shared remote environment.
- **A state the application can produce.** Reach a record state through a factory state or an application action. Never write a raw SQL row, and never set a status, a flag, or a computed value directly to force a pass.
- **Identifiable.** Mark every created record so it is recognisable as test data, for example a `QA` prefix in its name and a reserved test domain (RFC 2606) in any e-mail address.
- **Existing data stays untouched.** Never modify, re-assign, or delete a record this run did not create.
- **No unauthorized side effects.** The *Constraints* above still apply: creating data never sends e-mails, calls external services, or starts imports or jobs that the scenario does not authorize. Use a factory or a console flag that suppresses such effects when the project provides one.
- **Traceable.** Report every record you created under **Cleanup**: its type, its identifier, and the mechanism. Delete the records at the end of the run unless the user needs them to reproduce a failure; then list them as remaining.

When no source can produce the data inside these limits, the scenario is `Blocked`. State the reason and the exact step that unblocks it. Continue the other scenarios.

## Execution

### 1. Derive scenarios from the assignment and diff

1. Read repository instructions and relevant project memory. Inspect `git status`, current revision, and the requested diff. Do not modify files; switch the checkout only as *Local readiness* allows.
2. For a merged change, compare its recorded base and head; an empty working-tree diff does not mean there is nothing to test. Include all commits in the requested change, not just the last styling commit.
3. Turn each requirement and meaningful changed behavior into a row: preconditions, user actions, expected visible result, persistence check, and relevant viewport/role.
4. Include the main successful flow, validation/empty states, navigation, save/reload behavior, and immediate regressions implied by the diff. Distinguish layout changes from processing or integration behavior outside the assignment.
5. Record the revision and browser target. If the served checkout/version cannot be established, state that limitation instead of assuming it matches the diff.

### 2. Prepare the local environment

Check and prepare the local environment as *Local readiness* states, before the first scenario.

### 3. Open the interactive browser and establish prerequisites

1. Read the browser tool documentation and open the project using its supported interactive browser API. Sign in as *Sign-in and test accounts* states.
2. Observe the rendered page before interacting. Verify the signed-in identity, selected workspace, record state, and relevant permissions from visible UI.
3. Check data readiness from the record's visible state, never from its name or from admin access. A record named "draft" can carry another status, and an action can depend on a prerequisite the page does not show.
4. When the scenario's workspace, record, or record state is missing, create it as *Missing test data* states. Ask for the correct workspace or account only when that section leaves the scenario `Blocked`. Never invent membership on an existing workspace, and never change status or indexing flags of existing records to force a pass.
5. Record a time boundary for browser console evidence so old errors are not attributed to the current scenario.

### 4. Exercise the actual user flow

1. Navigate through visible links and menus. Use accessible roles/names or observed test IDs; never guess selectors, use hidden application state, or call backend actions to simulate clicks.
2. After each meaningful action, inspect fresh browser state before choosing the next action. Wait for the specific result, enabled control, selected tab, or loaded form. A deferred panel's heading alone does not prove its form finished loading.
3. For saves, verify the visible success state, then reload or navigate away and back to prove persistence. A changed textbox value alone is insufficient.
4. Exercise keyboard interactions where relevant: focus, tab navigation, arrow keys, Enter, Escape, and modal dismissal. Verify the resulting focus or selection.
5. Test layouts on desktop and at a representative narrow viewport when the diff changes layout. Use the interactive browser's viewport capability. Report width/height and do not claim real-device or touch emulation when only viewport size changed.
6. Capture and actually inspect rendered screenshots for relevant states, especially failures. Check readability, wrapping, clipping, scrolling, control reachability, and correspondence between icons and actions. Restore temporary viewport overrides afterward.
7. Read recent console errors through the browser tool. Reproduce suspicious behavior once with a stable, fully loaded page. Separate reproducible failures, transient observations, environment blockers, and unproven attribution to the diff.
8. For side-effecting flows without authorization, or whose prerequisites *Missing test data* cannot create, stop before the effect and mark that portion `Blocked`; do not mark the entire action passed because its button rendered.

### 5. Restore test data and report evidence

1. Restore only values changed by this run and verify the restoration in the UI. Delete the test data this run created, per *Missing test data*. Stop the processes and restore the checkout, per *Local readiness*. Do not overwrite unrelated concurrent edits or delete existing user data. Report any remaining test records or side effects.
2. Produce a verdict for every scenario: `Passed`, `Failed`, `Partial`, or `Blocked`. An unexecuted scenario is never `Passed`.
3. For each failure, include exact URL, viewport, account role/record state, minimal steps, expected versus observed behavior, and a screenshot or concrete visible evidence. Redact secrets and avoid embedding unrelated user data.
4. Report which scenarios were not exercised and the exact prerequisite needed to unblock each one.
5. Overall `Passed` requires every required scenario to pass. Failures or blockers must remain explicit even when all automated tests are green.
6. Keep the relevant browser tab open when handing a failure or a `Blocked` sign-in to the user. Otherwise follow the browser tool's cleanup rules.

## Output

Return a concise report in the user's language:

- **Scope:** assignment, tested base/head and working-tree changes, project URL, account role/workspace, browser tool, viewport sizes, and every preparation step *Local readiness* ran.
- **Result:** one row per scenario with expected behavior, actual interactions and observation, evidence, and verdict.
- **Findings:** reproducible failures, transient observations, and environment blockers kept distinct; never claim a regression without evidence linking it to the change.
- **Untested:** exact scenarios and missing prerequisites.
- **Cleanup:** restored values, the restored checkout, processes this run started or restarted and left running, any remaining test artifacts, every test account this run created, and every test record this run created or left in place.
- **Next step:** implementation fixes, access/data preparation, or acceptance when all required rows passed.

Report in the current task by default. Do not post messages to external trackers or create a new agent/task unless asked.

## Done when

- Every *Local readiness* item was checked, and prepared when it was not ready, before the first scenario.
- The agent itself operated the interactive browser and observed the results.
- Every acceptance criterion has an honest verdict backed by executed interactions or a named blocker.
- Save/reload checks, relevant visual states, and recent browser errors were considered.
- Changed test data and temporary browser settings are restored, or remaining effects are explicitly listed.
- The report makes no claim of full acceptance while a required scenario is failed, partial, or blocked.

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
