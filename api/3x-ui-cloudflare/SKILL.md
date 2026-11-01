---
name: 3x-ui-cloudflare
description: Проектировать, настраивать и диагностировать интеграцию 3X-UI с Cloudflare DNS, standard Proxy/CDN, TLS modes, WebSocket, gRPC, XHTTP, Origin Rules, Origin CA, Spectrum и Cloudflare Tunnel. Использовать при публикации панели/подписок и ошибках 522/525/526.
---

# 3X-UI Cloudflare

Cloudflare Proxy — HTTP/HTTPS reverse proxy, а не универсальный Xray transport. Сначала определить protocol/transport, затем решать, может ли endpoint быть proxied.

## Матрица совместимости

| Схема | Standard Cloudflare Proxy |
|---|---|
| Panel/subscription HTTP(S) | Да |
| VLESS/Trojan over WebSocket + TLS | Да, при совпадении host/path |
| VLESS/Trojan over gRPC + TLS | Да, port 443, HTTP/2 и gRPC enabled |
| VLESS/Trojan raw TCP | Нет; DNS-only либо Spectrum |
| VLESS/Trojan + REALITY | Нет перед standard proxy; использовать DNS-only/direct |
| Hysteria2/UDP | Нет для standard proxy |
| Cloudflare Tunnel для panel | Да |
| XHTTP over TLS | HTTP-dependent; тестировать выбранный mode end-to-end |

XHTTP/HTTPUpgrade не считать автоматически эквивалентными WebSocket. Для XHTTP открыть [references/xhttp.md](references/xhttp.md).

## CDN Camouflage Rules

Treat every Cloudflare-published VPN transport as a site-first architecture.

### Site-first architecture

- Do not invent obvious public hostnames such as `vpn.*`, `proxy.*`, `ws.*`, `panel.*` or `admin.*`.
- Prefer neutral hostnames such as `assets.*`, `static.*`, `media.*`, `content.*` or `files.*`.
- Prefer site-shaped paths such as `/assets/js/runtime-v2.js`, `/static/js/chunk-main.js`, `/media/content/stream` or `/api/v1/content/sync`.
- Do not use transport-labeled paths such as `/ws`, `/vpn`, `/proxy`, `/vless` or `/xray`.
- If a real site exists, embed the proxied transport into its visible structure instead of isolating it on an obvious VPN hostname.

### Hidden panel guidance

- Keep the panel on a separate hidden admin path or a restricted admin-only route; do not normalize public `panel.*` publication.

### Origin IP exposure checks

- Before final output, verify Cloudflare Proxy, `Full (strict)`, Host/SNI alignment, panel separation, and that public DNS does not expose the origin IP unnecessarily.

### Anti-template checklist

- no `vpn.*`, `proxy.*`, `ws.*`, `panel.*`, `admin.*`
- no `/ws`, `/vpn`, `/proxy`, `/vless`, `/xray`
- site-shaped hostname/path preserved
- panel separated from transport path
- origin IP not leaked via public DNS

## Рабочий процесс

1. Зафиксировать hostname, DNS record, proxy status, origin IP/port, transport, TLS termination и certificate.
2. Выбрать архитектуру по [references/overview.md](references/overview.md).
3. Настроить DNS: [references/dns.md](references/dns.md).
4. Для CDN проверить ports/limits: [references/proxy-cdn.md](references/proxy-cdn.md).
5. Настроить `Full (strict)`: [references/tls-modes.md](references/tls-modes.md) и [references/certificates.md](references/certificates.md).
6. Настроить transport: [references/websockets.md](references/websockets.md) или [references/grpc.md](references/grpc.md).
7. При необходимости применить [references/origin-rules.md](references/origin-rules.md) или [references/tunnel.md](references/tunnel.md).
8. Ошибки разбирать по [references/troubleshooting.md](references/troubleshooting.md).

## Проверка

```sh
dig +short <hostname>
curl -I https://<hostname>/<path>/
openssl s_client -connect <origin-ip>:443 -servername <hostname> </dev/null
journalctl -u x-ui -n 200 --no-pager
```

Проверять отдельно DNS-only origin, Cloudflare edge, origin TLS и Xray transport. Не отключать TLS verification как постоянное исправление.

## Правила безопасности

- Рекомендовать `Full (strict)`, не `Flexible`.
- Cloudflare API Token ограничивать `Zone:DNS:Edit` и одной zone.
- Origin CA private key хранить только на origin с mode `0600`.
- Если origin предназначен только для proxied traffic, ограничить source Cloudflare IP ranges либо использовать Tunnel.
- REALITY private key и Xray client secrets не загружать в Cloudflare.
- Cache для subscription endpoint отключать либо задавать осознанный короткий TTL; для proxy transport paths cache должен быть bypass.
- Cloudflare Tunnel не считать универсальным raw TCP/UDP CDN для публичных Xray clients.
- Проверять, что Cloudflare-side hostname и path выглядят как часть сайта, а не как transport label.

## Обязательный аудит детекта

Перед выдачей финального решения обязательно использовать репозиторий:

- `nidox-vpn-detection-defense-skill`

Проверять:

- GeoIP
- ASN
- hosting
- IP reputation
- DNS
- маршрутизацию
- MTU
- Android признаки VPN
- iOS признаки VPN
- ложноположительные срабатывания
- ограничения методики

Использовать также:

- `references/required-skills.md`
- `references/final-report-template.md`
- `skill-entrypoint.md`

## Mandatory VPN Detection Audit

Before any final recommendation, deployment guide, troubleshooting procedure, architecture review, routing analysis or VPN assessment related to VPN, Proxy, VLESS, Reality, Xray, sing-box, Cloudflare, CDN, Podkop or OpenWrt, the assistant MUST invoke:

nidox-vpn-detection-defense-skill

The final answer MUST include:

Проверка на признаки детекта

## Актуальность

Проверено 2026-06-12 по 3X-UI `v3.3.0` и официальной Cloudflare Developers documentation. Cloudflare plans, ports, Origin Rules actions и product limits изменяемы; проверять перед внедрением.
