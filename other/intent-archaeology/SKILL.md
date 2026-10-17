---
name: intent-archaeology
description: "Reconstructs WHY code exists the way it does: mines git history (log -follow, blame, ticket references) for a file or symbol, then has the LLM rebuild the intent story with commit-level evidence and confidence ratings. Read-only. Trigger: /intent"
trigger: /intent
---
# /intent

Reconstructs the intent story of a file (or a symbol within it) from
git history, blame and ticket references - with commit evidence instead of guesses.

## What this is for

- Understand foreign or your own old code before touching it: why is it built
  this way, why does this workaround exist, what discussion led to a
  strange condition?
- Replaces 2-4 hours of manual git archaeology with one invocation and
  commit evidence in minutes.
- **Read-only skill.** Analyzes one file or symbol (function/class) per
  run, no directory trees in one go, no access to external
  ticket systems (only extract IDs and list them).


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked

If `/intent -help` or `/intent -h` (without further arguments) is invoked: output
the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify: `-ProjectDir` (repo root or a subfolder), `-File`
(repo-relative to `-ProjectDir`), optional `-Symbol` (function/class name). If
something is missing, ask the user. Show what was detected, then:

```
ProjectDir: <path>
File:       <file>
Symbol:     <symbol or "none">
Continue? (yes/no)
```

Only continue after confirmation.

### Step 3 - Collect evidence

```powershell
& "<SKILL_DIR>/scripts/git-mine.ps1" -ProjectDir "<path>" -File "<file>" [-Symbol "<symbol>"]
```

Read JSON output. If script aborts with Exit-Code != 0 (no git repo, path
missing, file missing): show the `Write-Error` message to the user, stop.

### Step 4 - Analysis

With the JSON from Step 2:

1. Read commits chronologically (the script delivers them oldest-first),
   form phases (creation, refactors, fixes, workarounds).
2. Per phase reconstruct the intent: What was attempted? What triggered it
   (ticket ID, bugfix wording, revert)?
3. Explicitly handle anomalies: reverts, quick follow-up fixes (< 2 days after
   the previous change), commits with "hack", "workaround", "temp", "fix fix", etc.
4. If `symbol` is set but `symbolLogAvailable: false`: note this in the report,
   analysis falls back to file level.
5. Each statement gets a confidence level (`proven` / `likely` /
   `suspected`) according to the confidence level guidelines. `suspected` statements belong
   exclusively in the "Open questions" section, never among the proven findings.

### Step 5 - Write report

Report structure (Markdown):

1. **Summary** (max 5 sentences) - the why story in brief.
2. **Chronology** - per phase: time period, reconstructed intent, evidence
   (commit hashes), confidence level.
3. **Warnings** - workarounds/provisionals that were never cleaned up, with evidence.
4. **Open questions** - all `suspected` classifications, plus ticket IDs from
   `ticketIds` that would need to be looked up to close gaps.

Save the report as `intent-report-<filename>.md` in the current
working directory (**not** into the analyzed repo).

### Step 6 - Summarize

Tell the user the path of the written report and summarize the core findings (2-3
sentences) directly in chat.

## Usage

```
/intent                          # interactive: ask for repo, file, optional symbol
/intent <repo> <file>            # file analysis
/intent <repo> <file> <symbol>   # symbol analysis
/intent -help                    # show usage, stop
```


