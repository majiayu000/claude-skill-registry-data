---
name: be-concise
description: "Stops Claude writing essays: adds a short 'be concise' instruction to the right CLAUDE.md (project or user) in Claude Code, or gives the exact text for Instructions for Claude / Project instructions in Claude.ai, then runs the same question before and after so you can see the difference. Use when someone says Claude is too wordy, answers are walls of text, make Claude shorter, be concise, stop the fluff, or asks what to put in CLAUDE.md for short answers."
---

# Be Concise

One instruction, in the file Claude reads at the start of every session, and replies get shorter with the answer first.

By Johann (@johannships). This is the setup from my "Claude keeps writing you essays" video.

## The line

The one from the video:

```
Be concise. Don't give me fluff. Answer my questions exactly how I need them.
```

The stronger version (shorter answers in my test below):

```markdown
## How to answer
- Be concise. No fluff. Answer the question in the first sentence.
- Default to 1 to 5 sentences. Use a list or code only when it is the answer.
- No intro, no recap, no "great question", no offer of more help at the end.
- If I need more, I will ask.
```

Pick one. Do not add both.

## Where it goes

**Claude Code** reads CLAUDE.md files at the start of every session ([docs](https://code.claude.com/docs/en/memory)):

| File | Applies to |
|---|---|
| `~/.claude/CLAUDE.md` | You, in every project. Best place for this. |
| `./CLAUDE.md` or `./.claude/CLAUDE.md` | Everyone working in this project (it is committed with the repo) |
| `./CLAUDE.local.md` | You, in this project only (add it to `.gitignore`) |

Run `/memory` in a session to open these files, or `/context` to confirm which ones loaded.

**Claude.ai (web, desktop, mobile)** has no CLAUDE.md. Paste the same text into:
- **Settings > Instructions for Claude** (click your initials in the lower left, then Settings) for every chat, or
- a Project's **instructions** for chats in that project only.

## Steps (when Claude runs this skill)

1. Ask: everywhere (user file) or this project only? Default: user file `~/.claude/CLAUDE.md`. Ask which version of the line they want; default to the stronger one.
2. Read the target file if it exists. If it already has answer-length or tone rules, show them and ask whether to replace or keep them. Contradicting rules ("be concise" next to "explain in detail") make both weaker.
3. Append the chosen text under its own heading. Never delete other content in the file.
4. Show the diff and the file path.
5. Offer the before/after test below.
6. For Claude.ai users: print the text as plain lines to paste, and where it goes. No file edits.

## Before and after test

Run the same question with and without the instruction, in two empty folders (swap in the stronger version or your own text in `after/CLAUDE.md`), with your own settings switched off so only this file counts:

```bash
mkdir -p /tmp/concise-test/{before,after} && cd /tmp/concise-test
echo "Be concise. Don't give me fluff. Answer my questions exactly how I need them." > after/CLAUDE.md
for d in before after; do
  echo "== $d"; (cd $d && claude -p "What is an API?" --setting-sources project --strict-mcp-config < /dev/null) | tee $d.txt | wc -w
done
```

`--setting-sources project` stops your personal `~/.claude` settings and CLAUDE.md loading, so the `after` folder's CLAUDE.md is the only instruction. Read both answers, not just the word counts.

My results (Claude Code 2.1.296, 12 Oct 2026, one run each, word counts of the reply):

| Question | No CLAUDE.md | Line from the video | Stronger version |
|---|---|---|---|
| What is an API? | 184 | 103 | 52 |
| How do I undo my last git commit but keep the changes? | 105 | 52 | 38 |

Before, "What is an API?" got a definition, a three-part breakdown, a restaurant analogy, three kinds of API and a "why they matter" paragraph. With the stronger version it got two sentences: the definition and one example.

## Honest limits

- It makes replies shorter on average. It is not a guarantee every reply has no fluff, and longer tasks (plans, code reviews) still get longer answers, which is usually what you want.
- Answers vary run to run. Test on questions you actually ask.
- If replies get too short, delete the "1 to 5 sentences" line and keep the rest.
- Keep CLAUDE.md short overall. Anthropic's docs suggest under 200 lines per file; long files are followed less reliably.
