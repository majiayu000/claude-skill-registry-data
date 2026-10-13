---
name: code-review-nodejs
description: >
  Security review of Node.js / JavaScript code — dangerous sinks and Express/framework pitfalls.
  Load when reviewing a Node/JS codebase/PR, on package.json + Express/Next/Nest, or "review this
  Node app". Signals: child_process, eval, Function, prototype pollution, JWT, Mongoose/Sequelize.
domain: code-review
type: reference
stability: learning
modes: [bugbounty, defense, pentest]
severity: info
cwe: [CWE-94, CWE-78, CWE-1321, CWE-89]
tools: [semgrep, njsscan, ripgrep]
schema_version: 1
---

# Node.js / JavaScript security code review

## When it applies
Reading Node/JS source (Express, Next.js, NestJS, a package). Language companion to
`code-review-methodology` — the exact sinks and framework gotchas to grep and trace.

## Sinks & patterns (grep, then trace to user input)
- **Command exec**: `child_process.exec`/`execSync` with user input (use `execFile`/`spawn` w/ arg array);
  template strings in commands.
- **Code eval**: `eval`, `new Function`, `vm.runIn…`, `setTimeout("string")` — RCE.
- **Prototype pollution**: recursive merge/`Object.assign`/`lodash.merge`/`set`, `JSON.parse` into
  object merges, query parsers — `__proto__`/`constructor` keys (→ `web-prototype-pollution`).
- **SQL/NoSQL**: string-built SQL; Mongo queries taking raw `req.body`/`req.query` (operator injection
  `{$gt:''}`); Sequelize `.query()`/`literal`.
- **SSRF**: `axios`/`fetch`/`http.get`/`request` on a user URL.
- **Path/upload**: `fs.readFile`/`sendFile`/`path.join` with user paths; `res.sendFile` traversal.
- **XSS (server + client)**: `res.send` of unescaped input; DOM sinks `innerHTML`, `document.write`,
  `dangerouslySetInnerHTML` (React), `v-html` (Vue).
- **Deserialization**: `node-serialize`/`funcster` (unserialize RCE), untrusted `JSON`→object merge.

## Framework specifics
- **Express**: missing `helmet`/CSP, over-broad `cors()`, `req.query`/`req.params` into sinks, weak
  session `secret`, no per-object authz (IDOR/BOLA), `app.use` order bypassing auth middleware.
- **JWT**: `jsonwebtoken` with `algorithms` not pinned (alg confusion / `none`), weak secret
  (→ `web-auth-jwt`), secret in code.
- **Next.js/SSR**: `getServerSideProps` trusting client input; API routes missing auth; SSRF in image/proxy.
- **Mass assignment**: spreading `req.body` into a model/`create` (→ `api-mass-assignment`).

## Method
`rg -n "child_process|eval\(|new Function|innerHTML|dangerouslySetInnerHTML|\.merge\(|__proto__|node-serialize"`;
run `njsscan .` and `semgrep --config auto`; trace user input to each sink.

## Gotchas
- Client-side `innerHTML`/`v-html` = DOM XSS even in a "backend" review — check the front-end too.
- Mongo operator injection needs input validation/casting, not just parameterization.

## References
njsscan; Semgrep JS/TS rules; OWASP Node.js & NodeGoat; Express security best practices.
