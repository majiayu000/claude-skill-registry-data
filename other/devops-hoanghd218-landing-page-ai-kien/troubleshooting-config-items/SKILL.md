---
name: troubleshooting-config-items
description: Troubleshoots infrastructure and application configuration items in Mission Control by diagnosing health issues, analyzing recent changes, and investigating resource relationships. Use when users ask about unhealthy or failing resources, mention specific config items by name or ID, inquire about Kubernetes pods/deployments/services, AWS EC2 instances/volumes, Azure VMs, or other infrastructure components. Also use when investigating why a resource is down, stopped, degraded, or showing errors, or when analyzing what changed that caused an issue.
allowed-tools: search_catalog, describe_config, list_catalog_types, get_related_configs, search_catalog_changes, get_notification_detail, get_notifications_for_resource
---

# Config Item Troubleshooting Skill

## Core Purpose

This skill enables Claude to troubleshoot infrastructure and application configuration items in Mission Control, diagnose health issues, analyze changes, and identify root causes through systematic investigation of config relationships and history.

## Understanding Config Items

A **ConfigItem** represents a discoverable infrastructure or application configuration (Kubernetes Pods, AWS EC2 instances, Azure VMs, database instances, etc.). Each config item contains:

- **health**: Overall health status ("healthy", "unhealthy", "warning", "unknown")
- **status**: Operational state (e.g., "Running", "Stopped", "Pending")
- **description**: Human-readable description (often contains error messages when unhealthy)
- **.config**: The actual JSON specification/manifest (e.g., Kubernetes Pod spec, AWS instance details)
- **type**: The kind of resource (e.g., "Kubernetes::Pod", "AWS::EC2::Instance")
- **tags**: Metadata for filtering and organization
- **parent_id/path**: Hierarchical relationships to other configs
- **external_id**: External system identifier

## Key Workflows

### Initial Investigation

**1. Search and Identify the Config**
Use the MCP `search_catalog` tool to find the config item:

- Search by id, name, type, tags, or other attributes
- Narrow down to the specific config experiencing issues

**2. Get Complete Config Details**
Use the MCP `describe_config` tool to retrieve full config information:

- Review the **health** field for overall status
- Check the **status** field for operational state
- Read the **description** field carefully - this often contains error messages or status information
- Examine the **.config** JSON field - this contains the full specification/manifest

### Change Analysis

**3. Review Recent Changes**
If the issue isn't immediately apparent, use the MCP `search_catalog_changes` tool:

- Get changes for the specific config item
- Look for recent modifications to the specification
- Check `change_type` (created, updated, deleted)
- Review `severity` (critical, high, medium, low, info)
- Examine `patches` and `diff` fields to see what changed
- Check `source` to understand where the change originated
- Note the `created_at` timestamp to correlate with when issues started

### Relationship Navigation

**4. Investigate Related Configs**
Use the MCP `get_related_configs` tool to navigate the config hierarchy:

- **Children**: Resources created/managed by this config
  - Example: A Kubernetes Deployment → ReplicaSets → Pods
  - Example: An AWS Auto Scaling Group → EC2 Instances
- **Parents**: Resources that manage this config
  - Example: A Pod → ReplicaSet → Deployment
- **Dependencies**: Resources this config depends on
  - Example: A Pod → ConfigMaps, Secrets, PersistentVolumeClaims

**Troubleshooting Pattern:**
When a parent resource is unhealthy, investigate its children to find the actual failing component. When a child is unhealthy, check the parent for misconfigurations.

## Critical Requirements

**Hierarchical Thinking:**

- Kubernetes: Namespace → Deployment → ReplicaSet → Pod → Container
- AWS: VPC → Subnet → EC2 Instance → Volume
- Azure: Resource Group → VM → Disk

**Change Impact Analysis:**

- Compare current config with previous working state
- Identify what changed and when
- Correlate timing of changes with health degradation

**Evidence-Based Diagnosis:**

- Support conclusions with specific evidence from the config data
- Quote relevant error messages from description fields
- Reference specific fields in the .config JSON
- Cite change diffs and timestamps

## Diagnosis Workflow

Follow this systematic approach:

1. **Identify** - Find the config item
2. **Assess** - Review health, status, description, and .config spec
3. **Analyze Changes** - Check recent modifications and events
4. **Navigate Relationships** - Investigate parent/child/dependency configs
5. **Review Analysis** - Check automated findings
6. **Synthesize** - Determine root cause from all evidence
7. **Recommend** - Provide specific remediation steps

## Example Troubleshooting Scenarios

**Scenario 1: Unhealthy Kubernetes Deployment**

- Get Deployment details → health: unhealthy
- Get related configs (children) → ReplicaSets → Pods
- Find Pod in CrashLoopBackOff
- Check Pod .config → image pull error
- Check changes → recent image tag update
- Root cause: Invalid image tag deployed
- Recommendation: Rollback to previous image or fix image tag

**Scenario 2: AWS EC2 Instance Issues**

- Get Instance details → status: stopped, health: unhealthy
- Check description → "InsufficientInstanceCapacity"
- Review changes → instance type changed to unavailable type
- Get related configs → Security Groups, Volumes
- Root cause: Requested instance type not available in AZ
- Recommendation: Change to available instance type or different AZ
