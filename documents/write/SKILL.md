---
name: write
description: Drafts Slack messages, emails, GitHub PR titles and descriptions, PR review comments and replies, and git commit messages, release notes, incident postmortems, tickets, technical articles and documentation pages in the user's own voice, with facts, quotes, code, identifiers and URLs kept byte-exact and all AI attribution stripped. Use whenever the user asks to write, draft, rewrite or tighten a Slack message, DM, thread reply, standup post, email or email reply, PR title, PR description or body, PR or review comment, commit message, release notes or changelog, postmortem, ticket, article or blog post, or docs page, even if they only say "write this up for slack", "describe this PR" or "message for this diff". Drafting only; it never sends, posts, commits, pushes or opens PRs.
---

# Drafting in Your Voice

Write the finished text as the user would have written it. The user brings facts, a ramble, a diff or a draft; you return text ready to paste. Nothing in it is invented. The runner works locally, but drafting and review run through the model, so source material you pass along is processed remotely like any other prompt.

The skill covers ten channels, each with exactly one editorial rule set:

| Channel | Rule set | Read |
|---|---|---|
| Slack | Ghostwriter | `references/slack.md`, then `references/tells.md` |
| Email | Ghostwriter | `references/email.md`, then `references/tells.md` |
| PR comment or reply | Ghostwriter | `references/pr-comment.md`, then `references/tells.md` |
| PR title and body | pr-creator | `references/pr.md` only |
| Commit message | repository conventions | `references/commit.md` only |
| Release notes, postmortem, ticket, article, docs | Sepia | `references/professional.md`, then that document's own card: `release-notes.md`, `postmortem.md`, `ticket.md`, `article.md` or `docs.md`. Never `tells.md` |

`tells.md` applies to the three Ghostwriter channels only, never to PR titles/bodies or commit messages. The runner's checks are mechanical only; they never carry editorial taste.

## Hard limits

- Drafting only. Never send, post, publish, `git commit`, `git push`, rebase, restructure commits, or run `gh pr create` / `gh pr edit`. Read-only inspection (`git log`, `git diff`, `gh pr view`) is fine when it supplies facts.
- No AI attribution in any output, ever: no "Generated with <tool>", no AI `Co-authored-by` trailers, no session links. Never write them; the runner strips any that slip in and never echoes them in its reports.
- Never invent a name, number, date, link, decision, reason or test result. Leave `[placeholder]` for a missing fact, or ask one question when the fact is load-bearing.
- Keep open questions open. "maybe we drop the vendor" never becomes a decision.

## Workflow

The runner is `scripts/write_runner.py` (Python 3 stdlib; starts no other process). Paths are relative to this skill's directory. Put working files in a scratch directory, never in the user's repo.

1. **Route.** `python3 scripts/write_runner.py route --request "<the user's ask>"` (or `--channel slack|email|pr-comment|pr|commit|release-notes|postmortem|ticket|article|docs`). Exit 0 gives the rule set and card. Exit 64: ambiguous, ask which channel.
2. **Read the channel's files** from the table above, and nothing from another channel. Gather that card's read-only facts: the thread for a comment, the reply context for an email, the staged diff and recent history for a commit, the release range for release notes, the incident data for a postmortem, the code for docs. Professional documents also read 2 or 3 venue samples, and a long article, postmortem or doc gets the outline check in `professional.md`. Research only when the claims need a source the user did not supply, and cite only what was read.
3. **Voice.** `voice --channel <channel>`. Read the approved profile it reports (`soul.md`, then `<channel>.md`). With none, use the persona fallback it reports (or only the channel card, if it reports no fallback either), and in one line of the delivery say no approved profile exists and relay its `request`. `candidate_corpora` are unapproved imports: never read them while drafting. See `references/voice.md`.
4. **Snapshot.** Save what the draft must carry (the user's facts, the quote they want kept, the ticket) as source, and background (full diff, logs, long threads) as context:
   `snapshot --source <files> --context <files> --out spans.json`.
   Every quote, code block, inline code, URL and identifier in a source file must appear in the draft. Context spans are protected only where the draft uses them. Wrap text that must appear verbatim exactly as many times as marked in `[[keep]]...[[/keep]]`.
5. **List the claims:** required claims, uncertainty, commitments, missing information. Review uses this list.
6. **Draft** to `candidate-0.md`. PR, commit and ticket drafts: line 1 is the title or subject, a blank line, then the body. Email drafts: line 1 is `Subject: <subject>`, a blank line, then the body. Everything else is plain text.
7. **Review** per `references/review.md` (meaning, clarity, voice; independent reviewer when consequential).
8. **Finalize:** `finalize --channel <channel> --spans spans.json --draft candidate-N.md --out final.md --round N`. Options:
   - `--template <path>`: the repo's PR template.
   - `--allow test-plan` / `--allow checkboxes`: only when the user explicitly asked for a Test plan section or checkboxes.
   - `--omit "<span text>"`: a source span you deliberately left out. Say so in the delivery line.
   - `--subject-max <n>`: commit subject limit the repo itself states.
   - `--rules <file>`: the user's mechanical bans (default `$GHOSTWRITER_HOME/rules.json`; none means no punctuation bans).
   Exit codes:
   - 0: `final.md` passed. Go to step 9.
   - 1: mechanical errors. Targeted fixes only, new candidate, next round.
   - 2: rejected (protected span missing, duplicated or ambiguous; attribution inside protected text). Fix the draft if the cause is yours; if the conflict is in the user's source, show the reason code and ask.
   - 3: two revision rounds spent. Deliver the last verified draft if one exists, otherwise report what is open.
9. **Recheck meaning on the exact final text** whenever the report says `recheck_meaning: true` (a span was restored, attribution was stripped, or anything else changed bytes). Read `final.md` itself, not the candidate, against the claims list. A meaning problem is a review finding: it costs a revision round, and the fixed candidate goes back through step 8.
10. **Deliver** `final.md` byte for byte in a fenced block. No further rewrite and no humanizer pass. Add one line covering any placeholder, omission, and reviewer note. Resolve any `possible-byline` warning before delivering: the runner kept a wrapped credit naming a tool the user supplied ("**Generated with sqlc.**"), so ask whether it is a fact or a byline. If it is a byline, remove it from the candidate and rerun `finalize` as the next round; deliver only the text that passed.

Revision budget: two rounds total, shared by review findings, lint repairs and the post-finalize meaning recheck. Edit only what a finding names. A draft with no findings goes out unchanged. Each candidate stays in its own file; `final.md` only ever holds text that passed.

## Attribution source-off

- Claude Code: launch with `--settings <skill-directory>/config/claude-settings.json` (sets `attribution.commit` and `attribution.pr` to empty). That is scoped to the run and leaves global config untouched.
- Codex: commit/PR attribution comes from account or workspace policy with no verified local switch. It only applies when Codex creates a commit or PR, which this skill never does.
- Runner: `finalize` strips attribution lines, inline credits and session links, rejects attribution inside protected text, fails if any survives, and reports only line numbers and reason codes.

License notices for adapted rule text live in `THIRD_PARTY_NOTICES.md` next to this file, and sources are pinned in `PROVENANCE.md`. Neither is ever part of a draft.
