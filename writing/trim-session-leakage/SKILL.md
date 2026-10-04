---
name: trim-session-leakage
description: Find and fix prose in a repo that only makes sense from inside the session that wrote it — dead references to a conversation, change narration ("used to", "no longer"), reviewer-addressed asides, and pointers to work that never landed. Use before a PR, before publishing docs, and when a repo has been written largely by agents. The test is one question - could a reader at HEAD, with no transcript, verify every claim?
---

# trim-session-leakage — write from the repo's vantage, not the session's

An agent writing prose has two vantages available and only one of them survives:

- **the session** — what we just discussed, what the last attempt did, what a
  reviewer asked, what a later step will fix
- **the repo at HEAD** — what a stranger can read, resolve, and verify today

Prose written from the first vantage reads fine in the session that produced it
and becomes unresolvable a week later. That's session leakage, and it's the
characteristic decay of an agent-written codebase.

**The one test.** For every sentence:

> Could a reader at HEAD, with no access to any session transcript, PR thread,
> or uncommitted draft, resolve every reference and verify every claim?

If no, the sentence is written from the wrong vantage. Rewrite it to describe
what is true now, or delete it.

Method studied 2026-08-16 in `deepseek-ai/deepseek-harness` (`dsh-trim-cot-leakage`),
which applies the same test across 688 agent-authored records. It is the natural
mechanical companion to this repo's invariant that conversations never enter a
repo: that rule keeps transcripts out, this skill keeps the *vantage* out.

## The four leak classes

**1. Dead references.** Pointers to things a reader cannot open.

- ✗ `as decided in the earlier analysis` · `per the approach we chose` · `(decision 3)`
- ✓ name the file, the record, or the rule — `per CLAUDE.md rule #12`
- ✓ or state the fact directly and drop the citation

**2. Change narration.** Prose describing the edit rather than the state. The
repo is not a diff; git already holds the history.

- ✗ `this used to call the old parser` · `no longer needs the flag` · `now correctly handles…`
- ✓ describe what it does: `parses the frontmatter block`
- **Exception that matters:** a comment recording the *causal chain* of a real
  defect is not narration — it is the highest-value comment there is. Keep
  "returns null here because an empty ledger must not read as success." Cut
  "changed this to return null."

**3. Stack vantage.** References to work that isn't at HEAD.

- ✗ `a later PR in this stack adds validation` · `will be wired up next` · `pending the follow-up`
- ✓ state today's limit as a limit: `validation is not implemented; callers must pre-check`
- This is where leakage and dishonesty overlap — future work described in
  present tense is the aspiration-as-fact failure the honest-copy rule bans.

**4. Reviewer-addressed asides.** Sentences aimed at one reader in one moment.

- ✗ `as you suggested` · `to address the review comment` · `I kept this simple for now`
- ✓ delete, or convert to a stated limitation with a reason

## How to run it

1. **Scope it.** A PR's changed files, a docs folder, or one package. Whole-repo
   sweeps produce more findings than anyone acts on.
2. **Grep the tells**, then read around each hit — the patterns find candidates,
   not verdicts:

```bash
grep -rnE "\b(used to|no longer|previously|now correctly|as (we|you) (discussed|suggested|decided)|earlier (analysis|conversation)|a later (PR|step|commit)|will be (added|wired|fixed) (next|later)|for now|TODO\(follow-?up\))" --include="*.md" --include="*.ts" .
```

3. **Apply the test** to each hit. Most change-narration hits are cuts. Most
   dead references are either resolved to a real path or promoted to a stated
   fact.
4. **Preserve causal chains.** Before deleting any "why" comment, check whether
   it records a defect's cause. If it does, keep it and fix only its vantage.
5. **Report what you changed and what you deliberately left** — a sweep that
   silently rewrites prose is its own kind of leak.

## Known limits

- **Pattern-first, so it under-finds.** The grep catches phrasing, not vantage.
  A sentence like "the registry handles this correctly" can be pure session
  vantage with no tell-tale words, and this skill will walk past it.
- **It cannot tell a causal chain from narration by pattern.** That judgement is
  human or model reading, every time — which is why step 4 is a read, not a rule.
- **No autofix, deliberately.** Rewriting prose from a vantage the tool cannot
  verify is how meaning gets destroyed quietly. This skill proposes; a person or
  a reviewed session applies.
- **Not a substitute for the conversations-never-in-a-repo invariant.** That rule
  is absolute and prevents transcripts from landing at all. This skill only
  cleans vantage from prose that legitimately belongs in the repo.
- **Whole-repo sweeps are low-yield here.** On a repo with heavy prose density
  the grep returns hundreds of hits, most of them legitimate. Scope it or the
  findings go unread.
