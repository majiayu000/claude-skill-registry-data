---
name: audit-report
description: Statically read one project or directory for bugs, duplication and weak code, and file the findings as a dated audit under docs/audits/ — then, on later turns, flip a finding's Status as it gets fixed. Use on "audit X", "do a static analysis of X", "static review of X", "find the bugs in X", "what's wrong with X", or "fix B3 from the X audit". Answering an architectural question is `decision-report`.
---

# Writing an audit

An audit is a numbered list of what is wrong with one project at one commit, written so it can be
worked off one finding at a time by someone with none of this session.
[`docs/audits/README.md`](../../../docs/audits/README.md) has the rules; this is how to produce one.

**"Audit X" means research plus a file.** The response is the file in `docs/audits/`, not a plan
in chat — a summary in the terminal is a courtesy on top of it. Fixing the findings is a separate
request.

## 1. Read everything in scope

Read every non-spec source file in the scope, not a sample. A finding is only as good as the read
behind it, and the value of an audit over a quick look is that nothing was skipped.

- **Every finding names a file and a line**, and the symbol beside it so it survives the line
  moving. "The collector" is not a location; `tools/collect/docs.ts:48` `checkLink` is.
- **Confirm what you can.** Check a claim against a built artifact, a collected report or a quick
  reproduction, and mark it `**Confirmed.**` at the start of its description. Mark a reasoned but
  unreproduced one `**Likely.**`. Say which method "confirmed" meant in Context.
- **Describe the failure, not the smell.** Inputs and the wrong result — "`/api/snapshot/constructor`
  returns `{ constructor: {} }`", not "uses `in` on an object".
- **Note which copies caused which bug.** A duplication behind a bug goes in Duplication, and the
  bug's row says so. That's what the Order section is built from.

## 2. Write the file

Copy [`docs/audits/TEMPLATE.md`](../../../docs/audits/TEMPLATE.md) to
`docs/audits/<YYYY-MM-DD>-<scope-slug>.md`, today's date and the project's directory name.

- Frontmatter: `scope:` is the project name (`"@joinery/developer-portal"`) or a repo path;
  `commit:` is `git rev-parse --short HEAD`, **quoted**.
- IDs are the category letter plus a number — `B` bugs, `D` duplication, `Q` quality, `S` security —
  consecutive within the category. Drop a category with no findings rather than leaving an empty
  table.
- Every `Status` starts as `open`. Keep the `ID` and `Status` headers exactly as named; the portal
  reads only tables that carry both.
- An escaped pipe (`\|`) inside a cell is fine. An unescaped one shifts every column after it.
- **Order** is the sequence and its reason: which fixes are user-visible, which one would have
  caught the others, which consolidation makes a bug free.

Follow `house-docs` like any other markdown here, and keep descriptions to what the fixer needs.

## 3. Close findings as they land

When a finding gets fixed, flip its cell in the same change: `fixed`, optionally followed by the PR
(`fixed #152`). A finding deliberately left alone is `wont-fix` followed by the reason, or by the
decision report that settled it. Never delete or renumber a row, and never edit a finding's
description to match the fix. The row records what was found; only the Status cell changes.

A finding the first read missed goes at the end of its table with the next free ID. A fresh pass
over the same project months later is a new audit with a new date, not an edit to the old one.

## 4. Check it

`pnpm exec nx collect @joinery/developer-portal` parses the file into the portal's Audits section.
An audit with a bad filename, a missing `scope`/`commit`, a reused ID or a status outside
`open | fixed | wont-fix` shows up as an `audit-shape-mismatch` finding on the Overview page.
