---
name: reduce-relie-basics
description: Run REDUCE in Docker for this repo (using lunacamp/reduce-algebra), load the vendored ReLie file from resources/relie-src/relie.red, and perform a tiny smoke test. Use when you need the canonical docker run command or a minimal ReLie bootstrap.
---

# REDUCE + ReLie basics

## Ensure Docker is running

- Check the CLI is available: `docker --version`.
- Check the daemon is reachable: `docker info`.
- If the daemon is not available, start Docker Desktop (macOS: `open -a Docker`) and wait until `docker info` succeeds.
  - Example wait loop:
    ```bash
    for i in {1..60}; do docker info >/dev/null 2>&1 && break; sleep 1; done
    ```
- If you use Colima instead of Docker Desktop, start it with `colima start` and then re-check `docker info`.
- If you see `permission denied while trying to connect to the docker API at unix:///.../docker.sock`, rerun the command with elevated permissions or fix your socket access.
  - In Codex CLI with sandboxing, rerun the docker command with escalated permissions so it can reach the socket.

## Use local ReLie source

Use the vendored ReLie file in this repo:

`resources/relie-src/relie.red`

## Run REDUCE in Docker (repo mounted)

Use this canonical command from the repo root:

```bash
docker run --rm -it --platform linux/amd64 \
  -v "$PWD":/workspace -w /workspace \
  --entrypoint /usr/lib/reduce/cslbuild/csl/reduce \
  lunacamp/reduce-algebra
```

Notes:
- On Apple Silicon, keep `--platform linux/amd64`.
- If `docker` is not in PATH, use its full path.

## Load ReLie and run a tiny smoke test

In the REDUCE prompt:

```reduce
in "resources/relie-src/relie.red"$

% Tiny smoke test: confirm the REPL responds after load.
1+1;
```

Exit with `bye;` when done.

## Optional: run a tiny ReLie pipeline test (heat equation)

This mirrors a full run without interactive typing:

```bash
docker run --rm -i --platform linux/amd64 \
  -v "$PWD":/workspace -w /workspace \
  --entrypoint /usr/lib/reduce/cslbuild/csl/reduce \
  lunacamp/reduce-algebra <<'EOF'

in "resources/relie-src/relie.red"$

jetorder := 2$
xvar := {t,x}$
uvar := {u}$
diffeqs := {u_t - u_xx}$
leadders := {u_xx}$

relie(4)$
reliegen(1,{})$

symmetries;
generators;
bye;
EOF
```

If you present results to a user, summarize them in natural language (see `reduce-relie-lie-symmetries`).
