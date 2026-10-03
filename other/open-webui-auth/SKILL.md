---
name: open-webui-auth
description: Change Open WebUI authentication settings (enable/disable login requirement).
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [open-webui, auth, docker]
---

# Open WebUI Authentication Management

Change Open WebUI authentication settings (enable/disable login requirement).

## Disable Authentication (no login required)

1. **Inspect existing container** to capture original configuration:

   ```bash
   docker inspect open-webui --format '{{json .Config}}'
   docker inspect open-webui --format '{{json .HostConfig}}'
   ```

   Note: `Cmd`/`Entrypoint`, `NetworkMode`, `Binds`/`Volumes`, `RestartPolicy`.

2. **Stop and remove** the existing container:

   ```bash
   docker stop open-webui && docker rm open-webui
   ```

3. **Recreate with `WEBUI_AUTH=False`** and the same config:

   ```bash
   docker run -d --name open-webui \
     --network host \
     -v open-webui:/app/backend/data \
     --restart always \
     -e WEBUI_AUTH=False \
     -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
     -e PORT=8080 \
     ghcr.io/open-webui/open-webui:main \
     bash start.sh
   ```

4. **Verify** auth is disabled:

   ```bash
   curl -s http://localhost:8080/api/config | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['features']['auth'])"
   ```

   Should output `true`.

## Enable Authentication (require login)

Recreate the container **without** the `WEBUI_AUTH=False` flag (or set it to `True`).

## Key environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WEBUI_AUTH` | `True` | `False` disables all auth (anyone can use it) |
| `WEBUI_SECRET_KEY` | auto-generated | Session signing key; set to persist across restarts |
| `OLLAMA_BASE_URL` | (none) | URL to your Ollama instance |

## Notes

- The container must be fully removed (`docker rm`) before recreating — Docker won't allow two containers with the same name.
- If the container uses `--network host`, the web UI binds directly to the host port.
- Data persists in the Docker volume `open-webui` mounted at `/app/backend/data`.
