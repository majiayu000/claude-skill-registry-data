---
name: feature
description: The required loop for every change to Brain Games. Use for any new feature, bug fix, game port, UI tweak, or requirement change, and whenever the user types /feature <description>. Plan, get approval, write failing specs, implement, check, verify the UI against docs/design.html, review, then ask before committing.
---

# /feature: plan, red, green, verify, review

Run these steps in order. Do not skip a step. Do not start the next step until the current one is done.

Input: `$ARGUMENTS` is the request. If it is empty or vague, ask the user with AskUserQuestion before step 1.

## 1. Read

1. Read `CLAUDE.md` (rules 1 to 13 and the porting list).
2. Read the sections of `docs/functional-requirements.md` that the request touches.
3. Find the matching part of `docs/design.html`. For a game, read `RUN.<id>`. For a page, read its `render*` function and the CSS it uses.
4. Read every file you plan to change, and its spec under `test/nuxt/`.
5. If the request changes a product rule, draft the exact edit to `docs/functional-requirements.md`. It goes into the plan in step 2. The requirement changes first, then the tests, then the code.

For a game port, also follow the `port-game` skill.

## 2. Plan and get approval

Write a short plan:

- Goal in one sentence.
- Requirement edit (if any), quoted.
- Files to add or change, with `file:line` where it helps.
- Specs to add or change, per the path rule: `app/<path>/<Name>.<ext>` → `test/nuxt/<path>/<Name>.spec.ts`. List the behaviours each spec will check.
- UI touched: routes and components, or "none".
- Risks and open questions.

Ask for approval with AskUserQuestion. Offer "Approve", "Change the plan", and "Stop". Write no code before the user approves.

## 3. Red: failing specs first

1. Spawn the `test-writer` agent. Give it the approved plan, the requirement sections, and the spec paths. Tell it the code does not exist or is not changed yet.
2. When it returns, run the new specs yourself: `npx vitest run <spec paths>`.
3. Check that each one fails for the right reason: a missing behaviour or a wrong value. A failure from a typo, a bad import path, or a broken fixture is not red. Send those back to the test-writer.
4. Do not edit the specs to make them easier. If a spec is wrong about the requirement, say why and ask the user.

## 4. Green: implement

1. Write the smallest code that makes the specs pass. Follow `CLAUDE.md`.
2. Keep each component under about 150 lines (rule 13). Move logic into a composable before it grows.
3. No code comments unless the user asks.
4. Run the specs you are working on with `npx vitest run <paths>` until they pass.

## 5. Check

Run all three and read the output:

```
npm run lint
npm run typecheck
npm test
```

All must pass. The Stop hook runs the same checks and blocks the turn if they fail or a spec is missing. Never weaken or delete a test to get green.

## 6. UI check (only if UI changed)

Skip this step only when no `.vue` file, CSS, or game JSON copy changed.

1. Spawn the `ui-verifier` agent. Give it:
   - The touched routes, plus a regression sweep of `/`, `/games`, one game page (the touched one, or `/games/math`), and `/profile`.
   - What changed and which design.html view matches each route.
2. Read its report. Fix every real difference and every rule 7 to 9 violation it lists as high or medium. Ask the user about anything that looks like a design choice.
3. Re-run step 5, then spawn `ui-verifier` again on the pages you fixed. Repeat until it reports no high or medium findings.

## 7. Review

1. Spawn the `code-reviewer` agent on the diff (`git diff HEAD` plus untracked files). Give it the plan.
2. For each finding, fix it or write one line on why you decline it.
3. If you changed code, re-run step 5.

## 8. Report and ask

Report to the user:

- What changed, with `file:line` links.
- Evidence: the pass lines from lint, typecheck and test, the red-to-green spec list, and the UI verdict.
- Review findings you fixed and any you declined, with reasons.

Then propose a conventional commit message, for example `feat(games): port memory pairs`. Ask with AskUserQuestion before you run `git commit`. Never push unless the user says so.
