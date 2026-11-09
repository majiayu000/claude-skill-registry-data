---
name: web-feature
description: "Feature or feature-change playbook for React, Next.js and TypeScript web apps: intake, pattern discovery, plan, implement, tests, browser check, review, commit."
---

Read the project AGENTS.md (or GEMINI.md) and applicable guidance first. Fall back to CLAUDE.md if AGENTS.md is absent. Follow global rules for optional tools, specialist subagents and Git actions.

# Feature work: the user request

Repo facts (package manager, framework and router, scripts, test runners, design system, dev URL) come from the project's `AGENTS.md` (or `GEMINI.md`). Never guess them.

Skills named below are optional companions. When one is missing, follow `references/companions.md` in the `web-standards` skill and continue.

1. **Intake.** If an Atlassian MCP tool is available, fetch the Jira ticket and quote its acceptance criteria. Otherwise
   restate the goal in three bullets plus an out-of-scope list. Branch `feat/<ticket>-<slug>` (or the project's documented branch convention) off the default branch.
2. **Discover the pattern.** Use a research subagent to find the closest existing route or flow: its page or route
   segment, components, data fetching or server actions, state, and tests. Note whether it uses the App Router, the
   Pages Router or plain React, and which test runners it has. For a *modify* task also map every caller of the code you will change.
   If it changes UI, capture the touched routes now, the same way as step 7, and label them `before`.
3. **Consult references.** Load the `web-standards` skill for the sources and house patterns. Ask `web-researcher` only where
   guidance may have moved (framework major versions, rendering and caching defaults, deprecations).
4. **Plan.** Files to add or change, the state model (one discriminated union per screen: `loading`,
   `loaded`, `empty` where the screen can be empty, and `error`), the server or client boundary of each new component,
   where data code goes, the test list and the browser checks. For UI changes, consult `/design-standards` (tiered design rules, screen states, accessibility). Follow the project's architecture rules. Proceed within the user-authorized scope. Ask only about unresolved scope or consequential choices.
5. **Implement** in small steps, running the project's type check after each. New UI uses the project's design-system components and tokens and follows the design rules (WEB-1 landmarks, A11Y-1 contrast, A11Y-5 targets, TYP-5 text spacing). Components stay pure. In the App Router, Server Components stay the default and `'use client'` goes on the smallest interactive component. Add no dependency without approval.
6. **Tests.** Follow the web-kit testing rule, or the Testing section of `references/official-docs.md` in the `web-standards` skill when the rule is not installed. Hooks, data functions and component behaviour get unit or component tests with Testing Library. A new user journey gets a Playwright test when the repo already has Playwright. Otherwise write or update its journey in `journeys/`, run it in step 7 and list the missing Playwright test as a follow-up. Run the tests with a file filter and quote the summary.
7. **Browser verification.** `/web-run-app` starts the app and captures the touched routes at phone and desktop
   widths. Then hand off to the `web-verifier` agent with the test commands, the dev URL, the routes and the journey file(s)
   for the touched flow. For a new or changed screen, also ask for dark-mode captures, which A11Y-1 needs. It returns test
   totals, the JSON journey result and screenshot paths, so the images stay out of this session. A failure is a finding, not something to fix inside this step.
8. **Review.** `web-reviewer` against the acceptance criteria, and delegate UI changes to `ui-reviewer` with the labelled step 7 screenshot paths. Confirm each Blocker and Major against the code first, and decline a refuted one with the counter-evidence. Fix the rest, then re-run the type check and the affected tests. Send the same reviewer the finding IDs and their "Verified fixed when" criteria to re-review the fix delta. Stop after two re-review rounds and report anything still open. List declined Nits.
9. **Commit, only if asked.** Follow the shared Git conventions. Do not push unless asked.
10. **Report**: files changed, commands run with results, screenshot paths, what is left for QA.
