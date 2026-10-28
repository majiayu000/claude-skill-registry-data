---
name: verify-app
description: Run the quality gates for an app in this lab repo (typecheck, lint, tests, build) and look at it in a browser. Use before shipping an app, after changing one, or when asked whether an app works.
---

# verify-app

Input: `appName` (camelCase folder name). The Nx project is `@lab/<kebab-name>`.

1. Run `npx nx run-many -t typecheck lint test:run build -p @lab/<kebab-name>`. Add `--projects` for
   any `libs/*` you changed. Read the failures; fix real causes, never silence rules.
2. Run the `inspect-app` skill against the local dev server and fix any console errors or broken
   layout you find.
3. Report each gate as passed, failed or skipped. Never say "works" without having run it.
