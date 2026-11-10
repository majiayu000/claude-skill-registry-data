---
name: platform-hosting
description: Use to work with an org's apps on Platform Hosting. List, register from a template, deploy a tag, roll back, start or stop, read logs, and call an app's own MCP tools.
---

# Hosting

An app is something the org runs on a hosting provider: RunPod, where the org pays with its own key, or This server, the server Platform runs on. Each app has a manifest, a pod or container, a current tag and its deployments.

## Look

- `hosting.list`: every app, its provider, tag, pod and the latest deployment.
- `hosting.get`: one app's manifest, pod, tag and recent deployments.
- `hosting.pod`: the live pod: status, address, hardware.
- `hosting.logs`: the last lines of a This server app's output.
- `hosting.providers`: which providers the org set up.

## Change

| Task | Tool | Notes |
| --- | --- | --- |
| New app from a template | `hosting.templates`, then `hosting.create_from_template` | Secret inputs are saved as org secrets |
| New app or new manifest | `hosting.register` | A manifest object, or a repo with `platform.app.yaml`. `pod_id` adopts a pod that already runs |
| Deploy a tag | `hosting.deploy` | Confirm. The health check rolls a failed deploy back |
| Roll back | `hosting.rollback` | Confirm. Deploys the newest healthy tag other than the current one |
| Start, stop, restart | `hosting.action` | Confirm |
| Forget an app | `hosting.delete` | Confirm. A RunPod pod keeps running until it is terminated on RunPod |

Deploy steps:

1. `hosting.get` to see the current tag and the last deployment.
2. `hosting.deploy` without confirm: read the dry run with the person.
3. `hosting.deploy` with `confirm=true`.
4. `hosting.get` again until the deployment is healthy or failed. A deploy fails after 15 minutes.

A RunPod pod costs money while it runs. Say so before you create or start one.

## An app's own tools

An app can name its MCP server in its manifest, such as an agent or its tracing. `hosting.mcp_tools` lists its tools and `hosting.mcp_call` calls one. You reach the app through this one connection, with no token of its own.

## Shared apps

`hosting.shared` lists the apps the deployment runs for every org, such as the password vault. `hosting.subscribe_shared` (confirm) subscribes the org and invites people by email.
