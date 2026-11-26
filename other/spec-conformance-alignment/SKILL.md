---
name: spec-conformance-alignment
description: "Use when aligning a codebase with an external spec."
version: 1.0.1
author: Hermes Agent
license: MIT
compatibility: Any repository asked to conform to an outside specification, standard, or framework.
metadata:
  hermes:
    tags: [spec, conformance, standards, research, architecture, alignment, rfc2119]
    category: software-development
    related_skills:
      [grounded-citations, plan-to-tasks, write-docs, deep-repo-code-scan, kernel-audit-trace]
---

# Spec conformance alignment

## When to Use

- "Our system should align with <framework/spec/standard>" — Symphony, MCP, OWASP ASVS, WCAG,
  OpenTelemetry semantic conventions, a vendor's protocol.
- The user asks whether to follow an outside design, or wants the industry consensus applied to a
  codebase that already works.
- Someone hands you a spec's URL and expects a plan, not a rewrite.
- The "spec" is internal — a principles/rules corpus, a conventions doc, or a written protocol the code
  is supposed to implement — and the question is whether the document and the system still agree.

## The shape of the job

Conformance work is a mapping exercise with a decision at the end, not a port. You produce: what the
spec requires, what the code does today (with file paths), what the delta costs, and which forks only
the user can call. Then you stop and let them choose.

## Procedure

1. **Confirm the artifact exists and pin its version.** Search before designing: an unfamiliar
   framework name may be a misremembering of something else. Record the spec's own status line
   (`Draft v1`, preview, deprecated), its licence, and whether upstream intends to maintain it. Cite
   the primary document — the spec, the standard, the official announcement — never blog coverage of
   it.
2. **Read the normative layer before the prose.** Find the RFC 2119 section: `MUST`/`MUST NOT` are
   the tests, `SHOULD` is the default you may deviate from, `MAY` is optional, and
   "implementation-defined" means _document your choice_ — that clause is a deliverable, not filler.
   If the spec ships a conformance matrix or definition-of-done checklist, copy it: it is the task
   list, and it is what a reviewer will grade you against.
3. **Map three ways, with file-path evidence.** For each requirement: aligned (name the file),
   divergent by design (name the file and the reason), or gap (name the file that would change).
   A "gap" with no target file is an opinion. Order the table the way the spec orders itself so the
   reader can walk both side by side.
4. **Find the real conflict, then test whether it is capability or custody.** Every mature system
   has a place where the spec contradicts its architecture — usually a trust boundary (who holds
   credentials), an ownership boundary (who writes to the tracker), or a state model. Before
   calling it a conflict, read the normative section that governs that behaviour and quote it:
   specs often hand the _agent_ the same capability through a host-executed tool, which makes the
   divergence a **custody** difference (who holds the secret) rather than a capability loss. Say
   which one it is — only a capability conflict is a fork worth the user's decision; a custody gap
   is a hardening item you can plan without asking. Either way do not silently resolve it: state
   what each side buys, recommend one, and hand the fork over. Architecture choices are the user's.
5. **Treat the spec's non-goals as requirements.** The non-goals section tells you what not to bolt
   on and often names your competitive advantage ("no rich web UI" means the dashboard is yours to
   keep). Alignment that deletes a differentiator is a regression, not conformance.
6. **Phase it, cheapest-true first.** P0 = the conformance surface with no behaviour change (contract
   files, loaders, `docs/conformance.md`). P1 = scheduler/logic parity. P2 = boundary hardening.
   P3 = compatibility surfaces the spec defines. P4 = the spec's test matrix wired into CI. Each
   phase lands with the spec's own checklist items as tests, so conformance is measured, not
   asserted. P0 is the phase to get exactly right: land the contract as an _overlay_ — parsed,
   validated, rendered, and wired in additively — while the existing configuration stays
   authoritative, so a repository that ships no contract file behaves byte-identically. See
   `references/conformance-table.md` for that recipe and the table's shape.
7. **Deliver a document, then discuss.** Write `docs/<framework>-alignment.md`: executive summary,
   what the thing is, the normative core, the three-way map, the decisions, the phased plan, sources.
   Summarise in chat with the gap table and the forks. Do not start rewriting the architecture off
   the back of a research answer. When the user approves a phase, implement that phase only, and
   keep the conformance table in step with the code inside the same change.

## Pitfalls

- **Porting the reference implementation instead of the spec.** When upstream ships both, the spec is
  the durable artifact and the code is a demo. OpenAI publishes Symphony explicitly as "a reference
  implementation" that they do not plan to maintain; conforming means implementing its `SPEC.md` in
  whatever language the host repo already uses.
- **Skipping the "is this real?" check.** A confidently named framework that does not exist gets
  designed around if you assume rather than search. One search settles it, and the answer also tells
  you how mature it is.
- **Treating a preview as settled.** A preview or prototype can still be worth conforming to, but say
  so: record the upstream warning, and put the trust posture in your own docs, because specs of this
  kind routinely require implementations to "document the selected behavior".
- **Divergence without a reason.** "We do it differently" is not a classification. Either the spec
  allows it (`SHOULD`, `MAY`, implementation-defined) or you are non-conforming and should know it.
- **Citing a spec without a section number.** `SPEC.md §7.4` survives review; "the spec says" does
  not. Quoted evidence per claim beats paraphrase, and drafts renumber — pin the version you read.
- **Turning an audit into a rewrite.** The deliverable of this class of task is a decision-ready
  document plus phased issues the user approves; code follows the approval, one issue at a time.
- **Classifying a custody difference as a capability conflict.** Telling the user the spec would
  take away something they value is the expensive mistake: a clause that keeps the work with the
  agent and merely executes it with a host-held credential moves the secret, not the capability.
  When the primary text contradicts your earlier classification, correct the document and name what
  you overstated in one sentence — a defended wrong analysis costs more than the admission does.
- **Writing the conformance table as paperwork.** Filling every checklist row forces you to name the
  file that actually implements the requirement, and that is where defects surface: the rows that
  hold up are the ones you verified in code, and the rows that do not are new issues. Budget for
  finding something, and keep "parsed but not applied" separate from "applied" so the document
  cannot overclaim ahead of the code.
- **Shipping a doc's own recipe untested.** A `node -e` snippet, a test command or a config example
  inside the deliverable is a claim like any other: run it against a real sample file before you
  publish the doc, or the next session inherits a recipe that never worked.
- **Assuming a contract loader is tested because it parses the happy path.** The suffix does not, the
  comment placement does not, the folded marker does not. A hand-rolled parser for a repo-owned config
  file fails on comment-before-coercion, folded-versus-literal block scalars, quoted list entries
  containing commas, a nested block starting with a comment, single-`!` tags, BOM/CRLF, and
  mtime-preserving rewrites — each is one line of the parser and one test. See
  `references/conformance-table.md` and `references/evidence-recipes.md` §9.
- **Treating a document as evidence of the system.** A routing block, a label protocol, a ticket
  template, a config key: a doc that names them is making a claim, not reporting a fact. Count the live
  objects that actually carry it (one audit found zero of seventeen project descriptions containing the
  block its own rules described) and grep the implementation for the documented keys (the branch field
  the doc said to use had no call site at all). Align to what runs. The failure is silent in both
  directions — the agent follows the document, the code follows its own resolver, each believes it
  conforms, and nothing in either system raises a hand.
- **Auditing a normative document against itself.** When the corpus is yours (a principles skill, a
  conventions doc, stacked learned rules), contradictions hide across the tier boundary: a headline that
  states an invariant absolutely and a reference file that already documents the exception. Harvest the
  absolutes (`never|always|no |only|nothing|every|must`) and the exceptions
  (`except|unless|is fine|exempt|allowed|only when`), pair them by subject rather than by wording, then
  classify before fixing: hard contradiction, overstatement (the common case), duplicate, provenance
  conflict (a corpus claiming "law" over entries that were inferred), dangling pointer. Repair an
  overstatement by pulling the reference's qualifier up into the headline — never by deleting the
  stricter side, which is usually the rule the person actually cares about — and audit first anything
  you wrote yourself to smooth a merge, because invented text has no owner and no memory behind it.

## Related

- `references/evidence-recipes.md` — the commands that make an alignment claim checkable: proving a
  build or gate claim on a clean copy, sweeping a running service's logs, counting consumers, and
  before/after measurements.
- `references/conformance-table.md` — how to write and maintain `docs/conformance.md`: status
  vocabulary, row shape, the trust-posture section, and the P0 overlay recipe that adopts a
  contract file without changing behaviour.
- `grounded-citations` for the citation ledger and the Sources block format.
- `plan-to-tasks` once the user approves a phase.
