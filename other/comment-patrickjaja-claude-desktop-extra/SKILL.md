---
name: comment
description: Draft (and after approval, post) a reply on a claude-desktop-extra GitHub issue in this project's house voice - short, factual, friendly, no self-blame and no speculation - ending in one copy-pasteable command block that asks the reporter for the evidence we still need. Invoke as "/comment <issue number>".
disable-model-invocation: true
argument-hint: "<issue number>"
allowed-tools: Bash(gh issue view *), Bash(gh issue list *), Bash(gh issue comment *), Bash(gh release list *), Bash(gh run list *)
---

# Comment - reply to an issue reporter

Target issue: **$ARGUMENTS**

## Context
- Repo: `patrickjaja/claude-desktop-extra`
- Latest release: !`gh -R patrickjaja/claude-desktop-extra release list --limit 1 2>/dev/null || echo "(gh not ready)"`

## Step 1 - read the issue

```bash
gh issue view $ARGUMENTS --repo patrickjaja/claude-desktop-extra --json number,title,body,state,labels,comments
```

Read the whole thread, including earlier comments. Note what the reporter already told us so the ask does not repeat it, and note their distro / DE / session type / GPU, because that decides which command block is useful.

## Step 2 - the voice (these are hard rules)

The goal is that the reporter invests a little more time and sends us facts. Everything that does not serve that goal comes out.

- **Never attribute the cause to our own patches**, even when that is exactly what it was. Describe what changed in the release, not who broke it. No apologies for the bug.
- **No transparency theatre.** No "we tried to reproduce it in four variants and could not", no ranked hypotheses, no internals, no speculation about their hardware. If we do not know, we ask - we do not narrate the search.
- **Do not correct the reporter's diagnosis** unless they need the correction to collect the right data. It reads as pushback and costs goodwill for nothing.
- **One fenced command block**, copy-pasteable, no placeholders they have to fill in.
- **At most one question**, and it must be the highest-value one. Bold it so it does not get lost.
- **Short.** Target under 200 words of prose. If a paragraph explains our reasoning rather than their next action, delete it.
- **Regular dashes only** (`-`), never em-dashes. Project-wide rule.
- **No promises about timelines** or about what we will fix next.
- Thank them, assume good faith, never imply they should have known something.

## Step 3 - the shape

1. One line of thanks, specific if possible ("the log excerpt was useful").
2. What shipped, if anything: 1 to 3 bullets, each phrased as an observable behaviour change, with the version in bold.
3. The ask, as one action plus one command: say exactly what to do first ("upgrade to X, then in a Claude Code session ask Claude to take a screenshot and zoom a few times"), then "run this and paste the output here:" plus the single command block. Never ask them to look for strings themselves, and never explain what each line would mean. That confused the #298 reporter, who had to ask whether to use the feature at all.
4. If empty output is a valid answer, say so in one short sentence ("Empty output is good news too"). Otherwise skip this item.
5. Optionally one bolded question.
6. Short closing thanks.

Useful evidence commands, pick only what the issue needs:

```bash
claude-desktop --diagnose
grep -a '\[second-instance\]' ~/.config/Claude/logs/claude-patches.log
grep -a '\[claude-cu\]' ~/.config/Claude/logs/claude-patches.log
tail -100 ~/.config/Claude/logs/main.log
cat ~/.config/autostart/claude.desktop
pgrep -af claude | grep -v -- --type=
```

Note for 3p/enterprise deployments and named profiles the log dir is `~/.config/Claude-3p/logs` or `~/.config/Claude-<profile>/logs`. If the issue smells like either, ask for the path that applies rather than guessing.

## Step 4 - approval, then post

Print the full draft in the chat and **stop**. Posting is public and irreversible, so wait for the user to say go, or to hand back edits. Never post in the same turn as the first draft.

On approval, write the body to a file (avoids shell-quoting damage to backticks and code fences) and post:

```bash
gh issue comment $ARGUMENTS --repo patrickjaja/claude-desktop-extra --body-file <path>
```

Report the returned comment URL.

## Step 5 - then wait

Do not design the next fix in the comment or in the chat afterwards. The point of the ask is that their answer decides what we do, so stop and wait for their technical input instead of pre-building on assumptions.
