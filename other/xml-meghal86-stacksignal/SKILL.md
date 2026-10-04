---
name: XML
description: Parse, generate, and transform XML with correct namespace handling and encoding.
metadata: {"clawdbot":{"emoji":"📄","os":["linux","darwin","win32"]}}
---

## Namespaces

- XPath `/root/child` fails if document has default namespace—use `//*[local-name()='child']` or register prefix
- Default namespace (`xmlns="..."`) applies to elements, not attributes—attributes need explicit prefix
- Namespace prefix is arbitrary—`<foo:element>` and `<bar:element>` are identical if both prefixes map to same URI
- Child elements don't inherit parent's prefixed namespace—each must declare or use prefix explicitly

## Encoding

- `<?xml version="1.0" encoding="UTF-8"?>` must match actual file encoding—mismatch corrupts non-ASCII
- Encoding declaration must be first thing in file—no whitespace or BOM before it (except UTF-8 BOM allowed)
- Default encoding is UTF-8 if declaration omitted—but explicit is safer across parsers

## Escaping & CDATA

- Five entities always escape in text: `&amp;` `&lt;` `&gt;` `&quot;` `&apos;`
- CDATA sections `<![CDATA[...]]>` for blocks with many special chars—but `]]>` inside CDATA breaks it
- Attribute values: use `&quot;` if delimited by `"`, or `&apos;` if delimited by `'`
- Numeric entities `&#60;` and `&#x3C;` work everywhere—useful for edge cases

## Whitespace

- Whitespace between elements is preserved by default—pretty-printing adds nodes that may break processing
- `xml:space="preserve"` attribute signals whitespace significance—but not all parsers respect it
- Normalize-space in XPath: `normalize-space(text())` trims and collapses internal whitespace

## XPath Pitfalls

- `//element` is expensive—traverses entire document; use specific paths when structure is known
- Position is 1-indexed: `[1]` is first, not `[0]`
- `text()` returns direct text children only—use `string()` or `.` for concatenated descendant text
- Boolean in predicates: `[@attr]` tests existence, `[@attr='']` tests empty value—different results

## Structure

- Self-closing `<tag/>` and empty `<tag></tag>` are semantically identical—but some legacy systems choke on self-closing
- Comments cannot contain `--`—will break parser even inside string content
- Processing instructions `<?target data?>` cannot have `?>` in data
- Root element required—document with only comments/PIs and no element is invalid

## Validation

- Well-formed ≠ valid—parser may accept structure but fail against schema
- DTD validates but can't express complex constraints—prefer XSD or RelaxNG for new projects
- XSD namespace `xmlns:xs="http://www.w3.org/2001/XMLSchema"` commonly confused with instance namespace
