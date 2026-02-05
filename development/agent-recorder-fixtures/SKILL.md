---
name: agent-recorder-fixtures
description: Record real OpenAI/Anthropic HTTP back-and-forth (requests + responses, including streaming text/event-stream) and print paste-ready Swift fixtures for SwiftAgent unit tests (ReplayHTTPClient) using the AgentRecorder CLI or HTTPReplayRecorder. Use when adding/updating any provider adapter tests (text, streaming, structured outputs, tool calls), when payload formats change, or when debugging agent loop mismatches by inspecting recorded JSON/SSE payloads.
---

# Agent Recorder Fixtures

## Overview

Use `AgentRecorder` to capture real provider payloads and generate paste-ready Swift fixtures for tests using `ReplayHTTPClient`.
This is the fastest loop for keeping SwiftAgent’s unit tests (and agent-loop behavior) in sync with real OpenAI/Anthropic traffic.

## Workflow

1) Pick the right scenario
- Existing scenarios live in `AgentRecorder/AgentRecorder/Scenarios/` (grouped by provider + one file per scenario).
- List them quickly with `AgentRecorder --list-scenarios`.
- If no scenario matches your test, add one (keep it small and deterministic).

2) Set API keys
- Preferred: use a local `Secrets.plist` in the repo root (not committed).
  - Run with `--secrets-plist Secrets.plist`
  - Plist keys: `OpenAI_API_Key_Debug` / `Anthropic_API_Key_Debug`

Optional:
- Env vars fallback (useful for CI or quick runs): `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`
- `AGENT_RECORDER_SECRETS_PLIST` is also supported (fallback if env vars are missing).

Legacy:
- If you already have `Secrets.plist` under `Examples/Example App/ExampleApp/Secrets.plist`, either move/symlink it to the repo root or pass the full path via `--secrets-plist`.

3) Run the recorder (Xcode or Terminal)
- Xcode: select `AgentRecorder` scheme, set env vars, Run → copy stdout from Debug console.
- Terminal:

```bash
# Run from repo root.
# Apple Silicon: add `arch=arm64` to avoid “multiple matching destinations” warnings.
xcodebuild -workspace SwiftAgent.xcworkspace -scheme AgentRecorder -destination "platform=macOS,arch=arm64" -derivedDataPath .tmp/DerivedData build -quiet
./.tmp/DerivedData/Build/Products/Debug/AgentRecorder --list-scenarios
./.tmp/DerivedData/Build/Products/Debug/AgentRecorder --secrets-plist Secrets.plist --provider openai --scenario openai/streaming-tool-calls/weather --no-include-headers
```

4) Paste fixtures into tests
- Output is already formatted for `ReplayHTTPClient(recordedResponses:)`.
- Paste into the relevant test file (common locations):
  - `Tests/SwiftAgentTests/OpenAISession/...`
  - `Tests/SwiftAgentTests/AnthropicSession/...`

5) Run tests
- `xcodebuild -workspace SwiftAgent.xcworkspace -scheme SwiftAgentTests -testPlan SwiftAgentTests test -quiet`

## Notes

- Headers may include secrets. `HTTPReplayRecorder` redacts common auth header fields, but always review before committing.
- Prefer `--no-include-headers` unless you’re explicitly testing header handling.
- Always pass `-quiet` to `xcodebuild` to keep logs readable.
- `xcodebuild` may print noisy destination warnings; ignore if the build succeeds.
- Streaming fixtures are raw `text/event-stream`. If the SDK stops consuming early, the recorded payload may be partial (this is usually fine for replaying the SDK’s behavior).
- If you need request bodies for debugging, re-run with `--include-requests`.
- OpenAI scenarios: keep models pinned/stable (scenario-defined). Change only when you’re updating fixtures/tests.
- Cleanup: if you used `.tmp/DerivedData` (and/or wrote capture files like `.tmp/AgentRecorderOutput/*.txt`), delete them after you’ve pasted fixtures into tests.
