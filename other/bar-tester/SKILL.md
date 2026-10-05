---
name: bar-tester
description: "Design the smallest sufficient software verification around how people will actually use the product, including the 'fried rice' boundary that expected-input tests miss. Use automatically before MAGA forms or implements the first software Ticket, when a project has no confirmed validation profile, when that profile changes, or when the user asks how to test a code change, bug fix, build, or release. Calibrate from current audience, exposure, delivery, system size, and concrete risks; do not default to TDD or a new test framework."
---

# Bar Tester

A tester can exhaust every valid and invalid drink order and still miss the first real customer who orders fried rice. Start from real use, then choose the smallest proof that fits it. Treat future ambitions as planning notes until the project crosses that boundary.

## Get The Product Owner's Selection

Read `.ai-workflow/PROJECT.md` when it exists. Before the first software Ticket or implementation, require a Product Owner-confirmed Project Profile. First interpret the user's product description and repository evidence. Map vague language such as “a few people,” “online,” or “a small project” to a recommended profile instead of handing classification work back to the user.

If Project Memory does not exist and the current task is not MAGA onboarding, use the confirmed profile for the current task without initializing project files solely for validation. A later Project Lead onboarding must confirm and persist it again.

Repository evidence and inference may produce the recommendation but never the confirmation. Present the proposed mapping, its short factual basis, and the available choices in one compact question in the user's language:

```text
Before I choose the testing depth, please confirm the project's current profile—not its future ambition.

My current recommendation: <Use> / <Exposure> / <Delivery> / <Size>
Why: <one sentence based on the user's description and repository evidence>

1. Use: Personal / Controlled group / Public
2. Exposure: Local or offline / Internal network / Internet
3. Delivery: Run from source / Shared artifact / Public release
4. Size: Small / Medium / Large

For size: Small is one compact app or service; Medium has several connected
modules or services; Large is a monorepo or distributed system that already
benefits from dependency-graph or affected-change selection.

Confirm this recommendation or correct any item. If any of these changes later,
tell me before the next implementation or
release. I will update the profile and add only the validation required by the
new boundary.
```

When evidence is sparse, recommend the least expanded profile consistent with today's known use and mark the uncertain assumption in `Why`; do not proceed until the user confirms or corrects it. When the user already stated every field clearly, still summarize the mapping once and obtain confirmation before recording it. Accept a concise reply such as `Confirmed` or `Controlled, Internet, Shared artifact, Medium`. This profile confirmation is one product decision, not four rounds of interview.

Record the completed selection under `## Project Profile` in `.ai-workflow/PROJECT.md`:

```markdown
## Project Profile

- Current use: personal | controlled | public
- Exposure: local | internal | internet
- Delivery: source | shared-artifact | public-release
- System size: small | medium | large
- Risk modifiers: none | auth | sensitive-data | money | migration | concurrency | irreversible | untrusted-input | other
- Selection: Product Owner confirmed
- Change rule: Product Owner will report a material profile change before implementation or release.
```

Infer risk modifiers from the product and changed behavior. Ask only when an unknown risk changes authorization or minimum evidence.

## Choose The Baseline

Use current use to choose assurance:

- **Personal:** run the final change once from its real entry and observe the changed fact. Use one exact existing test for stable logic or a bug when it is cheaper and more direct. Add a persistent regression test only when recurrence has real cost.
- **Controlled:** include the Personal proof, then leave one repeatable proof at the public seam used by the known group. When environment or artifact shape differs, run it once in that target shape. For touched permissions or persisted state, prove the relevant allow/deny or write/read behavior.
- **Public:** include the Controlled proof, exercise one affected critical cross-boundary path, add the relevant negative case for a touched security control, and prove the final artifact or deployment from an explicit commit. Do not expand to unrelated paths.

Use system size only to select work economically:

- **Small:** one exact command, test name, or real-entry smoke.
- **Medium:** the affected component plus one cross-component proof only when the change crosses that boundary.
- **Large:** use existing affected/related selection, dependency graphs, caching, or sharding. Do not build this infrastructure for one narrow change.

Exposure and delivery add only their delta:

- Internal access does not cancel authentication, permission, or sensitive-data risk.
- Internet exposure adds a relevant untrusted-input, authorization, session, encoding, leakage, or abuse check only when the changed entry touches it.
- A shared artifact needs one clean install or start from that exact artifact.
- A public release needs an explicit clean commit, final artifact identity, known-good commit, rollback path, and one target-environment smoke.

For authentication, sensitive data, money, migration, concurrency, irreversible effects, or other high-risk behavior, state `specific risk → smallest added evidence` and obtain Product Owner confirmation before expanding validation beyond the selected baseline.

## Write An Adaptive Ticket Check

For Personal + Local + Source with no risk modifier, keep the existing one-line form:

```markdown
## Completion Check

Run <real entry or exact check> once and observe <changed product fact>.
```

For Controlled, Public, artifact delivery, Internet exposure, or a risk modifier, use the smallest durable proof that explains the added boundary:

```markdown
## Proof

- Break to catch: <one relevant failure>
- Evidence: <exact smoke, command, inspection, artifact, or target environment>
- Persistent regression: no | yes — <why>
- Risk delta: none | <risk → minimum added evidence>
- Stop when: <observable pass condition>
```

Outcome and Acceptance already contain the desired behavior. Do not duplicate them in `Proof`.

## Handle Profile Change

Treat a change from Personal to Controlled/Public, Local to Internal/Internet, source to an artifact/release, or a materially larger system shape as profile drift. If the user announces drift, update the profile before forming the next Ticket. If requested work itself appears to cross a stored boundary, pause and ask the Product Owner to choose the new value rather than silently promoting it.

Reuse still-valid Ticket evidence. Add only the proof for the new audience, exposure, artifact, environment, or selection boundary. A future public goal must not increase today's Personal prototype checks.

## Stop

Stop validation when the changed observable fact and the current highest relevant risk each have one direct proof from the final code—or from the final artifact and target environment during promotion. Coverage targets, test-layer counts, browser matrices, repeated green commands, and hypothetical future release are not reasons to continue by default.
