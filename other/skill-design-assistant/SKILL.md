---
name: skill-design-assistant
description: Turns debugging experiences into well-structured, reusable skills.
---

# Skill Design Assistant

## Problem it solves

Developers hit painful bugs, solve them, then move on without capturing the lesson. Six months later someone else hits the same bug. Skills exist to prevent this — but most people don't know how to turn a debugging session into a well-structured skill. The gap between "I fixed it" and "here's a skill" is where institutional knowledge dies.

## Detection triggers

Activate when:
- User says "let's create a skill for this" or "this should be a skill"
- A bug was just fixed and the fix was non-obvious
- User wants to document a pattern they keep hitting
- User asks "how do I write a skill?" or "what makes a good skill?"
- After a debugging session, user wants to prevent recurrence

## Protocol

### 1. Extract the pain story

Before writing anything, answer these questions (one at a time if needed):

1. **What broke?** — The symptom the user saw (crash, wrong result, cryptic error)
2. **What was the root cause?** — The actual underlying issue (not the symptom)
3. **Why was it hard to find?** — What made this non-obvious (misleading errors, wrong assumptions, scattered code)
4. **What fixed it?** — The specific change (file, line, what changed)
5. **How long did it take?** — Rough estimate (minutes, hours, days)
6. **How would you have found it faster?** — What signal was available but missed

### 2. Determine skill scope

A good skill solves ONE class of problems. Ask:

- Is this a **debugging** skill? (how to find this class of bug)
- Is a **prevention** skill? (how to avoid this class of bug)
- Is this a **workflow** skill? (the right sequence of steps)

If it's multiple, split into separate skills. Skills that try to do everything help no one.

### 3. Write the skill skeleton

Use this template:

```markdown
---
name: <kebab-case-name>
description: <one sentence: what it prevents/detects/solves>
---

# <Title> Skill

## Problem it solves
<What goes wrong without this skill. Be specific about the failure mode.>

## Detection triggers
<When should this skill activate? Be precise — not "when coding" but "when calling C library X from goroutine Y".>

## Protocol
### 1. <First step>
<Clear, actionable instruction.>

### 2. <Second step>
...

## When NOT to use
<When this skill would be counterproductive or irrelevant.>

## Cross-references
<Related skills that work well together.>
```

### 4. Write the "Detection triggers" section carefully

This is the most important section. Bad triggers:
- "When debugging" (too vague)
- "When using ORT" (too broad)
- "When you see an error" (which error?)

Good triggers:
- "When `session.Run()` crashes with access violation in Go"
- "When `index out of range [N] with length N` appears in sort code"
- "When embedding works in test but fails in server"

The triggers determine whether the skill loads at the right time. Vague triggers waste context.

### 5. Write the Protocol with file:line specificity

Every step should reference concrete repository paths and line numbers when a repository is available; when no repository is available, specific code patterns are acceptable:

BAD: "Check for thread safety issues"

GOOD: "Look for `runtime.LockOSThread()` — it MUST be called before `ort.NewDynamicAdvancedSession()` in the same goroutine. If session creation is in `InitEmbedder()` but `session.Run()` is called from MCP handlers, the lock doesn't apply."

### 6. Add "Lessons learned" for real debugging stories

After the Protocol, add a section with real bugs caught by this skill:

```markdown
## Lessons learned

Real bugs caught by this skill:
1. `defer embedding.CloseEmbedder()` in MCP handlers kills ORT for all subsequent requests
2. Insertion sort `j++` vs `j--` produces panics that look like embedding dimension errors
3. `runtime.LockOSThread()` must be in the goroutine that creates AND runs the session
```

This section is what makes skills discoverable — it's where people search from.

### 7. Iterate with real use

After creating the skill:

1. **Test the triggers** — Does the skill load when the bug class occurs? If not, refine triggers.
2. **Test the protocol** — Does following the protocol actually find the bug? If not, add missing steps.
3. **Add cross-references** — After using the skill with others, note which combinations work.
4. **Prune** — If a step is never needed, remove it. Longer skills waste context.

### 8. Cross-reference policy

Every skill should reference 2-5 related skills. The format:

```markdown
## Cross-references

- **debugging-and-error-recovery** — Apply structured debugging protocol when this skill's triggers fire.
- **anti-phantom-symbols** — Verify API calls exist before assuming they don't.
```

Cross-references help the skill-loader pick complementary skills. Don't reference skills that overlap — reference skills that complete the picture.

### 9. Quality checklist

Before shipping a skill, verify:

- [ ] Name is kebab-case, under 30 chars
- [ ] Description is one sentence, under 100 chars
- [ ] Problem section describes the failure, not the solution
- [ ] Triggers are specific enough to distinguish from other skills
- [ ] Protocol steps are actionable (not "consider doing X" but "run Y command")
- [ ] "When NOT to use" has at least 2 items
- [ ] Cross-references exist (minimum 2)
- [ ] No duplicate content with existing skills

### 10. Submit to the ai-skills repo

Once the skill passes the quality checklist, use the bundled script to copy it into the repo and open a PR:

```powershell
.\scripts\submit-skill.ps1 -SkillPath "C:\path\to\my-skill"
```

Options:
- `-Draft` — opens the PR as a draft for further iteration
- `-DryRun` — shows what would happen without making changes
- `-RepoPath` — override the ai-skills repo location (defaults to the repo this script lives in)

The script validates the SKILL.md frontmatter, copies the skill directory, runs the README catalog updater, creates a feature branch, and opens a PR via `gh`.

## When NOT to use

- The bug is a one-off (no recurrence pattern)
- The fix is language-specific and the skill would only help in one language
- The problem is already solved by an existing skill (check first)
- The user just wants to fix the bug, not create a skill

## Cross-references

- **debugging-and-error-recovery** — Use the structured debugging protocol to extract the root cause before writing the skill.

- **skill-loader** — Skills designed with good triggers load at the right time. Poor triggers mean the skill never activates.

- **verify-and-cite** — Verify the skill's protocol actually works by testing it against the original bug.

- **self-validate** — After adding cross-references, validate they don't create circular dependencies or duplicate content.

- **incremental-implementation** — Ship the skill skeleton first, then iterate. Don't try to write a perfect skill on the first pass.

- **writing-quality-anti-slop** — Skills are documentation. Avoid AI-generated prose patterns. Write like you're explaining to a coworker.
