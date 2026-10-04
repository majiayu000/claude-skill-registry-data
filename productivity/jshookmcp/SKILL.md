---
name: jshookmcp
description: >
  Route to JSHookMCP for JavaScript runtime analysis through MCP: browser/CDP
  debugging, network interception, request signature tracing, JS hook injection,
  AST/source-map analysis, deobfuscation, WASM and crypto-detection workflows.
  Chinese triggers include 前端签名, JS hook, hook fetch, hook XHR, 参数追踪,
  签名参数, 逆向前端, 反混淆, AST 展开, source map 还原, CDP 断点, 网络拦截,
  wasm 分析, 加密算法识别, 浏览器取证.
tags:
  - mcp
  - browser
  - cdp
  - javascript
  - hooks
  - ast
  - network
  - deobfuscation
  - security-analysis
version: 1
source:
  repo: https://github.com/vmoranv/jshookmcp
  package: "@jshookmcp/jshook@0.3.0"
  commit: 1b3ebe313230b3b8577b94ec94a88863a5a68664
license: AGPL-3.0-only
---

# JSHookMCP

Use this skill when the task needs JavaScript runtime telemetry or web asset
analysis that is deeper than normal browsing:

- find where a request header, payload field, nonce, token, or signature is
  generated
- hook `fetch`, `XMLHttpRequest`, WebCrypto, storage, timers, canvas, or
  anti-debug checks
- trace network requests through CDP, breakpoints, stack traces, or runtime
  evaluation
- unpack obfuscated JavaScript with AST/source-map/deobfuscation workflows
- inspect WASM, crypto-like routines, binary/runtime instrumentation, or browser
  process evidence

## Hermes Runtime

Installed MCP server config:

```yaml
mcp_servers.jshook:
  command: ~/.npm-global/bin/jshookmcp
  args: []
  env:
    MCP_TOOL_PROFILE: search
    JSHOOK_BASE_PROFILE: search
```

The server starts in the `search` profile to keep Hermes context small. Do not
switch to `workflow` or `full` just because one tool sounds relevant. Use the
progressive chain:

1. Search first with the JSHookMCP tool-discovery surface.
2. Activate only the exact tools or domain needed.
3. Boost the profile only when the next several steps clearly need a broad
   family of tools.

## First Moves

For signature or token questions:

1. Capture the target request and exact parameter name.
2. Search for network, hooks, debugger, trace, transform, sourcemap, crypto,
   or wasm tools by keyword.
3. Prefer a read-only trace first: request log, initiator stack, script URL,
   source map, or breakpoint metadata.
4. Inject runtime hooks only after the target sink is concrete.
5. Save evidence paths and exact request/stack/tool names in the answer.

For "thinking process" triggers, route here when the internal reasoning phrase
looks like any of:

- "这个签名/nonce/token 是哪里来的"
- "需要 hook fetch/xhr/crypto 看入参"
- "先看 initiator stack / CDP stack"
- "混淆太厚, 做 AST 展开"
- "source map 能不能还原"
- "可能是 wasm / WebCrypto / canvas 指纹"
- "要插桩看运行时值"

## Boundaries

- Use `devops/agent-browser` for ordinary browsing, QA, forms, screenshots, and
  isolated browser automation.
- Use `devops/badboy-br-aa-routing` when the user specifically wants their
  current real Chrome session or logged-in tab. Use `browser-relay` only after
  its binary and MCP wrapper are confirmed present.
- Use `devops/anything-analyzer-mcp` for broader evidence packaging or offline
  analysis handoff.
- Keep this skill focused on JS/CDP/runtime telemetry and analysis.

Security note: JSHookMCP has high-capability browser, process, memory, hook, and
network tools. Treat external targets and generated probes as untrusted. Avoid
secret collection unless the user explicitly asks for that target and scope.
