---
name: new-app
description: Turn an app idea into a working first version in this lab repo. Use when the user describes an app idea to prototype, or asks for a "new app", "draft" or "experiment". Scaffolds apps/<appName>, builds a clickable prototype, then verifies and ships it with a draft PR and Vercel preview.
---

# new-app

Input: an idea in a sentence or two. Read the root `CLAUDE.md` first; its rules apply here.

1. **Name it.** Pick a short camelCase `appName` (for example `budgetBuddy`). If the idea is too vague
   to build anything, ask one focused question. Otherwise do not ask: assume and record assumptions.
2. **Scaffold.** `npm run lab:new-app -- <appName>`. It also registers the app in the lockfile.
3. **Build the first version.** A clickable, single-purpose prototype of the core idea in one or two
   screens. Mock or local data only (Zustand or `localStorage`). No backend, auth, database,
   analytics or LLM calls. Mobile-friendly. Use `@lab/ui` and Tailwind. Replace the starter screen
   and the README stub. Keep the `noindex` setup untouched.
    - Add libraries only with `npm run lab:add -- <package> -w @lab/<kebab-name>`. If its check
      fails, nothing is installed and there is no override: only the user can install it,
      outside the sandbox. Follow the steps under "Dependencies" in the root `CLAUDE.md` (tell the
      user, give them the command, wait). In an unattended session use an alternative or leave
      the feature out. Direct `npm install` is denied.
    - Test only important logic and services (no TDD in `apps/*`).
4. **Verify.** Run the `verify-app` skill. If a gate fails, fix and retry. After 3 failed attempts on
   the same problem, stop fixing and ship it as a draft with the failure described in the PR.
5. **Ship.** Run the `ship-app` skill.
6. **Report briefly:** PR link, preview URL, assumptions made, what was skipped or unverified.
