---
name: human-review-publish-demo
description: Publish screenshots of an already-generated /human-review report to GitHub Pages — one full-page image per tab, light and dark, plus the feature video, committed and pushed as demo/<slug>/. Explicit invocation only — user types /human-review-publish-demo.
disable-model-invocation: true
---

# /human-review-publish-demo

Run this one command, and nothing else:

```sh
for c in "${CLAUDE_PLUGIN_ROOT:-/nonexistent}/skills/human-review" "${HUMAN_REVIEW_HOME:-/nonexistent}" \
         "$(readlink -f .claude/skills/human-review 2>/dev/null)" ".claude/skills/human-review" \
         "$HOME/workspace/human-review/skills/human-review"; do
  [ -x "$c/scripts/publish-demo-shots.sh" ] && { "$c/scripts/publish-demo-shots.sh" "$REPORT"; break; }
done
```

`$REPORT` is the path the user named, or `./.human-review/review.html` if they named none.
Add `--slug NAME` only if they asked for a name.

Then print the URL the script printed on its last line. That is the whole job.

Do not read the report, do not open the screenshots, do not check the deploy, do not
describe the change set. The script shoots every tab, builds the gallery, updates the
landing page, commits and pushes on its own. If it exits non-zero, show its stderr and stop.
