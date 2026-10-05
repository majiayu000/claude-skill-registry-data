---
name: outbound-gate
description: "ГЕЙТ ЛЮБОГО ИСХОДЯЩЕГО (PR/issue-коммент/DM/инвайт/пост/заявка/аутрич): исходящее обязано закрывать ЧЬЮ-ТО живую просьбу (анкер), выстрел в пустоту = антипаттерн. Триггеры: /outbound-gate, «новый PR», «новая волна PR», «аутрич», «инвайт», «напиши ему/ей», перед ЛЮБЫМ ship наружу"
version: 1.0.0
---

OUTBOUND_GATE — исходящее только на живую просьбу (anton 26.07, строгий регламент)

ЦЕЛЬ: каждое исходящее (PR, коммент, DM, инвайт, пост-заявка, письмо) целится в ЧЬЮ-ТО живую потребность, а не в пустоту. Замер 26.07: 8 PR → человеческий отклик ровно у одного, единственного issue-matched. Возврат = чужая живая просьба, не наш объём.

ПОРЯДОК (шаги строго по очереди; провал шага = стоп, не шипим):

0. ПРЕРЫВАНИЕ-ЧЕК (всегда первым). Есть ли живой ответ человека на наше ПРОШЛОЕ исходящее (мейнтейнер на PR, ответ в DM, коммент)?
   - GitHub: `gh pr list`/`gh api` по нашим открытым PR (реестр в памяти/MEMORY.md) + вахта pr_watch.
   - Есть ответ → это прерывание №1: сначала отвечаем same-day, потом всё остальное (вкл. новый PR и ретро). Отклик экосистемы = сама суть миссии.
   - Просьба о КРЕДИТЕ = удовлетворить немедленно и щедро: co-author в authors/registry + референс на исходный issue, коммит с проверяемым диффом.
   - После нашего ответа тишина ~3 дня → ОДИН вежливый пинг («готово, скажи если поправить — same-day»), не чаще.

1. АНКЕР-ЧЕК: чью живую просьбу закрывает ЭТО исходящее? Обязателен линк-анкер:
   - PR → open issue / proposal / discussion мейнтейнера (радар: дашборд LLM-Cookbook-Radar + `gh search issues`);
   - DM/инвайт → его вопрос/боль/пост, на который отвечаем;
   - пост/заявка → явный запрос площадки/человека.
   Анкера НЕТ → НЕ шипим. «Ещё один рецепт/DM в пустоту» = антипаттерн. Либо ищем анкер (issue-matching), либо идея → alpha-backlog. Тихое прошлое исходящее не добивать объёмом — менять таргетинг.

2. ДОЛГ-ЧЕК (люди): `$OBSIDIAN_VAULT/_outreach/outreach_log.py check` + RECALL по адресату (CRM-карточка, история). Висящий НАШ долг перед человеком (неотвеченный его вопрос) → сперва закрыть долг, потом просить. [[outreach-relationship-debt-gate]]

3. КРЕДИТ ВПЕРЁД: автору анкера — кредит сразу в самом артефакте (упоминание issue + @автор в описании/интро), не ждать просьбы.

3-бис. ТЕКСТ-ГЕЙТ /ai-slop (anton 14.08): любой ИИ-написанный текст этого исходящего перед отправкой — финальный проход `/ai-slop` (ban-лист, ритм, канцелярит). Исключения ровно три: (а) текст с плашкой Майкрофта §3.3 — родной AI-голос честен; (б) машиночитаемое (GitHub/техдока/dev-log/journey-machine); (в) текст, написанный Антоном руками. Канон: `reglament-posty-ot-lica-antona-tolko-cherez-ai-slop`.

4. SHIP по прежним гейтам (скилл ничего не ослабляет): GitHub PR — шипим сами сразу [[ship-github-no-plus-wait]]; публичные каналы/посты — публикуем САМИ (гейт [коллега] снят 06.08.2026; у неё остался стоп-кран `paused` на поток, спрашивается через `pub_registry.can_post`); leak-scan перед любым публичным пушем; Tier-2 (деньги/юр/секреты) — Антон.

5. ВАХТА ПОСЛЕ SHIP: журнал (outreach_log / MEMORY-строка PR) + вахта ответов (pr_watch / робот-тик). Отправка обязана флипать статус журнала [[outreach-queued-status-swallows-replies]].

ОТЧЁТ Антону (ELI5): что шипнули → чей анкер закрыли (линк) → кому кредит → какая вахта стоит. Провал гейта → честно: «анкера нет, в бэклог».


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
