---
name: ls-skill-capture-handoff
description: "Captures completed operational knowledge as a standalone global skill and prepares an authorized upstream feature request with complete compressed code. Use when the user asks to preserve a setup workflow, or when the capture workflow has been explicitly adopted for completion offers."
license: MIT
compatibility: "Python 3.12+ for archive tooling; GitHub submission requires an authorized account. LocalSetup is optional."
metadata:
  version: "1.0"
---

# Capture and upstream handoff

**Purpose:** Preserve working knowledge once, then deliver reusable code to the
maintainer without making another agent rebuild it from a prose request.

## Boundaries

This skill owns the completion offer, packaging and contribution handoff.
The host's skill authoring/import workflow retains ownership of content creation,
duplicate resolution, external import screening and framework registration.
No other skills, framework commands or secret provider are required standalone.
Never install this behavior as global policy without explicit user direction.

## Workflow

1. Finish the actual software setup/repair task and its documentation first.
   Only when the user explicitly selected this completion-offer workflow, ask
   once for reusable knowledge: “Would you like me to capture this as a global
   skill/workflow?” Merely discovering or installing this skill does not enable
   completion offers. Respect a prior answer; skip trivial changes, tasks with
   no reusable result, or a previously declined offer. A direct user request
   to capture already authorizes capture, so do not ask again.
2. With capture authorized, inspect existing skills for an appropriate owner.
   Improve that owner when appropriate; resolve actual collisions with the user.
   Capture the shortest repeatable procedure, reusable implementation, parameters,
   prerequisites, checks, expected failures and recovery. Put details in linked
   references. Keep credentials, private evidence and deployment identities out.
3. Exercise the package's real non-destructive entrypoints in a standalone
   temporary directory without framework imports. Run only checks authorized by
   the task and host policy. Record exact coverage and limitations. For an
   ordinary capture, use the host's owning skill authoring and install workflow;
   no network or latest-release check is needed. In a LocalSetup-managed
   library, use its skill creator/importer and canonical installation path;
   adapters reference that owner. Do not overwrite a managed package or
   silently opt other installations into policy.
4. If preparing a LocalSetup contribution, check its latest published release
   through verified public HTTPS. Record the exact tag and commit and follow
   that release's Agent Skills and registration contract. If it cannot be
   checked, report compatibility as unconfirmed rather than claiming latest.
5. Prepare the complete public candidate only when contribution is intended.
   Use an explicit reviewed file list;
   exclude private state, env files, logs, keys, signed URLs and Git history.
   Include code, references, templates, license, compatibility record and
   integration instructions. `scripts/package_skill.py` builds a deterministic
   tar.gz with per-file SHA-256 manifest and prints the archive digest. Its
   structural guards are not a substitute for reviewing public disclosure.
6. Once the concrete package is ready, ask: “Would you like me to submit this to
   LocalSetup as a feature request with the full code archive?” Existing explicit
   submission authorization satisfies this step. Silence is not authorization.
7. On approval, inspect the target repository and its contribution rules. Prefer
   an issue with a compressed attachment or a verified immutable archive link
   accessible to the receiving maintainer. If issue attachment upload is not
   supported, publish an explicitly scoped code-only proposal branch and link
   the raw compressed archive at its commit. Do not merge or release it.
   Avoid recipient-encrypted-only links the maintainer cannot decrypt.
8. The request includes the problem, proposed behavior, authorization boundaries,
   exact compatibility baseline, full code archive and SHA-256, check evidence,
   integration instructions and remaining work. Verify issue and download after
   submission. Record URLs and local ownership in durable documentation.

## Efficient reuse

Reuse the reviewed code and passing evidence; do not reconstruct implementations
from chat. Recheck changed layers and release-specific integration. Pass the next
agent a narrow action list: inspect archive/manifest, apply candidate, run focused
checks, adapt current contracts, review and integrate through normal project gates.
Submission is a recommendation, not automatic upstream acceptance.

## Examples and policy

- [Portable policy text](assets/global-policy.md) requires explicit adoption.
- [Feature request template](assets/feature-request.md) is an authoring aid;
  replace all placeholders before submission.
- [Compatibility](references/compatibility.md) records this package's baseline.
- Run `python3 scripts/package_skill.py --help` for archive arguments.
