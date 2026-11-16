---
name: zero-trust-network-mesh
description: Implement Zero Trust networking for multi-agent swarms. mTLS mutual authentication, egress proxy whitelisting, DNS-over-HTTPS pinning, Ed25519 message signing, and network segmentation for agent clusters.
origin: NIST Zero Trust Architecture (SP 800-207), Cilium (Apache-2.0), WireGuard (GPLv2)
license: Apache-2.0
version: 1.0.0
compatibility: claude-sonnet-4-6, claude-opus-4-7
---

# Zero Trust Network Mesh

"Never trust, always verify" applied to inter-agent communication. Every packet is authenticated; every connection is authorized; no implicit trust based on network location.

## When to Use

- Securing communication between distributed agent nodes across hosts
- Preventing a compromised agent from pivoting to other agents via the network
- Auditing and controlling all outbound API traffic from agent processes
- Building a production-grade swarm where network isolation is critical

## Do NOT use for

- Single-host local agent setups where all agents run in the same process
- Development environments where rapid iteration matters more than isolation

## mTLS for Agent-to-Agent Communication

```bash
# Generate agent identity certificate (per-agent, ephemeral 24h TTL)
openssl ecparam -name prime256v1 -genkey -noout -out agent-42.key
openssl req -new -key agent-42.key \
  -subj "/CN=agent-42/O=yamtam-swarm" \
  -out agent-42.csr
openssl x509 -req -in agent-42.csr \
  -CA swarm-ca.crt -CAkey swarm-ca.key \
  -days 1 -out agent-42.crt

# Agent connects to Bus with mutual TLS
curl --cert agent-42.crt --key agent-42.key \
     --cacert swarm-ca.crt \
     https://swarm-bus.internal:8443/route
```

## Egress Proxy Whitelist

```nginx
# nginx egress proxy — only allow approved upstream hosts
server {
  listen 3128;
  resolver 127.0.0.1;

  # Allowlist
  location ~ ^/(api\.anthropic\.com|api\.openai\.com|registry\.npmjs\.org) {
    proxy_pass https://$host$request_uri;
  }

  # Block everything else
  location / {
    return 403 "EGRESS BLOCKED: host not in allowlist";
  }
}
```

## Ed25519 Bus Message Signing

```js
import { generateKeyPairSync, sign, verify } from 'crypto';

// Generate ephemeral agent keypair on startup
const { privateKey, publicKey } = generateKeyPairSync('ed25519');

// Sign outbound message
function signMessage(payload) {
  const data = Buffer.from(JSON.stringify(payload));
  return sign(null, data, privateKey).toString('hex');
}

// Verify inbound message
function verifyMessage(payload, sig, senderPublicKey) {
  const data = Buffer.from(JSON.stringify(payload));
  return verify(null, data, senderPublicKey, Buffer.from(sig, 'hex'));
}
```

## WireGuard Agent Tunnel

```bash
# Isolated VPN tunnel between two agent nodes
wg genkey | tee agent-a.key | wg pubkey > agent-a.pub
wg genkey | tee agent-b.key | wg pubkey > agent-b.pub

# /etc/wireguard/wg-swarm.conf on agent-a
[Interface]
Address = 10.99.0.1/24
PrivateKey = <agent-a.key>

[Peer]
PublicKey = <agent-b.pub>
AllowedIPs = 10.99.0.2/32
```

## DNS-over-HTTPS Pinning

```js
// Force all DNS resolution through DoH — prevent DNS spoofing
const DOH_ENDPOINT = 'https://cloudflare-dns.com/dns-query';

async function resolveHost(hostname) {
  const res = await fetch(`${DOH_ENDPOINT}?name=${hostname}&type=A`, {
    headers: { Accept: 'application/dns-json' }
  });
  const data = await res.json();
  return data.Answer?.[0]?.data;
}
```

## Anti-Fake-Pass Checklist

- [ ] mTLS: both client and server present certificates (mutual, not just server-side TLS)
- [ ] Certificate TTL ≤ 24 hours for agent identities
- [ ] Egress proxy tested: `curl https://evil.com` from agent → 403
- [ ] Ed25519 signature verified before processing any Bus message
- [ ] DNS resolution goes through DoH — not system resolver (`/etc/resolv.conf`)
