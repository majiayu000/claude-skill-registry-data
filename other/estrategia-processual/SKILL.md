---
name: estrategia-processual
description: "Avalia riscos e oportunidades do caso civel e sugere os proximos passos processuais. Pondera probabilidade de exito, onus da prova, custos/beneficios de acordo x litigio, momento de tutela de urgencia, escolha de pedidos e de via (conhecimento x cumprimento), e calibra a postura. Use quando o operador disser qual a estrategia, vale a pena recorrer, devo fazer acordo, quais os riscos, proximo passo, ou pedir analise estrategica do caso."
---

# ESTRATEGIA-PROCESSUAL

> Camada 2 (gestao processual). Apoio de decisao. Acionada pelo `civel-master` em pontos de inflexao.

## Anexos obrigatorios (context/)
- `context/metodologia-civel.md` (fluxo e cross-links).
- `context/jurisprudencia-civel.md` (precedentes pertinentes a tese, sob demanda).

## Objetivo
Dar ao operador uma leitura honesta de riscos x oportunidades e um proximo passo recomendado, sem prometer resultado.

## Quando ativar
- Pontos de decisao: ajuizar ou notificar antes; pedir tutela ja; recorrer ou nao; aceitar acordo; cumular pedidos.

## Metodologia
1. **Mapear o caso** (via `memoria-de-caso-civel`): fase, pedidos, provas, posicao das partes.
2. **Probabilidade de exito:** confrontar tese com jurisprudencia verificada (so ✅/🟡 de `jurisprudencia-civel`, via `validador-civel`); evitar otimismo infundado.
3. **Onus da prova** (CPC 373) e quem suporta o risco.
4. **Custo x beneficio:** litigio x acordo; sucumbencia; tempo.
5. **Timing:** tutela de urgencia/evidencia agora? recurso vale o preparo/risco?
6. Recomendar o proximo passo + alternativas (2-3, no maximo).

## Entrega obrigatoria final
- Leitura de riscos/oportunidades + recomendacao de proximo passo + alternativas + gestao de expectativa (sem promessa de resultado — Codigo de Etica OAB).

## Guard
Honestidade: avisar divergencias jurisprudenciais (ex.: estabilizacao da tutela). Nenhuma estimativa de exito como certeza. Precedente so via `validador-civel`.
