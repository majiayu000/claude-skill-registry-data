---
name: publish-demo
description: Publish a finished /human-review page as a demo snapshot — copy it into the human-review repo's demo/, render its landing-page card from the page itself, commit and push, which is what makes the Pages copy, the rolling zip and the ghcr image. Explicit invocation only — user types /publish-demo.
disable-model-invocation: true
---

# /publish-demo

Run this one command, and nothing else:

```sh
for c in "${CLAUDE_PLUGIN_ROOT:-/nonexistent}/skills/human-review" "${HUMAN_REVIEW_HOME:-/nonexistent}" \
         "$(readlink -f .claude/skills/human-review 2>/dev/null)" ".claude/skills/human-review" \
         "$HOME/workspace/human-review/skills/human-review"; do
  [ -x "$c/scripts/publish-demo.sh" ] && { "$c/scripts/publish-demo.sh" --push $ARGS; break; }
done
```

`$ARGS` is empty unless the user named something:

- a slug — pass it as the first positional argument;
- a source directory other than `.human-review` — pass `--src DIR`;
- "don't push yet" / "let me look first" — drop `--push` and pass `--card` instead;
- "make this the featured demo" / "put this one in the README" — add `--feature`;
- "skip the screenshots" — add `--no-tour`.

The script derives the slug from the project directory, copies the snapshot, leaves
behind the run's own dot-prefixed bookkeeping and `*.raw.webm`, refuses any file over
50 MB, rewrites that snapshot's card in `demo/index.html` from `review.html` and
`content.json`, then commits and pushes. When the slug is the featured one (`demo`), it
also screenshots every tab headlessly and rewrites the README's tour, the pages under
`docs/tabs/` and the top of the Pages landing page around the new pictures, in the same
commit — about twenty seconds more.

Then print these three, substituting the slug the script reported, and say they take
about a minute to appear because three workflows fire on the push:

```
https://victorrentea.github.io/human-review/<slug>/
https://github.com/victorrentea/human-review/releases/download/demo/human-review-<slug>.zip
docker run --rm -p 8642:80 ghcr.io/victorrentea/human-review:<slug>
```

That is the whole job. Do not read the report, do not open the page, do not check the
deploy, do not describe the change set, do not hand-edit `demo/index.html` — the card is
rendered from the snapshot precisely so that nobody keeps it up to date by hand. If the
script exits non-zero, show its stderr and stop.

**Not this skill:** publishing *screenshots* of a review — one full-page image per tab,
light and dark, for readers who should not have to run anything — is `/human-review-publish-demo`.
This one publishes the live page.
