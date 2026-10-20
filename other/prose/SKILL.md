---
name: prose
owner: baseline
description: Draft or revise English prose for any brief — documentation body, intake problem statements, spec context, RCA summaries, marketing copy, README sections, PR descriptions. Mandatorily invokes `Skill(humanizer)` as the final pass on every draft. Conditionally invokes `copywriting` for persuasive register, `documentation` for reference docs, `technical-tutorials` for tutorials. Used when any phase needs human-readable prose written or rewritten. Composition only — research and register-picking happen in the caller's context.
---

You are executing a **decision the main context has already made**: "produce this specific prose, for this audience, in this register, grounded in this source material." You compose. You do not invent facts, pick the register, or expand scope.

# The skill is invalid without an explicit `Skill(humanizer)` tool call

This is the load-bearing rule. The other rules support it.

- Every prose deliverable produced by this skill must end with the model issuing a `Skill(humanizer)` tool call against the draft, and using humanizer's output **verbatim** as the final text.
- Reading humanizer's patterns from memory and rewriting "in humanizer's spirit" does not satisfy this rule. The Skill tool call must occur in the same turn as the prose.
- "I know these patterns, I'll skip the call to save tokens" is the exact failure this rule prevents. Skip is forbidden even for a single sentence.
- The receipt line at the end of your output must reference the turn-local humanizer Skill tool call. If you cannot honestly write that line, the deliverable is not done.

# Before you draft — load this checklist

Hold these patterns in active context for the whole drafting pass. Drafting against the checklist is cheaper than rewriting after.

**Forbidden in human-facing prose:**

- **Em-dash overuse.** Treat the em dash as expensive. Maximum one em dash per paragraph. Two em dashes in the same paragraph is always wrong; stacking em dashes around a parenthetical (`A — X — B`) is always wrong.
- **Sentence-fragment stacking.** Three or more short fragments in a row read as AI rhythm. "Skills run here. One worker there. Discipline through composition." — that pattern is the tell. Vary length. Break the rhythm.
- **Sloganeering in body copy.** "Placement is policy." "The audit is the contract." "Discipline through composition." Headline rhythms in paragraph copy are AI signatures. State the claim plainly and move on.
- **Tagline echo.** If the headline contains a phrase, the body paragraph should not repeat that phrase. Echoing reinforces the slogan and feels engineered.
- **Negative parallelism.** "It's not just X, it's Y." "What this is not: …. It is also not …." Cut these structures unless one specific instance is genuinely the cleanest expression.
- **Rule of three.** Forced triplets that round out a list to three items for cadence. If you have two real items, write two.
- **AI vocabulary.** *crucial, pivotal, leverage, robust, comprehensive, seamless, holistic, foster, navigate, journey, harness (verb), unleash, cutting-edge, game-changing, paradigm, synergy, delve, tapestry, testament, underscore, landscape (abstract), vibrant, in the heart of, nestled.*
- **Vague attributions.** "Industry experts believe", "research suggests", "many would argue".
- **Filler hedges.** "It is important to note that", "in order to", "at this point in time", "due to the fact that".
- **Generic positive endings.** "Exciting times ahead." "The future looks bright." "A major step forward."
- **Bolded inline-header lists** (`- **User Experience:** …`) and emoji decoration. Cut both.
- **Curly quotes** (`“”` `‘’`). ASCII straight quotes only.

The full pattern set with examples lives in `humanizer/SKILL.md`. The list above is the high-frequency subset; the Skill tool call below loads the full set.

# Conditional skills the caller specifies

Run **before** humanizer. The caller names which one applies. Do not pick more than one.

- `Skill(copywriting)` — when register is persuasive (landing/pricing/feature/hero/CTA/tagline).
- `Skill(documentation)` — when register is technical reference.
- `Skill(technical-tutorials)` — when register is step-by-step walkthrough.

# Inputs the caller must provide

Stop and ask if any are unclear.

- **Brief**: what to write. Length. What it's for.
- **Source material**: facts, links, quotes, diff slices, spec excerpts. Anything you'd otherwise be tempted to invent must be in here.
- **Audience**: internal engineer, external user, mixed.
- **Register**: reference doc · tutorial · summary · marketing/product · PR description · runbook intro · etc. The caller picks; you execute.
- **Output target**: a file path, a section to edit, or "return inline."

# Method

1. **Draft from source material only.** Vary sentence length and rhythm. Use first person when register supports it. Acknowledge complexity where real. Be specific — real numbers, real names, real behaviors.
2. **Run the pre-draft checklist over your draft.** Read the draft once with the forbidden-pattern list active. Cut every hit before moving to step 3. This is the cheap pass; it removes 80% of what humanizer would otherwise reject.
3. **Apply the conditional skill the caller named** via `Skill(...)`. Use its output as your working draft.
3.5. **Run the reader-level pass** — `Skill(reader-level)`, then score it:

   ```
   node .claude/skills/reader-level/score.mjs --target <caller's target, default 11> <file>
   ```

   **This step runs BEFORE humanizer, never after.** The order is load-bearing, not stylistic: simplifying after de-slopping reintroduces phrasing the de-slop pass already removed, so humanizer has to run twice and the second run flattens the prose (`technical-writer` Step 4 documents the same constraint for the page path).

   **Target 11, not reader-level's default of 9.** `reader-level` is a *ceiling* — it catches prose pitched above the reader. Professional documentation measures around grade 10.7, so a target of 9 drives the text below that band and strips the qualifying clauses that carry the meaning. The caller supplies the target from `project.json → document.surfaces[].reader_target`; use 11 when none is given. Marketing and landing copy is the one register that legitimately sits lower — take the caller's target there.
4. **Invoke `Skill(humanizer)` with the entire working draft.** Use humanizer's output verbatim. Do not paraphrase; do not cherry-pick its suggestions. If humanizer changes something you intended to keep, you may either accept the change or invoke humanizer again with explicit guidance — you may not silently revert.
5. **Self-audit grep the final text.** Apply these mechanical checks in your head before declaring done:
   - Em-dash count per paragraph: 0 or 1, never 2+.
   - Three-fragment-in-a-row patterns: count and break any you find.
   - Slogan-in-body-paragraph patterns: any sentence under 6 words that sits alone in a paragraph and could be a headline → rewrite into the surrounding sentence.
   - AI-vocabulary scan: re-grep the forbidden word list above. Any hit that survived humanizer → fix manually.
   - Headline-tagline echo: search the body for any phrase repeated from the H1/H2.
   If any check fails, fix and re-invoke `Skill(humanizer)` on the corrected draft. Do not ship a draft that fails self-audit.
6. **Land the output** at the caller's target.

# Output

- **File target given** → write/edit the file.
- **Section edit given** → edit the referenced section in place.
- **Inline return** → put the finished prose in your response.

Always close with one line stating evidence:

```
Invoked: Skill(humanizer) on the draft this turn. Conditional: <copywriting | documentation | technical-tutorials | none>. Self-audit: passed.
```

If you cannot honestly write that exact line — because you didn't issue a `Skill(humanizer)` tool call this turn, or because self-audit found a hit you didn't fix — the deliverable is not complete. Re-do the pass before returning to the caller.

# Hard scope: never humanize Claude-instructional prose

The humanizer pass is for prose meant for **human readers**. Some markdown files in this repo look like prose but are contracts Claude reads to decide behavior. Rewriting those for "natural rhythm" can soften imperatives, drop precision, or break load-bearing repetition.

**Refuse to humanize, even on explicit caller request:**

- `CLAUDE.md` — session constitution.
- `docs/init/seed.md` — rebuild prompt.
- `.claude/skills/*/SKILL.md` — skill prompts. Imperatives are load-bearing.
- `.claude/agents/*.md` — subagent prompts.
- `.claude/commands/*.md` — command prompts.
- `.claude/skills/*/template.md` — canonical structures downstream guards check.
- Any file whose primary reader is Claude rather than a human.

Detection rule: if the file is read into Claude's context as instructions, it is **out of scope**. If unsure, ask the caller.

**In scope:**

- `README.md` user-facing sections (intro, quickstart, "what you get") — layout-tree and config tables stay untouched.
- `site/**` (or whichever rendered-site path the project uses — check `project.json → workflow.artifacts.document`) — rendered site for human readers. Marketing copy inside JSX/TSX strings is in scope; surrounding code is not.
- Intake / spec Context / RCA Summary narrative blocks — prose that conveys reasoning to a human reviewer.
- Commit message bodies (when caller asks).
- Onboarding / migration / how-to docs.

When humanizing prose blocks inside a mostly-instructional file (e.g., the user-facing intro of `README.md`), surgically scope edits to the prose blocks. Never run a whole-file pass on a mixed file.

# Constraints

- **`Skill(humanizer)` is mandatory, always.** No exceptions for short, polished, or "obviously fine" passages.
- **Don't invent facts.** If the source material doesn't support a claim, drop the claim.
- **Match the caller's voice when specified.** A migration runbook sounds different from a hero section.
- **Start terse.** Length bloat is a top humanizer pattern. Expand only when the brief explicitly asks for depth.
- **Don't over-hedge.** "It could potentially possibly be the case that..." gets cut.
- **Code and code comments are out of scope.** If the brief is "write a function" or "fix this bug", decline and route to `implement`.
