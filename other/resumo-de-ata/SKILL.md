---
name: resumo-de-ata
description: "Le a ata de audiencia (CPC 367 — termo da AIJ) ou a transcricao/gravacao e extrai de forma estruturada: deliberacoes do juiz, decisoes interlocutorias proferidas, prazos abertos, provas deferidas/indeferidas, designacoes futuras e providencias a cargo das partes. Alimenta cronologia-e-providencias e memoria-de-caso-civel. Use quando o operador disser resumo da ata, ler a ata, ata de audiencia, termo de audiencia, transcricao da audiencia, o que ficou definido na audiencia, ou colar o conteudo de uma ata para extrair prazos e providencias."
---

# RESUMO-DE-ATA

> Camada 4 (conhecimento/1o grau). Extrator pos-audiencia. Alimenta `cronologia-e-providencias` e `memoria-de-caso-civel`.

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — art. 367 (termo/ata da AIJ) + 1.009 §1 (interlocutoria nao agravavel impugnada na apelacao) — **grep + ler a faixa**.
- `context/metodologia-civel.md` (fluxo processual, p/ posicionar os proximos passos).

## Objetivo
Transformar a ata/transcricao bruta em um sumario acionavel: o que foi decidido, o que corre prazo e o que cada parte precisa fazer — sem perder nenhuma deliberacao.

## Quando ativar
- Apos AIJ/audiencia 334 — ha ata ou transcricao a processar.
- Operador colou o conteudo da ata e pede prazos/providencias.

## Metodologia
1. **Ler a ata/transcricao** integralmente e identificar a estrutura (presentes, conciliacao, provas colhidas, deliberacoes finais).
2. **Extrair deliberacoes:** decisoes interlocutorias proferidas em audiencia, deferimento/indeferimento de provas, homologacao de acordo, designacao de nova data, conversao em diligencia.
3. **Mapear prazos abertos:** memoriais (364 §2 — 15 dias sucessivos), juntada de documento, manifestacao, complementacao de pericia — cada um com seu termo. Cross-link `tempestividade-civel` para o calculo.
4. **Listar providencias por responsavel:** o que cabe ao cliente (documento, testemunha, pagamento de acordo) e o que cabe ao escritorio (peticao, recurso).
5. **Avaliar recorribilidade:** interlocutoria de audiencia — se nao do rol do 1.015, impugnavel na apelacao (1.009 §1); se do rol, prazo de agravo (cross-link recursos).
6. **Alimentar o estado:** repassar a `cronologia-e-providencias` (linha do tempo) e `memoria-de-caso-civel` (ato praticado + proximo passo + prazo).

## Entrega obrigatoria final
- Resumo estruturado da ata (deliberacoes + prazos com termo + providencias por responsavel + recorribilidade) + atualizacao de `cronologia-e-providencias` e `memoria-de-caso-civel`.

## Guard
Nao inventar deliberacao ausente da ata; na duvida sobre prazo/recorribilidade, marcar para conferencia. Entrega pela `suprema-corte-civel`.
