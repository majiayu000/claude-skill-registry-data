---
name: cloudflare-containers
description: Deploy and manage Docker containers on Cloudflare's global network alongside Workers. Use when building applications that need to run Python code, process large files (multi-GB zips, video transcoding), execute CLI tools, run AI inference, create code sandboxes, or any workload requiring more memory/CPU than Workers provide. Triggers include requests to run containers, execute arbitrary code, process large files, deploy backend services in Python/Go/Rust, or integrate heavyweight compute with Workers.
---

# Cloudflare Containers

Run containers globally with on-demand scaling, controlled by Workers code.

## When to Use Containers vs Workers

| Use Case                          | Solution                   |
| --------------------------------- | -------------------------- |
| Lightweight API, JS/TS logic      | Worker                     |
| Python/Go/Rust backend            | Container                  |
| Large file processing (multi-GB)  | Container                  |
| AI inference, ML models           | Container                  |
| Code sandbox execution            | Container (or Sandbox SDK) |
| CLI tools (FFmpeg, zip utilities) | Container                  |

## Quick Start

```bash
npm create cloudflare@latest -- --template=cloudflare/templates/containers-template
npx wrangler deploy
```

First deploy takes 2-3 minutes for container provisioning. Check status:

```bash
npx wrangler containers list
```

## Project Structure

```
my-container-app/
├── src/
│   └── index.ts          # Worker entry point
├── container/
│   ├── Dockerfile        # Container image definition
│   └── app/              # Container application code
└── wrangler.jsonc        # Configuration
```

## Configuration (wrangler.jsonc)

```jsonc
{
  "name": "my-container-app",
  "main": "src/index.ts",
  "compatibility_date": "2025-11-14",
  "containers": [
    {
      "class_name": "MyContainer",
      "image": "./container/Dockerfile",
      "max_instances": 10,
      "instance_type": "standard-1", // See instance types below
    },
  ],
  "durable_objects": {
    "bindings": [{ "class_name": "MyContainer", "name": "MY_CONTAINER" }],
  },
  "migrations": [{ "new_sqlite_classes": ["MyContainer"], "tag": "v1" }],
}
```

## Instance Types

| Type       | vCPU | Memory  | Disk  | Use Case         |
| ---------- | ---- | ------- | ----- | ---------------- |
| lite       | 1/16 | 256 MiB | 2 GB  | Dev/testing      |
| basic      | 1/4  | 1 GiB   | 4 GB  | Light workloads  |
| standard-1 | 1/2  | 4 GiB   | 8 GB  | General purpose  |
| standard-2 | 1    | 6 GiB   | 12 GB | Memory-intensive |
| standard-3 | 2    | 8 GiB   | 16 GB | CPU-intensive    |
| standard-4 | 4    | 12 GiB  | 20 GB | Heavy workloads  |

For multi-GB file processing, use `standard-2` or higher.

## Worker Code Pattern

```typescript
import { Container, getContainer } from '@cloudflare/containers';

export class MyContainer extends Container {
  defaultPort = 8000; // Container's listening port
  sleepAfter = '10m'; // Auto-sleep after idle
  envVars = {
    // Environment variables
    MY_VAR: 'value',
  };

  override onStart() {
    console.log('Container started');
  }
  override onStop() {
    console.log('Container stopped');
  }
  override onError(error: unknown) {
    console.error('Error:', error);
  }
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // Route to specific container by ID (stateful)
    if (url.pathname.startsWith('/session/')) {
      const sessionId = url.pathname.split('/')[2];
      const container = getContainer(env.MY_CONTAINER, sessionId);
      return container.fetch(request);
    }

    // Load balance across containers (stateless)
    if (url.pathname === '/api') {
      const id = Math.floor(Math.random() * 5).toString();
      const container = getContainer(env.MY_CONTAINER, id);
      return container.fetch(request);
    }

    return new Response('Not found', { status: 404 });
  },
};
```

## Example: Python Code Executor

### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app
RUN pip install fastapi uvicorn

COPY app/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### container/app/main.py

```python
from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import os

app = FastAPI()

class CodeRequest(BaseModel):
    code: str

@app.post("/execute")
async def execute_code(req: CodeRequest):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(req.code)
        f.flush()
        try:
            result = subprocess.run(
                ['python', f.name],
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        finally:
            os.unlink(f.name)

@app.get("/health")
async def health():
    return {"status": "ok"}
```

### Worker calling Python executor

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method !== 'POST') {
      return new Response('POST /execute with {code: string}', { status: 400 });
    }

    const { code } = await request.json();
    const container = getContainer(env.CODE_EXECUTOR, 'shared');

    return container.fetch(
      new Request('http://container/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code }),
      })
    );
  },
};
```

## Example: Large File Processor (Multi-GB Zip)

### Dockerfile

```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y unzip && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN pip install fastapi uvicorn httpx

COPY app/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### container/app/main.py

```python
from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import zipfile
import tempfile
import os
from pathlib import Path

app = FastAPI()

class ProcessRequest(BaseModel):
    zip_url: str  # R2 presigned URL or public URL

@app.post("/process-zip")
async def process_zip(req: ProcessRequest):
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = Path(tmpdir) / "archive.zip"
        extract_dir = Path(tmpdir) / "extracted"

        # Stream download large file
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", req.zip_url) as response:
                with open(zip_path, "wb") as f:
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        f.write(chunk)

        # Extract and process
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(extract_dir)

        # Analyze contents
        files = []
        total_size = 0
        for path in extract_dir.rglob("*"):
            if path.is_file():
                size = path.stat().st_size
                files.append({"name": str(path.relative_to(extract_dir)), "size": size})
                total_size += size

        return {
            "file_count": len(files),
            "total_size_bytes": total_size,
            "files": files[:100]  # First 100 files
        }
```

Use `standard-2` or higher instance type for multi-GB files.

## Sandbox SDK (Simpler Code Execution)

For pure code execution without custom containers, use the Sandbox SDK:

```typescript
import { getSandbox, type Sandbox } from '@cloudflare/sandbox';

export { Sandbox } from '@cloudflare/sandbox';

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const sandbox = getSandbox(env.Sandbox, 'my-sandbox');

    // Execute Python
    const result = await sandbox.exec('python3 -c "print(2 + 2)"');

    // File operations
    await sandbox.writeFile('/workspace/data.txt', 'Hello');
    const file = await sandbox.readFile('/workspace/data.txt');

    return Response.json({ output: result.stdout });
  },
};
```

## Accessing R2 from Containers

Containers cannot directly access Worker bindings. Use one of these approaches:

### Option 1: R2's S3-compatible API

Pass R2 credentials as environment variables, then use any S3-compatible library:

```typescript
export class MyContainer extends Container {
  defaultPort = 8000;
  envVars = {
    AWS_ACCESS_KEY_ID: this.env.AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY: this.env.AWS_SECRET_ACCESS_KEY,
    R2_ENDPOINT: `https://${this.env.R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
    R2_BUCKET: this.env.R2_BUCKET_NAME,
  };
}
```

Python container using boto3:

```python
import boto3
import os

s3 = boto3.client(
    's3',
    endpoint_url=os.environ['R2_ENDPOINT'],
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
)

# Upload
s3.upload_file('/tmp/output.zip', os.environ['R2_BUCKET'], 'output.zip')

# Download
s3.download_file(os.environ['R2_BUCKET'], 'input.zip', '/tmp/input.zip')
```

### Option 2: Mount R2 with FUSE (Filesystem)

Mount R2 as a local filesystem using tigrisfs. Applications interact with R2 via standard file operations.

**Use cases**: Bootstrapping with assets, persisting state, large static files, editing files across instances.

**Dockerfile**:

```dockerfile
FROM alpine:3.20

# Install FUSE and tigrisfs
RUN apk update && apk add --no-cache ca-certificates fuse curl bash

RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then ARCH="amd64"; fi && \
    VERSION=$(curl -s https://api.github.com/repos/tigrisdata/tigrisfs/releases/latest | grep -o '"tag_name": "[^"]*' | cut -d'"' -f4) && \
    curl -L "https://github.com/tigrisdata/tigrisfs/releases/download/${VERSION}/tigrisfs_${VERSION#v}_linux_${ARCH}.tar.gz" -o /tmp/tigrisfs.tar.gz && \
    tar -xzf /tmp/tigrisfs.tar.gz -C /usr/local/bin/ && \
    rm /tmp/tigrisfs.tar.gz && chmod +x /usr/local/bin/tigrisfs

# Startup script that mounts bucket
RUN printf '#!/bin/sh\n\
set -e\n\
mkdir -p /mnt/r2\n\
R2_ENDPOINT="https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com"\n\
/usr/local/bin/tigrisfs --endpoint "${R2_ENDPOINT}" -f "${BUCKET_NAME}" /mnt/r2 &\n\
sleep 3\n\
exec "$@"\n\
' > /startup.sh && chmod +x /startup.sh

ENTRYPOINT ["/startup.sh"]
CMD ["your-app"]
```

**Worker configuration**:

```typescript
export class FUSEContainer extends Container<Env> {
  defaultPort = 8000;
  sleepAfter = '10m';
  envVars = {
    AWS_ACCESS_KEY_ID: this.env.AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY: this.env.AWS_SECRET_ACCESS_KEY,
    BUCKET_NAME: this.env.R2_BUCKET_NAME,
    R2_ACCOUNT_ID: this.env.R2_ACCOUNT_ID,
  };
}
```

**wrangler.jsonc** (store secrets via `wrangler secret put`):

```jsonc
{
  "vars": {
    "R2_BUCKET_NAME": "my-bucket",
    "R2_ACCOUNT_ID": "your-account-id",
  },
}
```

Files are accessible at `/mnt/r2/`. For read-only mount, add `-o ro` flag.

## Key Behaviors

- **Cold starts**: 2-3 seconds typically (depends on image size)
- **Ephemeral disk**: Disk resets on container restart
- **Auto-sleep**: Containers sleep after `sleepAfter` timeout
- **Scale to zero**: No charge when sleeping
- **Billing**: Per 10ms of active runtime
- **Architecture**: Must be `linux/amd64`
- **Shutdown**: SIGTERM sent, then SIGKILL after 15 minutes

## Pricing (Workers Paid - $5/month)

| Resource | Included     | Overage            |
| -------- | ------------ | ------------------ |
| Memory   | 25 GiB-hours | $0.0000025/GiB-sec |
| CPU      | 375 vCPU-min | $0.000020/vCPU-sec |
| Disk     | 200 GB-hours | $0.00000007/GB-sec |

## Limits (Open Beta)

| Limit             | Value   |
| ----------------- | ------- |
| Concurrent memory | 400 GiB |
| Concurrent vCPU   | 100     |
| Concurrent disk   | 2 TB    |

## Integrations

- **R2**: Access via S3 API with credentials or FUSE mount (see above)
- **D1**: Database access from Workers
- **Queues**: Trigger containers from queue messages
- **Workflows**: Orchestrate multi-step container tasks
- **Workers AI**: Combine with AI inference
