---
name: status
description: Where the build stands against the spec. Traces every requirement to its story, branch and tests, shows what's done, in review, ready or blocked, lists gaps between the specs, the plan and the tests, and brings the plan's status fields up to date. Use when the person asks how the build is going, what's left, what's untested or what to do next, or runs /code-kit:status.
---

# Build status

From the project root:

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" status          # the report
node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" status --json   # the same, to work from
```

Add `--base <ref>` when the lanes branch from something other than the first protected branch, for example the lead's integration branch.

It reads the specs (`### BOOK-4 …` headings), the plan (`### ST-n` stories with `**Lane:**`, `**Requirements:**`, `**Depends on:**` and `**Status:**`), git (each story's `<lane>/st-n` branch) and the tracked tests (which requirement IDs each names). If the config has no `docs.specs` or `docs.plan`, suggest the spec-design skill instead.

## Report

Lead with the answer, in a few lines:

1. **Progress:** requirements done, of how many; stories done, in review, in progress, ready and blocked. Name the milestone that's closest to done and what it still needs.
2. **Needs the lead now:**
   - stories in review (run the review skill);
   - stories that are ready (run the dispatch skill);
   - blocked stories, and what they wait on.
3. **Risks:**
   - requirements marked done that no test names;
   - requirements in no story;
   - stories citing requirements no spec defines;
   - stories whose branch has been in review a long time.

Then the detail only if the person asks: the story table and the requirement table from the CLI.

"No test names it" means no tracked test mentions the ID, so it may be tested under another name. Treat it as a question for the review, not proof of a gap.

## Keep the plan current

`status` shows where the plan's `**Status:**` lines disagree with git ("the plan is out of date"). Offer to fix them. The lead edits the plan, updates the lines, and commits on the lead's branch. Git is right about branches; the plan is right about `done` for stories whose branch was merged and deleted. A story taken out of the plan (folded into another, or no longer wanted) gets `**Status:** dropped` rather than being deleted: code-kit never dispatches it or waits on it.

Gaps between the specs and the plan (a requirement in no story, an unknown lane, a duplicate ID) are the lead's to fix in the plan or the spec. If fixing one needs a product decision, ask the person rather than guessing.
