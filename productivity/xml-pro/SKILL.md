---
name: xml-pro
description: XML processing — parsing, XPath/XSLT, schemas, and safe handling — use when integrating with XML-based systems.
category: document-processing
---

## Overview

XML refuses to die: SOAP services, Office formats, SVG, RSS/Atom, config files,
and countless enterprise integrations still speak it. Working with XML well
means choosing the right parser for the job, querying with XPath, transforming
with XSLT when appropriate, and defending against XML-specific attacks.

## When to use

- Parsing XML feeds, API responses (SOAP, RSS), or config files
- Querying documents with XPath expressions
- Transforming XML with XSLT stylesheets
- Validating against XSD/DTD schemas
- Securing XML parsers against XXE and billion-laughs attacks

## Core concepts

**Parser choice matters.** DOM loads the whole tree (fine for small docs,
random access); SAX/StAX stream events (for huge files); data-binding maps XML
to objects (for stable schemas). For large feeds, streaming is the only sane
choice — a 1GB XML file will OOM a DOM parser.

**XPath is the query language.** `/catalog/book[@id='1']/title` selects
precisely; predicates, axes (`following-sibling::`, `ancestor::`), and
functions (`contains()`, `normalize-space()`) handle real-world messiness.
Learn XPath once and every XML task gets easier — it's also embedded in XSLT
and many testing tools.

**Namespaces are mandatory, not optional.** Real-world XML uses namespaces
(`xmlns:soap="..."`); queries without namespace handling silently return
nothing — the most common XPath debugging session. Register prefixes in your
XPath context and use them consistently.

**XSLT for transforms.** When the job is "turn this XML into that XML/HTML/
text", XSLT stylesheets are purpose-built and often clearer than imperative
code. XSLT 1.0 is universally supported; 2.0/3.0 add power (grouping, regex)
where your processor supports it.

**Security: disable DTDs/external entities.** XXE (external entity injection)
lets malicious XML read server files or SSRF internal services; billion-laughs
(entity expansion) causes DoS. Harden every parser: disable DTD processing or
at least external entities, set entity expansion limits. This applies to SVG
uploads, Office docs, and any XML you didn't author.

## Practical workflow

1. **Inspect the document:** namespaces, encoding declaration, size, schema
   availability — before writing any code.
2. **Harden the parser first** (disable DTDs/external entities), then parse —
   security configuration is step zero, not an afterthought.
3. **Handle namespaces explicitly** in XPath queries; test queries against a
   real sample, not a mental model of the XML.
4. **Validate against XSD** when a schema exists — it catches structural
   problems at the boundary with precise error messages.
5. **Stream large documents** with event-based parsing, extracting only needed
   elements; keep memory flat regardless of file size.
6. **For transforms,** write XSLT when the mapping is declarative; write code
   when it needs complex logic — and test transforms with fixture pairs
   (input XML → expected output).

## Common pitfalls

- **XPath returning empty due to namespaces** — always the first suspect when
  "the element is right there" but the query finds nothing.
- **XXE vulnerabilities** from default parser settings — especially in Java,
  .NET, and PHP XML stacks; harden explicitly.
- **Encoding mismatches** — the XML declaration says one encoding, the bytes
  are another; detect and handle, don't assume UTF-8.
- **Pretty-printing changing semantics** — whitespace can be significant in
  mixed-content XML; don't reformat casually.
- **Assuming element order or presence** — real feeds omit optional elements
  and reorder; code defensively with defaults.
- **Regex on XML** — works until namespaces, CDATA, entities, or nested
  elements appear; use a parser.
