---
id: template-injection
version: "2.0.0"
title: "Template Injection (SSTI)"
description: "User input reaching a template compiler rather than its context: the source-versus-values distinction, double-render pipelines, template names chosen by the caller, why a template sandbox is a mitigation and not a boundary, minimizing what the render context exposes, and template-driven resource exhaustion. Use when rendering templates with user-influenced values, when a template string or template name is assembled from input, or when a product lets users author templates."
category: prevention
severity: critical
applies_to:
  - "when rendering a template with any user-influenced value (email or notification bodies, PDFs, HTML, config)"
  - "when a template's source string, or the template's name or path, comes from input"
  - "when a product feature lets users author or edit templates"
  - "when reviewing a two-step render or re-parse pipeline"
languages: ["*"]
token_budget:
  minimal: 1250
  compact: 1750
  full: 2100
rules_path: "rules/"
tests_path: "tests/"
related_skills: ["frontend-security", "api-security", "file-upload-security", "llm-app-security"]
last_updated: "2026-08-14"
sources:
  - "OWASP Testing Guide — Server-Side Template Injection (WSTG-INPV-18)"
  - "PortSwigger — Server-Side Template Injection"
  - "CWE-1336: Improper Neutralization of Special Elements Used in a Template Engine"
  - "CWE-94: Improper Control of Generation of Code"
  - "CWE-770: Allocation of Resources Without Limits or Throttling"
---

# Template Injection (SSTI)

## Rules (for AI agents)

### ALWAYS
- Pass user data as **bound values**, never into the template **source** string. This
  is the whole skill in one line: `render(tmpl, {"name": name})` is safe,
  `render("Hello " + name)` is SSTI. The compiler treats its source as code, and the
  context as data — so the only question that matters about any user value is which of
  the two it reaches.
- Keep the set of template sources **static and trusted**, loaded from files or
  constants. A template body read from a database column, an API response, or a
  request field is attacker-supplied code, whatever the column is called.
- Choose the template **by name from an allowlist**, never by a name the caller
  supplies. `render_template(user_value)` and `{% include user_value %}` are the same
  vulnerability as a user-supplied body: the caller picks which code runs, and on many
  engines the name resolves as a filesystem path, which makes it an arbitrary-file
  read as well.
- **Minimize the render context.** Pass the specific values the template needs, never
  the ambient objects — application config, settings, the request, `self`, a module, a
  live ORM instance. This is the control that still holds when a sandbox is escaped:
  an engine that cannot execute code can still print whatever it can reach, and
  configuration objects hold database URLs and signing keys.
- Treat a **second render pass** as compilation of whatever survived the first. If
  rendered output is parsed again, a user value that was inert data on pass one is
  `{{ }}` code on pass two. The fix is architectural — stop re-parsing rendered output.
  Neutralizing metacharacters before the second pass is a fallback that has to
  enumerate every delimiter of every engine, including ones a custom delimiter
  configuration introduces, and two adjacent fields can produce a delimiter that
  neither of them contains.
- **Bound the render**: cap iteration counts, recursion depth, include depth, output
  size, and wall-clock time. A template is a denial-of-service sink even where it is
  not a code-execution one, and an unbounded loop count is one request that allocates
  until the process dies.
- Keep **autoescaping on**, and know that autoescape is an XSS control rather than an
  SSTI one — it escapes what the template prints, not what the template *is*.
  `frontend-security` owns output encoding and the raw-output opt-outs
  (`|safe`, `{{{ }}}`, `template.HTML`) that turn it off per value.

### NEVER
- Build a template's source from user input — string concatenation, an f-string,
  `String.format`, or a `Template(...)` / `from_string` / `compile` call whose argument
  contains a value you did not write.
- Store a template body in a user-writable field — a profile name, an email subject, a
  CMS block — and later hand it to the engine.
- Treat a **sandbox as a trust boundary**. Sandboxed environments restrict attribute
  and builtin access, and they have a documented history of escapes in every engine
  that offers one; the escape is usually a way to reach an ordinary-looking attribute
  that leads back to a callable. A sandbox lowers the probability of RCE and does not
  make user-authored templates safe. If the product genuinely requires user-authored
  templates, isolate the renderer — separate process, no network, no filesystem, no
  credentials, a wall-clock timeout — and keep the engine patched.
- Enumerate forbidden attribute names as the control (`__class__`, `__globals__`,
  `constructor`, `getClass`). A denylist of literal names is defeated by string
  concatenation, indexing, and dynamic attribute lookup. Allowlist what the template
  may reach instead.
- Assume the client-side framework is out of scope when the *template string itself* is
  user-built. Runtime template compilation from user input — a compiler-included build
  compiling a user string, or `new Function` — is injection on the client. Interpolating
  a user value into a normal component template is XSS, which `frontend-security` owns.

### KNOWN FALSE POSITIVES
- User data passed as **context variables** to a static template is the correct
  pattern. This is the shape the whole skill is pointing at, not a finding.
- A `{{ … }}` or `${ … }` sequence in a string that never reaches a compiler is not
  SSTI: a client-side template shipped as a server-side string literal, an i18n
  catalogue, a Helm / Kubernetes / Grafana / Prometheus manifest, a CI expression. The
  finding requires a render call, not a delimiter.
- A logic-less engine with no user-authored template is not an RCE risk, though it is
  still subject to the output-size and XSS rules. Note that being *called* logic-less
  is not the same as being logic-less — engines that support helpers, partials and
  subexpressions are not, whatever their marketing says.
- Escaping opt-outs applied to content the application itself generated — a rendered
  Markdown block, a sanitized HTML fragment — are a `frontend-security` question about
  the sanitizer, not an SSTI finding.

## Context (for humans)

The distinction that makes this tractable is source versus context, and it survives
every engine and every language. A template engine compiles its source into something
executable and then evaluates it against a context. A value in the context is data by
construction — there is no expression that turns it back into code. A value in the
source is code by construction. So the review question is never "is this value
escaped"; it is "which of the two did it reach".

Everything else follows. A template body in a database is source. A template *name*
from a request selects source. A second render pass turns the first pass's output into
source. Those are three different-looking bugs and one property.

The sandbox deserves its own warning because it is where this goes wrong in production
systems. Products that let customers write their own email or document templates reach
for a sandboxed environment, and the sandbox is genuinely useful — but every engine
that ships one has had escapes, and the failure mode is total. The controls that still
work after an escape are the ones that assume it: a minimal context with nothing worth
reaching, and a renderer isolated from anything worth stealing.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `references/engines.md` — per-engine delimiters, the compile-a-string API to grep
  for, sandbox mechanism and its limits, autoescape behaviour, and which engines
  escalate to RCE versus disclosure
- `rules/template_injection.json`
- [OWASP WSTG — SSTI](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server-side_Template_Injection).
- [PortSwigger — Server-Side Template Injection](https://portswigger.net/web-security/server-side-template-injection).
- [CWE-1336](https://cwe.mitre.org/data/definitions/1336.html) · [CWE-94](https://cwe.mitre.org/data/definitions/94.html) · [CWE-917](https://cwe.mitre.org/data/definitions/917.html) · [CWE-770](https://cwe.mitre.org/data/definitions/770.html).
