---
name: platform-server
description: Use to check or operate the server Platform runs on, with status, services, logs, restarts and named commands. Only the deployment's superadmin token has these tools.
---

# Server

These tools act on the whole deployment, not one org. Only a token that the superadmin made has them.

## Look

- `server.status`: CPU, memory, disk, database size and job queue.
- `server.services`: each container and host process with state, image, ports and domains.
- `server.logs`: the last lines of one service from `server.services`.
- `server.commands`: the named commands `server.run` can run.

## Act

| Tool | Scope | Notes |
| --- | --- | --- |
| `server.control` | `server:manage` | Confirm. Start, stop or restart a service the runner's policy lists |
| `server.run` | `server:manage` | Confirm. One named command, such as health or deploy. No arguments |
| `server.shell` | `server:manage` | Confirm. bash as the runner's unprivileged user, never root. Off unless the policy turns it on |

## Steps

1. Look first: `server.status`, `server.services`, then `server.logs` of the service.
2. Say what you found and what you will do.
3. Prefer `server.run` with a named command over `server.shell`.
4. A restart drops the service's open requests. A deploy changes what every org runs. Get the person's go first.
5. Check again after: `server.services` and `server.logs`.
