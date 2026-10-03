---
name: rpr
description: Review the most recent permission requests in the current session, generalize them into safe allowlist rules, and append them to .claude/settings.local.json to reduce future prompts. Triggers when the user runs "/rpr", "/rpr <N>", "/rpr session", or says things like "stop asking me", "I keep getting permission prompts", or "reduce these requests". Differentiates from read-only (which pre-approves safe reads) and fewer-permission-prompts (which mines all history) by reacting only to the recent, specific commands that just prompted in this session.
---

# RPR (Reduce Permissions Requests)

React to the last few commands that prompted for permission and generate narrow, safe allowlist rules for them. This writes to the local, git-ignored `.claude/settings.local.json` file.

## Step 1: Scan Recent Transcript

This skill runs in **whatever project the user is working in**, not in its own repo, so
call its scripts by **absolute path** — a CWD-relative path like `python3 skills/4-occasional/rpr/scan.py`
only resolves when the project happens to be this skill's own repo. Locate the skill dir
once, then keep the current working directory on the **project** (do *not* `cd` into the
skill dir — `scan.py` reads the CWD to find that project's transcript and settings):

```bash
SK=""
# `find -L` so a SYMLINKED install (e.g. ~/.claude/skills/rpr -> .../skills/4-occasional/rpr) is traversed.
for root in "$HOME/.claude/skills" \
            "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/skills" \
            "$(git rev-parse --show-toplevel 2>/dev/null)/skills"; do
  [ -d "$root" ] || continue
  hit=$(find -L "$root" -path '*rpr/scan.py' 2>/dev/null | head -n1)
  [ -n "$hit" ] && { SK=$(dirname "$hit"); break; }
done
[ -n "$SK" ] || { echo "rpr: skill dir not found — pass it by absolute path" >&2; exit 1; }
```

Then run `scan.py` to find the recent un-allowed commands. If the user specified a number
(e.g. `/rpr 10`), pass it as an argument. If they specified `session`, pass `session`.
Otherwise, default to `5`.

```bash
python3 "$SK/scan.py" <N>
```

## Step 2: Analyze the Output

The script returns a JSON report containing the commands that were not covered by existing `permissions.allow` rules.
Review the report carefully:
- **Compound Commands**: If the script flags a command as compound, warn the user that a partial coverage rule won't silence the prompt because Claude checks the entire line.
- **Environment Variables**: If the script recommends a wrapper script, **do not propose a wildcard rule**. Instead, offer to generate the recommended `bin/qa.sh` (or similar) wrapper script that encapsulates the complex pipeline.
- **Dangerous Commands**: If the script marks a command as dangerous (e.g., `rm`, `sudo`, `npm i`), it will propose an *exact match* rule instead of a wildcard. Present this trade-off to the user clearly. You may propose skipping it entirely. Never propose a `:*` wildcard for these commands. Danger is detected by verb, not position, so option-prefixed forms like `git -C path push` or `npm --prefix app install` are still caught.
- **Option-Prefixed Subcommands**: When `needs_exact_match` is set — a subcommand-style command carries options *before* its verb (e.g. `git --no-pager log`) — the script proposes the *exact command* rather than a wildcard. A `:*` prefix built from an option (`Bash(git --no-pager:*)`) could silently cover destructive siblings (`git --no-pager push`), so present these as exact-match only, like dangerous commands.

## Step 3: Present Preview

Before writing anything, present a clear list to the user of what will be added.
For each proposed rule:
1. Show the rule (e.g., `"Bash(utils/queue-plan.sh:*)"`)
2. Provide a one-line rationale.
3. State the safety tier (e.g., Safe Read, Exact Match for Destructive, Wrapper Required).

Show a preview diff of what `.claude/settings.local.json` will look like.
Ask the user to accept all, pick a subset, or edit the rules.

## Step 4: Write to Settings

Once the user approves the rules, merge them into `.claude/settings.local.json` (never
`.claude/settings.json` or the global file unless explicitly requested). Do not touch
`deny` or `ask` lists.

Use the bundled `write_rules.py` rather than hand-editing JSON — it preserves existing
rules, skips duplicates (so re-running is safe), and handles the legacy `allowedTools`
shape. Critically, hand it the approved rules as a **file**, not a shell argument: write
that file with the editor (Write tool), so rule strings containing quotes, parens, or `$`
(e.g. `Bash(node -e "console.log('ok')":*)`) never have to survive shell escaping.

1. Write the approved rule strings as a JSON array to a temp file, e.g. `rpr-rules.json`:
   ```json
   ["Bash(git status:*)", "Bash(npm run:*)"]
   ```
2. Merge it into the project's settings (writes to `.claude/settings.local.json` in the
   current project by default; pass a second argument to target a different file):
   ```bash
   python3 "$SK/write_rules.py" rpr-rules.json
   ```

It prints how many rules were newly added versus already present.

## Step 5: Confirm and Revert Instructions

After writing, confirm the changes.
Provide the user with a one-line undo instruction:
"To undo these changes, simply remove the rules from `.claude/settings.local.json`."
