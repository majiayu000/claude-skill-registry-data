---
name: learn-from-fixes
description: Turn merged fixes and review feedback into better project guidance. Use when the user says "what do these fixes teach us", "find gaps in the docs", "learn from these pull requests", or "audit our local rules", or points at a set of fix pull requests, a label or a milestone. Classifies each fix at diff level, maps it to a documented rule or marks a gap, and drafts a documentation change or a local rule. Read-only on the forge; drafts only.
argument-hint: "<work item, label, pull request list, or 'rules <path>'>"
allowed-tools: Read, Grep, Glob, Write, Bash(git log:*), Bash(git show:*), Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh pr list:*), Bash(gh issue view:*), Bash(gh issue list:*), Bash(glab mr view:*), Bash(glab mr diff:*), Bash(glab mr list:*), Bash(jq:*)
---

# Learn from fixes

Input: what the user named. Either a set of merged fixes (a work item, a label, a milestone, an explicit list of pull or merge requests) or `rules <path>` for the audit mode.

Load [git-workflow](../../developer/git-workflow/SKILL.md) when reading local history or diffs. Use its inspection safeguards only; this workflow does not authorize checkout, staging, commits or history rewrites.

Real fixes show where guidance is thin. A bug that reached review or production means the documented rules did not stop it. This skill turns each fix into evidence, maps the evidence to the guidance, and drafts the smallest change that would have prevented the next one.
Do not assume every defect is a documentation gap. Check whether existing guidance was missing, unclear, not discoverable or simply not followed; keep uncertain causes labelled as hypotheses.

Guidance means whatever the project treats as its source of truth: contributing docs, documented conventions, an `AGENTS.md` or `CLAUDE.md`, a docs folder. Ask the user which files count if it is not obvious. Local rules means a file of tagged house rules the docs do not cover yet, when the team keeps one.

## Mode A: fixes to gaps

1. **Collect.** Resolve the input to merged changes. Use the forge CLI the project uses (`gh pr list`, `glab mr list`) or `git log`. Skip changes that only quarantine, skip or delete a test. Count them separately; they teach nothing.
2. **Classify at diff level.** For each fix read the diff and the root-cause note, not the title. Tag one `failure_mode` (what went wrong) and one `fix_pattern` (what the diff did). Reuse the same tokens across fixes so they can be counted. Mark confidence `low` when the diff is noise or CI-only.
3. **Map.** For each pattern, find the guidance file that covers those paths and cite the line. Verdict per pattern: `COVERED` (the rule exists and the fix slipped through anyway), `WEAK` (the line exists but is framed for something else), or `GAP` (nothing covers it).
4. **Decide the home.** For each `WEAK` or `GAP`:
   - The rule belongs in the project docs: draft the change there. This is the default, because documented conventions reach every contributor and every tool.
   - The rule depends on tooling state the docs do not describe, or is a house preference: draft it into the local rules file instead, tagged `baseline` (a candidate for the docs later) or `preference` (a stricter house style).
   - Nothing covers those paths at all: propose where a new section or file should live and who owns it.
5. **Output.** A pattern table (pattern, count, guidance line, verdict), then the drafts. Each draft is a diff with the source links that back it.

A `COVERED` verdict is a finding too. It means the rule exists but did not reach the author or the reviewer. Say where it should have surfaced (a checklist, a lint rule, a review skill) instead of repeating the rule.

## Mode B: `rules <path>`

Audit a local rules file against the project docs, the manual drift check.

1. For every rule in the file, search the guidance for the same content.
2. Verdict per rule: `now covered` (delete it from the local file, cite the doc line), `conflicts` (the doc wins, say what to change), or `still local`.
3. For each `still local` rule confirmed twice in real reviews, draft the upstream docs change so it stops being local.

Keep rule provenance: public evidence, rationale, owner and last audit date. Distinguish a temporary `baseline` from a deliberate `preference`; a preference is not a project-wide requirement. Propose removing redundant guidance once the canonical docs cover it, rather than maintaining two copies. Return audit diffs for approval, not automatic deletions.

## Rules

- Say at the top that the analysis is agent-generated and ask the owners to validate the wording.
- Never open a pull request, comment on one, or edit the docs directly. Write drafts to a file the user names, or return them in the reply.
- Read-only on the forge: view, diff and list commands only.
- Public sources only in anything written down. Confidential issues and internal links stay out.
- Plain English, no em dashes (see the `plain-voice` skill).
