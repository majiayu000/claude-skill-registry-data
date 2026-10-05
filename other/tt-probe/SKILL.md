---
name: tt-probe
description: "E2E-проба конвейера fleet-skill-autonomy (создан на [машина флота] 2026-07-16 для verify #41ac669a). Не вызывать - это тестовый маркер, после верификации писатель может удалить."
permissions: [filesystem]
risk_level: inert
processes_untrusted_data: false
disable-model-invocation: true
origin: [машина флота]
version: 1.0.0
---

# tt-probe — маркер end-to-end промоушена

Единственная задача файла: пройти путь local-скилл → гейт → писатель (Маяк) → общий набор → синк на все машины.
Если ты читаешь это в `skills/tt-probe/` на любой машине флота — конвейер автономии скиллов РАБОТАЕТ.
Проба: PROBE-41ac669a-[id].


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
