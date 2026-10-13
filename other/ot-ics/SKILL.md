---
name: ot-ics
description: "OT and ICS Security"
---

# OT and ICS Security

## Scope

Use this module only with written authorization that identifies the site, network segments, assets, maintenance window, contacts, and explicitly permitted actions. Production control environments are passive and read-only by default.

## Safety Rules

- Never write coils, registers, logic, firmware, recipes, or controller configuration by default.
- Never interrupt a safety instrumented system or process-control path.
- Do not run broad or high-rate scans on production OT networks.
- Stop immediately on unstable process behavior, device faults, unexpected latency, or operator concern.

## Workflow

1. Build a Purdue-style zone and conduit map from diagrams, switch tables, firewall rules, and passive traffic.
2. Inventory PLCs, RTUs, HMIs, engineering stations, historians, jump hosts, and safety systems.
3. Identify protocols and communication pairs from SPAN/TAP captures or existing logs.
4. Review offline controller exports, engineering projects, firmware inventories, remote-access paths, and firewall rules.
5. Record cleartext protocols, weak trust relationships, obsolete firmware, exposed management services, and segmentation gaps.
6. Perform low-rate read-only identification only when explicitly approved in a maintenance window.

## Output

Return the zone/conduit map, asset and protocol inventory, evidence source, operational impact, confidence, and prioritized remediation. Include the exact authorization boundary and state whether every observation was passive, offline, or actively verified.

## 使用前核对

目标与操作范围以用户当前请求为准；核对方法前置条件、工具和附件，按实际执行层级记录结果。正文不表示示例代码已经在本机执行或验证。
