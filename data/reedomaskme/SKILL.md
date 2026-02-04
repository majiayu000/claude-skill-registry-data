---
name: reedom:askme
description: Interactive clarification mode for uncertain situations. Use only when user invokes with --askme flag.
---

<purpose>
Prompt for clarification when uncertain, rather than proceeding with assumptions.
</purpose>

<target>
Any task where uncertainty exists about requirements, approach, or implementation details.
</target>

<effects>
- Interactive mode for ambiguous situations
- Ask before making uncertain decisions
- Clarify requirements when multiple interpretations exist
- Verify approach when multiple valid options exist
- Questions focus on genuine uncertainty, not confirmation
</effects>

<principle>
Reduce wasted effort from incorrect assumptions by asking upfront.
</principle>

<usage>
```bash
# Ask when uncertain during implementation
Implement user authentication --askme

# Ask during complex refactoring
Refactor payment module --askme

# Works with --foryou
Create API spec --askme --foryou
```
</usage>

<impact>
Without: Proceed autonomously with reasonable assumptions
With: Ask clarifying questions when uncertain before proceeding
</impact>

<default>
Autonomous operation unless `--askme` specified.
</default>
