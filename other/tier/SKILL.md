---
name: tier
description: "View or change the current Forge tier level. Use when user says \"forge tier\", \"show tier\", \"change tier\", \"set tier to light/medium/full\", or wants to understand or control the guardrail level."
---

<Purpose>
Make the adaptive tier system visible and controllable.
Shows current tier, explains what each tier does, and allows manual override.
</Purpose>

<Steps>
1. Read .forge/runtime.json and .forge/state.json
2. If user just wants to SEE the tier:
   Show:
   ```
   Current Tier: {tier}
   Task Type: {last_task_type}
   Active Hooks: {count based on tier}
   Recommended Agents: {list}
   
   Tier Levels:
   - off:    No guardrails, no hooks
   - light:  Basic hooks only (3/11), no write guards
   - medium: Write risk assessment, contract reminders
   - full:   All guards active, evidence required, stop protection
   ```

3. If user wants to CHANGE the tier:
   - Update runtime.json with new tier
   - Recalculate recommended agents
   - Show what changed

4. Tier can also be set via FORGE_TIER environment variable
</Steps>
