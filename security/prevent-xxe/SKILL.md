---
name: prevent-xxe
description: Use when parsing XML in any context — file uploads, SOAP APIs, RSS/Atom feeds, SVG processing, document conversion, or any XML-based data exchange format.
source: 'OWASP XML External Entity Prevention Cheat Sheet (owasp.org/www-project-cheat-sheets); OWASP Top 10 2021 A05; CWE-611; NIST NVD CVE-2019-0251'
tags: [security, owasp, xxe, xml, external-entity, developer, input-validation]
---

# Prevent XXE

Disable external entity processing and DTD loading in all XML parsers — eliminating file disclosure, SSRF, and denial-of-service attacks through XML document processing.

## Why This Is Best Practice

**Adopted by:** OWASP Top 10 included XXE (A04:2017, merged into A05:2021). CVE-2019-0251 (Apache Solr XXE), CVE-2018-1000632 (dom4j XXE), CVE-2017-5638 (Equifax Struts2) all resulted from default XML parser configurations. SANS Top 25 Most Dangerous Software Errors lists XXE. SAP, Oracle, and Microsoft have all issued XXE patches for their XML-parsing products.
**Impact:** XXE enables reading arbitrary server files (`/etc/passwd`, `/etc/shadow`, AWS credentials), internal SSRF to reach metadata endpoints, and billion-laughs XML bomb DoS that crashes parsers with 1KB of input. The Equifax breach (2017, 147M records) exploited an Apache Struts vulnerability where XXE was part of the attack chain. Facebook, Ubisoft, and Groupon have paid XXE bug bounties.
**Why best:** Input sanitization attempting to strip DOCTYPE declarations is the alternative — it fails on encoded variants and CDATA tricks. Disabling external entity processing and DTDs at the parser level eliminates the vulnerability structurally, regardless of input content.

Sources: OWASP XXE Prevention Cheat Sheet; Equifax breach post-mortem; CWE-611; NVD XXE CVE database

## Steps

1. **Python (lxml, ElementTree, xml.etree)**:

   ```python
   # ElementTree (safe by default since Python 3.8 — defusedxml for older)
   from defusedxml import ElementTree
   tree = ElementTree.parse(xml_file)

   # lxml — disable external entities explicitly
   from lxml import etree
   parser = etree.XMLParser(
       resolve_entities=False,
       no_network=True,
       load_dtd=False
   )
   tree = etree.parse(xml_file, parser)
   ```

2. **Java**:

   ```java
   DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
   // Disable DTDs entirely
   dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
   // Disable external entities
   dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
   dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
   // Disable external DTD loading
   dbf.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
   dbf.setXIncludeAware(false);
   dbf.setExpandEntityReferences(false);

   DocumentBuilder db = dbf.newDocumentBuilder();
   ```

   Same flags apply to SAX, StAX, and JAXB parsers — configure each parser instance, not globally.

3. **PHP**:

   ```php
   // Disable entity loading (PHP < 8.0)
   libxml_disable_entity_loader(true);

   // PHP 8.0+ — entity loading disabled by default
   $doc = new DOMDocument();
   $doc->loadXML($xml, LIBXML_NOENT | LIBXML_DTDLOAD); // Do NOT use these flags
   $doc->loadXML($xml); // Correct: no entity loading flags
   ```

4. **.NET (C#)**:

   ```csharp
   XmlReaderSettings settings = new XmlReaderSettings();
   settings.DtdProcessing = DtdProcessing.Prohibit;  // disables DTD
   settings.XmlResolver = null;                        // disables external resolution
   XmlReader reader = XmlReader.Create(xmlStream, settings);
   ```

5. **Node.js** — avoid XML parsers that enable entities. Use `fast-xml-parser` with entity disabled or `xml2js` (safe by default):

   ```javascript
   const { XMLParser } = require('fast-xml-parser');
   const parser = new XMLParser({
       processEntities: false,  // disable entity processing
   });
   const result = parser.parse(xmlString);
   ```

6. **Validate that DTD processing is disabled before accepting XML in production** — send a test payload and verify it's rejected or entities are unexpanded:

   ```xml
   <?xml version="1.0"?>
   <!DOCTYPE test [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
   <root>&xxe;</root>
   ```

   If the response contains passwd file contents, DTD processing is enabled.

7. **For SOAP and REST services that accept XML** — validate Content-Type and reject requests declaring `text/xml` or `application/xml` from untrusted sources unless your service explicitly needs to process them.

## Rules

- Each XML parser instance must be configured — library-level disabling often only affects one parser type. Configure DocumentBuilder, SAXParser, StAX, and JAXB separately in Java.
- SVG, DOCX, XLSX, ODF, and RSS are XML formats — they're vulnerable to XXE when parsed without entity protection.
- Disabling DTDs entirely (`disallow-doctype-decl`) is stronger than disabling only external entities — internal entity expansion can still cause DoS (billion laughs attack).
- JSON parsers are not vulnerable to XXE — only XML parsers.

## Common Mistakes

- **Configuring only DocumentBuilderFactory but not SAXParser** — SOAP frameworks often use SAX internally; both must be hardened.
- **Using `LIBXML_NOENT` in PHP** — this flag ENABLES entity substitution, the opposite of what's needed.
- **Thinking SVG upload is safe from XXE** — SVG is XML; a malicious SVG can trigger XXE when parsed by image processing libraries (ImageMagick, Inkscape).
- **Validating XML against a schema without disabling DTD first** — schema validation still triggers DTD processing.
