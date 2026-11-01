---
name: 3x-ui-security
description: "Проводить аудит и укрепление 3X-UI: credentials, API tokens, web base path, 2FA/TLS, panel/OpenAPI exposure, firewall, Fail2Ban/IP-limit, SSH hardening, databases, certificates, backups, subscription templates и remote outbound subscriptions."
---

# 3X-UI Security

Панель управляет Xray clients, ключами, подписками и базой. Компрометацию панели считать компрометацией всей proxy-инфраструктуры. README 3X-UI указывает personal-use scope; не превращать его в обещание enterprise security.

## Рабочий процесс

1. Снять инвентаризацию без вывода секретов: версия, bind/listen, panel port/path, TLS termination, firewall, SSH, DB backend, Docker/systemd.
2. Создать защищенный backup по [references/backups-security.md](references/backups-security.md).
3. Обеспечить второй канал доступа: активная SSH-сессия, console/VPS rescue.
4. Укреплять слоями:
   - panel exposure: [references/panel-security.md](references/panel-security.md)
   - credentials/2FA: [references/credentials.md](references/credentials.md)
   - TLS: [references/tls.md](references/tls.md)
   - firewall: [references/firewall.md](references/firewall.md)
   - Fail2Ban/IP-limit: [references/fail2ban.md](references/fail2ban.md)
   - SSH: [references/ssh-hardening.md](references/ssh-hardening.md)
5. После каждого слоя проверять новый доступ до закрытия старого.
6. При сбое идти по [references/troubleshooting.md](references/troubleshooting.md).

## Минимальный baseline

- уникальные username/password и 2FA;
- непредсказуемый web base path;
- HTTPS либо panel на loopback за SSH tunnel/reverse proxy;
- public firewall открывает только фактические SSH, reverse proxy и inbound ports;
- panel port ограничен admin IP/VPN или не опубликован;
- публичный hostname панели не выглядит как `panel.*` или `admin.*`; предпочтителен нейтральный hostname и hidden admin path;
- SSH keys, запрет password/root login после проверки;
- DB, private keys и backups доступны только владельцу;
- API tokens имеют минимальный жизненный цикл, хранятся как secrets и отзываются после использования;
- custom subscription template directory не writable недоверенными пользователями;
- remote outbound subscriptions не разрешают private destinations без явной причины;
- регулярные обновления после проверенного backup.

## Проверка

```sh
x-ui settings
ss -lntup
ufw status verbose
systemctl is-active x-ui
systemctl is-active fail2ban
ssh -G <host> | head
```

С внешней сети проверить HTTPS hostname/chain, недоступность лишних ports, отказ старых credentials и вход с 2FA.

## Ограничения

- Custom path уменьшает шум сканеров, но не заменяет authentication/firewall.
- Смена SSH port не заменяет keys и отключение password login.
- 3X-UI IP-limit/Fail2Ban защищает client sharing по access log; защита panel login требует отдельного контроля доступа/reverse proxy/WAF.
- Swagger/OpenAPI облегчает корректную автоматизацию, но также описывает attack surface; не публиковать panel API без authentication и network controls.
- MTProto secret, outbound subscription URLs и API tokens считать credentials.
- Не применять firewall/sshd restart без проверенного пути восстановления.

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

Проверено 2026-06-12 по 3X-UI `v3.3.0`, repository commit `f8e89cc848b908d8507f30e0e35a0a74d6fe983c`, Wiki commit `264a7b202aacc0036a1fbb95a285d3e2981a3578` и bundled Xray-core `v26.6.1`.
