---
name: doc-coauthoring
description: Use when asked to write, draft, create, or substantially revise a document, implementation plan, proposal, PRD, or technical specification, including changed requirements or review feedback. Supports autonomous drafting and guided coauthoring.
---

# Author a document

Produce a document its intended reader can use without the authoring conversation.
Preserve the user's requested format, scope, and meaning of completion. For a small
copyedit, make the requested edit directly. A research-only request stays research;
it does not require an implementation plan.

## Select the authoring owner

Complete this lookup as a separate tool phase. Its reads determine which workflow
references are valid, so wait for their results before scheduling reference reads.

1. Read the applicable repository instructions, such as `AGENTS.md` or `CLAUDE.md`,
   and any policy files they name. Use instructions already supplied in context;
   otherwise locate and read them now. Independent task context may be read during
   this lookup; workflow references wait until it is complete.
2. Find an explicit declaration directing authoring to a repo-relative `SKILL.md`.
   A mention in task evidence is not a declaration. Resolve the declared path
   from the repo root and follow the client's instruction precedence. Conflicting
   declarations without a precedence rule are a dependency problem: report them
   and leave authoring pending.
3. Read the declared `SKILL.md` and wait for the complete result. A failed read ends
   the lookup: report the declared path and leave authoring pending. When readable,
   continue from that copy. If it is this file, continue here without reinvoking
   it. With no declaration, continue from this copy after checking the repository
   instructions. Folder names are unrestricted.

This phase is complete when the selected file's absolute path is known and its
instructions have been read. Then follow workflow links only from the selected
copy. Resolve each link relative to the file containing it, including links reached
later, and pass the resulting absolute path to the reading tool.

## 1. Recover intent

Read the supplied context and existing documents. Scope every content search,
including searches that return only matching filenames, to project-owned paths
using explicit paths or exclusion globs. Keep copied skills' `evals/` trees out
of those searches and context reads: they contain test inputs and expected answers.
Use filename globs to discover paths before selecting content to read.
Find the existing document and its owner before creating a sibling. Search the
local index and relevant topic paths; inspect supplied branches or PRs when they
suggest parallel work. Distinguish editable, generated, and externally managed
content. Use the owning system's workflow for managed documents and preserve
unrelated user edits.

Finish when the audience, requested outcome, requirements, exclusions, and editing
home are known, or a specific inaccessible input is recorded. For guided drafting,
read [interactive drafting](references/interactive-drafting.md) before proceeding.
For pinning or upgrading this folder, read [adoption](references/adoption.md).

## 2. Establish consequential facts

Inspect the definitions, consumers, configuration, and existing checks behind the
proposal. Use history when evidence conflicts or the reason for a choice matters.
Cite the sources supporting claims that could change the design. Keep observed
facts, assumptions, chosen approaches, and unresolved decisions distinguishable.

Research discoverable facts with available authorized tools. Ask about judgment
or unavailable intent, and continue independent work while waiting when possible.
Use optional research capabilities when the task warrants a separate investigation;
this workflow must also finish with ordinary reading and research tools alone.

Finish when each consequential premise has a source or a named uncertainty with
its effect on the proposal. An inaccessible source limits the claim; it does not
make the claim true.

## 3. Outline and decide

Choose a provisional structure for the audience. Start a design with the problem
and desired result, then explain the mechanism and material alternatives. A long
investigation can save an outline early. Use the requested format and omit empty
sections.

For documents directing implementation, including PRDs with implementation
commitments, read [implementation plans](references/implementation-plans.md).
Finish when every requested outcome has a place and every implementation-blocking
choice is resolved or explicitly open. Resolve ordinary choices within the grant;
expose material unknowns instead of inventing answers.

## 4. Draft or revise

Write in the chosen home. Integrate new answers and evidence into the affected
sections. A substantive revision changes what a later reader would do. Preserve
valid user edits, including edits made directly during collaboration.

Keep the body evergreen: it reads as written today by someone who knows only the
current decisions. Justify each choice against its live alternatives. What
changed, when, and who asked belongs in the progress record or the commit
message. Give each fact one home and link to it from elsewhere.

Before every substantive revision, and before the first edit after a context
compaction, reread the whole document from disk and trace the change through
requirements, design, dependencies, acceptance, open decisions, and examples.
When the revision changes a decision, scope, or structure, rewrite each affected
section whole.

Use the repo's existing lifecycle owner for metadata, indexes, progress state, and
retirement. Its schema remains local. Optional prose guidance can improve the
writing; no sibling skill or publisher checkout is required to finish.

Finish when the affected sections agree, requested requirements remain represented,
remaining work is explicit, and no sentence in the body depends on a superseded
decision or refers to an earlier draft.

## 5. Test the reader and hand off

Give an isolated reader the document and realistic audience questions without the
authoring chat. Use a fresh agent when available and permitted. Otherwise perform
a separate reread and label it self-review. A user-run fresh-reader test is an
option, not a required stop. Use the plan-specific questions in the planning
reference when applicable.

Ask what the document enables, what to do next, and what context or decision is
missing. Ask equally what is stale, stated twice, cuttable, or narrating its own
history. Run the reader after any revision that changes a decision, after every
third substantive revision, and before handoff. Integrate findings by
restructuring the affected sections; a caveat appended beside the old text keeps
both versions alive. Repeat the affected questions.

Before handoff, read the whole document as someone with no context or history and
rewrite whatever leans on the conversation: an evergreen body with the baggage
dropped. Use the `writing-for-humans` skill for the prose when it is available.
Check links and applicable repo document rules. Finish when requirements are
covered, consequential claims are supported or qualified, each fact has one home,
and the reader can identify the result and next action. Report unresolved
decisions and missing verification with the artifact.
