---
name: log-injection-telemetry
version: "1.0.0"
description: Telemetry-pipeline integrity for mid-2026 — CR/LF log-injection neutralization across every sink, secret/PII redaction before shipping, authenticated metrics endpoints, and exporter destination allowlisting, secret-store credentials, verified TLS, and webhook SSRF guarding
triggers:
  - log injection
  - crlf injection
  - log forging
  - telemetry integrity
  - secrets in logs
  - log redaction
  - metrics endpoint exposure
  - prometheus exposure
  - otlp exporter
  - cloudwatch
  - webhook sink
  - exporter ssrf
  - observability security
  - log sink
  - telemetry exfiltration
discovery_mode: standalone
data_deps:
  - cve-catalog.json
  - atlas-ttps.json
  - attack-techniques.json
  - framework-control-gaps.json
  - cwe-catalog.json
  - rfc-references.json
atlas_refs: []
attack_refs:
  - T1565.001
  - T1530
  - T1213
framework_gaps:
  - NIST-800-53-SI-2
  - ISO-27001-2022-A.8.15
  - NIS2-Art21-network-security
  - UK-CAF-B4
  - AU-ISM-1815
cwe_refs:
  - CWE-117
  - CWE-532
  - CWE-918
  - CWE-200
last_threat_review: "2026-06-02"
---

# Telemetry-Pipeline Integrity (Log Injection + Sink Confidentiality)

## Threat Context (mid-2026)

The telemetry pipeline is both an integrity target and a confidentiality leak that "we centralize all logs" does not address. Integrity: un-sanitized CR/LF in interpolated log values lets an attacker forge or split log entries — injecting fake lines, breaking the log parser, or hiding their own actions — corrupting the observability record incident response depends on. Confidentiality: secrets and PII logged without a redaction pass persist in every downstream sink (SIEM, cloud log service); an unauthenticated /metrics or debug endpoint leaks internal topology and operational state; exporters (OTLP, CloudWatch, webhook) that ship to un-inventoried or input-derived destinations become exfiltration and SSRF channels; embedded sink credentials and plaintext export widen the exposure. These are pipeline-posture gaps, not log-volume gaps.

## Framework Lag Declaration

Organisational logging controls require events be recorded, centralized, and access-controlled. NIST 800-53 AU-9 (protection of audit information) is attested by access controls on the log store and does not address CR/LF log injection that forges entries before they reach the store. SI-11 (error handling / output neutralization) is named generally but not operationalised as per-sink CR/LF neutralization or secret redaction. ISO 27001 A.8.15 is met with "we log and protect logs." None address telemetry-exporter egress, SSRF, or unauthenticated metrics. A clean "we centralize logs to a SIEM with access controls" audit is therefore NON-EVIDENCE for telemetry-pipeline integrity; it confirms log presence and store ACLs, not neutralization, redaction, metrics auth, or exporter posture.

## TTP Mapping

The telemetry-pipeline failures map to MITRE ATT&CK: **T1565.001 (Stored Data Manipulation)** for CR/LF log forging that rewrites or splits the audit record; **T1530 (Data from Cloud Storage / shipped telemetry)** for secrets/PII leaking through logs, exporter exfiltration, and webhook-sink SSRF reaching internal services; and **T1213 (Data from Information Repositories)** for an unauthenticated metrics/debug endpoint disclosing internal state. The weakness classes are CWE-117 (improper output neutralization for logs — log injection), CWE-532 (insertion of sensitive information into log files), CWE-918 (server-side request forgery — exporter/webhook egress), and CWE-200 (exposure of sensitive information — unauthenticated metrics).

## Exploit Availability Matrix

These are pipeline-posture gaps, so the exploit is the absent control. CR/LF log injection requires only a request field that reaches a line-oriented sink un-neutralized — trivially reproduced. Secrets in logs are harvested wherever the logs land. An unauthenticated /metrics is a single unauthenticated GET. A webhook sink pointed at the cloud metadata endpoint is an SSRF with commodity payloads. The real-world priority is set by whether secrets/PII leak across every downstream sink (credential/PII breach), whether the audit record can be forged (defeating incident response), or whether the telemetry process can be turned into an SSRF channel to the internal network or metadata service.

## Analysis Procedure

1. Enumerate every log/trace/metric sink and exporter, and every metrics/debug endpoint. 2. Confirm each sink neutralizes CR/LF + control characters in interpolated values (or uses a structured format that cannot be line-split) — note any sink other than syslog that does not. 3. Confirm a redaction pass strips secrets/PII before values reach any sink. 4. Confirm metrics/debug endpoints require authentication or are bound to a private scrape network. 5. Confirm exporter destinations are an inventoried allowlist (not input-derived), credentials come from a secret store, and export uses verified TLS. 6. Confirm webhook sinks allowlist their URL and refuse private/link-local/metadata addresses. Run the `log-injection-telemetry` playbook to execute these as detect indicators with false-positive checks, then score by leakage breadth, audit-record corruptibility, and SSRF reach.

## Output Format

Report per sink/exporter/endpoint, marking each control enforced / missing / inconclusive (visibility gap). For every missing control, state whether it leaks secrets/PII across sinks, allows forging the audit record, or enables exfil/SSRF from the telemetry process, and whether the surface is internet-reachable. Distinguish a control enforced at a lower layer (a sanitizing collector/sidecar, a private scrape network) from an absent one. Provide the prioritised remediation (neutralize CR/LF + redact per sink, authenticate/private metrics, allowlist exporters with secret-store credentials over verified TLS, SSRF-guard webhook sinks) and the negative validation tests (CR/LF neutralized, secret redacted, metrics requires auth, webhook SSRF blocked) plus a functional test that legitimate telemetry still flows.

## Compliance Theater Check

The recurring theater is "we centralize all logs to a SIEM, so logging is handled," "the log store has access controls, so logs are protected," and "our metrics are internal-only." Centralization is not integrity or confidentiality; store ACLs do not stop injection at write time; an "internal" /metrics is often reachable via a default all-interfaces bind or an exposed ingress. The distinguishing test: inject CR/LF into a logged value and check for a forged line; log a secret and check redaction; reach /metrics unauthenticated; inspect exporter destinations, credentials, and TLS. If forging, secret leakage, or exfil/SSRF succeeds, centralization did not protect the pipeline and the assurance is paper.

## Defensive Countermeasure Mapping

Map findings to MITRE D3FEND: per-sink CR/LF neutralization realises Message Encoding / Output Neutralization (countering T1565.001 log forging); secret/PII redaction realises Sensitive-Data Scrubbing (countering T1530 leakage); metrics-endpoint authentication realises Network Traffic Filtering and Authentication Enforcement (countering T1213 disclosure); exporter destination allowlisting, secret-store credentials, verified TLS, and webhook SSRF guards realise Outbound Traffic Filtering and Resolution-Trust (countering T1530 exfil / SSRF). Pair the redaction pass with the dlp-gap-analysis skill for the broader data-egress picture, without duplicating its LLM/RAG focus. The residual risk is the inherent sensitivity of telemetry held in a legitimate access-controlled store, accepted at the CISO level.
