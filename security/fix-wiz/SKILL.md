---
name: fix-wiz
disable-model-invocation: true
# TODO(adapt): add Bash(<runner>:*) entries for INSTALL_CMD / TYPECHECK_CMD / TEST_CMD and the build command.
allowed-tools: mcp__wiz__discover, mcp__wiz__execute, Read, Edit, Grep, Glob, AskUserQuestion, Agent, Bash(scripts/worktree-create.sh:*), Bash(git:*), Bash(gh:*), Bash(jq:*), Bash(python3:*)
description: Triage each open Wiz finding (container CVEs and SAST), auto-fix the high-confidence ones in a worktree PR, and escalate the rest for review.
---

# Fix Wiz findings

Burn down a **worklist** of open Wiz findings. Each finding passes a confidence **gate**: high-confidence and mechanical gets fixed automatically; everything else **escalates** to a human decision. All fixes land in one PR reviewed at merge. Wiz stays read-only: never mark a finding resolved or rejected there, a landed fix clears itself on the next rescan.

> **Setup:** requires the Wiz MCP server and the same `.env` resource IDs as the `wiz` skill
> (`WIZ_REPO_BRANCH_ID`, `WIZ_CONTAINER_REPO_IDS` — see `.env.example`). Fill in your own IDs;
> never hardcode real UUIDs in the repo.

Scope from `$ARGUMENTS`: default both sources; `--cve` or `--sast` narrows.

## 1. Build the worklist

Read `.claude/skills/wiz/SKILL.md` for the project's resource IDs and the read-only query discipline (routing, array-typed params, large results persisting to a file). Then pull OPEN findings:

- **Container CVEs** (`vulnerabilities`): `list_vulnerability_findings` over the `container_repository` UUIDs from `${WIZ_CONTAINER_REPO_IDS}`, `severity: ["CRITICAL","HIGH"]`, `status: ["OPEN"]`, `has_fix: true`. Record per finding: image, CVE, `detailedName`, `version` to `fixedVersion`, `layerMetadata.isBaseLayer`, `artifactType.group`, `transitivity`, `hasCisaKevExploit` / `hasExploit`.
- **SAST** (`codesec`): `list_sast_findings` over the repo `resource_id` (`${WIZ_REPO_BRANCH_ID}`), `is_default_branch: true`, `status: ["OPEN"]`. Record: rule, severity, `filePath`:`startLine`, weakness (CWE).

Parse the persisted `tool-results/*.txt` with jq or python; dedupe. Print the worklist grouped by source and severity. Completion: every open finding is on the list with its fields, or the list is empty (stop and say so).

## 2. Branch

`scripts/worktree-create.sh fix-wiz-<yyyy-mm-dd>`, then work in `.worktrees/fix-wiz-<date>` via `git -C` (never the trunk, `GIT_TRUNK` in `.claude/project.env`). Confirm `branch --show-current` is not the trunk before the first edit.

## 3. Triage each finding through the gate

Assign every finding exactly one verdict. **AUTO-FIX** only when the fix is mechanical, semver-safe, and verifiable AND the weakness is confirmed real. Otherwise **ESCALATE**. Never contort code to silence a false positive; tag it **FP** with a reason instead.

**Container CVE:**
- AUTO-FIX: `fixedVersion` exists and the bump stays within the same major (patch or minor), it is a dependency bump or a base-image patch bump, and verify (step 5) stays green. Order by `hasCisaKevExploit`, then `hasExploit`, then severity.
- ESCALATE: major-version jump, no fixed version, a direct pinned production dependency with breaking risk, or verify goes red.

**SAST** (default ESCALATE, the false-positive base rate is high):
- AUTO-FIX only if reading `filePath`:`startLine` confirms the weakness is real, untrusted input actually reaches it, and the fix is behaviour-preserving.
- FP: record with rationale, do not edit. Known FP shapes live in `/wiz`'s "before treating a finding as real" (protocol-mandated weak hashes, timer callbacks as eval, internal config dirs as path traversal, plain-text templates with escaping off). Escalate anything touching crypto or auth even when it looks mechanical.

For a large SAST list, fan the per-finding code verification out to parallel `Agent` (security-reviewer) calls; keep the verdicts, not the transcripts.

Completion: every finding tagged AUTO-FIX, ESCALATE, or FP with a one-line reason.

## 4. Escalate (human in the loop)

Present all ESCALATE findings together via `AskUserQuestion` (batch them, do not ask one at a time): each with its finding, why it missed the gate, and the choices (apply a named fix / skip / mark FP). Fold approved fixes into the AUTO-FIX set. Do not touch an escalated finding without a decision.

## 5. Apply and verify

Apply the AUTO-FIX set, grouped by kind:
- **Dependency bump**: raise the dep, or pin a transitive one through the package manager's override / constraint mechanism, to `fixedVersion`, then regenerate the lockfile (`INSTALL_CMD` in `.claude/project.env`, or the package manager's update command).
- **Base image**: bump the `FROM` tag or digest in the Dockerfile.
- **SAST**: the confirmed mechanical edit.

Verify: `TYPECHECK_CMD`, the affected tests via `TEST_CMD` (both in `.claude/project.env`), and the project's build. Image base-bumps cannot build locally, so rely on the release image rescan and say so. A red verify sends the finding back to ESCALATE, never into the PR.

## 6. One PR

Commit the grouped fixes, push, and open a single PR (house style via `/pr-description`). Body carries three sections: **Fixed** (finding to bump/edit table), **Escalated / deferred** (with the decision), **False positives** (with rationale, for a human to mark in the Wiz portal). Link the Wiz findings. Reviewed at merge.
