---
name: feature-closeout
description: Feature close-out - type check, build, commit, push. Run when user asks to close out a feature.
disable-model-invocation: true
---

# Feature Close-Out

Run these in order. Stop and report any failure before continuing.

1. `npx tsc --noEmit --skipLibCheck` - must exit 0
2. `npx next build --no-lint` - must exit 0
3. `git add` relevant files + `git commit` with a clear message
4. `git push origin <current-branch>` - push to GitHub
5. Confirm branch is clean and ready

Do **NOT** merge to `main` or deploy to production. Only push the feature branch.
