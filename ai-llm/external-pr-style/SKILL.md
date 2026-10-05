---
name: external-pr-style
description: Write PR descriptions and maintainer replies for third-party upstream repos in natural, concise human prose to avoid maintainer AI-rejection patterns. Use before opening any PR against a repo we don't own, and before replying to a maintainer's comment or question on one.
---

# External PR Style

Use this whenever opening a PR against a repository we don't own or control, and whenever replying to a maintainer's comment or question on one: any upstream, third-party, open-source contribution.

## The problem

Some maintainers reject otherwise-correct, well-tested PRs purely because the description reads as AI-generated: generic section headers ("Root Cause:", "Why This Fix Works:", "Alternatives Considered:"), templated phrasing, over-explained one-line fixes. This is usually not an automated detector. It's a human maintainer pattern-matching by eye and closing with a canned rejection reply, sometimes on a diff that is otherwise correct and tested.

Maintainers in high-volume open-source repositories frequently pattern-match against common LLM artifacts: formulaic section headers, verbose explanations of trivial diffs, polite boilerplate, and hedging. Diffs that are completely correct and well-tested can be summarily closed if the PR text reads like an automated submission rather than a focused human contribution. Always inspect a target repository's recent merged and closed PR discussions to calibrate style before opening a PR.

## Rules

- Write the PR body as first-person prose describing the bug and the fix, the way you'd explain it to a coworker over chat, not as a templated report.
- No invented section headers unless the target repo's own template requires them (see exception below). Skip "Root Cause:", "Why This Works:", "Alternatives Considered:", "Summary:" unless the repo asks for exactly that.
- State what you verified (tests run, red→green proof, residual risk on security-sensitive changes) as plain sentences woven into the explanation, not as a labeled checklist.
- Don't over-explain a small fix. Match the length of the description to the size of the change:

  | Change size | Body shape | Rough ceiling |
  | :--- | :--- | :---: |
  | Small (1-20 lines) | 1-2 concise sentences on symptom and fix | ~40 words |
  | Medium (20-100 lines) | one compact paragraph (3-5 sentences) | ~90 words |
  | Large (100+ lines) | two focused paragraphs: what changed and why, then what was verified | ~220 words |
  | Reply (routine question, rebase request, acknowledgment) | 1-2 sentences answering exactly what was asked | ~40 words |
  | Reply (maintainer explicitly asked for detail) | as many sentences as the question needs, no more | ~150 words |

  These ceilings count the description prose only, not a repo-required template's own checklist items. Treat them as a budget to catch drift, not a target to fill: a correct 15-word body for a small fix is better than a 40-word one padded to hit the ceiling.
- Don't hedge excessively, enumerate edge cases nobody asked about, or offer unrequested follow-up work ("happy to also add X if useful"). If it's worth doing, do it before opening the PR; if it isn't necessary, don't mention it.
- Keep at most 3 external PRs open at a time (recommended). Submitting batches beyond this concurrency threshold risks being flagged as an automated spammer by maintainers or platform abuse filters.

## Replying to maintainer comments and questions

The same principle governs replies, not just the initial PR body: match the reply's length to what the maintainer actually asked, not to everything you know about the change.

- A yes/no question, a request to rebase, or a one-line clarification gets a one- or two-sentence reply. Don't re-derive or restate the original diagnosis the maintainer has already read in the PR body.
- Only go longer when the maintainer explicitly asks for more (e.g. "can you walk through why this doesn't regress X", "what about the case where Y"). Answer exactly what was asked, at the depth asked for, and stop there.
- If a maintainer closes the PR in favor of a different approach, a short acknowledgment is enough. Don't re-argue the case or re-explain the original fix; they've already made the call.
- The same em-dash, hedge-word, and compression-pass rules below apply to every reply, exactly as they apply to the PR body.

## Em dashes are a tell

In our own PR [litespeedtech/openlitespeed#509](https://github.com/litespeedtech/openlitespeed/pull/509), the body and one follow-up comment used 5 em dashes across 661 words of prose combined, about 1 per 130 words. This is a concrete measured example, not a universal statistic; most engineers write many PRs without using one at all.

- Don't default to em dashes. Rewrite with a period, comma, colon, or parentheses according to the sentence's purpose.
- For two independent clauses, split them into two sentences or use "because", "so", or "and" when the relationship is genuinely causal. For an aside or clarification, use parentheses or a comma.
- If an em dash remains genuinely clearer after rewriting, use at most one in any PR body or individual comment. Apply the same ceiling to each commit message and review comment. More than that reads as templated.
- Apply this rule to every PR body, PR comment, commit message, and review comment governed by this skill, not only the initial PR description.

## Compression pass (do this last, before posting)

Technique adapted from [mattpocock/skills — caveman](https://github.com/mattpocock/skills/blob/221ffca96736afefdc08ca7cf0b3965e9ea83f41/skills/productivity/caveman/SKILL.md) (filler/hedge/pleasantry stripping), applied to natural prose rather than caveman's fragment style to ensure PR descriptions read as clear, authentic engineer-to-engineer communication.

Long, padded explanations are themselves an AI-tell, independent of headers. Reread the drafted body and strip (see canonical [prose compression word list](references/compression-word-list.md)):

- Pleasantries/hedging: "I'd be happy to", "please note that", "it's worth mentioning", "certainly", "of course", "I believe".
- Filler intensifiers: "just", "really", "basically", "actually", "simply", "essentially".
- Restated context the maintainer already has (the issue title, the file name, "as described in the issue").
- Any sentence that explains something the diff already makes obvious.

This is a compression pass on your own draft, not a caveman-style rewrite. Keep full sentences, articles, and natural grammar. The goal is a shorter draft that reads like a person who typed fast, not a person who dropped words to save tokens. If a sentence survives after removing every filler word from it, it earns its place; if it doesn't survive, it wasn't saying anything.

Before posting, name the row from the table above that applies (a diff size tier, or one of the two reply rows) and roughly count the drafted words. If it's over that row's ceiling, cut until it isn't, rather than shipping the first draft.

## Exception: repos with a bot-enforced template

Some repos mechanically require specific sections (a PR-checks bot that blocks merge until a template is filled in, e.g. a required Summary/Why/How/Testing/Examples/Checklist structure, or a PR-title-lint bot with a fixed scope list). There, fill in exactly what's required. That's a hard requirement, not the AI-tell pattern: skipping it isn't concision, it's an incomplete submission that gets mechanically blocked before a human ever reads it.

Check for this before writing the PR body: look for `.github/pull_request_template.md`, a PR-checks workflow that validates title/body format, or CONTRIBUTING.md language describing a required structure. If one exists, follow it precisely. If none exists, default to natural prose.

## Distinct from an explicit no-AI-contributions policy

Some repos state an outright policy against AI-assisted contributions (e.g. a maintainer-applied "rejected AI" label, or CONTRIBUTING.md language explicitly declining AI-generated PRs). That is a different, harder line than a style preference. Don't try to write around an explicit policy like that. Skip the repo entirely. This skill is about writing genuinely well for repos that judge quality and effort, not about disguising AI involvement where a maintainer has drawn an explicit line against it.

## Commit messages

This governs PR *descriptions and replies* only. Commit message attribution rules (no AI co-author lines, ever) are unaffected and covered separately in `system-level/core.md`: they apply regardless of which repo you're contributing to.
