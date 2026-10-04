---
name: skill-system-architect
description: >
  Design the architecture for a multi-command skill system — the shared state schema, the
  command map, the router, and the boundary each command stops at — before any skill files
  get written. Use when the user wants to turn one skill into a system, combine several
  related or overlapping skills into a single coherent one, build a skill with subcommands
  (like `/thing audit`, `/thing polish`), design a suite, family, or collection of skills,
  or asks "how should I structure this skill set". Also trigger on "skill system", "skill
  architecture", "multi-command skill", "system of skills", "make these skills work
  together", "skill with slash commands", or complaints that their skills overlap, collide,
  duplicate each other, or never fire. Produces an architecture spec only — it never writes
  SKILL.md or reference files. Hand the finished spec to skill-creator to build from.
---

# Skill System Architect

Design the shape of a multi-command skill system and return a written architecture spec. This skill decides **what the system is**; `skill-creator` builds it.

**Writes:** one architecture spec (markdown), delivered to the user.
**Never writes:** `SKILL.md`, reference files, scripts, or any file inside a skill directory.
**Stops at:** the spec. Handing off is the last step, not an optional one.

---

## Doctrine

> **Design the state schema first. Commands are just things that read and write it.**

A collection of skills sharing a name prefix is not a system. It is a folder of prompts with a naming convention. What makes commands compose is a **shared artifact** they all agree on: one command writes it, another reads it, and the second is more useful because the first ran.

This is the load-bearing idea in this skill. Everything else follows from it:

- If a shared artifact exists, the command map almost derives itself — commands are the transitions on that artifact.
- If no shared artifact exists, there is no system to design, and saying so is the correct output.

The **prefix test**: if you renamed every proposed command to a standalone skill with an unrelated name, would anything actually break? If nothing breaks, they were never a system.

---

## Workflow

### Phase 0 — Establish what you're working from

Three entry paths. Identify which one before asking anything else:

- **Greenfield** — a domain with no skills yet. Go to Phase 1.
- **Consolidate** — several existing skills that overlap or should work together. Load [references/inventory.md](references/inventory.md) first, then Phase 1.
- **Expand** — one existing skill that should grow subcommands. Read that skill's `SKILL.md` in full before Phase 1; its current workflow is a strong candidate for the system's default command, and its `description` is the starting trigger surface.

For Consolidate and Expand, also enumerate the user's **other installed skills**. Trigger collisions are the most common failure of a new system and the cheapest to catch now.

### Phase 1 — Domain interview

Use the structured question tool when available; otherwise ask and stop.

**Cadence:** two or three questions per round, then wait. One round is the default; add a second only when the answers expose a material gap. Never dump a questionnaire. Assert the likely reading and invite correction rather than turning obvious facts into menus.

Ask only what changes the architecture. The four that usually do:

1. **What recurring jobs live in this domain?** Not "what should the skill do" — what does the user find themselves doing over and over, in what order?
2. **What persists between sessions?** What would you want to still be true next week? This is the state question in disguise, and asking it early prevents naming commands too soon.
3. **What would one job need to know that another job already figured out?** The answer is the shared artifact.
4. **Where does this stop?** What neighboring work must the system refuse to do, and which existing skill owns it?

Do not ask for command names. Names are Phase 3, and asking early anchors the whole design on whatever the user says first.

### Phase 2 — The state gate

**This phase is a gate. Do not proceed past it without a shared artifact.**

Load [references/state-schema.md](references/state-schema.md) and design the schema before naming a single command.

Apply the gate test from that file. If the domain has no shared artifact:

- Say so plainly and name what's missing.
- Do not invent state to justify the system. A registry nothing reads is worse than no registry.
- Offer the honest alternatives: keep them as separate skills with sharpened non-overlapping descriptions; or reconsider the scope, since the real system may be one level up or one level down from where the user is looking.
- Stop there. A refusal with a reason is a successful outcome of this skill.

### Phase 3 — Command map

Load [references/command-design.md](references/command-design.md).

Derive commands from the state, not from brainstorming. Every command gets five fields, and any command missing one of them is not ready:

| Field | Rule |
|---|---|
| **Verb** | One word if possible. It's what the user types. |
| **Category** | Groups the table and the no-argument menu. 3–6 categories max. |
| **Reads** | Exact state paths, or "nothing". |
| **Writes** | Exact state paths, or "nothing". |
| **Stops at** | The boundary it must never cross. |

A command that reads nothing and writes nothing is a standalone skill wearing the system's badge. Either connect it to the state or leave it out.

### Phase 4 — Router design

Load [references/router-anatomy.md](references/router-anatomy.md).

Produce the frontmatter, the commands table, the four routing cases, and the split between doctrine that lives in the router and procedure that lives in a reference file.

**Establish the target first — account skill or Claude Code plugin skill.** The two use different frontmatter dialects and the account one is a strict allow-list; the wrong choice fails at packaging. `references/router-anatomy.md` has both.

Check the `description` against the user's other installed skills for collisions before finalizing.

### Phase 5 — Emit the spec

The deliverable, in this order:

1. **System summary** — one paragraph: the domain, the shared artifact, and what composing looks like in one concrete example ("X writes the audit, Y reads it as its backlog").
2. **Directory layout** — the full tree, including where state lives.
3. **State schema** — files, formats, field-level definitions, closed enums, ID rules, write rules.
4. **Command map** — the five-field table, one row per command.
5. **Router** — the complete `SKILL.md` frontmatter and section skeleton, ready to paste. Commands table filled in; playbooks left as stubs.
6. **Command file stubs** — for each command, the five-part header (contract line, reads, writes, stops at, phase names). Headers only. Not the playbooks.
7. **Build order** — which command to write first and why. Usually whichever one *writes* the state before anything can read it.
8. **Open decisions** — what was deliberately left undecided, and what it would cost to change later. Anything cheap to defer belongs here rather than being guessed.

### Phase 6 — Handoff

End with the explicit handoff: this spec goes to `skill-creator`, which writes `SKILL.md` and the reference files from it. Name the first file to build.

---

## Calibration

Match the design to what's actually being built.

- **Small system (2–4 commands):** state may be a single file. Skip categories in the commands table. The spec can be two pages.
- **Large system (8+ commands):** state needs a registry plus per-entity records. Categories are required or the no-argument menu becomes unusable. Consider whether a shared-procedure reference file (loaded by several commands) earns its place.

More commands is not better. Two commands that compose beat six that don't.

---

## Anti-patterns

- **Naming commands before designing state.** Produces a menu that looks like a system and behaves like a folder. The command names will survive the whole design process unchallenged because they arrived first.
- **Inventing state to pass the gate.** A schema no command reads is decoration. If the gate fails, report the failure.
- **Doctrine bloat in the router.** Everything "every command needs" gets stuffed into `SKILL.md` until the router costs more than the playbooks. Test: is it a belief the whole system holds, or a procedure two commands share? Beliefs stay in the router; shared procedure becomes its own reference file that both commands load.
- **Over-splitting.** If two proposed commands read the same state, write the same state, and stop at the same boundary, they are one command with a parameter. Intensity variants ("more", "less", "harder") only earn separate commands when each has a genuinely different playbook.
- **Under-splitting.** A single command whose playbook contains "if the user wants X do this, if they want Y do that" is two commands that haven't been separated yet.
- **Ignoring the trigger surface.** A command that isn't represented in the `description` works when typed explicitly and never fires otherwise. Every command contributes verbs.
- **Designing the scripts.** Whether a system needs helper scripts is discovered after commands start hand-editing state and getting it wrong. Note it as an open decision; don't specify a CLI up front.

---

## Confirm and stop

Present the spec for confirmation or one correction round, then stop. This skill never writes skill files, never creates directories inside a skill, and never begins implementation — even when the user's next message sounds like approval to build. Approval to build is approval to hand off.
