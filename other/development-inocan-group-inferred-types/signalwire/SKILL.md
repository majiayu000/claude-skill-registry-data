---
name: signalwire
description: Use when building telephony, messaging, or video applications; implementing voice AI agents; working with SWML call flows; debugging webhook callbacks or call state issues; setting up real-time WebSocket communication; encountering authentication 401/403 errors; or troubleshooting SWAIG function errors - provides REST API patterns, SDK examples, and production-tested workflows for modern SignalWire communication systems
---

# SignalWire

## ⚠️ AVOID Deprecated APIs

SignalWire maintains compatibility APIs (LAML/CXML) that should NOT be used for new development:
- **LAML** endpoints (`/laml/`) → Use REST API (`/api/calling/`, `/api/video/`)
- **CXML** (XML markup) → Use SWML (YAML/JSON)

This skill documents ONLY modern APIs: REST with JSON, SWML, Relay SDK, AI Agents SDK.

## SignalWire Technologies Quick Reference

| Technology | Use When | Format/Protocol |
|------------|----------|-----------------|
| **REST APIs** | Trigger actions from backend, query state | HTTP + JSON |
| **SWML** | Define call flows, IVR, AI interactions | YAML/JSON documents |
| **Relay SDK** | Real-time WebSocket control | JavaScript/Python |
| **AI Agents SDK** | Build voice AI agents | Python decorators |
| **Call Fabric** | Route between subscribers/resources | WebSocket framework |
| **SWAIG** | AI agent calls server-side functions | HTTP POST to your endpoint |

## Practical Knowledge from Production

This skill combines technical API documentation with practical implementation guidance from real-world SignalWire deployments. Each workflow file includes:

- **Best Practices** - Production-tested techniques and patterns
- **Common Patterns** - Real-world implementation examples
- **Anti-Patterns** - What NOT to do, mistakes to avoid
- **Production Tips** - Deployment, monitoring, and testing insights
- **Real-World Examples** - Complete working patterns from live applications

These insights come from analysis of 89 SignalWire training videos, LiveWire sessions, and production deployments.

## Workflows by Use Case

**Getting Started:**
- [Authentication & Setup](workflows/authentication-setup.md) | [Number Management](workflows/number-management.md)

**Voice Calls:**
- [Outbound Calling](workflows/outbound-calling.md) | [Inbound Handling](workflows/inbound-call-handling.md) | [Call Control](workflows/call-control.md)

**AI Voice Agents:** Start with [Voice AI](workflows/voice-ai.md) overview
- **SDK:** [Basics](workflows/ai-agent-sdk-basics.md) | [Prompting](workflows/ai-agent-prompting.md) | [Functions](workflows/ai-agent-functions.md) | [Deployment](workflows/ai-agent-deployment.md)
- **Best Practices:** [Patterns](workflows/ai-agent-patterns.md) | [Error Handling](workflows/ai-agent-error-handling.md) | [Security](workflows/ai-agent-security.md) | [Testing](workflows/ai-agent-testing.md) | [Debug Webhooks](workflows/ai-agent-debug-webhooks.md)

**Other:**
- [Messaging](workflows/messaging.md) | [Video](workflows/video.md) | [Fabric & Relay](workflows/fabric-relay.md) | [Webhooks & Events](workflows/webhooks-events.md)

## Quick Start Patterns

**Authentication:** HTTP Basic Auth with Project ID (username) + API Token (password)

**Space URL:** All API requests go to `https://{space-name}.signalwire.com`

**SWML Variables:** `%{call.from}`, `%{call.to}`, `%{params.custom_field}`, `%{args.user_input}`

**Webhooks:** HTTP POST with JSON (`call_id`, `call_state`, `from`, `to`, `direction`)

**Errors:** REST returns HTTP status + JSON with `error`/`message`. SWML logs to Dashboard.

## Key Concepts

**Call States:** queued → created → ringing → answered → ended

**SWML Sections:** `main` (required entry point) | `execute` (call + return) | `transfer` (goto)

**Resources:** Subscribers, AI Agents, SWML Scripts, Video Rooms, SIP Gateways, Relay Apps (created via Dashboard or REST API)

## Critical Pattern: Loop Protection

SWML gather/prompt nodes can infinite loop. Always add counters:

```yaml
- set:
    loop_counter: "{{loop_counter | default(0) | int + 1}}"
- condition:
    if: "{{loop_counter}} > 3"
    then: hangup  # Prevent caller stuck in loop
```

For complete patterns, see [Inbound Call Handling](workflows/inbound-call-handling.md).

## AI Agents SDK Reference

**IMPORTANT:** For AI agent tasks, start with [Voice AI](workflows/voice-ai.md) - it covers 90% of use cases with examples and best practices.

**Only load reference docs for:** Complete API parameters, advanced features (Contexts/Steps, Prefabs), platform-specific deployment (Lambda/GCF/Azure), or debugging production issues.

See [Voice AI workflow](workflows/voice-ai.md) "When to Pull Additional Documentation" section for detailed guidance on when to use each reference document.

## Finding the Right Workflow

**New to SignalWire?** → [Authentication & Setup](workflows/authentication-setup.md)

**Building AI voice agent?** → [Voice AI](workflows/voice-ai.md)

**Making/receiving calls?** → [Outbound Calling](workflows/outbound-calling.md) or [Inbound Handling](workflows/inbound-call-handling.md)

**Debugging webhooks/callbacks?** → [Webhooks & Events](workflows/webhooks-events.md)

**Need real-time control?** → [Fabric & Relay](workflows/fabric-relay.md)

## Additional Resources

- Main Documentation: https://developer.signalwire.com/
- GitHub Examples: https://github.com/signalwire
- AI Agents SDK: https://github.com/signalwire/signalwire-agents
- Dashboard: `https://{your-space-name}.signalwire.com`
