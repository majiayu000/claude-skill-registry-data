---
name: code-review-java
description: >
  Security review of Java code — dangerous sinks and Spring pitfalls. Load when reviewing a Java/
  Spring codebase/PR, on .java source in scope, or "review this Java". Signals: pom.xml/build.gradle,
  Spring/Spring Boot, ObjectInputStream, XML parsers, Runtime.exec, JNDI/lookups.
domain: code-review
type: reference
stability: learning
modes: [bugbounty, defense, pentest]
severity: info
cwe: [CWE-502, CWE-611, CWE-78, CWE-89, CWE-917]
tools: [semgrep, codeql, find-sec-bugs, ripgrep]
schema_version: 1
---

# Java / Spring source review

## When it applies
Reviewing Java source, most often a Spring/Spring Boot service. Java's biggest hitters are
deserialization, XXE-by-default, and expression-language injection — all high impact and all
grep-able.

## Why it works
Several Java APIs are unsafe by default (XML parsers resolve external entities; `ObjectInputStream`
instantiates arbitrary classes) and frameworks expose powerful expression languages (SpEL/OGNL) that
turn a string into code. Tracing the source to a request parameter or message body confirms reach.

## Sinks & patterns (grep, then trace to user input)
- **Deserialization**: `ObjectInputStream.readObject`, Jackson `enableDefaultTyping`/polymorphic
  types, XMLDecoder, SnakeYAML `new Yaml().load`, unsafe `readValue` with type info → RCE gadgets.
- **XXE**: `DocumentBuilderFactory`, `SAXParser`, `XMLInputFactory`, `TransformerFactory` without
  `setFeature(disallow-doctype)`/secure-processing.
- **Command exec**: `Runtime.getRuntime().exec`, `ProcessBuilder` with concatenated input.
- **Expression injection**: SpEL (`SpelExpressionParser`, `@Value("#{...}")` on input), OGNL
  (Struts), MVEL; template engines with unescaped output.
- **SQL/HQL**: `Statement`/string-built queries, `createQuery` with concatenation.
- **SSRF**: `URL.openConnection`, `RestTemplate`, `HttpClient`, `WebClient` on user URLs.
- **JNDI**: `InitialContext.lookup`, log4j-style `${jndi:...}` (Log4Shell) reachable from input.

## Framework specifics
- **Spring**: mass assignment via `@ModelAttribute`/`DataBinder` (missing `setAllowedFields`),
  exposed/unsecured Actuator endpoints, `@RequestMapping` path traversal, permit-all misconfig in
  `SecurityFilterChain`, SpEL in `@PreAuthorize`.
- **Struts/older MVC**: OGNL injection (S2-* CVEs).

## Method
1. `rg` for the sinks; trace to controller params, headers, or message consumers.
2. Check XML parser factory configuration everywhere XML is read.
3. Review the Spring Security config for accidental `permitAll()`/disabled CSRF on state-changing routes.
4. Confirm with `web-deserialization`, `web-xxe`, `web-ssrf`, or `web-command-injection`.

## Gotchas
- Jackson is safe unless default/polymorphic typing is enabled — check for it specifically.
- `find-sec-bugs`/CodeQL surface candidates; you still must prove input reaches the sink.
- Log4Shell-style lookups can fire from headers (User-Agent, X-Forwarded-For), not just body.

## References
OWASP Deserialization & XXE cheat sheets; SpEL/OGNL injection research; find-sec-bugs rules.
