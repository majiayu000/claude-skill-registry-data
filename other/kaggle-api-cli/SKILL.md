---
name: kaggle-api-cli
description: Use when using Kaggle programmatically through the official kaggle CLI, kagglehub Python library, public API OAuth tokens, dataset/competition/model/notebook commands, or Kaggle authentication setup.
tags:
  - kaggle
  - datasets
  - competitions
  - cli
  - kagglehub
  - oauth
version: 1
---

# Kaggle API / CLI / kagglehub

## Scope
Use for Kaggle official programmatic access:
- `kaggle` CLI: competitions, datasets, kernels/notebooks, models, config.
- `kagglehub` Python library: download/load/upload datasets, models, competitions, notebook outputs.
- Kaggle Public API OAuth 2.0 provider: access tokens, refresh tokens, scopes.

Official sources read:
- `https://www.kaggle.com/docs/api`
- `https://github.com/Kaggle/kaggle-api/blob/main/docs/README.md`
- `https://github.com/Kaggle/kaggle-api/tree/main/docs`
- `https://github.com/Kaggle/kagglehub/blob/main/README.md`

## First Checks
```bash
command -v kaggle
kaggle --version
kaggle --help
python3 - <<'PY'
import importlib.util
print('kagglehub', bool(importlib.util.find_spec('kagglehub')))
PY
```

Important pitfall: Kaggle docs on GitHub `main` may be ahead of the PyPI CLI currently installed. If docs mention `kaggle auth`, `forums`, or `benchmarks` but `kaggle --help` does not show them, trust the live CLI for execution and use docs as forward reference.

## Install
Prefer isolated install on user machines:
```bash
python3 -m pip install --user kaggle
# or, if pipx is healthy:
pipx install kaggle
```
If `pipx` fails because its shared venv points at a broken Python, use a dedicated venv:
```bash
python3 -m venv ~/.local/venvs/kaggle-cli
~/.local/venvs/kaggle-cli/bin/python -m pip install -U pip kaggle
mkdir -p ~/.local/bin
ln -sf ~/.local/venvs/kaggle-cli/bin/kaggle ~/.local/bin/kaggle
```

For Python workflows:
```bash
python3 -m pip install kagglehub
```

## Authentication
Official docs list these auth methods:
1. OAuth CLI login: `kaggle auth login` if supported by the installed CLI.
2. API token env var: `export KAGGLE_API_TOKEN=***` if supported.
3. API token file: `~/.kaggle/access_token` if supported.
4. Legacy credentials: `~/.kaggle/kaggle.json` with JSON keys `username` and `key`.

Most reliable legacy setup:
```bash
mkdir -p ~/.kaggle
chmod 700 ~/.kaggle
# write ~/.kaggle/kaggle.json as: {"username":"...","key":"..."}
chmod 600 ~/.kaggle/kaggle.json
```

Verify without leaking secrets:
```bash
stat -f '%A %N' ~/.kaggle/kaggle.json 2>/dev/null || stat -c '%a %n' ~/.kaggle/kaggle.json
kaggle config view 2>&1 | sed -E 's/(key|token|password).*/\1: ***/Ig'
```

If `kaggle datasets download` raises `KeyError: 'username'`, the legacy JSON is missing `username` or the installed CLI does not understand the token-only auth method.

## Dataset Commands
Find/list:
```bash
kaggle datasets list -s iris
kaggle datasets list --file-type csv --sort-by updated --page 2
kaggle datasets files owner/dataset-slug
```

Download:
```bash
kaggle datasets download owner/dataset-slug
kaggle datasets download owner/dataset-slug --unzip -p ./data
kaggle datasets download owner/dataset-slug -f file.csv -p ./data -o
```
Flags: `-p/--path`, `--unzip`, `-f/--file-name`, `-o/--force`, `-q/--quiet`, `-w/--wp`.

Create/update:
```bash
kaggle datasets init -p ./dataset
# edit dataset-metadata.json: title, id/slug, licenses
kaggle datasets create -p ./dataset --public
kaggle datasets version -p ./dataset -m "update notes"
kaggle datasets metadata owner/dataset-slug -p ./dataset
kaggle datasets status owner/dataset-slug
```
Use delete only when explicitly requested:
```bash
kaggle datasets delete owner/dataset-slug --yes
```

## Competition Commands
```bash
kaggle competitions list --group general --category featured
kaggle competitions files titanic
kaggle competitions download titanic -p ./titanic
kaggle competitions submit titanic -f submission.csv -m "message"
kaggle competitions submissions titanic
kaggle competitions leaderboard titanic -d -p ./leaderboard
```
Code competition submit form:
```bash
kaggle competitions submit <competition> -k <username>/<kernel-slug> -f <output-file> -v <kernel-version> -m "message"
```

## Kernels / Notebooks
```bash
kaggle kernels list -s search-term
kaggle kernels files owner/kernel-slug
kaggle kernels init -p ./kernel
kaggle kernels pull owner/kernel-slug -p ./kernel -m
kaggle kernels push -p ./kernel
kaggle kernels output owner/kernel-slug -p ./output
kaggle kernels status owner/kernel-slug
```
Delete requires explicit user intent:
```bash
kaggle kernels delete owner/kernel-slug --yes
```

## Models
Current/legacy CLI commonly uses `models instances` rather than docs `models variations`:
```bash
kaggle models list -s gemini
kaggle models init -p ./model
kaggle models create -p ./model
kaggle models get owner/model-slug -p ./model
kaggle models update -p ./model
kaggle models instances files owner/model/framework/variation
kaggle models instances versions download owner/model/framework/variation/1 -p ./model --untar
```
Check `kaggle models --help` before using docs examples.

## kagglehub Python
Download dataset:
```python
import kagglehub
path = kagglehub.dataset_download('owner/dataset-slug')
print(path)
```

Load dataset directly:
```python
import kagglehub
from kagglehub import KaggleDatasetAdapter

df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    'owner/dataset-slug',
    'file.csv',
)
```
Supported adapters in docs: `PANDAS`, `HUGGING_FACE`, `POLARS`. It can also download models, competitions, notebook outputs, install utility scripts, and upload datasets/models.

Cache defaults to a local Kaggle cache outside Kaggle notebooks. Change it with:
```bash
export KAGGLEHUB_CACHE=./.kagglehub-cache
```

## OAuth 2.0 Public API
Kaggle supports Authorization Code with PKCE.

Discovery:
```bash
python3 - <<'PY'
import urllib.request
for u in [
 'https://www.kaggle.com/.well-known/oauth-authorization-server',
 'https://www.kaggle.com/.well-known/oauth-protected-resource',
]:
 print(u)
 print(urllib.request.urlopen(u, timeout=20).read().decode()[:1000])
PY
```

Endpoints:
- authorize: `GET https://www.kaggle.com/api/v1/oauth2/authorize`
- token: `POST https://www.kaggle.com/api/v1/oauth2/token`
- introspect: `POST https://www.kaggle.com/api/v1/oauth2/introspect`

Public clients require PKCE `code_verifier` / `code_challenge` and no auth header. Organization clients use client id `org:<slug>`, HTTP Basic auth with org owner's Kaggle API key, HTTPS redirect URIs, and no PKCE.

Tokens:
- access token prefix: `KGAT_...`
- refresh token prefix: `KGRT_...`
- access token expiry: 3 hours
- use `Authorization: Bearer KGAT_...` for API calls

Security rules:
- validate OAuth `state`
- request minimal scopes
- store refresh tokens securely
- never expose organization owner's API key client-side

Common scopes:
- `datasets.get:*`, `datasets.update:*`
- `models.get:*`, `models.create:*`, `models.update:*`
- `kernels.get:*`, `kernels.update:*`
- `competitions.get:*`, `competitions.submit:*`
- role scopes: `datasets.viewer:*`, `datasets.editor:*`, `models.viewer:*`, `kernels.editor:*`, `resources.viewer:*`

## Rate Limits
Kaggle uses dynamic rate limiting for both website and public API calls. On HTTP 429 / `Too many requests`:
1. pause and retry after minutes, preferably with exponential backoff;
2. inspect loops/retries for accidental request storms;
3. reduce pagination and redundant polling;
4. report platform-side bugs only after local logic is ruled out.

## Safe Defaults
- Do not print `KGAT_`, `KGRT_`, `KAGGLE_API_TOKEN`, or `key` values.
- Redact credentials in logs with `sed -E 's/(KGAT_|KGRT_)[A-Za-z0-9_\-]+/\1***/g'`.
- Confirm before destructive operations: dataset/model/kernel/version delete, competition submit, benchmark push/run if it spends quota.
- Prefer `--unzip -p <dir>` for dataset downloads to avoid dumping files into cwd.
- Always verify artifact paths after download:
```bash
find ./data -maxdepth 2 -type f | sort | head -50
```
