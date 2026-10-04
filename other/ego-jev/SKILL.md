---
name: ego-jev
description: "Jev (TypeSafe System One) inner loop for ego-browser — one ~0.4 s typed decision per DOM step instead of an LLM turn. Use for multi-step clicking through a semantic page: fill known values into a form, set filters, open a row/card/menu by name, reach a page via nav or site search. Escalates login, payment, free text, canvas and content reading back to you."
license: MIT
metadata:
  version: "0.4.1"
---

# ego-jev

ego executes; Jev decides. Each step: snapshot → number the interactive
elements (a11y refs `@N` + DOM-discovered clickables `dN`: `div` cards,
`cursor:pointer`, iframe/shadow content) → one System One call picks the
operation and its target together → ego clicks/fills/selects. Jev never writes
text and never sees a screenshot.

Read `ego-browser` first for TaskSpace and Page rules; this skill only replaces
the per-step "which element" judgment.

Requires: [ego lite](https://lite.ego.app/) installed and onboarded (provides
the `ego-browser` command, whose Node 24 runtime loads the `.ts` scripts
directly — no build step), the `ego-browser` skill, and `TYPESAFE_API_KEY` or
`AI_GATEWAY_API_KEY` resolvable in that runtime (see [backend and keys](reference.md#backend-and-keys)).

## Task boundary

For ordinary tasks, use only the user's goal, their URL or existing Page,
and provided values. If the goal or starting target is missing from the task
context, ask the minimum clarification needed before opening a Page. Fill
values come from the user; a missing value escalates for clarification.

Author examples, README/demo content and `scripts/selftest.mjs` are examples
or maintenance tests. Run them only when the user explicitly requests a test
or demo; never use them as the default entry or an automatic fallback for
missing credentials. A mock decision does not verify the real Jev service.

## Run

1. Preflight inside `ego-browser nodejs`, before creating a TaskSpace or
   navigating a Page (`SKILL_DIR` is the absolute directory containing this
   SKILL.md). Use the backend options intended for this task:

   ```js
   const { preflightJev } = await import(
     `file://${SKILL_DIR}/scripts/jev-loop.ts`
   );
   const backendOptions = {}; // use the task's supplied overrides, if any
   const ready = await preflightJev(backendOptions);
   if (ready.ok) {
     console.log({ ...ready, next: "continue_jev" });
   } else {
     console.log({ ...ready, next: "pause_jev" });
   }
   ```

   Treat `ready.ok: false` as a result for the agent to handle: pause the Jev
   branch and ask the user once: "Jev 未找到 TypeSafe / Vercel key。你愿意在
   本机安全配置，或说明已有配置的位置吗？也可以不用 Jev，继续普通
   ego-browser 路径。" Ask about configuration or the next step; never request
   or print a plaintext key or automatically change real configuration.
   While awaiting the answer, create no TaskSpace or Page, navigate no Page,
   make no model request and do not poll or retry preflight. If the user has
   already explicitly refused configuration or selected the fallback, reuse
   that choice without asking again. For fallback, continue the same user
   goal, URL/Page and supplied values with plain ego-browser; preserve any
   existing TaskSpace and its ownership. Do not switch to an author test page.

   When the user says a key already exists or is now configured, use its
   location through the supported [lookup](reference.md#backend-and-keys)
   without exposing the value. Recreate any cached `makeAsk` instance or use
   fresh backend options, then rerun preflight in the actual `ego-browser
   nodejs` runtime, not just the shell. Continue to step 2 only after
   `ready.ok: true`; otherwise keep Jev paused and report safe guidance without
   repeating the question or busy waiting. Preflight checks resolvability,
   not key validity, provider health or real Jev availability.
2. Ask the user once, before the first loop of the task: "是否开启网络请求 /
   cookie 记录（`record`）？" Recording is off by default. On yes, pass
   `record: true` (request metadata + cookie metadata only) and add
   `headers` / `bodies` / `cookieValues` / `dir` only when the user asks for
   them. Skip the question when the user already said yes or no, and reuse the
   answer for later loops in the same task. Details, redaction and limits:
   [`reference.md`](reference.md#record-opt-in).
3. Create or resume the task's one TaskSpace following `ego-browser`; reuse
   the user's starting Page or navigate to their URL (`goto` with
   `waitUntil: "domcontentloaded"` on slow sites). Preserve user ownership;
   stop when the user takes control. A backend failure is not a reason to
   create another TaskSpace.
4. Bind `userGoal`, `providedValues` and `verifyUserGoal` from the actual task;
   call the loop with that goal verbatim and the same backend options used
   for preflight:

   ```js
   const { runJevLoop } = await import(
     `file://${SKILL_DIR}/scripts/jev-loop.ts`
   );
   const result = await runJevLoop(page, {
     ...backendOptions,
     goal: userGoal,
     values: providedValues,
     verify: verifyUserGoal,
     // record: true,  // only after the user opted in (step 2)
   });
   ```

   - `values`: Jev picks which key goes in which field by `hint`; a fill with
     no matching value escalates instead of inventing data. Site search needs
     a value too.
   - `verify`: test URL, dialog text or a DOM fact — the thing the goal is
     about. A verify on a heading passes early (link clicked, navigation not
     yet committed) and a verify blind to modals makes Jev loop past a done
     state.
5. Branch on `result.status` — configuration failures return immediately;
   handle missing credentials with step 1's one-time question. Other backend
   failures may retry once and appear in timings:

   | status | meaning | you |
   | --- | --- | --- |
   | `done` | Jev claims visible evidence; `verified` true when your verify passed | read the page and report |
   | `escalate` | missing credentials, login/2FA, payment, upload, delete words, free text, low confidence, target missing, two action errors | `result.reason` names it; for missing credentials use step 1, `handOff` for login, or continue the user's goal with plain ego calls |
   | `blocked` | Jev reports stuck: dead end, nothing offered advances the goal | reason about the page yourself (e.g. the docs have no such page) |
   | `max_steps` | loop bound hit | inspect `result.trace` |

   `result.trace` is per-step `{op, ref, name, opConfidence, targetConfidence}`;
   `result.snapshot` is the last a11y tree. `result.timings` records where the
   time went: `timings.steps` per phase (snapshotMs / domMs / askMs / actMs /
   verifyMs / stepMs) and `timings.llmCalls`, one entry per System One request
   (`{seq, step, kind, ms, ok, model, usage}` — retries and option_retry
   included; `timings.model` names the serving model version, e.g.
   `jev-1.13.0`). `timings.planner` names the driving agent — env detection
   only finds the harness, so pass `planner: "<harness>/<model>"` (your own
   model id) for full attribution. Show the user the latency table once the
   loop exits:

   ```js
   const { formatTimings } = await import(
     `file://${SKILL_DIR}/scripts/jev-loop.ts`
   );
   console.log(formatTimings(result));
   ```

   If the default backend cannot resolve credentials, `runJevLoop` also stops
   before page/recording calls: `escalate`, `steps: 0`, empty timing step and
   LLM call arrays. That configuration check is not a model request.

With `record` on, `result.record` holds `network` (one entry per XHR / fetch /
document request, tagged with the `step` whose action caused it) and `cookies`
(`before` / `after` / `diff`); print it with `formatRecord(result)` (same
module) or query the arrays directly. Recorded endpoints can be replayed with
`page.fetch()`, which carries the page's cookies.

Done when the page state your goal describes is confirmed by `verify` or your
own `page.evaluate` — Jev's `done` is a claim, the check is yours. Complete
TaskSpace cleanup exactly once under `ego-browser`'s user ownership and
`finish({ keep })` rules; an error or user handoff is not successful completion.

## Gotchas

- A click on a `target=_blank` link opens a new Page; the loop stays on the
  old one and escalates on the unchanged page. Continue on the new label.
- Collapsed menus and teleported dropdown options are not in the DOM until
  opened: click/hover the parent first, then enter the loop. `select` on a
  `dN` target escalates by design.
- Jev will click "Continue with Google" on a login page; keep login pages out
  of the loop or `handOff` first.
- Semantic filtering ("not in the list → switch to All") is planner work; a
  `blocked` there is correct, not a bug.

## Reference

- Options, thresholds, backend/keys, latency numbers: [`reference.md`](reference.md).
- Explicit test/demo requests only: [maintenance tests](reference.md#maintenance-tests)
  describes the mock-decider selftest and its real browser/external-site dependencies.
