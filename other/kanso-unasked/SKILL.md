---
name: kanso-unasked
description: Use when the user wants to see or clean up what an agent did beyond the request, such as "what did you add that I didn't ask for", "did you go beyond the brief", "scope creep", "what decisions did you make for me", "undo the extras", or "clean up what I didn't ask for". Not for general code review (kanso-audit) or behaviour-preserving cleanup (kanso-refactor).
argument-hint: "[request text or brief path] [--base REF] [--fresh]"
allowed-tools: Bash(git *) Bash(python3 *)
---

# kanso-unasked

Traces every changed line to the user's words, shows what cannot be traced, and removes what they reject. A good idea nobody asked for is still unasked. The user decides what stays; the agent neither defends its choices nor reverts them unprompted.

Run `python3 <skill>/scripts/unasked.py <command>` from the repo, with `<skill>` resolved from this file's folder. Its files stay outside the working tree, so it adds nothing to the diff. Work in the repo itself, never a copy, because cuts must land there.

## 1. Find the request

Collect the user's own words, verbatim: `$ARGUMENTS` if it holds a request or brief, every instruction in this conversation, and anything they approved mid-session, such as an accepted plan or a "yes, do that".

With none of those, ask what they asked for and stop until they answer. Commit messages, PR descriptions, and code comments describe what was built, so they cannot stand in for the request.

## 2. Number the changes

`collect [--base REF]` compares the base with the working tree, untracked files included. It picks the branch point by default. If the user means something narrower, such as this session's work, pass that commit.

With `--fresh` and a read-only subagent available, have it do step 3 given only the request and this output, with no account of why anything was done. Otherwise classify inline, saying so in one line.

## 3. Classify every changed line

Ask of each: **would the request fail without this?**

- Named by the request: `asked`.
- The request fails without it: `needed`, saying why.
- Anything else: an item, whatever its merit. "Good practice", "while I was there", and "you'd have wanted this" are reasons, not requests.

| Item kind | Means | Impact starts at |
|---|---|---|
| `removed` | Deleted or weakened something that existed | high |
| `behaviour` | Changed how existing things act | high |
| `added` | New feature, file, helper, dependency, config, docs | med |
| `drive-by` | Reformatting, renames, unrelated refactors | low |
| `decision` | A choice inside requested work the user never made | by consequence |

A `decision` is one the user would want to know about: defaults, limits, truncation, retention, timing, permissions, wording users will read. Variable names and routine structure do not count. A decision sits on top of its lines, which still need their own `asked` or `needed` entry.

Split a mixed hunk by new-file lines: `h5:17-21`. Choose lines that leave the code whole, because a diff often pairs a closing brace with the wrong block. `show <hunk>` prints a shortened hunk in full. Group one idea's hunks into one item. Write this JSON to a temporary file outside the repo:

```json
{
  "ask": ["Add an Export CSV button to the reports page"],
  "asked": [
    {"kind": "asked", "quote": "Export CSV button", "hunks": ["h4:3-5"]},
    {"kind": "needed", "quote": "Export CSV", "because": "Nothing else produces CSV", "hunks": ["h3"]}
  ],
  "items": [
    {
      "title": "Removed the rate limit check from fetchRows",
      "kind": "removed",
      "impact": "high",
      "why": "Anyone can now hammer this endpoint.",
      "question": "Was this meant to go?",
      "hunks": ["h2"]
    }
  ]
}
```

`quote` must appear verbatim in `ask`. State `why` as the consequence, leaving out your reason for doing it.

## 4. Show it

`render <file>` validates the classification, computes the numbers, writes the report, and opens it (`--no-open` where no one can see a browser). Fix what it rejects, including any line left unclassified. Use its numbers, never your own.

If everything traces, it says so and writes nothing: pass that on and stop. Otherwise show its numbered list and the report path. Bugs you noticed in requested work are not items: add them in one line. End with this and stop:

```
Reply with what to do, or paste the line from the report: cut 2 3; keep 1; change 4: <what instead>
```

## 5. Act on the reply

- **cut:** run `cut <numbers>`. It reverses only those lines, saves an undo patch, and changes nothing if the lines have moved. Bare approval such as "yes" cuts nothing: ask which.
- **change:** make the edit asked for, and nothing else.
- **keep:** leave it. If `DECISIONS.md` exists, add a kept decision there with its reason.

Read any file a partial cut touched, because a diff's line boundaries need not match the code's. Then run the project's verify command and paste its exit code; say so if none exists. If a cut broke the request, `undo`, tell the user that item was `needed` after all, and ask how to proceed. A cut dependency leaves its lockfile behind, so regenerate that with the project's package manager.

## What this skill never does

- Cut, change, or commit before the user answers.
- Rewrite history. Cuts are uncommitted working-tree changes; `kanso-commit` can record them.
- Use whole-file checkouts, `git reset`, or `--amend` to clean up, which destroy neighbouring work.
- Pad the list. Zero items is a correct result.
