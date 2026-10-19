---
name: ovstorage-contributor-run-integration-tests
description: Run, troubleshoot, or explain ovstorage's app-level integration suite locally. Use when choosing between hermetic and live-cloud targets, exercising the Rust/C++ or Python legs, configuring a credential mapper or pre-exported credentials, or checking that backend skips cannot produce a false-green result.
license: CC-BY-4.0
version: "0.1.0"
author: NVIDIA Omniverse
tags: [ovstorage, integration, testing, cloud, contributor]
tools: [Read, Bash]
compatibility: Requires an ovstorage checkout. Live fixtures require suitable backend credentials; the C++ leg requires Unix, CMake 3.16+, and a C++20 compiler.
---

# Run Integration Tests

## Ground the run

Read [`ovstorage-integration-tests/README.md`](../../ovstorage-integration-tests/README.md)
for the local workflow and its scenario, credential, and skip semantics.

Check `git status --short` before running anything. Do not print credentials or
copy internal fixture names into public-source files.

## Choose the target

Run both legs unless the request explicitly narrows the binding surface:

| Mode | Rust + C++ | Python |
|---|---|---|
| Local hermetic (`file`) | `make test-integration` | `make test-integration-python` |
| Emulator hermetic (`file,azure,gcs`) | start the fixtures, then `make INTEGRATION_HERMETIC_REQUIRE=file,azure,gcs test-integration` | start the fixtures, then `make INTEGRATION_HERMETIC_REQUIRE=file,azure,gcs test-integration-python` |
| Live cloud | `OVSTORAGE_HUGGINGFACE_REPO_ID=<public repo> OVSTORAGE_REQUIRE_LIVE_BACKENDS=azure,s3,huggingface make test-integration-live` | `OVSTORAGE_HUGGINGFACE_REPO_ID=<public repo> OVSTORAGE_REQUIRE_LIVE_BACKENDS=azure,s3,huggingface make test-integration-python-live` |

The ordinary hermetic targets require `file` and forbid live
`azure,s3,gcs,huggingface`.
For the emulator matrix, run `python tools/ovtasks/fake_gcs.py start` and
`python tools/ovtasks/azurite.py start`, then set
`OVSTORAGE_FAKE_GCS_ENDPOINT=http://127.0.0.1:4443` and
`OVSTORAGE_AZURITE_ENDPOINT=http://127.0.0.1:10000` on each Make invocation.
Those endpoint variables accept loopback IPs only and never consume ambient
live credentials. The live targets must carry
`OVSTORAGE_REQUIRE_LIVE_BACKENDS`; otherwise missing or rejected credentials
can turn every requested cloud backend into a skip.

## Authenticate live runs

Private staging checkouts may provide a credential mapper that is deliberately
excluded from the public source tree. Set `LIVE_ENV_SCRIPT=<path>` to let the
live Make targets source a trusted mapper in the test shell. If the complete
fixture and credential environment is already exported, set
`OVSTORAGE_LIVE_AUTO_ENV=0` instead.

Azure and S3 are the required CI-grade baseline. Native GCS uses an ADC file
from `gcloud auth application-default login` and remains optional unless the
request explicitly requires it. Treat a credential provider's authorization
error as an authentication failure, not evidence that a field is absent.

Hugging Face needs no credentials: exporting
`OVSTORAGE_HUGGINGFACE_REPO_ID=<public repo>` is what opts its read-only
scenarios in, and anonymous reads are the exercised path. When the required
list names only huggingface, the Make prelude skips the credential mapper on
its own; naming any `azure`/`s3`/`gcs` selector alongside brings it back. An
ambient `HF_TOKEN` is used if present and fails verification when stale rather
than falling back to anonymous.

CI runs the full emulator matrix on every PR. It also runs both live legs for
every same-repository PR targeting `main`, including drafts, gated by the
`cloud-live` environment. Fork PRs receive only the hermetic integration job
because GitHub withholds repository secrets from them.

## Interpret and report

- Confirm every required backend connected; do not summarize required-backend
  skips as success.
- Distinguish capability skips and stated C++ ABI limitations from failures.
- Report the Rust/C++ and Python results separately.
- When source changed, finish with
  [`ovstorage-contributor-verify-before-merge`](../ovstorage-contributor-verify-before-merge/SKILL.md).
