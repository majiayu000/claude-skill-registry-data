---
name: adopt-context-docs
description: Adopt Context Docs in a new or existing project and add its ongoing maintenance rule to the project's agent instruction file, such as AGENTS.md or CLAUDE.md. Use for project setup or adoption requests; use context-docs directly for routine maintenance or audits.
---

# Adopt Context Docs

Apply the sibling [context-docs skill](../context-docs/SKILL.md)
to the current project and establish ongoing use. Read that skill first; it owns
the maintenance method. If unavailable, report the missing dependency rather than
silently inventing a substitute.

Apply core's clarity preference within adoption's existing edit scope, preserving
conditions, uncertainty, rationale and evidence. For concurrent work on the same
context file, follow core's
[shared-file coordination](../context-docs/SKILL.md#make-the-smallest-useful-update):
one writer per file, explicit handoff, and reconciliation after conflicts.

Read the project's instructions and entry points. Confirm the target from the
workspace; ask only when the intended project is ambiguous. Preserve existing
storage choices. If the user requests local-only context, follow the core skill's
[local-only guide](../context-docs/references/local-only.md) before initialization:
establish the ignored, untracked destination and a suitable discovery route,
preserve tracked context until any migration is explicitly scoped, and keep local
content out of shared docs and instructions. Skill installation, upgrade and repeat
adoption alone do not select local-only storage. Initialize missing
context or maintain existing documents using the skill. Preserve useful layouts,
approved decisions, rationale, source evidence, unresolved work and concurrent edits.
Do not manufacture missing intent or populate empty templates merely for completeness.

Apply core's [destination and reference filtering](../context-docs/SKILL.md#make-the-smallest-useful-update)
to new context and progress summaries. Prefer
portable project references; keep incidental machine/account details and repeated
setup bookkeeping out of shared additions. Preserve useful local knowledge,
diagnostic meaning and evidence boundaries. Adoption does not authorize rewriting
frozen records, moving private material or changing existing storage rules.

Use the core skill's [Markdown progress guide](../context-docs/references/progress.md)
during adoption. By default, create a simple inline visual path in a suitable
existing context section when a documented goal and supported work/status or
next-step facts make it useful. Reuse an existing progress view in its current
location and format instead of adding another. Follow the guide's adoption rules
for concise overviews with linked evidence, sparse context and preserving
authoritative details and the existing layout. Favor an overview over test/review
chronology when creating a view; do not reshape an established view merely to shorten it.
Refresh the view through core after meaningful changes during everyday work;
the user need not ask for each update.

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
Preserve existing equivalent guidance as written. For newly added maintenance
wording, adapt this example to local terminology without client-specific
invocation syntax:

> Use the context-docs skill for documentation audits and after meaningful changes
> to project facts, decisions, procedures, blockers or next actions. Read the skill
> before maintenance. Preserve project rules, document roles and decision status.
> Update affected canonical sections and check the diff, links and information
> preservation, keeping any existing progress view current without duplicate
> tracking. Keep audit-only requests read-only; make no bookkeeping edits
> when nothing durable changed.

Reuse the installed skills; do not create duplicate packages or change global
instructions. If the user requests audit-only, report adoption recommendations
without editing instruction files or documents. Existing equivalent setup
may require no changes. This workflow adds no authority to publish, deploy or
schedule work; follow the project's existing authorization.

Treat older Context Docs journal settings as inactive. Repeat adoption preserves
existing settings and files and omits journal setup from the maintenance rule.

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
section is also valid for shared context. For local-only adoption, record
`Context storage: local-only` beside the marker only in an existing local
instruction location or an explicitly agreed shared pointer location. If neither
is established, use the agreed session prompt and report the persistent discovery
gap; do not insert a marker into shared instructions as a fallback. Preserve
equivalent existing wording and avoid a public README link to an ignored target.
The marker records intent; separately verify tracking, ignore status and
instruction loading, reporting an unresolved setup without claiming it is complete.
For new adoption, use the current date. Preserve an existing
adoption date and equivalent marker rather than adding another. When adding a
marker to previously adopted guidance, use a supported original date or `unknown`
if none is recorded; do not invent the history. For setup records, if equivalent
maintenance guidance and context already exist, add only the missing marker. Preserve the guidance's
wording; a missing marker alone is not a reason to reinitialize or rewrite it.
Update the entry point only when its canonical location changes. Do not mark
incomplete setup as adopted or add a marker during an audit-only request. Existing
projects without markers may still follow the method; the marker records adoption,
not document accuracy or freshness.

Review the marker and its target along with the final diff. Report changes,
verification and unresolved questions, including whether ongoing guidance and
the marker were added, reused or remain incomplete.
