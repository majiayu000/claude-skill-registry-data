---
name: sodapop-verification
description: Verify code changes with repository-native checks and evidence before declaring completion.
---

# Sodapop verification

When changing a repository:

1. Read the repository guidance that applies to each affected file.
2. Use the smallest focused test, build, lint, or type-check command that covers the change.
3. Expand validation when focused results reveal cross-package or lifecycle risk.
4. Do not claim a check passed unless its command completed successfully.
5. Report incomplete or blocked verification plainly, without substituting an unrelated check.
