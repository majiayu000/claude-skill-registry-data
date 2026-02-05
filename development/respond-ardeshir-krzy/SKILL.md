---
name: respond
description: Add builder's exegesis to a critique post. Use /respond to add inline reflections to each Roman numeral section of a critique, exploring what it means for the ecosystem and the builder.
allowed-tools: Read, Glob, Grep, Bash(git:*), Bash(gh:*), Write, Edit
---

# Builder's Response - Exegesis Skill

This skill adds the builder's inline reflections to critique posts. Not a rebuttal at the bottom, but **exegesis woven into the text itself**.

## Purpose

The critique is not a verdict—it's an invitation to dialogue. This skill facilitates that dialogue by:

1. Walking through each Roman numeral section
2. Generating draft exegesis for each
3. Creating a PR for the builder to review and edit
4. Maintaining the critique's integrity while adding depth

## The Exegesis Pattern

The exegesis comes **after** the critique content, not before. Readers need to see the argument first, then the reflection.

```html
<h2>III. WHO BECOMES THE HUB?</h2>
<p>The critical question: what determines whether
an agent becomes a Hub or stays Dormant?</p>
<p>Connectivity requires resources...</p>

<div class="exegesis">
  <p><strong>Builder's reflection:</strong> This cuts to the heart of
  the ENR pricing model. If connectivity requires capital,
  we're recreating venture capital with extra steps.
  The Revival module was meant to address this—but does it?
  <code>src/revival/redistribution.rs</code> needs review.</p>
</div>
```

The critique comes first. The exegesis responds. This preserves narrative flow.

## Invocation

```
/respond [post-slug]
/respond the-hyphal-hierarchy
/respond the-platform-engineers-wager
```

## Workflow (Draft PR Mode)

### 1. Load the Critique

```bash
# Read the post content from data.ts
grep -A 500 "'[slug]':" src/posts/data.ts
```

### 2. Identify Sections

Parse the HTML to find all `<h2>` tags with Roman numerals:
- I, II, III, IV, V, VI, VII, VIII, etc.

### 3. Generate Draft Exegesis

For each section, generate a reflection that asks:

1. **What does this critique really mean?**
   - Surface reading vs. deeper implication
   - What assumption is being challenged?

2. **How does it affect the ecosystem?**
   - Technical implications
   - Economic implications
   - Power structure implications

3. **What action does it demand?**
   - Code to review
   - Decisions to reconsider
   - Documentation to update
   - Or: acknowledgment without action

### 4. Create PR with Exegesis

```bash
# Create branch
git checkout -b respond/[slug]-[date]

# Edit src/posts/data.ts
# Insert <div class="exegesis">...</div> at END of each section (before next <h2>)

# Commit
git add src/posts/data.ts
git commit -m "Add builder exegesis: [title]"

# Push and create PR
git push -u origin respond/[slug]-[date]
gh pr create --title "Respond: [title]" --body "..."
```

### 5. PR Body Format

```markdown
## Builder's Exegesis: [Title]

This PR adds inline reflections to the critique.

### Sections Addressed
- [ ] I. [Section Name] - [one-line summary of reflection]
- [ ] II. [Section Name] - [one-line summary]
- ...

### Review Instructions
1. Open the Files Changed tab
2. Read each exegesis block
3. Edit directly in GitHub if needed
4. Remove sections that don't need response
5. Merge when satisfied

### Exegesis Guidelines
- Keep the critique intact
- Add depth, not defense
- Be specific (cite code, commits, files)
- Acknowledge discomfort
- Name concrete actions where applicable

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### 6. Return to Main

```bash
git checkout main
```

## Exegesis Voice

The exegesis voice is different from the critique voice:

| Critique | Exegesis |
|----------|----------|
| Third person ("The platform engineer...") | First person ("I built this because...") |
| Questions | Answers (or deeper questions) |
| External view | Internal view |
| Challenging | Reflecting |

### Example Exegesis

**Critique says:**
> "The numbers are explicit. Hubs have priority 3. Dormant nodes have priority 0. This is not mycelium. This is hierarchy."

**Exegesis responds:**
```html
<div class="exegesis">
  <p><strong>Builder's reflection:</strong> The priority numbers
  were a debugging convenience that became architecture.
  I didn't intend hierarchy—I intended differentiation.
  But intent doesn't matter; effect does. The question is
  whether <code>role_assignment.rs</code> can be refactored
  to use capability-based selection instead of priority ordering.
  Adding to this week's review list.</p>
</div>
```

## Exegesis Types

Not every section needs the same response:

### 1. Acknowledgment
```html
<div class="exegesis">
  <p><strong>Builder's reflection:</strong> This is correct.
  I have no defense. The precedent is concerning.</p>
</div>
```

### 2. Clarification
```html
<div class="exegesis">
  <p><strong>Builder's reflection:</strong> The critique
  assumes X, but the implementation actually does Y.
  See <code>path/to/file.rs:123</code>. However, the
  underlying concern about Z remains valid.</p>
</div>
```

### 3. Commitment
```html
<div class="exegesis">
  <p><strong>Builder's reflection:</strong> This needs
  to change. Opening issue #47 to track. Target: before
  next release.</p>
</div>
```

### 4. Deeper Question
```html
<div class="exegesis">
  <p><strong>Builder's reflection:</strong> This raises
  a question I don't have an answer to: Can any permission
  system avoid becoming a power structure? Is the goal
  to eliminate hierarchy, or to make it visible and
  accountable?</p>
</div>
```

### 5. No Response Needed
Some sections may not need exegesis. The builder can delete generated exegesis blocks during PR review.

## Output Format

When generating a response:

1. **Create feature branch** - `respond/[slug]-YYYY-MM-DD`
2. **Parse critique** - Find all Roman numeral sections
3. **Generate exegesis** - Draft reflection for each section
4. **Insert into HTML** - At END of each section, before next `<h2>`
5. **Create PR** - With checklist of sections
6. **Return to main** - Leave PR open for editing
7. **Report PR URL** - Builder reviews in GitHub

## Integration with /critique

The typical Monday flow:

```
/critique recent
  → Creates PR with new critique

[Builder reviews in GitHub]

/respond [new-critique-slug]
  → Creates PR with exegesis on same post

[Builder edits exegesis in GitHub]

[Merge both PRs or combine]
  → Critique + Exegesis published together
```

Or for existing critiques:

```
/respond the-platform-engineers-wager
  → Add exegesis to previously published critique
  → Creates PR for review
```

## Future: Spirit App

This response workflow will become part of the Critic Spirit:
- Structured exegesis schema in DOL
- Version-tracked dialogue
- CryptoSaint reputation for quality responses
- Community can add their own exegesis

---

*"The critique is not a verdict. It is an invitation to examine, to respond, to adjust. The dialogue continues."*
