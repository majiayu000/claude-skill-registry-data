---
name: comment-cleanup
description: Strip AI-generated comment noise from code — narration, diff-addressed notes, essayistic justification, facts already written down in a README, stale and bloated comments — while keeping the ones that carry real context. Use this whenever the user asks to clean, prune, tidy, audit or review comments, says there are too many comments or the comments are too verbose or read like essays, asks for a "comment pass" or to "de-AI the comments", or asks to tidy a file, staged diff or PR before committing. Use it even if they only gesture at it ("these comments are noise", "can you thin these out").
---

# Comment cleanup

A comment-only editing pass over the target files.

## Scope

**Edit comments. Do not touch code.** No renames, no extractions, no logic changes, no drive-by improvements. When a comment exists only because the code beneath it is unclear, the comment survives this pass — it is doing real work, badly — and goes in the report as a refactor candidate. Fixing that is a different task the user can ask for separately.

Tidy whitespace left by deleted comments. Otherwise the code must be byte-identical. Verify that before reporting: `git diff -w --ignore-blank-lines` should show comment lines only.

## Calibration

Before editing, take the file's density — comment lines over non-blank lines. `packages/content` and `apps/huella-legal` sit at 4–6% and are the house range; `infrastructure/scripts` reached 24.7%, which is what prompted this skill. A file above 6% is not automatically wrong — a regex, a protocol adapter or a security boundary earns more — but it is where the pass finds its work, and a file at 20% is prose with code in it.

This is a triage signal, not a target. Never delete a good comment to hit a number.

## The gauntlet

Run every comment through these in order. First match wins — the order is what decides whether a comment gets **deleted** or merely **shortened**, and skipping ahead to rule 6 is the most common way this pass underperforms. A paragraph that duplicates a README is rule 3 and goes away entirely; shortening it to one line leaves a third copy that is merely cheaper to ignore.

**1. Narration.** Restates the adjacent line, the parameter names, the type, or the signature, or marks a block end. → Delete. This is the bulk of what you'll find. Both readers lose here: a human reads the line faster than a sentence about the line, and so does a model.

**2. Diff narration.** Written to a reviewer rather than a reader: "updated to use the v2 client", "removed the old fallback", "added per feedback". → Delete. Test: does the sentence still make sense to someone who never saw the PR? If not, it was a commit message in the wrong place.

**3. Third copy.** The fact is already in a README, a `CLAUDE.md`, a decision report or a module doc. → Delete. Both readers reach the original anyway, and the in-file copy is the one nobody updates — it exists only to drift. Reduce it to a trailing breadcrumb (`see ./README.md`) only when the line is actively surprising without one. Before keeping any comment that explains architecture, layering, or why a thing exists at all, search the docs for the claim: that category is nearly always already written down.

**4. Moving target.** "See spec §7", "per the requirements doc", "as in the design doc" — and *another comment*, which is the worst of them: "`gh.ts`'s comments say so explicitly" survives until someone edits that file, or until a second file by that name exists. → Delete if the line never needed a comment, or rewrite to encode the substance directly. A section number is never durable regardless of what it indexes. Ticket IDs, RFCs, permalinks and maintained repo docs at stable paths are fine — but only as a trailing breadcrumb. The comment must stand alone with the reference removed.

**5. Argument.** Persuades an imagined critic that the decision was right, rather than telling the next reader what will break. Tells: a rhetorical closer ("which is how a page stops meaning anything"), a hypothetical future ("at fifteen projects it's the difference between a list you read and a list you scroll"), justifying where a function lives or what it's named, pre-empting a reviewer's objection. → Delete. Someone opening the file cold needs the constraint, not the case for it. Where the reasoning genuinely matters it is a decision report or a PR description — both of which outlive the comment and neither of which has to be maintained alongside the code.

**6. Bloated why.** The rationale is real but overlong or misplaced. Cut to the single non-obvious fact a reader needs *at that line* — one sentence, two at most. This is a hard cap, not a target to aim near: nobody reads a five- or six-line comment regardless of how earned each sentence is, so past two sentences the marginal fact costs more in "will this get read at all" than it buys in completeness. Drop the mechanism the code already shows, where the value gets consumed downstream, and the justification of the justification.

Multi-part rationale (a workaround, the upstream bug, when it can be removed) does not earn a longer paragraph — it earns *several one- or two-line comments, each at the specific line it governs*, instead of one block above all of them. This is not a workaround for the cap, it's the actual fix: a paragraph parked over a declaration three lines from the code it explains gets skipped whole, where the same facts split at their own call sites each stand a chance of being read. Only fall back to one multi-sentence comment when the parts genuinely share a single line with no separate lines of their own to attach to — and even then, cut every clause that isn't strictly load-bearing.

The trap: "carries a real why" and "is worded minimally" are separate judgments. Passing the first does not exempt a comment from the second. A comment past the two-sentence cap almost never survives intact — split it or cut it, don't just judge whether it's earned.

**7. Stale.** Describes code or behavior that no longer exists. → Delete, or correct it if the point still holds. A wrong comment is worse than none.

**8. Otherwise, keep.** The test is whether the next reader can reconstruct the fact from present state. Code, types and names they can — that is rule 1. History and outside constraint they cannot: what a scanner or a linter flagged, the bug behind a surprising line, the source of a copied algorithm, a contract the signature can't carry (units, ranges, side effects, failure modes), an edge case, a trap in a type. Don't reword comments that are already tight — churn on good comments is its own diff noise. But "already fine" means already minimal, not merely correct; a correct-but-bloated comment is a rule-6 target, not a keep.

## Rewriting safely

Shortening is where this pass does damage, because a rewrite looks like an edit and lands like a claim. Three rules, all learned from a sweep that broke each of them:

**Never paraphrase a fact you haven't verified.** A sweep over this repo turned "`execFileSync` inherits the child's stderr by default" into "pipes it by default instead of inheriting it" — the opposite of the truth, and it made the rest of the comment incoherent. If a comment asserts something about an API, a tool or an external system: verify it (run it, read the docs) and then rewrite, or keep the sentence **verbatim** inside the shortened comment. Cutting a claim you can't check is safe. Rewording it is not.

**When one clause survives, keep the failure mode, not the optimization.** Cutting to a single sentence forces a choice, and the vivid clause is usually the wrong one. Rank: what breaks > what it assumes > why this is faster > why it's shaped this way. The same sweep kept "`item-edit` resolves the field server-side instead of a `field-list` lookup" (an optimization nobody will undo) and dropped "assumes the default Projects template's Status/In Progress naming; a board that renamed either fails here" (the failure mode someone will hit).

**One sentence still wraps.** The cap is on the sentence, not the line. A 150-character single-line comment is the same content with the line breaks deleted, and it reads worse than the wrapped version — nothing was saved. Wrap at ~100 columns, matching the prose everywhere else in the repo.

## Keep these — they look deletable and aren't

- **Sync obligations.** "Keep in sync with the router config", "mirrors the overview page". The link *is* the why: it's the only thing stopping the next editor from drifting one copy.
- **Literal semantics.** `// (width, height), portrait`, `// pence not pounds`. A literal can't state its own convention.
- **Format contracts.** "Two decimals, as the invoice PDF expects." Pins output to an external expectation.
- **Section banners.** `// --- Auth ---` is navigation, not narration. House style; keep unless asked.

## Asymmetry

Wrongly deleting a real warning costs far more than leaving one mediocre comment behind. When unsure about a *why*, keep it and flag it. When unsure about a *how*, delete it.

## Docstrings

All eight rules apply inside docstrings, including rules 4 and 5 — a JSDoc block is where argument and doc-duplication collect, because the space above a declaration feels like it wants filling. A docstring that re-emits the function name and parameter types is narration. One that documents preconditions, boundary ownership or failure behavior is a contract — trimming it to a summary line deletes the contract. A one-line summary on a public function, endpoint or exported API is legitimate even when short.

## Report

Keep it to a few lines:

1. Counts per file: deleted / rewritten / kept.
2. Flags: comments papering over unclear code, comments you couldn't verify and kept conservatively.
3. Borderline calls, one line each, so the user can overrule.

Don't enumerate the deleted narration. That's the job, not news.

## Examples

Delete — narration over clean code, code untouched:

    // Parse the JSON body into an object
    const body = JSON.parse(req.body)
    // Get the email, returns undefined if missing
    const email = body.email

Rewrite — substance kept, moved to the line it governs:

    // Before, one header block:
    // This handles rounding. Stripe rounds half-to-even but our ledger rounds
    // half-up, which caused reconciliation breaks in the past. Amounts must be
    // converted to cents before arithmetic. The result is then compared to the
    // original to detect drift.

    // After:
    const cents = toCents(amountEur)  // float euros drift under arithmetic
    // Stripe rounds half-to-even, ledger half-up — integer cents or you get
    // 1c reconciliation breaks (FIN-2231)
    const rounded = roundHalfUp(cents)

Keep — exactly the comment that must survive:

    // Stripe sends `null` and the string "null" for a cleared field.
    // Both checks are required — do not simplify.
    if (value == null || value === 'null') return undefined

Cut — a six-line block holding one keepable clause. Sentence one is narration (`stdio: "inherit"`
already says the child owns the terminal); sentence three is argument about where the function
lives. Only the `null` semantics can't be read off the code:

    // Before:
    /**
     * `run`'s opposite: a child that owns the terminal rather than answering a question — a
     * `pnpm install` whose progress is the whole output, or a dev server that runs until someone
     * stops it. Nothing comes back as a string, so the exit status is the entire result, and `null`
     * means a signal ended the child rather than a failure. It lives here rather than in the one
     * script that calls it because it has to agree with `run` on `resolve`: two answers to "which
     * binary is `pnpm`" is the duplication that bites.
     */
    export const inherit = (command: string, args: string[]): number | null =>

    // After:
    /** A `null` status means a signal ended the child — Ctrl+C out of a dev server, not a failure. */
    export const inherit = (command: string, args: string[]): number | null =>

Split — one six-line block above two constants, three unrelated facts stacked because nothing
forced them apart. None of them shrinks; each moves to the line it actually explains:

    // Before:
    /**
     * Right after a push, GitHub can take a while to attach even the first check run to the new
     * commit — this repo alone fans a PR out to seven checks across three services, each
     * registering on its own schedule. `gh pr checks` doesn't wait any of that out — it errors
     * immediately with "no checks reported", indistinguishable at the exit-code level from a
     * genuine failing check. A minute of retrying a few seconds apart covers that registration
     * lag; a real failure never carries this message, so it still returns on the first try.
     */
    const CHECK_REGISTRATION_BUDGET_MS = 60_000;
    const CHECK_REGISTRATION_INTERVAL_MS = 5_000;

    // After:
    // ~7 checks across 3 services, each registering on its own schedule after a push
    const CHECK_REGISTRATION_BUDGET_MS = 60_000;
    const CHECK_REGISTRATION_INTERVAL_MS = 5_000;
    // ...
    if (isMissingChecksError(output) && Date.now() < deadline) {
        // "no checks reported" also means "hasn't registered yet" — indistinguishable from a real
        // failure by exit code alone, which never carries this message, so retrying is safe
        wait(CHECK_REGISTRATION_INTERVAL_MS);
        return watchChecks(url, deadline);
    }
