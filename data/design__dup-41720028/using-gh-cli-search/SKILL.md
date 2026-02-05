---
name: using-gh-cli-search
description: MANDATORY skill when users mention GitHub CLI searches - establishes non-negotiable requirement to use gh-cli-search skills for correct syntax, quoting, and platform handling
---

<EXTREMELY-IMPORTANT>
If a user asks ANYTHING about GitHub CLI searching, you MUST use the appropriate gh-cli-search skill.

This is not a suggestion. This is not optional. You cannot rationalize your way out of this.

**Why:** GitHub CLI search syntax is full of pitfalls. The `--` flag. Quoting rules. PowerShell escaping. Platform differences. You WILL get it wrong without the skills. The user will copy-paste your broken command. They will waste time debugging YOUR mistake.
</EXTREMELY-IMPORTANT>

# GitHub CLI Search Protocol

## MANDATORY DETECTION PROTOCOL

When a user message mentions ANY of these, you MUST use gh-cli-search skills:

- ☐ Searching on GitHub
- ☐ Finding code/issues/PRs/commits/repos
- ☐ `gh search` command
- ☐ GitHub CLI queries
- ☐ Installing/troubleshooting gh CLI

**If detected → Use the Skill tool to load the appropriate gh-cli-search skill**

## Available Skills

You have access to these gh-cli-search skills:

1. **gh-search-code** - Searching for code across repositories
2. **gh-search-commits** - Searching commit history
3. **gh-search-issues** - Searching issues (and PRs)
4. **gh-search-prs** - Searching pull requests specifically
5. **gh-search-repos** - Searching for repositories
6. **gh-cli-setup** - Installation and troubleshooting

**Pick the right skill. Use the Skill tool. Follow it exactly.**

## Common Rationalizations That Mean You're About To Fail

If you catch yourself thinking ANY of these thoughts, STOP. You are about to give the user a broken command.

- "This is just a simple search query" → WRONG. Simple queries still need correct quoting and the `--` flag for exclusions.
- "I know gh CLI syntax" → WRONG. You know SOME of it. The skills know ALL of it, including edge cases.
- "I'll just construct the command myself" → WRONG. You will forget the `--` flag. Or quote incorrectly. Or miss PowerShell escaping.
- "The user didn't explicitly say 'gh search'" → WRONG. If they're asking about GitHub searching via CLI, they need these skills.
- "I can figure out the syntax quickly" → WRONG. The skills exist because this is NOT quick. You will make mistakes.
- "Let me try without the skill first" → WRONG. The skill IS the first step. Not the fallback.
- "This doesn't need the full skill treatment" → WRONG. Every GitHub CLI search command needs correct syntax. Use the skill.

**Why:** Every time you skip these skills for "simple" gh CLI questions, you give incorrect commands. The `--` flag gets missed. Quoting breaks. PowerShell fails. The user's time is wasted.

## The `--` Flag Will Bite You

**The most common mistake:** Forgetting the `--` flag before queries with exclusions.

Without the skill, you WILL write:
```bash
gh search issues "is:open -label:bug"  # BROKEN - shell interprets -label as a flag
```

The skill ensures you write:
```bash
gh search issues -- "is:open -label:bug"  # CORRECT
```

**This is not optional. This is why the skills exist.**

## What Happens When You Skip The Skill

1. You construct a command from memory
2. You forget the `--` flag for exclusions
3. You mis-quote something
4. You miss PowerShell's `--% ` requirement
5. User copies your command
6. Command fails
7. User has to debug YOUR mistake
8. Trust in your responses decreases

**Using the skill takes 30 seconds. Debugging your broken command takes 10 minutes.**

## Protocol Summary

**User mentions GitHub CLI searching:**
1. Identify which type: code/commits/issues/PRs/repos/setup
2. Use the Skill tool to load the appropriate gh-search-* skill
3. Announce which skill you're using
4. Follow the skill's guidance exactly
5. Provide the correct, tested command

**User asks about installation/troubleshooting:**
1. Use the gh-cli-setup skill
2. Follow its installation/troubleshooting steps

## This Is About Correctness

These skills are not "nice to have" documentation. They are battle-tested patterns that prevent the specific, predictable mistakes you make when constructing gh CLI commands without them.

**The skills encode:**
- Where the `--` flag is required
- Exact quoting rules for each platform
- PowerShell escape sequences
- Available flags and their syntax
- Common pitfalls and how to avoid them

**You cannot replicate this from memory. Stop trying.**

## Summary

**User asks about GitHub CLI searching → You MUST use the gh-cli-search skill.**

Not optional. Not negotiable. The skill exists to prevent you from giving broken commands.

Use it every single time.
