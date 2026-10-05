---
name: exigir-contas
description: "Redige a acao de exigir contas (CPC 550-553) em duas fases: 1a fase apura o DEVER de prestar contas (CPC 550 — citacao para prestar ou contestar em 15 dias; §5 condena o reu a prestar em 15 dias sob pena de nao impugnar as do autor); 2a fase julga as contas, apura o saldo e constitui titulo executivo judicial (CPC 552). Cabe contra quem administra bem ou interesse alheio. Use quando o operador disser prestar contas, exigir contas, acao de prestacao de contas, ou administrador nao presta contas."
---

# EXIGIR-CONTAS

> Camada 5 (acoes civeis). Acao bifasica para apurar o dever de prestar contas e o saldo. Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — arts. 550 (1a fase: dever de prestar; §1 razoes detalhadas; §4 revelia; §5 condenacao a prestar em 15 dias; §6 contas pelo autor), 551 (forma das contas), 552 (sentenca apura saldo e constitui titulo executivo), 553 (contas de administradores) — **grep + ler a faixa**.
- `context/cpc-cc-alteracoes-recentes.md` + `context/jurisprudencia-civel.md` (so ✅).

## Objetivo
Obter as contas de quem administra bem ou interesse alheio, vencer a 1a fase (dever de prestar) e chegar ao saldo apurado com titulo executivo (552), sem confundir as duas fases nem omitir as razoes detalhadas (550 §1).

## Quando ativar
- Ha quem administra bem/interesse alheio e nao presta contas (mandatario, gestor, administrador, depositario).
- Cliente quer apurar receitas, despesas e saldo de uma gestao.

## Metodologia
1. **Gestao processual SEMPRE (Camada 2) antes de redigir:** `competencia-e-foro` · `valor-da-causa` · `gratuidade-e-impugnacao` · `tempestividade-civel`.
2. **1a fase — dever de prestar (550):** citacao do reu para prestar contas ou contestar em 15 dias; na inicial, especificar detalhadamente as razoes que exigem as contas + documentos (§1). Revelia segue o art. 355 (§4).
3. **Sentenca da 1a fase (550 §5):** julgado procedente, condena o reu a prestar as contas em 15 dias, sob pena de nao lhe ser licito impugnar as que o autor apresentar; se nao prestar, o autor as apresenta (§6).
4. **Forma das contas (551):** especificar receitas, aplicacao das despesas e investimentos; impugnacao especifica e fundamentada com referencia ao lancamento questionado.
5. **2a fase — julgamento (552):** a sentenca apura o saldo e constitui titulo executivo judicial; pericia se necessario (550 §6).
6. **Administradores (553):** inventariante, tutor, curador, depositario e demais administradores prestam contas em apenso aos autos da nomeacao.

## Entrega obrigatoria final
- Peca redigida ponta a ponta (legitimidade + razoes detalhadas 550 §1 + pedido de prestar contas + apuracao de saldo) + checklist de documentos (prova da relacao de administracao) + indicacao da fase e foro/vara.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria. Entrega pela `suprema-corte-civel`. Cross-link, nao duplicar: execucao do saldo apurado -> `execucao-adv-os`; calculo do saldo -> `calculosjudiciais-adv-os`; contas de inventario (familia/sucessoes) fora do escopo.
