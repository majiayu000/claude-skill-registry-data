---
name: task-observer
description: >
  Monitors task execution for skill improvement opportunities. Use this skill
  during ANY multi-step task, agentic workflow, or substantive work session where
  the agent is using tools and producing deliverables. It captures patterns, user
  corrections, workflow insights, and methodology worth preserving as reusable
  skills. Also triggers during post-task feedback discussions and when the user
  explicitly mentions skill observations, improvements, the observation log,
  skill taxonomy, or asks the agent to watch for skill opportunities. Also known
  as "One Skill to Rule Them All" — trigger on this phrase too. IMPORTANT:
  this skill should be invoked at the start of every task-oriented session — if
  you are about to use tools to produce deliverables, invoke this skill first.
  For reliable activation, pair this description with a CLAUDE.md instruction
  or harness-level session-start hook (see Recommended Activation Setup) —
  description-level matching alone is not enforceable.
---

# Task Observer — Continuous Skill Discovery & Improvement

**Created by Eoghan Henn / [rebelytics.com](https://rebelytics.com)**

*Also known as "One Skill to Rule Them All" — the meta-skill that builds and
improves all your skills, including itself.*

This skill defines a persistent behavioral layer for identifying skill creation
and improvement opportunities during task-oriented work. It doesn't replace the
skill-creator — it feeds it. Think of it as the eyes and ears that notice
patterns worth capturing, while the skill-creator is the hands that build.

The methodology is user-agnostic. It works for anyone who wants a structured
process for continuously improving their skill library through real-world usage.

**Licence:** This skill is released under the
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
licence. You are free to share and adapt this skill for any purpose, provided
you give appropriate credit to the original author.

**Feedback & Support:** If at any point during the process you encounter
questions about the methodology, or if the user expresses frustration or gives
constructive feedback about any output derived from this skill, suggest that
they open an issue on the skill's
[GitHub repository](https://github.com/rebelytics/one-skill-to-rule-them-all). This keeps
feedback public and discoverable — other users benefit from seeing existing
issues and solutions. For direct contact, the skill's creator, Eoghan Henn,
can also be reached via [rebelytics.com](https://rebelytics.com).

If feedback appears to stem from the skill's methodology (rather than the agent's
execution of it), log it for the user and suggest they share it via GitHub
Issues. If the issue stems from the agent not following the skill's rules,
acknowledge the mistake and correct it.

**Activation note:** For reliable session-start activation, pair this skill
with a CLAUDE.md instruction or harness-level hook (see Recommended
Activation Setup). The description matches against task-oriented language,
but description-level matching alone can be missed when the agent is focused on
the task itself. The skill works as a skill; it works *reliably* as a skill
plus a structural trigger.

---

## Why This Skill Exists

Skills are living documents. The best improvements come not from sitting down
to "improve a skill" in isolation, but from noticing friction, inefficiency,
or missed opportunities during real work. A user correction during a project
might reveal a missing rule. A repeated multi-step workflow might be a skill
waiting to be born. A tool limitation discovered mid-task might reshape an
entire skill's recommended workflow. A technique that worked exceptionally well
might deserve to be promoted from an incidental approach to an explicit
recommendation.

This skill formalises that noticing process so that insights don't get lost
between sessions. Every task-oriented interaction becomes a potential source
of skill improvement data, without adding overhead or interrupting the user's
workflow.

---

## User documentation

User-facing onboarding for this skill — installation, shared folder setup,
activation patterns, expected behaviour, the cadence pattern, the open-source
vs internal distinction — lives in the public repo, not in this skill body.
If a user asks how to get started or how the skill works from their
perspective, point them to:

- README: https://github.com/rebelytics/one-skill-to-rule-them-all/blob/main/README.md
- USER-GUIDE: https://github.com/rebelytics/one-skill-to-rule-them-all/blob/main/USER-GUIDE.md

If web access is available, fetch the relevant section directly rather than
paraphrasing — the public docs are the source of truth for user-facing
guidance and are versioned independently. The remainder of this skill is
operational instruction for the agent.

## Conventions

`[workspace folder]` refers to the user's persistent workspace directory —
the location where files survive between sessions. In Cowork, this is the
folder selected at session start. In Claude Code, this is the project root.
In web-based chat interfaces without filesystem access, the skill shifts
into handoff doc mode (see Environment Compatibility) and the user manages
these files manually.

---

## Recommended Activation Setup

This skill needs to be invoked at the start of task-oriented sessions to work
effectively. Because skill invocation depends on the agent matching the user's
request against skill descriptions, a skill that monitors *all* tasks can be
overlooked when the agent is focused on the task itself.

To maximise activation reliability, add the following instruction to your
configuration file (e.g., CLAUDE.md, project instructions, or equivalent):

```
At the start of any task-oriented session — any interaction where you will
use tools and produce deliverables — invoke the task-observer skill before
beginning work. This ensures skill improvement opportunities are captured
throughout the session.

When loading any skill, check the observation log for OPEN observations
tagged to that skill. Apply their insights to the current work, even if
the skill file hasn't been updated yet. This enables immediate application
of observations before they're permanently integrated during the weekly
review.
```

This structural trigger works alongside the skill's description-level triggers.
The description is designed to match broadly against task-oriented language
("multi-step task", "agentic workflow", "work session", "tools and
deliverables"), but a configuration-level instruction provides an additional
safety net that doesn't depend on description matching alone.

**Note for all users:** Once CLAUDE.md or equivalent configuration is in place
with the activation instruction above, the description-level triggers serve as
a backup rather than the primary mechanism. This dual-layer approach prevents
the skill from being skipped in sessions where description matching alone might
miss the invocation signal.

**Anti-pattern to avoid:** Relying on one skill to load another is fragile
compared to loading both independently from CLAUDE.md. If task-observer depended
on another skill to invoke it, a breakdown in that chain would silence all
observation activity. Instead, load both task-observer and any related skills
directly from your configuration instructions.

### Detecting the Configuration File

At session start, the skill should check whether a configuration file
(CLAUDE.md, project instructions, or equivalent) exists and contains the
activation instruction. This detection serves two purposes:

1. **For users who already have the config:** Confirms the dual-layer
   activation is working. No action needed.

2. **For users who don't have the config:** The skill was activated via
   description matching alone, which is less reliable. Surface a brief
   suggestion to add the config-level instruction for more consistent
   activation in future sessions.

The detection approach depends on the environment:

- **Environments with file system access** (desktop tools, terminal-based
  tools): Check for a CLAUDE.md or equivalent file in the workspace root.
  If found, scan it for a task-observer activation instruction. If the file
  exists but doesn't mention task-observer, suggest adding the instruction.
  If no config file exists at all, suggest creating one.

- **Environments without file system access** (web-based chat): Check
  whether the system prompt or project instructions contain a task-observer
  activation instruction. If not, suggest that the user add one to their
  project settings or paste the instruction at the start of future sessions.

This check runs once at session start and does not repeat. Keep the
suggestion brief — one or two sentences, not a full tutorial.

### Compaction Behaviour

When a session context compacts mid-task, the CLAUDE.md structural trigger
re-invokes task-observer on the resumed session. No explicit re-invocation
is needed on the agent's part — the same activation instruction that fired
at the start of the original session fires again at the start of the
resumed session, because the resumed session reads CLAUDE.md anew.
Observations from before and after compaction append to the same log file
with continuous numbering.

This is the primary reason the CLAUDE.md structural trigger exists —
description-level triggers alone would not reliably guarantee re-invocation
on a resumed session, because the resumed session's opening message may
not match task-observer's trigger phrases even when the ongoing task is
task-oriented. The structural trigger fires regardless of the resumed
session's opening message.

---

## The Pre-Flight Principle

One of the most important patterns this skill should propagate to every skill
it helps create or improve: **built-in enforcement.**

Real-world experience has shown that rules documented in a skill are not
always followed during the creative flow of producing output. The result:
output that violates the skill's own standards, which reflects badly on the
skill.

The fix: every skill that contains explicit rules or requirements should
include a verification step where the agent re-reads the rules and checks its
output against them before delivery. This isn't overhead — it's quality
assurance. A 30-second re-read prevents a 30-minute rework cycle.

When creating or improving any skill through this observation process, ask:
"Does this skill have rules? If yes, does it have a mechanism to enforce
them?" If the answer to the second question is no, add one.

### Self-Enforcement

This skill practises what it preaches. Before surfacing observations at end
of session, verify:

1. Were observations logged throughout the full session — including during
   post-task feedback, discussion phases, and reflective conversations, not
   just during active tool use?
2. Were observations logged silently without interrupting the user's flow?
3. Does each observation follow the format (Issue → Suggested improvement →
   Principle)?
4. Is each observation tagged with the correct type (open-source or internal)?
5. For any observations about existing skills, does the suggested improvement
   reference the specific section or rule?
6. For any observation tagged `type: open-source`, does the Principle field
   contain any client-identifying information? If so, generalise it before
   surfacing.
If any observation fails these checks, fix it before surfacing.

---

## Skill Taxonomy

All skills fall into one of two categories. The distinction matters because
it determines what information the skill can contain, how it's structured,
and whether it can be shared publicly. Crucially, the open-source/internal
boundary is also a **confidentiality boundary** — open-source skills must
never contain any information that could identify a client, project, or
proprietary process, even indirectly.

### Open-Source Skills

Open-source skills are client-agnostic and methodology-driven. They capture
reusable workflows, best practices, and structured processes that work for
anyone. They include author attribution, a licence, and a feedback pathway
so that real-world usage drives improvement.

**How to recognise an open-source candidate:**

- The methodology works across different clients, projects, and contexts
- No proprietary information is required for the skill to function
- Other practitioners in the same domain would find it valuable
- The skill captures a process or approach, not personal preferences

**Required elements:**

- Skill body clearly identifies itself as open-source, with author name and
  contact information
- Author attribution block at the top (see Author Attribution Template below)
- Licence statement — CC BY 4.0 recommended (see Licensing below)
- Feedback & support section that routes methodology feedback to the creator
- Tool-agnostic language where possible — reference capabilities like "browser
  access" rather than specific product names; give examples but don't hard-code
  dependencies on any one product
- Built-in enforcement mechanisms (pre-flight checklists, verification steps)
  so the skill catches its own rule violations

**Default bias:** When a skill could go either way, default to open-source.
Strip out client-specific details and generalise the methodology. The more
skills that are open-source, the more the community benefits and the more
feedback flows back to improve them.

### Internal Skills

Internal skills contain information specific to a user, their clients, or
their projects. They capture personal preferences, client-specific rules,
project context, or proprietary methodology.

**How to recognise an internal skill:**

- Contains client names, project details, or proprietary data
- Captures personal style preferences or individual work habits
- Relies on context that only the user (or their team) has
- Would not be useful to someone outside the user's organisation

**Required elements:**

- Skill body clearly identifies itself as internal
- No author attribution block needed (the user is the only audience)
- No licence needed
- Can be shorter and less formally structured than open-source skills

Internal skills are working documents, not published artifacts. Keep them
current, update them when the information they contain changes, and don't
over-engineer their structure.

### Lean Content

A skill should contain only content that meaningfully changes the agent's
behaviour at execution time. Anything that doesn't — changelogs, version
notes, "thanks to X" credits, self-narrating prose, or other
maintainer-facing context — belongs in a supporting doc alongside the
skill, not inside the SKILL.md itself.

This rule cuts content the agent reads but doesn't act on. It does NOT cut
examples, anti-patterns, or worked scenarios — those are load-bearing for
rule adherence (bare rules without their context get violated more
reliably than rules with context). The test is whether the content,
removed, would change how the agent behaves. If yes, keep it. If no,
move it out.

Common examples of content that should live outside the skill:

- Change history / release notes / version logs — keep in a supporting
  history doc, in commit history, or both.
- Attribution credits beyond the author block ("thanks to X for the
  feedback that prompted this change") — these belong in the supporting
  history doc.
- Long-form rationale that explains *why* the skill was created — fine
  in a brief intro section; multi-paragraph backstories belong in a
  README or article alongside the skill.
- Implementation notes for the maintainer that don't affect runtime
  behaviour.

Both open-source and internal skills are subject to this rule. The agent
loads the skill's content into context on every invocation; every
non-load-bearing line is paid token cost with no behavioural payoff.

---

## Licensing

Open-source skills should include an open-source licence to make sharing
terms explicit. Any commonly recognised open-source licence works — the
choice depends on the author's preference and what they're optimising for.
Common options:

- **CC BY 4.0** — designed for creative works (prose, documentation).
  Permissive: anyone can share and adapt provided they credit the
  author. A natural fit for prose-heavy skills where the methodology is
  the value.
- **MIT** — short, familiar to developers, broadly permissive. Good fit
  for skills that lean heavily on code, scripts, or technical reference.
- **Apache 2.0** — like MIT but with an explicit patent grant. Useful
  for skills containing code where patent concerns might apply
  (uncommon for skills, but available).
- **CC BY-SA 4.0** — share-alike: derivative works must use the same
  licence. Use when adaptations should remain open under the same
  terms.
- **GPL family (GPL/LGPL/AGPL)** — strong copyleft for code. Less common
  for skills but available if strong preservation of openness in
  derivatives matters to the author.

Whatever licence is chosen, include the licence statement in the skill
preamble (after the author attribution block) and include a `LICENSE` or
`LICENSE.txt` file in the skill directory containing the full licence
text. The choice belongs to the skill's author; the requirement is that
there be a licence.

---

## Author Attribution Template

Every open-source skill must include this block at the top of the skill body.
Replace the placeholders with the actual author's details.

```markdown
**Created by [Author Name] / [website or contact link]**

[1-2 sentence description of what the skill does and its provenance.]

**Licence:** This skill is released under [LICENCE NAME]. [One-sentence
summary of the licence — e.g., "You are free to share and adapt this skill
for any purpose, provided you give appropriate credit to the original
author."]

**Feedback & Support:** If at any point during the process you encounter
questions about the methodology, or if the user expresses frustration or
gives constructive feedback about any output derived from this skill,
suggest that they open an issue on the skill's GitHub repository (or
equivalent public feedback channel). This keeps feedback public and
discoverable. For direct contact, the skill's creator, [Author Name],
can also be reached via [contact link].

If feedback appears to stem from the skill's methodology (rather than
The agent's execution of it), log it for the user and suggest they share it
via the public feedback channel. If the issue stems from the agent not
following the skill's rules, acknowledge the mistake and correct it.
```

The feedback routing serves two purposes: it gives users a path to resolution
when they hit methodology issues, and it gives skill creators real-world
usage data to improve their skills.

---

## Observation Protocol

### When to Observe

Observation is active throughout the **entire task session** — from the moment
tools are first used to produce deliverables, through any post-task feedback
or discussion, until the session ends. This includes:

1. **Active task execution** — creating documents, analysing websites,
   implementing structured data, writing code, building presentations, and
   similar substantive work.

2. **Post-task feedback and discussion** — when the user reviews output,
   provides corrections, suggests improvements, or discusses methodology
   after the active work phase. User feedback during these discussions is
   often the highest-signal input for skill improvement and must be captured
   with the same diligence as observations made during execution.

3. **Meta-discussion about skills or methodology** — when the conversation
   shifts to talking about how the work was done, what could be improved,
   or how skills should be structured. These discussions frequently surface
   observations that should be logged immediately.

4. **Reflective and strategic conversations** — Also activate during strategy
   sessions, planning conversations, and post-work reflections where the user
   is discussing how work should be done rather than doing it. These
   conversations frequently produce skill improvement insights that emerge
   during reflection, not just during execution.

**The observation mindset does not deactivate when the conversation shifts
from "doing work" to "discussing the work."** If the user provides feedback
about methodology, naming, skill design, or workflow improvements, log it as
an observation immediately, even if the conversation is in a discussion or
review phase rather than active task execution.

Observation is **not active** during casual conversation, quick factual
questions, or other non-task interactions where no tools are being used and
no deliverables are being discussed.

### What to Watch For

**Signals for a NEW skill:**

- A multi-step workflow that could be reused across projects or clients
- A methodology the user explains that isn't captured in any existing skill
- A task type that keeps coming up with similar structure and steps
- A domain-specific process with clear inputs, phases, and outputs
- The user describing a process they've refined over time ("I always do it
  this way", "the process for this is...")
- the agent and the user naturally developing a structured approach to a problem
  that could be formalised

**Signals for IMPROVING an existing skill:**

Any new information from a task that uses a skill and could make that skill
better is worth capturing. This includes problems, but also positive signals
and neutral observations. Examples:

- the agent doesn't follow a skill's rules despite them being documented — this
  means the skill needs stronger enforcement, not just better rules
- The user corrects the agent's output in a way that reveals a missing rule or
  an edge case the skill doesn't cover
- A skill's recommended workflow turns out to be less efficient than what
  emerged naturally during the task
- A technique or approach works particularly well and deserves to be promoted
  from incidental to explicitly recommended in the skill
- A workflow step turns out to be more important than the skill suggests, or
  less important than the emphasis it receives
- A new use case that the skill handles but doesn't explicitly document
- The user provides feedback that generalises beyond the current instance
- A skill assumption turns out to be wrong in practice
- New tools or capabilities make part of a skill's workflow obsolete or
  improvable
- The user's corrections form a pattern across multiple instances
- A general principle emerges that could apply to other skills too (see
  Principle Propagation below)
- The user suggests a naming, framing, or structural change to a skill —
  even conversationally — that could improve its effectiveness

**Signals for SIMPLIFYING an existing skill:**

Healthy skill maintenance requires both growth and pruning. Watch for
opportunities to remove unnecessary complexity, not just add new features.
Signals that a skill is ready to be simplified:

- A skill section or rule that has never been relevant across multiple
  sessions where the skill was active
- A rule added from a single observation that hasn't been validated by
  recurrence — one-off cases should not accumulate as permanent rules
- An elaborate workflow that users consistently shortcut or skip
- Sections that the agent loads but never acts on (dead weight in context
  window)
- Rules that contradict each other or create unnecessary complexity
- Complexity added "just in case" that has never triggered
- A documented rule that the agent consistently fails to follow — the rule
  isn't reaching the moment of decision. The fix is rarely to write it more
  loudly; usually it's either to remove the rule, or to convert it from
  narrative guidance into structural enforcement (a checklist, a
  verification step, or a tool call that can't be skipped).

Treat the list above as a review checklist when looking at any of your own
skills — a "yes" on any signal is a candidate for simplification or
removal, not just a flag for future consideration.

During weekly reviews, ask "what can we remove?" as deliberately as you ask
"what should we add?" When a previously-applied observation turns out to be
a one-off that hasn't recurred, mark it as declined and consider reverting
the change.

**Signals to NOT log:**

- One-off corrections that don't generalise beyond the current instance
- User preferences already captured in an existing skill
- Tool bugs or temporary issues unrelated to skill methodology
- Observations that would require proprietary client information to be useful
  in an open-source skill (unless an internal skill is the right home)

### How to Log

Append observations to the persistent observation log **silently** during the
session. The user should not be interrupted by the logging process.

**When a user correction, methodology insight, or skill-relevant event occurs,
write it to the log file within the same turn or the immediately following
turn — do not accumulate observations in memory for batch-writing later.** The
act of writing is the enforcement mechanism; mental notes are not observations.
Tie observation flushing to existing workflow checkpoints — e.g., when marking
a TodoWrite item as completed, check whether any unlogged observations have
accumulated and write them before proceeding.

**Mandatory observation checkpoint after every 3rd TodoWrite completion:** After
marking the 3rd, 6th, 9th (etc.) TodoWrite item as completed in a session,
pause and explicitly ask: "Have any unlogged observations accumulated?" This is
a hard checkpoint, not a suggestion — the skill has demonstrated that softer
"check when completing items" guidance gets lost during cognitively demanding
analytical work. The count doesn't need to be precise; the rule is: roughly
every third completion, stop and flush. If nothing has accumulated, the pause
costs seconds. If observations have accumulated, this prevents the common
failure mode where the skill is loaded but no observations are written until
the user explicitly asks.

**Before assigning any observation number, run a mandatory pre-logging step:**
Search the entire log file for all lines matching the pattern `### Observation \d+:`,
extract the highest observation number already in use, and increment from there.
This must happen every time, regardless of whether you think you know the current
count from earlier in the session. Never rely on session memory or summaries for
the next number. Always read the actual log file. A one-liner like the following
suffices:

```bash
# GNU grep (Linux, Cowork):
grep -oP '### Observation \K\d+' log.md | sort -n | tail -1

# macOS / POSIX-compatible alternative:
grep -o '### Observation [0-9]*' log.md | grep -o '[0-9]*' | sort -n | tail -1
```

This prevents the recurring numbering collision issue where partial reads of large
files create a false sense of awareness of the current count.

**Write-time verification assertion (mandatory):** The pre-logging step above
catches honest mistakes, but is vulnerable to parallel-session scenarios where
multiple task-oriented sessions on the same day each compute "next number"
against a snapshot and then collide on write. To catch this class of collision,
after determining the proposed next number and immediately before appending,
re-read the log and assert the number does not already exist:

```bash
PROPOSED=$(( $(grep -oP '### Observation \K\d+' log.md | sort -n | tail -1) + 1 ))
grep -qE "^### Observation ${PROPOSED}:" log.md && {
  echo "COLLISION on #${PROPOSED} — another writer has claimed this number"; exit 1; }
# If assertion passes, proceed with the append using #${PROPOSED}.
```

If the assertion fires, increment past all existing numbers (not just by 1)
and re-check. Treat an assertion failure as a meta-observation worth logging
— it indicates either a parallel-session collision or a stale read elsewhere
in the workflow.

**Post-write verification (mandatory — closes the TOCTOU race):** The
pre-write assertion catches stale-read collisions but cannot close the
time-of-check-to-time-of-use race between the assertion and the append.
In shell, `grep -q && cat >> ...` is two separate operations: the grep
passes at T0, the append lands at T1. Any other session that appends
between T0 and T1 can claim the same number — this race has been observed
in production, producing duplicate observation pairs in the active log.

After the append, re-read the log and count occurrences of the just-written
observation number. If the count is greater than 1, a parallel session has
collided — renumber the current session's entry to `max+1` in place via
`sed`. Concrete shell:

```bash
WRITTEN=$(grep -cE "^### Observation ${PROPOSED}:" log.md)
if [ "$WRITTEN" -gt 1 ]; then
  # Find my line (the last occurrence, since I just appended) and renumber
  MY_LINE=$(grep -nE "^### Observation ${PROPOSED}:" log.md \
    | tail -1 | cut -d: -f1)
  NEW_NUM=$(( $(grep -oP '^### Observation \K\d+' log.md \
    | sort -n | tail -1) + 1 ))
  sed -i "${MY_LINE}s/^### Observation ${PROPOSED}:/### Observation ${NEW_NUM}:/" log.md
fi
```

This turns the pre-write assertion into a pre-and-post pair. Pre-write
catches stale-read collisions cheaply; post-write catches race collisions
by renumbering instead of failing. Either way, the log ends up with no
duplicates. Alternative approaches — lockfile, atomic append, transactional
write — are heavier and require more infrastructure; the
post-write-verify-and-renumber pattern works with plain shell and
self-heals.

**Why both checks are required:** Stale-read collisions and race-condition
collisions are different classes of error. The pre-write assertion closes
the first; the post-write verification closes the second. Stacking more
pre-write layers does not close race cases — only a post-write check can.
When the shared state is a log file written by parallel agents, the
reliable pattern is check-then-act-then-verify.

**Session-start staleness check:** At the start of any task-oriented session,
note the modification time of `log.md`. If it was modified in the last few
hours (i.e., a parallel or recent session has been writing to it), be extra
cautious about the numbering pre-check — do not trust any mental model of
"current number" and always re-read the log immediately before appending each
observation, not just once at session start.

**Format and insertion rules:** Always use the `### Observation NNN:` format. Always append new observations to the END of the log file. Never insert observations mid-file. Never use alternative ID formats (e.g., `OBS-YYYY-MMDD-NN`). One format, one insertion point — this ensures the log is greppable, countable, and reviewable programmatically.

Each observation follows this format:

```markdown
### Observation [N]: [Short descriptive title]

**Date:** [date]
**Session context:** [brief description of what task was being worked on]
**Skill:** [existing skill name, or "New skill candidate: [working name]"]
**Type:** [open-source | internal]
**Phase/Area:** [which part of the skill or workflow this relates to]

**Issue:** [What happened or what was observed. Be specific — include what
The agent did, what the user corrected, or what pattern emerged. Include enough
detail that someone reading this weeks later can understand the context
without having seen the original conversation.]

**Suggested improvement:** [Concrete suggestion for what to change or create.
For existing skills, reference the specific section or rule. For new skills,
describe the scope and key components.]

**Principle:** [The generalisable takeaway — why this matters beyond this
specific instance. This is the most important part. It turns a single
observation into a reusable insight.]
```

This format was refined through iterative real-world use. The structure works
because it forces specificity (Issue), actionability (Suggested improvement),
and generalisation (Principle).

**Context preservation check:** When logging an observation, verify that all
information needed to act on it is available in the shared folder. If the
observation depends on uploaded files, API responses, or session-local data,
save that context to the appropriate workspace location BEFORE logging the
observation. Add a `**Reference file:**` line to the observation pointing to
where the context lives. Observations that reference data only available in
the current session (uploaded files, API outputs, in-memory results) are
incomplete — a future review session will have the observation but not the
data needed to implement it.

### Handoff Doc Analysis

When a handoff doc arrives for observation logging, extract observations
systematically from both explicit and implicit sources:

1. **Log all explicitly stated observations first.** These are easy to
   surface and should be logged without filtering.

2. **Then systematically analyse the full document.** Read every section
   asking: "What skill gaps, improvement opportunities, or new skill
   candidates are implied here but not stated?" Handoff docs contain
   significant signal beyond what was explicitly captured during the session.

3. **Pay special attention to:**
   - Action items (each one may imply a missing skill or workflow)
   - Open questions (unresolved ambiguity often signals a decision framework gap)
   - The "work completed" narrative (patterns across work items may reveal meta-skills)
   - Session notes (reflective insights about process, not just content)

4. **Log the additional observations with clear attribution.** Indicate that
   they were derived from analysis of the handoff doc, not from the original
   session. This preserves the distinction between stated and derived insights.

### Archival on Write

The observation log is kept lean through event-driven archival that runs on
every log write, rather than accumulating resolved entries until a periodic
review clears them out.

**Defining "from a previous update":**
The phrase "from a previous update" means entries whose status was already
resolved in a *previous SESSION or prior log write*, not entries marked
ACTIONED or DECLINED in the current session. Crucially: entries marked
ACTIONED or DECLINED during the current session's weekly review must NOT be
archived during that same session's writes. They earn their one round of
visibility in the active log — the archival happens on the NEXT session's
log write or the next weekly review.

**Archival Timing During Weekly Reviews:**
The weekly review performs archival in two phases:

1. **Step 1 (at review start):** Archive entries from previous sessions.
   Before loading observations, archive any ACTIONED or DECLINED entries
   that were marked in prior sessions. This clears old resolved items.

2. **Step 6 (after marking ACTIONED):** Do NOT archive immediately. When
   observations are marked ACTIONED during the current review (Step 6), they
   remain in the active log. Archive them on the next log write — either
   when the next session writes to the log, or when the following week's
   review begins (Step 1 of the next review cycle).

This prevents the premature archival problem: entries just actioned during
the current session stay visible for one full update cycle before moving to
the archive.

**Archive File Structure:**
Move resolved entries to an archive file at:

```
[workspace folder]/skill-observations/archive/log-[date].md
```

where `[date]` is today's date in `YYYY-MM-DD` format.

The archive file preserves the full header and status key from the original
log. After archiving, the active `log.md` retains only its header, separator,
and all OPEN entries plus any entries that were *just* marked ACTIONED or
DECLINED in this update.

**Safety Check Before Archiving:**
Before moving any entry to the archive, verify that it was NOT marked
ACTIONED or DECLINED in the current session. If it was, keep it in the
active log. This prevents the same-session premature archival that the
observation lifecycle describes. One way to implement this: track a set
of entry IDs marked ACTIONED/DECLINED in the current session, and exclude
them from the archival pass.

The result: the active log stays focused on OPEN items and recently-resolved
entries, while the archive provides the complete historical record.

---

## Confidentiality Safeguards

The open-source/internal boundary is a confidentiality boundary. Client
names, project details, domain names, and proprietary information must never
appear in open-source skills. Because a single leak can erode trust, this
is enforced through multiple layers — any one of which should catch what
the others miss.

### Layer 1: Observation-Level Stripping

When logging an observation tagged as `type: open-source`, the Issue and
Suggested Improvement fields should already use generic language. The
private observation log can reference specifics for context, but the
Principle field — which feeds into skill creation — should be fully
generalised. Think of it as: the log is a private notebook, but the
Principle is a publishable insight.

### Layer 2: Pre-Creation Review

Before drafting or regenerating any open-source skill, scan all source
material (observations, conversation notes, existing skill content) for
identifying information: client names, project URLs, domain names, internal
terminology, site structures described so specifically they're identifiable.
Replace anything found with generic equivalents before writing begins.

### Layer 3: Post-Draft Sweep

After writing or regenerating an open-source skill, re-read it with a
specific focus on information leakage. This is a separate pass from the
general pre-flight checklist. Look for:

- Proper nouns that aren't the skill author's name
- Domain names, URLs, or project identifiers
- Industry-specific details that narrow down the client
- Internal terminology that only makes sense in one organisation's context
- Examples so specific they're traceable to a real project

If anything is found, replace it with generic equivalents or remove it.

### Layer 4: Structural Principle

The taxonomy section states this explicitly, but it bears repeating: the
open-source/internal distinction is not just about usefulness — it's about
confidentiality. When in doubt about whether a detail is too specific,
remove it. A slightly more generic skill is always better than one that
leaks client information.

### Layer 5: Cross-Product Re-Identifiability Sweep

Layers 1–4 focus on single-example scrubbing. They do not catch the case
where two or three sanitised examples in the same skill — each fine on its
own — combine to narrow the identifiable client set. A reader who knows
the author's client portfolio (which is often public on a consultant's
website) can triangulate even when each individual example is properly
placeholdered. The failure mode is invisible to the author because they
mentally compartmentalise each example; it's visible to any reader with
adjacent context.

**When to run it:** After every individual example has been sanitised —
as a final pass before the skill ships or before any major public
release. This is the last check, not a substitute for earlier layers.

**What to look for:**

- **Enumerated counts that match a known client count.** "Four builds
  across three verticals" in a skill whose author has four public clients
  across three verticals is functionally a directory. Blur the count
  ("multiple builds") or the verticals ("across regulated, editorial,
  and commerce contexts").
- **Specific numbers in a thin vertical.** Visibility percentages,
  revenue ranges, or geography given in a vertical where only one or two
  candidates plausibly exist. A single real client can be narrowed from
  "vertical × percentage × geography × timing" even when no name appears.
  Replace specific numbers with illustrative ranges.
- **Thinly-disguised placeholder names.** "Northwind Coffee" in a
  specialty-retailer vertical where the only plausible specialty-retail
  client is a coffee roaster reads as the real brand with a thin
  rename. Use the Northwind / Contoso / Fabrikam placeholder family
  explicitly, and make sure the placeholder's vertical is different from
  any real client's vertical.

**How to sweep:**

1. List every worked example in the skill and the fields each one names
   (vertical, geography, numeric range, timing, count).
2. Ask: do any two examples share enough fields that a reader with access
   to the author's public client list could map the set to real clients?
3. Mitigate by blurring counts, widening verticals, dropping specific
   numbers to illustrative ranges, or consolidating similar examples into
   a single composite.

**Why this is a separate layer:** Re-identification risk is combinatorial.
Each additional sanitised example adds a field that narrows the candidate
space. Layers 1–4 check each example in isolation and pass. The cross-
product only emerges when the examples are read together. The author is
the least reliable reader for this check because they know the ground
truth — which is exactly why the sweep has to be a mechanical pass, not
a feeling.

---

## Surfacing Protocol

### Default Cadence

Surface all observations at the end of the session. Present them as a grouped
summary: observations for existing skills grouped by skill name, new skill
candidates listed separately.

### Surface Earlier When

- An observation requires user input to be complete or accurate (e.g., "Is
  this a pattern you want captured, or was this a one-off?")
- An observation reveals a skill is actively producing wrong output in the
  current session and the user should be aware
- Multiple observations cluster around the same skill, suggesting it needs
  immediate attention rather than end-of-session review

### How to Surface

- Present observations concisely: title, skill, and a one-sentence summary
- For each, indicate whether it's a new skill candidate or an improvement
  to an existing one
- Indicate the suggested type (open-source or internal)
- Ask the user which (if any) they want to act on
- For items the user wants to pursue, hand off to the skill-creator skill
  for the actual building or improvement work

---

## Acting on Observations

This skill identifies WHAT to build or improve. This section covers HOW —
specifically, the cross-context decision framework for choosing between
direct application, skill-creator handoff, and new-skill creation.

**Trigger gate (when):** Observations are acted on only in three contexts:

1. **The comprehensive review** — scheduled mode preferred, in-session
   fallback if no scheduled review has run in 7+ days. See
   "## Comprehensive Review (scheduled or fallback)" for the procedure.
2. **Explicit user requests during a task session** — "update X skill",
   "act on observation #N now", "apply this rule to the skill". The user
   is naming the action; the agent executes within the framework below.
3. **In-session correction when a skill is producing wrong output and
   the user should be aware** — surface immediately rather than wait
   for the next review.

Observations are NOT applied during normal task sessions outside these
contexts. Mid-task work produces observations only; those observations
get applied at the next review or by request. The default is log,
don't act.

**Mechanism framework (which):** When acting in any of those contexts,
the rest of this section guides the choice between applying changes
directly to the skill file, handing off to the skill-creator for
substantial restructuring, or creating a new skill from scratch.

### Small Changes

If the improvement is clearly additive, low-risk, and doesn't require testing
to verify it works, it can be applied directly to the skill:

- Adding a new rule or anti-pattern to an existing list
- Clarifying existing wording that proved ambiguous
- Adding a note or edge case to an existing section
- Fixing a factual error

Examples: Adding a new anti-pattern to a skill's anti-patterns list.
Clarifying that inline code comments should be context-aware within their
own document.

After creating or updating any skill file, always present it using `present_files` so the user can review and install it directly from the conversation.

### Substantial Changes (Use Skill-Creator if Available)

If the change could affect the skill's behaviour in ways that need
verification, hand off to the skill-creator if available:

- Restructuring phases or workflows
- Adding new capabilities or sections
- Changing core methodology or decision frameworks
- Any change where "does this actually work better?" is a genuine question

However, match the rigour of the skill creation process to the complexity and
audience. Skill-creator is valuable for open-source skills that need testing,
for skills with complex logic, or when the design isn't yet clear. For internal
skills where requirements are established in conversation, writing directly is
more efficient.

If skill-creator is not available, use the observations as a specification
and make the changes directly — but flag them to the user as substantial
changes that may need manual review.

Examples: Restructuring a skill to make an automated workflow the primary
path instead of a secondary option. Adding an entirely new setup phase to
a skill that previously started with content work.

### Creating New Skills

Use the skill-creator for new skills when available. Provide the
observation(s) as context — they contain the intent, scope, and initial
design thinking needed to get started efficiently. Without skill-creator,
the observations serve as a detailed brief for building the skill manually.

When creating a new skill, determine its type early:

- If it's open-source, strip out any client-specific details and generalise
- If it's internal, include all relevant specifics freely
- If uncertain, default to open-source — strip out specifics and generalise,
  then let the user decide whether any internal details need to be added


## Task-Oriented Sessions — Observation vs Action

Skill development and iteration work happens in multiple environments: in Cowork with persistent storage, in Claude Code with project directories, and in web-based chat without file system access. Cross-environment coordination is essential to prevent regressions — a skill updated in one environment can silently omit content from another if the wrong base file is used.

### Skill file locations — read-only mount vs workspace copy

When working with skills, understand the distinction between the **live file** (the authoritative source) and **workspace copies** (working drafts or staged updates):

1. **The live file is read-only in Cowork.** In Cowork, the live skill file is mounted read-only at `.claude/skills/{skill}/SKILL.md`. You can read it, but you cannot edit it directly — the file system will reject write attempts with `EROFS` (Read-Only File System). This is intentional: it prevents accidental overwrites of the canonical version.

2. **Read from the live file, not cached memory.** Always start skill edits by reading the current live file — not from a workspace copy, a prior draft, or a memory-based reconstruction. This is the only way to guarantee your updates are based on the current canonical content.

3. **Stage edits in the workspace folder.** Write updated versions to `[workspace folder]/skill-updates/[date]/[skill-name]/SKILL.md`. This separation keeps the read-only mount clean and gives you a clear staging area for review before the user replaces the live file.

4. **After staging, present the file for user review.** Always use `present_files` to show the updated skill so the user can review changes and upload directly. Do not attempt to write directly to the mounted skills directory — that will fail with a permission error.

5. **Before overwriting or replacing any existing staged or workspace copy of a skill, diff it against the live file.** If they differ, the workspace copy is stale and your edits must be rebased on the live version — otherwise you risk silently dropping content added by another session. This rule is also codified in CLAUDE.md under "Skill Editing — Always Start From the Live File" as a cross-environment guard. The concrete failure mode: a Claude Code session produced an updated skill that was based on a stale snapshot and silently omitted two substantial sections added to the live skill earlier the same day. The regression was caught only because a pre-merge diff against the mount revealed the missing content.

### Task-session skill updates — stage in the workspace

When a task session produces a skill update (through weekly review, direct improvement, or observation-driven changes), follow this workflow:

1. Read the live file at `.claude/skills/{skill}/SKILL.md`
2. Make all edits to that content
3. Save the complete updated file to `[workspace folder]/skill-updates/[today]/[skill-name]/SKILL.md`
4. Use `present_files` to show it to the user for review
5. The user uploads the file to install it

This keeps the mount clean, stages updates for review, and gives you a clear separation between read-only source and working copy.

**Cross-environment note:** Claude Code now shares the same skills as Cowork via the anthropic-skills capability. The "always start from the live file" rule applies in both environments. In Claude Code, the live file is surfaced by the capabilities system; in Cowork, it's the read-only mount at `.claude/skills/{skill}/SKILL.md`. The diff-before-overwrite requirement applies regardless of which environment produced the update.

---
---

## Principle Propagation

When an observation reveals a general principle — something that applies not
just to the skill being improved but to skills in general — it should be
propagated across the skill library, not just applied to the one skill that
triggered it.

### The Cross-Cutting Principles File

Cross-cutting principles are tracked in a persistent file alongside the
observation log:

```
[workspace folder]/skill-observations/cross-cutting-principles.md
```

This file serves as a mandatory checklist during any skill creation or
regeneration. Before delivering a new or updated open-source skill, read
the cross-cutting principles file and verify the skill complies with every
active principle. This is what turns general principles from good intentions
into enforced standards.

### How It Works

1. During a skill update, an observation reveals a principle that applies
   broadly — not just to the skill being worked on
2. Log it as an observation with `Skill: All skills` and surface it to the
   user
3. If the user approves it as a cross-cutting principle, add it to the
   cross-cutting principles file
4. From that point forward, every skill creation or regeneration includes
   a compliance check against the full list of active principles

### Propagation Timing

The user decides when and how to propagate each principle:

- **Immediate propagation** — for principles important enough to warrant
  updating all existing skills right away (e.g., a confidentiality rule)
- **Opportunistic propagation** — for principles that can be applied the
  next time each skill is updated or regenerated (e.g., adding a licence
  statement)

### Cross-Cutting Principles File Structure

```markdown
# Cross-Cutting Principles

Principles that apply to all skills. This file is read as a mandatory
checklist during any skill creation or regeneration.

---

## Active Principles

### 1. [Principle title]
**Added:** [date]
**Applies to:** [all skills | all open-source skills | all skills with rules]
**Requirement:** [what the principle requires]
**Propagation:** [immediate | opportunistic]
**Status:** [active]
```

---

## Comprehensive Review (scheduled or fallback)

The comprehensive review cross-checks all open observations against all
skills, propagates cross-cutting principles to skills that don't yet
comply, and applies the improvements that don't need user input. There
are two ways it runs.

**Preferred mode — scheduled autonomous review.** A user-defined recurring
task (typical cadence: Monday/Wednesday/Friday mornings) registered with
the agent's scheduling system. This is preferred because it picks up open
observations on a regular cadence without depending on the user being
mid-session at exactly the right moment, and because the user is not
present, the review applies the non-escalated observations autonomously.

**Fallback mode — in-session 7-day trigger.** If no scheduled review is
registered (or none has run successfully in the last 7 days), a
comprehensive review fires automatically at the start of the next
task-oriented session. The fallback is a safety net for users who haven't
set up scheduled reviews — either because the environment doesn't support
scheduling or because they haven't done it yet.

### Trigger Mechanism

**Scheduled mode** runs via the user's chosen scheduling tool — no in-skill
trigger required.

**Fallback mode** is triggered by step 3 of the Session Start Protocol
(see Observation Log Management). The fallback fires when both of the
following are true:

- No scheduled review task is registered, OR the most recent successful
  scheduled review was more than 7 days ago.
- The in-session timestamp at
  `[workspace folder]/skill-observations/last-review-date.txt` is also
  more than 7 days old (or missing).

When the fallback fires, inform the user that the comprehensive review is
running and walk through Step 0 (recommend scheduling) before Step 1.

### Interactive vs Scheduled Runs — Approval Policy

The approval behaviour depends on who is present:

**Interactive sessions (user present):** Always ask the user before applying
or declining observations. Present observations grouped by skill with a one-
sentence summary each, and wait for explicit approval (blanket "apply all" or
selective). This preserves the collaborative feel and lets the user catch
observations they disagree with before any staging occurs.

**Scheduled autonomous runs (user not present):** Apply observations
autonomously by default. The safety net is the staging-plus-upload pattern:
updates go to `skill-updates/YYYY-MM-DD/{skill-name}/SKILL.md` and only
become live when the user explicitly uploads them. Nothing can silently
break because nothing is live until the user approves upload.

**Escalate without applying (report only) when any of these apply:**

1. **New skill creation.** Naming, scope, type (open-source vs internal),
   and licence are decisions that benefit from user input. Note the
   candidate in the report; don't create the skill.
2. **Removing or substantially restructuring existing content.** Any edit
   that deletes a section, replaces it with something smaller, or reshapes
   core methodology risks dropping institutional memory. Flag and report.
3. **An observation that flags its own uncertainty.** Phrases like "not
   sure if...", "this might be...", "worth discussing..." in the
   Suggested Improvement field are the observation asking for user input.
   Respect that.
4. **Conflicting observations.** Two observations that point in opposite
   directions, or where the integration path isn't obvious, should be
   surfaced rather than resolved autonomously.

Scheduled runs that escalate should still apply every non-escalated
observation before producing the report. A scheduled review that
produces 0 applied updates is functionally a report generator, which
wastes the scheduling.

### Review Steps

**Step 0 — Recommend scheduled review setup**

Before running the in-session fallback, check whether scheduled autonomous
reviews are set up. If not, surface a recommendation to the user — but
respect prior declines.

1. Check for the suppression marker at
   `[workspace folder]/skill-observations/scheduled-review-decline.txt`.
   If it exists and was last updated less than 30 days ago, AND the
   in-session fallback has not fired multiple times in that window, skip
   the recommendation. Proceed to Step 1.

2. Check whether a scheduled review task is registered. The signal is
   either a presence check via the platform's scheduling tool (preferred)
   or the existence of
   `[workspace folder]/skill-observations/scheduler-registered.txt`. If a
   registered scheduled review is found, no recommendation needed — skip
   to Step 1.

3. If no scheduled review is registered AND no recent decline marker
   exists (or the marker is stale because the fallback keeps firing),
   make an active recommendation:

   > "I notice you don't have a recurring skill review scheduled. The
   > task-observer recommends running this review on a cadence — e.g.,
   > Monday/Wednesday/Friday mornings — so it doesn't depend on you
   > being mid-session at the right moment. Want help setting one up?"

   - **If the user says yes:** walk through registering a scheduled task
     using the platform's scheduling capability. In Cowork, invoke the
     `create-shortcut` skill and its `set_scheduled_task` tool. In
     terminal-based environments, use cron or an equivalent scheduler.
     Use task name `weekly-skill-review` (or similar) and a sensible
     default cadence; let the user pick the day(s) and time. Once
     registered, read the draft task description at
     `[workspace folder]/skill-observations/scheduled-task-draft.md` and
     pass it as the task prompt. On success, write today's date to
     `[workspace folder]/skill-observations/scheduler-registered.txt`.
   - **If the user says no or defers:** write today's date to
     `[workspace folder]/skill-observations/scheduled-review-decline.txt`
     to suppress the recommendation for 30 days. Proceed to Step 1 and
     run the in-session fallback.

4. If no scheduling capability is available in the current environment,
   skip the recommendation silently and proceed to Step 1. Do not surface
   the recommendation in environments where the user couldn't act on it.

The 30-day suppression isn't permanent. If the in-session fallback keeps
firing within the suppression window — a signal that the recurring need
is real and the one-time decline was situational — the recommendation
re-surfaces on the next firing.

**Step 1 — Load observations and principles**

Read the observation log at `[workspace folder]/skill-observations/log.md`.
Extract all observations with status OPEN. Also read
`[workspace folder]/skill-observations/cross-cutting-principles.md` and
extract all active principles.

If there are no OPEN observations and all principles are already propagated,
skip the review, update the timestamp, and proceed with the session. Inform
the user briefly: "Weekly skill review: no open observations or outstanding
principles. All skills are current."

**Step 2 — Inventory all skills**

Use `<available_skills>` from the system prompt to identify all skills. In
environments where this tag is not present, use the skills directory or
equivalent listing mechanism to discover available skills.

For each skill, read its SKILL.md file at the location provided. Exclude
built-in platform skills from being updated — only update custom skills
created by the user.

**Known system skills (read-only, cannot be replaced by the user):**
docx, pdf, xlsx, pptx, skill-creator, schedule. This list may grow as the
platform evolves — if a skill update fails because the user cannot overwrite
the file, add it to this list.

**Custom skills** (owned by the user, can be replaced) are everything else
in the skills directory that isn't on the system list above.

**Step 3 — Cross-check observations against every skill**

For each OPEN observation, evaluate whether it is relevant to each skill. Do
NOT rely solely on the observation's own "Skill" field — observations may
contain general principles that apply more broadly than the original context
suggested. Consider both the specific "Suggested improvement" and the general
"Principle" fields. Build a mapping of skill → [relevant observations].

**If the review is interactive (user present):** Present ALL observations to the user in a single message, grouped by skill. For each observation, show the number, title, and a one-sentence summary. Flag any observations that are ambiguous, risky, or require a judgment call as 'Needs your input'. All other observations are treated as straightforward and can be applied without individual discussion.

**If the review is scheduled autonomous (user not present):** Skip the user-facing present step. Apply the approval policy from "Interactive vs Scheduled Runs" above: apply every non-escalated observation and record the escalated ones (new-skill candidates, removal/restructuring, self-flagged uncertainty, conflicting observations) in the review report without applying them. Proceed directly to Step 4.

**Step 4 — Cross-check cross-cutting principles against every skill**

For each active cross-cutting principle, check whether each skill already
complies. Flag any skills that do not yet implement the principle.

**Step 5 — Apply updates**

In interactive runs, wait for user confirmation (blanket "apply all" or selective approval) before creating updates. In scheduled autonomous runs, proceed directly to applying all non-escalated observations. For each skill that has relevant observations or non-compliant principles, create an updated version of its SKILL.md. When editing:

- Integrate the insight into the appropriate section of the skill (don't just
  append a list of observations at the bottom)
- Preserve the skill's existing structure, voice, and author attribution
- Make the improvement feel native to the skill, not bolted on
- If an observation suggests a new phase, step, anti-pattern, or checklist
  item, place it where it logically belongs

**Routing observations that target system skills:** When an observation
targets a system skill (see the known system skills list in Step 2), do NOT
skip it. Instead, route the improvement to a **complementary skill** — a
user-owned skill named `{system-skill}-extras` (e.g., `docx-extras`) that
layers additional guidance on top of the system skill. If the complementary
skill doesn't exist yet, create it. The complementary skill should:
- State which system skill it extends
- Contain only the delta — the additional rules, anti-patterns, or guidance
  not present in the system skill
- Be loaded alongside the system skill (add a note to CLAUDE.md or
  equivalent configuration if needed)

This ensures observations targeting system skills are still actionable,
even though the system skill files themselves cannot be modified.

**Important:** Do not edit skill files in place. Save updated versions to the
workspace folder for user review and manual replacement (see Delivering
Updated Skills below).

**Step 6 — Mark observations as ACTIONED**

After successfully creating an updated skill based on an observation, update
that observation's status in `log.md` from OPEN to ACTIONED. Add a brief note
about which skill(s) were updated, e.g.:

`ACTIONED — Applied to [skill-name] (weekly review [date])`

Note: the standard archival-on-write mechanism (see "Archival on Write" in
the Observation Protocol) will automatically archive these newly-resolved
entries on the next log write. No separate archival step is needed here.

**Step 7 — Update timestamp**

Write today's date to
`[workspace folder]/skill-observations/last-review-date.txt`.

**Step 8 — Present summary and user action items**

Present each updated skill file using `present_files`, then show the user a summary following the format in Delivering Updated Skills above. The user can install updated skills directly from the conversation using the upload button on each presented file.

### Constraints

- Do not modify observation entries beyond their status field
- Do not create new skills — only update existing ones. If an observation
  suggests a new skill, note it in the summary for the user to action
  separately via the skill-creator
- If an observation seems relevant but you're unsure how to integrate it,
  skip it and note the uncertainty in the summary
- Treat observations marked "internal" with the same rigour as "open-source"

---

## Delivering Updated Skills to the User

When the weekly review (or any other process) produces updated skill files,
they are delivered to the user through the conversation using `present_files`.
Cowork's UI includes an upload button on presented skill files that allows
the user to install them directly into their capabilities — no manual file
copying needed.

### Delivery Process

1. Save each updated SKILL.md to the workspace folder for record-keeping:

   ```
   [workspace folder]/skill-updates/[date]/[skill-name]/SKILL.md
   ```

2. Present each updated skill file using `present_files` so the user can
   review it inline and install it directly via the upload button.

3. Present the user with a summary using this format:

   ```
   ## Weekly Skill Review Complete — [date]

   The following skills have been updated based on [N] open observations
   and [N] cross-cutting principles.

   ### Updated Skills

   **[skill-name]**
   - Changes: [1-sentence summary of what changed]
   - Observations applied: #[N], #[N]

   [repeat for each updated skill]

   ### Observations Actioned
   [list of observation numbers and titles marked ACTIONED]

   ### Skipped (needs manual review)
   [any observations that couldn't be applied, with reasons]
   ```

### Keep-Two Rule

The `skill-updates/` directory uses a rolling retention policy: for any
given skill, keep only the two most recent date directories. When a skill
appears in more than two date directories, delete the oldest copies. This
prevents the workspace from accumulating stale update history while still
keeping a short rollback window.

3. Do not proceed with other work until the user has acknowledged the
   summary. The user does not need to replace the files immediately, but
   they should be aware of what's pending.

---

## Observation Log Management

### Location

The observation log persists between sessions in the user's workspace folder.
Create the log file on first use if it doesn't exist. Default path:

```
[workspace folder]/skill-observations/log.md
```

### Log Structure

```markdown
# Skill Observation Log

Observations captured during task-oriented work. Each entry identifies a
potential skill improvement or new skill opportunity.

**Status key:** OPEN = not yet actioned | ACTIONED = skill updated/created |
DECLINED = user decided not to pursue

---

## [Date or Session Identifier]

### Observation 1: [Title]
**Status:** OPEN
[... full observation format ...]

### Observation 2: [Title]
**Status:** ACTIONED — Applied to [skill-name], rule 35
[... full observation format ...]
```

### Session Start Protocol

This is the single entry point for all session-start checks. Run through
these steps at the start of each task-oriented session:

1. **Check whether files exist.** If the observation log or cross-cutting
   principles file don't exist yet, this is a first-time setup — create
   them using the templates in the Log Structure section (below in this
   document) and the Cross-Cutting Principles File Structure section (under
   Principle Propagation). If the files already exist, proceed to step 2.

2. **Scan for relevant context.** Read any OPEN observations and active
   cross-cutting principles. Don't surface them unprompted unless they're
   directly relevant to the current task — just hold them in awareness.

3. **Check the weekly review trigger.** Read the timestamp in
   `[workspace folder]/skill-observations/last-review-date.txt`. If the
   file doesn't exist or the date is more than 7 days ago, trigger the
   Weekly Comprehensive Review (described in full under its own section)
   before proceeding with the user's task. If fewer than 7 days have
   passed, proceed normally.

4. **Check the configuration file.** Run the config detection described in
   Detecting the Configuration File (under Recommended Activation Setup).
   This runs once per session.

### Keeping the Log Clean

Archival is event-driven and runs on every log write. Before appending new
observations or updating statuses, entries that were already marked ACTIONED
or DECLINED in a previous update are moved to a timestamped archive file
(see "Archival on Write" in the Observation Protocol). This keeps the active
log focused on OPEN items and recently-resolved entries, while the archive
provides the complete historical record.

---

## Environment Compatibility

The observation methodology works in any environment where the agent can interact
with users during task-oriented work. The persistence mechanism is what varies.

### With Persistent Storage

In environments with file system access (desktop tools with workspace folders,
terminal-based tools with project directories, or similar), the full workflow
applies as described: observations are logged to a persistent file, the cross-
cutting principles file is read during skill regeneration, and the log carries
over between sessions automatically.

### Without Persistent Storage

In environments without file system access (web-based chat interfaces or
similar), the skill still works — the observation methodology is environment-
independent. The difference is that persistence becomes the user's
responsibility, and the skill shifts into **handoff doc mode** to support
this.

**How handoff doc mode works:**

- Observations are captured within the conversation and surfaced before the
  session ends, as usual
- Instead of writing to a log file, observations are collected in-session
  and presented in a structured **handoff document** before the session ends
- The handoff doc includes: all observations in full format, any decisions
  made during the session, action items and next steps, and any working
  artifacts (drafts, analyses) that need to survive into the next session
- The user copies this document to their own storage (notes app, file system,
  etc.) and pastes it into the next session to restore context
- Cross-cutting principles should be included in the handoff doc so the user
  can provide them when starting a new session

**Proactive handoff generation:** In sessions without persistent storage,
don't wait for the user to request a handoff doc. When the conversation
starts to wind down — the user is summarising, saying "that's it for now,"
or the substance is wrapping up — proactively offer to generate one. A
premature offer is a minor interruption; a missing one is lost work.

**Handoff doc format:**

```markdown
# Session Handoff: [Session Topic]

**Date:** [date]
**Context:** [what was worked on and what the next session needs to know]

## Decisions Made
[numbered list of decisions]

## Observations Logged
[full observation entries in standard format]

## Cross-Cutting Principles (current)
[any principles that were active or newly added]

## Action Items
[what needs to happen next, with enough context to resume]

## Working Artifacts
[any drafts, analyses, or intermediate work products in full]
```

This is less seamless than the persistent-storage workflow, but the core value
— systematically capturing insights that would otherwise be lost — is
preserved. The observation format and surfacing protocol are identical in both
environments.

---

## Quick Reference

| Question | Answer |
|----------|--------|
| When do I observe? | Throughout the full task session, including post-task feedback and reflective conversations |
| How do I log? | Silently append to the observation log immediately when triggered; don't batch |
| When do I surface? | End of session, or earlier if needed |
| How do I activate reliably? | Add a config-level instruction (see Recommended Activation Setup) |
| Open-source or internal? | Default to open-source when possible |
| Licence for open-source? | CC BY 4.0 recommended |
| Small fix or skill-creator? | Needs testing → skill-creator (if available). For internal skills with established requirements, writing directly is efficient. Clearly additive → apply directly |
| What format? | Issue → Suggested improvement → Principle |
| Author attribution? | Required for open-source skills; use the template |
| Cross-cutting principle? | Add to principles file, enforce during regeneration |
| Confidentiality check? | Four layers: observation, pre-creation, post-draft, structural |
| No persistent storage? | Handoff doc mode — observations surfaced in a structured doc at session end |
| Scheduler automation? | Step 0 of weekly review auto-checks; silent until tool is available |
| Observation numbering? | Mandatory pre-logging search ensures no collisions; never use cached numbers |
| Log archival? | Event-driven — resolved entries are archived on the next log write |
| Simplification signals? | Watch for one-off rules, never-used sections, elaborate workflows users skip, and contradictions |
| Handoff doc analysis? | Systematically extract implied observations from action items, open questions, and narrative sections |
