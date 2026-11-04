---
name: agent-system-live-quality-ops
description: Operate and validate AgentSystem live quality alarm (systemd timer + alert state) to keep memory/proactivity/consistency regressions visible in real time.
---

# AgentSystem Live Quality Ops

Use this skill when you need to verify that live quality alerts are active and not silently failing.

## Quick Start

1. Dry-run alarm logic:
```bash
bash /Users/user/clawd/scripts/agent-system-live-quality-alarm.sh --dry-run
```

2. Inspect timer + last run:
```bash
bash scripts/check_live_alarm.sh
```

3. Force a manual alert test (optional):
```bash
bash /Users/user/clawd/scripts/agent-system-live-quality-alarm.sh --force-alert --dry-run
```

## Workflow

1. Confirm `hachix-agent-system-live-quality-alarm.timer` is active.
2. Verify latest health report and alarm state file exist.
3. Check if alert suppression/cooldown is working as expected.
4. If timer is inactive, enable it and re-run a dry check.
5. Record findings in reports or memory notes.

## Resources

- `scripts/check_live_alarm.sh`: one-shot operational status summary.
- `/Users/user/clawd/scripts/agent-system-live-quality-alarm.sh`: main alarm runner.
- `/Users/user/clawd/reports/agent-system-plan2-health-latest.json`: last health metrics snapshot.
