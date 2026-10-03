---
name: ls-scrapling
description: "Host-first Scrapling integration skill: plan or run supported single-URL extraction through pipx, with Docker as an optional escape hatch and controlled adapter refresh."
metadata:
  version: "1.0"
---

# LocalSetup Scrapling skill

## Purpose

Provide a host-first interface to the Scrapling CLI for single-URL extraction, guided installation and upgrades, and controlled adapter refresh. As verified on 2026-09-03, this guidance is scoped to Scrapling 0.4.15. It is not runtime proof of a host installation.

## When to use this skill

- A task needs Scrapling-specific setup, status, or one URL extraction.
- A caller needs a host-first pipx plan or a Docker escape hatch.
- A caller needs the result and sibling status artifact at a known filesystem path.
- A maintainer needs to compare observed top-level and extraction help with the adapter state before proposing a refresh.

Use ls-web-scraping-patterns first for authorization, robots expectations, terms, API-first choices, bounded crawl scope, rate limits, privacy, and retention. This skill owns only Scrapling-specific execution mechanics.

## Capabilities

- Host-first management:
  - Report host and Docker daemon availability without running or pulling a Scrapling image.
  - Return concrete pipx installation or upgrade plans; execution requires explicit caller confirmation.
  - Keep pipx app discovery process-local and follow ls/docs/CLI_SKILLS_ENV.md.
- Single-URL extraction:
  - Run one supported extraction mode against one URL, optionally scoped by one CSS selector.
  - Use adaptive get then fetch behavior when no mode is chosen.
  - Write a sibling .status.json artifact with command, attempts, return code, and stderr.
- Filesystem job records:
  - Read, cancel, and list existing job records without inventing a CLI spider runner.
- Controlled adapter refresh:
  - Compare top-level and extraction help to the stored adapter state.
  - Write state and the packaged capability index only when the caller explicitly requests the non-dry-run operation.
- Docker escape hatch:
  - Use the configured official image only when the host route is not viable.
  - Mount only the extraction work directory; the image entrypoint receives extraction arguments directly.

## Rule ownership

This skill owns the Scrapling helper contract. ls/docs/scrapling-cheat-sheet.md is a public quick reference; host-versus-Docker selection, approval gates, helper verb signatures, adapter refresh, and status-artifact behavior live here.

- Prefer a user-level pipx plan on the host. Docker is optional, not an automatic fallback.
- Treat the packaged capability index as the helper contract. Keep it synchronized with the static builder; do not run a live refresh merely to rewrite it.
- Treat installation, upgrade, image pull, and any external extraction as consequential execution. Present the exact plan and obtain the required approval before running it.
- Keep ls-web-scraping-patterns as the policy owner for web access decisions.

## Agent-facing verbs

Agents normally use ls.tools.scrapling_helper.main:

- scrapling_status():
  - Return host environment type, availability, Docker daemon availability, host CLI health, and an availability marker in version; it never starts Scrapling in Docker.
- extract_url_simple(url, output_path, selector?, mode_hint?, use_docker?):
  - Extract one URL to the requested output path.
  - A mode hint must be one of get, post, put, delete, fetch, or stealthy-fetch.
  - Without a hint, try get once and then fetch once only when get returns non-zero.
  - Return the final mode, every attempt, output_path, status_path, and status_write.
- scrapling_job_status(job_id), scrapling_cancel_job(job_id), and scrapling_list_jobs(kind?):
  - Inspect, cancel, or list existing filesystem-backed records. These operations do not start a spider or other long-running process.
- refresh_adapters(dry_run?):
  - Parse top-level and extraction help, compare it to adapter state, and return a diff. The non-dry-run path writes adapter state and the packaged capability index.
- upgrade_scrapling(host?, dry_run?, auto_confirm?):
  - Return a host pipx or Docker image-pull plan unless explicit caller confirmation authorizes execution.
- scrapling_self_test(mode):
  - Run the helper's offline-first fixture check only after the caller has chosen to execute it.

The machine-readable index is ls/tools/scrapling_helper/scrapling_capabilities.json. The packaged verifier accepts an optional --capabilities path for isolated validation and rejects retired capability names or an unsupported spider CLI claim.

### Quick verbs table

| Verb | Category | Key parameters | Summary |
| --- | --- | --- | --- |
| scrapling_status | status and planning | none | Report host and Docker daemon availability; it does not run or pull a Scrapling image. |
| extract_url_simple | single URL | url, output_path, selector?, mode_hint?, use_docker? | Extract one URL with an exact supported mode or adaptive get then fetch behavior. |
| scrapling_job_status | filesystem jobs | job_id | Read one existing job record. |
| scrapling_cancel_job | filesystem jobs | job_id | Attempt to cancel one existing job record. |
| scrapling_list_jobs | filesystem jobs | kind? | List recorded jobs and parse errors. |
| refresh_adapters | adapter maintenance | dry_run? | Compare top-level and extraction help with stored state. |
| upgrade_scrapling | installation planning | host?, dry_run?, auto_confirm? | Plan a pipx upgrade or image pull; apply only after confirmation. |
| scrapling_self_test | verification | mode | Run the helper's chosen self-test mode after execution is authorized. |

## Supported single-URL extraction

The stored 0.4.15 upstream documentation lists these extraction commands:

~~~text
scrapling extract get <url> <output-path>
scrapling extract post <url> <output-path>
scrapling extract put <url> <output-path>
scrapling extract delete <url> <output-path>
scrapling extract fetch <url> <output-path>
scrapling extract stealthy-fetch <url> <output-path>
~~~

The helper preserves a conservative default: get first, then fetch only when the first command fails. Pass an explicit supported mode when a caller knows the required transport. The helper creates the parent directory, records each attempt, and writes a sibling .status.json so filesystem-only workflows can inspect success and failure details.

Spiders are Python classes started with .start(); they are outside this CLI-helper surface. Do not add a local spider command, capability, parser probe, or compatibility wrapper.

## Environment and installation behavior

The host is the primary runtime:

- Prefer an isolated user-level pipx installation with the required extras. If pipx is absent, return bootstrap plans for review.
- Follow ls/docs/CLI_SKILLS_ENV.md for process-local PATH augmentation, pipx plans, health checks, and status artifacts. Do not edit a shell profile or use a system-wide installation unless an explicit maintainer decision requires it.
- Only execute an install or upgrade after the caller has approved the exact command. A dry run is a plan, not authorization.
- Use Docker only when the host route is constrained or incompatible. The configured image receives the official extraction arguments directly, with a narrowly scoped work-directory mount.

Call scrapling_status before an authorized execution when current environment details matter.

### Example: guarded tmux-session handoff

Use ls-workflow-ops-tmux-session to pick and probe the managed session first. After that workflow has established the target session and any required approval, run this command from the repository checkout:

~~~bash
repo_root="$(git rev-parse --show-toplevel)"
session="<managed-session>"
"$repo_root/ls/tools/tmux_ops" run -t "$session" -- bash -c 'cd -- "$1" && exec python3 -c "$2"' bash "$repo_root" '
from pathlib import Path
from ls.tools.scrapling_helper import main

repo_root = Path.cwd()
output = repo_root / "scrapling_output" / "reddit-home.md"
result = main.extract_url_simple(
    "https://www.reddit.com/",
    output,
    selector=None,
    mode_hint=None,
    use_docker=False,
)
print(result.get("output_path"), result.get("status_path"))
'
~~~

The outer command resolves the repository root before dispatching, invokes the repository's tmux_ops wrapper by absolute path, passes that root explicitly to bash -c, and changes into it before importing ls or resolving the relative output location. The managed pane's inherited working directory is therefore irrelevant.

After the command returns, inspect the content path and its sibling status artifact. On failure, surface the recorded return code, attempt list, and stderr. If installation is required, ask for approval to run the exact ensure_available or upgrade plan; do not execute a plan implicitly.

## Adapter refresh and version updates

The adapter flow is intentionally narrow:

- Parse top-level help and extraction help only.
- Compare observed commands and flags with the stored AdapterState.
- Return a human-readable diff in dry-run mode.
- Write adapter state and the capability index only after the caller explicitly selects the non-dry-run action.

A refresh is not authorization to install Scrapling, pull an image, execute extraction, or broaden the helper surface. Validate any proposed upstream capability against tagged upstream documentation before changing the helper contract.

## Safety and web-access boundary

- Before any extraction, apply ls-web-scraping-patterns: verify authorization, terms, robots expectations, API-first alternatives, rate limits, bounded concurrency and retries, privacy, and retention.
- Treat URLs, selectors, and output paths as untrusted input. Do not expose secrets, sensitive query parameters, or extracted private data in logs or status artifacts.
- Keep public-content extraction narrow. This skill must not be repurposed for abusive traffic, credentialed access, or high-volume crawling.

## Evidence boundary

As recorded on 2026-09-03, PyPI and deps.dev identified Scrapling 0.4.15 as the default release, published on 2026-08-23 for Python 3.10 or later. Tagged upstream documentation supplied the six extraction commands above and the Python-class spider model. Those are documentation snapshots, not runtime validation.

Recorded advisory queries on that date returned no advisory affecting the named PyPI release from OSV, the GitHub Advisory Database, deps.dev, or PyPI. Package identity and CPE coverage remain incomplete; this does not authorize installation, upgrade, pinning, deployment, or a categorical safety claim. Any dependency action needs its own current advisory preflight and explicit authorization.

Primary references used for this stored snapshot:

- https://pypi.org/pypi/scrapling/0.4.15/json
- https://api.deps.dev/v3/systems/pypi/packages/scrapling/versions/0.4.15
- https://raw.githubusercontent.com/D4Vinci/Scrapling/v0.4.15/docs/cli/extract-commands.md
- https://raw.githubusercontent.com/D4Vinci/Scrapling/v0.4.15/docs/spiders/getting-started.md

## Integration with other skills and workflows

Use ls-web-scraping-patterns for web-access policy and this skill for Scrapling mechanics. Higher-level workflows may consume the content and status files, but must preserve the host-first, explicit-approval, and bounded-extraction decisions documented here. Prefer another engine when its documented constraints fit the task better.
