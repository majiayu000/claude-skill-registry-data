---
name: 3x-ui-routing
description: Проектировать, настраивать, проверять и диагностировать Xray routing, DNS, geosite, geoip, direct/proxy/block outbounds, subscription outbounds, WARP rotation и balancers в 3X-UI. Использовать для split tunneling, multi-hop, блокировки private/BitTorrent, domainStrategy, geofiles и согласования с sing-box или Podkop.
---

# 3X-UI Routing

Работать только с инфраструктурой, которой пользователь вправе управлять. Считать routing server-side политикой Xray на VPS: она не заменяет правила на клиенте, OpenWrt, sing-box или Podkop.

## Рабочий процесс

1. Зафиксировать версии 3X-UI/Xray, текущие inbounds, outbounds, routing rules, DNS и geofiles.
2. Сохранить backup БД и экспорт Xray settings.
3. Сформулировать требуемый путь каждого класса трафика: `direct`, конкретный proxy/VPN outbound, balancer или `block`.
4. Проверить существование всех `inboundTag`, `outboundTag`, `balancerTag` и geosite/geoip списков.
5. Добавлять правила от частных к общим. Первое совпавшее routing rule определяет действие.
6. Для доменных правил выбрать `domainStrategy` осознанно; не включать IP resolution без необходимости.
7. После сохранения перезапустить Xray и проверить журнал, DNS и фактический внешний IP.

## Навигация

- Общая модель и `domainStrategy`: [references/routing.md](references/routing.md)
- Встроенный DNS Xray и DNS routing: [references/dns.md](references/dns.md)
- Доменные наборы: [references/geosite.md](references/geosite.md)
- IP-наборы: [references/geoip.md](references/geoip.md)
- Поля и порядок правил: [references/rules.md](references/rules.md)
- `direct` / `proxy` / `block`: [references/direct-proxy-block.md](references/direct-proxy-block.md)
- Balancers: [references/balancer.md](references/balancer.md)
- Subscription outbounds: [references/outbound-subscriptions.md](references/outbound-subscriptions.md)
- WARP и rotation: [references/warp.md](references/warp.md)
- Диагностика: [references/troubleshooting.md](references/troubleshooting.md)

## Обязательные проверки

```sh
x-ui status
x-ui restart-xray
journalctl -u x-ui -n 200 --no-pager
ss -lntup
```

Проверить:

- Xray принимает конфигурацию без `failed to load config`;
- теги в rules существуют;
- нужный домен разрешается ожидаемым DNS server;
- тестовый запрос выходит через ожидаемый public IP;
- block rule действительно блокирует, а не отправляет direct;
- после restart порядок rules и geofile aliases сохраняется.

## Правила безопасности

- Не отправлять private/metadata IP через внешний proxy без явной причины.
- Не публиковать proxy credentials, WARP keys, VPN configs и полный Xray JSON.
- Не создавать catch-all rule до правил панели/API, DNS и исключений.
- Если routing обслуживает CDN-публикованный transport или panel route, не предлагать obvious hostname/path вроде `vpn.*`, `proxy.*`, `ws.*`, `panel.*`, `admin.*`, `/ws`, `/vpn`, `/proxy`, `/vless`, `/xray`.
- Для HTTP/CDN-сценариев сохранять site-shaped hostname/path и разделять panel route от transport route.
- `outboundTag` и `balancerTag` не задавать одновременно: текущий UI предупреждает, что `outboundTag` получает приоритет.
- Не переносить `geosite:`/`geoip:` напрямую в sing-box 1.13: legacy databases и rule fields удалены, нужны rule-sets.
- Legacy WireGuard outbound sing-box удалён; использовать WireGuard endpoint.
- Remote outbound subscription считать недоверенным input: запретить private destinations по умолчанию и проверить tags до включения.
- Для Podkop настраивать client-side policy в Podkop отдельно; серверные rules 3X-UI не экспортируются в него автоматически.

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

Проверено 2026-06-12 по 3X-UI `v3.3.0`, repository commit `f8e89cc848b908d8507f30e0e35a0a74d6fe983c`, Wiki commit `264a7b202aacc0036a1fbb95a285d3e2981a3578`, bundled Xray-core `v26.6.1` и sing-box `v1.13.13`.
