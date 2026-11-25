---
name: adopt-context-docs
description: Adopt Context Docs in a new or existing project and add its ongoing maintenance rule to the project's agent instruction file, such as AGENTS.md or CLAUDE.md. Use for project setup or adoption requests; use context-docs directly for routine maintenance or audits.
---

# Adopt Context Docs

Apply the sibling [context-docs skill](../context-docs/SKILL.md)
to the current project and establish ongoing use. Read that skill first; it owns
the maintenance method. If unavailable, report the missing dependency rather than
silently inventing a substitute.

Read the project's instructions and entry points. Confirm the target from the
workspace; ask only when the intended project is ambiguous. Initialize missing
context or maintain existing documents using the skill. Preserve useful layouts,
approved decisions, rationale, source evidence, unresolved work and concurrent edits.
Do not manufacture missing intent or populate empty templates merely for completeness.

Add or update a concise rule in the instruction file this project's agent actually
loads, merging with existing guidance rather than duplicating it. Establish loading
from explicit session evidence or documented behavior for the observed client
version and settings. A file's presence, or reading it with a tool, does not prove
automatic loading. Distinguish an existing maintenance rule from verified loading;
report loading as unconfirmed when that evidence is absent, including during audits.
`AGENTS.md` and `CLAUDE.md` are both common; clients can load different files. When the
project keeps several, add the rule to the one in effect and make it reachable
from the others by their supported reference or import, instead of maintaining
separate copies. A rule placed in an unloaded file silently does nothing.
Adapt this wording to local terms and to how this client invokes skills:

> Use the context-docs skill for documentation audits and after meaningful changes
> to project facts, decisions, procedures, blockers or next actions. Read the skill
> before maintenance. Preserve project rules, document roles and decision status.
> Update affected canonical sections and check the diff, links and information
> preservation. Keep audit-only requests read-only; make no bookkeeping edits
> when nothing durable changed.

Reuse the installed skills; do not create duplicate packages or change global
instructions. If the user requests audit-only, report adoption recommendations
without editing instruction files or documents. Existing equivalent setup
may require no changes. This workflow adds no authority to publish, deploy or
schedule work; follow the project's existing authorization.

Review the resulting diff, affected links and information preservation before
recording adoption. Once the setup is complete, add or reuse one small marker beside
the maintenance rule in that instruction file:

```text
Method: context-docs
Adopted: YYYY-MM-DD
Entry point: path/to/context.md
```

When creating a new maintenance section, prefer a `Context maintenance` heading,
followed by the adoption marker, then maintenance instructions. Preserve existing
equivalent sections and marker positions; do not rearrange them solely for
formatting consistency.

Use the actual context entry point, relative to that instruction file; a README
section is also valid. For new adoption, use the current date. Preserve an existing
adoption date and equivalent marker rather than adding another. When adding a
marker to previously adopted guidance, use a supported original date or `unknown`
if none is recorded; do not invent the history. If equivalent maintenance guidance
and context already exist, add only the missing marker. Preserve the guidance's
wording; a missing marker alone is not a reason to reinitialize or rewrite it.
Update the entry point only when its canonical location changes. Do not mark
incomplete setup as adopted or add a marker during an audit-only request. Existing
projects without markers may still follow the method; the marker records adoption,
not document accuracy or freshness.

Review the marker and its target along with the final diff. Report changes,
verification and unresolved questions, including whether ongoing guidance and
the marker were added, reused or remain incomplete.

## Optional logging

Adoption and skill upgrades leave logging off unless explicitly enabled by the
project. Preserve existing logging preferences and history. For a request to
enable or disable JSONL, follow the core skill's
[journal guide](../context-docs/references/event-journal.md), merging only the
requested settings into the existing loaded maintenance section. Do not change
adoption dates, context paths or equivalent maintenance wording. Repeated setup
with the same settings makes no edits or events; audit-only requests change nothing.
