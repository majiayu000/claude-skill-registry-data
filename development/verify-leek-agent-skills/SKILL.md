---
name: verify
description: Exercise a change end to end in the running application (hit the route, run the command, click through the page) and report what actually happened. Use after tests pass, when a change needs proving in the real app, or when another skill's build step ends.
---

# Verify

Tests passing is not the finish line. Exercise the actual flow once, in the running application, and report **what you observed: never what should happen**.

## Process

1. **Pick the flow the change owns.** The route a user would hit, the command an operator would run, the job the system would dispatch, the Filament/Livewire page a back-office user would open. Select a small scenario that can expose the changed behavior: grouped or aggregated UI needs multiple related records with distinct values; interactive state needs the action and its reversal (for example expand, collapse, expand), checking controls and content agree each time. Use existing suitable records or isolated fixtures under the guardrails below. Keep the pass focused on the change, not a broad test suite.
2. **Run it for real.**
   - HTTP / UI: load the URL the app is already served at. For a Laravel app on Herd that is `https://<dir>.test`. Use the project's browser tooling (`agent-browser`, Boost's `browser-logs`) to load the page, perform the action, and screenshot the result. A Pest browser test, including one pointed at `127.0.0.1`, is a test run, not this step. If `agent-browser` fails with `ERR_CERT_COMMON_NAME_INVALID` after `herd secure`, close and reopen the browser session so Chromium reloads the trust store; if a dev toolbar (such as Laravel Debugbar) covers a click target, collapse or disable it rather than forcing the click.
   - Console: run the artisan command with realistic arguments.
   - Jobs / listeners: dispatch through the real path (`dispatchSync` or trigger the event), then check the side effect where it lands, database rows, storage, logs.
3. **Check the seams the tests can't see.** Before driving the flow, watch them under `Monitor` where available: `tail -f storage/logs/laravel.log | grep --line-buffered -E 'ERROR|CRITICAL|Exception'`, plus `php artisan queue:work` when a queued job is involved, so each error arrives tied to the action that caused it. Otherwise read the log tail after each action. Look for browser console errors, the Laravel log (`storage/logs/` or Boost's `read-log-entries`/`last-error`), a queue that needed a running worker, an unbuilt frontend (a Vite manifest error means run `npm run build`, not that the change is broken).
   - **Calculated reports:** for one nontrivial record, reconcile detail rows, totals, badges/status, units, and the selected period against an independent worked example or source records. When adjacent values intentionally use different periods or populations, confirm the UI makes that difference explicit. Record the scenario and observed values; an unexplained mismatch fails verification.
4. **Report faithfully.** What you did, what you saw (status codes, redirects, rendered state, rows written), and anything that surprised you: with the evidence. If a step couldn't be exercised (needs credentials, a webhook, a human), say so plainly instead of marking it verified. List each screenshot's path, so a PR opened later can embed it. Start each step's line with ✅ worked as expected, ❌ broke, or ⚠️ surprised you or could not be exercised.

## Guardrails

- Verify against local/dev: never run mutating flows against a real environment's data without explicit approval.
- Leave no residue: throwaway records created during verification get cleaned up, or created under an obviously-fake identity the seeds already use.
