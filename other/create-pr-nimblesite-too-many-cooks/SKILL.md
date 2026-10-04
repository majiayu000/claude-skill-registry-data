---
name: create-pr
description: Create a pull request for the too-many-cooks repo
disable-model-invocation: true
allowed-tools: Bash, Read, Grep, Glob
---

# Create Pull Request

## Steps

1. **Check state**:
   ```bash
   git status
   git diff main...HEAD
   git log main..HEAD --oneline
   ```

2. **Ignore all commit messages** — only look at the diff.

3. **Draft PR using the template** from `.github/PULL_REQUEST_TEMPLATE.md` if it exists.

4. **Create the PR**:
   ```bash
   gh pr create --title "Short title under 70 chars" --body "$(cat <<'EOF'
   ## TLDR;
   ...

   ## What Does This Do?
   ...

   ## Brief Details?
   ...

   ## How Do The Tests Prove The Change Works?
   ...
   EOF
   )"
   ```

## Rules

- Title under 70 chars
- Only diff against `main` — ignore commit messages
- Return the PR URL when done
