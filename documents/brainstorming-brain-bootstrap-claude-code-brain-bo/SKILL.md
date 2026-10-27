---
name: brainstorming
description: Use before any new feature, component, or behavioral change — when you need to explore requirements and design before writing code
user-invocable: true
disable-model-invocation: true
---

# Brainstorming Ideas Into Designs

Turn ideas into fully formed designs and specs through collaborative dialogue. Understand the idea first, explore approaches, present a design, get approval — then plan.

<HARD-GATE>
Do NOT write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it. This applies to EVERY request regardless of perceived simplicity.
</HARD-GATE>

## Anti-Pattern: "This Is Too Simple To Need A Design"

Every feature goes through this process. A todo list, a single-function utility, a config change — all of them. "Simple" projects are where unexamined assumptions cause the most wasted work. The design can be short (a few sentences for truly simple requests), but you MUST present it and get approval.

## Checklist

Complete in order:

1. **Explore project context** — check files, docs, recent commits
2. **Ask clarifying questions** — one at a time: purpose, constraints, success criteria
3. **Propose 2-3 approaches** — with trade-offs and your recommendation
4. **Present design** — in sections scaled to complexity, get user approval after each section
5. **Write design doc** — save to `claude/tasks/specs/YYYY-MM-DD-<topic>-design.md` and commit
6. **Spec self-review** — check for placeholders, contradictions, ambiguity (fix inline)
7. **User reviews written spec** — ask user to review before proceeding
8. **Transition to implementation** — run `/plan` command to create implementation plan

## The Process

**Understanding the idea:**

- Check the current project state first (files, docs, recent commits)
- Before asking detailed questions, assess scope: if the request describes multiple independent subsystems, flag this immediately and help decompose into sub-projects first
- Ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible
- Only one question per message — break complex topics into multiple questions
- Focus on: purpose, constraints, success criteria

**Exploring approaches:**

- Propose 2-3 different approaches with trade-offs
- Lead with your recommended option and explain why

**Presenting the design:**

- Scale each section to its complexity: a few sentences if straightforward, up to 200-300 words if nuanced
- Ask after each section whether it looks right
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify

**Design for isolation and clarity:**

- Break the system into smaller units with one clear purpose each
- For each unit: what does it do, how do you use it, what does it depend on?
- Can someone understand a unit without reading its internals? Can you change internals without breaking consumers? If not, boundaries need work.

**Working in existing codebases:**

- Explore the current structure before proposing changes — follow existing patterns
- Include targeted improvements that serve the current goal; don't propose unrelated refactoring

## After the Design

**Documentation:**

- Write the validated design to `claude/tasks/specs/YYYY-MM-DD-<topic>-design.md`
- Commit the design document to git

**Spec Self-Review:**

1. **Placeholder scan:** Any "TBD", "TODO", incomplete sections? Fix them.
2. **Internal consistency:** Do sections contradict each other?
3. **Scope check:** Focused enough for a single implementation plan?
4. **Ambiguity check:** Can any requirement be interpreted two ways? Pick one and make it explicit.

Fix issues inline. No need to re-review — just fix and move on.

**User Review Gate:**

> "Spec written and committed to `claude/tasks/specs/<filename>`. Please review it and let me know if you want any changes before I write the implementation plan."

Wait for user response. If changes requested, update spec and re-run self-review. Only proceed once approved.

**Implementation:**

- Run `/plan` to create a detailed implementation plan
- Do NOT write code yet — `/plan` is the next step

## Key Principles

- **One question at a time** — don't overwhelm
- **YAGNI ruthlessly** — remove unnecessary features from all designs
- **Explore alternatives** — always propose 2-3 approaches
- **Incremental validation** — present design, get approval before moving on
