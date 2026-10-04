---
name: audit-security
description: Scan the codebase for security vulnerabilities. Check OWASP top 10, input validation, auth, crypto, and known BACKLOG security items.
allowed-tools: Read, Glob, Grep, Agent, Bash(ls *), Bash(wc *)
---

# Security Audit

Scan the codebase for security vulnerabilities and verify that known issues from `docs/ai/BACKLOG.md` (Security section) are tracked.

## Scope

### 1. Input Validation & Injection

- **JSON Patch / prototype pollution** — verify `__proto__`, `constructor`, `prototype` are blocked in all code paths that apply external data to objects
- **XSS** — check for `innerHTML`, `{@html}`, `document.write`, `eval` usage; verify user-supplied strings are escaped
- **Command injection** — check for shell exec, dynamic `import()`, `Function()` with user input
- **localStorage / IndexedDB** — verify `validateSongData()` / `validateRecoverySnapshot()` are called before casting raw JSON to Song

### 2. Authentication & Authorization

- **multiDevice signaling** — room code entropy, rate limiting on connection attempts, room TTL
- **WebRTC data channel** — message validation, param whitelist, bounds checking on guest inputs
- **No secrets in client code** — scan for API keys, tokens, credentials in source files

### 3. Cryptographic Safety

- **Room code generation** — must use `crypto.getRandomValues()`, not `Math.random()`
- **Sufficient entropy** — room codes, IDs, nonces should have adequate bit strength

### 4. Network & Transport

- **CORS / CSP** — check for overly permissive headers
- **WebSocket origin validation** — signaling server should validate origin
- **Data channel message size** — verify chunking limits prevent memory exhaustion (MAX_CHUNKS, memory budget)

### 5. Resource Exhaustion

- **Rate limiting** — verify post-connection message rate limits exist
- **Memory budgets** — chunk reassembly budget, undo stack cap, sample pool limits
- **CPU abuse** — AudioWorklet cannot be starved by malicious patterns (step count limits, track count limits)

### 6. Known Issues Tracking

- **Read `docs/ai/BACKLOG.md`** Security section — verify all known vulnerabilities are listed
- **Cross-reference with tests** — check `security.test.ts` covers each known issue
- **Identify gaps** — find vulnerabilities NOT yet listed in BACKLOG

## Process

1. **Read BACKLOG.md** Security section for known issues.
2. **Scan source files** using Grep/Glob for vulnerability patterns.
3. **Read security-critical modules** in detail:
   - `src/lib/multiDevice/` — all files
   - `src/lib/validate.ts` — data validation
   - `src/lib/storage.ts` — persistence layer
   - `src/lib/audio/engine.ts` — worklet bridge
   - `workers/signaling/` — signaling server (if present)
4. **Cross-reference with tests** in `src/lib/multiDevice/security.test.ts`.
5. **Output a report**:

```
## Security Audit Report

### Category: [Input Validation / Auth / Crypto / Network / Resources]

#### [Vulnerability name]
- **Severity**: Critical / High / Medium / Low / Info
- **Location**: file:line
- **Description**: what's wrong
- **Status**: Known (in BACKLOG) / New finding / Tested (in security.test.ts)
- **Recommendation**: fix approach

### Summary
- X critical, Y high, Z medium findings
- N known issues tracked in BACKLOG
- M gaps in test coverage
```

## Severity Levels

- **Critical**: Remote exploitation without auth, data loss, arbitrary code execution
- **High**: Auth bypass, session hijack, significant data exposure
- **Medium**: Requires specific conditions, limited blast radius (e.g., room code brute-force)
- **Low**: Defense-in-depth improvement, unlikely exploitation path
- **Info**: Best practice suggestion, no direct vulnerability

## Rules

- This is a **read-only** operation — do not modify any files
- Use parallel Agent tools for different scan categories
- Report ONLY confirmed issues with specific file/line references
- Do not report theoretical vulnerabilities without evidence in the code
- Check the BACKLOG Security section — don't re-report known issues unless their description is incomplete
