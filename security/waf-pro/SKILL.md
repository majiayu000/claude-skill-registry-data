---
name: waf-pro
description: Deploy and operate web application firewalls — policy tuning, bot management, and virtual patching done right.
category: security
---

## Overview

A WAF sits in front of web applications filtering malicious HTTP traffic: injection attempts, protocol abuse, and automated attacks. It is a valuable compensating control — especially for virtual patching when code fixes take time — but it is not a substitute for secure code. Professional WAF practice is tuning: a well-tuned WAF blocks real attacks with minimal false positives; a default WAF mostly generates tickets.

This skill covers WAF deployment modes, rule tuning, bot management, and the honest accounting of what a WAF can and cannot do.

A WAF is a compensating control with an expiration date on every rule — it buys time for real fixes and filters the internet's background radiation of automated attacks. Respect both halves of that: it genuinely reduces noise and buys patching windows, and it genuinely cannot fix your application's broken authorization. Report its value honestly and retire its rules deliberately.

## When to use

- Protecting internet-facing web apps and APIs, especially legacy apps that are hard to patch.
- Virtual patching: blocking exploitation of a known vulnerability while the code fix is developed.
- Reducing automated abuse: credential stuffing, scraping, vulnerability scanning.
- Meeting compliance expectations for application-layer protection.

## Core concepts

- **Deployment modes:** reverse-proxy/inline (sees and can block everything; adds latency/failure domain), CDN/cloud WAF (easy, scales, less control), host-based/agent (close to the app). Choose by architecture and risk.
- **Positive vs negative security models:** negative (blocklist known-bad) is the default and needs constant updates; positive (allowlist expected behavior) is stronger but harder to maintain — best for stable, well-understood APIs.
- **Virtual patching:** writing a WAF rule to block a specific CVE's exploitation pattern buys time for the real fix. It is a bandage with an expiry date: track it and remove when patched.
- **Tuning lifecycle:** log/monitor mode → analyze false positives → tune → enforce → continuous review. Enforcing an untuned ruleset breaks legitimate users.
- **Bot management:** distinguishing good bots (search, monitoring) from bad (stuffing, scraping, scalping) via behavioral signals and challenge layers — separate from but adjacent to WAF.
- **What a WAF cannot do:** fix broken access control, business-logic flaws, or insecure design. It sees HTTP, not application semantics. Pair with secure code and testing.

- **API schema enforcement.** For well-defined APIs, positive-security validation against the OpenAPI schema blocks malformed and unexpected requests more reliably than generic attack signatures.
- **Layered rate limiting.** WAF-level, application-level, and account-level rate limits together handle volumetric abuse, targeted stuffing, and business-logic abuse respectively.
- **Geographic and reputation policy.** Geo-blocking and IP-reputation feeds are blunt instruments — use them as risk signals in layered policy, not as sole controls.

## Practical workflow

1. **Inventory and prioritize:** which apps/APIs get WAF protection first (internet-facing, sensitive data, known-vulnerable). Define success: block rate on attack traffic, FP rate near zero on legitimate traffic.
2. **Deploy in monitor mode:** full ruleset logging, no blocking, for 1–2 weeks of real traffic. Baseline legitimate patterns, especially for APIs (unusual but valid clients break naive rules).
3. **Tune:** disable rules that fire on legitimate traffic (document why); tighten rules for your actual threat profile; build custom rules for app-specific abuse patterns.
4. **Enforce gradually:** switch to block mode per application, watching error rates and support tickets like a hawk for the first 48 hours. Keep a fast rollback/disable path.
5. **Operate:** virtual-patch critical CVEs with tracked expiry; review blocked-traffic samples weekly for new attack patterns; tune quarterly or after app changes.
6. **Measure honestly:** report blocked attacks *and* false-positive rate *and* coverage gaps (what the WAF cannot see). Feed bypass patterns back to developers as code-fix tickets.

### WAF checklist

- [ ] Deployment mode chosen; failure/latency impact assessed
- [ ] Monitor-mode baseline completed before enforcement
- [ ] Rules tuned to app traffic; FP rate measured and acceptable
- [ ] Fast disable/rollback path tested
- [ ] Virtual patches tracked with expiry tied to code-fix dates
- [ ] Bot policy defined (allowlist good bots, challenge bad)
- [ ] Logging to SIEM; blocked-traffic review cadence set

### Sustaining the practice

- Review blocked-traffic samples weekly for emerging attack patterns
- Re-tune after every application release that changes request shapes
- Track virtual-patch age; escalate code fixes past their committed dates
- Benchmark false-positive rate per application monthly

### Metrics that prove it works

- Block rate on confirmed malicious traffic samples
- False-positive rate on legitimate traffic (per application)
- Age of oldest virtual patch without a code fix (should shrink)
- Bypass reports received and converted to code fixes

## Common pitfalls

- **Enforcing on day one.** Untuned blocking breaks legitimate traffic and gets the WAF blamed and bypassed. Monitor first.
- **Treating WAF as the fix.** Virtual patches without code-fix tickets are permanent bandages. Every virtual patch needs a real fix date.
- **Ignoring APIs.** API traffic patterns differ from browser traffic; generic rulesets cause false positives on valid API clients. Tune per API.
- **Set-and-forget.** Apps change, attacks change. Untended WAFs drift into irrelevance or false-positive hell.
- **No rollback plan.** When the WAF breaks checkout on Black Friday, you need a tested 60-second disable path, not a change ticket.
- **Overclaiming.** "WAF protected" does not mean "secure." Be honest about the control's limits in risk reporting.
- **WAF in front of the CDN but not the origin.** Attackers who discover the origin IP bypass the WAF entirely. Restrict origin access to the WAF/CDN only.
- **Rate limiting left to the WAF alone.** Credential stuffing and scraping need layered controls — rate limiting, bot management, and account-level defenses together.
- **WAF logs nobody reads.** Block events are threat intelligence about who is probing you and how. Feed them to the SOC and review trends.
- **SSL/TLS termination gaps.** If the WAF cannot see decrypted traffic properly, it is filtering blind. Ensure correct certificate deployment and cipher support.
