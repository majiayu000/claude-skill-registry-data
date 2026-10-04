---
name: council
description: Five independent critic subagents in parallel on an idea, plan, design, R&R strategy, grant, or SKILL.md, then a synthesis pass that ranks findings by how much of the argument rests on them, never by vote count. A markdown work plan gets the plan roster (assumptions, pre-mortem, what to delete, alternatives per piece, can it be run as written). TRIGGER on "council", "spawn critics", "parallel critique", "kitchen cabinet", "panel review", "stress-test this", "poke holes in this", "critique my plan", "review this plan", "what would five experts say". A complete manuscript goes to review-paper; a rendered deck to slide-review.
---

# council

Five independent critics, one synthesizer, no majority voting. Single round. Adapted from Chris
Blattman's [claudeblattman](https://github.com/chrisblattman/claudeblattman), including the rule
that the synthesizer ranks by how much of the argument rests on a finding and never by how many critics raised it.

## When to use

- Stuck between two framings of a paper, R&R, or grant, and you want adversarial pressure on both.
- A plan, design, or skill draft is almost right and needs failure-mode pressure before it ships.
- The target is heterogeneous (idea plus design plus venue choice, or a strategy memo) so a
  manuscript-shaped review does not fit.

Not for a complete manuscript you want line-edited and refereed against a journal bar: that is
`review-paper`. Not for numeric or reproducibility audits. This skill produces a checklist and
never edits the target.

## Inputs

| Argument | Default | Meaning |
|---|---|---|
| target | required | file path, or an inline paragraph describing the idea, plan, or decision |
| `--plan` | inferred | force the plan roster; inferred for a markdown plan or project document when no roster flag is given |
| `--chef-skill` | off | swap in the skill-design roster |
| `--goal="..."` | none | the overarching goal the target serves, passed verbatim to every critic; without it each critic infers the goal from the target and states the inference at the top of its output |
| `--critics=a,b,c` | default roster | explicit roster; unknown names become free-form role prompts |
| `--n=K` | 5 | number of critics, hard cap 5 |

A file target may be `.tex`, `.md`, `.qmd`, `.txt`, `.pdf`, `.R`, `.py`, or a `SKILL.md`. Read it
once in the main thread before dispatching, and pass the contents inline to the critics so five
subagents do not each re-read it. This setup assumes the Read tool cannot open a `.pdf` (no
poppler; adjust to your machine), so extract
it with `~/.claude/assets/bin/pdfread.py text <file.pdf>` and pass that text inline. Do not call
`pdftotext`.

If the user asks for more than five critics, refuse: "Hard cap is 5. Pick a tighter panel."

## Default roster (quantitative marketing)

Spawned as `general-purpose` subagents with inline role-string prefixes. No persona files.

1. Skeptic. "Challenge the core claim. What would have to be true for this to be wrong? Where is
   the key assumption the author has not stress-tested? Name the specific assumption in
   this target, not the genre-typical one."
2. Pre-mortem. "It is twelve months from now and this paper, plan, or grant has failed. What is
   the most likely failure mode? Walk back from the failure and name the decision point today at
   which it could have been avoided."
3. Methodologist. "Challenge identification, measurement, and design. Quant-marketing tuned: DiD,
   IV, RD, RCT, discrete choice experiment, eye-tracking, vignette, field experiment, scraped
   panel, and embedding methods. Are the exclusion restrictions defensible? Is the unit of analysis
   consistent with the unit of treatment? Is the clustering level defensible? For ML or GenAI
   components, is train/test/holdout discipline intact, and does anything leak?"
4. Academic editor. "Venue fit, narrative tightness, contribution framing. Default targets
   Marketing Science, JMR, JCR, Management Science; recalibrate if the user signals
   general-science (PNAS, Nature Human Behaviour) or economics. Does the contribution fit that
   audience? Is the framing tight enough for a non-specialist editor? What gets cut, what gets
   expanded?"
5. Harsh referee. "You are the most likely Reviewer 2. Produce the rejection arguments a sharp
   referee at the target venue would write. Do not be balanced. Name the specific objection
   (overclaiming, identification, sample, mechanism, novelty, scope) and write the sentence you
   would put in the report."

Each critic ends with `VERDICT: APPROVE | REVISE | REJECT` plus a one-line rationale.

## `--chef-skill` roster (skill and tool design)

For a `SKILL.md` the user wants stress-tested before installing.

1. Skill engineer. "Will this work, will it last, does the abstraction earn its keep? Invocation
   discoverability (do the trigger phrases match how this user actually talks?), prompt-budget
   discipline, failure recovery, and duplicated coverage against skills already installed."
2. Trigger-overlap critic. "Glob `~/.claude/skills/*/SKILL.md` and read the frontmatter
   descriptions of every installed skill, plus the `hpc:*` plugin skills and the built-in slash
   commands. Where would the user say one phrase and fire the wrong skill? Name the collision and
   the disambiguating phrase that fixes it."
3. Edge-case critic. "What breaks this skill? Empty input, file not found, ambiguous target, a
   PDF with no text layer, an MCP that is not authenticated, a path containing spaces (Overleaf
   project directories all have them), a Dropbox conflicted copy shadowing the real file, a
   project the skill was not tuned for. List the top five and what the skill should do in each."
4. Tooling fit, macOS. "Does this skill match what is actually on this machine? Available: Zotero
   MCP (`mcp__zotero__*`, including semantic search, PDF page reads, annotations, bibliography
   export), Claude in Chrome (`mcp__claude-in-chrome__*`, the user's real Chrome with its logins, one tab group per session, no headless mode), Wiley Scholar Gateway
   (`search_wiley_fulltext`, a semantic passage search over a Wiley-leaning corpus, not a fetcher for
   arbitrary DOIs), WebSearch and WebFetch, and whichever claude.ai connectors the session has
   enabled. Local CLI:
   `~/.claude/skills/reading-papers/scripts/paper.py` (search, resolve, get, author,
   cites, `--json`) for literature lookup and citation checks. This inventory may lag the
   machine, so verify against the live tool list in your own context before flagging a tool as
   missing. LaTeX is MacTeX `latexmk`. This setup assumes
   no Homebrew and no poppler, so `pdftotext` and `pdftoppm` do not exist and the Read tool cannot
   open a PDF; PDFs go through `~/.claude/assets/bin/pdfread.py` (`text` to extract, `png` to
   rasterize a page for Read). Images are read visually by the Read tool. An HPC cluster, if
   you use one, may be reachable as `ssh hpc`. Flag any tool the skill names that is not on this list, any shell
   command that assumes a package manager, any Windows-ism, and any place the skill should be
   using a tool that exists and is not."
5. Cold-start tester. "You are this user three weeks from now, having forgotten the skill exists.
   Read only the frontmatter description. Will you know when to invoke it? Does it tell you what
   to type? Are the failure modes intelligible? If not, name the exact missing phrase."

Each ends with `VERDICT: SHIP | REVISE | REJECT` plus a one-line rationale.

## `--plan` roster (work plans and project documents)

For a markdown plan, a PLAN.md, a pipeline design, a project brief, or any document that says what
will be built and in what order. Every critic gets the goal (from `--goal`, or inferred and stated)
and judges each piece of the plan against it.

1. Skeptic. "Challenge the core claim of this plan: that doing these steps reaches the goal. What
   would have to be true for that to fail? Name the specific assumption in this plan that has not
   been stress-tested, not the genre-typical one, and say what evidence would settle it."
2. Pre-mortem. "It is three months from now and this plan has failed. What is the most likely
   failure mode? Walk back from the failure and name the decision point today at which it could
   have been avoided."
3. Reductionist. "Think from first principles about what this plan is trying to achieve, given the
   goal. Interrogate each piece: is it unnecessary, overly complicated, or resting on a weak
   assumption? First name what can be deleted entirely. Then, with those pieces gone, name what
   can be simplified. Quote each piece you cut or shrink and give the shorter form. A piece that
   moves no reported number and answers no objection is a deletion candidate by default."
4. Alternatives. "Take each major piece of the plan in turn (a method, a model, a package, a data
   source, a step) and ask whether there is a better, more current, more stable, or cheaper way to
   serve its purpose given the goal. Verdict per piece: keep, swap (name the alternative and its
   tradeoff), or drop. Implementability weighs as much as performance: maintained code, published
   weights, a clean licence, a form the user can state in a methods section. You may run up to five
   WebSearch calls, only on pieces where you doubt that your own knowledge is current (models,
   packages, APIs, benchmarks); say which pieces you searched and which you judged from memory."
5. Executor. "You are the agent who will run this plan tomorrow with nobody to ask. Walk it step by
   step. Where does it stop you: a missing input, an undefined threshold, an ambiguous order, a
   step that depends on a result not yet available, a success criterion nobody wrote down, a
   destructive action with no confirmation point? List the top five blockers and the sentence
   that would unblock each."

Each ends with `VERDICT: SHIP | REVISE | REJECT` plus a one-line rationale. `--n=3` keeps the
skeptic, the pre-mortem, and the reductionist.

## Workflow

Phase 0, prep. Parse the target and flags. With `--chef-skill` or `--plan`, lock that roster and
skip target-type inference. Otherwise infer: a `.md` or `.txt` whose headings read as phases,
steps, milestones, or a plan of record takes the plan roster; a paper idea, R&R strategy, grant, or
design memo takes the default roster; say which roster was chosen and why in one line before
dispatching. Read a file target once here; use inline text as-is. Resolve the roster,
truncating to `--n`. Truncation keeps the first K critics in list order, so `--n=3` on the
default roster drops the academic editor and the harsh referee. Create a scratch directory `~/.claude/cache/council_<YYYYMMDD>_<run_id>/`
for raw critic output.

Phase 1, parallel dispatch. This is the key step. Send ONE message containing N subagent
calls, one per critic, so they run concurrently. Never serialize them. Each call uses
`subagent_type: general-purpose`, a three-to-five word description, and a prompt made of the
critic's role string, the goal line (`Goal, as stated by the user: ...` when `--goal` was passed;
otherwise `Goal: not stated; infer it from the target and open your output with the goal you
inferred`), the target content, and: "Produce raw critique in this role's voice. Be
specific to this target, not to the genre. Quote the target where you object to it. End with
VERDICT plus a one-line rationale. Write your output to
`~/.claude/cache/council_<YYYYMMDD>_<run_id>/critic_<role>.md` and also return it as your final
message."

Do not synthesize inline. Do not summarize across critics in the main thread. Collect.

Phase 2, synthesis, a separate call after all critics return. One more `general-purpose` subagent
gets the raw critic outputs, the original target, the report shape below, and this instruction
spelled out verbatim:

> You are not summarizing votes. A single critic raising a key concern outweighs four
> critics who did not notice it. Decide which concerns are key, meaning they would kill
> the paper, plan, or skill if true, and put those first. A minority concern that is key
> dominates. A majority concern that is cosmetic goes to the bottom.

Phase 3, emit. Print the synthesis to the conversation with the raw critic outputs in a
`<details>` block underneath.

## Why the non-majority rule matters

Multi-critic systems drift toward majority voting because counting is the easy aggregation, and
that defeats the point of running specialized lenses. If the methodologist names an identification
problem nobody else noticed, it goes at the top, not at the bottom for lack of seconds. The
synthesizer reasons about which concerns have the most resting on them, never frequency. Re-read its output before emitting:
if it ranked by how many critics agreed, re-spawn it with a sharper instruction.

## Report shape

```markdown
# Council review: <target>

Date: YYYY-MM-DD | Mode: <default | plan | chef-skill> | Goal: <stated | inferred: ...> | Critics: <N> (<roster>)
Synthesizer verdict: <SHIP | REVISE-MINOR | REVISE-MAJOR | REJECT-AND-REFRAME>

## Key concerns (action required)
1. [lens] <concern>. Why it matters, one sentence. Recommended fix.

## Second-tier concerns
- [lens] <concern>. Recommended fix.

## Polish (optional)

## Per-critic verdicts
| Critic | Verdict | Rationale |

## Contradictions between critics
<If two critics disagree, for example the editor wants the contribution framing expanded and the
referee calls the same passage overclaiming, surface it and recommend a reconciliation. Never
silently average them.>

<details><summary>Raw critic outputs</summary>
<each critic's raw output, headed by lens>
</details>
```

## Failure modes

Target unreadable (path wrong, PDF has no text layer, `.tex` with unresolved `\input`s): surface
the error and ask for a clean version. Do not dispatch critics on empty content.

A critic returns empty or off-topic: mark it DEGRADED in the synthesis and continue. Re-spawn it
once at most; never block the report on one critic.

Every critic approves: report it honestly with a SHIP verdict. Do not manufacture concerns to
justify the run.

`--chef-skill` on a non-skill target: say so and ask whether to switch to the default roster.

`--plan` on a paper idea or a manuscript: run it anyway, since the reductionist and alternatives
lenses apply to a research design too, but say that the default roster carries the venue and
referee pressure this run will not.

## Out of scope

Round-two critic calls, because multi-round debate drifts toward conformity. Auto-applying fixes.
Model-invented personas: the roster is default, `--chef-skill`, or explicit `--critics=`.
