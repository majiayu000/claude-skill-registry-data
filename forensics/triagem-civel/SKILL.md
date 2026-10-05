---
name: triagem-civel
description: "Classifica a demanda civel e roteia para a skill certa. Identifica a FASE PROCESSUAL (consulta, ajuizamento, conhecimento, recursal, execucao, incidente) e o OBJETIVO juridico, e indica a skill alvo + o foro competente. Use quando o operador descrever uma situacao civel e nao souber o caminho, ou disser triagem civel, qual o caminho, que peca eu uso, em que fase estou, /triagem-civel."
---

# TRIAGEM-CIVEL

> Tier 0. Porta de classificacao. Chamada pelo `civel-master` no inicio de todo caso.

## Anexos obrigatorios (context/)
- `context/metodologia-civel.md` (mapa de skills + fluxo).
- `context/recursos-tutelas-civel.md` (se a fase for recursal/tutela).

## Objetivo
Em poucas perguntas, dizer: fase processual + objetivo + skill alvo + (se aplicavel) foro/tribunal.

## Arvore de decisao
1. **Vai AJUIZAR (autor)?** -> gestao processual (competencia/foro, valor da causa, gratuidade) + a acao da Camada 5 conforme o objetivo: reparar dano -> `acao-indenizatoria`; compelir/impedir conduta -> `obrigacao-fazer-nao-fazer`; desfazer/revisar contrato -> `resolucao-rescisao-contratual`/`revisional-contratual`; cobrar sem titulo -> `cobranca-e-monitoria`; consignar -> `consignacao-em-pagamento`; declarar (in)existencia -> `acao-declaratoria`; vicio do negocio -> `anulatoria-negocio-juridico`; posse -> `possessorias`; propriedade por posse -> `usucapiao-judicial`; reaver coisa -> `reivindicatoria-petitoria`; contas -> `exigir-contas`; bem de terceiro constrito -> `embargos-de-terceiro`; desconstituir coisa julgada -> `acao-rescisoria`; perpetuar prova -> `producao-antecipada-de-provas`. Sem acao tipificada -> `peticao-inicial-civel`. Some `tutela-urgencia`/`tutela-evidencia` se houver.
2. **Foi CITADO (reu)?** -> `contestacao-civel` (+ `preliminares-civel`, `reconvencao` se cabivel; `revelia` se perdeu prazo).
3. **Esta no fluxo de CONHECIMENTO?** -> conforme o ato: `replica-civel`, `saneamento`, `producao-de-provas`, `audiencia-conciliacao-mediacao`, `audiencia-instrucao`, `razoes-finais-memoriais`, `resumo-de-ata`.
4. **Recebeu DECISAO/SENTENCA e quer recorrer?** -> escolher o recurso: interlocutoria do rol 1.015 -> `agravo-de-instrumento`; sentenca -> `apelacao-civel`; vicio (omissao/contradicao) -> `embargos-de-declaracao`; decisao monocratica -> `agravo-interno`; ultima instancia vs lei federal/CF -> `recursos-excepcionais`. Sempre `admissibilidade-e-tempestividade-recursal`.
5. **Cumprimento/execucao?** -> credor: `cumprimento-de-sentenca`; executado: `impugnacao-ao-cumprimento` (titulo judicial) ou `defesa-do-executado` (escolhe embargos/pre-executividade); constricao: `penhora-e-expropriacao`; atingir socio/fraude: `idpj-e-fraude-a-execucao`; devedor contumaz: `medidas-executivas-atipicas`. Maquina pesada de execucao -> cross-link `execucao-adv-os`.
6. **Incidente?** -> juiz parcial: `suspeicao-impedimento`; qual juizo: `conflito-de-competencia`; demandas repetitivas/tese: `irdr-iac`; exibicao de documento/falsidade: `incidentes-probatorios-e-exibicao` (IDPJ fica na Camada 7: `idpj-e-fraude-a-execucao`).

## Entrega obrigatoria final
- Fase + objetivo + skill alvo + foro/tribunal, em 3-5 linhas, e o handoff para o `civel-master`.

## Guard
Na duvida de competencia/foro, consultar `context/cpc-13105-15.md` (arts. 42-66) + `context/cpc-cc-alteracoes-recentes.md` (Lei 14.879/2024). Nao redigir peca aqui — so classificar e rotear.
