---
name: iot-firmware
description: Orchestrate firmware rollouts with canary deployment and anomaly-gated advancement
allowed-tools: Bash(npx *) mcp__claude-flow__memory_store mcp__claude-flow__memory_search Read
argument-hint: "<deploy|advance|rollback|status|list> [options]"
---
Manage firmware rollouts across device fleets.

**deploy**: `npx -y -p @claude-flow/plugin-iot-cognitum@latest cognitum-iot firmware deploy FLEET_ID --version VERSION`
**advance**: `npx -y -p @claude-flow/plugin-iot-cognitum@latest cognitum-iot firmware advance ROLLOUT_ID`
**rollback**: `npx -y -p @claude-flow/plugin-iot-cognitum@latest cognitum-iot firmware rollback ROLLOUT_ID`
**status**: `npx -y -p @claude-flow/plugin-iot-cognitum@latest cognitum-iot firmware status ROLLOUT_ID`
**list**: `npx -y -p @claude-flow/plugin-iot-cognitum@latest cognitum-iot firmware list`

Rollout stages: pending → canary → rolling → complete (or rolled-back)
