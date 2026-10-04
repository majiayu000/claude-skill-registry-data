---
name: shape
description: "Primary pipeline entry for structured requirements discovery. Use first when the problem, scope, or user needs are still fuzzy and you need shared understanding before /research. Not for already-shaped PRDs or implementation-ready work."
sources:
  primary:
    - "Exploring Requirements — Gause & Weinberg"
  secondary:
    - "The Mom Test — Rob Fitzpatrick"
    - "Thinking in Bets — Annie Duke"
    - "Thinking in Systems — Donella Meadows"
    - "Release It! — Michael Nygard"
    - "Domain Storytelling — Hofer & Schwentner"
    - "The Checklist Manifesto — Atul Gawande"
---

# Shape

This skill applies structured requirements discovery to prevent the most expensive class of engineering error: building the right thing wrong, or building the wrong thing right. Quality is a pre-design activity — better solutions come from more accurate problem definition, not from better solution-finding techniques.

Output is shared understanding in the conversation. No file is produced. This normally feeds into `/research` and later `/write-a-prd`, but for work that requires multiple independent PRDs it can instead hand off to `/create-milestone`.

> **One question per turn.** Throughout every phase of this skill, ask one question at a time and wait for the user's answer before asking the next. Never batch questions into a list. This is a conversation, not a questionnaire.
>
> **Prefer single-select.** Use single-select multiple choice when the user is choosing one direction, one priority, or one next step.
>
> **Use multi-select rarely.** Reserve it for compatible sets — goals, constraints, non-goals, success criteria — that can all coexist. If prioritization matters, follow up asking which selected item is primary.
>
> **Use the platform's question tool when available.** In Claude Code, use `AskUserQuestion`; in Codex, `request_user_input`; in Gemini, `ask_user`. Otherwise, present numbered options in chat and wait for the user's reply before proceeding.

Use `/shape` when the problem, user needs, or scope boundaries are still fuzzy and you need shared understanding before doing technical research or shaping. This applies both to ordinary feature work and to larger app-sized or tranche-sized outcomes that may later branch to `/create-milestone`.

Do not start here when the work is already well-shaped enough to research, when the user already has a PRD they want decomposed, or when the task is clearly an implementation or QA task.

## Before You Ask Anything

Before asking a single question, do three things:

**Surface your own biases.** Write down 3-5 assumptions you are making about what the user is building based on what they've told you so far. Show these to the user. The user often corrects an assumption that would have silently distorted every subsequent question. This takes 60 seconds and prevents root-level errors that propagate through every branch of the design tree.

**Separate events from structure.** Before you lock onto the first apparent problem, ask yourself: are you looking at a visible event, or at the underlying structure producing that event repeatedly? If the user describes a symptom that keeps recurring, treat that recurrence as a signal that the real problem may be in incentives, handoffs, delays, missing feedback, or mismatched goals rather than in the nearest visible failure.

**Test the name.** Take the project or feature name the user gave. Critique it — give three ways the name might mislead someone about scope, imply a premature solution, or exclude something important. If any critique lands, propose a sharper name. Names carry hidden scope assumptions: "User Dashboard" implies a single page; "User Activity Center" implies something broader; "User Insights" implies analytics. Resolving this early prevents scope drift downstream.

If the user's name is already precise and no critique lands, acknowledge that and move on. Don't belabor this.

## Phase 1: Open

Start with domain-independent questions before any technical framing. These establish the problem space. Ask one at a time, with your recommended answer for each:

- **What problem does this solve?** Not "what does it do" — problems, not features. If the user leads with a solution ("I need a notification system"), ask what problem they're solving that makes them think they need that solution.
- **Who are the users?** Distinguish who pays (customer) from who uses (user) from who is affected (stakeholder). These are often different people with different authority over requirements.
- **What does success look like?** How would you know this feature succeeded six months from now? This forces measurable thinking.
- **What is this worth?** Time, money, competitive advantage — forces prioritization and reveals whether the investment is proportionate.
- **What happens if we don't build this?** The null alternative. Sometimes the answer is "nothing bad," which is diagnostic — it means the feature is a preference, not a constraint.

**Check for shared vision problems.** If different stakeholders seem to want different outcomes from the same feature, surface that explicitly before continuing. Misaligned goals create false clarity: everyone says yes to the feature, but each person is optimizing for a different result.

**Identify who's missing.** Think about who would use this feature if it worked well but isn't in the conversation. A bad experience drives users away — those absent users can't tell you what they need, so the product stays bad. Also consider who might be harmed or disrupted by this change — every improvement has opponents. Finding them during requirements is cheaper than finding them during rollout.

**Explore the codebase early.** If the user describes an existing system they want to improve, explore the codebase now to understand current state before asking more questions. This grounds the interview in reality rather than imagination.

## Phase 2: Explore

This is the heart of the interview — walking the decision tree one branch at a time.

**Walk each branch to resolution.** For each significant design decision, resolve it before moving to the next branch. Don't jump between topics. Ask one question at a time — present your recommended answer, wait for the user's response, then move to the next question. When you encounter a dependency ("we can't decide X until we know Y"), note it, resolve Y first, then return to X.

**Classify functions as you go.** As features emerge, classify each:
- **Evident** — the user perceives it working (UI, notifications, responses). Usually well-specified because users can see them.
- **Hidden** — operates below the surface (caching, retry logic, auth validation, error handling). These are the most dangerous omissions — nobody mentions them because nobody thinks about them until they're missing. Actively hunt for Hidden functions: "What happens when the network drops? What happens when two users do this simultaneously? What if the data is malformed? What does the admin see?"
- **Frill** — nice to have if resources allow. Don't spend interview time on these beyond noting them.

**Probe hidden functions for stability failures.** When a Hidden function matters to production behavior, ask what happens under cascading failure, 10x load, resource leaks, or missing timeouts. These are often the omissions that only surface after rollout.

**Separate constraints from preferences.** When the user states a requirement, probe whether it's a hard constraint (binary pass/fail, non-negotiable) or a preference (a gradient, negotiable). "It must be real-time" — is 100ms acceptable? 500ms? 2 seconds? If there's a sharp threshold where value drops off a cliff, it's a constraint. If it's "as fast as reasonably possible," it's a preference. This distinction determines which technical approaches are viable in `/research`.

**Probe constraints that feel immovable.** When a constraint seems fixed, gently push: "What if that constraint didn't exist? What would you do differently?" Sometimes constraints are actually preferences that calcified through repetition. Sometimes they're genuinely hard. Either way, you learn something. Go to the source — stated constraints often get distorted through telephone-game relay.

**Stress-test major decisions.** Before accepting any significant design choice, articulate three things that might cause it to fail. This isn't pessimism — it's calibration. If you can't think of three failure modes, you don't understand the decision well enough. Present these to the user: "Before we lock this in, here are three things that could go wrong..."

**Watch for false clarity.** When something seems "obvious" or "simple," that's your cue to probe harder. The plainest language is the most ambiguous. "The user logs in" — with what credentials? Through what provider? What if they're already logged in? What if their session expired? What if they have two accounts? Treat "obvious" as a danger signal, not a green light.

**Surface the governing mental model.** When a user or stakeholder is confident about a cause or solution, ask what belief is carrying that confidence: "What are we assuming is true about why this problem exists?" or "What would have to be true for this solution to be the right one?" The goal is not abstract philosophy — it is to surface hidden assumptions early enough that `/research` can verify them.

**Explore the codebase.** When a question can be answered by reading the code, read the code instead of asking. When exploring reveals constraints the user didn't mention, surface them: "I see the current auth system uses X — does that constrain our approach here?"

## Phase 3: Close

**End by agreement, not completion.** The session ends when you and the user have shared understanding of what to build — not when every conceivable question has been answered. Some questions will be answered by `/research`; some will be resolved during PRD writing; some will emerge during implementation. The goal is "enough understanding to research intelligently," not "every detail specified." Accept imperfection and proceed.

**Present a closing summary.** Before ending, summarize the decisions made in four categories:

- **Choices** — decisions that are settled. The user chose these deliberately. Example: "We're building a real-time presence indicator for the lesson page." These are locked — downstream skills should not re-debate them. Classification schemes, scoring rubrics, taxonomies, role/permission matrices, and decision rules are Choices that must be **enumerated** in the summary, not named in the abstract — listing the categories or levels by name, not just by their count.
- **Assumptions** — things we believe to be true but haven't verified. Tag each with a confidence level (see below). Example: "[Uncertain] We assume Ably's free tier handles our expected concurrent user count."
- **Impositions** — external constraints we can't change. Example: "The app uses Next.js App Router; we can't switch frameworks."
- **Structural signals** — recurring symptoms, delayed effects, missing feedback loops, or stakeholder goal conflicts that suggest the visible problem may not be the underlying one. Keep this list short and concrete. These are prompts for better `/research` and `/write-a-prd`, not a request to fully solve the system during the interview.

**Confidence tags for Assumptions:**

| Tag | Meaning |
|-----|---------|
| `Established` | Well-supported by existing code or prior solutions |
| `Likely` | Reasonable belief, no strong contradicting signals |
| `Uncertain` | Genuinely unknown, multiple plausible answers |
| `Speculative` | Could easily be wrong |

Ask the user to confirm this classification. Anything marked as an Assumption is a direct input to the `/research` phase.

**Close gate (DO-CONFIRM — verify before presenting the summary):**

- [ ] Problem is stated without referencing any implementation or technology
- [ ] At least one appetite or hard constraint is on record (time, scope, or cost boundary)
- [ ] All three stakeholder roles have been named: who uses, who pays, who is affected
- [ ] Every `Uncertain` or `Speculative` assumption has a stated research question attached
- [ ] If a classification scheme, rubric, taxonomy, or decision rule was discussed, its members are enumerated in the summary (not just referenced by count or label)

If any item is unchecked, ask one targeted question to fill the gap before presenting the summary. Do not present an incomplete summary as a handoff.

**This closing summary is the compressed handoff to `/research`.** If `/research` runs in this same session, it should work from this summary rather than re-reading the full interview transcript. If the interview ran long (20+ minutes), suggest the user start `/research` in a fresh session using this summary as context.

For work that requires multiple independent PRDs — where the shaped outcome decomposes into several features that each need their own research-PRD cycle — use this same closing summary as the compressed handoff to `/create-milestone` instead. `/create-milestone` should use it to define a GitHub milestone, feature sequencing, and the first feature to promote from `roadmap bet` to `research-ready`. Note: a blank project or large-scope effort that is still one cohesive product stays on the default path; `/write-a-prd` will create a container milestone for big-batch work.

**At the end of the closing summary, print the runtime handoff line** (default path):

```
**Next session:** /research <feature-slug>
**Input:** paste the closing summary above
```

For the milestone branch, print `/create-milestone <feature-slug>` instead of `/research <feature-slug>` on the first line; the input remains the closing summary.

## Handoff

Hand off to `/research` by default. For work that requires multiple independent PRDs — where the shaped outcome decomposes into several features that each need their own research-PRD cycle — branch to `/create-milestone` instead. Big-batch work (6 weeks) that fits a single PRD stays on the default path and gets a container milestone from `/write-a-prd`. Treat assumptions by confidence tag: `Uncertain` and `Speculative` assumptions are first-priority research targets because they carry the most downstream risk. `Likely` assumptions can usually be confirmed during PRD writing. `Established` assumptions need only targeted verification.

- **Carries forward:** choices, assumptions with their confidence tags, impositions, and structural signals
- **Comes next by default:** `/research`, or `/create-milestone` when the shaped work requires multiple independent PRDs

**Next-step menu.** This is a genuine branch point, so offer the next step as a menu rather than leaving the user to retype a command (see `references/next-step-menu.md`). Present a single `AskUserQuestion` with the recommended step first, each option naming its outcome rather than just its skill: **→ `/research` (recommended — verify the unknowns before the PRD)**, **→ `/create-milestone` (this needs multiple independent PRDs)**, **Keep shaping — the problem is still fuzzy**. The platform's free-text "Other" option is the escape hatch — don't add one.

## What to Avoid

**Premature solutioning.** Don't jump to "how to implement" before "what to build" is clear. If the user starts discussing database schemas before the problem is established, gently redirect: "Let's nail down what this needs to do for the user before we decide how to build it."

**Endless questioning.** If you've been going for 20+ minutes and keep finding new branches, step back: "Do we have enough understanding to move to research? The remaining questions might be better answered by looking at the code and documentation."

**Evaluating during generation.** When the user proposes something, explore it fully before pointing out problems. "Let's follow that thread..." not "That won't work because..."

**Dismissing edge cases.** Never drop an edge case because "no one would do that." Users do everything. The case you're most tempted to exclude is often the most important to keep.

**Accepting stated solutions as fixed.** The user says "I need a dropdown." Do they need a dropdown, or do they need a way to select from options? The stated need is a solution — probe for the underlying desire.
