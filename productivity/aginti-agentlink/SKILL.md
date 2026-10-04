---
name: aginti-agentlink
description: Coordinate multiple agent sessions across machines, repos, tools, and runtimes using safe handoff packets, peer identity maps, private session mirrors, status probes, and action contracts. Use for AgentMesh-style collaboration, AgInTi agent collaboration, Codex-to-Codex handoff, board/workstation control, cross-repo orchestration, and preserving durable context without committing private logs.
---

# AgInTi AgentLink

Use this skill when two or more agent sessions must collaborate across hosts, repositories, devices, or tool environments.

Examples:

- Windows Codex controls Arduino while KV260 Codex records event-camera data.
- A board agent and workstation agent need to know each other's IPs, repos, scripts, and responsibilities.
- One agent has raw session history while another needs only safe operational context.
- AgInTi needs a reusable collaboration protocol between specialized subagents.

## Core Model

Treat each agent session as a node:

```text
agent node = identity + role + workspace + tools + reachability + constraints + current state
```

Treat collaboration as an explicit link:

```text
AgentLink = peer identity map + handoff packet + status probe + action contract + verification evidence
```

Do not rely on chat memory alone. Durable shared context must live in tracked docs, skills, or explicit private mirrors.

## Operating Rules

- Read local `AGENTS.md` first when present.
- Identify every peer agent before acting: hostname, IP, user, repo path, branch, role, reachable protocols.
- Prefer curated handoff docs and skills over raw session history.
- Mirror raw histories only into ignored private folders, never tracked Git.
- Summarize operational facts into tracked docs; do not paste full private logs.
- Before controlling hardware or services, verify real state with probes, not conversation claims.
- Use action contracts for cross-agent work: who owns which device, which commands are allowed, and what evidence closes the task.
- Commit and push durable docs/skills after updating shared memory, unless the repo policy says otherwise.

## Workflow

1. Build a peer map.
2. Read each peer's curated memory.
3. Probe live state.
4. If needed and permitted, fetch private session history into an ignored folder.
5. Extract only relevant operational facts.
6. Write or update handoff docs.
7. Create an action contract.
8. Execute only the part owned by the current agent.
9. Verify with evidence.
10. Sync durable updates back to shared repos or skill packs.

## Peer Map Template

```markdown
## AgentLink Peer Map

| Peer | Host | Address | User | Workspace | Role | Reachability |
| --- | --- | --- | --- | --- | --- | --- |
| windows-codex | CSG1175-P | 192.168.1.166 | Administrator | C:\Users\Administrator\Projects | Arduino and repo control | SSH/PowerShell/Git |
| kv260-codex | xilinx-kv260-starterkit-20222 | 192.168.1.250 | petalinux | /home/petalinux/Projects | Event-camera recording | SSH/HTTP API/Git |
```

## Handoff Packet Template

```markdown
# AgentLink Handoff

Updated: YYYY-MM-DD

## Objective

What the multi-agent system is trying to achieve.

## Peers

Hostnames, IPs, users, repo paths, branches, remotes, and responsibilities.

## Current State

What is actually true now, based on probes and files.

## Tools and APIs

Commands, scripts, API URLs, ports, device paths, and required auth assumptions.

## Ownership Boundaries

Which agent controls which machine, hardware, repo, service, or file.

## Action Contract

Next commands each agent may run, expected outputs, and stop conditions.

## Evidence

Commit hashes, API results, status output, file paths, recordings, screenshots, or logs.

## Private Context

Ignored local mirrors or session-history paths, with rules not to commit them.
```

## Memory Priority

Use this priority order:

1. Current files and live device/service state.
2. Tracked `AGENTS.md`, handoff docs, and skills.
3. Versioned helper scripts and API docs.
4. Private ignored mirrors.
5. Targeted raw session history reads.
6. Conversation memory.

Raw session history helps explain intent, but it is not ground truth.

## Privacy Rules

Never commit:

```text
private/
.agentlink/private/
*.history.jsonl
*.sqlite
auth.json
tokens
cookies
browser profiles
raw session dumps
```

If a raw history is needed, store it under an ignored folder and document only:

- source path;
- local private path;
- line/session counts;
- non-sensitive operational themes;
- commands for targeted search.

## References

Read `references/protocol.md` for the full AgentLink protocol, status probes, private mirror rules, and examples.

Use scripts when useful:

```bash
python3 scripts/agentlink_handoff.py --template
python3 scripts/agentlink_jsonl_summary.py path/to/history.jsonl --pattern "arduino|recording|api"
```

