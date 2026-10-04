---
name: openclaw-setup
description: Bootstrap OpenClaw in a project — install the orchestrator if missing, run project setup script (or `openclaw onboard`), configure gateway (bind mode, auth, UI), start Mission Control if compose exists, verify healthy. Loads when no OpenClaw deployment exists for a project, or when the operator says "set up OpenClaw", "install the orchestrator", "bootstrap the fleet", "wire up Mission Control".
argument-hint: [project-path, default cwd]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# openclaw-setup

The bootstrap skill that creates an OpenClaw deployment for a project from scratch. Distinct from `openclaw-add-agent` (adds to existing deployment) and `openclaw-health` (audits existing deployment) — this skill creates the deployment itself: gateway, Mission Control, supporting Docker services, initial config.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **No deployment exists**: project has no `openclaw status` output (command not found OR returns "no gateway"), no Mission Control on `:8000`, no `agent-tooling.yaml`.
- **Direct verb**: operator says "set up OpenClaw", "install the orchestrator", "bootstrap the fleet", "wire up Mission Control", "first OpenClaw run".
- **New sister project**: a fleet-class project (e.g., new `openfleet-*` instance) needs its own OpenClaw.

Do NOT load when:

- OpenClaw exists; you're adding agents — load `openclaw-add-agent`.
- OpenClaw exists; auditing health — load `openclaw-health`.
- Mission Control specifically needs reconnection (gateway up but MC connection lost) — load `openclaw-configure-mc`.
- Operator wants to scale an existing deployment to multi-host — load `evolve-scale`.

## Operations

This skill has 4 named operations. Execute in order. Each step verifies before proceeding.

### Operation 1: Pre-flight + install OpenClaw

**Trigger**: skill loaded; operator confirmed greenfield setup.

**Process**:

1. Pre-flight check:
   ```bash
   command -v openclaw && openclaw --version || echo "NOT INSTALLED"
   docker --version || echo "DOCKER MISSING"
   command -v claude && claude --version || echo "CLAUDE CLI MISSING"
   ```
   Capture: which prerequisites are present.
2. If OpenClaw not installed: install per the operator's tool of choice (npm / brew / source build per project README). Verify with `openclaw --version` again.
3. If Docker missing: STOP — operator must install Docker first (system-level, not in scope here).
4. If Claude CLI missing: STOP — OpenClaw orchestrates Claude Code instances; without CLI it can't run agents.
5. Pick the project path (`$ARGUMENTS` or cwd). Verify it's a git repo and has a clear identity (CLAUDE.md or README). If neither, ask operator if this really is the right path.

**Quality bar (Operation 1 done when)**:

- [ ] All 3 prerequisites verified or explicitly stopped-on.
- [ ] OpenClaw installed and `--version` returns successfully.
- [ ] Project path confirmed.
- [ ] No backed-up config overwritten silently — if existing OpenClaw config exists, back up first (rename to `.bak.<timestamp>`).

### Operation 2: Run project setup or onboard

**Trigger**: Operation 1 complete.

**Process**:

1. Look for project-specific setup:
   ```bash
   ls <project>/setup.sh <project>/scripts/openclaw-setup.sh 2>/dev/null
   ```
2. If a setup script exists: read it FIRST (don't run blind). Verify it's not destructive (no `rm -rf` outside its scope, no `chmod` on system paths). If it looks safe, run it; capture output.
3. If no setup script: run the OpenClaw default onboarding:
   ```bash
   cd <project>
   openclaw onboard --workspace . --no-interactive
   ```
   This creates `.openclaw/` config dir, registers the project as a workspace, and produces a default `agent-tooling.yaml` skeleton.
4. After either path: verify `.openclaw/` exists with the expected files (`config.yaml`, `agents/`, `gateway.log` after first start).
5. Check the resulting `agent-tooling.yaml` (or equivalent) — it should have at minimum: `agents:` block, `skills:` referenced, `mode_defaults:`. Empty or trivial configs need operator guidance to populate.

**Quality bar (Operation 2 done when)**:

- [ ] Setup or onboard ran to completion (exit 0).
- [ ] `.openclaw/` directory exists with expected structure.
- [ ] `agent-tooling.yaml` (or equivalent) is non-trivial — at least lists agent slots.
- [ ] Any setup-script output read; warnings/errors flagged to operator.

### Operation 3: Configure gateway + Mission Control

**Trigger**: Operation 2 complete.

**Process**:

1. Configure gateway via `openclaw config` (or edit `.openclaw/config.yaml`):
   - **bind mode**: `local` (default — only localhost can talk to gateway) or `bind` (network-exposed for multi-host fleets). Pick `local` unless operator confirms multi-host.
   - **auth**: enable token-auth for the control UI. Generate a token; store in `.env` (gitignored). Don't commit the token.
   - **control UI port**: default :7000 unless operator wants different.
2. If a Mission Control `docker-compose.yaml` exists in the project (typical for `openfleet/`):
   ```bash
   docker compose -f openfleet/mission-control/docker-compose.yaml up -d
   ```
   Wait up to 60s for MC to come up; verify with `curl -sS -m 5 http://localhost:8000/health`.
3. Wire MC ↔ Gateway: typically MC reads gateway URL from env (`OPENCLAW_GATEWAY_URL`). Set in MC's compose file or `.env`.
4. Some auth flows need interactive operator input (Claude Code login token, OAuth flow). DETECT this; pause and tell operator: *"Run `claude login` to authenticate before continuing."*

**Quality bar (Operation 3 done when)**:

- [ ] Gateway config has bind mode + auth + UI port set.
- [ ] Auth token in `.env`, gitignored, NOT committed.
- [ ] Mission Control running (if compose existed) and responding to `/health`.
- [ ] Any interactive auth surfaced to operator with clear instructions.

### Operation 4: Verify all components

**Trigger**: Operation 3 complete.

**Process**:

1. Verify gateway:
   ```bash
   openclaw status   # should report "running, version X.Y.Z"
   ```
2. Verify Mission Control (if applicable):
   ```bash
   curl -sS -m 5 http://localhost:8000/health   # 200 OK
   curl -sS -m 5 -o /dev/null -w "%{http_code}" http://localhost:3000   # 200 (frontend)
   ```
3. Verify Docker services:
   ```bash
   docker compose ps   # all "running (healthy)"
   ```
4. Verify the workspace is registered:
   ```bash
   openclaw agents list   # should be empty for now (no agents added yet) but command works
   ```
5. Suggest the next skill: `openclaw-add-agent` to register the first agent.

**Quality bar (Operation 4 done when)**:

- [ ] Gateway returns "running" with version.
- [ ] MC backend + frontend respond (or explicitly "MC not deployed, gateway-only" stated).
- [ ] Docker services all healthy (or "no docker services" if compose-less setup).
- [ ] Workspace registered.
- [ ] Operator told to load `openclaw-add-agent` next.

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Overwriting existing OpenClaw config

Operator runs setup again on a project that already has `.openclaw/`. The skill silently overwrites `config.yaml`, losing operator's custom auth tokens, agent registrations, queue state.

**The rule**: Operation 1 always checks for existing `.openclaw/` BEFORE running setup. If it exists, back up to `.openclaw.bak.<timestamp>/` first. Then proceed (or ask operator if they want to abort and audit existing instead — `openclaw-health`).

### Gotcha 2: Running setup.sh blind

Project's `setup.sh` is read by the skill and run without inspection. The script does `rm -rf $HOME/.config/openclaw/`, wiping operator's other-project credentials. Setup "succeeds" but operator's other deployments break.

**The rule**: read every setup script before running. Look for `rm -rf` / `chmod` / `sudo` / writes outside the project tree. If any of those, present the suspicious line(s) to the operator and ask before running. Trust no setup script that hasn't been reviewed.

### Gotcha 3: Auth token committed by accident

Operation 3 generates an auth token; skill writes it to `.openclaw/config.yaml` instead of `.env`. `config.yaml` is committed to git. Token is now in history.

**The rule**: secrets ONLY in `.env` (gitignored). Config files reference env-var names, not values. Verify with `git diff` after Operation 3 — no token literals.

### Gotcha 4: Gateway up but MC unreachable, declared healthy

`openclaw status` returns "running"; the skill marks setup successful. But MC compose hasn't started, MC backend isn't reachable, the operator can't see the board. Setup is technically complete; the system is not actually usable.

**The rule**: Operation 4 verifies BOTH gateway AND MC (if compose exists). One being healthy isn't enough; both must respond. If MC is "deferred" by design (gateway-only setup), state that explicitly.

### Gotcha 5: Skipping interactive auth detection

OpenClaw needs `claude login` (or equivalent) to dispatch agents. Skill runs setup, declares success. First time operator tries to add an agent, the agent fails to start because auth isn't done. Operator scratches head — "but setup said success!"

**The rule**: detect interactive-auth requirements during Operation 3 step 4. Surface them to the operator with EXACT command to run. Setup is "complete" only when interactive auth is also done — or explicitly noted as a follow-up step the operator must complete.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

## Domain context

This skill primarily targets the **OpenFleet** sister project (where OpenClaw runs). AICP itself doesn't run OpenClaw — it provides the inference + skills the orchestrated agents consume. Per [docs/architecture/fleet-integration.md](../../../docs/architecture/fleet-integration.md), the AICP↔OpenFleet split keeps the inference path off the orchestrator.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| openclaw-add-agent | Add agents to existing deployment | This skill creates the deployment first |
| openclaw-health | Audit an existing deployment | This skill creates; openclaw-health audits |
| openclaw-fleet-status | Operational snapshot | This skill is bootstrap; fleet-status is post-bootstrap operations |
| openclaw-configure-mc | Reconnect MC to existing gateway | Sub-task; this skill includes MC bootstrap as part of full setup |
| evolve-scale | Add a second host | Multi-host evolution; this skill is single-host bootstrap |
