---
name: thalarch-skill-intelligence
description: >
  Autonomous skill-selection layer for Thalarch. Use at the start of non-trivial work and again
  after project discovery when the current host may expose stronger project-local, official
  platform, Thalarch, or third-party expertise. Shortlists the smallest high-value skill stack
  based on task fit, project/toolchain compatibility, authority/currentness, tool leverage,
  evidence needs, redundancy, conflicts, context cost, and actual host availability.
---

# Thalarch Skill Intelligence

Use the **current host's real skill/capability inventory** as a capability catalog instead of
requiring the user to name every useful specialist manually.

The goal is **best-fit expertise, not maximum skill count**.

Do not assume Antigravity, Codex, Claude Code, or any other host exposes identical skill APIs,
agent names, tools, or discovery paths. Inspect what this session actually makes available.

## 1. Automatic discovery pass

For every non-trivial task, before deep exploration or mutation:

1. inspect skill names/descriptions/metadata exposed by the current host when available;
2. inspect applicable project-local skills and repository rules through host-supported locations;
3. infer the task phase, language/runtime, framework/platform, risk, and evidence needs;
4. shortlist only skills whose descriptions materially match one of those dimensions;
5. read full instructions only for shortlisted candidates;
6. confirm any specialist agent/tool named by a skill actually exists on this host before relying on it;
7. choose the smallest compatible stack that covers the task.

Do not wait for the user to say “use skill X” when a clearly relevant installed skill already
exists.

Do not read every installed `SKILL.md` merely because it is available. Discovery metadata exists to
avoid context pollution.

When the inventory contains candidate skills from known high-value ecosystems, consult
`references/known-high-value-sources.md` only as a tie-breaking/source-quality aid. It is not a
reason to activate a skill that does not fit the task.

## 2. Capability-before-name rule

A role described by Thalarch is not proof that a host-specific named agent or tool exists.

Before delegating or invoking:

- confirm the current host exposes that exact agent/tool/capability;
- if the exact named specialist is unavailable, load the relevant canonical Thalarch skill into a
  compatible host-native agent/context instead;
- if no compatible capability exists, perform the strongest safe fallback in the current context;
- if a required proof depends on a missing browser/device/image/runtime capability, keep that claim
  `UNVERIFIED` rather than fabricating execution.

Never invent an agent, skill, tool, MCP server, browser integration, image generator, or command
because another Thalarch host has one.

## 3. Re-route after evidence

Initial routing is provisional.

After repository preflight reveals the actual stack, versions, framework, runtime, or problem
mechanism, repeat selection when that evidence could change the best skill set.

Examples:

- generic Kotlin becomes Kotlin + a precise JetBrains/official Android/Kotlin skill after build and
  import evidence proves its exact scope;
- generic Java becomes Java + concurrency/JPA/Maven specialization only when those surfaces exist;
- generic frontend becomes framework-specific + an actually available browser/design capability
  after the package graph and visual brief are known;
- generic Python becomes Python + API/data/framework skills only after those dependencies are proven;
- a suspected performance issue may drop the performance skill if root-cause evidence shows the
  problem is actually correctness/configuration.

Skills may be removed as well as added.

## 4. Selection priority

Evaluate candidates in this order of authority, while still requiring task fit:

1. **Explicit user constraints and repository rules** — these are not optional skill suggestions.
2. **Project/workspace-local skill** with direct knowledge of the current repository/workflow.
3. **Official platform/vendor skill** matching the actual technology/version when available.
4. **Thalarch process/language/domain skill** that supplies orchestration, verification, or a
   missing engineering lens.
5. **Trusted third-party/community skill** when it is more specific or useful than the generic
   fallback and does not conflict with stronger sources.
6. **Generic fallback reasoning** when no suitable skill exists.

A higher-authority skill does not win merely because of its source if it is irrelevant to the
actual task.

For Kotlin-specific tooling/migrations, an installed skill from the official Kotlin/JetBrains skill
collection is normally preferred over a generic community Kotlin guide when both match the same
problem. For version-sensitive Java/JVM facts from community skills, confirm against the project's
actual version and primary documentation before implementation.

## 5. Candidate scoring

For each serious candidate, reason over these dimensions:

- **Task fit** — does it directly address the current operation/problem?
- **Project specificity** — does it understand this repository/framework/workflow?
- **Version compatibility** — is its guidance compatible with the runtime/library/toolchain in use?
- **Authority/currentness** — project-owned or official/current guidance beats stale generic memory.
- **Host availability** — can this host actually load/use the skill, agent, or tool it depends on?
- **Tool leverage** — does it unlock a real browser, device, profiler, generator, MCP, or
  deterministic script that improves evidence?
- **Evidence leverage** — does it improve the ability to prove the acceptance criterion?
- **Complementarity** — does it add a missing lens rather than duplicate another loaded skill?
- **Context cost** — how much instruction/context will it consume relative to its value?
- **Conflict risk** — could its style/process rules contradict stronger project or user constraints?

Select the highest-value compatible set, not every candidate with a positive score.

## 6. Skill-stack shape

A normal engineering stack should usually contain only:

- one process skill (debug/spec/refactor/performance/focused-repair/etc.);
- one language skill when useful;
- zero to two domain/platform skills;
- one verification/review path.

Complex high-risk work may exceed this when independent concerns genuinely require it.

Avoid “skill soup”. If two skills cover the same concern, choose the more project-specific,
current, evidence-producing one unless the second adds a distinct capability.

## 7. Official/platform specialization

When installed and relevant, prefer current official platform skills for platform-specific facts
and workflows — for example Kotlin/JetBrains tooling, Android, browser tooling, Firebase,
cloud/vendor SDKs, or other curated integrations.

Thalarch remains the orchestration/quality layer around them. Do not duplicate their entire guidance
into active context when the **current host** can load the official skill directly.

## 8. Project-local skills

Treat project-local skill locations supported by the current host as high-value candidates because
they can encode repository-specific build, test, deploy, architecture, or style rules.

Examples of host-native locations may include `.agents/skills/`, `.claude/skills/`, or other
locations documented by the active host. Do not assume a path exists; inspect before using it.

Before trusting a project skill blindly, check that its scope still matches current repository
state. A stale project skill can be less reliable than current build/configuration evidence.

## 9. Deterministic tools beat extra prose

When a shortlisted skill ships a relevant read-only analyzer/script and it can run safely in the
current environment, prefer using that tool to guessing manually from a large codebase.

Examples include project/dependency scans, coverage parsing, architecture/dependency analysis, or
visual/browser evidence collection.

Treat script output as **evidence/leads**, not infallible verdicts. Confirm material findings in the
actual source/runtime before changing code.

## 10. Missing capability

If no installed skill adequately covers a high-value domain:

- use the host's available research/web/documentation capability and current primary documentation;
- when a Thalarch research specialist exists on this host, it may own that bounded research task;
- if research discovers a potentially useful external skill/plugin, report it as optional rather
  than silently installing it unless installation/customization is authorized;
- never fabricate a skill name or pretend a missing skill/tool was loaded.

## 11. Conflict resolution

When loaded guidance conflicts, resolve in this order:

1. platform/system safety constraints;
2. explicit current user instruction;
3. repository/project rules and exact build/runtime contracts;
4. current official platform/vendor guidance for the proven version;
5. Thalarch acceptance/safety/verification invariants;
6. third-party/general style guidance.

Do not let a community style skill override a repository's established conventions or an explicit
scope constraint.

A skill that requires artificial findings, arbitrary global style thresholds, blanket framework
migration, or unmeasured optimization must be narrowed to its useful evidence-producing part or
rejected.

## 12. Skill-selection ledger

For non-trivial work keep a compact working record:

- `Selected:` skill/capability → why it materially helps;
- `Rejected:` only close alternatives → why redundant/incompatible/unavailable/lower-value;
- `Deferred:` skill → condition that would make it relevant later.

Do not spam the user with the full candidate list. Surface the final stack when useful or when the
user asks how Thalarch routed the task.

## 13. Failure modes

Never:

- load all skills for “maximum power”;
- prefer a skill because its name sounds expert;
- use a language/framework skill before confirming the stack;
- keep a skill active after evidence shows it is irrelevant;
- assume another host's agent/tool exists here;
- duplicate official platform guidance into the main prompt when it can be loaded on demand;
- install third-party skills without authorization;
- let a skill's rigid checklist override stronger project evidence;
- treat skill activation as proof that the task was executed correctly.

A skill is guidance. Fresh repository/runtime evidence remains the authority for completion.
