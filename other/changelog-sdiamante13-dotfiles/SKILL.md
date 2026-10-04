---
name: changelog
description: Generate a bullet-point summary of branch changes for a PR description. Triggers on "changelog", "pr summary", "summarize branch", or "/changelog".
---

# Changelog — PR Summary Generator

Generate a concise bullet-point summary of all changes on the current branch vs the base branch.

## Activation Triggers

Activate when: "changelog", "pr summary", "summarize branch", "what changed on this branch", "/changelog"

## Process

1. **Detect base branch**: Default to `main`. If the user specifies a different base, use that.
2. **Gather data** — run these in parallel:
   - `git log <base>..HEAD --oneline` — commit list
   - `git diff <base>..HEAD --stat` — files changed
3. **Read the full diff** for context:
   - `git diff <base>..HEAD` — scan for meaningful changes (skip lockfiles, generated files)
4. **Verify before claiming** — this is the most important step. Diffs show fragments, not the full picture. Before writing any bullet that mentions specific details (service names, flag names, config values, architectural claims), read the actual file to confirm. For example:
   - If the diff shows a docker-compose file was added, read it to see what services it actually defines — don't infer from variable names or comments
   - If the diff touches a CLI script's argparse, read the argument definitions to get the real flag names
   - If the diff modifies a config file, read it to understand the actual structure
   - When in doubt, use the Read tool on the file rather than guessing from diff context
5. **Filter for materiality** — a changelog is a high-level summary, not an audit trail. Aim for 4-8 bullets for a typical PR. Each bullet should represent a distinct *user-visible or reviewer-relevant* change. Fold implementation details into the parent feature bullet rather than listing them separately. Skip changes that are:
   - Implementation details of a larger feature (e.g., "added file locking" or "added retry logic" — these belong as context in the parent feature's bullet, if mentioned at all)
   - Minor adjustments to existing files that are incidental to the main feature (e.g., a small import tweak, a threshold change)
   - Mechanical/routine changes driven by the primary feature (e.g., updating an existing script to pass through a new env var)
   - Only meaningful in combination with other changes already covered by another bullet
6. **Synthesize** — produce a bullet-point summary grouped by theme, not by commit. Merge related commits into single bullets. If a bullet needs implementation details, keep them to a brief parenthetical — don't enumerate every internal mechanism.

## Output Format

```markdown
## Summary

- **<Theme/area>** — concise description of what changed and why
- **<Theme/area>** — concise description of what changed and why
...
```

## Accuracy Rules

These exist because diffs provide partial context, and it's easy to hallucinate plausible-sounding details that are wrong. Wrong specifics are worse than correct generalities.

- Only state details you've confirmed by reading the actual file — never invent flag names, service names, endpoints, or config keys from diff fragments alone
- If you can't verify a detail, use a general description instead. "New Docker Compose environment with Juno and PostgreSQL" is better than a wrong claim about what services are in it
- Prefer conservative/vague over specific/wrong — the user can always ask for more detail
- Treat the diff as a hint about *what changed*, not as a source of truth about *what the code does*

## Formatting Rules

- Group by logical change, not by commit — multiple commits on the same topic become one bullet
- Lead each bullet with a bold area label (e.g., **CI**, **Coordinator prompt**, **Experiment data**)
- Keep each bullet to 1-2 lines max — if you're writing more, you're including too much implementation detail
- Focus on *what* and *why*, not *how* — "added CI credential fetching" not "pulls email/password pairs from AWS Secrets Manager using env-var-based credentials"
- Omit trivial changes (whitespace, formatting-only) unless they're the only change
- If a skill or tool was added, mention it by name
- Do NOT include commit hashes in the output
- Output plain markdown — no code fences wrapping the whole thing
