---
name: network-engineer
description: >
  Networking, DNS, proxies, firewalls, TLS/SSL, CDN y balanceo de carga.
  Diseño y troubleshooting de infraestructura de red.
  Trigger: Cuando necesitás configurar DNS, proxies, firewalls, certificados SSL, CDN, o debuggear problemas de red.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# Skill: network-engineer

Redes bien hechas. DNS, proxies, firewalls, TLS — la capa que nadie ve hasta que falla.

## Trigger

- Hay que configurar DNS para un dominio
- Necesitás un reverse proxy (Nginx, Caddy, Traefik)
- Un certificado SSL venció o hay que renovarlo
- Problemas de conectividad entre servicios
- Configurar firewall, CDN o load balancer

## Workflow LEND

1. ANALIZAR
   ├── Stack: Nginx, Caddy, Traefik, Cloudflare, AWS, HAProxy
   ├── Estado actual: ¿qué está funcionando? ¿qué no?
   ├── Requisitos: SSL, CDN, balanceo, WAF?
   └── Riesgo: ¿es producción? ¿hay downtime aceptable?

2. OFRECER (Menú del Senior)
   ├── A) Reverse proxy simple — Nginx/Caddy con SSL automático (acme.sh/certbot)
   ├── B) Stack completo — proxy + CDN (Cloudflare) + WAF + balanceo
   └── C) Mesh/infra moderna — Tailscale + Caddy + internal DNS

3. ELEGIR → confirmación

4. HACER
   ├── DNS: registrar A/AAAA/CNAME, TTL adecuado, propagación verificada
   ├── SSL: Let's Encrypt con certbot o acme.sh, renovación automática
   ├── Reverse proxy: Nginx/Caddy config, upstreams, headers, rate limiting
   ├── Firewall: iptables/nftables o security groups, mínimo privilegio
   ├── CDN: Cloudflare/CloudFront, caching, purging
   └── Load balancing: ALB/NLB/HAProxy, healthchecks, sticky sessions si aplica

5. VERIFICAR
   ├── DNS resuelve correctamente (dig +noshort)
   ├── SSL válido (curl -vI https://dominio)
   ├── Proxy responde (curl -H "Host: dominio" localhost)
   └── Firewall permite solo lo necesario (nmap desde afuera)
