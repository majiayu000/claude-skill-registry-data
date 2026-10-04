---
name: coap
description: "Constrained Application Protocol (RFC 7252): RESTful UDP messaging, confirmable messages, observe pattern, and DTLS security"
category: iot
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/iot/coap/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# CoAP Protocol

## Scope
CoAP is a specialized web transfer protocol for use with constrained nodes and constrained networks (6LoWPAN), mapping RESTful semantics onto UDP.

## Protocol Architecture (RFC 7252)
- **Transport**: UDP-based, small 4-byte fixed header overhead.
- **Message Types**: Confirmable (CON, requires ACK), Non-confirmable (NON), Acknowledgment (ACK), Reset (RST).
- **RESTful Methods**: GET, POST, PUT, DELETE mapping directly to HTTP via gateways.
- **Observe Option (RFC 7641)**: Publisher notifies registered clients on state change without polling.
- **Security**: Datagram Transport Layer Security (DTLS) providing encryption and authentication.

## Tools & Standards
- **Standards**: IETF RFC 7252 (CoAP), RFC 7641 (Observing Resources in CoAP).
- **Software**: Californium (Java), libcoap, aiocoap (Python).
