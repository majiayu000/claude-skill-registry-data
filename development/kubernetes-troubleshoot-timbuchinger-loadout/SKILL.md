---
name: kubernetes-troubleshoot
description: "Troubleshoot and manage Kubernetes clusters, including resource inspection, debugging, pod logs, events, and cluster operations. Use when the user needs to diagnose issues, inspect workloads, analyze pod failures, or perform Kubernetes cluster operations."
---

# Kubernetes Troubleshooting & Management Skill

## What this Skill does

Use this skill when the user needs to troubleshoot or manage Kubernetes clusters. This includes operations such as:

- Listing pods, deployments, namespaces, nodes
- Getting pod logs
- Fetching events for a resource
- Inspecting workloads and resource conditions
- Understanding CrashLoopBackOff, ImagePullBackOff, pending pods
- Multi-cluster interactions through kubeconfig contexts
- Suggesting next debugging steps

## Tool Preference: MCP First, kubectl as Fallback

**Preferred Method**: Use the Kubernetes MCP server when available

- MCP tools allow pre-approved operations for faster execution
- More efficient for common read operations
- Built-in safety guardrails

**Fallback Method**: Use kubectl commands via terminal when:

- MCP server is not available or fails
- MCP cannot provide the information needed
- Specific kubectl features are required (port-forward, plugins, etc.)

This skill helps Claude:

- Choose the appropriate tool based on availability and capabilities
- Restrict queries to namespace/cluster automatically  
- Ask for confirmation before destructive actions  
- Recommend stepwise debugging strategies  
- Provide safe, context-efficient responses

## Best Practices

### 1. Always scope operations

- Include **namespace** unless user explicitly wants cluster-wide.
- Include **context** when user has multiple clusters.
- Encourage **label selectors** instead of listing all resources.

### 2. Prefer read-only operations first

Recommended sequence for debugging:

1. List pods matching a selector  
2. Describe pod  
3. Fetch pod events  
4. Retrieve logs  
5. Inspect configmaps/secrets/environment  
6. Only then consider restart/delete/scale

### 4. Tool Usage Guidelines

**When using MCP** (preferred):
Examples of safe MCP-driven operations:

- **List Pods**: `list pods --namespace=<ns> --context=<cluster>`
- **Get Pod Logs**: `logs --namespace=<ns> --pod=<pod>`
- **Get Events**: `get events --namespace=<ns> --field-selector=involvedObject.name=<name>`
- **Inspect Deployment**: `get deployment <name> --namespace=<ns>`

**When using kubectl** (fallback):

- Always specify namespace with `-n <namespace>` or `--namespace=<namespace>`
- Use `--context` when multiple clusters are configured
- Consider using `-o yaml` or `-o json` for detailed inspection
- Use `kubectl explain` for resource documentation

- **List Pods**
  - `list pods --namespace=<ns> --context=<cluster>`

- **Get Pod Logs**
  - `logs --namespace=<ns> --pod=<pod>`

- **Get Events**
  - `get events --namespace=<ns> --field-selector=involvedObject.name=<name>`

- **Inspect Deployment**
  - `get deployment <name> --namespace=<ns>`

### 5. Multi-Cluster Awareness

If multiple contexts exist:

- Always request or infer the correct context.
- Avoid ambiguous commands that default to the wrong cluster.

## Example User Requests → Recommended Actions

| User wants                          | Preferred (MCP)                                                                         | Fallback (kubectl)                                                  |
|-------------------------------------|-----------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| "List pods in frontend namespace" | `list pods --namespace=frontend` | `kubectl get pods -n frontend` |
| "Show me events for api-server" | `get events --namespace=<ns> --field-selector=involvedObject.name=api-server` | `kubectl get events -n <ns> --field-selector involvedObject.name=api-server` |
| "Get logs for db-0" | `logs --namespace=<ns> --pod=db-0` | `kubectl logs -n <ns> db-0` |
| "Why is pod web-123 CrashLooping?" | List pod → describe → events → logs (stepwise) | `kubectl describe pod -n <ns> web-123`, then logs |
| "Restart worker deployment" | Ask confirmation → delete pods or rollout restart if supported | `kubectl rollout restart deployment/<name> -n <ns>` |

## Tool Limitations

**MCP Limitations**:

- Some advanced operations may not be available (port-forward, plugin commands)
- Complex manifest edits may require kubectl fallback

**kubectl Limitations**:

- Requires user approval for each command
- Less efficient for multiple sequential operations
- No pre-approval mechanisms) may not be available  
- Complex edits to manifests may require manual patching  
