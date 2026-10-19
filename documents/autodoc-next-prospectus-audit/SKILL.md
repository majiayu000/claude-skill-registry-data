---
name: autodoc-next-prospectus-audit
description: Audit one local prospectus PDF, DOC, or DOCX through PDRouter and download the annotated document with AutoDoc NEXT2.0.
metadata:
  {
    'author': 'PAODINGAI',
    'version': '1.0.0',
    'openclaw':
      {
        'requires':
          {
            'env': ['PAODINGAI_API_KEY'],
            'bins': ['node'],
          },
      },
  }
---

# AutoDoc NEXT2.0

Run the JavaScript workflow that submits one local prospectus to the AutoDoc NEXT2.0 API through PDRouter
(`POST /openapi/autodoc-next/audits`), polls its JSON status, and downloads the annotated result in a
separate explicit command.

## Installation

```bash
npx skills add PaodingAI/skills
```

Configure the PDRouter client credentials before running the Skill:

```bash
export PAODINGAI_API_KEY="<your-pdrouter-api-key>"
export PAODINGAI_API_BASE_URL="https://platform.paodingai.com/"
```

## Usage

```bash
node skills/autodoc-next-prospectus-audit/scripts/audit_document.mjs start <local-file-path> [--max-wait-seconds <seconds>] [--json]
node skills/autodoc-next-prospectus-audit/scripts/audit_document.mjs watch <request_id> [--max-wait-seconds <seconds>] [--json]
node skills/autodoc-next-prospectus-audit/scripts/audit_document.mjs status <request_id> [--json]
node skills/autodoc-next-prospectus-audit/scripts/audit_document.mjs download <request_id> [--output-dir <dir>] [--json]
```

`start` validates and uploads the local file, then continuously polls until a terminal state. `watch`
continues polling an existing request after a local interruption. Neither command downloads a file.
`status` performs one foreground status query. Only `download` queries the terminal result and downloads
the annotated file after verifying its size and SHA-256. Return the `output_file` absolute path only from
the download command.

Use `watch <request_id>` after a client interruption or polling connection failure. Watch mode does not
read or upload the source document again and never downloads the result. Use `status <request_id>` when
the user wants a current status without starting a long-running watcher. Add `--max-wait-seconds <seconds>`
only when the user explicitly wants to limit a start/watch session.

Environment variables:

- `PAODINGAI_API_KEY`: Required. Bearer API key for PDRouter requests.
- `PAODINGAI_API_BASE_URL`: Optional. PDRouter origin URL, such as `https://platform.paodingai.com/`. Defaults to that production origin.
- `AUTODOC_MAX_WAIT_SECONDS`: Optional positive integer. Limits the current polling session only; no total waiting limit is applied by default.

The client uses `${PAODINGAI_API_BASE_URL%/}/openapi/autodoc-next/audits` for submission, `${PAODINGAI_API_BASE_URL%/}/openapi/autodoc-next/status` for polling, and `${PAODINGAI_API_BASE_URL%/}/openapi/autodoc-next/download` for result download.

`AUTODOC_OUTPUT_DIR` optionally changes the output directory. Treat authentication values as confidential.

## When to Use

- Use this Skill when the user asks to audit or review one local prospectus document.
- Supported input formats are PDF, DOC, and DOCX. Only one file is accepted per invocation.
- When the user asks to save the result beside the input, pass `--output-dir` with the input file's parent directory.
- The result is an annotated PDF for PDF input, or an annotated DOCX for DOC/DOCX input.

## Execution Constraints

- Run upload/polling and download through the separate commands in `scripts/audit_document.mjs`.
- Route submission, status polling, and result download through the script's `AutoDocNextClient`, which owns the PDRouter base URL, service prefix, authentication headers, and HTTP transport.
- The script performs local validation, submits one multipart request, polls the protected JSON status response,
  or performs an explicit protected result download with size and SHA-256 verification.
- Progress and diagnostics are written to stderr. User-facing diagnostics contain sanitized status and error information; API keys, JWTs, and request secrets remain confidential.
- Tool output is implementation detail, not the user-facing progress report. After each meaningful
  command, wait, or polling response, interpret the returned status instead of relaying a raw
  command output or an unprocessed stdout/stderr block.

## User-Visible Progress Reporting (Required)

The `start`/`watch` client runs as a host-managed background task. While the AI session is active,
inspect its output and send a short ordinary assistant message after each meaningful state change.
When the user asks for an update, run the foreground `status` command instead of assuming the task
is stuck or relying on buffered background output.

- Report these phases in order when applicable: local file validation, upload/submission, queued,
  auditing, audit completed/failed, explicit result download, and checksum verification.
- Each update must state the current phase and the concrete information available from the latest
  response, such as a sanitized service status, event/log text, processed item count, percentage,
  elapsed time, retry number, or the `request_id`. Do not invent a percentage, ETA, or internal
  detail that the tool or API did not return.
- When the service returns a new progress event, summarize that event in Chinese in one concise
  sentence. Preserve the event order, and do not repeat identical events.
- When polling returns no new event, do not emit repeated empty updates. After a meaningful
  interval, emit a heartbeat such as `审核仍在进行，当前状态：<status>，已等待约 <duration>` so
  the user knows the session is still actively tracking the task.
- Before every continued wait or poll, make the next action explicit, for example `审核尚未完成，
  将继续查询状态；当前 request_id：...`. This is a progress update, not a terminal response.
- When the audit reaches a terminal success, state that the audit is complete but the result has not
  been downloaded. After an explicit download, report the checksum result and absolute `output_file`
  path. On failure, state the terminal phase, sanitized reason, and retained `request_id`.
- Never present raw tool output, a process identifier, or `still running` alone as the progress
  report. Never claim the annotated file is available locally until the explicit download and its
  integrity checks pass.

## Script Behavior

1. Require `PAODINGAI_API_KEY` before execution.
2. Resolve `PAODINGAI_API_BASE_URL`, with `https://platform.paodingai.com` as the default.
3. Validate that the input is one regular, non-empty PDF, DOC, or DOCX file no larger than 100 MiB and that its content signature matches its extension.
4. Generate the audit `request_id` and send exactly one multipart request with a single `file` field to `POST /openapi/autodoc-next/audits`, using `Authorization: Bearer <token>` and `X-Request-Id: <audit request_id>`.
5. Keep that audit `request_id` and poll `GET /openapi/autodoc-next/status?request_id=<audit request_id>` until it reports `completed`/`succeeded` or a failure state. Each polling round uses a new `X-Request-Id`; retries of that same round reuse it. A returned `status_url` may override the path, but its `request_id` query parameter is always replaced with the audit request ID. Preserve response order and interpret every user-safe progress, event, and log item returned by the status endpoint. After each new item or meaningful status change, convert it into a concise Chinese assistant progress update; do not expose raw tool output. Suppress exact duplicate events and high-frequency heartbeat entries, while emitting one user-facing processing heartbeat every 30 seconds when no meaningful event arrives.
6. `status <request_id>` performs one status request and returns the current state and latest progress. It never downloads.
7. `download <request_id>` first confirms a successful terminal result, then sends a GET to `/openapi/autodoc-next/download?request_id=<audit request_id>` with a new download `X-Request-Id`, verifies the declared size and SHA-256, and atomically writes the final file. Any returned same-origin `download_url` is forced to use the audit request ID in its query.
8. If `--output-dir` is supplied to `download`, write the result there; otherwise use `AUTODOC_OUTPUT_DIR` or `./autodoc-results`. Preserve an existing same-name file and save the new result with a numbered suffix such as `document（1）.docx`.
9. Print stable JSON objects to stdout and write progress/errors to stderr. `start` prints an
   immediate `accepted` object containing the `request_id`, followed by its terminal audit object;
   `status` and `download` print one final object. The AI assistant must interpret these objects and
   provide a human-readable summary; the JSON objects alone are not user progress updates.

## Long-running Execution

Large prospectus audits have no predictable maximum duration, so the client has no default total
polling timeout. Each status request has a 30-second timeout and transient failures are attempted up
to three times with the same status-call request ID; the URL continues to use the audit request ID.
Run `start` or `watch` as the host's managed background task so long audits continue without binding
the AI request to the audit duration. Those commands only poll and never download. Use the foreground
`status` command to show an intermediate state to the user, and use the foreground `download` command
only after a successful terminal status. Stopping the local watcher does not cancel the Lite task; use
`watch <request_id>` to resume polling later.

## Cancellation and Process Ownership (Required)

The local Node client must be managed explicitly by the host task runner. A cancelled assistant task
must not leave an unmanaged local process behind.

- Run `start`/`watch` through the host's managed background-task facility and retain the submitted
  `request_id` and task handle. Run `status` and `download` as foreground commands.
- Do not make the script daemonize itself or spawn a second Node process. The host task runner owns
  starting, observing, and terminating the background watcher.
- If the user cancels the local watcher, terminate the host-managed `start`/`watch` task and do not
  start a download automatically. The remote task continues unless the service explicitly cancels it.
- Report the retained `request_id`; later use `status` for a one-time customer-visible update or
  `watch` to restart continuous polling.
- A local interruption stops the client process; it does not prove that the remote Lite audit was
  cancelled. Do not claim remote cancellation unless the service explicitly confirms it.

## Network and Sandbox Handling

- If DNS resolution, connection, or TLS negotiation fails, verify the configured hostname, DNS/hosts, certificate trust, and any required proxy.
- If a loopback address (`127.0.0.1`, `localhost`, or `::1`) or a private address is unreachable only from the sandbox, treat it as an execution-environment isolation issue. Request an approved sandbox-external execution context before submitting the audit.
- If the audit request reaches PDRouter but returns HTTP `404`, `401`, or another response, treat it as a service, authentication, or routing/configuration issue rather than a sandbox connectivity failure.
- For a customer-isolated environment, configure `PAODINGAI_API_BASE_URL` to its routable PDRouter OpenAPI base. The domain must resolve from the actual client sandbox, allow outbound HTTPS/443, have a trusted certificate, and expose the configured `autodoc-next` capability.

After an audit POST connection failure, preserve and report the returned `request_id`, then confirm
or watch that request according to the API contract before starting another audit.
