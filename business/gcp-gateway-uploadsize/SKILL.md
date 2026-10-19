---
name: gcp-gateway-uploadsize
description: GCP GKE Gateway upload size limit — Gateway API has no native client_max_body_size, enforcement at IIP/Kong/application layer. Use when designing file-upload paths in GKE Gateway 2.0 or answering upload-size questions.
---

# GCP Gateway Upload Size Limit

## Key Fact

GKE Gateway (Gateway API HTTPRoute) has **no native body-size filter**. HTTPRoute Filter types: RequestHeaderModifier, ResponseHeaderModifier, RequestRedirect, ResponseRedirect, URLRewrite, RequestMirror. No `client_max_body_size` equivalent.

## Enforcement Layers (correct to wrong)

1. **IIP nginx .so** — `client_max_body_size` (correct primary enforcement)
2. **Kong Gateway** — `request-size-limiting` plugin (if Kong is upstream)
3. **Application/pod** — application code or nginx sidecar
4. ~~GKE Gateway~~ — not possible, Gateway API does not support it
5. ~~Cloud Armor~~ — WAF rules, not precise upload control

## Layered Strategy

Set a loose upper bound at IIP (e.g., 500M) as a security guard, then precise business limits at Kong/Runtime (e.g., 10M per team/service).

## Reference

- Full analysis: `/Users/lex/git/knowledge/gateway/no-gateway/gke-gateway-uploadsize.md`
- Gateway API HTTPRoute spec: https://gateway-api.sigs.k8s.io/reference/api-types/httproute/#filters
- Kong `request-size-limiting`: https://docs.konghq.com/hub/kong-inc/request-size-limiting/
