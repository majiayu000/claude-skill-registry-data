---
name: bucketmanager-s3control-e2e
description: Rebuild and run the local bucketmanager final image, then execute the current S3Control bitmap-based end-to-end workflow for minimal validation or 300MB memory-peak tests. Use when testing local multi-s3gw S3Control parent/child jobs in this repository.
metadata:
  author: codex
  version: "1.0.0"
---

# Bucketmanager S3Control E2E

Use this skill when working in `/data/myproject/bucketmanager_tianjl-devel` and you need to rebuild the **current** local `bucketmanager` image, restart `bkt-mgr`, and validate the bitmap-based S3Control merge flow against the local `9000/9300` gateways.

## Known local topology

- Compose service: `bktmgr`
- Runtime container: `bkt-mgr`
- Bucketmanager HTTP: `http://127.0.0.1:9900`
- Data gateways: `9000`, `9300`
- Child S3Control gateways: `9010`, `9310`
- Local S3 credentials: `admin/admin`
- Internal bucket: `s3control-internal`
- Report bucket used in tests: `pool2`
- Test account id commonly observed in local runs: `fae6914e982811efad2ac85b766b7df7`

## Rebuild and restart

Always rebuild the **final** image. Do not rely on `make -C docker image`; that can produce the wrong target.

```bash
cd /data/myproject/bucketmanager_tianjl-devel
docker build --target final \
  --build-arg PIP_REG_FLAG='-i https://pypi.tuna.tsinghua.edu.cn/simple' \
  --build-arg DIST_VERSION='0.0.0.dev1' \
  --build-arg BUILD_DOCKER_REG='' \
  --build-arg BUILD_IMG='python:3.11' \
  --build-arg BASE_IMG='python:3.11-slim' \
  -t bucketmanager:latest \
  -f docker/Dockerfile .
docker rm -f bkt-mgr || true
docker compose up -d bktmgr
docker logs --tail 30 bkt-mgr
```

Healthy startup should show:

```text
Uvicorn running on http://0.0.0.0:9900
```

## Minimal bitmap E2E

Use this when validating current merge logic.

### 1. Prepare buckets and objects

- Clear `pool`, `pool2`, `s3control-internal` on both `9000` and `9300`.
- Put `pool/obj1` only on `9000`.
- Put `pool/obj2` only on `9300`.
- Do **not** create `pool/missing-obj`.
- Upload manifest on `9000`:

```csv
pool,obj1
pool,obj2
pool,missing-obj
```

### 2. Create parent job

Create a parent S3Control job through `bkt-mgr` with:

- `Manifest.Location.ObjectArn = arn:aws:s3:::pool/<manifest-key>`
- `Operation.S3InitiateRestoreObject.ExpirationInDays = 123`
- `Report.Bucket = arn:aws:s3:::pool2`
- `Report.Prefix = JobReport/RestoreReports`

Then discover child jobs on `9010` and `9310` and wait until both child jobs finish.

### 3. Inject simulated valid bitmap artifacts

Stop `bkt-mgr` before the parent completes final merge, then inject child artifacts:

- `9000` child bitmap content: `0b00000001`
- `9300` child bitmap content: `0b00000010`

Write them to:

```text
s3control-internal/reports/<account>/<parent>/job-<child>/valid.bitmap
```

Then patch each child report `manifest.json` to include:

```json
"ValidBitmaps": [
  {
    "Bucket": "s3control-internal",
    "Key": "reports/<account>/<parent>/job-<child>/valid.bitmap"
  }
]
```

Restart `bkt-mgr` after both child artifacts are in place.

Hard timing rule:

- The valid bitmap injection must finish before the parent job performs its **first** `Completing` merge.
- Treat this as a hard boundary, not a best-effort recommendation.
- If logs already show either:
  - `moving to Completing`
  - or `Processing job <parent> status Completing`
  then the manual bitmap injection window is already invalid for a clean test.
- In that case, discard the run and restart the test from a fresh parent job instead of continuing with late bitmap injection.

### 4. Validate final reports

Read from `pool2` under:

```text
JobReport/RestoreReports/<account>/<parent>/succeeded.csv
JobReport/RestoreReports/<account>/<parent>/failed.csv
```

Expected final shape:

```csv
pool,obj1,,successed,200,,""
pool,obj2,,successed,200,,""
```

```csv
pool,missing-obj,,failed,200,NoSuchKey,The specified key does not exist.
```

## 300MB memory-peak test

Use the same flow as the minimal test, but:

- create `obj1` and `obj2` as `300MB`
- keep the same manifest shape
- run a `docker stats` sampler during the job

Recommended sampler:

```bash
while true; do
  TS=$(date +%s.%N)
  docker stats --no-stream --format '{{.MemUsage}}' bkt-mgr 2>/dev/null | awk -v ts="$TS" '{print ts, $0}'
  sleep 0.1
done
```

Ignore `0B / 0B` samples from deliberate `bkt-mgr` stop/restart windows. The relevant peak is the highest non-zero `MiB` sample.

## Important constraints

- Current local testing still simulates `s3gw` bitmap generation by manual injection.
- Parent job completion can race with manual bitmap injection. Prefer stopping `bkt-mgr` immediately after child jobs are done and before the parent performs its first `Completing` merge.
- `/jobs/<id>` may return `403` without auth in this environment. If that happens, validate completion by:
  - `docker logs bkt-mgr`
  - checking final `pool2` reports directly on `9000`
- Final merged reports are currently written only to the **first** matching and reachable `s3gw` endpoint for the configured report bucket, not to every matching endpoint.
- Report success lines are copied from child `successed.csv`.
- Final `NoSuchKey` rows are generated by bucketmanager from manifest order and merged valid bitmap.
