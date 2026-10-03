---
skill_id: junction-guard
name: Junction Guard
description: "Block writes through filesystem junctions and symlinks — file write through .mxm-system or .claude junction, git commit through a junction, delete through a junction. Enforces the junction read-only rule so the real repo stays the source of truth."
version: 1.0.0
category: safety
type: enforcement
frameworks: []
triggers:
  - file write through .mxm-system\
  - file write through .claude\ junction
  - git commit through junction
  - delete through junction
collaborates_with:
  - session-memory
  - operator-profile
ethics_required: false
priority: critical
tags: [safety, enforcement, junction, nk-universe-rule]
created: 2026-04-16
updated: 2026-04-16
---

# Junction Guard

## Purpose

Enforce the NK universe **junction read-only rule**: when Maxim detects that a target file path resolves through a filesystem junction or symlink (typically `.mxm-system\` or `.claude\` inside a sister project), it must refuse all write, delete, and git commit operations through that path. Reading is allowed.

Without this guard, an agent could accidentally write to the `maxim` source repo while operating in another project (e.g., `mxm-simplification`) — corrupting cross-project state and violating the data flow rule.

## When This Skill Activates

- Any tool call that writes/edits/deletes a file
- Any git commit operation
- Any directory creation under a path that resolves through a junction

## The Rule (from PROJECT_STRUCTURE_NK.md)

> `.mxm-system\` and `.claude\` inside mxm-simplification\ are junctions.
> ✅ Reading through junctions is ALLOWED
> ❌ Writing through junctions is FORBIDDEN
> ❌ Deleting through junctions is FORBIDDEN
> ❌ Git commits through junctions are FORBIDDEN

This applies to ANY junction created by `bootstrap/link-local-project.ps1` or any user-created junction pointing back at the maxim repo.

## Detection Logic

For any write target path `P`:

1. Walk `P` upward to find any junction or symlink ancestor.
2. If an ancestor resolves to a path OUTSIDE the current project root, that ancestor is a JUNCTION (or cross-project symlink).
3. If the junction target is the Maxim source repo (`E:\Projects\Maxim\maxim\` or symlink-equivalent): apply READ-ONLY rule.
4. If the junction target is any other project: apply CROSS-PROJECT WRITE rule (also forbidden).

### Detection Commands

**PowerShell:**
```powershell
$item = Get-Item -Path "<target-path>"
if ($item.LinkType -in @("Junction", "SymbolicLink")) {
    $resolved = $item.Target
    # Compare $resolved to current project root
}
```

**Bash:**
```bash
real_target=$(readlink -f "<target-path>")
project_root=$(pwd)
if [[ "$real_target" != "$project_root"* ]]; then
    echo "BLOCK: write resolves outside project root via junction"
fi
```

## Enforcement

When a forbidden write is detected:

1. **REFUSE** the operation immediately. Do not proceed.
2. Output the error message:
   ```
   🔒 JUNCTION READ-ONLY VIOLATION

   Target path:  <target-path>
   Resolves to:  <real-resolved-path>
   Junction at:  <junction-ancestor>
   Reason:       <real-resolved-path> is outside the current project root

   This operation is FORBIDDEN by the NK universe junction rule.

   Allowed:
     ✅ Read this file through the junction
     ❌ Write / Edit / Delete / Commit through the junction

   To make this change:
     1. Open the source repo directly:
        cd <real-resolved-path-without-junction>
     2. Make the change there.
     3. Commit there.
     4. Pull updates here through the junction.
   ```
3. Log the attempt to `.mxm-skills/junction-guard.log`:
   ```jsonl
   {"timestamp":"2026-04-16T11:00:00Z","tool":"Write","target":"<path>","resolved":"<real>","blocked":true,"agent":"<calling-agent>"}
   ```

## When NOT To Block

- The junction target IS the current project root (false positive — junction created in a way that loops back). Verify with absolute path comparison.
- The target is a regular file inside the project (not through any junction).
- The user has explicitly invoked `/mxm-junction-bypass` (NOT IMPLEMENTED — would require CSO approval).

## Skill Output Format

```
Junction Guard Verdict: ALLOW | BLOCK
Target: [path]
Resolves to: [real-path or "same project"]
Crosses junction: YES | NO
Action: [proceed | refuse]
Logged to: .mxm-skills/junction-guard.log
```

## Handoff

- BLOCK → return refusal to caller agent; log incident; suggest direct repo access
- ALLOW → return immediately, no action
- Repeated BLOCKs from same agent → escalate to CSO `security-analyst` (potential agent misconfiguration)

## Frameworks Used

None. This is a structural safety enforcer, not a behavioral skill.

## Source References

- `PROJECT_STRUCTURE_NK.md` (Junction Rule section)
- `CLAUDE.d/session-memory.md` (Junction Read-Only Enforcement section)
- `bootstrap/link-local-project.ps1` (creates the junctions this guard protects)

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
