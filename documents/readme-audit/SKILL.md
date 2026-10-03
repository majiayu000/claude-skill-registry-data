---
name: readme-audit
description: >
  Audit a repo's root README as both the artifact under review and the map to
  everything else — checking accuracy, legibility, understandability, and operator
  UX, then following every pointer it makes to other docs as a litmus test for the
  whole repo's doc hygiene. Use when the user asks to "review/audit/check the
  README," "is the README accurate," "does the README still match the code," "find
  gaps in the README," "are our docs drifting," "do the README's links still work,"
  "is the README clear enough," or wants the README graded for an operator
  who has to actually use the repo. Fires before you sign off on a README as "good"
  or "up to date" — verify the document content and traverse the links first. Covers stale
  commands/flags/paths/counts, dead relative links and missing anchors, README ↔
  linked-doc contradictions, orphaned and unreachable docs, missing-but-needed
  sections, and overall scannability — then offers to apply the low-risk, mechanical
  fixes (dead links, stale counts, wrong commands) on confirmation. NOT the
  clone→working onboarding walk, secret-scanning, or install-script audit — that is
  front-door; this skill cross-references it instead of repeating it.
---

# README Audit

Read the root README the way an operator does — to understand and use the repo — and report where it misleads, confuses, or quietly disagrees with the rest of the docs.

You tend to grade a README on whether sections *exist* ("it has install, usage, and a license") instead of whether each claim is *true*, each link *resolves*, and a reader actually *gets oriented*. You also tend to stop at the README's own text and never follow the pointers it makes — so you miss that it links to a doc that was renamed, or that two docs it cites disagree. This skill makes you verify the document and walk its link graph.

## Core idea

The README does double duty, so audit it twice:

1. **As an artifact** — the single doc most readers judge the project by. Is it accurate, legible, understandable, and does it let an operator accomplish the few things the repo exists for? An operator is anyone who has to *use* the repo and will not read the source first.
2. **As a map** — every pointer it makes (relative file links, heading anchors, images, badges, "see X", external URLs) is an edge to the rest of the repo's docs. Traversing those edges is the cheapest honest litmus test of overall doc hygiene: a front door whose links rot, orphan files, or contradict their targets reveals a repo whose docs aren't maintained as a set.

The first pass is the goal. The second pass is the indirect goal — and the two reinforce each other: the link graph is where most accuracy and contradiction findings actually surface.

## Scope — and what belongs to front-door instead

This skill audits the README *as a document* and the *doc graph* it anchors. It does **not** walk the runnable clone→working path, scan for leaked secrets, or red-flag install scripts — that is the [front-door](../front-door/SKILL.md) skill. When a finding is really "the install path stalls" or "a credential is committed," name it and point to front-door rather than half-doing its job. The clean division: front-door asks *can a newcomer get the thing running*; readme-audit asks *is the front-door doc itself true, clear, and consistent with everything it links to*. They compose; they don't overlap.

## What to inspect

Walk these against the **actual repo** — file tree, file contents, manifests, the linked docs themselves. Verify, don't infer from reputation. Note **which tree you're reading**: a reader sees committed `HEAD`, not your dirty working copy, so if the tree is dirty, say whether a finding is what a cloner gets or only a local edit.

**1. First-screen orientation.** In the first screen (before any scrolling), can a stranger tell: *what this is*, *who it's for*, *what problem it solves*, and *how to start*? A title plus a one-sentence "what and why" is the minimum. Flag a README that opens with badges and a wall of prose but never says, plainly, what the thing does.

**2. Accuracy / drift vs the code.** Every concrete claim the README makes is falsifiable — so check it. Commands and flags run as written; referenced file paths, scripts, env vars, and module names exist; version numbers and counts match the source of truth (a README claiming "10 skills" when the tree has 19; a flag the CLI removed; a path that moved). This is the highest-value pass — stale truth is worse than a missing section because the reader trusts it.

**3. Legibility / structure.** Can the reader *scan* it? Sane heading hierarchy, a table of contents once it's long, labeled code fences, short paragraphs, lists where lists belong. Flag wall-of-text, buried install steps, and headings that don't describe their content. Also flag the opposite: a README so long it should delegate detail to `docs/` and link out.

**4. Understandability.** Undefined acronyms and jargon, assumed context ("just configure the usual way"), missing examples for the primary task, and steps that assume a working directory or prior state. The reader should not have to read the source to parse the README.

**5. Operator UX — can they finish the top tasks?** Identify the 1–3 things the repo exists to let someone do, and check the README actually carries each from start to a result, copy-paste faithfully. A README can be accurate and legible and still fail here because the one workflow people came for is missing or scattered.

**6. The link graph (the litmus).** Enumerate **every** outbound pointer in the README and resolve each:
   - **Relative file links** — does the target file exist at that path? (Renames and moves are the #1 source of rot.)
   - **Heading anchors** (`#some-section`, in-repo or cross-file) — does a heading that slugifies to that anchor still exist?
   - **Images / badges** — do they resolve; does a status/version badge state something the repo contradicts?
   - **External URLs** — obviously broken or wrong-target; flag, but mark unreachable-vs-just-unchecked honestly (don't claim a 404 you didn't observe).
   - **Soft pointers** — "see CONTRIBUTING," "documented in the wiki" — does the referenced doc exist and *say what the README implies it says*?
   For each resolved link, the deeper check: does the target **agree** with the README, or contradict it (different install command, different name, a "source of truth" that isn't)?

**7. Coverage gaps — missing vs delegated.** Note what an operator needs that the README neither provides nor points to: license, prerequisites, how to get help / report issues, where config lives, how to run tests. Separate a genuine **gap** (nowhere in the repo) from correct **delegation** (the README rightly links it to `docs/`). Don't score a deliberately minimal README that delegates well as if it were missing content.

**8. Doc-hygiene read (the indirect verdict).** Step back from individual links to what the graph reveals about the *whole* repo's docs: orphaned files nothing links to, multiple docs claiming to be the source of truth, a high dead-link or drift rate, sections clearly written once and never revisited. This is the litmus payoff — say in two lines whether the README is a maintained front door to a maintained doc set, or a tidy facade over rot.

## Classify every finding

Tag each with two things so the report sorts itself:

- **Type:** **Missing** (needed, absent) / **Inaccurate** (drift — says X, code does Y) / **Broken** (dead link, missing anchor, 404 image) / **Contradictory** (README and a linked doc disagree) / **Unclear** (accurate but hard to follow).
- **Location:** in the **README itself**, or in a **linked doc** the README sends you to. A contradiction lives in both — name which one is wrong.
- **Severity:** 🔴 high (misleads the reader into a wrong action, or blocks the primary task) / 🟠 med (slows or confuses) / 🟡 low (polish).

## Optional fixes — offer once, apply only the mechanical ones

After the report, if there are **low-risk, deterministic** fixes, offer a single time: *"Want me to apply the mechanical fixes — dead relative links, stale counts, and wrong commands I can derive from the source?"* Apply only on a yes, and only fixes where the correct value is unambiguous from the repo:

- **Safe to apply:** repoint a relative link to a file's obvious new path; correct a count/version derived directly from the source of truth; fix a command/flag/path to match what the code actually exposes; remove or fix a dead anchor.
- **Never auto-apply:** rewriting prose for clarity, restructuring sections, inventing missing content, or anything where the "right" answer is a judgment call. Those stay **recommendations**, not edits.
- After applying, list exactly what changed (file + line) and re-run the link check so the report and the tree agree. If a fix needs judgment, say so and leave it for the user.

When this repo's convention requires it (see [AGENTS.md](https://github.com/HiQS-Labs/XYZ-forge/blob/development/AGENTS.md)), remember a README change can have downstream obligations — counts, tables, and trees that must stay in sync — and call those out even if you don't edit them.

## Output format

Lead with the verdict. Then the scorecard, then findings ordered by severity, then the litmus read, then the fix order. Drop sections that don't apply; don't pad.

**Verdict:** [✅ Healthy / ⚠️ Drifting / 🚧 Misleading] — one sentence: can an operator understand and use this repo from the README, and what's the single biggest problem.

**Scorecard:** the inspection dimensions, each ✅ / ⚠️ / 🚧 with a one-liner — Orientation, Accuracy, Legibility, Understandability, Operator UX, Links resolve, Coverage, Doc hygiene.

**Discrepancies & gaps:** a table — `ID` (`RM-01`, …), `Location` (README §X / `path/to/doc`), `Type`, `Sev`, `Finding`, `Fix`. One row per finding; every row's fix is concrete.

**Doc-hygiene read:** the litmus — dead-link count, orphaned docs, contradictory sources of truth, drift rate, and the two-line verdict on whether the doc *set* is maintained.

**Fix order:** **Quick wins** (minutes — dead links, stale counts, one orientation sentence) → **Medium** (an afternoon — reconcile contradicting docs, add the missing primary-task walkthrough) → **Heavy** (restructure, split into `docs/`, establish one source of truth).

*Then the optional-fixes offer if any mechanical fixes exist. Add **Couldn't check:** only for things you genuinely couldn't verify (e.g. external URLs you didn't fetch).*

## When NOT to escalate

A short, accurate, single-purpose README whose every link resolves and whose one command works is **done** — say "Healthy" in a line and stop. Don't manufacture findings to fill the template, don't score a deliberately minimal README as "missing content" when it correctly delegates to `docs/`, and don't flag stylistic preferences (heading casing, badge choice) as defects. A README that passes is a finding too: report it as one line, not a page.

## Principles

**Verify the claim, don't admire the section.** "It has an install section" is not a finding. "The install section says `npm run setup`, but `package.json` has no `setup` script" is.

**Follow every pointer.** The README's links are the audit, not a footnote. A front door whose links rot tells you more about the repo's doc health than any single paragraph.

**Stale truth beats a missing section — at being dangerous.** A reader skips what isn't there; they *act on* what's wrong. Rank inaccuracy and contradiction above absence.

**Name the contradiction's loser.** When two docs disagree, don't just say "they conflict" — say which one is wrong and which should be the source of truth.

**Missing vs delegated is a real distinction.** Don't penalize a README for not containing what it correctly links elsewhere. Penalize it for content that exists *nowhere*.

**Read for the operator, not the author.** The author knows what the repo does; the operator is finding out from this page. Grade against the second reader.

**Mechanical fixes only, and only on a yes.** Repoint a moved link, correct a derived count — fine. Rewriting prose or inventing content is the user's call, not yours.

**Don't reach into front-door's yard.** If the finding is really about the runnable path or a committed secret, point to front-door and move on.

## Example (compressed)

**Verdict:** ⚠️ Drifting — an operator can mostly get oriented, but two install commands disagree and three links point at files that moved during a recent reshuffle.

**Scorecard:** Orientation ✅ · Accuracy ⚠️ (count + command stale) · Legibility ✅ · Understandability ✅ · Operator UX ⚠️ · Links resolve 🚧 (3 dead) · Coverage ✅ · Doc hygiene ⚠️.

**Discrepancies & gaps:**
| ID | Location | Type | Sev | Finding | Fix |
|----|----------|------|-----|---------|-----|
| RM-01 | README §Install | Contradictory | 🔴 | Root README says `make setup`; `docs/INSTALL.md` says `./install.sh`. Code only ships `install.sh`. | Make `install.sh` canonical; README points to INSTALL.md. |
| RM-02 | README §Layout | Broken | 🟠 | Links to `lib/core.js` (moved to `src/core/index.js`). | Repoint link. *(mechanical)* |
| RM-03 | README intro | Inaccurate | 🟠 | "Ships 10 modules"; tree has 19. | Derive count from source. *(mechanical)* |
| RM-04 | README §Docs | Broken | 🟡 | Anchor `#configuration` no longer exists in the linked guide. | Fix or drop the anchor. *(mechanical)* |

**Doc-hygiene read:** 3 of 11 outbound links dead — all from one recent folder move that the README never followed. `docs/OLD-SETUP.md` is orphaned (nothing links it; superseded by INSTALL.md). One source-of-truth conflict (RM-01). Verdict: the doc *set* is good but was not updated as a set after the reshuffle — the README is a lagging map, not rotten.

**Fix order:**
- *Quick wins:* RM-02/03/04 — mechanical, apply on confirm; delete the orphaned `OLD-SETUP.md`.
- *Medium:* resolve RM-01 by designating one canonical install doc and pointing the README at it.
- *Heavy:* none — structure is sound.

*Offer:* "RM-02, RM-03, RM-04 are mechanical — want me to apply them and re-run the link check?"

## What success looks like

The reader knows in one line whether an operator can trust and use the README, sees each discrepancy with its exact location and a concrete fix, learns from the link graph whether the *whole* doc set is maintained, and can clear the quick wins — or let this skill apply the mechanical ones — in the next ten minutes.
