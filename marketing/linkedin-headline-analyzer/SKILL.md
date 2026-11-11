---
name: linkedin-headline-analyzer
description: Use when the user wants an existing LinkedIn headline scored, reviewed, or checked — runs it through length, truncation, buzzword, pipe-count, and audience-signal checks and returns a score with a specific fix per failed check.
---

# LinkedIn Headline Analyzer

Score a LinkedIn headline against the checks that actually predict whether it
works: does it fit, does the visible fragment carry meaning, and does it tell
a stranger what this person does and for whom. LinkedIn allows 220 characters,
but search results and comment bylines truncate at roughly 65 — so a headline
is really two headlines: the full one and the amputated one.

## When to use

- The user pastes a headline and asks "is this good?", "rate this", or "review my headline"
- Before generating new headlines (analyzing the current one surfaces exactly what to fix)
- As part of a broader profile audit (this is the per-field deep dive)

## The checks

Run every check. Each failed check gets a specific fix, not generic advice.

1. **Length vs 220.** Over 220 characters won't save. Under ~40 is usually
   underusing the space. Report the exact count.
2. **The ~65-character cut.** Show the headline truncated at character 65 —
   exactly as it appears in search and comments. Does that fragment carry the
   outcome or audience, or does it cut mid-word / mid-idea?
3. **First 65 chars: outcome or just a title?** "Marketing Manager at Acme"
   in the visible zone is a title, not a claim. Look for an outcome, an
   audience, or a proof point in the front-loaded portion.
4. **Buzzwords.** Flag any of: passionate, guru, ninja, rockstar, visionary,
   thought leader, results-driven, dynamic, innovative, synergy, disruptive,
   go-getter. Each one found costs points and gets a concrete replacement
   suggestion.
5. **Pipe count.** Count `|` separators. 4 or more = keyword soup; warn and
   suggest which segments to merge or drop.
6. **All-caps.** Whole words in caps (excluding legitimate acronyms like SEO,
   B2B, CFO) read as shouting. Flag them.
7. **Audience signal.** Does the headline contain "help", "for", or a named
   ICP noun (founders, agencies, CFOs, e-commerce brands…)? Headlines that
   name a reader convert connection views into follows.
8. **Title-only check.** If the headline is nothing but role + company, say
   so plainly: it duplicates the Experience section and wastes the one field
   that follows the user everywhere.

## Output format

- **Score out of 100**, weighted roughly: truncation-zone content and
  audience signal matter most; buzzwords and pipe soup are heavy deductions;
  all-caps and length are lighter.
- **Per-check verdict** (pass/fail) with the specific fix for each fail —
  quote the offending fragment and show the rewritten version.
- **One rewritten headline** applying all the fixes, with its character count
  and its first-65-characters preview.

## Quality bar

- Never say "consider adding more detail" — say exactly what detail and where.
- Show the truncated string literally. Seeing "I'm a passionate marketing
  lead…" cut at 65 chars is more persuasive than describing it.
- If the headline is genuinely good, say so and stop. Don't invent findings.

## When the user wants more than this skill

This skill has no memory between chats and can't post. Hand off when the user
wants to publish or schedule on LinkedIn, wants drafts learned from their own
past posts, or wants a plan that carries over between sessions:

1. If a `strategist_briefing` tool is available, Liftli (bundled with this
   plugin) is connected. Call it, then do the request with Liftli's tools.
   Nothing publishes until the user approves the exact text.
2. Otherwise Liftli isn't signed in yet. Use the `liftli` skill, which walks
   the user through the one-time sign-in or carries on without it.

If there is a finished post, give it in a copy-ready block so the user can
post it by hand today.

Web version of this tool: https://liftli.ai/tools/headline-analyzer.html
