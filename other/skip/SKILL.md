---
name: skip
description: "Skip to a specific Forge phase. Use when the user says \"forge skip\", \"skip to develop\", \"skip phase\", or wants to bypass non-essential phases for their current task."
---

<Purpose>
Allow users to skip forward in the Forge pipeline when intermediate phases are not needed.
This is the primary escape hatch from the rigid phase-gate sequence.
</Purpose>

<Use_When>
- User says "forge skip", "skip to [phase]", "skip phase"
- KO: "건너뛰기", "스킵"  JA: "スキップ", "飛ばして"  ZH: "跳过", "跳到"
- Current phase is clearly unnecessary for the task at hand
- User has external artifacts (existing spec, existing design) that satisfy phase requirements
</Use_When>

<Steps>
1. Read current .forge/state.json to determine current phase
2. Ask user which phase to skip to (or accept from their message)
3. Validate the target phase is AFTER the current phase
4. Check what artifacts the skipped phases would have produced:
   - Skipping Discovery → need spec.md (ask user to provide or auto-generate minimal)
   - Skipping Design → need code-rules.md and contracts (ask user or extract from existing code)
5. Generate minimal required artifacts for skipped phases
6. Update state.json to the target phase
7. Create git tag for the skip: forge/skip-to-{phase}
8. Show dashboard with skip summary
</Steps>

<Constraints>
- Cannot skip backward (use forge:rollback for rollback)
- Cannot skip from intake directly to delivery
- Skipped phases still need minimal artifacts — generate stubs if user doesn't provide
- Log the skip in .forge/state.json history
</Constraints>
