---
name: snifftest
license: MIT
description: >
  Check a draft against the writer's house rules with the Sniff Test linter.
  Use when the user says /snifftest, hands you a Markdown or text file and asks
  whether it passes, asks which house rules a draft trips, or asks for a style
  or prose check on something they wrote. Reports the rule, the line and how
  sure the checker is, so the prose can be fixed rather than argued about.
user-invocable: true
---

# Sniff Test

A prose linter. It reads Markdown and plain text files, checks them against a
YAML ruleset, and prints one line per flag.

There are two kinds of rule and they behave differently.

**Countable rules** are regular expressions. Dash counts, banned words,
sentence rhythm, anything a computer can decide exactly. They run on the
machine, cost nothing, and send nothing anywhere. Run them whenever you like.

**Judgment rules** need something read rather than counted: a line that
undercuts its own claim, a cost stated without a price, a closing sentence that
only restates. Deciding those means sending the text to a model, so they only
run when the user has already agreed to it on this machine, or agrees now.

## Running it

Both passes go through the script in this skill's folder. It pins the version
of the tool it fetches and never answers the sending question on your behalf.

The free pass, which is the default and the one to reach for first:

```sh
sh "<skill-dir>/scripts/run.sh" path/to/draft.md
```

The judgment pass, only when the user has asked for it:

```sh
sh "<skill-dir>/scripts/run.sh" --judge path/to/draft.md
```

Directories work in place of files. Several paths work too.

Check the file the user asked about and nothing else. A file they did not name
is not yours to send.

## Rules about the judgment pass

Run the free pass as often as it is useful. It is local and free.

The judgment pass sends the draft off the machine, so it is the user's call and
not yours:

- The user has to have said yes. That is either a yes stored from an earlier
  run on this machine, or a yes in this conversation.
- Never talk them into it and never answer for them. Do not add flags to the
  command that skip the question, and do not put an answer into the
  environment. The script and the tool handle consent between them.
- If the tool exits with code 3, consent is missing and nothing was sent. Say
  so plainly, say what running the judgment rules would send, and let the user
  decide.
- The key the judgment rules use is read from the environment by the tool
  itself. Never read it, never print it, never put it in a command or a file.

## Reading the output

A flag is one line:

```
path:line rule score message
```

`rule` is the rule id from the ruleset. `score` is between 0 and 1, and it is
how sure the checker is rather than how bad the problem is. A countable rule
always scores 1.00. Judgment rules count as flags at or above the threshold,
0.7 unless the ruleset or the command says otherwise.

A line that reads `skipped, not text.` means the file was binary or not UTF-8.
Nothing was checked and nothing was sent.

Exit codes: 0 clean, 1 at least one flag, 2 the tool could not do its job, 3
the judgment rules need an answer before anything is sent.

`snifftest rules` prints the ruleset in force and where it came from, which is
the quickest way to answer "why did that flag".

## What to do with a flag

Fix the prose. A flag is a sentence to rewrite, not a rule to turn off.

Show the user the flagged line, say which rule it trips in plain words, and
offer a rewrite. Then rerun the check on the edited file, because a rewrite can
trip a different rule.

If the user decides a rule is wrong for their writing, the answer is to edit
the rule in their `.snifftest.yaml`, not to work around it in the draft. Ask
before changing their ruleset.

A score near the threshold is a judgment call, not a verdict. Say so rather
than rewriting a line the user likes.
