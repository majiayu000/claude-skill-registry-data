---
name: civel-master
description: "Orquestrador do plugin civel (Civil Litigation Master) e porta unica do contencioso civel. Recebe qualquer demanda em linguagem natural, identifica a fase processual e o objetivo, e DIRIME (seleciona e conduz) TODAS as skills pertinentes sem esquecer nenhuma, fechando pela suprema-corte-civel. Use quando o operador descrever uma tarefa civel sem chamar skill especifica, ou disser civel-master, novo caso civel, vou ajuizar, fui citado, recebi sentenca, quero recorrer, preciso da inicial, contestacao, replica, tutela, agravo, apelacao."
---

# CIVEL-MASTER — Orquestrador (Civil Litigation Master)

> Tier 0. Porta unica do plugin civel-adv-os. Dirige TODAS as skills necessarias por tarefa, sem esquecer nenhuma.

## Anexos obrigatorios (context/)
- `context/metodologia-civel.md` (mapa de uso, fluxo, regras de ouro) — **ler primeiro, sempre**.
- Demais anexos sob demanda (CPC/CC por grep do artigo; reformas; jurisprudencia; recursos/tutelas).

## Objetivo
Transformar qualquer demanda de contencioso civel em entrega correta e validada, conduzindo o ciclo sem perder o estado e sem esquecer nenhuma exigencia processual.

## Metodologia
1. **Ler** `context/metodologia-civel.md`.
2. **Classificar** via `triagem-civel` (fase processual + objetivo + skill alvo + foro).
3. **Carregar** `memoria-de-caso-civel` (partes, vara, fase, prazos, atos, providencias).
4. **Gestao processual SEMPRE (Camada 2):** antes/junto de qualquer peca, acionar `tempestividade-civel`, `gratuidade-e-impugnacao`, `competencia-e-foro`, `preliminares-civel`, `valor-da-causa` — e so entao a skill da fase. Esse e o "nao esquecer nada".
5. **Conduzir os desdobramentos** na ordem: inicial (ou acao especifica da Camada 5) -> (emenda) -> contestacao+preliminares -> replica -> saneamento -> provas -> audiencias -> razoes finais -> sentenca -> recursos (ED/agravo/apelacao/excepcionais) -> cumprimento de sentenca/execucao (defesa do executado, penhora, IDPJ, impugnacao) -> incidentes quando surgirem (suspeicao/impedimento, conflito de competencia, IRDR/IAC, exibicao/falsidade).
6. **Gate final:** toda entrega passa pela `suprema-corte-civel` (R1-R4).
7. **Atualizar** `memoria-de-caso-civel` (ato praticado, proximo passo, prazo).

## Regras de ouro
- Prazos em **dias uteis** (CPC 219); regra 15 dias; ED 5 dias; dobro por art. (Fazenda 183 / MP 180 / Defensoria 186 / litisconsortes 229 — nao em autos eletronicos).
- **Lei vigente:** CC/2002 (PL 4/2025 so monitorar) · CPC + Lei 14.879/2024 (foro) + Lei 14.939/2024 (feriado local) · EC 136 = precatorios (nao CPC).
- **Cross-link, nao duplicar:** execucao pesada -> execucao-adv-os; revisional bancaria -> bancario-adv-os; calculos -> calculosjudiciais-adv-os; familia -> direito-familia-adv-os.

## Entrega obrigatoria final
- Artefato da skill acionada, validado pela suprema-corte-civel + `memoria-de-caso-civel` atualizado + proximo passo/prazo.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Nunca produzir peca sem a gestao processual transversal. Na duvida de vigencia/existencia, bloquear e checar.
