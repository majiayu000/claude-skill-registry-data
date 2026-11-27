---
name: delegated-work-acceptance
description: >-
  Accept or send back a subagent handoff: inspect artifacts and diff, recount repairs and check
  patches against assigned folders. For a bug in another worker's directory, reproduce the failing
  command under the reporter's PATH and cwd, route it to the maintainer who owns the fix, and
  escalate one scoped landing decision. Not for dispatch.
metadata:
  revision: "19"
  areas: "work-management,software-development"
  targets: "runtime-agnostic"
  summary: "verify delegated work against artifacts and write scope; route rejected or out-of-scope fixes to their owner"
  summary_zh: "按 artifact 和写入边界验收委派成果，将退回或越界的修复交还给负责人"
  kind: "entry"
  consumes: "work-report"
  produces: "acceptance-verdict, scope-seal"
---

# Delegated work acceptance

A teammate's completion message is a claim, not evidence. Accept a repair,
report, corpus scan, or writing handoff only after independently verifying both:

1. **The artifact matches the claim.** Inspect the delivered files, including
   untracked ones, and run the applicable gates yourself. The sender's counts,
   gate results, exit status, and landing receipt do not transfer as proof.
2. **The change stayed inside the sender's write surface and outside reserved
   lanes.** Verify the path set against the approved scope, not the report hash.

## Authority boundary

- Re-open the role contract before ruling: your write list, the sender's write
  list, and what needs operator approval. Verify, rule, and route; send repairs
  back to the write owner rather than fixing them from the wrong surface.
- Authorize only a bounded, meaning-preserving subset and name the exclusions.
  Resolve reversible house-convention questions yourself when they touch no
  knowledge. Meaning changes, merges, and code changes stay with the operator.
- Compare a scope block with the approved plan's manifest. Name the exact path
  classes it covers, require a fresh pre-execute backup, and restate reserved
  lanes. Unlisted paths and overlapping writers need an explicit operator ruling.
- A bounded batch stops and reports a missing approved value; it does not invent
  one or make live or production calls. In-place probes and CI reruns need
  explicit authority. Commit and push stay with the operator.
- For a rejected or out-of-scope change, verify the claim first and route it to
  the maintainer. Check for scheduled publication before touching a shared tree.
  Ask the landing owner for one scoped decision; stop when only authorization
  remains. Re-verify the exact revised candidate, not an earlier approved head.

## What to read and when

| When to read | Reference |
|---|---|
| Before accepting any handoff: inspect the diff, re-run gates, re-derive counts, or verify a landing receipt | [Delivery checks](references/delivery-checks.md) |
| When reconstructing the dispatch boundary, matching a handoff to an approved manifest, or sealing or verifying the working increment | [Dispatch and scope seal](references/dispatch-and-scope-seal.md) |
| When judging corpus/graph findings, correcting an imprecise or revised report, or routing a rejected or out-of-scope defect | [Corpus and escalation](references/corpus-and-escalation.md) |

## Acceptance pass

1. Check status and the diff in the intended repository, then inspect changed
   lines in the files. Compare to the approved scope before accepting claims.
2. Recount against the real population and independently run the applicable
   gates. For a delivered tool, verify coverage of the actual action, failure
   path, and relevant flags before trusting a test count. Require a mutation
   check for each fix; a suite that stays green without it proves nothing.
3. Inspect the diff for semantic defects. Get an independent reviewer for new
   gate, policy, or validation logic, or a large diff; ask which guard can be
   removed without failing the suite.
4. When sealing with `scripts/worktree-scope.py`, put the same path set and
   `scope_sha` in the acceptance verdict and PR body. Do not include the receipt
   directory in the digest it records. Verify the seal before landing.
5. Re-check status at the end and list the exact uncommitted paths and owners.
   Reconcile revised reports against the latest operator or reviewer ruling;
   supersede contradictory drafts rather than leaving them executable.

## Output shape

1. What reproduced, with the numbers you computed (not the ones quoted back).
2. What did not, correct value first, in a numbered list the sender can act on.
3. What you authorized and what you explicitly withheld, with the revert unit.
4. Current uncommitted path list and what still needs the operator — as a numbered choice list.

Plain text, one point per line, no decoration: the reader may be on a phone.
