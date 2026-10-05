---
name: memoria-de-caso-civel
description: "Mantem o estado append-only de um caso civel — partes, vara/comarca, numero, fase processual, pedidos, prazos, atos praticados, providencias e cronologia. Use quando o operador retomar um caso, perguntar onde paramos, pedir o status, a cronologia ou os prazos, ou quando o civel-master precisar carregar/atualizar o estado. Tambem ao iniciar caso novo."
---

# MEMORIA-DE-CASO-CIVEL

> Tier 0. Registro append-only do caso. O `civel-master` le no inicio e atualiza no fim de cada ato.

## Anexos obrigatorios (context/)
- `context/metodologia-civel.md` (fluxo processual).

## Objetivo
Nunca perder o fio do caso: partes, fase, prazos que vencem, atos praticados e proximo passo.

## Onde grava
`civel/casos/<slug-do-caso>.md` no diretorio de trabalho. Append-only: cada ato vira nova linha, nunca apaga o anterior.

## Estrutura do arquivo de caso
```markdown
# Caso: <titulo>
## Identificacao
- Partes: <autor> x <reu> | Polo do cliente: autor/reu
- Acao: <tipo> | Vara/Comarca: <...> | Processo: <numero CNJ>
- Valor da causa: R$ <...> | Gratuidade: sim/nao
## Fase processual
- <fase atual> (conhecimento/recursal/execucao/incidente)
## Prazos
- <data fatal> | <ato> | <fonte: intimacao/publicacao> | dias uteis
## Historico (append-only)
- <data> | <ato praticado> | <skill> | <resultado>
## Proximo passo
- <acao> ate <data>
```

## Metodologia
1. Ao iniciar: criar o arquivo com identificacao + fase + valor da causa.
2. A cada ato: **acrescentar** linha no Historico + atualizar Fase/Prazos/Proximo passo.
3. Nunca sobrescrever historico (auditabilidade).

## Entrega obrigatoria final
- Arquivo de caso criado/atualizado + resumo do estado (fase, proximo prazo, pendencias).

## Guard
Estado e fato, nao opiniao. Registrar numeros/prazos exatamente como constam na fonte (intimacao/publicacao); prazos em dias uteis — nao estimar datas sem o marco.
