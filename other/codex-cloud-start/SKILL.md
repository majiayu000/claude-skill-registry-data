---
name: codex-cloud-start
description: Start and health-check the agent-ebpf-filter Codex Cloud frontend or docs development services without elevated kernel privileges.
---

# Start skill

When a task needs an interactive UI, start only the required service from the repository root:

- `bash scripts/codex-cloud/maintain.sh doctor` first. If it fails, inspect `reports/codex-cloud/latest.md`; run `maintain.sh install` only when network and package permissions allow it.
- Frontend: `bash scripts/codex-cloud/start.sh frontend`. Verify `http://127.0.0.1:5173/`; change `CODEX_FRONTEND_PORT` if required.
- Documentation: `bash scripts/codex-cloud/start.sh docs`. Verify `http://127.0.0.1:5174/`.
- `bash scripts/codex-cloud/start.sh status` to inspect, `bash scripts/codex-cloud/start.sh stop` to stop recorded PIDs.
- After code changes, `bash scripts/codex-cloud/maintain.sh verify`; report its real pass/fail status and the saved log paths.

Never implicitly run `make dev`, `scripts/dev-backend.sh`, privileged containers, BPF LSM/cgroup enforcement, or kernel attach in Codex Cloud. Do not read `.env.dev` or inject production keys into the environment. The frontend proxies backend requests to localhost:8080; if no privileged backend is running, UI rendering can work but API-backed features are unavailable. State that limitation explicitly. Live eBPF tests require a separately authorized Linux/BTF host.
