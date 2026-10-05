---
name: project-management
description: >
  Autonomous work execution across all Swarm projects. Reads last session summary,
  picks highest-priority work, executes it, then loops to the next item. Only stops
  when blocked on the operator or nothing remains. Trigger on: "what's the status", "project
  status", "what needs work", "prioritize", "what's next", "plan work", "coordinate",
  "which projects", "phase status", "roadmap", "backlog", "session start", "session end",
  "wrap up", "what should I work on", "keep going", "crank it out", or any request to
  understand or organize work across multiple Swarm heads.
---

# Project Management — Autonomous Execution Loop

Work continuously across all Swarm projects. **Do not stop to ask permission.**
Execute the highest-priority item, commit, move to the next. Only stop when:

1. **Nothing left to do** — all actionable items complete
2. **Blocked on operator** — needs credentials, physical access, review, or a decision
3. **Operator says stop** — explicit instruction to halt

---

## Startup (fast — under 60 seconds)

### 1. Read Last Session Summary
```bash
ls -t /opt/swarm/artifacts/summaries/*.yaml | head -1 | xargs cat
```
This is the source of truth. It tells you what was done, what's blocked, and
`context_for_next`. **Do NOT rediscover project state from scratch.**

### 2. Quick Status (parallel)
```bash
python3 <coordination-tool-root>/src/swarm_cli.py status
python3 <coordination-tool-root>/src/swarm_cli.py inbox
ls /opt/swarm/tasks/pending/task-*.yaml 2>/dev/null
```

### 3. Targeted Checks
Only check repos/services mentioned in `context_for_next`. Skip everything else.

### 4. Build Work Queue
Apply Priority Framework. Build an ordered list of actionable items.
Separate into two lists:
- **ACTIONABLE** — can do right now, no blockers
- **BLOCKED** — needs operator, hardware, credentials, etc.

Start executing immediately. Don't pause to report the queue — the operator will see progress in commits and status lines.

---

## Work Loop

```
WHILE actionable_items remain:
    1. Pick highest-priority ACTIONABLE item
    2. Execute it (write code, run tests, commit, push)
    3. After completing each item:
       a. Commit with meaningful message
       b. Run tests if applicable
       c. Update the project registry if phase changed
       d. Brief status line to operator (1 sentence)
    4. Re-evaluate: did this unblock anything? Add to queue.
    5. Continue to next item

WHEN all actionable items done OR blocked:
    → Run Session End Protocol
    → Report blocked items to operator
```

### Work Loop Rules
- **Commit after every meaningful unit of work.** Don't batch up.
- **Run tests before moving on** from any project that has them.
- **Pre-flight batch operations**: check target schema first, test on 1 record, verify full pipeline, then scale.
- **Verify before editing specs**: SSH to the machine (`nvidia-smi`, `lscpu`, `free -h`) before changing hardware claims.
- **If a task takes >30 min and you haven't updated the operator**, give a brief status line.
- **If you hit an unexpected blocker**, log it and move to the next item. Don't spin.
- **Use subagents for parallel work** when items are independent (e.g., tests on <gpu-host>
  while writing code on <primary-host>).
- **Use <gpu-host> for speed** — SSH to <gpu-host> for test execution, heavy builds, anything CPU-bound.
- **Never ask "want me to do X?"** — if it's non-breaking and moves forward, just do it.

---

## Session End Protocol

Execute when all work is done or all remaining items are blocked.

### 1. Uncommitted Work Check
```bash
for dir in <repo-path>/e <repo-path>/f <repo-path>/g <repo-path>/h \
           <repo-path>/i <repo-path>/j /opt/projects/main <repo-path>/b \
           <coordination-tool-root> <repo-path>/a <repo-path>/c <repo-path>/d \
           <repo-path>/k; do
  if [ -d "$dir/.git" ]; then
    changes=$(git -C "$dir" status --porcelain 2>/dev/null | wc -l)
    if [ "$changes" -gt 0 ]; then
      echo "UNCOMMITTED: $dir ($changes files)"
    fi
  fi
done
```
Commit everything. Don't leave dirty repos.

### 2. Generate Session Summary
Write to `/opt/swarm/artifacts/summaries/<hostname>-<timestamp>.yaml`:
```yaml
hostname: <hostname>
session_id: <session>
timestamp: <now>
project: <primary project worked on>
duration_minutes: <estimate>
key_decisions:
  - <decision 1>
files_changed:
  - <file 1>
issues_found:
  - <issue if any>
artifacts_produced:
  - <artifact if any>
context_for_next: "<explicit handoff — what to pick up, what's blocked, what changed>"
```
The `context_for_next` field is the most important. Be specific.

### 3. Skill & Config Sync
ALWAYS run — catches skill edits, script changes, hook updates:
```bash
cd /opt/claude-configs/claude-config && ./scripts/collect.sh
git -C /opt/claude-configs/claude-config add -A
git -C /opt/claude-configs/claude-config diff --cached --stat
git -C /opt/claude-configs/claude-config commit -m "sync: updates from $(hostname) session" || true
git -C /opt/claude-configs/claude-config push || true
```
This is NOT optional. Every session end must sync claude-config.

### 4. Final Report
Tell the operator:
- What was completed
- What's blocked and why
- What the next session should pick up

---

## Priority Framework

### Tier 1: Revenue & Active Delivery
| Priority | Criteria | Current Projects |
|---|---|---|
| P0 | Revenue-generating, user-facing, deadline | <your-project> |
| P1 | Revenue potential, actively building | ClauseHound, Audit Sentinel |

### Tier 2: Infrastructure & Dependencies
| Priority | Criteria | Current Projects |
|---|---|---|
| P2 | Unblocks other projects | hydra-swarm, AI Server |
| P3 | Operational stability | <internal-project-1>, fleet hardening |

### Tier 3: Growth & Future
| Priority | Criteria | Current Projects |
|---|---|---|
| P4 | Phase 0 scaffolding | DocuMint, <internal-project-3>, <internal-project-4> |
| P5 | Research & exploration | Prompt Forge, Hashrate Hedger |

### Tiebreaker Rules
1. Revenue potential breaks ties between same-tier items.
2. "What unblocks the most?" breaks ties between infrastructure items.
3. Resource fit: GPU work only when <gpu-host> is available; CPU/web work anytime on <primary-host>.
4. Quick wins (<30 min) get a +1 tier bump if they close out a phase.
5. Security hardening before feature work, always.

---

## Decision Trees

### "<gpu-host> is offline"
```
Available on <primary-host> alone:
- <internal-project-1> maintenance (fullnode, P2Pool, monitoring)
- <your-project> development (CPU-only)
- Audit Sentinel development (SQLite, no GPU needed)
- ClauseHound development (CPU-only)
- Prompt Forge development (CPU-only)
- hydra-swarm development
- Fleet hardening (Ansible roles)
- Documentation, planning, PRDs

Available on <worker-host> (if <gpu-host> down):
- Ollama inference via phi4:14b or qwen3:8b (RTX 5060 Ti)
- ComfyUI workflows (http://<worker-host-ip>:<comfyui-port>)
- <your-project> QA review (phi4 on <worker-host> Ollama)

NOT available without <gpu-host>:
- <internal-project-2> (needs ChromaDB + Ollama on <gpu-host>)
- AI Server stack management (Swarm manager)
- Docker Swarm control plane operations
- Milvus-dependent <internal-project-4> work
```

### "Project at phase boundary"
```
1. Run verification for current phase (tests, health checks).
2. Update project registry (phase field in this skill + project CLAUDE.md).
3. Check plans/<project>/plan.md for next phase requirements.
4. If next phase needs different resources, create swarm task for appropriate host.
5. Continue to next work item — don't stop.
```

### "New task from operator mid-session"
```
1. If operator gives explicit work → do it immediately, it's highest priority.
2. After completing it, resume the work queue where you left off.
```

---

## Project Registry

| Head | Project | Location | Phase | Status | Host |
|---|---|---|---|---|---|
| #1 | <internal-project-2> | <repo-path>/a | 3+ | Active, v1 production, v3 degenerate | <gpu-host> |
| #2 | <internal-project-1> | <repo-path>/b | Production | Hardened, public repo | <primary-host> |
| #3 | <internal-project-3> | <repo-path>/c | 1 | Scaffolded (58 tests) | <gpu-host> |
| -- | <internal-project-4> | <repo-path>/d | 2 | Form gen + PDF (204 tests) | <gpu-host> |
| -- | AI Server | /opt/projects/infra | Production | Docker Swarm v6.0.3, <worker-host> worker | <gpu-host>+<worker-host> |
| #4 | Audit Sentinel | <repo-path>/f | M7 | Security hardened (201 tests) | <primary-host>+<gpu-host> |
| #5 | Hashrate Hedger | <repo-path>/i | H6 | Live dashboard (158 tests), needs <mining-host> | <primary-host> |
| #6 | ClauseHound | <repo-path>/g | C7 | Security hardened (165 tests) | <primary-host>+<gpu-host> |
| #7 | Prompt Forge | <repo-path>/h | P6 | Security hardened (163 tests) | <primary-host> |
| #8 | DocuMint | <repo-path>/j | D6 | Cross-document validation (326 tests) | <primary-host> |
| #9 | ProjectK | <repo-path>/k | 1 | Built (98 tests), needs Firewalla + JWT | <primary-host> |
| #10 | Swarm Media | <repo-path>/l | M4 | ffmpeg assembly (155 tests) | <primary-host> |
| -- | <your-project> | <repo-path>/e | E5 | 1,112 CPA questions, 6 sections (299 tests) | <gpu-host> |
| -- | hydra-swarm | <coordination-tool-root> | 5 | Operational maturity (627 tests) | <primary-host> |

## Fleet Resource Map

| Host | CPU | GPU | Available For |
|---|---|---|---|
| <primary-host> | i5-8500 (6c, light load) | none | Fullnode, web services, CLI tools, orchestration |
| <gpu-host> | EPYC 7V12 (64c) | RTX 5080 16GB | LLM inference, Docker Swarm, <internal-project-2>, GPU workloads |
| <mining-host> | Ryzen 9600X (6c) | none | XMRig mining (offline, pending Ubuntu) |
| <worker-host-2> | TBD | TBD | Future |
| <worker-host> | EPYC 7443P (24c/48t) | RTX 5060 Ti 16GB | Swarm worker, Ollama, ComfyUI, inference |

## Phase Tracking Convention

Each project uses its own phase prefix:
- M1, M2... (Audit Sentinel milestones)
- H1, H2... (Hashrate Hedger)
- C1, C2... (ClauseHound)
- P1, P2... (Prompt Forge)
- D1, D2... (DocuMint)
- E1, E2... (<your-project>)

Plans live in `<project>/plans/` as markdown files.

## Coordination Rules

- Check swarm status before starting work on any shared project.
- Don't work on the same project another instance is actively editing.
- Use git worktrees for parallel work on the same repo.
- Commit frequently — other instances pull your changes.

## Repos (19)

| Visibility | Repos |
|---|---|
| Public (3) | monero-farm, shared-claude-skills, hydra-swarm-public |
| Private (16) | swarm-project, claude-config, hydra-swarm, claude-to-cursor, examforge, prompt-forge, hashrate-hedger, audit-sentinel, clausehound, documint, ai-project, project-a, project-c, project-d, solar-sentinel, swarm-media |
