---
name: rseng-project-kickoff
description: >-
  Covers starting a new research software project with a short kickoff
  interview: asking the user the few questions whose answers actually change
  decisions (goal, software tier, stack, data sensitivity, openness,
  collaboration, compute, deadlines, and how much the agent may decide alone),
  then deriving tier-appropriate defaults, setting the project up, and making
  proactive decisions afterwards while keeping the user informed. Use
  PROACTIVELY when a new project is starting in an empty or fresh directory,
  and when the user asks to kick off, bootstrap or set up a new research
  software project or wants the agent to interview them about it. (Drafting
  SMPs is rseng-management-planning; steady-state operation after setup is
  rseng-project-tracking.)
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Project kickoff: ask well, then decide well

The first hour of a project fixes decisions that cost months to
change later. A short interview beats both extremes: asking nothing
(the agent guesses the user's constraints) and asking everything
(the user abandons the questionnaire). Ask only what changes
decisions, derive the rest, and write down which is which.

## The interview

Eight questions cover what defaults cannot infer. Ask them in the
user's language, batched sensibly, skipping any the context already
answers:

1. Goal and audience: what research question, who runs this
   software - just you, your group, a community? (Sets the tier -
   rseng-quality-framework - which calibrates everything else.)
2. Stack: a language/ecosystem preference, or should the agent
   choose per the state of the art for the domain
   (rseng-language-guides, verified online when unfamiliar)?
3. Data: what data, how big, and is any of it personal or
   sensitive? (Routes rseng-data-management and
   rseng-regulatory-compliance before the first file lands in git.)
4. Openness: license preference and open-science intent - open
   from day one or open at publication (rseng-licensing,
   rseng-open-science-practices)?
5. Collaboration: solo or team, internal or external contributors
   (rseng-community-governance's scale)?
6. Compute: laptop, cluster, GPUs (rseng-hpc-computing,
   rseng-gpu-computing shape structure early)?
7. Deadlines: the research calendar dates that planning works
   backwards from (rseng-project-tracking).
8. The delegation contract - the question most kickoffs skip: which
   decisions may the agent make alone (tooling, structure,
   dependencies within policy) and which always come back to the
   user (scientific choices, anything on the ask-list they name,
   spending, publishing)? Record the answer; it governs the whole
   collaboration (rseng-pair-programming's boundary, made explicit
   per project).

Offer sensible defaults with every question so "accept all" is a
one-word answer for users who want speed.

## From answers to a running project

Derive and execute, don't re-ask: tier-appropriate scaffolding
(rseng-project-scaffolding), version control with guards
(rseng-version-control-review, rseng-security's ignore rules before
any secret exists), environment and lockfile per the chosen stack
(rseng-reproducible-environments), LICENSE and citation files
(rseng-licensing, rseng-citation-metadata), aidecl.yaml from the start
(rseng-ai-declaration), a minimal tracker and the deadline
milestones (rseng-project-tracking), and - when answers warrant -
the data-sensitivity guards, the SMP/DMP skeletons
(rseng-management-planning, rseng-data-management-plans) and a
discovery pass over prior art (rseng-discovery).

## Deciding proactively, keeping the user informed

After kickoff the delegation contract is the operating agreement:

- Decisions inside the contract are MADE, not re-asked - and each
  consequential one is reported as a compact decision note at
  delivery: what was decided, the one-line why anchored in the
  user's answers ("pytest, because you chose Python and asked for
  team-friendly tooling"), and how to change it. Silence is not an
  option; neither is a question that was already answered.
- Decisions outside the contract come back as a short question
  with a recommended default.
- The kickoff answers and every later decision note land in the
  decision log (rseng-project-tracking), so the project's WHY
  survives the chat session.
- Revisit the contract at milestones: trust earned can widen it;
  surprises can narrow it - either direction is a normal
  adjustment, not a failure (rseng-lessons-learned records the
  trigger).

## Working with this skill

This skill is source-independent: it encodes kickoff-interview
practice for AI-assisted research software projects. It
orchestrates the pack's setup skills and hands steady-state
operation to rseng-project-tracking.

Learn more (verified):
  - https://opensource.guide/starting-a-project/ - starting an open
    source project
  - https://learn.scientific-python.org/development/ - Scientific
    Python development guide
  - https://book.the-turing-way.org - The Turing Way handbook
  - https://www.software.ac.uk/resource-hub - Software Sustainability
    Institute resources

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-data-management - data questions route here early
- rseng-discovery - prior-art pass before building
- rseng-management-planning - SMP skeleton after kickoff answers
- rseng-project-scaffolding - executes the scaffolding step
- rseng-project-tracking - hands over steady-state operation
- rseng-quality-framework - tier classification calibrates all defaults

<!-- related-skills:end -->
