---
name: 3x-ui-inbounds
description: "Проектировать, создавать, проверять и диагностировать inbounds актуального 3X-UI: VLESS, VMess, Trojan, Shadowsocks, WireGuard, Hysteria2, MTProto FakeTLS, HTTP, SOCKS/Mixed, Tunnel/Dokodemo-door и TUN; REALITY/XTLS Vision; TCP/Raw, mKCP, WebSocket, gRPC, HTTPUpgrade и XHTTP. Использовать при настройке server/client полей, UDP/QUIC, сертификатов, mtg sidecar, share links и совместимости с Xray, sing-box, v2rayNG, Shadowrocket и Podkop."
---

# 3X-UI Inbounds

Работать только с инфраструктурой, которой пользователь вправе управлять. Не обещать “неблокируемую” конфигурацию: фильтрация зависит от сети, адреса VPS, SNI, TLS fingerprint, транспорта и версии клиента.

## Рабочий процесс

1. Зафиксировать среду:
   - версия 3X-UI и bundled Xray-core;
   - ОС/провайдер VPS, IP, домен, CDN/reverse proxy;
   - сеть клиента и наблюдаемый тип блокировки;
   - клиент, версия и core: Xray, sing-box или другой;
   - нужен ли Podkop/OpenWrt, UDP, CDN, fallback или subscription.

2. Выбрать минимальную схему:
   - универсальный direct baseline: VLESS + TCP + REALITY + Vision;
   - сеть с потерями, где UDP/QUIC доступен: Hysteria2 + TLS;
   - TLS/reverse proxy/CDN: VLESS или Trojan + WS/HTTPUpgrade/gRPC/XHTTP;
   - Telegram-only proxy: MTProto FakeTLS через управляемый `mtg` sidecar;
   - простой legacy-compatible вариант: VLESS/Trojan + TCP + TLS;
   - Shadowsocks: только когда его client compatibility и простота важнее устойчивости VLESS/REALITY.

3. Проверить допустимость сочетания по текущему 3X-UI:
   - Vision: только VLESS, `network=tcp`, `security=tls|reality`;
   - REALITY: VLESS или Trojan; `tcp`, `grpc`, `xhttp` и legacy `http`;
   - REALITY не доступен в форме для `ws` и `httpupgrade`;
   - TLS: VMess/VLESS/Trojan/Shadowsocks на `tcp`, `ws`, `grpc`, `httpupgrade`, `xhttp`;
   - Hysteria2: protocol `hysteria`, dedicated network `hysteria`, обязательный TLS и UDP/QUIC;
   - VMess поддерживает stream transports и TLS, но не REALITY/Vision;
   - HTTP, Mixed, Tunnel, TUN и WireGuard имеют собственные settings и не используют обычный stream selector;
   - MTProto не обслуживается Xray: у него нет Xray clients/stream settings, а share link предназначен для Telegram;
   - актуальное имя SplitHTTP transport в панели: `xhttp`.

4. Открыть нужные references:
   - proxy-протоколы: [vless.md](references/vless.md), [vmess.md](references/vmess.md), [trojan.md](references/trojan.md), [shadowsocks.md](references/shadowsocks.md), [hysteria.md](references/hysteria.md), [mtproto.md](references/mtproto.md);
   - VPN/local inbounds: [wireguard.md](references/wireguard.md), [http-mixed.md](references/http-mixed.md), [tunnel.md](references/tunnel.md), [tun.md](references/tun.md);
   - security/flow: [reality.md](references/reality.md), [vision.md](references/vision.md);
   - transports: [tcp.md](references/tcp.md), [mkcp.md](references/mkcp.md), [websocket.md](references/websocket.md), [grpc.md](references/grpc.md), [httpupgrade.md](references/httpupgrade.md), [splithttp.md](references/splithttp.md);
   - выбор схемы: [comparison.md](references/comparison.md);
   - client matrix: [clients.md](references/clients.md);
   - общая диагностика: [troubleshooting.md](references/troubleshooting.md).

5. Перед изменением экспортировать DB/config и сохранить старую share link без секретов в отчете.

6. В панели создать inbound, добавить отдельного test client, сохранить, перезапустить Xray и проверить:
   ```sh
   x-ui status
   x-ui restart-xray
   journalctl -u x-ui -n 150 --no-pager
   ss -lntup
   ```

7. Импортировать ссылку/подписку в точную версию клиента. Сравнить UUID/password, address, port, `type`, `security`, `flow`, SNI, public key, short ID, path/host/serviceName/mode.

8. Тестировать отдельно DNS, TCP connect, TLS/REALITY handshake, HTTP path и фактический трафик. Не менять несколько полей одновременно.

## Совместимость

- **v2rayNG:** Xray-based; VLESS, REALITY, Vision и Xray transports зависят от bundled core и версии приложения. XHTTP требует актуальной версии.
- **sing-box 1.13:** поддерживает VLESS/`xtls-rprx-vision`, WS, gRPC и HTTPUpgrade. XHTTP не входит в официальную V2Ray transport schema. Legacy WireGuard outbound удалён; использовать WireGuard endpoint.
- **sing-box и Hysteria2:** использовать отдельный `type: hysteria2`; должны совпадать password, TLS SNI, Salamander и port-hopping fields.
- **Shadowrocket:** актуальные App Store release notes подтверждают VLESS/XTLS/REALITY и XHTTP, но XHTTP активно меняется; проверять конкретную версию и импортированные поля.
- **Podkop:** URL mode поддерживает VLESS, Shadowsocks, Trojan и Hysteria2, а также custom sing-box outbound. Для REALITY/Vision использовать VLESS URL или официальный custom outbound example. XHTTP считать неподтвержденным, пока его не поддерживает используемый sing-box/парсер Podkop.

## Правила конфигурации

- Не публиковать UUID, passwords, private keys, subscription URLs и Reality private key.
- Генерировать Reality keypair и short IDs средствами панели; клиент получает только public key и один short ID.
- Не использовать CDN перед REALITY: обычный CDN должен завершать TLS и несовместим с direct REALITY handshake.
- Для CDN/reverse proxy точно синхронизировать host/path/service name и protocol support.
- Для CDN-публикации использовать нейтральные hostname вроде `assets.*`, `static.*`, `media.*`, `content.*`, `files.*` и site-shaped paths вроде `/assets/js/runtime-v2.js`, `/static/js/chunk-main.js`, `/media/content/stream`, `/api/v1/content/sync`.
- Не генерировать очевидные hostname или paths вроде `vpn.*`, `proxy.*`, `ws.*`, `panel.*`, `admin.*`, `/ws`, `/vpn`, `/proxy`, `/vless`, `/xray`.
- Не включать `acceptProxyProtocol`, если upstream proxy реально не отправляет PROXY protocol.
- Не считать HTTP camouflage для Raw TCP эквивалентом TLS или REALITY.
- Для Podkop сначала пробовать минимальную VLESS REALITY Vision link; при unsupported link использовать custom sing-box outbound без XHTTP.
- Для Hysteria2 открывать именно UDP, проверять сертификат/SNI и не путать UDP listener с TCP на том же номере порта.
- Не включать Hysteria2 как единственный вариант, если целевая сеть полностью блокирует или стабильно режет UDP; держать TCP-based fallback.
- Не путать official Hysteria `v2.9.2` с Xray Hysteria transport: Gecko, Realms и расширенные QUIC/congestion fields могут отсутствовать в форме 3X-UI.
- Для MTProto использовать валидный FakeTLS domain и хранить `ee`-prefixed secret как credential.

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

## Критерии завершения

- Xray принимает config без ошибки;
- порт слушает нужный address;
- test client подключается из целевой сети;
- DNS и UDP работают в требуемом режиме;
- импорт не потерял security/flow/transport fields;
- после перезапуска настройки сохраняются;
- описан fallback с другим IP, transport или client core.

## Актуальность

База повторно проверена 2026-06-12:

- 3X-UI release `v3.3.0`, commit `f8e89cc848b908d8507f30e0e35a0a74d6fe983c`;
- Wiki commit `264a7b202aacc0036a1fbb95a285d3e2981a3578`;
- bundled Xray-core artifact `v26.6.1`, module revision `94ffd50060f1`;
- sing-box `v1.13.13`;
- Hysteria `v2.9.2`.

Клиентскую совместимость проверять заново перед применением.
